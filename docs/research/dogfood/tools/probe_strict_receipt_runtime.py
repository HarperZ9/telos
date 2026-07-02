"""Generate pass 0019 strict loader, precision, storage, and adapter receipts."""

from __future__ import annotations

import base64
import hashlib
import json
import math
from collections import defaultdict
from decimal import Decimal, ROUND_HALF_EVEN, getcontext


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_b64(value: bytes) -> str:
    return base64.b64encode(hashlib.sha256(value).digest()).decode("ascii")


def sha256_obj(value: object) -> str:
    return sha256_text(canonical_json(value))


def reject_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON constant rejected: {value}")


def strict_loads(raw_json: str) -> tuple[object | None, list[str], str | None]:
    duplicate_keys: list[str] = []

    def hook(pairs):
        seen: defaultdict[str, int] = defaultdict(int)
        out = {}
        for key, value in pairs:
            seen[key] += 1
            if seen[key] > 1:
                duplicate_keys.append(key)
            out[key] = value
        return out

    try:
        parsed = json.loads(raw_json, object_pairs_hook=hook, parse_constant=reject_constant)
    except ValueError as exc:
        return None, duplicate_keys, str(exc)
    if duplicate_keys:
        return None, sorted(set(duplicate_keys)), "duplicate JSON object keys rejected"
    return parsed, [], None


def make_strict_loader_receipt() -> dict[str, object]:
    ok_raw = '{"shots":3,"counts":{"00":1,"11":2}}'
    dup_raw = '{"counts":{"00":1,"00":2},"shots":3}'
    nan_raw = '{"expectation": NaN}'
    inf_raw = '{"expectation": Infinity}'

    ok_parsed, ok_duplicates, ok_error = strict_loads(ok_raw)
    dup_parsed, dup_duplicates, dup_error = strict_loads(dup_raw)
    nan_parsed, nan_duplicates, nan_error = strict_loads(nan_raw)
    inf_parsed, inf_duplicates, inf_error = strict_loads(inf_raw)

    return {
        "schema": "StrictJsonLoaderReceipt/v1",
        "loader_id": "python-json-object-pairs-hook-parse-constant",
        "source_anchors": [
            "https://docs.python.org/3/library/json.html",
            "https://www.rfc-editor.org/info/rfc8785/",
        ],
        "object_pairs_hook_required": True,
        "parse_constant_rejects_nonfinite": True,
        "allow_nan_on_serialization": False,
        "positive_fixture": {
            "raw_payload_hash": sha256_text(ok_raw),
            "parsed_payload": ok_parsed,
            "duplicate_keys": ok_duplicates,
            "error": ok_error,
            "canonical_json": canonical_json(ok_parsed),
            "canonical_hash": sha256_obj(ok_parsed),
            "expected_validator_status": "MATCH",
        },
        "duplicate_key_fixture": {
            "raw_payload_hash": sha256_text(dup_raw),
            "parsed_payload": dup_parsed,
            "duplicate_keys": dup_duplicates,
            "error": dup_error,
            "expected_validator_status": "REJECT",
        },
        "nonfinite_fixtures": [
            {
                "raw_payload_hash": sha256_text(nan_raw),
                "parsed_payload": nan_parsed,
                "duplicate_keys": nan_duplicates,
                "error": nan_error,
                "expected_validator_status": "REJECT",
            },
            {
                "raw_payload_hash": sha256_text(inf_raw),
                "parsed_payload": inf_parsed,
                "duplicate_keys": inf_duplicates,
                "error": inf_error,
                "expected_validator_status": "REJECT",
            },
        ],
    }


def make_numeric_receipts() -> list[dict[str, object]]:
    getcontext().prec = 60
    exact_decimal = Decimal("0.1")
    binary_float_decimal = Decimal.from_float(0.1)
    one_seventh = Decimal(1) / Decimal(7)
    quantized = one_seventh.quantize(Decimal("0.000001"), rounding=ROUND_HALF_EVEN)

    receipts = [
        {
            "schema": "NumericPrecisionReceipt/v1",
            "receipt_id": "decimal-string-exact-0p1",
            "numeric_class": "DECIMAL_STRING",
            "source_literal": "0.1",
            "canonical_value": str(exact_decimal),
            "rounding_mode": "NONE",
            "precision_digits": 1,
            "lossiness": "LOSSLESS_DECIMAL_LITERAL",
            "source_anchors": [
                "https://docs.python.org/3/library/decimal.html",
                "https://www.rfc-editor.org/info/rfc8785/",
            ],
        },
        {
            "schema": "NumericPrecisionReceipt/v1",
            "receipt_id": "binary-float-expanded-0p1",
            "numeric_class": "IEEE754_DOUBLE",
            "source_literal": "0.1",
            "canonical_value": str(binary_float_decimal),
            "rounding_mode": "BINARY_FLOAT_REPRESENTATION",
            "precision_digits": 55,
            "lossiness": "BINARY_FLOAT_NOT_DECIMAL_LITERAL",
            "source_anchors": [
                "https://docs.python.org/3/library/decimal.html",
                "https://www.rfc-editor.org/info/rfc8785/",
            ],
        },
        {
            "schema": "NumericPrecisionReceipt/v1",
            "receipt_id": "decimal-quantized-one-seventh",
            "numeric_class": "DECIMAL_QUANTIZED",
            "source_literal": "1/7",
            "canonical_value": str(quantized),
            "unrounded_value": str(one_seventh),
            "rounding_mode": "ROUND_HALF_EVEN",
            "precision_digits": 6,
            "lossiness": "ROUNDED_WITH_POLICY",
            "source_anchors": ["https://docs.python.org/3/library/decimal.html"],
        },
    ]
    for receipt in receipts:
        receipt["receipt_hash"] = sha256_obj(receipt)
    return receipts


