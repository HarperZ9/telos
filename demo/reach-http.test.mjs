// HTTP behaviour: honest identity, pacing, backoff, cache and bot-check stop.
import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { mkdtempSync, readdirSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import { fakeHttp } from "./reach/fake-net.mjs";
import { userAgent } from "./reach/identity.mjs";
import { MAX_RETRIES, backoffMs, parseRetryAfter } from "./reach/limiter.mjs";
import { maxAgeMs } from "./reach/cache.mjs";

const URL_A = "https://a.test/page";

test("every request carries the one honest User-Agent", async () => {
  const { http, calls } = fakeHttp({ [URL_A]: { body: "ok" } }, { env: { TELOS_REACH_CONTACT: "me@example.test" } });
  await http.get(URL_A);
  const ua = calls[0].headers["user-agent"];
  assert.match(ua, /^Telos\/\d+\.\d+\.\d+ \(\+https:\/\/github\.com\/HarperZ9\/telos; reach crawler; contact me@example\.test\)$/);
  assert.doesNotMatch(ua, /Mozilla|Chrome|Safari|Gecko/);
  // Paired: the contact cannot inject header syntax or replace the name.
  assert.match(userAgent({ TELOS_REACH_CONTACT: "x)\r\nEvil: 1" }), /^Telos\/\S+ \(\+\S+; reach crawler; contact xEvil:1\)$/);
  assert.doesNotMatch(userAgent({ TELOS_REACH_CONTACT: "a\r\nb" }), /[\r\n]/);
});

test("requests to one host are spaced; other hosts are not delayed", async () => {
  const { http, sleeps } = fakeHttp({ [URL_A]: { body: "1" }, "https://a.test/two": { body: "2" }, "https://b.test/": { body: "3" } });
  await http.get(URL_A);
  await http.get("https://b.test/");
  assert.deepEqual(sleeps, [], "a different host must not wait");
  await http.get("https://a.test/two");
  assert.equal(sleeps.length, 1);
  assert.ok(sleeps[0] > 0 && sleeps[0] <= 1000);
});

test("Crawl-delay lengthens the interval and never shortens it", async () => {
  const { http, sleeps } = fakeHttp({ [URL_A]: { body: "1" }, "https://a.test/b": { body: "2" } });
  http.limiter.setCrawlDelay("a.test", 5);
  http.limiter.setCrawlDelay("b.test", 0.1);
  assert.equal(http.limiter.intervalFor("b.test"), 1000);
  await http.get(URL_A);
  await http.get("https://a.test/b");
  assert.equal(sleeps[0], 5000);
});

test("429 waits for Retry-After, then succeeds", async () => {
  const { http, calls, sleeps } = fakeHttp({ [URL_A]: [{ status: 429, headers: { "retry-after": "7" } }, { body: "ok" }] });
  const res = await http.get(URL_A);
  assert.equal(res.status, 200);
  assert.equal(calls.length, 2);
  assert.ok(sleeps.includes(7000));
});

test("backoff gives up after the retry cap instead of hammering", async () => {
  const { http, calls } = fakeHttp({ [URL_A]: { status: 503, body: "busy" } });
  const res = await http.get(URL_A);
  assert.equal(res.status, 503);
  assert.equal(calls.length, MAX_RETRIES + 1);
});

test("Retry-After and backoff arithmetic", () => {
  assert.equal(parseRetryAfter("3"), 3000);
  assert.equal(parseRetryAfter(new Date(10_000).toUTCString(), 4_000), 6000);
  assert.equal(parseRetryAfter("soon"), null);
  assert.equal(backoffMs(0, null), 1000);
  assert.equal(backoffMs(3, null), 8000);
  assert.equal(backoffMs(0, 10 * 60_000), 60_000, "capped");
});

test("a fresh cache entry skips the network; a stale one revalidates with 304", async () => {
  const routes = { [URL_A]: [{ body: "v1", headers: { etag: '"1"', "cache-control": "max-age=60" } }, { status: 304 }] };
  const { http, calls, advance } = fakeHttp(routes);
  await http.get(URL_A);
  const again = await http.get(URL_A);
  assert.equal(calls.length, 1);
  assert.equal(again.cache, "fresh");
  advance(61_000);
  const third = await http.get(URL_A);
  assert.equal(calls.length, 2);
  assert.equal(calls[1].headers["if-none-match"], '"1"');
  assert.equal(third.cache, "revalidated");
  assert.equal(third.body, "v1");
});

test("no-store responses and credentialed requests are never cached", async () => {
  const { http, calls } = fakeHttp({ [URL_A]: { body: "x", headers: { "cache-control": "no-store" } }, "https://a.test/api": { body: "y" } });
  await http.get(URL_A);
  await http.get(URL_A);
  await http.get("https://a.test/api", { headers: { authorization: "Bearer t" } });
  await http.get("https://a.test/api", { headers: { authorization: "Bearer t" } });
  assert.equal(calls.length, 4);
  assert.equal(http.cache.get(URL_A), null, "no-store must leave no entry");
  assert.equal(http.cache.get("https://a.test/api"), null, "a credentialed response must leave no entry");
  assert.equal(maxAgeMs("private, max-age=9"), 0);
});

test("the directory cache is written only when the user names one", async () => {
  const dir = mkdtempSync(path.join(tmpdir(), "reach-cache-"));
  const { http } = fakeHttp({ [URL_A]: { body: "x" } }, { cacheDir: path.join(dir, "c") });
  await http.get(URL_A);
  assert.equal(readdirSync(path.join(dir, "c")).length, 1);
  const plain = fakeHttp({ [URL_A]: { body: "x" } });
  assert.equal(plain.http.cache.dir, null);
});

test("a bot check is reported, not passed, and not cached", async () => {
  const { http, calls } = fakeHttp({ [URL_A]: { status: 403, body: "<html>Please verify you are human</html>" } });
  const res = await http.get(URL_A);
  assert.equal(res.bot_check, true);
  await http.get(URL_A);
  assert.equal(calls.length, 2, "a bot-check page must not be served from cache");
  const ok = fakeHttp({ [URL_A]: { status: 403, body: "forbidden" } });
  assert.equal((await ok.http.get(URL_A)).bot_check, false, "a plain 403 is not a bot check");
});

test("the byte hash in the result is the SHA-256 of the body", async () => {
  const { http } = fakeHttp({ [URL_A]: { body: "hello" } });
  const res = await http.get(URL_A);
  assert.equal(res.bytes_sha256, createHash("sha256").update("hello").digest("hex"));
  assert.equal(res.bytes, 5);
});

test("network errors become a refused record instead of a crash", async () => {
  const { http } = fakeHttp({ [URL_A]: new Error("socket hang up") });
  const res = await http.get(URL_A);
  assert.equal(res.status, 0);
  assert.match(res.refused, /network error: socket hang up/);
});
