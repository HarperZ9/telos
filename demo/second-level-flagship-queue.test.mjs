import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { spawnSync } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const queue = JSON.parse(
  readFileSync(new URL("./integrations/second-level-flagship-queue.json", import.meta.url), "utf8")
);

assert.equal(queue.schema, "project-telos.second-level-flagship-queue/v1");
assert.equal(queue.tool, "telos.second_level.queue");
assert.equal(queue.privacy_boundary.raw_private_payloads_included, false);
assert.equal(queue.privacy_boundary.private_paths_in_public_records, false);
assert.equal(queue.privacy_boundary.source_body_required_for_interop, false);
assert.ok(queue.promotion_standard.includes("public-safe README receipt"));
assert.ok(queue.promotion_standard.includes("Crucible-verifiable claim"));

const byId = new Map(queue.public_candidates.map((candidate) => [candidate.id, candidate]));
for (const id of [
  "reconcile",
  "studio-engine",
  "provenance-sensorium",
  "proof-surface",
  "model-provenance-validator",
  "public-surface-sweeper",
  "agent-routing-kit",
  "agent-hook-pack",
  "coherence-membrane",
  "workflow-harness-lite"
]) {
  assert.ok(byId.has(id), `missing second-level candidate ${id}`);
}

assert.equal(byId.get("reconcile").lane, "creative-verification-engine");
assert.ok(byId.get("reconcile").host_flagships.includes("telos.creative.engine"));
assert.ok(byId.get("reconcile").receipts[0].sha256.startsWith("8d6ff02e"));

assert.equal(byId.get("studio-engine").lane, "world-rendering-engine");
assert.ok(byId.get("studio-engine").host_flagships.includes("telos.rendering.capabilities"));
assert.match(byId.get("studio-engine").risk_boundary, /untrusted/);

assert.equal(byId.get("model-provenance-validator").lane, "model-provenance-validation");
assert.ok(byId.get("model-provenance-validator").host_flagships.includes("telos.model.foundry"));
assert.match(byId.get("model-provenance-validator").risk_boundary, /private datasets/);

assert.equal(byId.get("agent-routing-kit").lane, "deterministic-agent-routing");
assert.ok(byId.get("agent-routing-kit").host_flagships.includes("forum.route"));
assert.match(byId.get("agent-routing-kit").risk_boundary, /hidden policy authority/);

for (const candidate of queue.public_candidates) {
  assert.ok(candidate.origin.startsWith("C:/dev/public/"), `${candidate.id} stays in public source lane`);
  assert.equal(candidate.visibility, "public-github-remote");
  assert.ok(candidate.host_flagships.length > 0, `${candidate.id} has hosts`);
  assert.ok(candidate.value.length > 0, `${candidate.id} has value`);
  assert.ok(candidate.risk_boundary.length > 0, `${candidate.id} has risk boundary`);
  assert.ok(candidate.first_action.length > 0, `${candidate.id} has first action`);
  assert.ok(candidate.receipts[0].sha256.length === 64, `${candidate.id} has README hash`);
}

assert.equal(queue.private_local_tranches.length, 5);
const privatePathPrefix = ["C:", "Users", "Zain"].join("/");
for (const tranche of queue.private_local_tranches) {
  assert.ok(!JSON.stringify(tranche).includes(privatePathPrefix), `${tranche.lane} does not publish private paths`);
  assert.match(tranche.public_boundary, /Do not|No /);
}

const cli = spawnSync(process.execPath, [path.join(here, "second-level-flagship-queue.mjs")], {
  cwd: path.resolve(here, ".."),
  encoding: "utf8"
});
assert.equal(cli.status, 0, cli.stderr || cli.stdout);
assert.deepEqual(JSON.parse(cli.stdout), queue);

const summary = spawnSync(process.execPath, [path.join(here, "second-level-flagship-queue.mjs"), "--summary"], {
  cwd: path.resolve(here, ".."),
  encoding: "utf8"
});
assert.equal(summary.status, 0, summary.stderr || summary.stdout);
assert.match(summary.stdout, /Telos Second-Level Flagship Queue/);
assert.match(summary.stdout, /public\s+10/);
assert.match(summary.stdout, /private_tranche\s+5/);
assert.match(summary.stdout, /creative-verification-engine/);
