// X readers on permitted routes only.
//
// 1. oEmbed: X's public embed endpoint returns the text, author and date of
//    one public post from its URL. Keyless and free; one post per call.
// 2. The official X API v2 with the user's own bearer token (X_BEARER_TOKEN).
//    X bills reads, so each call reports an estimated cost.
// 3. Pages the user opens and signs into personally are read through the
//    native-control browser verbs under a grant; that path lives there.
//
// There is no code here for private web endpoints, guest tokens, automated
// logins, session cookies or page scraping. Bulk search and timelines without
// a paid key have no permitted route, and the reach doctor says so.

export const OEMBED_URL = "https://publish.x.com/oembed";
export const API_BASE = "https://api.x.com/2";
const POST_HOSTS = new Set(["x.com", "www.x.com", "mobile.x.com", "twitter.com", "www.twitter.com", "mobile.twitter.com"]);
const POST_PATH = /^\/([A-Za-z0-9_]{1,15})\/status(?:es)?\/(\d{1,25})\/?$/;
const NUMERIC_ID = /^\d{1,25}$/;
const USERNAME = /^[A-Za-z0-9_]{1,15}$/;
// Pay-per-use read price as reported in early 2026; override with
// X_API_COST_PER_READ_USD. Your X developer console is the bill of record.
export const DEFAULT_COST_PER_READ_USD = 0.005;
const FIELDS = "tweet.fields=created_at,author_id,public_metrics,lang,conversation_id";

/** Validate a post URL and return { username, id, url }. */
export function parsePostUrl(input) {
  let url;
  try {
    url = new URL(input);
  } catch {
    throw new Error(`not a URL: ${input}`);
  }
  const match = url.pathname.match(POST_PATH);
  if (url.protocol !== "https:" || !POST_HOSTS.has(url.hostname.toLowerCase()) || !match) {
    throw new Error(`not an X post URL (https://x.com/<user>/status/<id>): ${input}`);
  }
  return { username: match[1], id: match[2], url: `https://x.com/${match[1]}/status/${match[2]}` };
}

/** Text and date from oEmbed's blockquote HTML. */
export function oembedText(html) {
  const para = String(html ?? "").match(/<p[^>]*>([\s\S]*?)<\/p>/i)?.[1] ?? "";
  const text = para.replace(/<br\s*\/?>/gi, "\n").replace(/<[^>]+>/g, "").replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&quot;/g, '"').replace(/&#39;/g, "'").trim();
  const anchors = [...String(html ?? "").matchAll(/<a[^>]*>([^<]*)<\/a>/gi)].map((m) => m[1]);
  return { text, date: anchors.at(-1) ?? null };
}

export function costPerRead(env = process.env) {
  const value = Number(env.X_API_COST_PER_READ_USD);
  return Number.isFinite(value) && value >= 0 ? value : DEFAULT_COST_PER_READ_USD;
}

export class XReader {
  constructor({ http, env = process.env }) {
    this.http = http;
    this.env = env;
    this.records = [];
  }

  record(url, result, extra = {}) {
    this.records.push({ url, channel: "x", at: new Date().toISOString(), status: result.status, robots: null, cache: result.cache ?? null, bytes: result.bytes, bytes_sha256: result.bytes_sha256, ...extra });
  }

  /** Read one public post through oEmbed. */
  async oembed(postUrl) {
    const post = parsePostUrl(postUrl);
    const url = `${OEMBED_URL}?url=${encodeURIComponent(post.url)}&omit_script=true&dnt=true`;
    const result = await this.http.get(url);
    this.record(url, result, { route: "oembed" });
    if (result.status === 404) return { ...post, available: false, reason: "post is deleted, private or not embeddable" };
    if (result.status !== 200) throw new Error(`X oEmbed returned ${result.status}`);
    const data = JSON.parse(result.body);
    return { ...post, available: true, author_name: data.author_name, author_url: data.author_url, ...oembedText(data.html) };
  }

  requireToken() {
    const token = this.env.X_BEARER_TOKEN?.trim();
    if (!token) throw new Error("the X API needs X_BEARER_TOKEN from your own X developer app; X bills reads per call (see docs/REACH.md)");
    return token;
  }

  async api(pathAndQuery) {
    const token = this.requireToken();
    const url = `${API_BASE}${pathAndQuery}`;
    const result = await this.http.get(url, { headers: { authorization: `Bearer ${token}` } });
    this.record(url, result, { route: "api", ratelimit_remaining: result.headers["x-rate-limit-remaining"] ?? null });
    if (result.status === 402 || result.status === 403) throw new Error(`X API refused with ${result.status}: your plan or credit balance does not cover this endpoint`);
    if (result.status !== 200) throw new Error(`X API returned ${result.status}`);
    return JSON.parse(result.body);
  }

  withCost(data, op) {
    const posts = Array.isArray(data.data) ? data.data.length : data.data ? 1 : 0;
    const rate = costPerRead(this.env);
    return { op, data: data.data ?? null, includes: data.includes ?? null, meta: data.meta ?? null, cost: { reads: posts, usd_per_read: rate, usd_estimate: Number((posts * rate).toFixed(4)), note: "estimate; your X developer console is the bill of record" } };
  }

  async post(id) {
    if (!NUMERIC_ID.test(String(id))) throw new Error(`not an X post id: ${id}`);
    return this.withCost(await this.api(`/tweets/${id}?${FIELDS}`), "post");
  }

  async searchRecent(query, { max = 10 } = {}) {
    const q = String(query ?? "").trim();
    if (!q || q.length > 512) throw new Error("search query must be 1 to 512 characters");
    const n = Math.max(10, Math.min(100, Number(max) || 10));
    return this.withCost(await this.api(`/tweets/search/recent?query=${encodeURIComponent(q)}&max_results=${n}&${FIELDS}`), "search_recent");
  }

  async userPosts(username, { max = 10 } = {}) {
    if (!USERNAME.test(String(username))) throw new Error(`not an X username: ${username}`);
    const user = await this.api(`/users/by/username/${username}`);
    const id = user.data?.id;
    if (!id) throw new Error(`no X user ${username}`);
    const n = Math.max(5, Math.min(100, Number(max) || 10));
    return this.withCost(await this.api(`/users/${id}/tweets?max_results=${n}&${FIELDS}`), "user_posts");
  }
}
