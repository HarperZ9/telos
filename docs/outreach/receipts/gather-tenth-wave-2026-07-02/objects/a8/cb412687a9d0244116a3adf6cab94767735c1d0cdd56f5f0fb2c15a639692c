# Dogfood Pass 0015 Ledger

Date: 2026-07-01

Status: `CRUCIBLE_MATCH`.

Crucible assessment:

- thesis id: `9523ffdeed3a5a59`;
- claims: `9`;
- match: `9`;
- drift: `0`;
- unverifiable: `0`;
- thesis seal: `9523ffdeed3a5a59e5d3e567b7d94bd6bfd29be53b57023620279dffef7adfb8`;
- verdict seal: `4fc49f7dfc047f75faa3a2c78f92d8f332ebfdfad8c35d92db9fad78d5cdc22a`;
- measurement seal: `3c6bf38af77a52c55f7b4851f2cff3995a086eb9b2d2192a9a0d5b8d07c1fb1d`;
- assessment seal: `c40e10b77824dc6600428b7617269aa4ee76f52f04a1199317e685852fa73cb0`;
- integrity: `seals_ok=True`, `thesis_ok=True`, `verdicts_rederive=True`.

Pass theme: provider-specific cloud quantum task receipt profiles. This pass defines Braket, IBM Runtime, Azure Quantum, and provider-simulator profiles that separate hardware jobs, simulator jobs, resource-estimate artifacts, and shape-only fixtures.

No new theorem, quantum hardware result, quantum advantage claim, cryptographic break, natural law, biological result, material result, medical result, finance result, or safety result is promoted in this pass.

## Profile Set

Profile-set seal:

```text
da29ddb01c060ea4af511cec8c901895e9f1c3c62622d367aefb15e7f82fcf62
```

Validator result:

```text
status = MATCH
match = 1
drift = 0
profile_count = 4
negative_fixture_count = 4
sample_receipt_count = 3
```

## Profiles

| Profile | Branch | Role |
| --- | --- | --- |
| `cloud-quantum-profile-braket-task` | `CLOUD_HARDWARE` | Amazon Braket task receipt profile. |
| `cloud-quantum-profile-ibm-runtime-job` | `CLOUD_HARDWARE` | IBM Quantum Runtime job receipt profile. |
| `cloud-quantum-profile-azure-job` | `CLOUD_HARDWARE` | Azure Quantum job receipt profile. |
| `cloud-quantum-profile-provider-simulator` | `CLOUD_SIMULATOR` | Cloud simulator receipt profile with no hardware claim allowed. |

## Hardware-Claim Gate

Braket hardware-claim eligibility requires:

- device ARN;
- task id;
- device kind declared as QPU or simulator;
- shots;
- status;
- submit timestamp or provider date;
- result reference;
- result payload hash;
- calibration or device-properties reference;
- source program hash.

IBM Runtime hardware-claim eligibility requires:

- backend name;
- job id;
- primitive name;
- PUB or circuit reference;
- shots or precision;
- status;
- result reference;
- result payload hash;
- source program hash;
- session or job mode;
- calibration or backend-properties reference.

Azure Quantum hardware-claim eligibility requires:

- workspace reference;
- provider id;
- target id;
- job id;
- job input hash;
- job input format;
- job output format;
- shots or target parameters;
- status;
- output or storage reference;
- result payload hash;
- calibration or target-properties reference.

## Negative Fixtures

| Fixture | Expected Result |
| --- | --- |
| `negative-braket-missing-result-payload-hash` | `REJECT` |
| `negative-ibm-missing-calibration-reference` | `REJECT` |
| `negative-azure-resource-estimator-promoted-to-execution` | `REJECT` |
| `negative-hardware-mock-promoted-to-cloud-hardware` | `REJECT` |

## Tool Substrate Receipt

Pass 0015 refreshed the tool surfaces:

