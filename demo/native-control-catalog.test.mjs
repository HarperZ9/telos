// The MCP catalog for native control loads no driver. The client plugin ships
// this module and leaves the drivers in the npm package, so the catalog must
// stay importable on its own and match what the CLI prints.
import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { HELP, SCHEMA, helpReceipt, makeReceipt } from "./native-control-catalog.mjs";
import * as cli from "./native-control.mjs";
import { actions as learnActions } from "./native-control/learn.mjs";

const here = (rel) => fileURLToPath(new URL(rel, import.meta.url));
const fixedClock = () => "2026-10-01T00:00:00.000Z";

test("catalog module imports nothing but the focus classifier", () => {
  const source = readFileSync(here("./native-control-catalog.mjs"), "utf8");
  const imports = [...source.matchAll(/^import\s.*?from\s+["']([^"']+)["']/gm)].map((m) => m[1]);
  assert.deepEqual(imports.sort(), ["./native-control/focus.mjs", "node:url"]);
  assert.doesNotMatch(source, /\bimport\(/, "no dynamic driver import");
});

test("CLI re-exports the catalog's receipt shape", () => {
  assert.equal(cli.SCHEMA, SCHEMA);
  assert.equal(cli.makeReceipt, makeReceipt);
});

test("MCP catalog and CLI help print the same receipt", () => {
  const run = (script) => {
    const out = spawnSync(process.execPath, [here(script)], { encoding: "utf8", timeout: 20000 });
    assert.equal(out.status, 0, out.stderr);
    const { at, ...rest } = JSON.parse(out.stdout);
    assert.match(at, /^\d{4}-\d{2}-\d{2}T/);
    return rest;
  };
  assert.deepEqual(run("./native-control-catalog.mjs"), run("./native-control.mjs"));
});

test("help receipt is background, read-only and says where actuation lives", () => {
  const r = helpReceipt({ clock: fixedClock });
  assert.equal(r.schema, "project-telos.native-control/v1");
  assert.equal(r.action, "help");
  assert.equal(r.background, true);
  assert.equal(r.focus_effect, "none_requested");
  assert.equal(r.at, "2026-10-01T00:00:00.000Z");
  assert.equal(r.result, HELP);
  assert.match(HELP.delivery, /npm package/);
  assert.match(HELP.delivery, /catalog only/);
});

test("catalog lists every verb the CLI dispatcher accepts, and no other", () => {
  const source = readFileSync(here("./native-control.mjs"), "utf8");
  const body = (name) => {
    const start = source.indexOf(`async function ${name}(`);
    assert.ok(start >= 0, `${name} not found`);
    const end = source.indexOf("\nasync function ", start + 1);
    return source.slice(start, end < 0 ? undefined : end);
  };
  const cases = (text) => [...text.matchAll(/\bcase\s+"([^"]+)"\s*:/g)].map((m) => m[1]);
  const aliased = Object.keys(HELP.aliases).map((k) => k.split(" ")[1]);
  const browserVerbs = ["tabs", ...cases(body("runBrowser"))].filter((v) => !aliased.includes(v));
  assert.deepEqual([...HELP.browser].sort(), browserVerbs.sort());
  assert.deepEqual([...HELP.app].sort(), cases(body("runApp")).sort());
  assert.deepEqual([...HELP.device].sort(), cases(body("runDevice")).sort());
  assert.deepEqual([...HELP.learn].sort(), Object.keys(learnActions).sort());
  for (const [alias, target] of Object.entries(HELP.aliases)) {
    const [domain, verb] = target.split(" ");
    assert.ok(HELP[domain].includes(verb), `${alias} points at a listed verb`);
  }
});
