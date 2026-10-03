// Per-host pacing and backoff. One request at a time per host, spaced by the
// larger of the default interval and the site's Crawl-delay. A 429 or 503
// waits for Retry-After when the server sends it, otherwise doubles the wait,
// and gives up after a fixed number of retries instead of hammering.

export const DEFAULT_INTERVAL_MS = 1000;
export const MAX_BACKOFF_MS = 60_000;
export const MAX_RETRIES = 2;
export const RETRY_STATUSES = new Set([429, 503]);

const realSleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

/** Parse Retry-After as seconds or an HTTP date. Returns ms or null. */
export function parseRetryAfter(value, now = Date.now()) {
  if (value === null || value === undefined || value === "") return null;
  const seconds = Number(value);
  if (Number.isFinite(seconds) && seconds >= 0) return Math.round(seconds * 1000);
  const at = Date.parse(value);
  return Number.isFinite(at) ? Math.max(0, at - now) : null;
}

/** Backoff for attempt n (0-based): Retry-After if given, else 2^n seconds, capped. */
export function backoffMs(attempt, retryAfterMs) {
  const base = retryAfterMs ?? 1000 * 2 ** attempt;
  return Math.min(MAX_BACKOFF_MS, Math.max(0, base));
}

export class HostLimiter {
  constructor({ intervalMs = DEFAULT_INTERVAL_MS, now = () => Date.now(), sleep = realSleep } = {}) {
    this.intervalMs = intervalMs;
    this.now = now;
    this.sleep = sleep;
    this.next = new Map();
    this.delays = new Map();
    this.waits = [];
  }

  /** Record a site's Crawl-delay (seconds); it can only lengthen the interval. */
  setCrawlDelay(host, seconds) {
    if (Number.isFinite(seconds) && seconds > 0) this.delays.set(host, Math.round(seconds * 1000));
  }

  intervalFor(host) {
    return Math.max(this.intervalMs, this.delays.get(host) ?? 0);
  }

  /** Wait until this host may be called again, then reserve the next slot. */
  async acquire(host) {
    const due = this.next.get(host) ?? 0;
    const wait = Math.max(0, due - this.now());
    if (wait > 0) {
      this.waits.push({ host, ms: wait, reason: "pace" });
      await this.sleep(wait);
    }
    this.next.set(host, this.now() + this.intervalFor(host));
  }

  /** Push the host's next slot out after a 429 or 503. */
  async backoff(host, attempt, retryAfterMs) {
    const ms = backoffMs(attempt, retryAfterMs);
    this.waits.push({ host, ms, reason: "backoff" });
    this.next.set(host, this.now() + ms);
    await this.sleep(ms);
  }
}
