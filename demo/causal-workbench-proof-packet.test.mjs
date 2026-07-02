import assert from "node:assert/strict";
import { existsSync, readFileSync, rmSync } from "node:fs";
import { spawnSync } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, "..");
const cli = path.join(here, "causal-workbench-proof-packet.mjs");

function run(args = []) {
  return spawnSync(process.execPath, [cli, ...args], {
    cwd: root,
    encoding: "utf8"
  });
}

const result = run();
assert.equal(result.status, 0, result.stderr);

const packet = JSON.parse(result.stdout);
assert.equal(packet.schema, "project-telos.causal-workbench/proof-packet-fixture/v1");
assert.equal(packet.result, "CAUSAL_DAG_FIXTURE_MATCH");
assert.equal(packet.claim_card.verdict, "MATCH");
assert.equal(packet.checks.dag_acyclic, true);
assert.deepEqual(packet.checks.minimal_adjustment_sets, [["age", "baseline_health"]]);
assert.ok(packet.checks.treatment_descendants.includes("health_outcome"));
assert.ok(packet.checks.treatment_descendants.includes("biomarker"));
assert.ok(packet.checks.backdoor_paths.some((pathItem) => pathItem.join("->") === "exercise->age->health_outcome"));
assert.ok(packet.checks.backdoor_paths.some((pathItem) => pathItem.join("->") === "exercise->baseline_health->health_outcome"));

const empty = packet.checks.negative_controls.find((entry) => entry.adjustment.length === 0);
assert.equal(empty.valid, false);
assert.equal(empty.active_backdoor_paths.length, 2);

const ageOnly = packet.checks.negative_controls.find((entry) => entry.adjustment.join(",") === "age");
assert.equal(ageOnly.valid, false);
assert.equal(ageOnly.active_backdoor_paths.length, 1);

const baselineOnly = packet.checks.negative_controls.find((entry) => entry.adjustment.join(",") === "baseline_health");
assert.equal(baselineOnly.valid, false);
assert.equal(baselineOnly.active_backdoor_paths.length, 1);

const encouragement = packet.checks.negative_controls.find((entry) => entry.adjustment.join(",") === "encouragement");
assert.equal(encouragement.valid, false);
assert.equal(encouragement.active_backdoor_paths.length, 2);

const biomarker = packet.checks.negative_controls.find((entry) => entry.adjustment.join(",") === "biomarker");
assert.equal(biomarker.valid, false);
assert.deepEqual(biomarker.descendant_violations, ["biomarker"]);

assert.match(packet.claim_card.scope, /One deterministic DAG fixture only/);
assert.ok(packet.non_claims.some((item) => /medical recommendation/.test(item)));
assert.ok(packet.toolchain_implications.some((item) => /BuildLang\/buildc/.test(item)));

const summary = run(["--summary"]);
assert.equal(summary.status, 0, summary.stderr);
assert.match(summary.stdout, /CAUSAL_DAG_FIXTURE_MATCH/);

const outPath = path.join(root, "docs", "outreach", "receipts", "causal-workbench-proof-packet.tmp.json");
try {
  const write = run(["--out", outPath]);
  assert.equal(write.status, 0, write.stderr);
  assert.equal(existsSync(outPath), true);
  const written = JSON.parse(readFileSync(outPath, "utf8"));
  assert.equal(written.result, "CAUSAL_DAG_FIXTURE_MATCH");
} finally {
  rmSync(outPath, { force: true });
}
