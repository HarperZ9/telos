// Reddit and X readers against a fake network: official routes only, the
// user's own credentials from the environment, never a secret in a record.
import test from "node:test";
import assert from "node:assert/strict";
import { fakeHttp } from "./reach/fake-net.mjs";
import { API_BASE as REDDIT_API, RedditReader, TOKEN_URL, flattenComments, redditUserAgent } from "./reach/reddit.mjs";
import { OEMBED_URL, XReader, parsePostUrl } from "./reach/x.mjs";
import { buildApiCall, callApi } from "./reach/apis.mjs";

const CREDS = { REDDIT_CLIENT_ID: "abcdefgh12345", REDDIT_CLIENT_SECRET: "shh-value-123", REDDIT_USERNAME: "someone" };
const TOKEN = { body: JSON.stringify({ access_token: "tok-1", expires_in: 3600 }) };
const listing = (children) => JSON.stringify({ data: { after: "t3_z", children } });

test("Reddit without credentials explains the fix and touches no network", async () => {
  const { http, calls } = fakeHttp({});
  await assert.rejects(new RedditReader({ http, env: {} }).listing("rust"), /REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET/);
  assert.equal(calls.length, 0);
});

test("Reddit uses the app-only OAuth grant and the requested User-Agent form", async () => {
  const url = `${REDDIT_API}/r/rust/hot?limit=2&t=day&raw_json=1`;
  const { http, calls } = fakeHttp({ [TOKEN_URL]: TOKEN, [url]: { body: listing([{ kind: "t3", data: { id: "p1", title: "Hi", subreddit: "rust", permalink: "/r/rust/comments/p1/hi/" } }]) } }, { env: CREDS });
  const out = await new RedditReader({ http, env: CREDS }).listing("rust", { limit: 2 });
  assert.equal(calls[0].url, TOKEN_URL);
  assert.equal(calls[0].body, "grant_type=client_credentials");
  assert.equal(calls[0].headers.authorization, `Basic ${Buffer.from("abcdefgh12345:shh-value-123").toString("base64")}`);
  assert.equal(calls[1].headers.authorization, "Bearer tok-1");
  assert.match(calls[1].headers["user-agent"], /^node:telos-reach\.abcdefgh:\d+\.\d+\.\d+ \(by \/u\/someone\)$/);
  assert.equal(out.posts[0].permalink, "https://www.reddit.com/r/rust/comments/p1/hi/");
});

test("Reddit records hold no secret and no token", async () => {
  const url = `${REDDIT_API}/r/rust/new?limit=25&t=day&raw_json=1`;
  const { http } = fakeHttp({ [TOKEN_URL]: TOKEN, [url]: { body: listing([]) } });
  const reader = new RedditReader({ http, env: CREDS });
  await reader.listing("rust", { sort: "new" });
  const text = JSON.stringify(reader.records);
  assert.doesNotMatch(text, /shh-value-123|tok-1|abcdefgh12345/);
});

test("Reddit waits out its window when X-Ratelimit-Remaining hits zero", async () => {
  const url = `${REDDIT_API}/r/rust/hot?limit=25&t=day&raw_json=1`;
  const headers = { "x-ratelimit-remaining": "0", "x-ratelimit-reset": "42" };
  const { http, sleeps } = fakeHttp({ [TOKEN_URL]: TOKEN, [url]: { body: listing([]), headers } });
  await new RedditReader({ http, env: CREDS }).listing("rust");
  assert.ok(sleeps.includes(42_000));
  const calm = fakeHttp({ [TOKEN_URL]: TOKEN, [url]: { body: listing([]), headers: { "x-ratelimit-remaining": "50", "x-ratelimit-reset": "42" } } });
  await new RedditReader({ http: calm.http, env: CREDS }).listing("rust");
  assert.ok(!calm.sleeps.includes(42_000), "no wait while requests remain");
});

test("Reddit inputs are validated before any request", async () => {
  const { http, calls } = fakeHttp({});
  const reader = new RedditReader({ http, env: CREDS });
  await assert.rejects(reader.listing("../etc"), /not a subreddit/);
  await assert.rejects(reader.listing("rust", { sort: "best?x" }), /sort must be/);
  await assert.rejects(reader.comments("bad/id"), /not a Reddit post id/);
  assert.equal(calls.length, 0);
  assert.equal(redditUserAgent({ id: "x", username: null }, { REDDIT_USER_AGENT: "mine:1 (by /u/me)" }), "mine:1 (by /u/me)");
});

