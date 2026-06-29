import assert from "node:assert/strict";
import { readFileSync } from "node:fs";

const fixture = JSON.parse(
  readFileSync(new URL("./integrations/agent-boundary-fixtures.json", import.meta.url), "utf8")
);

assert.equal(fixture.schema, "project-telos.agent-boundary-fixtures/v1");
assert.equal(fixture.stage, "public_synthetic_fixture_pack");
assert.deepEqual(fixture.verdicts, ["MATCH", "DRIFT", "UNVERIFIABLE"]);
assert.equal(fixture.privacy.raw_prompts_required, false);
assert.equal(fixture.privacy.raw_tool_args_required, false);
assert.equal(fixture.privacy.raw_reasoning_required, false);

const cases = new Map(fixture.cases.map((item) => [item.id, item]));
assert.equal(cases.size, 4);

for (const id of [
  "signed_approval_resume",
  "cancellation_partial_stream",
  "mcp_lifecycle_fake_recorder",
  "loop_guard_idempotency"
]) {
  assert.ok(cases.has(id), `missing fixture case ${id}`);
}

const approval = cases.get("signed_approval_resume");
assert.equal(approval.target.url, "https://github.com/vercel/ai/issues/16334");
assert.equal(approval.records.approval_request.envelope_immutable, true);
assert.equal(approval.records.approval_response.preserves_signature, true);
assert.equal(approval.records.resume_boundary.rejects_missing_signature, true);
assert.equal(approval.records.resume_boundary.rejects_mutated_args_hash, true);
assert.deepEqual(approval.expected_verdicts.map((item) => item.code), [
  "match",
  "signature_missing",
  "args_hash_changed"
]);

const cancellation = cases.get("cancellation_partial_stream");
assert.equal(cancellation.target.url, "https://github.com/langchain-ai/langgraph/issues/5672");
assert.equal(cancellation.records.terminal_receipt.terminal_status, "partial");
assert.equal(cancellation.records.terminal_receipt.last_stream_sequence_seen > 0, true);
assert.equal(cancellation.records.terminal_receipt.resume_policy, "reconcile");
assert.ok(cancellation.expected_verdicts.some((item) => item.code === "streamed_state_not_checkpointed"));

const mcp = cases.get("mcp_lifecycle_fake_recorder");
assert.equal(mcp.target.url, "https://github.com/modelcontextprotocol/python-sdk/issues/421");
assert.equal(mcp.contract.otel_hard_dependency_required, false);
assert.deepEqual(mcp.records.lifecycle_events.map((event) => event.kind), [
  "send_request",
  "handle_request",
  "tool_call",
  "tool_result",
  "span_end"
]);
assert.equal(mcp.records.lifecycle_events.every((event) => event.request_id === "req_mcp_421_001"), true);
assert.equal(mcp.records.lifecycle_events[3].mcp_is_error, true);
assert.equal(mcp.records.lifecycle_events[3].result_state, "failed");

const loop = cases.get("loop_guard_idempotency");
assert.equal(loop.target.url, "https://github.com/continuedev/continue/issues/12702");
assert.equal(loop.records.guard_state.identical_tool_call_count, 3);
assert.equal(loop.records.guard_state.max_identical_tool_calls, 2);
assert.equal(loop.records.guard_state.terminal_status, "blocked");
assert.equal(loop.records.guard_state.stop_reason, "idempotency_guard");
assert.ok(loop.expected_verdicts.some((item) => item.code === "repeat_tool_call_blocked"));

for (const item of fixture.cases) {
  assert.match(item.fixture_hash, /^sha256:[a-f0-9]{64}$/);
  assert.equal(item.public_links_ok, true);
  assert.ok(["MATCH", "DRIFT", "UNVERIFIABLE"].includes(item.default_verdict));
  assert.equal(item.requires_live_service, false);
}
