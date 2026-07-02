# Dogfood Pass 0013 Ledger

Date: 2026-07-01

Status: `CRUCIBLE_MATCH`.

Crucible assessment:

- thesis id: `f913da2728a49106`;
- claims: `8`;
- match: `8`;
- drift: `0`;
- unverifiable: `0`;
- thesis seal: `f913da2728a4910617a6b67c061741351194dcbf79e42b4c157bfdd3b7787124`;
- verdict seal: `f07ee9dc8050bfaced9c8dbed508eb120adf6fab5a12590cb04364a4b1e2e0e1`;
- measurement seal: `3ec4abbd0be2866d0bdaf95ba2c5174844c0bc5b4bc6d5ece298132c8fa23b64`;
- assessment seal: `3fc5059ece29da40f18768f7ee5893830c17d137dbedf4f184650a0505dd331f`;
- integrity: `seals_ok=True`, `thesis_ok=True`, `verdicts_rederive=True`.

Pass theme: quantum experiment receipts and branch-separation hardening. This pass implements `QuantumExperimentReceipt/v1` as a compact receipt shape for exact simulator, noisy simulator, hardware mock, and cloud-hardware evidence boundaries.

No new theorem, quantum hardware result, quantum advantage claim, cryptographic break, natural law, biological result, material result, medical result, finance result, or safety result is promoted in this pass.

## Receipt Finding

The schema requires:

- receipt id;
- schema id;
- backend branch;
- hardware-claim boolean;
- theorem claim reference;
- circuit record;
- backend record;
- resource estimate;
- result record;
- verifier verdict.

The branch values are:

| Branch | Meaning |
| --- | --- |
| `EXACT_SIMULATOR` | Exact analytic or statevector-style simulator evidence. |
| `NOISY_SIMULATOR` | Simulator evidence with explicit noise assumptions. |
| `HARDWARE_MOCK` | Mocked hardware-style task evidence. |
| `CLOUD_HARDWARE` | Real provider/device/task evidence, valid only with hardware metadata. |

`branch_promotion_forbidden=true` is part of the schema.

## Negative Fixture

The pass uses the no-cloning `|+>|0>` CNOT witness from pass 0012.

The exact simulator branch reports:

```text
fidelity_to_desired_clone = 0.5
histogram = {00: 0.5, 01: 0.0, 10: 0.0, 11: 0.5}
hardware_claim_allowed = false
```

The noisy simulator branch applies a target phase-flip component with probability `0.1`. It reports:

```text
fidelity_to_desired_clone = 0.45
histogram_l1_drift_from_exact = 0.0
histogram = {00: 0.5, 01: 0.0, 10: 0.0, 11: 0.5}
hardware_claim_allowed = false
```

This is the pass's central evidence lesson: identical computational-basis histograms can hide phase-sensitive fidelity drift. Histogram equality alone is not sufficient for state-sensitive quantum claims.

Receipt-set seal:

```text
e5bcaf8a0cbe73fd51d6745539a8fca2ea1faff3ff9f375fe94a646761ce3ea9
```

## Source Anchors

| Source | Evidence Used |
| --- | --- |
| Qiskit Aer noise models | Noise model and noisy-simulator branch semantics. |
| IBM Quantum noise-model guide | Backend-derived and explicit noise-model receipt fields. |
| Cirq noisy simulation | Noisy simulation and channel-level branch semantics. |
| Azure Quantum Resource Estimator | Resource-estimation receipt fields and assumptions. |
| Amazon Braket task monitoring | Cloud task, status, and result receipt boundaries. |
| IonQ simulation with noise models | Cloud-style simulator noise-model evidence boundaries. |

## Forum Steelman Receipt

Forum status and chain verification were reachable:

```text
entries=3
checkpoint=a146467e8ef2c07fac3932cf8ce3900a532b8829795d6bf377f012f476b62668
chain=true
deep=true
```

Both Forum submit paths returned the executor JSON parsing error:

```text
the configured executor did not return valid JSON
```

This pass records Forum submit status as `UNVERIFIABLE` and includes a local adversarial steelman in `adversarial/pass-0013-branch-separation-steelman.md`.

## Validator Result

The pass 0013 validator reports:

```text
status = MATCH
match = 2
drift = 0
```

Checks:

- `QuantumExperimentReceiptSchema`: `MATCH`;
- `QuantumExperimentReceiptSet`: `MATCH`.

## Artifacts

| Artifact | Role |
| --- | --- |
| `tools/probe_quantum_experiment_receipt.py` | Deterministic exact/noisy quantum experiment receipt generator. |
| `tools/validate_pass_0013_quantum_experiment.py` | Validator for schema and branch-separation receipt fixtures. |
| `packets/023-quantum-experiment-receipts.md` | Human-readable receipt architecture and market implication packet. |
| `adversarial/pass-0013-branch-separation-steelman.md` | Forum failure receipt plus local adversarial steelman. |
| `schemas/quantum-experiment-receipt-schema-pass-0013.json` | `QuantumExperimentReceiptSchema/v1` contract. |
| `schemas/quantum-experiment-receipts-pass-0013.json` | Exact and noisy simulator `QuantumExperimentReceipt/v1` fixtures. |
| `schemas/pass-0013-quantum-experiment-validator-result.json` | Validator receipt for pass 0013. |
| `crucible/pass-0013-thesis.json` | Falsifiable claims for the thirteenth pass. |
| `crucible/pass-0013-measurements.json` | Measurements/evidence for the thirteenth pass. |
| `crucible/pass-0013-report.md` | Crucible assessment report. |
| `crucible/pass-0013-run.json` | Crucible run record. |

## Primary Next Push

`QuantumExperimentReceipt/v1` cloud-hardware and adapter hardening.

Implement negative and positive fixtures for:

- invalid simulator-to-hardware promotion;
- `HARDWARE_MOCK` with cloud-shaped task metadata but no hardware claim;
- Qiskit or Cirq adapter output;
- resource-estimation receipt joined to circuit metadata but not promoted to execution;
- metric-specific claim binding for histogram, statevector, density matrix, observable expectation, and fidelity.

## Natural-Law Promotion

Current promoted natural laws: none.

## Next-Pass Queue

1. Add a validator-negative fixture that tries to promote `EXACT_SIMULATOR` to `CLOUD_HARDWARE` and must fail.
2. Add a mock cloud task receipt with task id, provider, device, shots, calibration reference, queue timestamp, and payload hash, while keeping branch `HARDWARE_MOCK`.
3. Add a Qiskit or Cirq adapter fixture for the no-cloning circuit.
4. Add a resource-estimation receipt with explicit assumptions and a non-execution status.
5. Repair Forum executor JSON output so adversarial review can become a witnessed Forum receipt.

