import hashlib
import json


def sha256_text(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def canonical_json(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_canonical(value):
    return sha256_text(canonical_json(value))


def main():
    raw_payload_a = '{"status":"COMPLETED","shots":1000,"counts":{"00":500,"11":500}}'
    raw_payload_b = '{ "counts": { "11": 500, "00": 500 }, "shots": 1000, "status": "COMPLETED" }'
    parsed_a = json.loads(raw_payload_a)
    parsed_b = json.loads(raw_payload_b)
    normalized = {
        "counts": {
            "00": 500,
            "11": 500
        },
        "shots": 1000,
        "status": "COMPLETED"
    }
    fixture = {
        "schema": "CloudQuantumCanonicalizationSet/v1",
        "pass": "0016",
        "generated_on": "2026-07-01",
        "status": "CANONICALIZATION_MATCH",
        "canonicalization_policy": {
            "schema": "CloudQuantumResultCanonicalization/v1",
            "raw_payload_hash_required": True,
            "normalized_result_hash_required": True,
            "canonicalization_reference": "RFC 8785 JSON Canonicalization Scheme, with this fixture using a strict sorted-key JSON subset for reproducible local testing.",
            "normalization_steps": [
                {
                    "step": "preserve_raw_provider_payload",
                    "lossiness": "LOSSLESS",
                    "output": "raw_payload_hash"
                },
                {
                    "step": "parse_json_payload",
                    "lossiness": "LOSSLESS_IF_PROVIDER_JSON_VALID_AND_DUPLICATE_KEYS_ABSENT",
                    "output": "parsed_payload"
                },
                {
                    "step": "sort_object_keys_and_strip_insignificant_whitespace",
                    "lossiness": "LOSSLESS_FOR_JSON_SEMANTICS_BUT_BYTE_LAYOUT_LOSSY",
                    "output": "canonical_json"
                },
                {
                    "step": "normalize_provider_counts_to_common_counts_map",
                    "lossiness": "PROVIDER_METADATA_LOSSY_UNLESS_RAW_PAYLOAD_RETAINED",
                    "output": "normalized_result"
                }
            ],
            "required_hashes": [
                "raw_payload_hash",
                "normalized_result_hash",
                "canonicalization_policy_hash"
            ]
        },
        "raw_payload_order_fixture": {
            "fixture_id": "raw-order-normalized-equality",
            "raw_payload_a": raw_payload_a,
            "raw_payload_b": raw_payload_b,
            "raw_payload_a_hash": sha256_text(raw_payload_a),
            "raw_payload_b_hash": sha256_text(raw_payload_b),
            "parsed_payloads_equal": parsed_a == parsed_b,
            "normalized_result": normalized,
            "normalized_result_canonical_json": canonical_json(normalized),
            "normalized_result_hash_a": sha256_canonical(parsed_a),
            "normalized_result_hash_b": sha256_canonical(parsed_b),
            "expected_status": "RAW_HASH_DRIFT_NORMALIZED_HASH_MATCH"
        },
        "calibration_reference_profiles": [
            {
                "profile_id": "calibration-ref-braket-device-properties",
                "provider": "Amazon Braket",
                "schema": "CloudQuantumCalibrationReferenceProfile/v1",
                "required_fields": [
                    "device_arn",
                    "retrieval_timestamp",
                    "device_properties_reference",
                    "device_properties_payload_hash",
                    "calibration_data_reference_or_unavailable_reason",
                    "native_gate_set_reference"
                ],
                "unavailable_policy": "If provider calibration data is unavailable, record unavailable reason and mark hardware-calibration-dependent claims UNVERIFIABLE.",
                "source_anchors": [
                    "https://docs.aws.amazon.com/braket/latest/developerguide/braket-devices.html",
                    "https://docs.aws.amazon.com/braket/latest/developerguide/braket-result-types.html"
                ]
            },
            {
                "profile_id": "calibration-ref-ibm-backend-properties",
                "provider": "IBM Quantum Runtime",
                "schema": "CloudQuantumCalibrationReferenceProfile/v1",
                "required_fields": [
                    "backend_name",
                    "retrieval_timestamp",
                    "backend_properties_reference",
                    "backend_properties_payload_hash",
                    "last_update_date",
                    "qubit_properties_reference",
                    "gate_properties_reference"
                ],
                "unavailable_policy": "If backend properties are unavailable, mark calibration-dependent claims UNVERIFIABLE.",
                "source_anchors": [
                    "https://quantum.cloud.ibm.com/docs/en/guides/qpu-information",
                    "https://quantum.cloud.ibm.com/docs/en/api/qiskit-ibm-runtime/models-backend-properties"
                ]
            },
            {
                "profile_id": "calibration-ref-azure-target-properties",
                "provider": "Azure Quantum",
                "schema": "CloudQuantumCalibrationReferenceProfile/v1",
                "required_fields": [
                    "workspace_ref",
                    "provider_id",
                    "target_id",
                    "retrieval_timestamp",
                    "target_properties_reference",
                    "target_properties_payload_hash",
                    "capability_profile_reference"
                ],
                "unavailable_policy": "If target properties or calibration data are not exposed, record target metadata and mark calibration-dependent claims UNVERIFIABLE.",
                "source_anchors": [
                    "https://learn.microsoft.com/en-us/azure/quantum/how-to-submit-jobs",
                    "https://learn.microsoft.com/en-us/cli/azure/quantum/job?view=azure-cli-latest"
                ]
            }
        ],
        "backend_kind_mapping": [
            {
                "provider": "Amazon Braket",
                "qpu_indicators": [
                    "device_kind=QPU",
                    "device_arn contains /device/qpu/"
                ],
                "simulator_indicators": [
                    "device_kind=SIMULATOR",
                    "device_arn contains /device/quantum-simulator/"
                ],
                "hardware_claim_rule": "Reject hardware claims when simulator indicators match or QPU indicators are absent."
            },
            {
                "provider": "IBM Quantum Runtime",
                "qpu_indicators": [
                    "backend.simulator is false",
                    "backend configuration identifies a real backend"
                ],
                "simulator_indicators": [
                    "backend.simulator is true",
                    "backend name or configuration identifies simulator"
                ],
                "hardware_claim_rule": "Reject hardware claims when backend simulator status is true or unavailable."
            },
            {
                "provider": "Azure Quantum",
                "qpu_indicators": [
                    "target_id belongs to hardware target profile",
                    "provider target metadata identifies QPU"
                ],
                "simulator_indicators": [
                    "target_id belongs to simulator target profile",
                    "target metadata identifies simulator"
                ],
                "hardware_claim_rule": "Reject hardware claims when target profile is simulator or target kind cannot be verified."
            }
        ],
        "resource_estimator_profile": {
            "profile_id": "cloud-quantum-resource-estimate-profile-azure",
            "schema": "CloudQuantumResourceEstimateReceiptProfile/v1",
            "provider": "Azure Quantum",
            "execution_claim_allowed": False,
            "hardware_claim_allowed": False,
            "required_fields": [
                "application_model_hash",
                "architecture_model_hash",
                "error_correction_model_hash",
                "max_error",
                "resource_estimator_version_or_tool_ref",
                "estimate_payload_hash",
                "normalized_estimate_hash",
                "physical_qubits",
                "runtime",
                "overall_error_or_error_budget",
                "pareto_point_count_or_selection_rule"
            ],
            "non_promotion_rules": [
                "Resource estimates are planning artifacts, not execution results.",
                "Resource estimates cannot satisfy cloud hardware task receipt requirements.",
                "Claims using resource estimates must state model assumptions and uncertainty."
            ],
            "source_anchors": [
                "https://learn.microsoft.com/en-us/azure/quantum/intro-to-resource-estimation",
                "https://learn.microsoft.com/en-us/azure/quantum/qre-estimation-results"
            ]
        },
        "negative_fixtures": [
            {
                "fixture_id": "negative-raw-only-hash-for-normalized-claim",
                "failure_mode": "A normalized result claim cites only raw_payload_hash and omits normalized_result_hash.",
                "expected_validator_status": "REJECT"
            },
            {
                "fixture_id": "negative-normalized-only-hash-for-forensic-claim",
                "failure_mode": "A forensic provenance claim cites only normalized_result_hash and omits raw_payload_hash.",
                "expected_validator_status": "REJECT"
            },
            {
                "fixture_id": "negative-nondeterministic-payload-order-without-canonicalization",
                "failure_mode": "Two semantically equal JSON payloads have different raw hashes and no canonicalization policy hash.",
                "expected_validator_status": "REJECT"
            },
            {
                "fixture_id": "negative-simulator-backend-cited-as-qpu",
                "failure_mode": "Backend kind maps to simulator but claim branch is CLOUD_HARDWARE QPU.",
                "expected_validator_status": "REJECT"
            },
            {
                "fixture_id": "negative-resource-estimator-cited-as-execution",
                "failure_mode": "Azure resource estimate receipt is cited as executed hardware result.",
                "expected_validator_status": "REJECT"
            }
        ],
        "source_anchors": [
            {
                "source": "RFC 8785 JSON Canonicalization Scheme",
                "url": "https://www.rfc-editor.org/info/rfc8785/"
            },
            {
                "source": "Amazon Braket device properties",
                "url": "https://docs.aws.amazon.com/braket/latest/developerguide/braket-devices.html"
            },
            {
                "source": "Amazon Braket result types",
                "url": "https://docs.aws.amazon.com/braket/latest/developerguide/braket-result-types.html"
            },
            {
                "source": "IBM Quantum QPU information",
                "url": "https://quantum.cloud.ibm.com/docs/en/guides/qpu-information"
            },
            {
                "source": "IBM BackendProperties API",
                "url": "https://quantum.cloud.ibm.com/docs/en/api/qiskit-ibm-runtime/models-backend-properties"
            },
            {
                "source": "Azure Quantum Resource Estimator",
                "url": "https://learn.microsoft.com/en-us/azure/quantum/intro-to-resource-estimation"
            },
            {
                "source": "Azure Quantum resource-estimator results",
                "url": "https://learn.microsoft.com/en-us/azure/quantum/qre-estimation-results"
            }
        ],
        "non_promotion_statement": "Pass 0016 defines canonicalization and calibration receipt profiles only. It does not run a cloud job, report a quantum hardware result, or promote a resource estimate to execution evidence."
    }
    fixture["canonicalization_policy"]["canonicalization_policy_hash"] = sha256_canonical(fixture["canonicalization_policy"])
    fixture["seal"] = sha256_canonical(fixture)
    print(json.dumps(fixture, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
