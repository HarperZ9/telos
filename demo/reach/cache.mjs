// Response cache. In memory by default, so a run that is not asked to persist
// writes nothing. TELOS_REACH_CACHE_DIR turns on a directory cache the user
// owns. Entries keep ETag and Last-Modified so a repeat read can be a cheap
// conditional request; fresh entries inside max-age skip the network.
import { createHash } from "node:crypto";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";

export const DEFAULT_TTL_MS = 15 * 60 * 1000;

const keyOf = (url) => createHash("sha256").update(url).digest("hex");

/** max-age from Cache-Control in ms, 0 for no-store/no-cache, else null. */
export function maxAgeMs(cacheControl) {
  const value = String(cacheControl ?? "").toLowerCase();
  if (/no-store|no-cache|private/.test(value)) return 0;
  const match = value.match(/max-age=(\d+)/);
  return match ? Number(match[1]) * 1000 : null;
}

export class ResponseCache {
  constructor({ dir = null, now = () => Date.now(), ttlMs = DEFAULT_TTL_MS } = {}) {
    this.dir = dir;
    this.now = now;
    this.ttlMs = ttlMs;
    this.memory = new Map();
  }

  static fromEnv(env = process.env, options = {}) {
    const dir = typeof env.TELOS_REACH_CACHE_DIR === "string" && env.TELOS_REACH_CACHE_DIR ? env.TELOS_REACH_CACHE_DIR : null;
    return new ResponseCache({ ...options, dir });
  }

  get(url) {
    const key = keyOf(url);
    if (this.memory.has(key)) return this.memory.get(key);
    if (!this.dir) return null;
    try {
      const entry = JSON.parse(readFileSync(path.join(this.dir, `${key}.json`), "utf8"));
      this.memory.set(key, entry);
      return entry;
    } catch {
      return null;
    }
  }

  isFresh(entry) {
    return Boolean(entry) && this.now() < entry.expiresAt;
  }

  /** Store a 200 response unless the server forbids caching. */
  put(url, { status, headers, body }) {
    const lifetime = maxAgeMs(headers["cache-control"]);
    if (status !== 200 || lifetime === 0) return null;
    const entry = {
      url,
      status,
      headers,
      body,
      etag: headers.etag ?? null,
      lastModified: headers["last-modified"] ?? null,
      storedAt: this.now(),
      expiresAt: this.now() + (lifetime ?? this.ttlMs),
    };
    const key = keyOf(url);
    this.memory.set(key, entry);
    if (this.dir) {
      mkdirSync(this.dir, { recursive: true });
      writeFileSync(path.join(this.dir, `${key}.json`), JSON.stringify(entry));
    }
    return entry;
  }

  /** Conditional request headers for a stale entry. */
  validators(entry) {
    const out = {};
    if (entry?.etag) out["if-none-match"] = entry.etag;
    if (entry?.lastModified) out["if-modified-since"] = entry.lastModified;
    return out;
  }
}
