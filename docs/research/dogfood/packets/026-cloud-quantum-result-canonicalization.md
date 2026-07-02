# Pass 0016 - Cloud Quantum Result Canonicalization

Status: CANONICALIZATION_MATCH
Date: 2026-07-01

## Purpose

This pass closes an evidence gap in the cloud quantum proof packet plan: a provider
result payload can be byte-different while semantically equal. A proof packet that
uses only one hash can either lose forensic provenance or fail to recognize a
stable normalized result.

Pass 0016 defines a conservative receipt profile that keeps both:

- `raw_payload_hash`: the exact provider bytes received.
- `normalized_result_hash`: a canonical result object hash used for cross-provider
  comparison.
- `canonicalization_policy_hash`: the policy that explains how raw provider output
  became normalized result output.

No hardware job was run in this pass. No quantum result, theorem, or natural law is
promoted.

## Source Anchors

- RFC 8785 JSON Canonicalization Scheme: https://www.rfc-editor.org/info/rfc8785/
- Amazon Braket device properties: https://docs.aws.amazon.com/braket/latest/developerguide/braket-devices.html
- Amazon Braket result types: https://docs.aws.amazon.com/braket/latest/developerguide/braket-result-types.html
- IBM Quantum QPU information: https://quantum.cloud.ibm.com/docs/en/guides/qpu-information
- IBM BackendProperties API: https://quantum.cloud.ibm.com/docs/en/api/qiskit-ibm-runtime/models-backend-properties
- Azure Quantum Resource Estimator: https://learn.microsoft.com/en-us/azure/quantum/intro-to-resource-estimation
- Azure Quantum resource-estimator results: https://learn.microsoft.com/en-us/azure/quantum/qre-estimation-results

## Canonicalization Fixture

The fixture compares two JSON result payloads:

- Payload A: `{"status":"COMPLETED","shots":1000,"counts":{"00":500,"11":500}}`
- Payload B: `{ "counts": { "11": 500, "00": 500 }, "shots": 1000, "status": "COMPLETED" }`

The byte-level raw hashes differ:

- A: `0e1dcbc4d17e5aefa10085b2e94ffea9d50f54bbda8ab9ecdb5ea10a5d7289e2`
- B: `5a74fc56521b8ad30033a3b828a7fefeeb3c01687a2c74c5c39d1ccf7fdc653f`

The parsed payloads are equal, and the normalized result hashes match:

- A: `601220fead53491134647a9c82790700cb98267b764237a93b94320d85dd3747`
- B: `601220fead53491134647a9c82790700cb98267b764237a93b94320d85dd3747`

This proves only a receipt mechanics property: normalized semantic equivalence can
be stable while raw evidence remains separately preserved.

## Lossiness Labels

The canonicalization policy labels each step:

- `preserve_raw_provider_payload`: `LOSSLESS`
- `parse_json_payload`: `LOSSLESS_IF_PROVIDER_JSON_VALID_AND_DUPLICATE_KEYS_ABSENT`
- `sort_object_keys_and_strip_insignificant_whitespace`:
  `LOSSLESS_FOR_JSON_SEMANTICS_BUT_BYTE_LAYOUT_LOSSY`
- `normalize_provider_counts_to_common_counts_map`:
  `PROVIDER_METADATA_LOSSY_UNLESS_RAW_PAYLOAD_RETAINED`

The important design constraint is that normalization is allowed only when the raw
payload remains attached. A normalized proof object without raw evidence is not a
forensic receipt.

## Calibration Reference Profiles

The schema adds three provider-specific calibration reference profiles:

- `calibration-ref-braket-device-properties`
- `calibration-ref-ibm-backend-properties`
- `calibration-ref-azure-target-properties`

Each profile requires a retrieval timestamp, source reference, payload hash, and an
unavailable-data policy. Calibration-dependent claims become `UNVERIFIABLE` when
the provider metadata needed for the claim cannot be fetched or cited.

## Backend Kind Mapping

The pass adds a first backend-kind guardrail:

- Amazon Braket: reject hardware claims when simulator indicators match or QPU
  indicators are absent.
- IBM Quantum Runtime: reject hardware claims when backend simulator status is true
  or unavailable.
- Azure Quantum: reject hardware claims when the target profile is simulator or
  target kind cannot be verified.

This is an admission-control rule, not a performance claim.

## Azure Resource Estimator Profile

The pass defines `CloudQuantumResourceEstimateReceiptProfile/v1` for Azure-style
resource-estimator output. The profile explicitly sets:

- `execution_claim_allowed`: false
- `hardware_claim_allowed`: false

Resource estimates are planning artifacts. They can support feasibility reasoning,
but they cannot satisfy executed cloud hardware task receipt requirements.

## Negative Fixtures

The validator must reject:

- A normalized result claim with only `raw_payload_hash`.
- A forensic provenance claim with only `normalized_result_hash`.
- Semantically equal payloads with different raw hashes and no policy hash.
- A simulator backend cited as a QPU.
- A resource estimate cited as executed hardware evidence.

## Market And Architecture Implication

This pass adds a proof-layer primitive useful across the Telos/Build ecosystem.
Research labs, AI infrastructure buyers, and scientific-compute users all have the
same hidden failure mode: execution evidence gets flattened into a convenient
summary. The megatool should preserve exact source bytes, normalized analytical
objects, transformation policy, backend identity, and verdict state as distinct
receipts.

For BuildLang/buildc, this becomes a runtime-receipt design requirement: compiler
outputs, measurement outputs, color-calibration outputs, quantum results, finance
backtests, and security scans should all carry both raw and canonicalized forms.

## Artifacts

- `schemas/cloud-quantum-canonicalization-pass-0016.json`
- `tools/probe_cloud_quantum_canonicalization.py`
- `tools/validate_pass_0016_cloud_quantum_canonicalization.py`

## Non-Promotion Statement

Pass 0016 defines canonicalization and calibration receipt profiles only. It does
not run a cloud job, report a quantum hardware result, prove a theorem, or promote
a new law.
