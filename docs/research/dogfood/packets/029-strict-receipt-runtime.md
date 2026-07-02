# Pass 0019 - Strict Receipt Runtime

Status: STRICT_RUNTIME_MATCH
Date: 2026-07-01

## Purpose

Pass 0019 turns pass 0018's policy shapes into local executable fixtures:

- a strict JSON loader that rejects duplicate object keys and non-finite JSON
  constants;
- `NumericPrecisionReceipt/v1` examples for exact decimal strings, binary float
  expansion, and rounded decimal quantization;
- `ObjectStorageEvidenceReceipt/v1` with locator, version, retrieval timestamp,
  content length, and content hashes;
- executable adapter functions over synthetic Qiskit, Braket, Cirq, PennyLane,
  and QIR-shaped outputs.

This pass does not import quantum frameworks, fetch cloud objects, run quantum
jobs, or promote hardware results.

## Source Anchors

- RFC 8785 JSON Canonicalization Scheme: https://www.rfc-editor.org/info/rfc8785/
- Python json module: https://docs.python.org/3/library/json.html
- Python decimal module: https://docs.python.org/3/library/decimal.html
- Amazon S3 GetObject API: https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetObject.html
- Amazon S3 object integrity: https://docs.aws.amazon.com/AmazonS3/latest/userguide/checking-object-integrity.html
- Amazon S3 versioning: https://docs.aws.amazon.com/AmazonS3/latest/userguide/Versioning.html
- IBM Quantum bit-ordering guide: https://quantum.cloud.ibm.com/docs/guides/bit-ordering
- Amazon Braket SDK task result: https://amazon-braket-sdk-python.readthedocs.io/en/latest/_apidoc/braket.tasks.gate_model_quantum_task_result.html
- Cirq Result API: https://quantumai.google/reference/python/cirq/Result
- PennyLane counts measurement: https://docs.pennylane.ai/en/stable/code/qp_measurements.html
- QIR specification: https://github.com/qir-alliance/qir-spec/blob/main/specification/README.md

## Strict JSON Loader

`StrictJsonLoaderReceipt/v1` uses Python's `object_pairs_hook` shape to detect
duplicate keys and `parse_constant` shape to reject non-finite JSON constants.

Fixtures:

| Fixture | Expected |
| --- | --- |
| Positive JSON payload | `MATCH` |
| Duplicate key `00` | `REJECT` |
| `NaN` constant | `REJECT` |
| `Infinity` constant | `REJECT` |

The loader serializes with `allow_nan=false` and preserves a canonical hash for
the positive payload.

## Numeric Precision

`NumericPrecisionReceipt/v1` examples:

| Receipt | Class | Lossiness |
| --- | --- | --- |
| `decimal-string-exact-0p1` | `DECIMAL_STRING` | `LOSSLESS_DECIMAL_LITERAL` |
| `binary-float-expanded-0p1` | `IEEE754_DOUBLE` | `BINARY_FLOAT_NOT_DECIMAL_LITERAL` |
| `decimal-quantized-one-seventh` | `DECIMAL_QUANTIZED` | `ROUNDED_WITH_POLICY` |

The important rule is that measurements cannot silently move between decimal
strings, binary floats, and rounded decimal values without a receipt.

## Object Storage Evidence

`ObjectStorageEvidenceReceipt/v1` records a shape-only S3 locator with:

- provider;
- URI;
- retrieval timestamp;
- version id;
- ETag or generation;
- content type;
- content length;
- SHA-256 hex;
- SHA-256 base64;
- `locator_only_allowed=false`.

A storage URI by itself remains a locator, not immutable evidence.

## Executable Adapter Fixtures

The pass adds five `ExecutableFrameworkOutputFixture/v1` receipts. Each fixture
runs a local adapter function over a synthetic framework-shaped output, records raw
and normalized hashes, and keeps `framework_imported=false`.

| Fixture | Framework | Adapter |
| --- | --- | --- |
| `executable-fixture-qiskit-counts` | Qiskit | `layout-adapter-qiskit` |
| `executable-fixture-braket-measurement-counts` | Amazon Braket | `layout-adapter-amazon-braket` |
| `executable-fixture-cirq-histogram` | Cirq | `layout-adapter-cirq` |
| `executable-fixture-pennylane-counts` | PennyLane | `layout-adapter-pennylane` |
| `executable-fixture-qir-result-record-map` | QIR | `layout-adapter-qir` |

These are adapter-execution receipts, not framework integration tests.

## Negative Fixtures

The validator must reject:

- proof packet ingestion without the strict JSON loader;
- `NaN` accepted as canonical JSON;
- decimal measurement serialized through binary float without precision receipt;
- object-storage URI without content hash, version/generation, and retrieval time;
- Qiskit counts without layout;
- Braket counts without measured qubit order;
- Cirq histogram without `fold_func`;
- PennyLane counts without wire order;
- QIR output without result record map.

## Architecture Implication

This pass moves the proof packet layer from static receipt taxonomy toward runtime
adapter execution. The same pattern should be reused outside quantum:

- strict loader for every evidence format;
- numeric precision receipt for scientific, financial, and color outputs;
- object-storage evidence receipt for remote artifacts;
- adapter execution receipts for every external framework or runtime.

## Artifacts

- `tools/probe_strict_receipt_runtime.py`
- `tools/validate_pass_0019_strict_receipt_runtime.py`
- `schemas/strict-receipt-runtime-fixtures-pass-0019.json`

## Non-Promotion Statement

Pass 0019 executes local parser and adapter fixtures only. It does not import
quantum frameworks, fetch cloud objects, run a quantum job, prove a theorem, or
promote a hardware result.
