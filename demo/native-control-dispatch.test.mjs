// Dispatcher checks for demo/native-control.mjs.
//
// PR #52 left two `case "apifetch":` labels in the browser switch. The first
// one won, so the CLI stopped reading the positional body and --contenttype.
// These tests pin the verb to its behavior from before #52 and fail on any
// repeated case label in a dispatcher switch.
//
// The behavior test injects a fake connection through run()'s `connect`
// option, so no browser is launched or attached.
import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { run } from "./native-control.mjs";

const dispatcher = readFileSync(fileURLToPath(new URL("./native-control.mjs", import.meta.url)), "utf8");

// Case labels grouped by the function that holds them.
function caseLabelsByFunction(source) {
  const groups = new Map();
  const chunks = source.split(/^(?:export\s+)?(?:async\s+)?function\s+/m).slice(1);
  for (const chunk of chunks) {
    const name = /^(\w+)/.exec(chunk)?.[1] ?? "?";
    groups.set(name, [...chunk.matchAll(/\bcase\s+["'`]([^"'`]+)["'`]\s*:/g)].map((m) => m[1]));
  }
  return groups;
}

test("no dispatcher function repeats a case label", () => {
  const groups = caseLabelsByFunction(dispatcher);
  assert.ok((groups.get("runBrowser") ?? []).length > 20, "runBrowser cases not found");
  const repeats = [];
  for (const [fn, labels] of groups) {
    const seen = new Set();
    for (const label of labels) {
      if (seen.has(label)) repeats.push(`${fn}: ${label}`);
      seen.add(label);
    }
  }
  assert.deepEqual(repeats, []);
});

test("the repeat detector catches a synthetic duplicate", () => {
  const groups = caseLabelsByFunction('async function f(v) { switch (v) { case "a": break; case "a": break; } }');
  assert.deepEqual(groups.get("f"), ["a", "a"]);
});

function fakeConnection() {
  const evaluated = [];
  const session = {
    closed: false,
    async send(method, params = {}) {
      if (method !== "Runtime.evaluate") return {};
      evaluated.push(params.expression);
      if (/fetch\(/.test(params.expression)) return { result: { value: { ok: true, status: 200 } } };
      return { result: { value: { url: "https://example.test/", host: "example.test" } } };
    },
    close() { this.closed = true; },
  };
  return { session, evaluated, connect: async () => ({ session }) };
}

test("browser apifetch sends the positional body with --contenttype and --method", async () => {
  const conn = fakeConnection();
  const result = await run(
    "browser",
    "apifetch",
    ["https://example.test/api", "name=telos", "v=1"],
    { method: "PUT", contenttype: "application/x-www-form-urlencoded" },
    { connect: conn.connect },
  );
  assert.deepEqual(result, { ok: true, status: 200 });
  const fetchExpr = conn.evaluated.find((e) => /fetch\(/.test(e));
  assert.ok(fetchExpr, "no in-page fetch was evaluated");
  assert.match(fetchExpr, /"https:\/\/example\.test\/api"/);
  assert.match(fetchExpr, /"PUT"/);
  assert.match(fetchExpr, /"application\/x-www-form-urlencoded"/);
  assert.match(fetchExpr, /"name=telos v=1"/);
  assert.equal(conn.session.closed, true);
});

test("browser apifetch with no positional body sends no body and defaults to POST JSON", async () => {
  const conn = fakeConnection();
  await run("browser", "apifetch", ["https://example.test/api"], {}, { connect: conn.connect });
  const fetchExpr = conn.evaluated.find((e) => /fetch\(/.test(e));
  assert.match(fetchExpr, /"POST"/);
  assert.match(fetchExpr, /"application\/json"/);
  assert.match(fetchExpr, /const b=null;/);
});
