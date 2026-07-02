# Quantum Receipt Hardening

Date: 2026-07-01

Status: `PROBE_MATCH`.

Pass 0014 extends `QuantumExperimentReceipt/v1` from a simulator/noisy-simulator boundary into a stricter adapter and promotion-control shape. It does not claim a quantum hardware result. It creates fixtures that future validators must use to reject bad promotions before any public demo or research packet can imply more than the evidence supports.

## Product Rule

Quantum evidence must be typed by branch and metric.

Branch answers the question:

```text
What produced this evidence?
```

Metric binding answers the question:

```text
Which measurements are sufficient for this claim?
```

The hard case is when a plausible-looking artifact has enough shape to pass casual review but not enough evidence to support the stronger claim. Pass 0014 creates that shape directly.

## Negative Promotion Fixture

The fixture attempts to promote the pass 0013 exact simulator receipt into a cloud-hardware claim:

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

This is the minimum guardrail. A simulator receipt cannot become a hardware receipt by being copied into a more impressive context.

## Hardware Mock Receipt

The pass also creates a cloud-task-shaped mock receipt:

```text
branch = HARDWARE_MOCK
hardware_claim_allowed = false
verdict = MOCK_MATCH_NOT_HARDWARE
```

It includes task-shaped metadata:

- provider;
- device ARN;
- task id;
- shot count;
- queue timestamp;
- calibration reference;
- result payload hash.

That structure is useful for UI, adapter, and validator development, but it is explicitly not a hardware result.

## Adapter Fixtures

The pass includes two adapter fixtures:

| Adapter | Source Format | Purpose |
| --- | --- | --- |
| `qiskit-openqasm3-export-fixture` | OpenQASM 3 | Normalize a simple two-qubit circuit from an OpenQASM-shaped artifact. |
| `cirq-json-shape-fixture` | Cirq JSON shape | Normalize a simple two-moment circuit from a Cirq-shaped artifact. |

Both normalize to:

```text
qubits = 2
gate_count = 2
two_qubit_gate_count = 1
depth = 2
```

The goal is not complete Qiskit or Cirq compatibility yet. The goal is to make the adapter boundary explicit, source-backed, and validator-addressable.

## Resource Estimate Receipt

The resource-estimate fixture is intentionally not executable:

```text
schema = QuantumResourceEstimateReceipt/v1
status = ESTIMATE_ONLY_NOT_EXECUTION
execution_claim_allowed = false
```

This preserves the distinction between:

- planning evidence;
- simulator evidence;
- mock hardware evidence;
- real task evidence.

## Metric Claim Binding

Pass 0014 binds claim families to sufficient and insufficient evidence:

| Claim | Sufficient | Insufficient |
| --- | --- | --- |
| Basis histogram claim | `measurement_histogram` | no phase-sensitive state evidence |
| Phase-sensitive clone claim | `statevector_or_density_matrix`, `fidelity_to_desired_clone` | `measurement_histogram_only` |
| Cloud hardware result claim | provider/device identity, task id, shots, calibration reference, result payload hash | simulator histogram, hardware mock task shape |

This is the architectural bridge from quantum receipts to broader scientific receipts. Biology, materials, finance, graphics, and robotics will need the same distinction: a claim must name the metrics that can actually support it.

## Index/Gather/Telos Context

Pass 0014 refreshed the tool substrate:

| Tool | Observed Role |
| --- | --- |
| Gather | Perception-intake for source, media, and research material with provenance. |
| Index | Structure-context layer for workspace maps, context envelopes, and source-ref expansion handles. |
| Forum | Routing and adversarial/humanization layer, with submit still blocked by executor JSON parsing. |
| Crucible | Verification-pressure layer for claim verdicts, rechecks, and measurement gates. |
| Telos | Operator catalog tying tools into action receipts, context packs, workflow, model foundry, learning labs, display calibration, browser evidence, and native control. |

Index's router output for the local `telos` checkout is intentionally compact: it sees a single leaf and the top-level docs. That is enough for this pass because the target is the dogfood research corpus, not a whole-repo refactor.

## Source Anchors

| Source | Relevance |
| --- | --- |
| IBM Qiskit qasm3 API | Supports OpenQASM 3 export/import boundary. |
| IBM Qiskit OpenQASM 3 interop guide | Supports Qiskit/OpenQASM interoperability caveats. |
| Cirq import/export interop guide | Supports JSON circuit transfer and storage fixture. |
| Amazon Braket task monitoring | Supports cloud task/result receipt boundaries. |
| Amazon Braket task submission | Supports device, shots, polling, and result workflow fields. |
| Azure Quantum Resource Estimator | Supports resource-estimate-only receipt distinction. |

## Natural-Law Promotion

Current promoted natural laws: none.

