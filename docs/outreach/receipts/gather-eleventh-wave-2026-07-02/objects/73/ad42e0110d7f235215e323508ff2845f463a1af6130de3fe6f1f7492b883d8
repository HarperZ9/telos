# Dogfood Pass 0016 Ledger

Date: 2026-07-01

Status: `CRUCIBLE_MATCH`.

Crucible assessment:

- thesis id: `48f09d160e6adb24`;
- claims: `10`;
- match: `10`;
- drift: `0`;
- unverifiable: `0`;
- thesis seal: `48f09d160e6adb246516f25a4f8781df5799dae226b9ccb4e4051ab22ccff2fe`;
- verdict seal: `f117f9df6709a2e63636dad7de44fa3cba0a5a69894b16898f3f1eb139fff924`;
- measurement seal: `2d62b397256cc89b895a48fd8cf8f8804d582da948d14937a46be9317b9b2228`;
- assessment seal: `7f42a5ce4acad8ee4d72913b6d53967e0e280d17ad21d83520e2c6b829d25fab`;
- integrity: `seals_ok=True`, `thesis_ok=True`, `verdicts_rederive=True`.

Pass theme: cloud quantum result canonicalization. This pass separates raw
provider payload evidence from normalized semantic result evidence, then adds
lossiness labels, calibration-reference profiles, backend-kind rejection rules,
and a non-promotional resource-estimator receipt profile.

No new theorem, quantum hardware result, quantum advantage claim, cryptographic
break, natural law, biological result, material result, medical result, finance
result, or safety result is promoted in this pass.

## Canonicalization Set

Canonicalization-set seal:

```text
11b2ee3baa95764f32395bb4a22e975a0f63b751c127f7f6b2351c79efb75915
```

Validator result:

```text
status = MATCH
match = 1
drift = 0
calibration_profile_count = 3
backend_mapping_count = 3
negative_fixture_count = 5
source_anchor_count = 7
```

## Raw Versus Normalized Hash Fixture

Two semantically equal provider-style JSON payloads intentionally use different
key order and whitespace.

| Field | Value |
| --- | --- |
| `parsed_payloads_equal` | `true` |
| `raw_payload_a_hash` | `0e1dcbc4d17e5aefa10085b2e94ffea9d50f54bbda8ab9ecdb5ea10a5d7289e2` |
| `raw_payload_b_hash` | `5a74fc56521b8ad30033a3b828a7fefeeb3c01687a2c74c5c39d1ccf7fdc653f` |
| `normalized_result_hash_a` | `601220fead53491134647a9c82790700cb98267b764237a93b94320d85dd3747` |
| `normalized_result_hash_b` | `601220fead53491134647a9c82790700cb98267b764237a93b94320d85dd3747` |

Result: `RAW_HASH_DRIFT_NORMALIZED_HASH_MATCH`.

## Canonicalization Policy

Required hashes:

- `raw_payload_hash`;
- `normalized_result_hash`;
- `canonicalization_policy_hash`.

Lossiness labels:

- `LOSSLESS`;
- `LOSSLESS_IF_PROVIDER_JSON_VALID_AND_DUPLICATE_KEYS_ABSENT`;
- `LOSSLESS_FOR_JSON_SEMANTICS_BUT_BYTE_LAYOUT_LOSSY`;
- `PROVIDER_METADATA_LOSSY_UNLESS_RAW_PAYLOAD_RETAINED`.

## Calibration Reference Profiles

| Profile | Provider | Role |
| --- | --- | --- |
| `calibration-ref-braket-device-properties` | Amazon Braket | Device properties, native gate set, and calibration/unavailable reference. |
| `calibration-ref-ibm-backend-properties` | IBM Quantum Runtime | Backend properties, qubit properties, gate properties, and last update date. |
| `calibration-ref-azure-target-properties` | Azure Quantum | Workspace, provider, target, target properties, and capability profile reference. |

Calibration-dependent claims become `UNVERIFIABLE` when required provider
metadata cannot be retrieved or cited.

## Backend-Kind Gate

Hardware claims are rejected when:

- simulator indicators match;
- QPU indicators are absent;
- provider target kind is unavailable or unverified.

The mapping currently covers Amazon Braket, IBM Quantum Runtime, and Azure
Quantum. It is a policy scaffold; provider-specific parsers remain future work.

## Resource Estimator Profile

The pass defines `CloudQuantumResourceEstimateReceiptProfile/v1`.

Required estimator fields include:

- application, architecture, and error-correction model hashes;
- estimator version or tool reference;
- estimate payload hash;
- normalized estimate hash;
- physical qubits;
- runtime;
- error budget;
- Pareto-point count or selection rule.

