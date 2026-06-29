import assert from "node:assert/strict";
import { mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { spawnSync } from "node:child_process";
import { tmpdir } from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { buildTriagePacket, classifyLogText } from "./ci-triage.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));

const seedLog = `
[doctest] test cases:   3699 |   3698 passed | 1 failed | 1 skipped
[doctest] Status: FAILURE!
Write-Error: 1 test(s) failed
##[error]Process completed with exit code 1.
Node 20 is being deprecated. This workflow is running with Node 24 by default.
##[warning]Node.js 20 is deprecated. The following actions target Node.js 20 but are being forced to run on Node.js 24: actions/cache@v4, actions/checkout@v4, actions/upload-artifact@v4, ilammy/msvc-dev-cmd@v1.
`;

const formatLog = `
Run cargo fmt --check
Diff in /home/runner/work/quantalang/quantalang/compiler/src/codegen/backend/c.rs:241:
-                                kind: TypeDefKind::Struct { fields, packed: false },
+                                kind: TypeDefKind::Struct {
##[error]Process completed with exit code 1.
`;

const warningOnlyLog = `
Node 20 is being deprecated. This workflow is running with Node 24 by default.
##[warning]Node.js 20 is deprecated. The following actions target Node.js 20 but are being forced to run on Node.js 24: actions/checkout@v4, actions/upload-artifact@v4.
`;

const seed = classifyLogText(seedLog, {
  repo: "HarperZ9/seed",
  run_id: 28346374847,
  workflow: "WARDEN CI"
});
assert.equal(seed.verdict, "DRIFT");
assert.equal(seed.blocking_failure, true);
assert.deepEqual(seed.failure_codes, ["test_gate_failed"]);
assert.ok(seed.warning_codes.includes("node_runtime_migration_warning"));
assert.ok(seed.warning_codes.includes("javascript_action_node20_forced_node24"));
assert.ok(seed.action_refs.includes("actions/checkout@v4"));
assert.equal(seed.route_to.includes("crucible.assess"), true);
assert.equal(JSON.stringify(seed).includes(seedLog), false, "raw log must not be included");

const fmt = classifyLogText(formatLog, {
  repo: "HarperZ9/quantalang",
  run_id: 28342495903,
  workflow: "CI"
});
assert.equal(fmt.verdict, "DRIFT");
assert.deepEqual(fmt.failure_codes, ["rust_format_failure"]);
assert.deepEqual(fmt.warning_codes, []);
assert.equal(fmt.remediation_kind, "format_source");

const warningOnly = classifyLogText(warningOnlyLog, {
  repo: "HarperZ9/seed",
  run_id: 28353077838,
  workflow: "WARDEN CI"
});
assert.equal(warningOnly.blocking_failure, false);
assert.equal(warningOnly.verdict, "MATCH");
assert.deepEqual(warningOnly.failure_codes, []);
assert.deepEqual(warningOnly.warning_codes, [
  "node_runtime_migration_warning",
  "javascript_action_node20_forced_node24"
]);
assert.equal(warningOnly.remediation_kind, "workflow_runtime_migration");

const packet = buildTriagePacket({
  cases: [
    { id: "seed-failed", log_text: seedLog, repo: "HarperZ9/seed", run_id: 28346374847, workflow: "WARDEN CI" },
    { id: "quantalang-format", log_text: formatLog, repo: "HarperZ9/quantalang", run_id: 28342495903, workflow: "CI" },
    { id: "warning-only", log_text: warningOnlyLog, repo: "HarperZ9/seed", run_id: 28353077838, workflow: "WARDEN CI" }
  ],
  generatedAt: "2026-06-29T00:00:00.000Z"
});
assert.equal(packet.schema, "project-telos.ci-triage/v1");
assert.equal(packet.tool, "telos.ci.triage");
assert.equal(packet.generated_at, "2026-06-29T00:00:00.000Z");
assert.equal(packet.aggregate.case_count, 3);
assert.equal(packet.aggregate.blocking_failure_count, 2);
assert.equal(packet.aggregate.runtime_warning_count, 2);
assert.equal(packet.aggregate.ci_result_verdict, "DRIFT");
assert.equal(packet.aggregate.runtime_migration_verdict, "DRIFT");
assert.equal(packet.aggregate.verdict, "DRIFT");
assert.deepEqual(packet.aggregate.failure_codes, ["test_gate_failed", "rust_format_failure"]);
assert.ok(packet.aggregate.warning_codes.includes("node_runtime_migration_warning"));
assert.equal(packet.privacy_boundary.raw_logs_included, false);
assert.equal(packet.privacy_boundary.tokens_or_secrets_included, false);

const serialized = JSON.stringify(packet);
for (const forbidden of ["C:/Users", "C:\\Users", "gho_", "ghp_", "Authorization", seedLog, formatLog]) {
  assert.equal(serialized.includes(forbidden), false, `forbidden detail leaked: ${forbidden}`);
}

const tempRoot = mkdtempSync(path.join(tmpdir(), "telos-ci-triage-"));
try {
  const fixturePath = path.join(tempRoot, "triage.json");
  writeFileSync(fixturePath, JSON.stringify({ cases: packet.cases.map((item) => ({
    id: item.id,
    repo: item.repo,
    run_id: item.run_id,
    workflow: item.workflow,
    log_text: item.evidence_excerpt
  })) }, null, 2));
  const cli = spawnSync(process.execPath, [path.join(here, "ci-triage.mjs"), "--input", fixturePath], {
    cwd: path.resolve(here, ".."),
    encoding: "utf8"
  });
  assert.equal(cli.status, 0, cli.stderr || cli.stdout);
  assert.equal(JSON.parse(cli.stdout).aggregate.case_count, 3);

  const summary = spawnSync(process.execPath, [path.join(here, "ci-triage.mjs"), "--input", fixturePath, "--summary"], {
    cwd: path.resolve(here, ".."),
    encoding: "utf8"
  });
  assert.equal(summary.status, 0, summary.stderr || summary.stdout);
  assert.match(summary.stdout, /Telos CI Triage/);
  assert.match(summary.stdout, /cases\s+3/);
  assert.match(summary.stdout, /blocking\s+2/);
  assert.match(summary.stdout, /runtime\s+DRIFT/);
  assert.match(summary.stdout, /verdict\s+DRIFT/);
} finally {
  rmSync(tempRoot, { recursive: true, force: true });
}
