import assert from "node:assert/strict";
import { existsSync, readFileSync, rmSync } from "node:fs";
import { spawnSync } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, "..");
const cli = path.join(here, "embodied-sim2real-proof-packet.mjs");

function run(args = []) {
  return spawnSync(process.execPath, [cli, ...args], {
    cwd: root,
    encoding: "utf8"
  });
}

const result = run();
assert.equal(result.status, 0, result.stderr);

const packet = JSON.parse(result.stdout);
assert.equal(packet.schema, "project-telos.embodied-sim2real/proof-packet-fixture/v1");
assert.equal(packet.result, "EMBODIED_SIM2REAL_FIXTURE_MATCH");
assert.equal(packet.claim_card.verdict, "MATCH");
assert.equal(packet.checks.trajectory_match, true);
assert.equal(packet.checks.safety_envelope_match, true);
assert.equal(packet.checks.latency_match, true);
assert.equal(packet.checks.unit_contract_match, true);
assert.equal(packet.traces.predicted.length, packet.fixture.commands.length + 1);
assert.equal(packet.traces.observed.length, packet.traces.predicted.length);
assert.ok(packet.metrics.mean_path_error_m <= packet.fixture.tolerances.mean_path_error_m);
assert.ok(packet.metrics.max_path_error_m <= packet.fixture.tolerances.max_path_error_m);
assert.ok(packet.metrics.terminal_position_error_m <= packet.fixture.tolerances.terminal_position_error_m);
assert.ok(packet.metrics.terminal_heading_error_rad <= packet.fixture.tolerances.terminal_heading_error_rad);
assert.ok(packet.metrics.min_obstacle_clearance_m >= packet.fixture.tolerances.min_obstacle_clearance_m);
assert.ok(packet.metrics.command_envelope.wheel_speed_ok);
assert.ok(packet.metrics.command_envelope.angular_speed_ok);

const expectedControls = new Map(packet.checks.negative_controls.map((control) => [control.id, control]));
for (const id of [
  "wrong_wheel_base",
  "swapped_wheels",
  "centimeters_treated_as_meters",
  "unsafe_clearance",
  "latency_over_limit"
]) {
  assert.equal(expectedControls.get(id).verdict, "DRIFT");
  assert.ok(expectedControls.get(id).failed_checks.length >= 1);
}

assert.match(packet.claim_card.scope, /One local differential-drive sim-to-real fixture only/);
assert.ok(packet.non_claims.some((item) => /real-world robot safety/.test(item)));
assert.ok(packet.non_claims.some((item) => /vision-language-action/.test(item)));
assert.ok(packet.toolchain_implications.some((item) => /BuildLang\/buildc/.test(item)));

const summary = run(["--summary"]);
assert.equal(summary.status, 0, summary.stderr);
assert.match(summary.stdout, /EMBODIED_SIM2REAL_FIXTURE_MATCH/);

const outPath = path.join(root, "docs", "outreach", "receipts", "embodied-sim2real-proof-packet.tmp.json");
try {
  const write = run(["--out", outPath]);
  assert.equal(write.status, 0, write.stderr);
  assert.equal(existsSync(outPath), true);
  const written = JSON.parse(readFileSync(outPath, "utf8"));
  assert.equal(written.result, "EMBODIED_SIM2REAL_FIXTURE_MATCH");
} finally {
  rmSync(outPath, { force: true });
}
