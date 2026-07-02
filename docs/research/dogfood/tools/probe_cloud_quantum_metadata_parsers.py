"""Generate pass 0017 cloud quantum metadata parser fixtures."""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_obj(value: object) -> str:
    return sha256_text(canonical_json(value))


def with_payload_hash(payload: dict[str, object]) -> dict[str, object]:
    payload = deepcopy(payload)
    payload["payload_hash"] = sha256_obj({k: v for k, v in payload.items() if k != "payload_hash"})
    return payload


braket_sample = with_payload_hash(
    {
        "deviceArn": "arn:aws:braket:us-east-1::device/qpu/example/ExampleQPU",
        "deviceName": "ExampleQPU",
        "deviceType": "QPU",
        "deviceStatus": "ONLINE",
        "providerName": "ExampleProvider",
        "deviceCapabilities": {
            "action": {"braket.ir.openqasm.program": {"supportedOperations": ["x", "cnot"]}},
            "paradigm": {"qubitCount": 2, "connectivity": {"fullyConnected": False}},
        },
    }
)

ibm_sample = with_payload_hash(
    {
        "backend_name": "example_backend",
        "backend_version": "1.2.3",
        "last_update_date": "2026-07-01T00:00:00Z",
        "qubits": [
            [{"name": "T1", "date": "2026-07-01T00:00:00Z", "unit": "us", "value": 100.0}],
            [{"name": "T1", "date": "2026-07-01T00:00:00Z", "unit": "us", "value": 95.0}],
        ],
        "gates": [
            {
                "gate": "cx",
                "qubits": [0, 1],
                "parameters": [
                    {"name": "gate_error", "date": "2026-07-01T00:00:00Z", "unit": "", "value": 0.01}
                ],
            }
        ],
        "general": [],
    }
)

azure_sample = with_payload_hash(
    {
        "workspace_ref": "subscriptions/example/resourceGroups/example/providers/Microsoft.Quantum/workspaces/example",
        "provider_id": "example-provider",
        "target_id": "example.qpu",
        "target_profile": "hardware",
        "availability": "Available",
        "capability_profile": "qir-base",
        "job_submission": {"input_data_format": "qir.v1", "output_data_format": "microsoft.quantum-results.v1"},
    }
)

register_layout = {
    "schema": "QuantumRegisterLayoutReceipt/v1",
    "layout_id": "qiskit-two-qubit-counts-layout",
    "source_anchor": "https://quantum.cloud.ibm.com/docs/guides/bit-ordering",
    "convention": "Qiskit strings display bit n-1 leftmost and bit 0 rightmost.",
    "quantum_registers": [{"name": "q", "size": 2, "indices": [0, 1]}],
    "classical_registers": [{"name": "c", "size": 2, "indices": [0, 1]}],
    "measurement_map": [
        {"qubit": "q[0]", "classical_bit": "c[0]", "string_position": "rightmost"},
        {"qubit": "q[1]", "classical_bit": "c[1]", "string_position": "leftmost"},
    ],
    "example_counts": {"10": 7, "01": 5},
    "interpretation": {
        "bitstring_10": {"q[1]": 1, "q[0]": 0},
        "bitstring_01": {"q[1]": 0, "q[0]": 1},
    },
}
register_layout["layout_hash"] = sha256_obj(register_layout)

post_processing_receipt = {
    "schema": "QuantumPostProcessingReceipt/v1",
    "receipt_id": "no-post-processing-baseline",
    "raw_result_hash_required": True,
    "normalized_result_hash_required": True,
    "operations": [],
    "mitigation_applied": False,
    "filtering_applied": False,
    "truncation_applied": False,
    "claim_rule": "A result packet that changes counts, bit order, mitigation, filtering, or truncation must add a post-processing receipt.",
}
post_processing_receipt["receipt_hash"] = sha256_obj(post_processing_receipt)


