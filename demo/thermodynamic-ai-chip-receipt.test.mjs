import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const packet = JSON.parse(
  readFileSync(new URL("./research/thermodynamic-ai-chip-receipt.json", import.meta.url), "utf8")
);

assert.equal(packet.schema, "project-telos.research-intake/youtube-verified-transcript-v1");
assert.equal(packet.tool, "gather.video");
assert.equal(packet.source.url, "https://www.youtube.com/watch?v=5pieVHmlbyk&t=29s");
assert.equal(packet.source.title, "The Thermodynamic AI Chip - Thomas Ahle");
assert.equal(packet.gather_receipt.transcript_item_hash, "40a31546b7a391bbb016ba4e3b86a06fc4027636ab85831a0be8b8ca44d6fc56");
assert.equal(packet.gather_receipt.digest_seal, "77bd2c9c39aa0628238f074efe3cd2a3ef64c7d7a373cec23128845f215a59a6");
assert.equal(packet.gather_receipt.verified_items.metadata, "MATCH");
assert.equal(packet.gather_receipt.verified_items.transcript, "MATCH");

for (const theme of [
  "hardware-design-verification-pipeline",
  "tests-are-not-proof",
  "autoformalization",
  "multiple-formal-representations",
  "timed-petri-nets",
  "tla-plus",
  "thermodynamic-stochastic-computing",
  "bayesian-uncertainty",
  "hybrid-compute-search"
]) {
  assert.ok(packet.verified_transcript_themes.includes(theme), `missing theme ${theme}`);
}

assert.deepEqual(packet.claim_state.MATCH.sort(), [
  "gather captured metadata and transcript receipts and verified both stored bodies",
  "transcript contains the core terms and themes in this packet"
].sort());
assert.ok(packet.claim_state.INFERRED.some((claim) => /external formal/.test(claim)));
assert.ok(packet.claim_state.UNVERIFIABLE_FROM_THIS_PACKET.some((claim) => /Normal Computing/.test(claim)));
assert.equal(packet.boundaries.raw_transcript_text_stored, false);
assert.equal(packet.boundaries.external_technical_correctness_promoted, false);
assert.equal(packet.integration_boundary.public_sources_only, true);
assert.equal(packet.integration_boundary.partnership_claimed, false);
assert.equal(packet.integration_boundary.private_ip_required, false);

const publicSources = new Set(packet.public_source_receipts.map((receipt) => receipt.id));
for (const id of [
  "source-thomas-ahle-site",
  "source-normal-team",
  "source-normal-verilog-simulator",
  "source-thermodynamic-computing-nature",
  "source-normal-matrix-inversion"
]) {
  assert.ok(publicSources.has(id), `missing public source ${id}`);
}

const integrationModules = new Set(packet.integration_strategy.modules.map((module) => module.id));
for (const id of [
  "normal-public-source-graph",
  "verilog-formal-receipt-bridge",
  "thermodynamic-simulation-lab",
  "uncertainty-meter-lane",
  "spec-representation-workbench"
]) {
  assert.ok(integrationModules.has(id), `missing integration module ${id}`);
}

const labIds = new Set(packet.build_implications.map((item) => item.id));
for (const id of [
  "spec-representation-lab",
  "test-is-not-proof-fixture",
  "formalization-drift-receipt",
  "stochastic-compute-lab",
  "hybrid-search-demo"
]) {
  assert.ok(labIds.has(id), `missing build implication ${id}`);
}

for (const role of ["gather", "index", "forum", "crucible", "telos"]) {
  assert.ok(packet.telos_fit.roles[role].length > 0, `missing Telos role ${role}`);
}

const run = spawnSync(process.execPath, [path.join(here, "thermodynamic-ai-chip-receipt.mjs")], {
  cwd: path.resolve(here, ".."),
  encoding: "utf8"
});
assert.equal(run.status, 0, run.stderr || run.stdout);
assert.deepEqual(JSON.parse(run.stdout), packet);