The profile sets:

```text
execution_claim_allowed = false
hardware_claim_allowed = false
```

## Negative Fixtures

| Fixture | Expected Result |
| --- | --- |
| `negative-raw-only-hash-for-normalized-claim` | `REJECT` |
| `negative-normalized-only-hash-for-forensic-claim` | `REJECT` |
| `negative-nondeterministic-payload-order-without-canonicalization` | `REJECT` |
| `negative-simulator-backend-cited-as-qpu` | `REJECT` |
| `negative-resource-estimator-cited-as-execution` | `REJECT` |

## Tool Substrate Receipt

Pass 0016 refreshed the tool surfaces:

| Tool | Status | Note |
| --- | --- | --- |
| Index | `MATCH` | Version 2.8.0; structure-context role observed. |
| Gather | `MATCH` | Version 1.5.0; perception-intake role observed. |
| Telos | `MATCH` | Operator doctor reports 14/14 checks passing and 65 tools. |
| Forum | `MATCH_WITH_SUBMIT_GAP` | Ledger status/verify works; submit remains `UNVERIFIABLE` due to executor JSON parsing. |
| Crucible | `MATCH` | Version 1.1.0; verification-pressure role observed. |

Forum ledger status:

```text
entries=7
checkpoint=bac6330587361860a30fb9e069d880f69a1a27b11d0aa0e3802220e95581c8f9
chain=true
deep=true
```

## Source Anchors

| Source | Evidence Used |
| --- | --- |
| RFC 8785 JSON Canonicalization Scheme | Canonical JSON should be deterministic for repeatable hashing/signing. |
| Amazon Braket device properties | Device properties, topology, calibration, and native gate-set references. |
| Amazon Braket result types | Result-type distinction and simulator-only result type warning. |
| IBM Quantum QPU information | Backend properties change on calibration and may be retrieved historically. |
| IBM BackendProperties API | Backend properties include qubits, gates, general data, and last update date. |
| Azure Quantum Resource Estimator | Resource estimation is a planning/workload-estimation surface. |
| Azure Quantum resource-estimator results | Estimator outputs include physical qubits, runtime, error, and related fields. |

## Artifacts

| Artifact | Role |
| --- | --- |
| `tools/probe_cloud_quantum_canonicalization.py` | Deterministic canonicalization profile generator. |
| `tools/validate_pass_0016_cloud_quantum_canonicalization.py` | Validator for pass 0016 canonicalization, calibration profiles, backend mapping, and negative fixtures. |
| `packets/026-cloud-quantum-result-canonicalization.md` | Human-readable cloud quantum result canonicalization packet. |
| `adversarial/pass-0016-canonicalization-steelman.md` | Forum failure receipt plus local canonicalization steelman. |
| `schemas/cloud-quantum-canonicalization-pass-0016.json` | `CloudQuantumCanonicalizationSet/v1` fixture and profiles. |
| `schemas/pass-0016-cloud-quantum-canonicalization-validator-result.json` | Validator receipt for pass 0016. |
| `schemas/tool-receipts-pass-0016.json` | Compact Index, Gather, Telos, Forum, and Crucible receipts. |
| `crucible/pass-0016-thesis.json` | Falsifiable claims for the sixteenth pass. |
| `crucible/pass-0016-measurements.json` | Measurements/evidence for the sixteenth pass. |
| `crucible/pass-0016-report.md` | Crucible assessment report. |
| `crucible/pass-0016-run.json` | Crucible run record. |

## Primary Next Push

Provider metadata parser fixtures and register-layout hardening.

Implement:

- Braket `GetDevice` sample parser profile;
- IBM backend-properties sample parser profile;
- Azure target-properties sample parser profile;
- duplicate-key JSON negative fixture;
- binary/object-storage payload receipt fixture;
- floating-point precision fixture;
- register layout and endian-convention receipt;
- post-processing and mitigation receipt.

## Natural-Law Promotion

Current promoted natural laws: none.

## Next-Pass Queue

1. Add parser-level fixtures for Braket device properties, IBM backend properties,
   and Azure target metadata.
2. Add duplicate-key, binary-payload, object-storage reference, and floating-point
   canonicalization negative fixtures.
3. Add `QuantumRegisterLayoutReceipt/v1` for endian convention, classical register
   mapping, shot ordering, and bitstring normalization.
4. Add `QuantumPostProcessingReceipt/v1` for readout mitigation, truncation,
   filtering, and provider/client-side transformations.
5. Compare this proof-layer primitive against Qiskit, Cirq, PennyLane, provider
   dashboards, and resource-estimation workflows as a focused market pass.
