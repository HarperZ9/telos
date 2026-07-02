# Dogfood Pass 0017 Ledger

Date: 2026-07-01

Status: `CRUCIBLE_MATCH`.

Crucible assessment:

- thesis id: `76cc95d75900dfd1`;
- claims: `11`;
- match: `11`;
- drift: `0`;
- unverifiable: `0`;
- thesis seal: `76cc95d75900dfd1cdcb1791245d943cd2c3a4531fda25b6ed0a6793c517703a`;
- verdict seal: `6d1e369b9946e788958472d85072127cfd9ed0f8eea91649d19fb17bd2fed1b8`;
- measurement seal: `4e15dbece7af885c4cb54396858c9d35f2460c6faaa1586a869071d957d3505f`;
- assessment seal: `16bde39313bb3bff66bcb3c1b30ad9b0309bc6d958e7af5e715dc2e43901e8fb`;
- integrity: `seals_ok=True`, `thesis_ok=True`, `verdicts_rederive=True`.

Pass theme: provider metadata parser and register-layout hardening. This pass
adds parser profiles for Braket `GetDevice`, IBM `BackendProperties`, Azure
Quantum target metadata, and the first `QuantumRegisterLayoutReceipt/v1` plus
`QuantumPostProcessingReceipt/v1` baseline.

No live provider metadata retrieval, new theorem, quantum hardware result,
quantum advantage claim, cryptographic break, natural law, biological result,
material result, medical result, finance result, or safety result is promoted in
this pass.

## Parser Set

Parser-set seal:

```text
e098df09eb2556049e1b9e676b0ace8f0000d1f0bda7565628e2195711e84b21
```

Validator result:

```text
status = MATCH
match = 1
drift = 0
parser_profile_count = 3
negative_fixture_count = 8
source_anchor_count = 7
```

## Parser Profiles

| Profile | Provider | Input Surface | Hardware Gate |
| --- | --- | --- | --- |
| `parser-braket-get-device` | Amazon Braket | `GetDevice` | Requires device ARN, QPU device type, status, capabilities, and payload hash. |
| `parser-ibm-backend-properties` | IBM Quantum Runtime | `BackendProperties` | Requires backend name/version, last update date, qubits, gates, and payload hash. |
| `parser-azure-target-list` | Azure Quantum | `az quantum target list/show` | Requires workspace, provider, target, target profile, and payload hash. |

These are shape fixtures only. They do not prove that live provider metadata was
retrieved.

## Register Layout Receipt

`QuantumRegisterLayoutReceipt/v1` seal:

```text
04cd4fff62e90a8888e74243fab8bf249d74c795650649c1a545e375fdde49fe
```

Qiskit-style convention recorded:

- bit `n-1` is the leftmost string position;
- bit `0` is the rightmost string position;
- `q[0]` maps to `c[0]` and rightmost;
- `q[1]` maps to `c[1]` and leftmost.

Example interpretation:

| Bitstring | Meaning |
| --- | --- |
| `10` | `q[1]=1`, `q[0]=0` |
| `01` | `q[1]=0`, `q[0]=1` |

## Post-Processing Receipt

The pass adds `QuantumPostProcessingReceipt/v1` with a no-op baseline:

- `raw_result_hash_required=true`;
- `normalized_result_hash_required=true`;
- `mitigation_applied=false`;
- `filtering_applied=false`;
- `truncation_applied=false`;
- `operations=[]`.

Any counts mutation, bit-order mutation, mitigation, filtering, truncation, or
result merging must add a post-processing receipt.

## Negative Fixtures

| Fixture | Expected Result |
| --- | --- |
| `negative-provider-metadata-without-payload-hash` | `REJECT` |
| `negative-azure-unknown-target-kind-promoted-to-hardware` | `REJECT` |
| `negative-register-layout-omitted` | `REJECT` |
| `negative-endian-convention-absent` | `REJECT` |
| `negative-duplicate-json-key-payload` | `REJECT` |
| `negative-binary-payload-treated-as-json` | `REJECT` |
| `negative-float-precision-policy-absent` | `REJECT` |
| `negative-post-processing-without-receipt` | `REJECT` |

