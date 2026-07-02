"""Generate pass 0018 strict canonicalization and layout-adapter fixtures."""

from __future__ import annotations

import hashlib
import json
from collections import defaultdict


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_obj(value: object) -> str:
    return sha256_text(canonical_json(value))


def duplicate_paths(raw_json: str) -> list[str]:
    paths: list[str] = []

    def hook(pairs):
        seen: defaultdict[str, int] = defaultdict(int)
        out = {}
        for key, value in pairs:
            seen[key] += 1
            if seen[key] > 1:
                paths.append(key)
            out[key] = value
        return out

    json.loads(raw_json, object_pairs_hook=hook)
    return sorted(set(paths))


duplicate_key_payload = "{\"counts\":{\"00\":1,\"00\":2},\"shots\":3}"
binary_payload = b"\x1f\x8b\x08\x00telos-pass-0018"

strict_policy = {
    "schema": "StrictQuantumCanonicalizationPolicy/v1",
    "policy_id": "strict-json-binary-float-object-storage",
    "duplicate_json_key_detection_required": True,
    "duplicate_key_fixture": {
        "raw_payload": duplicate_key_payload,
        "detected_duplicate_keys": duplicate_paths(duplicate_key_payload),
        "expected_validator_status": "REJECT",
    },
    "binary_payload_policy": {
        "media_type_required": True,
        "content_hash_required": True,
        "parsed_json_allowed": False,
        "sample_media_type": "application/gzip",
        "sample_payload_hash": sha256_bytes(binary_payload),
    },
    "object_storage_reference_policy": {
        "required_fields": ["uri", "provider", "retrieval_timestamp", "content_hash", "etag_or_generation"],
        "claim_rule": "A storage URI without a content hash is a locator, not an immutable evidence receipt.",
    },
    "floating_point_policy": {
        "precision_policy_required": True,
        "canonicalization_reference": "RFC 8785 constrains JSON numbers to IEEE 754 double precision; higher precision should be represented as strings.",
        "sample_value": 0.1,
        "sample_policy": "IEEE754_DOUBLE_OR_DECIMAL_STRING_REQUIRED",
    },
}
strict_policy["policy_hash"] = sha256_obj(strict_policy)

adapter_profiles = [
    {
        "adapter_id": "layout-adapter-qiskit",
        "framework": "Qiskit",
        "schema": "QuantumRegisterLayoutAdapter/v1",
        "source_anchor": "https://quantum.cloud.ibm.com/docs/guides/bit-ordering",
        "known_policy": "Bit n-1 is displayed leftmost and bit 0 rightmost in strings.",
        "required_receipt_fields": ["quantum_registers", "classical_registers", "measurement_map", "string_position_policy"],
        "adapter_status": "FRAMEWORK_POLICY_DEFINED",
    },
    {
        "adapter_id": "layout-adapter-amazon-braket",
        "framework": "Amazon Braket",
        "schema": "QuantumRegisterLayoutAdapter/v1",
        "source_anchor": "https://amazon-braket-sdk-python.readthedocs.io/en/latest/_apidoc/braket.tasks.gate_model_quantum_task_result.html",
        "known_policy": "Measurement-count keys are big-endian binary strings in the SDK result helper.",
        "required_receipt_fields": ["measured_qubit_order", "measurement_counts_key_policy", "result_source"],
        "adapter_status": "FRAMEWORK_POLICY_DEFINED",
    },
    {
        "adapter_id": "layout-adapter-cirq",
        "framework": "Cirq",
        "schema": "QuantumRegisterLayoutAdapter/v1",
        "source_anchor": "https://quantumai.google/reference/python/cirq/Result",
        "known_policy": "Result.histogram fold_func defaults to interpreting sampled bits as a big-endian integer.",
        "required_receipt_fields": ["measurement_key", "qubit_order", "fold_func", "histogram_key_policy"],
        "adapter_status": "FRAMEWORK_POLICY_DEFINED",
    },
    {
        "adapter_id": "layout-adapter-pennylane",
        "framework": "PennyLane",
        "schema": "QuantumRegisterLayoutAdapter/v1",
        "source_anchor": "https://docs.pennylane.ai/en/stable/code/qp_measurements.html",
        "known_policy": "Counts return a dictionary of sampled quantum states; proof packets must still bind wire order and device policy.",
        "required_receipt_fields": ["wire_order", "counts_key_policy", "device_name", "shots"],
        "adapter_status": "COUNTS_SHAPE_DEFINED_LAYOUT_POLICY_REQUIRED",
    },
    {
        "adapter_id": "layout-adapter-qir",
        "framework": "QIR",
        "schema": "QuantumRegisterLayoutAdapter/v1",
        "source_anchor": "https://github.com/qir-alliance/qir-spec/blob/main/specification/README.md",
        "known_policy": "QIR is an LLVM-based representation for quantum programs; proof packets must bind output-recording and result mapping policy.",
        "required_receipt_fields": ["qir_module_hash", "result_record_map", "runtime_output_policy"],
        "adapter_status": "INTERMEDIATE_REPRESENTATION_LAYOUT_POLICY_REQUIRED",
    },
]
for adapter in adapter_profiles:
    adapter["adapter_hash"] = sha256_obj(adapter)

