# Pass 0014 Promotion-Control Steelman

Date: 2026-07-01

Status: `UNVERIFIABLE` for Forum submit; `MATCH` for local adversarial analysis.

## Forum Tool Receipt

Forum status remains reachable through the operator-spine status tool:

```text
tool_version=1.12.0
status=MATCH
role=orchestration-routing
```

Forum submit still fails:

```json
{
  "error": "the configured executor did not return valid JSON; point the daemon at a real model executor (could not parse JSON from output: Extra data: line 2 column 1 (char 98))"
}
```

Therefore this pass does not claim a witnessed Forum adversarial answer.

## Steelman Objections

### Objection 1: Hardware Mock Metadata Can Still Mislead

The mock receipt intentionally contains cloud-task-shaped fields. That is useful for UI and adapter development, but a reader could still infer real hardware if the UI hides `branch=HARDWARE_MOCK` or `hardware_claim_allowed=false`.

Required hardening:

- branch label must be visible in human reports;
- hardware mock receipts must render with a non-hardware warning;
- any claim using mock task metadata as hardware evidence must fail validation.

### Objection 2: Adapter Fixtures Are Shape Tests, Not Full Parser Compatibility

The Qiskit/OpenQASM and Cirq JSON fixtures only prove the local normalized circuit shape. They do not prove full SDK compatibility, dynamic circuit support, hardware compilation, or round-trip equivalence.

Required hardening:

- mark adapter fixture status as shape-level only;
- add real SDK adapter tests later when dependencies are pinned;
- record SDK version and parser/exporter version in production receipts.

### Objection 3: Resource Estimate Receipts Can Be Overclaimed

Resource estimates can be treated as computational results by non-expert readers. The pass 0014 receipt prevents this by setting `execution_claim_allowed=false`, but future UI and APIs must preserve that bit.

Required hardening:

- resource-estimate reports must display `ESTIMATE_ONLY_NOT_EXECUTION`;
- execution result fields must not be satisfiable by resource estimate fields;
- benchmark or advantage claims need both estimate and execution receipts.

### Objection 4: Metric Binding Needs Claim-Specific Validators

The pass binds metric families, but a generic validator cannot know every scientific claim's sufficient evidence.

Required hardening:

- every domain proof packet should include a claim-to-metric map;
- validator contracts should reject claims without sufficient metrics;
- domain adapters should expose metric provenance, not just metric values.

### Objection 5: Cloud Hardware Requires Provider-Specific Receipts

A generic `CLOUD_HARDWARE` branch is insufficient for production. Providers differ in task ids, result payloads, calibration APIs, compilation pipelines, and billing/runtime metadata.

Required hardening:

- add provider-specific receipt profiles;
- require task result payload hashes;
- include calibration or device-properties reference;
- record transpilation/compilation path;
- include queue, run, and retrieval timestamps.

## Verdict

Pass 0014 correctly hardens the most important branch-promotion failures, but it remains a fixture-level pass. The next serious step is provider-specific receipt profiles and real SDK adapter tests.

