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

const relevance = convention.conformance_fixture.context_relevance;
const contextReceiptContract = relevance.receipt_contract;
assert.equal(
  contextReceiptContract.load_receipt.decisionClaim,
  "valid_load_receipt_not_usefulness_claim"
);
assert.equal(contextReceiptContract.load_receipt.claims_usefulness, false);
assert.equal(contextReceiptContract.load_receipt.raw_payload_required, false);
assert.equal(contextReceiptContract.relevance_receipt.optional, true);
assert.equal(contextReceiptContract.relevance_receipt.only_valid_when_joined_to_loaded_inputs, true);
assert.deepEqual(contextReceiptContract.relevance_receipt.required_join_fields, [
  "input_id",
  "delivered_hash"
]);

const loadOnly = relevance.load_only_variant;
assert.equal(loadOnly.decisionClaim, "valid_load_receipt_not_usefulness_claim");
assert.equal(loadOnly.relevance_event, null);
assert.equal(loadOnly.claims_usefulness, false);
assert.equal(loadOnly.expected_verdict, "MATCH");
assert.equal(loadOnly.selected_count, relevance.selection.selected_count);
assert.deepEqual(
  loadOnly.loaded_input_ids,
  relevance.loaded_inputs.map((input) => input.input_id)
);

assert.equal(relevance.selection.selected_count, 3);
assert.equal(relevance.selection.delivered_count, 3);
assert.equal(relevance.selection.suppressed_count, 1);
assert.equal(
  relevance.selection.selected_count,
  relevance.relevance.decisive_count +
    relevance.relevance.supporting_count +
    relevance.relevance.unused_count +
    relevance.relevance.unknown_count
);

for (const loaded of relevance.loaded_inputs) {
  assert.match(loaded.source_hash, /^sha256:[a-f0-9]{64}$/);
  assert.match(loaded.delivered_hash, /^sha256:[a-f0-9]{64}$/);
  assert.equal("relevance_label" in loaded, false, "load event must not claim later relevance");
  assert.equal("raw_context" in loaded, false, "load event must not expose raw context");
}

for (const suppressed of relevance.suppressed_inputs) {
  assert.match(suppressed.source_hash, /^sha256:[a-f0-9]{64}$/);
  assert.equal("raw_context" in suppressed, false, "suppressed event must not expose raw context");
}

for (const ref of relevance.relevance.input_refs) {
  assert.equal("raw_context" in ref, false, "relevance event must not expose raw context");
  assert.ok(["decisive", "supporting", "unused", "unknown"].includes(ref.relevance));
  const loaded = relevance.loaded_inputs.find((input) => input.input_id === ref.input_id);
  assert.ok(loaded, `relevance references input that was not delivered: ${ref.input_id}`);
  assert.equal(ref.delivered_hash, loaded.delivered_hash, `relevance hash drifted for ${ref.input_id}`);
}

const negativeCodes = new Set(convention.negative_test_cases.map((item) => item.failure_code));
assert.equal(negativeCodes.size, convention.negative_test_cases.length);
for (const code of convention.failure_codes) {
  assert.ok(negativeCodes.has(code), `failure code lacks negative case: ${code}`);
}
for (const code of ["missing_relevance", "over_selection", "unjoinable_relevance"]) {
  assert.ok(negativeCodes.has(code), `context evidence taxonomy missing ${code}`);
}
for (const item of convention.negative_test_cases) {
  assert.notEqual(item.expected_verdict, "MATCH");
}

assert.ok(convention.quality_gates.readability.some((gate) => gate.includes("small named helpers")));
assert.ok(convention.quality_gates.large_workspace.some((gate) => gate.includes("expand exact source refs")));
assert.ok(convention.quality_gates.unattended_agent.some((gate) => gate.includes("git status")));