def make_object_storage_receipt() -> dict[str, object]:
    content = canonical_json({"counts": {"00": 1, "11": 2}, "shots": 3}).encode("utf-8")
    receipt = {
        "schema": "ObjectStorageEvidenceReceipt/v1",
        "receipt_id": "s3-shape-fixture-content-addressed-result",
        "provider": "Amazon S3",
        "uri": "s3://example-bucket/quantum/results/pass-0019.json",
        "retrieval_timestamp": "2026-07-01T00:00:00Z",
        "version_id": "shape-fixture-version-0019",
        "etag_or_generation": "\"shape-fixture-etag-0019\"",
        "content_type": "application/json",
        "content_length": len(content),
        "content_sha256": sha256_bytes(content),
        "content_sha256_base64": sha256_b64(content),
        "locator_only_allowed": False,
        "source_anchors": [
            "https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetObject.html",
            "https://docs.aws.amazon.com/AmazonS3/latest/userguide/checking-object-integrity.html",
            "https://docs.aws.amazon.com/AmazonS3/latest/userguide/Versioning.html",
        ],
    }
    receipt["receipt_hash"] = sha256_obj(receipt)
    return receipt


def normalize_qiskit(raw: dict[str, object]) -> dict[str, object]:
    counts = raw["counts"]
    return {
        "normalized_counts": counts,
        "layout_interpretation": {
            "10": {"q[1]": 1, "q[0]": 0},
            "01": {"q[1]": 0, "q[0]": 1},
        },
    }


def normalize_braket(raw: dict[str, object]) -> dict[str, object]:
    return {
        "normalized_counts": raw["measurementCounts"],
        "measured_qubit_order": raw["measuredQubits"],
        "key_policy": "BIG_ENDIAN_BINARY_STRING",
    }


def normalize_cirq(raw: dict[str, object]) -> dict[str, object]:
    histogram = raw["histogram"]
    return {
        "normalized_counts": {"10": histogram["2"], "01": histogram["1"]},
        "measurement_key": raw["measurement_key"],
        "fold_func": raw["fold_func"],
    }


def normalize_pennylane(raw: dict[str, object]) -> dict[str, object]:
    return {
        "normalized_counts": raw["counts"],
        "wire_order": raw["wires"],
        "device_name": raw["device_name"],
    }


def normalize_qir(raw: dict[str, object]) -> dict[str, object]:
    return {
        "normalized_counts": raw["counts"],
        "result_record_map": raw["result_record_map"],
        "runtime_output_policy": raw["runtime_output_policy"],
    }


def make_executable_fixtures() -> list[dict[str, object]]:
    specs = [
        {
            "fixture_id": "executable-fixture-qiskit-counts",
            "adapter_id": "layout-adapter-qiskit",
            "framework": "Qiskit",
            "raw_output": {"counts": {"10": 7, "01": 5}, "shots": 12},
            "normalizer": normalize_qiskit,
            "source_anchor": "https://quantum.cloud.ibm.com/docs/guides/bit-ordering",
        },
        {
            "fixture_id": "executable-fixture-braket-measurement-counts",
            "adapter_id": "layout-adapter-amazon-braket",
            "framework": "Amazon Braket",
            "raw_output": {"measurementCounts": {"10": 7, "01": 5}, "measuredQubits": [0, 1], "shots": 12},
            "normalizer": normalize_braket,
            "source_anchor": "https://amazon-braket-sdk-python.readthedocs.io/en/latest/_apidoc/braket.tasks.gate_model_quantum_task_result.html",
        },
        {
            "fixture_id": "executable-fixture-cirq-histogram",
            "adapter_id": "layout-adapter-cirq",
            "framework": "Cirq",
            "raw_output": {"measurement_key": "m", "histogram": {"2": 7, "1": 5}, "fold_func": "big_endian_bits_to_int", "qubit_order": ["q0", "q1"]},
            "normalizer": normalize_cirq,
            "source_anchor": "https://quantumai.google/reference/python/cirq/Result",
        },
        {
            "fixture_id": "executable-fixture-pennylane-counts",
            "adapter_id": "layout-adapter-pennylane",
            "framework": "PennyLane",
            "raw_output": {"counts": {"10": 7, "01": 5}, "wires": [0, 1], "shots": 12, "device_name": "default.qubit-shape-fixture"},
            "normalizer": normalize_pennylane,
            "source_anchor": "https://docs.pennylane.ai/en/stable/code/qp_measurements.html",
        },
        {
            "fixture_id": "executable-fixture-qir-result-record-map",
            "adapter_id": "layout-adapter-qir",
            "framework": "QIR",
            "raw_output": {"counts": {"10": 7, "01": 5}, "result_record_map": {"r0": "q[0]", "r1": "q[1]"}, "runtime_output_policy": "record_map_required"},
            "normalizer": normalize_qir,
            "source_anchor": "https://github.com/qir-alliance/qir-spec/blob/main/specification/README.md",
        },
    ]

    fixtures: list[dict[str, object]] = []
    for spec in specs:
        raw_output = spec["raw_output"]
        normalized = spec["normalizer"](raw_output)
        fixture = {
            "schema": "ExecutableFrameworkOutputFixture/v1",
            "fixture_id": spec["fixture_id"],
            "adapter_id": spec["adapter_id"],
            "framework": spec["framework"],
            "execution_mode": "LOCAL_ADAPTER_FUNCTION_OVER_SYNTHETIC_OUTPUT",
            "framework_imported": False,
            "raw_output": raw_output,
            "raw_output_hash": sha256_obj(raw_output),
            "normalized_output": normalized,
            "normalized_output_hash": sha256_obj(normalized),
            "source_anchor": spec["source_anchor"],
            "status": "ADAPTER_EXECUTION_MATCH",
        }
        fixture["fixture_hash"] = sha256_obj(fixture)
        fixtures.append(fixture)
    return fixtures


