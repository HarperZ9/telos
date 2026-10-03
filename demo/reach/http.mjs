// The one HTTP path every reach reader uses. It adds the honest User-Agent,
// paces each host, backs off on 429 and 503, serves and revalidates the cache,
// follows redirects only through a caller-supplied permission check, caps the
// body size, and hashes the bytes for the receipt. A bot check ends the read.
import { createHash } from "node:crypto";
import { ResponseCache } from "./cache.mjs";
import { userAgent } from "./identity.mjs";
import { HostLimiter, MAX_RETRIES, RETRY_STATUSES, parseRetryAfter } from "./limiter.mjs";

export const MAX_BODY_BYTES = 5 * 1024 * 1024;
export const TIMEOUT_MS = 20_000;
const MAX_REDIRECTS = 5;

const sha256 = (bytes) => createHash("sha256").update(bytes).digest("hex");

function headerObject(headers) {
  const out = {};
  for (const [key, value] of headers.entries()) out[key.toLowerCase()] = value;
  return out;
}

/**
 * A response that is a bot check rather than content. Telos reports it and
 * stops; it never tries to pass one.
 */
export function isBotCheck(status, headers, body) {
  if (headers["cf-mitigated"] === "challenge") return true;
  if (status !== 403 && status !== 429 && status !== 503) return false;
  return /captcha|are you a robot|verify you are human|challenge-platform/i.test(String(body).slice(0, 20_000));
}

async function readCapped(response) {
  const buffer = Buffer.from(await response.arrayBuffer());
  return buffer.length > MAX_BODY_BYTES ? { bytes: buffer.subarray(0, MAX_BODY_BYTES), truncated: true } : { bytes: buffer, truncated: false };
}

export class ReachHttp {
  constructor({ fetchImpl = globalThis.fetch, limiter = new HostLimiter(), cache = ResponseCache.fromEnv(), env = process.env } = {}) {
    this.fetchImpl = fetchImpl;
    this.limiter = limiter;
    this.cache = cache;
    this.env = env;
    this.calls = 0;
  }

  /** One request with pacing and retries. Returns a plain response object. */
  async request(url, { method = "GET", headers = {}, body = undefined } = {}) {
    const host = new URL(url).host;
    for (let attempt = 0; ; attempt += 1) {
      await this.limiter.acquire(host);
      this.calls += 1;
      const response = await this.fetchImpl(url, {
        method,
        body,
        redirect: "manual",
        headers: { "user-agent": userAgent(this.env), ...headers },
        signal: AbortSignal.timeout(TIMEOUT_MS),
      });
      const head = headerObject(response.headers);
      if (RETRY_STATUSES.has(response.status) && attempt < MAX_RETRIES) {
        await response.arrayBuffer().catch(() => null);
        await this.limiter.backoff(host, attempt, parseRetryAfter(head["retry-after"]));
        continue;
      }
      const { bytes, truncated } = await readCapped(response);
      return { url, status: response.status, headers: head, bytes, truncated, attempts: attempt + 1 };
    }
  }

  /**
   * GET with cache and redirects. `allow(url)` is awaited before every hop and
   * returns { allowed, reason }; a refused hop ends the read with status 0.
   */
  async get(url, { headers = {}, allow = async () => ({ allowed: true }) } = {}) {
    let target = url;
    for (let hop = 0; hop <= MAX_REDIRECTS; hop += 1) {
      const gate = await allow(target);
      if (!gate.allowed) return { url: target, status: 0, refused: gate.reason ?? "refused", headers: {}, body: "", bytes_sha256: null, bytes: 0 };
      let result;
      try {
        result = await this.getOne(target, headers);
      } catch (err) {
        return { url: target, status: 0, refused: `network error: ${err.message}`, headers: {}, body: "", bytes_sha256: null, bytes: 0 };
      }
      const location = result.headers.location;
      if (result.status >= 300 && result.status < 400 && location) {
        target = new URL(location, target).toString();
        continue;
      }
      return result;
    }
    return { url: target, status: 0, refused: "too many redirects", headers: {}, body: "", bytes_sha256: null, bytes: 0 };
  }

  // Requests that carry credentials skip the cache in both directions.
  async getOne(url, headers) {
    const authed = Object.keys(headers).some((k) => k.toLowerCase() === "authorization");
    const cached = authed ? null : this.cache.get(url);
    if (cached && this.cache.isFresh(cached)) return this.fromCache(cached, "fresh");
    const raw = await this.request(url, { headers: { ...this.cache.validators(cached), ...headers } });
    if (raw.status === 304 && cached) return this.fromCache(cached, "revalidated");
    const body = raw.bytes.toString("utf8");
    const out = {
      url,
      status: raw.status,
      headers: raw.headers,
      body,
      bytes: raw.bytes.length,
      bytes_sha256: sha256(raw.bytes),
      truncated: raw.truncated,
      attempts: raw.attempts,
      cache: "miss",
      bot_check: isBotCheck(raw.status, raw.headers, body),
    };
    if (!authed && !out.bot_check && !out.truncated) this.cache.put(url, { status: out.status, headers: out.headers, body });
    return out;
  }

  fromCache(entry, mode) {
    const bytes = Buffer.from(entry.body, "utf8");
    return { url: entry.url, status: entry.status, headers: entry.headers, body: entry.body, bytes: bytes.length, bytes_sha256: sha256(bytes), truncated: false, attempts: 0, cache: mode, bot_check: false };
  }
}