## Tool Substrate Receipt

Pass 0017 refreshed the tool surfaces:

| Tool | Status | Note |
| --- | --- | --- |
| Index | `MATCH` | Version 2.8.0; structure-context role observed. |
| Gather | `MATCH` | Version 1.5.0; perception-intake role observed. |
| Telos | `MATCH` | Operator doctor reports 14/14 checks passing and 65 tools. |
| Forum | `MATCH_WITH_SUBMIT_GAP` | Ledger status/verify works; submit remains `UNVERIFIABLE` due to executor JSON parsing. |
| Crucible | `MATCH` | Version 1.1.0; verification-pressure role observed. |

Forum ledger status:

```text
entries=8
checkpoint=71c70b180daa2c24e41d80463a3bc03acddec8fdfacb2d1e3b2c4dd4d26ea42a
chain=true
deep=true
```

## Source Anchors

| Source | Evidence Used |
| --- | --- |
| Amazon Braket GetDevice API | `GetDevice` is the provider metadata input surface for device capabilities. |
| Amazon Braket device properties | Device properties, topology, calibration data, native gate sets, QPU/simulator distinctions. |
| IBM BackendProperties API | Backend properties include backend name/version, last update, qubits, gates, and general fields. |
| IBM Quantum backend information | Dynamic backend properties change after calibration and support optimization/noise-model use. |
| Azure Quantum target CLI | Azure target list/show surface exposes provider/target selection metadata. |
| Azure Quantum job CLI | Job target id and output fields inform target/job receipt separation. |
| IBM Quantum bit-ordering guide | Qiskit bitstrings display bit `n-1` leftmost and bit `0` rightmost. |

## Artifacts

| Artifact | Role |
| --- | --- |
| `tools/probe_cloud_quantum_metadata_parsers.py` | Deterministic provider metadata parser fixture generator. |
| `tools/validate_pass_0017_metadata_parsers.py` | Validator for parser profiles, register layout, post-processing baseline, and negative fixtures. |
| `packets/027-cloud-quantum-metadata-parser-hardening.md` | Human-readable metadata parser hardening packet. |
| `adversarial/pass-0017-metadata-parser-steelman.md` | Forum failure receipt plus local metadata parser steelman. |
| `schemas/cloud-quantum-metadata-parsers-pass-0017.json` | `CloudQuantumProviderMetadataParserSet/v1` fixture and profiles. |
| `schemas/pass-0017-metadata-parser-validator-result.json` | Validator receipt for pass 0017. |
| `schemas/tool-receipts-pass-0017.json` | Compact Index, Gather, Telos, Forum, and Crucible receipts. |
| `crucible/pass-0017-thesis.json` | Falsifiable claims for the seventeenth pass. |
| `crucible/pass-0017-measurements.json` | Measurements/evidence for the seventeenth pass. |
| `crucible/pass-0017-report.md` | Crucible assessment report. |
| `crucible/pass-0017-run.json` | Crucible run record. |

## Primary Next Push

Strict canonicalization and cross-framework layout adapters.

Implement:

- executable duplicate-key detection;
- binary/object-storage payload receipt profiles;
- floating-point precision and rounding policy receipts;
- Qiskit, Braket, Cirq, PennyLane, and QIR register-layout adapters;
- operation-specific post-processing receipts with input/output hashes.

## Natural-Law Promotion

Current promoted natural laws: none.

## Next-Pass Queue

1. Add strict duplicate-key JSON parser fixtures.
2. Add binary payload and object-storage reference receipt fixtures.
3. Add floating-point precision policy receipt fixtures.
4. Add cross-framework `QuantumRegisterLayoutAdapter/v1` profiles.
5. Add operation-specific `QuantumPostProcessingOperation/v1` receipts.
