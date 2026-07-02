# Dogfood Pass 0014 Ledger

Date: 2026-07-01

Status: `CRUCIBLE_MATCH`.

Crucible assessment:

- thesis id: `c21d40b308c02a39`;
- claims: `8`;
- match: `8`;
- drift: `0`;
- unverifiable: `0`;
- thesis seal: `c21d40b308c02a3943bb16e09826858dc5ebf9245cfe10d3e6609d9f08d8cccf`;
- verdict seal: `954a018b4c4a40ac7d4047dd939562679bcfb2768441bb6d4c7eaa6dca721636`;
- measurement seal: `924d32a353caa48e5599fa32fb96b6eb2382627de88a54d8ffc422abf0060478`;
- assessment seal: `e5e7d91eb68145e57197d99b3d14a06e48b243261bc9ff4be5b3fd8050a66881`;
- integrity: `seals_ok=True`, `thesis_ok=True`, `verdicts_rederive=True`.

Pass theme: quantum receipt promotion hardening. This pass adds negative promotion, hardware mock, adapter, resource-estimate, metric-binding, and tool-receipt fixtures around the pass 0013 `QuantumExperimentReceipt/v1` boundary.

No new theorem, quantum hardware result, quantum advantage claim, cryptographic break, natural law, biological result, material result, medical result, finance result, or safety result is promoted in this pass.

## Hardening Fixture

Fixture seal:

```text
5f68b4cb41349c3b0b8fd83a0ba35c6a9aef09283e61b55cb11a407172ecb8c4
```

Validator result:

```text
status = MATCH
match = 1
drift = 0
adapter_count = 2
source_anchor_count = 6
```

## Negative Promotion

The negative fixture attempts:

```text
source_branch = EXACT_SIMULATOR
attempted_target_branch = CLOUD_HARDWARE
attempted_claim = hardware_result
expected_validator_status = REJECT
```

Required rejection reasons:

- `branch_mismatch`;
- `hardware_claim_allowed_false`;
- `missing_cloud_task_metadata`;
- `missing_calibration_reference`;
- `missing_result_payload_hash`.

## Hardware Mock

The mock receipt is cloud-task-shaped but explicitly non-hardware:

```text
branch = HARDWARE_MOCK
hardware_claim_allowed = false
verdict = MOCK_MATCH_NOT_HARDWARE
result.status = MOCK_TASK_SHAPE_ONLY
```

It includes provider, device ARN, task id, shots, queue timestamp, calibration reference, and result payload hash so UI and adapters can be built against realistic fields without creating a false hardware claim.

## Adapter Fixtures

| Adapter | Source Format | Normalized Result |
| --- | --- | --- |
| `qiskit-openqasm3-export-fixture` | OpenQASM 3 | 2 qubits, 2 gates, 1 two-qubit gate, depth 2 |
| `cirq-json-shape-fixture` | Cirq JSON shape | 2 qubits, 2 gates, 1 two-qubit gate, depth 2 |

These are shape fixtures, not full SDK compatibility claims.

## Resource Estimate

The resource-estimate receipt is explicitly non-execution:

```text
schema = QuantumResourceEstimateReceipt/v1
status = ESTIMATE_ONLY_NOT_EXECUTION
execution_claim_allowed = false
```

## Metric Binding

| Claim | Sufficient Evidence | Insufficient Evidence |
| --- | --- | --- |
| `basis_histogram_claim` | `measurement_histogram` | no phase-sensitive evidence |
| `phase_sensitive_clone_claim` | `statevector_or_density_matrix`, `fidelity_to_desired_clone` | `measurement_histogram_only` |
| `cloud_hardware_result_claim` | provider/device identity, task id, shots, calibration reference, payload hash | simulator histogram, hardware mock task shape |

## Tool Substrate Receipt

Pass 0014 refreshed the tool surfaces:

| Tool | Status | Note |
| --- | --- | --- |
| Index | `MATCH` | Version 2.8.0; structure-context role and router map observed. |
| Gather | `MATCH` | Version 1.5.0; perception-intake role observed. |
| Telos | `MATCH` | Catalog reports 65 tools and operator doctor reports 14/14 checks passing. |
| Forum | `MATCH_WITH_SUBMIT_GAP` | Status works; submit remains `UNVERIFIABLE` due to executor JSON parsing. |
| Crucible | `MATCH` | Version 1.1.0; verification-pressure role observed. |

## Source Anchors

| Source | Evidence Used |
| --- | --- |
| IBM Qiskit qasm3 API | OpenQASM 3 export/import boundary. |
| IBM Qiskit OpenQASM 3 interop guide | Qiskit/OpenQASM interoperability caveats. |
| Cirq import/export interop guide | JSON circuit transfer and storage fixture. |
| Amazon Braket task monitoring | Cloud task/result receipt boundaries. |
| Amazon Braket task submission | Device, shots, polling, and result workflow fields. |
| Azure Quantum Resource Estimator | Resource-estimate-only receipt distinction. |

## Forum Steelman Receipt

Forum submit remains blocked by executor JSON parsing:

```text
the configured executor did not return valid JSON
```

This pass records Forum submit status as `UNVERIFIABLE` and includes a local adversarial steelman in `adversarial/pass-0014-promotion-control-steelman.md`.

## Artifacts

| Artifact | Role |
| --- | --- |
| `tools/probe_quantum_receipt_hardening.py` | Deterministic hardening fixture generator. |
| `tools/validate_pass_0014_quantum_hardening.py` | Validator for hardening, adapter, metric-binding, and non-promotion fixtures. |
| `packets/024-quantum-receipt-hardening.md` | Human-readable hardening packet. |
| `adversarial/pass-0014-promotion-control-steelman.md` | Forum failure receipt plus local promotion-control steelman. |
| `schemas/quantum-receipt-hardening-fixtures-pass-0014.json` | Negative promotion, hardware mock, adapter, resource-estimate, and metric-binding fixture. |
| `schemas/pass-0014-quantum-hardening-validator-result.json` | Validator receipt for pass 0014. |
| `schemas/tool-receipts-pass-0014.json` | Compact Index, Gather, Telos, Forum, and Crucible receipts. |
| `crucible/pass-0014-thesis.json` | Falsifiable claims for the fourteenth pass. |
| `crucible/pass-0014-measurements.json` | Measurements/evidence for the fourteenth pass. |
| `crucible/pass-0014-report.md` | Crucible assessment report. |
| `crucible/pass-0014-run.json` | Crucible run record. |

## Primary Next Push

Provider-specific cloud quantum receipt profiles.

Add profiles for:

- Amazon Braket task receipt;
- IBM Qiskit Runtime job receipt;
- Azure Quantum job/resource-estimate receipt;
- simulator result receipt with provider simulator identity;
- SDK adapter version pinning and round-trip checks.

## Natural-Law Promotion

Current promoted natural laws: none.

## Next-Pass Queue

1. Define `CloudQuantumTaskReceiptProfile/v1`.
2. Add a Braket-shaped profile requiring device ARN, task id, S3/result reference, shots, status, timestamps, and payload hash.
3. Add an IBM Runtime-shaped profile requiring backend name, job id, primitive/session metadata where applicable, result reference, shots, status, timestamps, and payload hash.
4. Add an Azure-shaped profile separating resource-estimator output from execution job output.
5. Add validator-negative fixtures for missing calibration reference, missing payload hash, and mock-to-hardware promotion.