| Tool | Status | Note |
| --- | --- | --- |
| Index | `MATCH` | Version 2.8.0; structure-context role observed. |
| Gather | `MATCH` | Version 1.5.0; perception-intake role observed. |
| Telos | `MATCH` | Operator doctor reports 14/14 checks passing and 65 tools. |
| Forum | `MATCH_WITH_SUBMIT_GAP` | Ledger status/verify works; submit remains `UNVERIFIABLE` due to executor JSON parsing. |
| Crucible | `MATCH` | Version 1.1.0; verification-pressure role observed. |

Forum ledger status:

```text
entries=6
checkpoint=253900c51d9c6444119aac10be5730f2d00bfc13894c5bec9ebde8e2634b9c6b
chain=true
deep=true
```

## Source Anchors

| Source | Evidence Used |
| --- | --- |
| Amazon Braket task monitoring | Task id, status, metadata, shots, result retrieval. |
| Amazon Braket overview | Device selection, QPU/simulator distinction, S3 result storage, task lifecycle. |
| Amazon Braket task submission | Device, shots, polling, and result workflow fields. |
| IBM Runtime Jobs REST API | Job id, status, and result review requirement. |
| IBM retrieve/save jobs guide | Job id retrieval and result retrieval pattern. |
| IBM primitive input/output guide | Primitive workloads execute as jobs and return PUB-dependent results. |
| IBM session guide | Session/job mode distinction and session lifecycle. |
| Azure submit jobs guide | Workspace, target, shots, job status, result download, and submit workflow. |
| Azure CLI quantum job docs | Job id, input/output format, target id, shots, and output command fields. |
| Azure job lifecycle docs | Job id, provider, target, status, output storage, and lifecycle states. |
| Azure Resource Estimator | Planning artifact, not execution-result artifact. |

## Artifacts

| Artifact | Role |
| --- | --- |
| `tools/probe_cloud_quantum_profiles.py` | Deterministic provider profile generator. |
| `tools/validate_pass_0015_cloud_quantum_profiles.py` | Validator for provider profiles, negative fixtures, and shape-only samples. |
| `packets/025-cloud-quantum-task-receipt-profiles.md` | Human-readable cloud quantum task receipt profile packet. |
| `adversarial/pass-0015-cloud-profile-steelman.md` | Forum failure receipt plus local cloud-profile steelman. |
| `schemas/cloud-quantum-task-receipt-profiles-pass-0015.json` | `CloudQuantumTaskReceiptProfileSet/v1` provider profiles. |
| `schemas/pass-0015-cloud-quantum-profile-validator-result.json` | Validator receipt for pass 0015. |
| `schemas/tool-receipts-pass-0015.json` | Compact Index, Gather, Telos, Forum, and Crucible receipts. |
| `crucible/pass-0015-thesis.json` | Falsifiable claims for the fifteenth pass. |
| `crucible/pass-0015-measurements.json` | Measurements/evidence for the fifteenth pass. |
| `crucible/pass-0015-report.md` | Crucible assessment report. |
| `crucible/pass-0015-run.json` | Crucible run record. |

## Primary Next Push

Provider-specific canonicalization and calibration references.

Implement:

- `CloudQuantumResultCanonicalization/v1`;
- raw payload hash versus normalized result hash;
- provider-specific calibration/device/backend/target property reference schemas;
- simulator/QPU backend-kind mapping;
- separate Azure resource-estimator profile family.

## Natural-Law Promotion

Current promoted natural laws: none.

## Next-Pass Queue

1. Define canonicalization rules for raw provider result payloads and normalized result payloads.
2. Add lossiness labels for each normalization step.
3. Add Braket, IBM Runtime, and Azure calibration/property reference profiles.
4. Add negative fixtures for nondeterministic payload order, missing raw payload hash, missing normalized payload hash, and simulator backend cited as QPU.
5. Add `CloudQuantumResourceEstimateReceiptProfile/v1` for Azure-style resource estimator outputs.

