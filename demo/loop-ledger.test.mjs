import assert from "node:assert/strict";
import { readFileSync } from "node:fs";

const convention = JSON.parse(
  readFileSync(new URL("./integrations/loop-ledger-conventions.json", import.meta.url), "utf8")
);

assert.equal(convention.schema, "project-telos.loop-ledger/v1");
assert.equal(convention.contract.ledger_first_class, true);
assert.equal(convention.contract.todo_is_current_turn_scratchpad, true);
assert.equal(convention.contract.fresh_context_reads_ledger_first, true);
assert.equal(convention.contract.one_action_per_iteration, true);
assert.equal(convention.contract.unverifiable_must_not_inherit_confidence, true);

for (const field of [
  "id",
  "status",
  "claim",
  "action",
  "evidence[]",
  "verdict",
  "next",
  "updated_at"
]) {
  assert.ok(convention.ledger_entry.required_fields.includes(field), `missing ${field}`);
}

assert.deepEqual(convention.ledger_entry.status_values, ["pending", "active", "blocked", "done"]);
assert.deepEqual(convention.ledger_entry.verdict_values, ["MATCH", "DRIFT", "UNVERIFIABLE"]);
assert.deepEqual(convention.ledger_entry.next_values, ["resume", "ask_user", "retry", "stop"]);

assert.equal(convention.fresh_context_iteration.steps[0], "read_ledger");
assert.ok(convention.fresh_context_iteration.steps.includes("write_result_evidence_verdict"));
assert.ok(convention.fresh_context_iteration.stop_conditions.includes("UNVERIFIABLE"));
assert.ok(convention.fresh_context_iteration.stop_conditions.includes("ask_user"));

assert.equal(convention.headless_scheduled_fire.open_ended_goal_loop_allowed, false);
assert.equal(convention.headless_scheduled_fire.max_iterations_required, true);
assert.equal(convention.headless_scheduled_fire.per_fire_timeout_required, true);
assert.equal(convention.headless_scheduled_fire.cancellation_required, true);
assert.equal(convention.headless_scheduled_fire.dangerous_actions_always_denied, true);
assert.deepEqual(convention.headless_scheduled_fire.terminal_status_values, [
  "ok",
  "error",
  "cancelled",
  "needs_attention"
]);
assert.equal(convention.headless_scheduled_fire.ask_user_mid_fire_status, "needs_attention");

const happy = convention.conformance_fixture.happy_path;
assert.equal(happy.entry.verdict, "MATCH");
assert.equal(happy.iteration.selected_action, happy.entry.action);
assert.ok(happy.iteration.evidence_added.length > 0);

const blocked = convention.conformance_fixture.ask_user_escape;
assert.equal(blocked.entry.next, "ask_user");
assert.equal(blocked.headless_result.status, "needs_attention");
assert.equal(blocked.headless_result.continued_with_dismissed_answer, false);

const codes = new Set(convention.negative_test_cases.map((item) => item.failure_code));
assert.equal(codes.size, convention.negative_test_cases.length);
for (const code of convention.failure_codes) {
  assert.ok(codes.has(code), `failure code lacks negative case: ${code}`);
}
