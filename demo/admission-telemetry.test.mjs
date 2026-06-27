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
assert.ok(convention.privacy.raw_prompt_allowed === false);
assert.ok(convention.privacy.raw_tool_args_allowed === false);
assert.ok(convention.required_fields.includes("decision.outcome"));
assert.ok(convention.required_fields.includes("verification.verdict"));
assert.ok(convention.required_fields.includes("action.identity.action_id"));
assert.ok(convention.required_fields.includes("evidence.reference"));

const negativeCases = new Set(convention.negative_test_cases.map((item) => item.name));
for (const name of [
  "changed_args",
  "missing_evidence",
  "stale_criterion",
  "missing_verifier_result",
  "unjoinable_action_identity"
]) {
  assert.ok(negativeCases.has(name), `missing ${name}`);
}

const unverifiable = convention.examples.find((item) => item.name === "unverifiable_requires_review");
assert.equal(unverifiable.decision.outcome, "require_review");
assert.equal(unverifiable.verification.verdict, "unverifiable");
