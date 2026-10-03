// The general web crawler. It asks robots.txt before every URL (redirect hops
// included), honors Crawl-delay through the host limiter, prefers feeds and
// sitemaps over link-walking, dedupes URLs, and returns a record per fetch.
// Budgets are hard caps so one call cannot turn into a site mirror.
import { ReachHttp } from "./http.mjs";
import { ROBOTS_TOKEN } from "./identity.mjs";
import { isFeed, parseFeed, parseHtml, parseSitemap } from "./parse.mjs";
import { fetchRecord } from "./receipt.mjs";
import { decide, robotsFromStatus } from "./robots.mjs";

export const MAX_DEPTH = 3;
export const MAX_PAGES = 50;
export const MAX_TEXT_CHARS = 20_000;

/** Canonical form for dedupe: no fragment, lowercase host, no default port. */
export function normalizeUrl(input) {
  const url = new URL(input);
  url.hash = "";
  if ((url.protocol === "https:" && url.port === "443") || (url.protocol === "http:" && url.port === "80")) url.port = "";
  return url.toString();
}

export function assertWebUrl(input) {
  let url;
  try {
    url = new URL(input);
  } catch {
    throw new Error(`not a URL: ${input}`);
  }
  if (url.protocol !== "http:" && url.protocol !== "https:") throw new Error(`only http and https are read: ${input}`);
  return url;
}

function classify(result) {
  const type = String(result.headers["content-type"] ?? "").toLowerCase();
  const body = result.body;
  if (type.includes("json")) {
    try {
      return { kind: "json", data: JSON.parse(body) };
    } catch {
      return { kind: "text", text: body.slice(0, MAX_TEXT_CHARS) };
    }
  }
  if (isFeed(body)) return { kind: "feed", ...parseFeed(body) };
  if (/<(urlset|sitemapindex)[\s>]/i.test(body.slice(0, 2000))) return { kind: "sitemap", ...parseSitemap(body) };
  if (type.includes("html") || /<html[\s>]/i.test(body.slice(0, 2000))) {
    const page = parseHtml(body, result.url);
    return { kind: "html", ...page, text: page.text.slice(0, MAX_TEXT_CHARS) };
  }
  return { kind: "text", text: body.slice(0, MAX_TEXT_CHARS) };
}

export class Crawler {
  constructor({ http = new ReachHttp(), token = ROBOTS_TOKEN } = {}) {
    this.http = http;
    this.token = token;
    this.robots = new Map();
    this.records = [];
    this.decisions = new Map();
  }

  async robotsFor(origin) {
    if (this.robots.has(origin)) return this.robots.get(origin);
    const url = `${origin}/robots.txt`;
    let result;
    try {
      result = await this.http.get(url);
    } catch (err) {
      result = { url, status: 0, headers: {}, body: "", refused: `unreachable: ${err.message}` };
    }
    const policy = robotsFromStatus(result.status, result.body);
    this.records.push(fetchRecord(result, { robots: policy.basis, channel: "robots" }));
    this.robots.set(origin, policy);
    return policy;
  }

  /** Robots decision for one URL; also feeds Crawl-delay to the limiter. */
  async permit(target) {
    const url = new URL(target);
    const policy = await this.robotsFor(url.origin);
    const verdict = decide(policy.parsed, this.token, `${url.pathname}${url.search}`);
    if (verdict.crawlDelay) this.http.limiter.setCrawlDelay(url.host, verdict.crawlDelay);
    const note = `${verdict.allowed ? "allowed" : "disallowed"} (${verdict.rule ?? policy.basis})`;
    this.decisions.set(normalizeUrl(target), note);
    return { allowed: verdict.allowed, reason: `robots.txt ${note}` };
  }

  /** Fetch and parse one URL. Returns { url, status, page } and logs a record. */
  async fetchPage(input) {
    const start = normalizeUrl(assertWebUrl(input).toString());
    const result = await this.http.get(start, { allow: (u) => this.permit(u) });
    const robots = this.decisions.get(normalizeUrl(result.url)) ?? this.decisions.get(start) ?? null;
    this.records.push(fetchRecord(result, { robots }));
    if (result.refused) return { url: result.url, status: 0, refused: result.refused, page: null };
    if (result.bot_check) return { url: result.url, status: result.status, stopped: "bot check: Telos stops here and does not try to pass it", page: null };
    if (result.status < 200 || result.status >= 300) return { url: result.url, status: result.status, page: null };
    return { url: result.url, status: result.status, page: classify(result) };
  }

  /** Seed URLs in preference order: sitemaps from robots.txt, then the start page. */
  async seeds(start) {
    const policy = await this.robotsFor(new URL(start).origin);
    return [...policy.parsed.sitemaps.slice(0, 3), start];
  }

  /**
   * Breadth-first crawl inside one site. Feeds and sitemaps found on the way
   * are read before ordinary links, and every page counts against the budget.
   */
  async crawlSite(input, { depth = 1, pageBudget = 10, sameHost = true } = {}) {
    const start = normalizeUrl(assertWebUrl(input).toString());
    const maxDepth = Math.max(0, Math.min(MAX_DEPTH, Number(depth) || 0));
    const budget = Math.max(1, Math.min(MAX_PAGES, Number(pageBudget) || 1));
    const host = new URL(start).host;
    const seen = new Set();
    const queue = (await this.seeds(start)).map((url) => ({ url, depth: 0 }));
    const pages = [];
    while (queue.length && pages.length < budget) {
      const next = queue.shift();
      const key = normalizeUrl(next.url);
      if (seen.has(key) || (sameHost && new URL(key).host !== host)) continue;
      seen.add(key);
      const got = await this.fetchPage(key);
      pages.push(summarize(got));
      if (next.depth < maxDepth && got.page) enqueue(queue, got.page, next.depth + 1);
    }
    return { start, depth: maxDepth, page_budget: budget, pages, unvisited: queue.length };
  }
}

function enqueue(queue, page, depth) {
  const preferred = [...(page.feeds ?? []), ...(page.kind === "sitemap" ? page.urls : [])];
  const ordinary = page.kind === "feed" ? page.items.map((i) => i.link).filter(Boolean) : page.links ?? [];
  queue.unshift(...preferred.map((url) => ({ url, depth })));
  queue.push(...ordinary.map((url) => ({ url, depth })));
}

function summarize(got) {
  if (!got.page) return { url: got.url, status: got.status, refused: got.refused ?? null, stopped: got.stopped ?? null };
  const { kind, title = null } = got.page;
  const text = got.page.text ? got.page.text.slice(0, 2000) : null;
  const items = got.page.items ? got.page.items.slice(0, 20) : undefined;
  return { url: got.url, status: got.status, kind, title, text, items, links: got.page.links?.length ?? 0 };
}
