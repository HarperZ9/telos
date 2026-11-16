// The search scrape in native-control/scrape.mjs identifies itself as Telos,
// and a block, a human-verification page or an HTTP 403/429 ends the call with
// a reported stop. It never retries with a different identity or headers.
//
// Offline: a fake CDP session stands in for the browser and globalThis.fetch
// is replaced for the duration of each test. No network, no browser.
import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import * as scrape from "./native-control/scrape.mjs";
import { TELOS_VERSION } from "./version.mjs";

const RESULTS_HTML = `
<div class="result"><a rel="nofollow" class="result__a" href="https://example.org/a">Alpha</a>
<a class="result__snippet" href="https://example.org/a">First snippet</a></div>
<div class="result"><a rel="nofollow" class="result__a" href="https://example.net/b">Beta</a>
<a class="result__snippet" href="https://example.net/b">Second snippet</a></div>`;

// In-page evaluations: the gate scan returns `scan`; the result parse returns `list`.
function fakeSession({ scan = { url: "https://html.duckduckgo.com/html/", host: "html.duckduckgo.com" }, list = [] } = {}) {
  const calls = [];
  return {
    calls,
    async send(method, params = {}) {
      calls.push(method);
      if (method !== "Runtime.evaluate") return {};
      if (/result__a/.test(params.expression)) return { result: { value: list } };
      return { result: { value: scan } };
    },
  };
}

async function withFetch(respond, fn) {
  const requests = [];
  const real = globalThis.fetch;
  globalThis.fetch = async (url, init = {}) => {
    requests.push({ url: String(url), headers: { ...(init.headers || {}) } });
    const { status = 200, body = "" } = respond(requests.length);
    return new Response(body, { status });
  };
  try {
    return { result: await fn(), requests };
  } finally {
    globalThis.fetch = real;
  }
}

const fetchCall = (session) => scrape.targets(session, { query: "q", limit: 5, via: "fetch", settleMs: 0 });
const browserCall = (session) => scrape.targets(session, { query: "q", limit: 5, settleMs: 0 });

test("the fetch path sends one request whose User-Agent names Telos and its version", async () => {
  const { requests } = await withFetch(() => ({ body: RESULTS_HTML }), () => fetchCall(fakeSession()));
  assert.equal(requests.length, 1);
  const ua = requests[0].headers["User-Agent"];
  assert.ok(ua.startsWith(`Telos/${TELOS_VERSION}`), `User-Agent was ${ua}`);
  assert.doesNotMatch(ua, /Mozilla|Chrome|Safari|Windows NT/);
});

test("fetched results are parsed and counted", async () => {
  const { result } = await withFetch(() => ({ body: RESULTS_HTML }), () => fetchCall(fakeSession()));
  assert.equal(result.results.length, 2);
  assert.equal(result.count, 2);
  assert.equal(result.via, "fetch");
  assert.equal(result.results[0].url, "https://example.org/a");
});

for (const status of [403, 429]) {
  test(`HTTP ${status} is a reported stop with no second request`, async () => {
    const { result, requests } = await withFetch(() => ({ status, body: "blocked" }), () => fetchCall(fakeSession()));
    assert.equal(requests.length, 1);
    assert.equal(result.stopped?.reason, `http-${status}`);
    assert.equal(result.count, 0);
    assert.deepEqual(result.results, []);
    assert.match(result.stopped.action, /person/i);
  });
}

test("a human-verification page on the fetch path is a reported stop", async () => {
  const body = "<html><body><h1>Please verify you are human to continue</h1></body></html>";
  const { result, requests } = await withFetch(() => ({ body }), () => fetchCall(fakeSession()));
  assert.equal(requests.length, 1);
  assert.equal(result.stopped?.reason, "human-check");
  assert.deepEqual(result.results, []);
});

test("a human-verification page in the browser stops without a fetch", async () => {
  const session = fakeSession({ scan: { url: "https://html.duckduckgo.com/html/", host: "html.duckduckgo.com", hasHumanCheck: true } });
  const { result, requests } = await withFetch(() => ({ body: RESULTS_HTML }), () => browserCall(session));
  assert.equal(requests.length, 0, "a blocked browser page must not fall back to another identity");
  assert.equal(result.stopped?.gate, "human-check");
  assert.deepEqual(result.results, []);
});

test("an empty browser result is reported as empty, with no fallback request", async () => {
  const { result, requests } = await withFetch(() => ({ body: RESULTS_HTML }), () => browserCall(fakeSession()));
  assert.equal(requests.length, 0);
  assert.equal(result.via, "browser");
  assert.equal(result.count, 0);
  assert.equal(result.stopped, undefined);
});

test("browser results come back with their count", async () => {
  const list = [{ title: "Alpha", url: "https://example.org/a", snippet: "" }];
  const { result } = await withFetch(() => ({}), () => browserCall(fakeSession({ list })));
  assert.equal(result.count, 1);
  assert.deepEqual(result.results, list);
});

test("the module carries no bot-block framing or browser identity string", () => {
  const source = readFileSync(fileURLToPath(new URL("./native-control/scrape.mjs", import.meta.url)), "utf8");
  assert.doesNotMatch(source, /bot-?blocks?|reputation/i);
  assert.doesNotMatch(source, /Mozilla\//);
});
