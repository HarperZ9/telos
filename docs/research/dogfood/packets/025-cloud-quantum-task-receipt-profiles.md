# Cloud Quantum Task Receipt Profiles

Date: 2026-07-01

Status: `PROBE_MATCH`.

Pass 0015 moves from generic quantum receipt hardening into provider-specific cloud quantum task receipt profiles. The pass defines receipt profiles for Amazon Braket, IBM Quantum Runtime, Azure Quantum, and provider simulators. It also adds negative fixtures for missing payload hashes, missing calibration/backend references, resource-estimator overpromotion, and hardware-mock overpromotion.

This pass does not run a cloud job. All sample receipts are shape-only and explicitly set:

```text
hardware_claim_allowed = false
sample_status = SHAPE_ONLY_NOT_EXECUTED
```

## Design Rule

A cloud quantum receipt must bind four surfaces:

| Surface | Question |
| --- | --- |
| Identity | Which provider, account/workspace/instance, device/target/backend, and task/job id? |
| Execution | What branch, shots or precision, status, timestamps, and mode? |
| Result | Where is the result, what format is it, and what payload hash proves integrity? |
| Provenance | Which source program, SDK/CLI version, adapter, and calibration/device/backend/target reference? |

Without all four, the receipt may still be useful as a planning or UI artifact, but it cannot support a hardware claim.

## Profiles

| Profile | Branch | Hardware Claim Requirement |
| --- | --- | --- |
| `cloud-quantum-profile-braket-task` | `CLOUD_HARDWARE` | device ARN, task id, device kind, shots, status, timestamp/date, result reference, payload hash, calibration/device reference, source hash |
| `cloud-quantum-profile-ibm-runtime-job` | `CLOUD_HARDWARE` | backend, job id, primitive, PUB/circuit reference, shots/precision, status, result reference, payload hash, source hash, job/session mode, calibration/backend reference |
| `cloud-quantum-profile-azure-job` | `CLOUD_HARDWARE` | workspace, provider, target, job id, input hash, input/output formats, shots/params, status, output/storage ref, payload hash, calibration/target reference |
| `cloud-quantum-profile-provider-simulator` | `CLOUD_SIMULATOR` | no hardware claim allowed |

## Negative Fixtures

| Fixture | Expected Result |
| --- | --- |
| `negative-braket-missing-result-payload-hash` | `REJECT` |
| `negative-ibm-missing-calibration-reference` | `REJECT` |
| `negative-azure-resource-estimator-promoted-to-execution` | `REJECT` |
| `negative-hardware-mock-promoted-to-cloud-hardware` | `REJECT` |

These are deliberately narrow. The point is to make later adapters fail loudly when they attempt to convert an incomplete provider object into a hardware proof packet.

## Provider Notes

### Amazon Braket

The Braket profile is anchored around task identity, task state, result retrieval, metadata, and S3 result storage. The profile requires device ARN, task id, status, shots, result reference, result payload hash, and calibration or device-properties reference.

Simulator task receipts must identify simulator branch and cannot be cited as QPU hardware.

### IBM Quantum Runtime

The IBM Runtime profile is anchored around Runtime job id, primitive execution, result retrieval, backend identity, and optional session/job mode. The profile requires backend name, job id, primitive name, PUB or circuit reference, shots or precision, status, result reference, result payload hash, source program hash, mode, and calibration/backend-properties reference.

A session receipt cannot substitute for a job result receipt.

### Azure Quantum

The Azure profile is anchored around workspace, provider, target, job id, input/output formats, job status, and output storage. The profile explicitly separates resource-estimator output from execution output.

Resource-estimator receipts remain planning artifacts unless joined to a real execution receipt.

## Market Implication

This pass gives Telos a sharper quantum wedge:

- incumbent SDKs and clouds expose job/task primitives;
- labs need to prove which backend produced which result;
- models can easily overclaim cloud, simulator, and resource-estimate evidence;
- Telos can win by making branch, provider, result hash, and non-promotion policy impossible to omit.

The same pattern generalizes directly to:

- autonomous lab runs;
- GPU/HPC simulations;
- BuildLang/buildc scientific runtime receipts;
- color calibration instrumentation;
- financial backtests;
- robotics experiments;
- bioinformatics pipelines.

## Source Anchors

| Source | Evidence Used |
| --- | --- |
| Amazon Braket task monitoring | Task id, status, metadata, shots, and result retrieval boundaries. |
| Amazon Braket overview | Device selection, QPU/simulator distinction, S3 result storage, and task lifecycle. |
| Amazon Braket task submission | Device, shots, polling, and result workflow fields. |
| IBM Runtime Jobs REST API | Job id, status, and result review requirement. |
| IBM retrieve/save jobs guide | Job id retrieval and result retrieval pattern. |
| IBM primitive input/output guide | Primitive workloads execute as jobs and return PUB-dependent results. |
| IBM session guide | Session/job mode distinction and session lifecycle. |
| Azure submit jobs guide | Workspace, target, shots, job status, result download, and `submit` workflow. |
| Azure CLI quantum job docs | Job id, input/output format, target id, shots, and output command fields. |
| Azure job lifecycle docs | Job id, provider, target, status, output storage, and lifecycle states. |
| Azure Resource Estimator | Planning artifact, not execution-result artifact. |

## Natural-Law Promotion

Current promoted natural laws: none.

