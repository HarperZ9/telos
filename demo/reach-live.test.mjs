// One live smoke call per channel that has a public, keyless endpoint. Off by
// default so CI never depends on third-party uptime; run with
// TELOS_REACH_LIVE=1 to check the real endpoints. Reddit, the X API, YouTube
// and Brave need the user's own credentials and have no smoke here.
import test from "node:test";
import assert from "node:assert/strict";
import { runReach } from "./reach/run.mjs";

const live = process.env.TELOS_REACH_LIVE === "1";
const opts = { skip: live ? false : "set TELOS_REACH_LIVE=1 to run live smokes", timeout: 60_000 };
const deps = { env: { ...process.env, TELOS_REACH_CACHE_DIR: "" } };

test("live web: example.com through robots and the crawler", opts, async () => {
  const out = await runReach("fetch", { url: "https://example.com/" }, deps);
  assert.equal(out.result.status, 200);
  assert.match(out.result.page.title, /Example Domain/);
  assert.equal(out.receipt.fetches[0].channel, "robots");
});

test("live X oEmbed: one public post", opts, async () => {
  const out = await runReach("x-oembed", { url: "https://x.com/XDevelopers/status/1861111969639481848" }, deps);
  assert.equal(out.result.available, true);
  assert.equal(out.result.author_url, "https://x.com/XDevelopers");
});

for (const [channel, op, params, check] of [
  ["hackernews", "item", { id: 8863 }, (d) => d.id === 8863],
  ["github", "repo", { repo: "HarperZ9/telos" }, (d) => d.full_name === "HarperZ9/telos"],
  ["v2ex", "hot", {}, (d) => Array.isArray(d)],
  ["wikipedia", "summary", { title: "Robots exclusion standard" }, (d) => typeof d.extract === "string"],
  ["arxiv", "search", { q: "all:robots.txt", limit: 1 }, (d) => d.items.length === 1],
]) {
  test(`live ${channel}: ${op}`, opts, async () => {
    const out = await runReach("api", { channel, op, params }, deps);
    assert.equal(out.result.error, null);
    assert.ok(check(out.result.data), `${channel} ${op} returned an unexpected shape`);
  });
}
