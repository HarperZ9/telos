import assert from "node:assert/strict";
import { readFileSync } from "node:fs";

const convention = JSON.parse(
  readFileSync(new URL("./integrations/action-receipt-conventions.json", import.meta.url), "utf8")
);

assert.equal(convention.schema, "project-telos.action-receipt/v1");
assert.equal(convention.contract.raw_parameters_required, false);
assert.equal(convention.contract.digest_references_required, true);
assert.equal(convention.contract.append_only_compensation_required, true);
assert.equal(convention.contract.adapter_boundary.includes("Signing"), true);
assert.equal(convention.contract.receipt_is_trace_span, false);
assert.equal(convention.contract.proposed_completed_action_separation_required, true);
assert.equal(convention.contract.exportable_outside_trace_retention, true);

assert.equal(convention.trace_relation.receipt_is_trace_span, false);
assert.equal(convention.trace_relation.links_to_trace_span, true);
assert.equal(convention.trace_relation.survives_trace_retention, true);
assert.deepEqual(convention.trace_relation.required_join_fields, [
  "action_intent_id",
  "trace.span_ref",
  "execution.external_request_id",
  "execution.idempotency_key"
]);

for (const field of [
  "input_materials[].digest",
  "component.version",
  "component.config_hash",
  "action.kind",
  "intent_ref",
  "authority_ref",
  "execution_ref",
  "evidence_ref",
  "review_ref",
  "compensation_ref",
  "trace.span_ref",
  "execution.external_request_id",
  "execution.idempotency_key",
  "execution.terminal_status",
  "execution.redacted_before_ref",
  "execution.redacted_after_ref",
  "side_effect.class",
  "result.stop_reason",
  "verification.verdict",
  "policy.decision",
  "policy.ref",
  "persistence.append_only"
]) {
  assert.ok(convention.required_fields.includes(field), `missing required field ${field}`);
}

assert.deepEqual(convention.state_model.verification_verdicts, ["MATCH", "DRIFT", "UNVERIFIABLE"]);
assert.ok(convention.state_model.side_effect_classes.includes("external_call"));
assert.ok(convention.state_model.typed_stop_reasons.includes("policy_denied"));
assert.ok(convention.state_model.typed_stop_reasons.includes("verification_unverifiable"));

for (const kind of [
  "payment",
  "purchase",
  "refund",
  "booking",
  "email",
  "ticket",
  "file_write",
  "deployment",
  "database_write",
  "pull_request",
  "account_setting",
  "message"
]) {
  assert.ok(convention.external_action_kinds.includes(kind), `missing external action kind ${kind}`);
}

const event = convention.conformance_fixture.happy_path;
assert.match(event.component.config_hash, /^sha256:[a-f0-9]{64}$/);
assert.match(event.input_materials[0].digest, /^sha256:[a-f0-9]{64}$/);
assert.equal(event.side_effect.class, "read");
assert.equal(event.policy.decision, "allow");
assert.equal(event.policy.ref.length > 0, true);
assert.equal(event.verification.verdict, "MATCH");
assert.equal(event.result.stop_reason, "completed");
assert.equal(event.persistence.append_only, true);

const failedToolCall = convention.conformance_fixture.failed_tool_call;
assert.equal(convention.contract.failure_typed_persistence_required, true);
assert.equal(failedToolCall.event_type, "execution_failed");
assert.equal(failedToolCall.result.state, "failed");
assert.equal(failedToolCall.result.stop_reason, "tool_error");
assert.equal(failedToolCall.result.error_payload_ref.length > 0, true);
assert.match(failedToolCall.result.error_payload_digest, /^sha256:[a-f0-9]{64}$/);

for (const surface of ["stream_chunk", "persisted_message_part", "trace_span", "scorer_eval_input"]) {
  assert.equal(
    failedToolCall.failure_surfaces[surface].failure_typed,
    true,
    `${surface} must preserve failure typing`
  );
  assert.equal(
    failedToolCall.failure_surfaces[surface].payload_preserved,
    true,
    `${surface} must preserve the failure payload reference`
  );
}

const compensation = convention.conformance_fixture.append_only_compensation;
assert.equal(compensation.compensates, event.action_id);
assert.equal(compensation.result.state, "compensated");
assert.equal(compensation.persistence.append_only, true);
assert.notEqual(compensation.event_id, event.event_id);

const externalWrite = convention.conformance_fixture.external_write_completed;
assert.equal(externalWrite.event_type, "external_write_completed");
assert.equal(externalWrite.action.kind, "message");
assert.equal(externalWrite.intent_ref.startsWith("intent:"), true);
assert.equal(externalWrite.authority_ref.startsWith("approval:"), true);
assert.equal(externalWrite.execution_ref.startsWith("external:"), true);
assert.equal(externalWrite.evidence_ref.startsWith("artifact:"), true);
assert.equal(externalWrite.review_ref.startsWith("review:"), true);
assert.equal(externalWrite.compensation_ref, null);
assert.equal(externalWrite.trace.receipt_is_trace_span, false);
assert.equal(externalWrite.trace.span_ref.length > 0, true);
assert.equal(externalWrite.execution.external_request_id.length > 0, true);
assert.equal(externalWrite.execution.idempotency_key.length > 0, true);
assert.equal(externalWrite.execution.terminal_status, "completed");
assert.equal(externalWrite.execution.redacted_before_ref.length > 0, true);
assert.equal(externalWrite.execution.redacted_after_ref.length > 0, true);
assert.match(externalWrite.execution.result_hash, /^sha256:[a-f0-9]{64}$/);
assert.equal(externalWrite.privacy.raw_prompt_required, false);
assert.equal(externalWrite.privacy.raw_tool_args_required, false);
assert.equal(externalWrite.privacy.raw_external_payload_required, false);
assert.equal(externalWrite.report_boundaries.proposed_action_is_completed_action, false);

const sourceCorrection = convention.source_corrections.find(
  (item) => item.submitted_ref === "https://arxiv.org/abs/2605.22967"
);
assert.equal(sourceCorrection?.verdict, "DRIFT");
assert.equal(sourceCorrection?.replacement_ref, "https://arxiv.org/abs/2604.15367");

const negativeCodes = new Set(convention.negative_test_cases.map((item) => item.failure_code));
assert.equal(negativeCodes.size, convention.negative_test_cases.length);
for (const code of convention.failure_codes) {
  assert.ok(negativeCodes.has(code), `failure code lacks negative case: ${code}`);
}

for (const adapter of ["receptor", "signing", "anchor", "storage"]) {
  assert.ok(convention.adapter_interfaces[adapter], `missing ${adapter} adapter`);
}
