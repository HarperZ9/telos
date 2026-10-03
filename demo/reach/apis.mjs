// Official API channels: documented endpoints that are free and keyless, or
// that take the user's own key from an environment variable. Each operation
// builds its URL from validated parameters, so the caller can name a channel
// and an operation but never an arbitrary URL. Keys travel in headers, never
// in a URL, so a receipt that records the URL records no secret.
import { parseFeed } from "./parse.mjs";

const str = (value, name, max = 256) => {
  const text = String(value ?? "").trim();
  if (!text || text.length > max) throw new Error(`${name} must be 1 to ${max} characters`);
  return text;
};
const int = (value, lo, hi, fallback) => Math.max(lo, Math.min(hi, Number.parseInt(value, 10) || fallback));
const slug = (value, name, pattern) => {
  const text = String(value ?? "");
  if (!pattern.test(text)) throw new Error(`invalid ${name}: ${value}`);
  return text;
};
const REPO = /^[A-Za-z0-9-]{1,39}\/[A-Za-z0-9._-]{1,100}$/;
const enc = encodeURIComponent;

export const API_CHANNELS = Object.freeze({
  hackernews: {
    base: "https://hacker-news.firebaseio.com/v0",
    ops: {
      top: () => ({ path: "/topstories.json" }),
      item: (p) => ({ path: `/item/${int(p.id, 1, 1e9, 1)}.json` }),
      user: (p) => ({ path: `/user/${slug(p.id, "user", /^[A-Za-z0-9_-]{2,15}$/)}.json` }),
    },
  },
  github: {
    base: "https://api.github.com",
    keyEnv: "GITHUB_TOKEN",
    keyOptional: true,
    auth: (key) => ({ authorization: `Bearer ${key}` }),
    headers: { accept: "application/vnd.github+json", "x-github-api-version": "2022-11-28" },
    ops: {
      repo: (p) => ({ path: `/repos/${slug(p.repo, "repo", REPO)}` }),
      issues: (p) => ({ path: `/repos/${slug(p.repo, "repo", REPO)}/issues?state=${p.state === "closed" ? "closed" : "open"}&per_page=${int(p.limit, 1, 100, 30)}` }),
      search_repos: (p) => ({ path: `/search/repositories?q=${enc(str(p.q, "q"))}&per_page=${int(p.limit, 1, 100, 10)}` }),
    },
  },
  v2ex: {
    base: "https://www.v2ex.com/api",
    ops: { hot: () => ({ path: "/topics/hot.json" }), latest: () => ({ path: "/topics/latest.json" }) },
  },
  wikipedia: {
    base: "https://en.wikipedia.org/api/rest_v1",
    ops: { summary: (p) => ({ path: `/page/summary/${enc(str(p.title, "title").replace(/ /g, "_"))}` }) },
  },
  arxiv: {
    base: "https://export.arxiv.org/api",
    crawlDelaySeconds: 3,
    format: "feed",
    ops: { search: (p) => ({ path: `/query?search_query=${enc(str(p.q, "q"))}&max_results=${int(p.limit, 1, 50, 10)}` }) },
  },
  youtube: {
    base: "https://www.googleapis.com/youtube/v3",
    keyEnv: "YOUTUBE_API_KEY",
    auth: (key) => ({ "x-goog-api-key": key }),
    ops: {
      search: (p) => ({ path: `/search?part=snippet&type=video&q=${enc(str(p.q, "q"))}&maxResults=${int(p.limit, 1, 50, 10)}` }),
      video: (p) => ({ path: `/videos?part=snippet,statistics,contentDetails&id=${slug(p.id, "video id", /^[A-Za-z0-9_-]{11}$/)}` }),
    },
  },
  brave: {
    base: "https://api.search.brave.com/res/v1",
    keyEnv: "BRAVE_SEARCH_API_KEY",
    auth: (key) => ({ "x-subscription-token": key }),
    headers: { accept: "application/json" },
    ops: { web: (p) => ({ path: `/web/search?q=${enc(str(p.q, "q", 400))}&count=${int(p.limit, 1, 20, 10)}` }) },
  },
});

function authHeaders(channel, env) {
  if (!channel.keyEnv) return {};
  const key = env[channel.keyEnv]?.trim();
  if (key) return channel.auth(key);
  if (channel.keyOptional) return {};
  throw new Error(`this channel needs ${channel.keyEnv} from your own account (see docs/REACH.md)`);
}

/** Resolve channel and operation to { url, headers } without any I/O. */
export function buildApiCall(channelName, op, params = {}, env = process.env) {
  const channel = API_CHANNELS[channelName];
  if (!channel) throw new Error(`unknown API channel ${channelName}; known: ${Object.keys(API_CHANNELS).join(", ")}`);
  const build = channel.ops[op];
  if (!build) throw new Error(`unknown operation ${op} for ${channelName}; known: ${Object.keys(channel.ops).join(", ")}`);
  const { path } = build(params ?? {});
  return { channel, url: `${channel.base}${path}`, headers: { ...(channel.headers ?? {}), ...authHeaders(channel, env) } };
}

/** Call one official API operation. Returns { data, record }. */
export async function callApi(http, channelName, op, params = {}, env = process.env) {
  const { channel, url, headers } = buildApiCall(channelName, op, params, env);
  if (channel.crawlDelaySeconds) http.limiter.setCrawlDelay(new URL(url).host, channel.crawlDelaySeconds);
  const result = await http.get(url, { headers });
  const record = { url, channel: channelName, at: new Date().toISOString(), status: result.status, robots: "not applicable: documented API", cache: result.cache ?? null, bytes: result.bytes, bytes_sha256: result.bytes_sha256 };
  if (result.status !== 200) return { data: null, error: `${channelName} returned ${result.status}`, record };
  const data = channel.format === "feed" ? parseFeed(result.body) : JSON.parse(result.body);
  const trimmed = channelName === "hackernews" && op === "top" && Array.isArray(data) ? data.slice(0, int(params.limit, 1, 500, 30)) : data;
  return { data: trimmed, record };
}
