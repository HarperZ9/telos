import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { spawnSync } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const substrate = JSON.parse(
  readFileSync(new URL("./integrations/workstation-substrate.json", import.meta.url), "utf8")
);

assert.equal(substrate.schema, "project-telos.workstation-substrate/v1");
assert.equal(substrate.tool, "telos.workstation.substrate");
assert.equal(substrate.privacy_boundary.absolute_private_paths_included, false);
assert.equal(substrate.privacy_boundary.raw_private_payloads_included, false);
assert.equal(substrate.privacy_boundary.private_filenames_included, false);
assert.equal(substrate.privacy_boundary.credentials_or_signing_material_included, false);
assert.equal(substrate.aggregate.mapped_roots, 2);
assert.equal(substrate.aggregate.repo_count, 331);
assert.equal(substrate.aggregate.public_class_repos, 163);
assert.equal(substrate.aggregate.local_class_repos, 168);
assert.equal(substrate.aggregate.dirty_repos, 333);
assert.equal(substrate.aggregate.verdict, "MATCH");

const byRoot = new Map(substrate.index_evidence.map((entry) => [entry.root_id, entry]));
assert.equal(byRoot.get("operator-dev-root").repo_count, 124);
assert.equal(byRoot.get("operator-dev-root").class_counts.public, 114);
assert.equal(byRoot.get("operator-dev-root").class_counts.local, 10);
assert.equal(byRoot.get("operator-profile-root").repo_count, 207);
assert.equal(byRoot.get("operator-profile-root").class_counts.public, 49);
assert.equal(byRoot.get("operator-profile-root").class_counts.local, 158);

const byLane = new Map(substrate.lane_families.map((lane) => [lane.id, lane]));
for (const id of [
  "public-flagship-and-second-level-repos",
  "local-only-tooling-and-prototypes",
  "agent-plugin-and-runtime-caches",
  "scratch-temp-and-build-fixtures",
  "ops-security-and-release-assurance",
  "creative-media-rendering-assets",
  "research-docs-and-attachments",
  "contracts-signing-and-sensitive-corpus"
]) {
  assert.ok(byLane.has(id), `missing lane family ${id}`);
}

assert.ok(byLane.get("creative-media-rendering-assets").host_flagships.includes("telos.creative.engine"));
assert.ok(byLane.get("ops-security-and-release-assurance").host_flagships.includes("crucible.review"));
assert.match(byLane.get("contracts-signing-and-sensitive-corpus").risk_boundary, /No raw corpus/);

for (const lane of substrate.lane_families) {
  assert.ok(lane.host_flagships.length > 0, `${lane.id} has flagship hosts`);
  assert.ok(lane.value.length > 0, `${lane.id} has value`);
  assert.ok(lane.risk_boundary.length > 0, `${lane.id} has risk boundary`);
  assert.ok(lane.first_action.length > 0, `${lane.id} has first action`);
}

const serialized = JSON.stringify(substrate);
for (const forbidden of [
  "C:/Users",
  "C:\\Users",
  "signer.",
  "auth_private",
  "PORTAL.md",
  "ZERO-TO-ACCESS",
  "private key"
]) {
  assert.equal(serialized.includes(forbidden), false, `forbidden private detail leaked: ${forbidden}`);
}

const cli = spawnSync(process.execPath, [path.join(here, "workstation-substrate.mjs")], {
  cwd: path.resolve(here, ".."),
  encoding: "utf8"
});
assert.equal(cli.status, 0, cli.stderr || cli.stdout);
assert.deepEqual(JSON.parse(cli.stdout), substrate);

const summary = spawnSync(process.execPath, [path.join(here, "workstation-substrate.mjs"), "--summary"], {
  cwd: path.resolve(here, ".."),
  encoding: "utf8"
});
assert.equal(summary.status, 0, summary.stderr || summary.stdout);
assert.match(summary.stdout, /Telos Workstation Substrate/);
assert.match(summary.stdout, /roots\s+2/);
assert.match(summary.stdout, /repos\s+331/);
assert.match(summary.stdout, /lanes\s+8/);