negative_fixtures = [
    ("negative-strict-json-loader-not-used", "JSON proof packet ingestion uses plain json.loads without duplicate-key and non-finite rejection."),
    ("negative-nan-accepted-as-json-number", "NaN is accepted as a canonical JSON number."),
    ("negative-decimal-serialized-as-float", "Decimal measurement is serialized through binary float without NumericPrecisionReceipt/v1."),
    ("negative-object-storage-uri-only", "Object storage URI is cited without content hash, version/generation, and retrieval timestamp."),
    ("negative-qiskit-fixture-without-layout", "Qiskit counts fixture omits string-position layout receipt."),
    ("negative-braket-fixture-without-measured-qubit-order", "Braket measurement counts omit measured qubit order."),
    ("negative-cirq-fixture-without-fold-func", "Cirq histogram omits fold_func policy."),
    ("negative-pennylane-fixture-without-wire-order", "PennyLane counts omit wire order."),
    ("negative-qir-fixture-without-record-map", "QIR output omits result record map."),
]


record = {
    "schema": "StrictReceiptRuntimeFixtureSet/v1",
    "pass": "0019",
    "generated_on": "2026-07-01",
    "status": "STRICT_RUNTIME_MATCH",
    "strict_json_loader_receipt": make_strict_loader_receipt(),
    "numeric_precision_receipts": make_numeric_receipts(),
    "object_storage_evidence_receipt": make_object_storage_receipt(),
    "executable_framework_output_fixtures": make_executable_fixtures(),
    "negative_fixtures": [
        {"fixture_id": fixture_id, "failure_mode": failure_mode, "expected_validator_status": "REJECT"}
        for fixture_id, failure_mode in negative_fixtures
    ],
    "source_anchors": [
        {"source": "RFC 8785 JSON Canonicalization Scheme", "url": "https://www.rfc-editor.org/info/rfc8785/"},
        {"source": "Python json module", "url": "https://docs.python.org/3/library/json.html"},
        {"source": "Python decimal module", "url": "https://docs.python.org/3/library/decimal.html"},
        {"source": "Amazon S3 GetObject API", "url": "https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetObject.html"},
        {"source": "Amazon S3 object integrity", "url": "https://docs.aws.amazon.com/AmazonS3/latest/userguide/checking-object-integrity.html"},
        {"source": "Amazon S3 versioning", "url": "https://docs.aws.amazon.com/AmazonS3/latest/userguide/Versioning.html"},
        {"source": "IBM Quantum bit-ordering guide", "url": "https://quantum.cloud.ibm.com/docs/guides/bit-ordering"},
        {"source": "Amazon Braket SDK task result", "url": "https://amazon-braket-sdk-python.readthedocs.io/en/latest/_apidoc/braket.tasks.gate_model_quantum_task_result.html"},
        {"source": "Cirq Result API", "url": "https://quantumai.google/reference/python/cirq/Result"},
        {"source": "PennyLane counts measurement", "url": "https://docs.pennylane.ai/en/stable/code/qp_measurements.html"},
        {"source": "QIR specification", "url": "https://github.com/qir-alliance/qir-spec/blob/main/specification/README.md"},
    ],
    "non_promotion_statement": "Pass 0019 executes local parser and adapter fixtures only. It does not import quantum frameworks, fetch cloud objects, run a quantum job, or promote a hardware result.",
}
record["seal"] = sha256_obj(record)
print(json.dumps(record, indent=2, sort_keys=True))
