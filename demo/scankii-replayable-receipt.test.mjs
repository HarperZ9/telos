import assert from "node:assert/strict";
import { readFileSync } from "node:fs";

const receipt = JSON.parse(
  readFileSync(new URL("./integrations/scankii-synthetic-receipt.json", import.meta.url), "utf8")
);

assert.equal(receipt.schema, "project-telos.scankii-dogfood-receipt/v1");
assert.equal(receipt.scanner.name, "scankii");
assert.equal(receipt.scanner.source_branch, "feature/replayable-receipt");
assert.match(receipt.scanner.source_commit, /^[a-f0-9]{40}$/);
assert.equal(receipt.scanner_run.exit_code, 0);
assert.equal(receipt.scanner_run.corpus_path, "demo/integrations/scankii-synthetic-corpus");
assert.equal(receipt.scanner_run.raw_output_committed, false);
assert.ok(receipt.scanner_run.raw_output_not_committed_reason.toLowerCase().includes("absolute"));

const findings = receipt.findings;

assert.ok(findings.length >= 3, "expected at least three synthetic findings");

const byFile = new Map();
for (const finding of findings) {
  const file = String(finding.file_path || "");
  if (file) {
    byFile.set(file.replaceAll("\\", "/"), finding);
  }
  assert.equal(file.startsWith("demo/integrations/scankii-synthetic-corpus/"), true);
  assert.equal(file.includes("C:"), false, "receipt must not commit absolute Windows paths");
  assert.equal(file.startsWith("/"), false, "receipt must not commit absolute POSIX paths");
}

const stdoutFinding = findFinding("stdout-logging-skill");
const networkFinding = findFinding("network-sink-skill");
const unresolvedFinding = findFinding("unresolved-boundary-skill");

for (const finding of [stdoutFinding, networkFinding, unresolvedFinding]) {
  assert.ok(finding.scankii_version || receipt.scanner.version, "missing scankii version");
  assert.match(String(finding.file_hash), /^sha256:[a-f0-9]{64}$/, "missing stable file hash");
  assert.match(String(finding.fragment_hash), /^sha256:[a-f0-9]{64}$/, "missing stable fragment hash");
  assert.equal(finding.observed_static, true, "finding must state static observation");
  assert.equal(finding.raw_window_text_committed, false, "raw finding text should not be committed");
}

assert.equal(receipt.shape_status, "DRIFT");
const driftCodes = new Set(receipt.drift_cases.map((item) => item.code));
for (const code of [
  "pip_git_checkout_failed_windows_trailing_space_path",
  "wheel_missing_rules_package_data",
  "ast_sink_correlation_missing",
  "raw_output_absolute_paths",
  "raw_hashes_lack_algorithm_prefix",
  "network_runtime_witness_not_set",
  "containment_not_sink_specific",
  "unresolved_dependency_boundary_not_detected"
]) {
  assert.ok(driftCodes.has(code), `missing drift case ${code}`);
}

assert.equal(stdoutFinding.expected_containment, "redact");
assert.equal(stdoutFinding.observed_containment, "UNVERIFIABLE");
assert.equal(networkFinding.expected_requires_runtime_witness, true);
assert.equal(networkFinding.observed_requires_runtime_witness, false);
assert.equal(unresolvedFinding.expected_unverifiable_static_boundary, true);
assert.equal(unresolvedFinding.observed_unverifiable_static_boundary, false);

function findFinding(fragment) {
  for (const [file, finding] of byFile.entries()) {
    if (file.includes(fragment)) {
      return finding;
    }
  }

  assert.fail(`missing finding for ${fragment}`);
}
