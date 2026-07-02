# Pass 0018 - Quantum Strict Canonicalization Adapters

Status: STRICT_ADAPTER_MATCH
Date: 2026-07-01

## Purpose

Pass 0018 hardens the receipt layer where provider payloads and framework result
formats can silently diverge:

- duplicate JSON keys;
- binary or compressed result payloads;
- object-storage references;
- floating-point precision;
- cross-framework register-layout adapters;
- post-processing operation hashes.

No cloud job was run. No hardware result is promoted.

## Source Anchors

- RFC 8785 JSON Canonicalization Scheme: https://www.rfc-editor.org/info/rfc8785/
- Amazon Braket task results: https://docs.aws.amazon.com/braket/latest/developerguide/braket-submit-tasks-to-braket.html
- Amazon Braket SDK task result: https://amazon-braket-sdk-python.readthedocs.io/en/latest/_apidoc/braket.tasks.gate_model_quantum_task_result.html
- Cirq Result API: https://quantumai.google/reference/python/cirq/Result
- PennyLane counts measurement: https://docs.pennylane.ai/en/stable/code/qp_measurements.html
- IBM Quantum bit-ordering guide: https://quantum.cloud.ibm.com/docs/guides/bit-ordering
- QIR specification: https://github.com/qir-alliance/qir-spec/blob/main/specification/README.md
- OpenQASM 3 introduction: https://openqasm.com/versions/3.0/intro.html

## Strict Policy

The pass defines `StrictQuantumCanonicalizationPolicy/v1`.

Required guardrails:

- duplicate JSON key detection;
- binary payload media type and content hash;
- rejection of binary payloads through JSON canonicalization;
- object-storage references with provider, URI, retrieval timestamp, content hash,
  and etag or generation;
- floating-point precision policy.

Fixture:

```json
{"counts":{"00":1,"00":2},"shots":3}
```

The duplicate key `00` must be rejected.

## Layout Adapters

The pass defines five `QuantumRegisterLayoutAdapter/v1` profiles:

| Adapter | Scope | Status |
| --- | --- | --- |
| `layout-adapter-qiskit` | Qiskit string-position policy. | `FRAMEWORK_POLICY_DEFINED` |
| `layout-adapter-amazon-braket` | Braket measurement-count key policy. | `FRAMEWORK_POLICY_DEFINED` |
| `layout-adapter-cirq` | Cirq measurement key, qubit order, and `fold_func`. | `FRAMEWORK_POLICY_DEFINED` |
| `layout-adapter-pennylane` | Counts shape plus required wire-order binding. | `COUNTS_SHAPE_DEFINED_LAYOUT_POLICY_REQUIRED` |
| `layout-adapter-qir` | QIR module/result-record mapping. | `INTERMEDIATE_REPRESENTATION_LAYOUT_POLICY_REQUIRED` |

The design rule is intentionally strict: never normalize counts across frameworks
unless the matching adapter and its required receipt fields are present.

## Post-Processing Operation

The pass adds `QuantumPostProcessingOperation/v1`.

Baseline operation:

- `operation_kind=NOOP_BASELINE`;
- `input_hash` equals `output_hash`;
- `parameters_hash` present;
- `operation_hash` present;
- `deterministic=true`.

Any real operation must bind input hash, output hash, parameters, determinism, and
operation kind.

## Negative Fixtures

The validator must reject:

- duplicate JSON keys accepted as canonical JSON;
- binary payload parsed as JSON;
- object-storage URI without content hash;
- floating-point result without precision policy;
- Qiskit counts normalized through Braket adapter;
- Cirq histogram without measurement key and `fold_func`;
- PennyLane counts without wire-order receipt;
- QIR result without result-record map;
- post-processing operation without input or output hash.

## Architecture Implication

This pass is not quantum-specific in the deeper architecture. It defines the
minimum shape for any Telos/Build scientific proof packet where raw outputs pass
through a framework:

- framework adapter;
- raw evidence hash;
- semantic normalized object;
- transformation policy;
- precision policy;
- layout/unit policy;
- operation-level input/output hashes.

That same shape applies to BuildLang/buildc runtime outputs, rendering/color
measurements, finance simulations, security scans, and biology lab data.

## Artifacts

- `tools/probe_quantum_strict_canonicalization_adapters.py`
- `tools/validate_pass_0018_strict_canonicalization_adapters.py`
- `schemas/quantum-strict-canonicalization-adapters-pass-0018.json`

## Non-Promotion Statement

Pass 0018 defines strict canonicalization and framework layout adapter fixtures
only. It does not run a quantum job, prove a theorem, or promote a quantum
hardware result.
