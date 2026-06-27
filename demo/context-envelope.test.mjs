import assert from "node:assert/strict";
import { readFileSync } from "node:fs";

const convention = JSON.parse(
  readFileSync(new URL("./integrations/context-envelope-conventions.json", import.meta.url), "utf8")
);

assert.equal(convention.schema, "project-telos.context-envelope/v1");
assert.equal(convention.contract.hidden_payloads_allowed, false);
assert.equal(convention.contract.steganography_for_required_context_allowed, false);
assert.equal(convention.contract.lossless_requirement.includes("source refs"), true);
assert.equal(convention.contract.model_visible_context.includes("compact"), true);
assert.equal(convention.contract.authoritative_context.includes("hash-addressed"), true);

for (const field of [
  "envelope_id",
  "workspace.root_hash",
  "context_budget.target_packet_tokens",
  "compression.lossless_by_ref",
  "source_refs[].content_hash",
  "source_refs[].expansion_command",
  "summary.claims[].source_ref_ids",
  "receipt_chain[].receipt_hash",
  "quality_gates.readability",
  "failure_code"
]) {
  assert.ok(convention.required_fields.includes(field), `missing required field ${field}`);
}

for (const tool of ["gather", "index", "forum", "crucible", "telos"]) {
  assert.ok(Array.isArray(convention.flagship_roles[tool]), `missing role for ${tool}`);
  assert.ok(convention.flagship_roles[tool].length >= 2, `thin role for ${tool}`);
}

const happyPath = convention.conformance_fixture.happy_path;
assert.equal(happyPath.compression.lossless_by_ref, true);
assert.equal(happyPath.compression.hidden_payloads_used, false);
assert.equal(happyPath.quality_gates.readability, "MATCH");
assert.equal(happyPath.quality_gates.test_evidence, "MATCH");
assert.equal(happyPath.failure_code, null);

const sourceRefs = new Map(happyPath.source_refs.map((ref) => [ref.id, ref]));
for (const ref of sourceRefs.values()) {
  assert.match(ref.content_hash, /^sha256:[a-f0-9]{64}$/);
  assert.ok(ref.path.length > 0);
  assert.ok(ref.range.length > 0);
  assert.ok(ref.expansion_command.length > 0);
}

for (const claim of happyPath.summary.claims) {
  assert.ok(claim.source_ref_ids.length > 0);
  for (const refId of claim.source_ref_ids) {
    assert.ok(sourceRefs.has(refId), `claim references unknown source ref ${refId}`);
  }
}

for (const receipt of happyPath.receipt_chain) {
  assert.match(receipt.receipt_hash, /^sha256:[a-f0-9]{64}$/);
}

const negativeCodes = new Set(convention.negative_test_cases.map((item) => item.failure_code));
assert.equal(negativeCodes.size, convention.negative_test_cases.length);
for (const code of convention.failure_codes) {
  assert.ok(negativeCodes.has(code), `failure code lacks negative case: ${code}`);
}
for (const item of convention.negative_test_cases) {
  assert.notEqual(item.expected_verdict, "MATCH");
}

assert.ok(convention.quality_gates.readability.some((gate) => gate.includes("small named helpers")));
assert.ok(convention.quality_gates.large_workspace.some((gate) => gate.includes("expand exact source refs")));
assert.ok(convention.quality_gates.unattended_agent.some((gate) => gate.includes("git status")));
