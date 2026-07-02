import assert from "node:assert/strict";
import { existsSync, readFileSync, rmSync } from "node:fs";
import { spawnSync } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, "..");
const cli = path.join(here, "quantum-error-correction-proof-packet.mjs");

function run(args = []) {
  return spawnSync(process.execPath, [cli, ...args], {
    cwd: root,
    encoding: "utf8"
  });
}

const result = run();
assert.equal(result.status, 0, result.stderr);

const packet = JSON.parse(result.stdout);
assert.equal(packet.schema, "project-telos.quantum-error-correction/proof-packet-fixture/v1");
assert.equal(packet.result, "QEC_STABILIZER_FIXTURE_MATCH");
assert.equal(packet.claim_card.verdict, "MATCH");
assert.equal(packet.checks.single_error_rows.length, 8);
assert.equal(packet.checks.unique_syndromes, true);
assert.equal(packet.checks.all_single_x_errors_correct, true);
assert.ok(packet.checks.single_error_rows.every((row) => row.logical_match));

const syndromeMap = new Map(packet.checks.single_error_rows
  .filter((row) => row.logical === 0)
  .map((row) => [row.error, row.syndrome.join(",")]));
assert.equal(syndromeMap.get("none"), "0,0");
assert.equal(syndromeMap.get("X0"), "1,0");
assert.equal(syndromeMap.get("X1"), "1,1");
assert.equal(syndromeMap.get("X2"), "0,1");

const controls = new Map(packet.checks.negative_controls.map((control) => [control.id, control]));
assert.equal(controls.get("double_bit_flip_aliases_to_logical_error").verdict, "DRIFT");
assert.equal(controls.get("double_bit_flip_aliases_to_logical_error").decoded, 1);
assert.equal(controls.get("phase_error_out_of_scope").verdict, "UNVERIFIABLE");
assert.equal(controls.get("wrong_syndrome_map_for_middle_qubit").verdict, "DRIFT");
assert.equal(controls.get("missing_stabilizer_measurement").verdict, "UNVERIFIABLE");
assert.equal(controls.get("non_codeword_input").verdict, "DRIFT");

assert.match(packet.claim_card.scope, /One local stabilizer-code fixture only/);
assert.ok(packet.non_claims.some((item) => /surface-code decoder/.test(item)));
assert.ok(packet.non_claims.some((item) => /fault-tolerant quantum computing/.test(item)));
assert.ok(packet.toolchain_implications.some((item) => /BuildLang\/buildc/.test(item)));

const summary = run(["--summary"]);
assert.equal(summary.status, 0, summary.stderr);
assert.match(summary.stdout, /QEC_STABILIZER_FIXTURE_MATCH/);

const outPath = path.join(root, "docs", "outreach", "receipts", "quantum-error-correction-proof-packet.tmp.json");
try {
  const write = run(["--out", outPath]);
  assert.equal(write.status, 0, write.stderr);
  assert.equal(existsSync(outPath), true);
  const written = JSON.parse(readFileSync(outPath, "utf8"));
  assert.equal(written.result, "QEC_STABILIZER_FIXTURE_MATCH");
} finally {
  rmSync(outPath, { force: true });
}
