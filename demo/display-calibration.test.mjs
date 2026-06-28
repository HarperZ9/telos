import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { spawnSync } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const contract = JSON.parse(readFileSync(new URL("./integrations/display-calibration.json", import.meta.url), "utf8"));

assert.equal(contract.schema, "project-telos.display-calibration/v1");
assert.equal(contract.tool, "telos.display.calibration");
assert.equal(contract.generated_at, "2026-06-28T00:00:00.000Z");
assert.equal(contract.contract.protocol_agnostic, true);
assert.equal(contract.contract.hardware_mutation_allowed, false);
assert.equal(contract.contract.receipts_required, true);
assert.equal(contract.contract.raw_assets_required_for_interop, false);

for (const surface of ["cli-json", "mcp-json-rpc", "ide", "tui", "app-bridge", "proof-artifact"]) {
  assert.ok(contract.contract.io_surfaces.includes(surface), `missing surface ${surface}`);
}

const sourceIds = new Set(contract.sources.map((source) => source.id));
assert.ok(sourceIds.has("calibrate-pro"));
assert.ok(sourceIds.has("quanta-color"));
assert.ok(
  contract.sources
    .find((source) => source.id === "calibrate-pro")
    .receipt.sha256.startsWith("04e294f1"),
  "calibrate-pro receipt is wired"
);
assert.ok(
  contract.sources
    .find((source) => source.id === "quanta-color")
    .receipt.sha256.startsWith("afeec67"),
  "quanta-color receipt is wired"
);

for (const target of ["generic-sdr-reference", "wide-gamut-hdr-reference", "sensorless-panel-database"]) {
  assert.ok(contract.display_targets.some((item) => item.id === target), `missing target ${target}`);
}

for (const patchSet of ["colorchecker-24", "grayscale-tracking", "hdr-ramp", "gamut-boundary"]) {
  assert.ok(contract.patch_sets.some((item) => item.id === patchSet), `missing patch set ${patchSet}`);
}

for (const artifact of [
  "icc-v4-profile-ref",
  "cube-3d-lut-ref",
  "calibration-report-ref",
  "delta-e-summary",
  "restore-state-ref"
]) {
  assert.ok(contract.artifact_types.includes(artifact), `missing artifact ${artifact}`);
}

assert.ok(contract.color_library.dependencies.includes("quanta-color"));
assert.ok(contract.color_library.metrics.includes("CIEDE2000"));
assert.ok(contract.color_library.spaces.includes("Oklab"));
assert.ok(contract.color_library.spaces.includes("JzAzBz"));

assert.ok(contract.measurement_gates.some((gate) => gate.tool === "crucible.measurement_gate"));
assert.ok(contract.measurement_gates.some((gate) => gate.expected_verdicts.includes("UNVERIFIABLE")));
assert.equal(contract.privacy.raw_device_telemetry_required, false);
assert.equal(contract.privacy.raw_lut_payload_required, false);
assert.match(contract.boundary, /read-only/);
assert.match(contract.boundary, /no DDC\/CI/);
assert.ok(contract.next_actions.includes("Implement a read-only color packet generator before adding live monitor controls."));

const cli = spawnSync(process.execPath, [path.join(here, "display-calibration.mjs")], {
  cwd: path.resolve(here, ".."),
  encoding: "utf8"
});
assert.equal(cli.status, 0, cli.stderr || cli.stdout);
assert.deepEqual(JSON.parse(cli.stdout), contract);

const summary = spawnSync(process.execPath, [path.join(here, "display-calibration.mjs"), "--summary"], {
  cwd: path.resolve(here, ".."),
  encoding: "utf8"
});
assert.equal(summary.status, 0, summary.stderr || summary.stdout);
assert.match(summary.stdout, /Telos Display Calibration/);
assert.match(summary.stdout, /hardware\s+read-only/);
assert.match(summary.stdout, /targets\s+3/);
assert.match(summary.stdout, /patches\s+4/);