post_processing_operation = {
    "schema": "QuantumPostProcessingOperation/v1",
    "operation_id": "counts-normalization-noop",
    "operation_kind": "NOOP_BASELINE",
    "input_hash": "601220fead53491134647a9c82790700cb98267b764237a93b94320d85dd3747",
    "output_hash": "601220fead53491134647a9c82790700cb98267b764237a93b94320d85dd3747",
    "parameters_hash": sha256_obj({"operation": "noop"}),
    "deterministic": True,
}
post_processing_operation["operation_hash"] = sha256_obj(post_processing_operation)

negative_fixtures = [
    ("negative-duplicate-json-key-accepted", "Duplicate JSON key payload is accepted as canonical JSON."),
    ("negative-binary-payload-parsed-as-json", "Binary payload is routed through JSON canonicalization."),
    ("negative-object-storage-uri-without-content-hash", "Object storage URI is treated as immutable evidence without content hash."),
    ("negative-float-result-without-precision-policy", "Floating-point result is normalized without precision policy."),
    ("negative-qiskit-counts-using-braket-layout", "Qiskit counts are normalized using the Braket adapter."),
    ("negative-cirq-histogram-without-fold-func", "Cirq histogram is cited without measurement key and fold_func policy."),
    ("negative-pennylane-counts-without-wire-order", "PennyLane counts are cited without wire-order receipt."),
    ("negative-qir-result-without-record-map", "QIR result output is cited without result-record map."),
    ("negative-post-processing-operation-without-hashes", "Post-processing operation lacks input or output hash."),
]

record = {
    "schema": "QuantumStrictCanonicalizationAdapterSet/v1",
    "pass": "0018",
    "generated_on": "2026-07-01",
    "status": "STRICT_ADAPTER_MATCH",
    "strict_policy": strict_policy,
    "adapter_profiles": adapter_profiles,
    "post_processing_operation": post_processing_operation,
    "negative_fixtures": [
        {"fixture_id": fixture_id, "failure_mode": failure_mode, "expected_validator_status": "REJECT"}
        for fixture_id, failure_mode in negative_fixtures
    ],
    "source_anchors": [
        {"source": "RFC 8785 JSON Canonicalization Scheme", "url": "https://www.rfc-editor.org/info/rfc8785/"},
        {"source": "Amazon Braket task results", "url": "https://docs.aws.amazon.com/braket/latest/developerguide/braket-submit-tasks-to-braket.html"},
        {"source": "Amazon Braket SDK task result", "url": "https://amazon-braket-sdk-python.readthedocs.io/en/latest/_apidoc/braket.tasks.gate_model_quantum_task_result.html"},
        {"source": "Cirq Result API", "url": "https://quantumai.google/reference/python/cirq/Result"},
        {"source": "PennyLane counts measurement", "url": "https://docs.pennylane.ai/en/stable/code/qp_measurements.html"},
        {"source": "IBM Quantum bit-ordering guide", "url": "https://quantum.cloud.ibm.com/docs/guides/bit-ordering"},
        {"source": "QIR specification", "url": "https://github.com/qir-alliance/qir-spec/blob/main/specification/README.md"},
        {"source": "OpenQASM 3 introduction", "url": "https://openqasm.com/versions/3.0/intro.html"},
    ],
    "non_promotion_statement": "Pass 0018 defines strict canonicalization and framework layout adapter fixtures only. It does not run a quantum job or promote a hardware result.",
}
record["seal"] = sha256_obj(record)
print(json.dumps(record, indent=2, sort_keys=True))
