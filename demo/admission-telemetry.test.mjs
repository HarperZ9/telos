import assert from "node:assert/strict";
import { readFileSync } from "node:fs";

const convention = JSON.parse(
  readFileSync(new URL("./integrations/admission-telemetry-conventions.json", import.meta.url), "utf8")
);

assert.equal(convention.schema, "project-telos.admission-telemetry/v1");
assert.deepEqual(convention.decision_outcomes, [
  "allow",
  "block",
  "escalate",
  "require_review"
]);
assert.deepEqual(convention.verification_verdicts, [
  "match",
  "drift",
  "unverifiable"
]);
assert.deepEqual(convention.failure_codes, [
  "binding_failed",
  "unjoinable_action",
  "verification_unverifiable",
  "stale_criterion",
  "policy_denied"
]);
assert.ok(convention.privacy.raw_prompt_allowed === false);
assert.ok(convention.privacy.raw_tool_args_allowed === false);
assert.ok(convention.required_fields.includes("decision.outcome"));
assert.ok(convention.required_fields.includes("verification.verdict"));
assert.ok(convention.required_fields.includes("expected_failure_code"));
assert.ok(convention.required_fields.includes("proposed.action_intent_id"));
assert.ok(convention.required_fields.includes("admission.action_intent_id"));
assert.ok(convention.required_fields.includes("execution.action_intent_id"));
assert.ok(convention.required_fields.includes("action.identity.action_id"));
assert.ok(convention.required_fields.includes("evidence.reference"));

const happyPath = convention.conformance_fixture.happy_path;
const proposed = happyPath.records.proposed_action;
const admission = happyPath.records.admission_record;
const execution = happyPath.records.execution_span;
assert.equal(proposed.action_intent_id, admission.action_intent_id);
assert.equal(admission.action_intent_id, execution.action_intent_id);
assert.equal(admission.args_hash, proposed.args_hash);
assert.equal(admission.criterion_ref, proposed.criterion_ref);
assert.equal(happyPath.resolved_criterion.criterion_ref, proposed.criterion_ref);
assert.equal(happyPath.resolved_criterion.evaluated, true);
assert.ok(Boolean(execution.result_ref || execution.result_hash));
assert.equal(happyPath.expected_failure_code, null);

const expectedCodesByCase = new Map([
  ["changed_args_hash", "binding_failed"],
  ["missing_action_intent_id", "unjoinable_action"],
  ["missing_verifier_result", "verification_unverifiable"],
  ["stale_or_unresolved_criterion_ref", "stale_criterion"],
  ["evaluated_policy_denial", "policy_denied"]
]);
const negativeCases = new Map(
  convention.negative_test_cases.map((item) => [item.name, item])
);
for (const [name, expectedCode] of expectedCodesByCase) {
  const item = negativeCases.get(name);
  assert.ok(item, `missing ${name}`);
  assert.equal(item.expected_failure_code, expectedCode);
}

const uniqueNegativeCodes = new Set(
  convention.negative_test_cases.map((item) => item.expected_failure_code)
);
assert.equal(uniqueNegativeCodes.size, convention.negative_test_cases.length);
for (const item of convention.negative_test_cases) {
  assert.ok(convention.failure_codes.includes(item.expected_failure_code));
  if (item.expected_failure_code !== "policy_denied") {
    assert.notEqual(item.decision, "allow");
  }
}

const policyDenied = negativeCases.get("evaluated_policy_denial");
assert.equal(policyDenied.decision, "block");
assert.equal(policyDenied.verification, "match");
assert.equal(policyDenied.requires.joined_action_intent_id, true);
assert.equal(policyDenied.requires.criterion_evaluated_against_proposed_action, true);

function collectKeys(value, keys = []) {
  if (Array.isArray(value)) {
    for (const item of value) {
      collectKeys(item, keys);
    }
    return keys;
  }
  if (value && typeof value === "object") {
    for (const [key, nested] of Object.entries(value)) {
      keys.push(key);
      collectKeys(nested, keys);
    }
  }
  return keys;
}

const fixtureRecordKeys = collectKeys(happyPath.records);
for (const prohibited of convention.conformance_fixture.privacy_prohibited_fields) {
  assert.ok(!fixtureRecordKeys.includes(prohibited), `raw field leaked: ${prohibited}`);
}

const unverifiable = convention.examples.find((item) => item.name === "unverifiable_requires_review");
assert.equal(unverifiable.decision.outcome, "require_review");
assert.equal(unverifiable.verification.verdict, "unverifiable");
