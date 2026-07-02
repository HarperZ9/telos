# Dogfood Pass 0018 Ledger

Date: 2026-07-01

Status: `CRUCIBLE_MATCH`.

Crucible assessment:

- thesis id: `06cb6c4d2955e456`;
- claims: `9`;
- match: `9`;
- drift: `0`;
- unverifiable: `0`;
- thesis seal: `06cb6c4d2955e456abb26e0fda948beddd4a135ce8e4b35779ec4985ae505b86`;
- verdict seal: `d7d5ec7a1f66e2925029df6a75581b2d51d2c36fec55eaaebbaa02642cbd5b88`;
- measurement seal: `eedc62bbd504da9016e787535c649bd8fec04a0065313bdf89d4dcf61ee27692`;
- assessment seal: `42b11dbdb1892ced33402b88b0be6082f65dfc9739506af71c8b592951df0222`;
- integrity: `seals_ok=True`, `thesis_ok=True`, `verdicts_rederive=True`.

Pass theme: strict canonicalization and cross-framework layout adapters. This
pass adds duplicate-key rejection, binary payload policy, object-storage
content-hash policy, floating-point precision policy, five framework layout
adapters, and operation-level post-processing hashes.

No quantum job, quantum hardware result, quantum advantage claim, theorem proof,
natural law, biological result, material result, medical result, finance result,
or safety result is promoted in this pass.

## Strict Adapter Set

Adapter-set seal:

```text
0727efc532db5c9c759bec5319d0ab547942129880d20823764cba12edd007fd
```

Validator result:

```text
status = MATCH
match = 1
drift = 0
adapter_profile_count = 5
negative_fixture_count = 9
source_anchor_count = 8
```

## Strict Policy

`StrictQuantumCanonicalizationPolicy/v1` requires:

- duplicate JSON key detection;
- binary payload media type;
- binary payload content hash;
- rejection of binary payloads through JSON canonicalization;
- object-storage content hash;
- floating-point precision policy.

Policy hash:

```text
a54c16072736fa63bece139a42caf3265931553087cbca8738058ad7dbd57e62
```

## Layout Adapters

| Adapter | Scope | Status |
| --- | --- | --- |
| `layout-adapter-qiskit` | Qiskit bitstring position policy. | `FRAMEWORK_POLICY_DEFINED` |
| `layout-adapter-amazon-braket` | Braket measurement-count key policy. | `FRAMEWORK_POLICY_DEFINED` |
| `layout-adapter-cirq` | Cirq measurement key, qubit order, and `fold_func`. | `FRAMEWORK_POLICY_DEFINED` |
| `layout-adapter-pennylane` | Counts shape with required wire-order receipt. | `COUNTS_SHAPE_DEFINED_LAYOUT_POLICY_REQUIRED` |
| `layout-adapter-qir` | QIR module and result-record mapping. | `INTERMEDIATE_REPRESENTATION_LAYOUT_POLICY_REQUIRED` |

Design rule: never normalize counts across frameworks unless the matching adapter
and its required receipt fields are present.

## Post-Processing Operation

`QuantumPostProcessingOperation/v1` baseline:

- `operation_kind=NOOP_BASELINE`;
- `input_hash=601220fead53491134647a9c82790700cb98267b764237a93b94320d85dd3747`;
- `output_hash=601220fead53491134647a9c82790700cb98267b764237a93b94320d85dd3747`;
- `parameters_hash=c769c10a29fc6f05ca2164d2b3ccd6668b633a29c99c9e758ec09ab09c03cdbf`;
- `operation_hash=16884278600cf76f54aa463c0e4dc4459afdd71df5c5b046a663ec4eefac4a43`;
- `deterministic=true`.

## Negative Fixtures

| Fixture | Expected Result |
| --- | --- |
| `negative-duplicate-json-key-accepted` | `REJECT` |
| `negative-binary-payload-parsed-as-json` | `REJECT` |
| `negative-object-storage-uri-without-content-hash` | `REJECT` |
| `negative-float-result-without-precision-policy` | `REJECT` |
| `negative-qiskit-counts-using-braket-layout` | `REJECT` |
| `negative-cirq-histogram-without-fold-func` | `REJECT` |
| `negative-pennylane-counts-without-wire-order` | `REJECT` |
| `negative-qir-result-without-record-map` | `REJECT` |
| `negative-post-processing-operation-without-hashes` | `REJECT` |

