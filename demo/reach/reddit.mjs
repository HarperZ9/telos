// Reddit reader on the official Data API. It authenticates with the user's
// own Reddit app (REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET) through the
// application-only OAuth grant, sends the User-Agent format Reddit asks for,
// and paces itself from the X-Ratelimit headers Reddit returns. Read-only: it
// lists subreddits and reads posts and comments, and never posts or votes.
import { TELOS_VERSION } from "../version.mjs";

export const TOKEN_URL = "https://www.reddit.com/api/v1/access_token";
export const API_BASE = "https://oauth.reddit.com";
export const SORTS = new Set(["hot", "new", "top", "rising", "controversial"]);
export const TIMES = new Set(["hour", "day", "week", "month", "year", "all"]);
const SUBREDDIT = /^[A-Za-z0-9_]{2,21}$/;
const POST_ID = /^[a-z0-9]{4,10}$/i;

/** Credentials from the environment. Values never leave this module. */
export function redditCredentials(env = process.env) {
  const id = env.REDDIT_CLIENT_ID?.trim();
  const secret = env.REDDIT_CLIENT_SECRET?.trim();
  const username = env.REDDIT_USERNAME?.trim() || null;
  return id && secret ? { id, secret, username } : null;
}

/** Reddit's requested form: <platform>:<app id>:<version> (by /u/<username>). */
export function redditUserAgent(creds, env = process.env) {
  if (env.REDDIT_USER_AGENT?.trim()) return env.REDDIT_USER_AGENT.trim();
  const by = creds.username ? ` (by /u/${creds.username})` : "";
  return `node:telos-reach.${creds.id.slice(0, 8)}:${TELOS_VERSION}${by}`;
}

function normalizePost(child) {
  const d = child.data ?? {};
  return {
    id: d.id, subreddit: d.subreddit, title: d.title, author: d.author,
    score: d.score, comments: d.num_comments, created_utc: d.created_utc,
    url: d.url, permalink: d.permalink ? `https://www.reddit.com${d.permalink}` : null,
    text: typeof d.selftext === "string" ? d.selftext.slice(0, 4000) : "",
  };
}

/** Flatten a comment tree to a depth-first list with depth markers. */
export function flattenComments(children, depth = 0, out = []) {
  for (const child of children ?? []) {
    if (child.kind !== "t1") continue;
    const d = child.data;
    out.push({ id: d.id, author: d.author, score: d.score, depth, created_utc: d.created_utc, body: String(d.body ?? "").slice(0, 4000) });
    if (d.replies && typeof d.replies === "object") flattenComments(d.replies.data?.children, depth + 1, out);
  }
  return out;
}

export class RedditReader {
  constructor({ http, env = process.env }) {
    this.http = http;
    this.env = env;
    this.creds = redditCredentials(env);
    this.token = null;
    this.records = [];
  }

  requireCreds() {
    if (!this.creds) throw new Error("Reddit needs REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET from your own app at https://www.reddit.com/prefs/apps (see docs/REACH.md)");
    return this.creds;
  }

  async authorize() {
    if (this.token) return this.token;
    const creds = this.requireCreds();
    const basic = Buffer.from(`${creds.id}:${creds.secret}`).toString("base64");
    const raw = await this.http.request(TOKEN_URL, {
      method: "POST",
      headers: { authorization: `Basic ${basic}`, "content-type": "application/x-www-form-urlencoded", "user-agent": redditUserAgent(creds, this.env) },
      body: "grant_type=client_credentials",
    });
    this.records.push({ url: TOKEN_URL, channel: "reddit", at: new Date().toISOString(), status: raw.status, robots: null, bytes: 0, bytes_sha256: null, note: "token exchange; body not recorded" });
    const parsed = safeJson(raw.bytes.toString("utf8"));
    if (raw.status !== 200 || !parsed?.access_token) throw new Error(`Reddit token exchange failed with status ${raw.status}`);
    this.token = parsed.access_token;
    return this.token;
  }

  /** Wait out Reddit's window when the last response said none remain. */
  async pace(headers) {
    const remaining = Number(headers["x-ratelimit-remaining"]);
    const reset = Number(headers["x-ratelimit-reset"]);
    if (Number.isFinite(remaining) && remaining < 1 && Number.isFinite(reset) && reset > 0) {
      await this.http.limiter.backoff("oauth.reddit.com", 0, reset * 1000);
    }
  }

  async api(pathAndQuery) {
    const token = await this.authorize();
    const url = `${API_BASE}${pathAndQuery}`;
    const result = await this.http.get(url, { headers: { authorization: `Bearer ${token}`, "user-agent": redditUserAgent(this.creds, this.env) } });
    this.records.push({ url, channel: "reddit", at: new Date().toISOString(), status: result.status, robots: null, cache: result.cache, bytes: result.bytes, bytes_sha256: result.bytes_sha256, ratelimit_remaining: result.headers["x-ratelimit-remaining"] ?? null });
    await this.pace(result.headers);
    if (result.status !== 200) throw new Error(`Reddit API returned ${result.status} for ${pathAndQuery}`);
    return JSON.parse(result.body);
  }

  async listing(subreddit, { sort = "hot", limit = 25, time = "day" } = {}) {
    if (!SUBREDDIT.test(String(subreddit))) throw new Error(`not a subreddit name: ${subreddit}`);
    if (!SORTS.has(sort)) throw new Error(`sort must be one of ${[...SORTS].join(", ")}`);
    if (!TIMES.has(time)) throw new Error(`time must be one of ${[...TIMES].join(", ")}`);
    const n = Math.max(1, Math.min(100, Number(limit) || 25));
    const data = await this.api(`/r/${subreddit}/${sort}?limit=${n}&t=${time}&raw_json=1`);
    return { subreddit, sort, posts: (data.data?.children ?? []).map(normalizePost), after: data.data?.after ?? null };
  }

  async comments(postId, { depth = 3, limit = 100 } = {}) {
    const id = String(postId).replace(/^t3_/, "");
    if (!POST_ID.test(id)) throw new Error(`not a Reddit post id: ${postId}`);
    const d = Math.max(1, Math.min(10, Number(depth) || 3));
    const n = Math.max(1, Math.min(500, Number(limit) || 100));
    const data = await this.api(`/comments/${id}?depth=${d}&limit=${n}&raw_json=1`);
    const post = data?.[0]?.data?.children?.[0];
    return { post: post ? normalizePost(post) : null, comments: flattenComments(data?.[1]?.data?.children) };
  }
}

function safeJson(text) {
  try {
    return JSON.parse(text);
  } catch {
    return null;
  }
}