parser_profiles = [
    {
        "profile_id": "parser-braket-get-device",
        "provider": "Amazon Braket",
        "schema": "CloudQuantumProviderMetadataParserProfile/v1",
        "input_api": "GetDevice",
        "source_anchors": [
            "https://docs.aws.amazon.com/braket/latest/APIReference/API_GetDevice.html",
            "https://docs.aws.amazon.com/braket/latest/developerguide/braket-devices.html",
        ],
        "sample_payload": braket_sample,
        "normalized_output": {
            "provider": "Amazon Braket",
            "target_id": braket_sample["deviceArn"],
            "target_kind": "QPU",
            "availability": "ONLINE",
            "qubit_count": 2,
            "native_or_supported_operations": ["x", "cnot"],
            "hardware_claim_allowed": True,
        },
        "required_raw_fields": ["deviceArn", "deviceType", "deviceStatus", "deviceCapabilities", "payload_hash"],
        "hardware_rejection_rules": [
            "Reject when deviceType is SIMULATOR.",
            "Reject when deviceArn does not identify a QPU path.",
            "Reject when deviceCapabilities are unavailable.",
        ],
    },
    {
        "profile_id": "parser-ibm-backend-properties",
        "provider": "IBM Quantum Runtime",
        "schema": "CloudQuantumProviderMetadataParserProfile/v1",
        "input_api": "BackendProperties",
        "source_anchors": [
            "https://quantum.cloud.ibm.com/docs/api/qiskit-ibm-runtime/models-backend-properties",
            "https://quantum.cloud.ibm.com/docs/guides/get-qpu-information",
        ],
        "sample_payload": ibm_sample,
        "normalized_output": {
            "provider": "IBM Quantum Runtime",
            "target_id": "example_backend",
            "backend_version": "1.2.3",
            "last_update_date": "2026-07-01T00:00:00Z",
            "qubit_count": 2,
            "gate_count": 1,
            "hardware_claim_allowed": True,
        },
        "required_raw_fields": ["backend_name", "backend_version", "last_update_date", "qubits", "gates", "payload_hash"],
        "hardware_rejection_rules": [
            "Reject when last_update_date is absent.",
            "Reject when qubits or gates are absent for calibration-dependent claims.",
            "Reject when backend simulator status is true or unavailable in the paired backend metadata.",
        ],
    },
    {
        "profile_id": "parser-azure-target-list",
        "provider": "Azure Quantum",
        "schema": "CloudQuantumProviderMetadataParserProfile/v1",
        "input_api": "az quantum target list/show",
        "source_anchors": [
            "https://learn.microsoft.com/en-us/cli/azure/quantum/target?view=azure-cli-latest",
            "https://learn.microsoft.com/en-us/cli/azure/quantum/job?view=azure-cli-latest",
        ],
        "sample_payload": azure_sample,
        "normalized_output": {
            "provider": "Azure Quantum",
            "target_id": "example.qpu",
            "provider_id": "example-provider",
            "target_kind": "hardware",
            "availability": "Available",
            "input_data_format": "qir.v1",
            "output_data_format": "microsoft.quantum-results.v1",
            "hardware_claim_allowed": True,
        },
        "required_raw_fields": ["workspace_ref", "provider_id", "target_id", "target_profile", "payload_hash"],
        "hardware_rejection_rules": [
            "Reject when target_profile is simulator.",
            "Reject when provider_id or target_id is absent.",
            "Reject when output format or target kind cannot be verified for an execution claim.",
        ],
    },
]


negative_fixtures = [
    {
        "fixture_id": "negative-provider-metadata-without-payload-hash",
        "expected_validator_status": "REJECT",
        "failure_mode": "Provider metadata parser input omits payload_hash.",
    },
    {
        "fixture_id": "negative-azure-unknown-target-kind-promoted-to-hardware",
        "expected_validator_status": "REJECT",
        "failure_mode": "Azure target profile is unknown but claim branch is CLOUD_HARDWARE.",
    },
    {
        "fixture_id": "negative-register-layout-omitted",
        "expected_validator_status": "REJECT",
        "failure_mode": "Counts bitstrings are normalized without QuantumRegisterLayoutReceipt/v1.",
    },
    {
        "fixture_id": "negative-endian-convention-absent",
        "expected_validator_status": "REJECT",
        "failure_mode": "Bitstring interpretation is claimed without explicit endian/string-position convention.",
    },
    {
        "fixture_id": "negative-duplicate-json-key-payload",
        "expected_validator_status": "REJECT",
        "failure_mode": "Raw JSON payload contains duplicate keys and cannot be treated as lossless canonical JSON.",
        "raw_payload": "{\"counts\":{\"00\":1,\"00\":2}}",
    },
    {
        "fixture_id": "negative-binary-payload-treated-as-json",
        "expected_validator_status": "REJECT",
        "failure_mode": "Binary or compressed provider payload is parsed through the JSON canonicalization path.",
    },
    {
        "fixture_id": "negative-float-precision-policy-absent",
        "expected_validator_status": "REJECT",
        "failure_mode": "Floating-point result fields are normalized without a precision and rounding policy.",
    },
    {
        "fixture_id": "negative-post-processing-without-receipt",
        "expected_validator_status": "REJECT",
        "failure_mode": "Counts were filtered, truncated, mitigated, or reordered without QuantumPostProcessingReceipt/v1.",
    },
]


record = {
    "schema": "CloudQuantumProviderMetadataParserSet/v1",
    "pass": "0017",
    "generated_on": "2026-07-01",
    "status": "PARSER_PROFILE_MATCH",
    "parser_profiles": parser_profiles,
    "register_layout_receipt": register_layout,
    "post_processing_receipt": post_processing_receipt,
    "negative_fixtures": negative_fixtures,
    "source_anchors": [
        {
            "source": "Amazon Braket GetDevice API",
            "url": "https://docs.aws.amazon.com/braket/latest/APIReference/API_GetDevice.html",
        },
        {
            "source": "Amazon Braket device properties",
            "url": "https://docs.aws.amazon.com/braket/latest/developerguide/braket-devices.html",
        },
        {
            "source": "IBM BackendProperties API",
            "url": "https://quantum.cloud.ibm.com/docs/api/qiskit-ibm-runtime/models-backend-properties",
        },
        {
            "source": "IBM Quantum backend information",
            "url": "https://quantum.cloud.ibm.com/docs/guides/get-qpu-information",
        },
        {
            "source": "Azure Quantum target CLI",
            "url": "https://learn.microsoft.com/en-us/cli/azure/quantum/target?view=azure-cli-latest",
        },
        {
            "source": "Azure Quantum job CLI",
            "url": "https://learn.microsoft.com/en-us/cli/azure/quantum/job?view=azure-cli-latest",
        },
        {
            "source": "IBM Quantum bit-ordering guide",
            "url": "https://quantum.cloud.ibm.com/docs/guides/bit-ordering",
        },
    ],
    "non_promotion_statement": "Pass 0017 defines provider metadata parser and register-layout fixtures only. It does not fetch live provider metadata, run a quantum job, or promote a quantum hardware result.",
}

record["seal"] = sha256_obj(record)
print(json.dumps(record, indent=2, sort_keys=True))