## Tool Substrate Receipt

Pass 0018 refreshed the tool surfaces:

| Tool | Status | Note |
| --- | --- | --- |
| Index | `MATCH` | Version 2.8.0; structure-context role observed. |
| Gather | `MATCH` | Version 1.5.0; perception-intake role observed. |
| Telos | `MATCH` | Operator doctor reports 14/14 checks passing and 65 tools. |
| Forum | `MATCH_WITH_SUBMIT_GAP` | Ledger status/verify works; submit remains `UNVERIFIABLE` due to executor JSON parsing. |
| Crucible | `MATCH` | Version 1.1.0; verification-pressure role observed. |

Forum ledger status:

```text
entries=9
checkpoint=063a6d962a0711ff98e2b62347ced7d34c42662ae7ff90a50f701bc9294c46b8
chain=true
deep=true
```

## Source Anchors

| Source | Evidence Used |
| --- | --- |
| RFC 8785 JSON Canonicalization Scheme | Canonicalization and JSON-number constraints. |
| Amazon Braket task results | Provider result and task-result context. |
| Amazon Braket SDK task result | Measurement-count key policy anchor. |
| Cirq Result API | Histogram and fold-function adapter requirements. |
| PennyLane counts measurement | Counts shape and wire-order adapter requirement. |
| IBM Quantum bit-ordering guide | Qiskit bitstring position policy. |
| QIR specification | QIR module/result-record mapping requirement. |
| OpenQASM 3 introduction | Program representation and classical/quantum semantics context. |

## Artifacts

| Artifact | Role |
| --- | --- |
| `tools/probe_quantum_strict_canonicalization_adapters.py` | Deterministic strict canonicalization and layout-adapter generator. |
| `tools/validate_pass_0018_strict_canonicalization_adapters.py` | Validator for strict policies, adapters, post-processing operation, and negative fixtures. |
| `packets/028-quantum-strict-canonicalization-adapters.md` | Human-readable strict canonicalization adapter packet. |
| `adversarial/pass-0018-strict-adapter-steelman.md` | Forum failure receipt plus local strict-adapter steelman. |
| `schemas/quantum-strict-canonicalization-adapters-pass-0018.json` | `QuantumStrictCanonicalizationAdapterSet/v1` fixture set. |
| `schemas/pass-0018-strict-canonicalization-adapter-validator-result.json` | Validator receipt for pass 0018. |
| `schemas/tool-receipts-pass-0018.json` | Compact Index, Gather, Telos, Forum, and Crucible receipts. |
| `crucible/pass-0018-thesis.json` | Falsifiable claims for the eighteenth pass. |
| `crucible/pass-0018-measurements.json` | Measurements/evidence for the eighteenth pass. |
| `crucible/pass-0018-report.md` | Crucible assessment report. |
| `crucible/pass-0018-run.json` | Crucible run record. |

## Primary Next Push

Executable adapters and generalized receipts.

Implement:

- shared strict JSON loader used by all proof-packet parsers;
- `NumericPrecisionReceipt/v1`;
- `ObjectStorageEvidenceReceipt/v1`;
- executable framework output fixtures for Qiskit, Braket, Cirq, PennyLane, and
  QIR;
- a market pass on quantum workflow/provenance gaps against provider dashboards,
  Qiskit Runtime, Braket, Cirq, PennyLane, Covalent, and workflow engines.

## Natural-Law Promotion

Current promoted natural laws: none.

## Next-Pass Queue

1. Add a shared strict JSON loader fixture and validator.
2. Add `NumericPrecisionReceipt/v1`.
3. Add `ObjectStorageEvidenceReceipt/v1`.
4. Add executable framework output fixtures for Qiskit, Braket, Cirq, PennyLane,
   and QIR.
5. Add a focused quantum workflow/provenance market map.
