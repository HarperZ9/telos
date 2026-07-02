# Pass 0017 - Cloud Quantum Metadata Parser Hardening

Status: PARSER_PROFILE_MATCH
Date: 2026-07-01

## Purpose

Pass 0016 separated raw provider payload hashes from normalized result hashes.
Pass 0017 hardens the layer before and after that normalization:

- before: provider metadata parser receipts for target identity and hardware
  eligibility;
- after: register-layout and post-processing receipts for bitstring
  interpretation.

This is still a profile pass. It does not fetch live provider metadata, run a
cloud quantum job, or promote a quantum hardware result.

## Source Anchors

- Amazon Braket GetDevice API: https://docs.aws.amazon.com/braket/latest/APIReference/API_GetDevice.html
- Amazon Braket device properties: https://docs.aws.amazon.com/braket/latest/developerguide/braket-devices.html
- IBM BackendProperties API: https://quantum.cloud.ibm.com/docs/api/qiskit-ibm-runtime/models-backend-properties
- IBM Quantum backend information: https://quantum.cloud.ibm.com/docs/guides/get-qpu-information
- Azure Quantum target CLI: https://learn.microsoft.com/en-us/cli/azure/quantum/target?view=azure-cli-latest
- Azure Quantum job CLI: https://learn.microsoft.com/en-us/cli/azure/quantum/job?view=azure-cli-latest
- IBM Quantum bit-ordering guide: https://quantum.cloud.ibm.com/docs/guides/bit-ordering

## Parser Profiles

The pass defines three `CloudQuantumProviderMetadataParserProfile/v1` fixtures:

| Profile | Provider | Input Surface | Claim Gate |
| --- | --- | --- | --- |
| `parser-braket-get-device` | Amazon Braket | `GetDevice` | Requires device ARN, QPU device type, status, capabilities, and payload hash. |
| `parser-ibm-backend-properties` | IBM Quantum Runtime | `BackendProperties` | Requires backend name/version, last update date, qubits, gates, and payload hash. |
| `parser-azure-target-list` | Azure Quantum | `az quantum target list/show` | Requires workspace, provider, target, target profile, and payload hash. |

These are parser fixtures, not live provider retrieval receipts. They prove the
shape of the admission-control logic we need before a proof packet can assert
hardware eligibility.

## Register Layout Receipt

The pass adds `QuantumRegisterLayoutReceipt/v1`.

The sample fixture records Qiskit-style bitstring interpretation:

- bit `n-1` is the leftmost string position;
- bit `0` is the rightmost string position;
- `q[0]` maps to `c[0]` and the rightmost bit;
- `q[1]` maps to `c[1]` and the leftmost bit.

Example:

| Bitstring | Interpretation |
| --- | --- |
| `10` | `q[1]=1`, `q[0]=0` |
| `01` | `q[1]=0`, `q[0]=1` |

Without this receipt, normalized counts can look correct while silently reversing
the scientific meaning of a result.

## Post-Processing Receipt

The pass adds a baseline `QuantumPostProcessingReceipt/v1`.

Baseline fields:

- `raw_result_hash_required=true`
- `normalized_result_hash_required=true`
- `mitigation_applied=false`
- `filtering_applied=false`
- `truncation_applied=false`
- `operations=[]`

Claim rule: if a result packet changes counts, bit order, mitigation, filtering,
or truncation, it must add a post-processing receipt.

## Negative Fixtures

The validator must reject:

- provider metadata without `payload_hash`;
- unknown Azure target kind promoted to hardware;
- counts normalization without register layout;
- bitstring interpretation without endian/string-position convention;
- duplicate JSON keys treated as lossless canonical JSON;
- binary provider payload treated as JSON;
- floating-point normalization without precision policy;
- post-processed counts without a post-processing receipt.

## Market And Architecture Implication

Quantum cloud providers expose useful metadata, but proof packets need a stricter
contract than dashboards. A Telos/Build proof layer should preserve:

- exact provider metadata payload hash;
- parser policy;
- normalized target identity;
- hardware/simulator admission result;
- register layout;
- result post-processing operations;
- raw and normalized result hashes.

The same shape generalizes to BuildLang/buildc runtime receipts, color
calibration, rendering validation, finance backtests, and security scans:
measurement output is not enough unless the system also records how the target,
layout, units, and post-processing were interpreted.

## Artifacts

- `tools/probe_cloud_quantum_metadata_parsers.py`
- `tools/validate_pass_0017_metadata_parsers.py`
- `schemas/cloud-quantum-metadata-parsers-pass-0017.json`

## Non-Promotion Statement

Pass 0017 defines provider metadata parser and register-layout fixtures only. It
does not fetch live provider metadata, run a quantum job, prove a theorem, or
promote a quantum hardware result.
