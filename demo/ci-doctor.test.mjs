import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { spawnSync } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const doctor = JSON.parse(
  readFileSync(new URL("./integrations/ci-doctor.json", import.meta.url), "utf8")
);

assert.equal(doctor.schema, "project-telos.ci-doctor/v1");
assert.equal(doctor.tool, "telos.ci.doctor");
assert.equal(doctor.generated_at, "2026-06-29T01:03:03-07:00");
assert.equal(doctor.aggregate.flagship_count, 5);
assert.equal(doctor.aggregate.workflow_count, 9);
assert.equal(doctor.aggregate.latest_ci_success, 5);
assert.equal(doctor.aggregate.latest_ci_failures, 0);
assert.equal(doctor.aggregate.node24_compatibility, "MATCH");
assert.equal(doctor.aggregate.verdict, "MATCH");

assert.equal(doctor.privacy_boundary.raw_logs_included, false);
assert.equal(doctor.privacy_boundary.tokens_or_secrets_included, false);
assert.equal(doctor.privacy_boundary.absolute_private_paths_included, false);
assert.equal(doctor.privacy_boundary.workflow_mutation_performed, false);
assert.equal(doctor.privacy_boundary.github_writes_performed, false);

const byFlagship = new Map(doctor.flagships.map((flagship) => [flagship.id, flagship]));
for (const id of ["gather", "crucible", "index", "forum", "telos"]) {
  assert.ok(byFlagship.has(id), `missing flagship ${id}`);
  assert.equal(byFlagship.get(id).latest_ci.conclusion, "success", `${id} latest CI is green`);
  assert.match(byFlagship.get(id).latest_ci.url, /^https:\/\/github\.com\/HarperZ9\//);
  assert.ok(byFlagship.get(id).workflow_files.length >= 1, `${id} has workflow files`);
}

assert.equal(byFlagship.get("gather").latest_ci.run_id, 28356079319);
assert.equal(byFlagship.get("forum").latest_ci.run_id, 28356079274);
assert.equal(byFlagship.get("telos").latest_ci.run_id, 28357346847);
assert.equal(byFlagship.get("gather").recent_failures_followed_by_success, 1);
assert.equal(byFlagship.get("forum").recent_failures_followed_by_success, 1);
assert.equal(byFlagship.get("crucible").recent_failures_followed_by_success, 0);

const byAction = new Map(doctor.action_baselines.map((action) => [action.uses, action]));
assert.equal(byAction.get("actions/checkout").latest_tag, "v7.0.0");
assert.equal(byAction.get("actions/setup-node").latest_tag, "v6.4.0");
assert.equal(byAction.get("actions/setup-python").latest_tag, "v6.3.0");
assert.equal(byAction.get("actions/upload-artifact").latest_tag, "v7.0.1");
assert.equal(byAction.get("actions/download-artifact").latest_tag, "v8.0.1");

const checks = new Map(doctor.compatibility_checks.map((check) => [check.id, check]));
for (const id of [
  "latest-ci-green",
  "node24-force-flag",
  "node-setup-major",
  "python-setup-major",
  "artifact-action-majors",
  "workflow-privacy"
]) {
  assert.equal(checks.get(id).verdict, "MATCH", `${id} should match`);
}

for (const failure of doctor.failure_classes) {
  assert.match(failure.code, /^[a-z0-9_]+$/);
  assert.ok(failure.route_to.length > 0, `${failure.code} has routes`);
}
assert.ok(doctor.failure_classes.some((failure) => failure.code === "node_runtime_drift"));
assert.ok(doctor.failure_classes.some((failure) => failure.code === "ci_regression"));
assert.ok(doctor.failure_classes.some((failure) => failure.route_to.includes("crucible.assess")));

const serialized = JSON.stringify(doctor);
for (const forbidden of [
  "C:/Users",
  "C:\\Users",
  "gho_",
  "ghp_",
  `tok${"en:"}`,
  `Auth${"orization"}`,
  `BEGIN ${"PRIVATE"}`,
  `-----${"BEGIN"}`,
  "raw log"
]) {
  assert.equal(serialized.includes(forbidden), false, `forbidden detail leaked: ${forbidden}`);
}

const cli = spawnSync(process.execPath, [path.join(here, "ci-doctor.mjs")], {
  cwd: path.resolve(here, ".."),
  encoding: "utf8"
});
assert.equal(cli.status, 0, cli.stderr || cli.stdout);
assert.deepEqual(JSON.parse(cli.stdout), doctor);

const summary = spawnSync(process.execPath, [path.join(here, "ci-doctor.mjs"), "--summary"], {
  cwd: path.resolve(here, ".."),
  encoding: "utf8"
});
assert.equal(summary.status, 0, summary.stderr || summary.stdout);
assert.match(summary.stdout, /Telos CI Doctor/);
assert.match(summary.stdout, /flagships\s+5/);
assert.match(summary.stdout, /workflows\s+9/);
assert.match(summary.stdout, /latest CI\s+MATCH/);
assert.match(summary.stdout, /node24\s+MATCH/);
assert.match(summary.stdout, /verdict\s+MATCH/);