test("comment trees flatten depth-first with depth markers", () => {
  const tree = [{ kind: "t1", data: { id: "a", body: "top", replies: { data: { children: [{ kind: "t1", data: { id: "b", body: "reply", replies: "" } }] } } } }, { kind: "more", data: {} }];
  assert.deepEqual(flattenComments(tree).map((c) => [c.id, c.depth]), [["a", 0], ["b", 1]]);
});

test("X post URLs are checked: only x.com and twitter.com status links", () => {
  assert.equal(parsePostUrl("https://twitter.com/jack/status/20").id === undefined, false, "short ids are rejected below");
  assert.deepEqual(parsePostUrl("https://twitter.com/XDevelopers/status/1861111969639481848"), { username: "XDevelopers", id: "1861111969639481848", url: "https://x.com/XDevelopers/status/1861111969639481848" });
  for (const bad of ["https://evil.test/a/status/123456", "http://x.com/a/status/123456", "https://x.com/i/api/graphql/abc", "https://x.com/a"]) {
    assert.throws(() => parsePostUrl(bad), /not an X post URL/, bad);
  }
});

test("X oEmbed calls only the public embed endpoint and parses text and date", async () => {
  const post = "https://x.com/a/status/123456";
  const url = `${OEMBED_URL}?url=${encodeURIComponent(post)}&omit_script=true&dnt=true`;
  const html = '<blockquote class="twitter-tweet"><p lang="en">Hello &amp; welcome<br>line</p>&mdash; A (@a) <a href="x">May 1, 2026</a></blockquote>';
  const { http, calls } = fakeHttp({ [url]: { body: JSON.stringify({ author_name: "A", author_url: "https://x.com/a", html }) } });
  const out = await new XReader({ http, env: {} }).oembed(post);
  assert.equal(calls.length, 1);
  assert.equal(new URL(calls[0].url).host, "publish.x.com");
  assert.equal(calls[0].headers.cookie, undefined);
  assert.equal(out.text, "Hello & welcome\nline");
  assert.equal(out.date, "May 1, 2026");
  const gone = fakeHttp({ [url]: { status: 404 } });
  assert.equal((await new XReader({ http: gone.http, env: {} }).oembed(post)).available, false);
});

test("the X API needs the user's token, reports cost, and keeps the token out of records", async () => {
  const none = fakeHttp({});
  await assert.rejects(new XReader({ http: none.http, env: {} }).post("123456"), /X_BEARER_TOKEN/);
  assert.equal(none.calls.length, 0);
  const url = "https://api.x.com/2/tweets/123456?tweet.fields=created_at,author_id,public_metrics,lang,conversation_id";
  const env = { X_BEARER_TOKEN: "xtok-secret", X_API_COST_PER_READ_USD: "0.01" };
  const { http, calls } = fakeHttp({ [url]: { body: JSON.stringify({ data: { id: "123456", text: "t" } }) } });
  const reader = new XReader({ http, env });
  const out = await reader.post("123456");
  assert.equal(calls[0].headers.authorization, "Bearer xtok-secret");
  assert.deepEqual(out.cost, { reads: 1, usd_per_read: 0.01, usd_estimate: 0.01, note: "estimate; your X developer console is the bill of record" });
  assert.doesNotMatch(JSON.stringify(reader.records), /xtok-secret/);
});

test("official API calls take keys in headers, never in the URL", async () => {
  const call = buildApiCall("youtube", "search", { q: "robots" }, { YOUTUBE_API_KEY: "yt-key-9" });
  assert.doesNotMatch(call.url, /yt-key-9/);
  assert.equal(call.headers["x-goog-api-key"], "yt-key-9");
  assert.throws(() => buildApiCall("youtube", "search", { q: "x" }, {}), /YOUTUBE_API_KEY/);
  assert.throws(() => buildApiCall("github", "repo", { repo: "../../x" }, {}), /invalid repo/);
  assert.throws(() => buildApiCall("nope", "x"), /unknown API channel/);
  const { http } = fakeHttp({ "https://hacker-news.firebaseio.com/v0/topstories.json": { body: "[1,2,3,4]" } });
  const out = await callApi(http, "hackernews", "top", { limit: 2 }, {});
  assert.deepEqual(out.data, [1, 2]);
  assert.equal(out.record.robots, "not applicable: documented API");
});
