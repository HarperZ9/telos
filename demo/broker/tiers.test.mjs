// The tier table covers every verb the native-control dispatcher accepts, and
// promotion only ever raises a tier (DESIGN.md 1.1, build step 3).
import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { actions as learnActions } from "../native-control/learn.mjs";
import { effectiveTier, LADDER, tierRank, TIERS, VERBS, verbSpec } from "./tiers.mjs";

const dispatcher = readFileSync(fileURLToPath(new URL("../native-control.mjs", import.meta.url)), "utf8");

function labels(fnName) {
  const start = dispatcher.indexOf(`function ${fnName}(`);
  assert.ok(start >= 0, `${fnName} not found in the dispatcher`);
  const next = dispatcher.indexOf("\nasync function ", start + 1);
  const chunk = dispatcher.slice(start, next < 0 ? undefined : next);
  return [...chunk.matchAll(/\bcase\s+["'`]([^"'`]+)["'`]\s*:/g)].map((m) => m[1]);
}

function dispatcherVerbs() {
  const verbs = [];
  for (const [fn, domain] of [["runBrowser", "browser"], ["runApp", "app"], ["runDevice", "device"]]) {
    for (const label of labels(fn)) verbs.push(`${domain}.${label}`);
  }
  if (/verb === "tabs"/.test(dispatcher)) verbs.push("browser.tabs");
  for (const name of Object.keys(learnActions)) verbs.push(`learn.${name}`);
  return verbs;
}

test("every dispatcher verb has a tier floor", () => {
  const verbs = dispatcherVerbs();
  assert.ok(verbs.length > 40, `only ${verbs.length} dispatcher verbs found`);
  const missing = verbs.filter((v) => !verbSpec(v));
  assert.deepEqual(missing, []);
});

test("the enumeration catches a verb with no tier", () => {
  assert.equal(verbSpec("browser.newverb"), null);
  assert.equal(verbSpec("constructor"), null, "prototype keys are not verbs");
});

test("state-changing verbs sit at T3 or above, hardware input at T5", () => {
  for (const v of ["browser.navigate", "browser.click", "browser.fill", "browser.upload", "app.invoke", "app.setvalue", "browser.apifetch"]) {
    assert.ok(tierRank(verbSpec(v).tier) >= 3, `${v} below T3`);
  }
  for (const v of ["browser.eval", "browser.evalfile", "browser.evalframe", "device.exec", "browser.run"]) assert.equal(verbSpec(v).tier, "T4", v);
  for (const v of ["app.input", "app.type"]) assert.equal(verbSpec(v).tier, "T5", v);
  for (const [name, spec] of Object.entries(VERBS)) {
    if (name.startsWith("hardware.")) assert.equal(spec.tier, "T5", name);
  }
});

test("confirmation is required from T3 up, with the design's windows and ceilings", () => {
  assert.deepEqual(TIERS.filter((t) => LADDER[t].confirm), ["T3", "T4", "T5"]);
  assert.equal(LADDER.T3.window_s, 120);
  assert.equal(LADDER.T4.window_s, 60);
  assert.equal(LADDER.T5.window_s, 60);
  assert.deepEqual(TIERS.map((t) => LADDER[t].ceiling_s), [0, 28800, 14400, 3600, 900, 900]);
  assert.equal(LADDER.T3.batch_max, 10);
  assert.equal(LADDER.T4.batch_max, 1);
});

test("promotion raises a floor and never lowers one", () => {
  assert.equal(effectiveTier("browser.gettext", { resolution: "coordinate" }), "T3");
  assert.equal(effectiveTier("device.write", { writesInSandbox: true }), "T2");
  assert.equal(effectiveTier("device.write", { writesInSandbox: true, preimageFailed: true }), "T3");
  assert.equal(effectiveTier("device.write", { writesOutsideSandbox: true }), "T3");
  for (const [verb, spec] of Object.entries(VERBS)) {
    for (const ctx of [{}, { resolution: "coordinate" }, { writesInSandbox: true }, { preimageFailed: true }]) {
      assert.ok(tierRank(effectiveTier(verb, ctx)) >= tierRank(spec.tier), `${verb} lowered by ${JSON.stringify(ctx)}`);
    }
  }
});
