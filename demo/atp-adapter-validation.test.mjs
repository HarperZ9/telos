import assert from "node:assert/strict";
import { readFileSync } from "node:fs";

const fixture = JSON.parse(
  readFileSync(new URL("./integrations/atp-adapter-validation.json", import.meta.url), "utf8")
);

assert.equal(fixture.schema, "project-telos.atp-adapter-validation/v1");
assert.equal(fixture.protocol.name, "Agent Transaction Protocol");
assert.equal(fixture.protocol.version, "1.2.0");
assert.equal(fixture.validation_scope.claims_production_readiness, false);
assert.equal(fixture.validation_scope.requires_live_atp_server, false);
assert.equal(fixture.validation_scope.signing_anchoring_storage_validated, false);

const sourceNames = new Set(fixture.sources_checked.map((source) => source.name));
for (const source of [
  "Haystack ATP feedback thread",
  "ATP v1.2.0 branch",
  "ATP transaction spec",
  "ATP TypeScript example",
  "ATP Python example",
  "ATP cURL example"
]) {
  assert.ok(sourceNames.has(source), `missing source evidence: ${source}`);
}

for (const requiredField of [
  "atp_version",
  "action_id",
  "idempotency_key",
  "guarantee_level",
  "agent_id",
  "input_digest",
  "material_digest",
  "side_effect_class",
  "component_version",
  "config_hash",
  "policy.decision",
  "result.stop_reason",
  "verification.verdict"
]) {
  assert.ok(fixture.required_fields.includes(requiredField), `missing ATP field ${requiredField}`);
}

assert.deepEqual(fixture.allowed_values.verification_verdicts, ["MATCH", "DRIFT", "UNVERIFIABLE"]);
assert.deepEqual(fixture.allowed_values.side_effect_classes, ["read", "write", "external", "human"]);
assert.ok(fixture.allowed_values.policy_decisions.includes("APPROVED"));
assert.ok(fixture.allowed_values.stop_reasons.includes("policy_denied"));

const cases = new Map(fixture.validation_cases.map((item) => [item.id, item]));
for (const id of [
  "gather.intake.digest_refs",
  "index.workspace_map.config_hash",
  "forum.route.policy_action",
  "crucible.verdict.unverifiable",
  "telos.compensation.append_only"
]) {
  assert.ok(cases.has(id), `missing validation case ${id}`);
}

for (const item of cases.values()) {
  assert.equal(item.raw_payload_required, false, `${item.id} should not require raw payloads`);
  assert.match(item.input_digest, /^sha256:[a-f0-9]{64}$/);
  assert.match(item.material_digest, /^sha256:[a-f0-9]{64}$/);
  assert.match(item.config_hash, /^sha256:[a-f0-9]{64}$/);
  assert.ok(fixture.allowed_values.side_effect_classes.includes(item.side_effect_class));
  assert.ok(fixture.allowed_values.policy_decisions.includes(item.policy.decision));
  assert.ok(fixture.allowed_values.verification_verdicts.includes(item.verification.verdict));
  assert.ok(fixture.allowed_values.stop_reasons.includes(item.result.stop_reason));
  assert.notEqual(
    item.policy.decision,
    item.verification.verdict,
    `${item.id} collapsed policy decision and verification verdict`
  );
}

const compensation = cases.get("telos.compensation.append_only");
assert.equal(compensation.event_type, "compensation");
assert.equal(compensation.compensates, "act_forum_route_001");
assert.equal(compensation.original_action_snapshot.action_id, "act_forum_route_001");
assert.equal(compensation.original_action_snapshot.result.state, "COMPLETED");
assert.equal(compensation.original_action_snapshot.mutated_by_compensation, false);
assert.equal(compensation.derived_views.compensated_by, compensation.action_id);

const unverifiable = cases.get("crucible.verdict.unverifiable");
assert.equal(unverifiable.verification.verdict, "UNVERIFIABLE");
assert.equal(unverifiable.result.stop_reason, "verification_unverifiable");
assert.notEqual(unverifiable.policy.decision, "DENIED");

const negativeCodes = new Set(fixture.negative_cases.map((item) => item.failure_code));
assert.equal(negativeCodes.size, fixture.negative_cases.length);
for (const code of fixture.failure_codes) {
  assert.ok(negativeCodes.has(code), `failure code lacks negative case: ${code}`);
}

for (const route of [
  "/v1/transaction/create-transaction",
  "/v1/transaction/commit",
  "/v1/transaction/compensate",
  "/v1/transaction/{action_id}/status",
  "/v1/transaction/{action_id}/verify"
]) {
  assert.ok(fixture.adapter_operations.includes(route), `missing adapter operation ${route}`);
}
