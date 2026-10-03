// Reach doctor, action menu, receipts and the run entry point.
import test from "node:test";
import assert from "node:assert/strict";
import { mkdtempSync, readFileSync, readdirSync, existsSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { reachDoctor } from "./reach/doctor.mjs";
import { reachMenu, readMemory } from "./reach/menu.mjs";
import { traceProvider } from "./reach/receipt.mjs";
import { runReach } from "./reach/run.mjs";
import { fakeFetch } from "./reach/fake-net.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const status = (report, id) => report.channels.find((c) => c.id === id).status;

test("the doctor makes no network call", () => {
  const original = globalThis.fetch;
  let called = 0;
  globalThis.fetch = async () => {
    called += 1;
    throw new Error("network used");
  };
  try {
    reachDoctor({});
  } finally {
    globalThis.fetch = original;
  }
  assert.equal(called, 0);
});

test("the doctor CLI writes no file in its working directory or cache", () => {
  const dir = mkdtempSync(path.join(tmpdir(), "reach-doctor-"));
  const env = { ...process.env, TELOS_REACH_CACHE_DIR: path.join(dir, "cache"), TELOS_REACH_RECEIPTS: path.join(dir, "r.jsonl"), TELOS_REACH_MEMORY: path.join(dir, "m.jsonl") };
  const run = spawnSync(process.execPath, [path.join(here, "reach.mjs"), "doctor", "--json"], { cwd: dir, env, encoding: "utf8" });
  assert.equal(run.status, 0, run.stderr);
  assert.equal(JSON.parse(run.stdout).schema, "telos.reach-doctor/v1");
  assert.deepEqual(readdirSync(dir), []);
});

test("status follows credentials, and values never appear in the report", () => {
  const bare = reachDoctor({});
  assert.equal(status(bare, "reddit"), "needs credentials");
  assert.equal(status(bare, "web"), "ready");
  assert.equal(status(bare, "x-session"), "user-present only");
  const env = { REDDIT_CLIENT_ID: "id-value-77", REDDIT_CLIENT_SECRET: "secret-value-88", X_BEARER_TOKEN: "x-value-99" };
  const keyed = reachDoctor(env);
  assert.equal(status(keyed, "reddit"), "ready");
  assert.equal(status(keyed, "x-api"), "ready");
  assert.equal(keyed.channels.find((c) => c.id === "reddit").auth.REDDIT_CLIENT_SECRET, "set");
  assert.doesNotMatch(JSON.stringify(keyed), /id-value-77|secret-value-88|x-value-99/);
  assert.ok(keyed.no_permitted_route.some((r) => /X bulk search/.test(r.name)));
});

test("the menu offers only verbs at or below the grant tier", () => {
  const t0 = reachMenu({ tier: "T0", env: {} });
  assert.deepEqual(t0.verbs.map((v) => v.verb), ["reach.doctor"]);
  const t1 = reachMenu({ tier: "T1", env: {} }).verbs.map((v) => v.verb);
  assert.ok(t1.includes("crawl.fetch") && t1.includes("browser.gettext"));
  assert.ok(!t1.includes("browser.click") && !t1.includes("browser.navigate"), "no act verbs in a read menu");
  const t5 = reachMenu({ tier: "T5", env: {} }).verbs.map((v) => v.verb);
  assert.ok(!t5.includes("browser.eval"), "the reach menu never offers script execution");
  assert.throws(() => reachMenu({ tier: "T9" }), /tier must be/);
});

test("the menu marks verbs whose credentials are missing", () => {
  const verbs = reachMenu({ tier: "T1", env: {} }).verbs;
  const reddit = verbs.find((v) => v.verb === "reddit.listing");
  assert.equal(reddit.available, false);
  assert.match(reddit.why, /REDDIT_CLIENT_ID/);
  assert.equal(verbs.find((v) => v.verb === "x.oembed").available, true);
});

test("trace line names the provider from the user's setting or the MCP client", () => {
  assert.equal(traceProvider({}).provider, "unknown");
  assert.equal(traceProvider({ TELOS_MCP_CLIENT: "claude-code" }).provider, "Anthropic");
  assert.equal(traceProvider({ TELOS_MCP_CLIENT: "codex-mcp-client" }).provider, "OpenAI");
  assert.equal(traceProvider({ TELOS_MCP_CLIENT: "claude-code", TELOS_TRACE_PROVIDER: "ollama local" }).provider, "local model (no remote provider)");
  assert.match(traceProvider({}).retention, /unknown/);
});

test("a networked run returns a receipt, and writes files only when named", async () => {
  const dir = mkdtempSync(path.join(tmpdir(), "reach-run-"));
  const post = "https://x.com/a/status/42";
  const url = `https://publish.x.com/oembed?url=${encodeURIComponent(post)}&omit_script=true&dnt=true`;
  const { fetchImpl } = fakeFetch({ [url]: { body: JSON.stringify({ author_name: "A", html: "<p>hi</p>" }) } });
  const deps = { env: { TELOS_MCP_CLIENT: "claude-code" }, fetchImpl, sleep: async () => {} };
  const quiet = await runReach("x-oembed", { url: post }, deps);
  assert.equal(quiet.receipt_file, null);
  assert.equal(quiet.receipt.schema, "telos.reach-receipt/v1");
  assert.equal(quiet.receipt.trace.line, "Trace seen by: Anthropic (source: mcp clientInfo.name)");
  assert.deepEqual(readdirSync(dir), []);
  const receiptFile = path.join(dir, "receipts.jsonl");
  const memoryFile = path.join(dir, "memory.jsonl");
  await runReach("x-oembed", { url: post }, { ...deps, receiptFile, memoryFile });
  assert.equal(JSON.parse(readFileSync(receiptFile, "utf8").trim()).fetches[0].status, 200);
  const memory = readMemory(memoryFile);
  assert.equal(memory.length, 1);
  assert.deepEqual(reachMenu({ tier: "T1", env: {}, memory }).already_read, [post]);
  assert.ok(existsSync(memoryFile));
});

test("unknown commands fail with the list of known ones", async () => {
  await assert.rejects(runReach("scrape-everything", {}, { env: {} }), /known: doctor, menu, fetch/);
});
