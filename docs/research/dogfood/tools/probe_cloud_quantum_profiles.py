import hashlib
import json


def canonical_sha256(value):
    body = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(body).hexdigest()


def main():
    profiles = {
        "schema": "CloudQuantumTaskReceiptProfileSet/v1",
        "pass": "0015",
        "generated_on": "2026-07-01",
        "status": "PROFILE_SET_MATCH",
        "profiles": [
            {
                "profile_id": "cloud-quantum-profile-braket-task",
                "provider": "Amazon Braket",
                "schema": "CloudQuantumTaskReceiptProfile/v1",
                "branch": "CLOUD_HARDWARE",
                "hardware_claim_allowed_requirements": [
                    "device_arn",
                    "task_id",
                    "device_kind_qpu_or_simulator_declared",
                    "shots",
                    "status",
                    "submit_timestamp_or_provider_date",
                    "result_s3_reference_or_result_reference",
                    "result_payload_hash",
                    "calibration_or_device_properties_reference",
                    "source_program_hash"
                ],
                "profile_required_fields": {
                    "identity": [
                        "provider",
                        "region",
                        "account_or_tenant_ref",
                        "device_arn",
                        "task_id"
                    ],
                    "execution": [
                        "device_kind",
                        "shots",
                        "status",
                        "queue_or_submit_timestamp",
                        "completion_timestamp_or_provider_date"
                    ],
                    "result": [
                        "result_reference",
                        "result_payload_hash",
                        "result_format"
                    ],
                    "provenance": [
                        "source_program_hash",
                        "sdk_name",
                        "sdk_version",
                        "calibration_or_device_properties_reference"
                    ]
                },
                "source_anchors": [
                    "https://docs.aws.amazon.com/braket/latest/developerguide/braket-monitor-tasks-sdk.html",
                    "https://docs.aws.amazon.com/braket/latest/developerguide/braket-how-it-works.html",
                    "https://docs.aws.amazon.com/braket/latest/developerguide/braket-submit-tasks-to-braket.html"
                ],
                "non_promotion_rules": [
                    "An Amazon Braket simulator task must declare simulator identity and cannot be cited as QPU hardware.",
                    "A Braket-shaped mock receipt cannot be promoted to CLOUD_HARDWARE.",
                    "A hardware claim is invalid without task id, device ARN, result reference, payload hash, and calibration/device-property reference."
                ]
            },
            {
                "profile_id": "cloud-quantum-profile-ibm-runtime-job",
                "provider": "IBM Quantum Runtime",
                "schema": "CloudQuantumTaskReceiptProfile/v1",
                "branch": "CLOUD_HARDWARE",
                "hardware_claim_allowed_requirements": [
                    "backend_name",
                    "job_id",
                    "primitive_name",
                    "pub_or_circuit_reference",
                    "shots_or_precision",
                    "status",
                    "result_reference",
                    "result_payload_hash",
                    "source_program_hash",
                    "session_or_job_mode",
                    "calibration_or_backend_properties_reference"
                ],
                "profile_required_fields": {
                    "identity": [
                        "provider",
                        "instance_ref",
                        "backend_name",
                        "job_id"
                    ],
                    "execution": [
                        "primitive_name",
                        "session_or_job_mode",
                        "shots_or_precision",
                        "status",
                        "created_or_retrieved_timestamp"
                    ],
                    "result": [
                        "result_reference",
                        "result_payload_hash",
                        "result_format"
                    ],
                    "provenance": [
                        "source_program_hash",
                        "sdk_name",
                        "sdk_version",
                        "pub_or_circuit_reference",
                        "calibration_or_backend_properties_reference"
                    ]
                },
                "source_anchors": [
                    "https://quantum.cloud.ibm.com/docs/en/api/qiskit-runtime-rest/tags/jobs",
                    "https://quantum.cloud.ibm.com/docs/en/guides/save-jobs",
                    "https://quantum.cloud.ibm.com/docs/en/guides/primitive-input-output",
                    "https://quantum.cloud.ibm.com/docs/en/guides/run-jobs-session"
                ],
                "non_promotion_rules": [
                    "A Runtime job receipt must bind job id, primitive, backend, result reference, and payload hash.",
                    "A session receipt cannot substitute for a job result receipt.",
                    "A simulator backend must declare simulator identity and cannot be cited as QPU hardware."
                ]
            },
            {
                "profile_id": "cloud-quantum-profile-azure-job",
                "provider": "Azure Quantum",
                "schema": "CloudQuantumTaskReceiptProfile/v1",
                "branch": "CLOUD_HARDWARE",
                "hardware_claim_allowed_requirements": [
                    "workspace_ref",
                    "provider_id",
                    "target_id",
                    "job_id",
                    "job_input_hash",
                    "job_input_format",
                    "job_output_format",
                    "shots_or_target_params",
                    "status",
                    "output_reference_or_storage_ref",
                    "result_payload_hash",
                    "calibration_or_target_properties_reference"
                ],
                "profile_required_fields": {
                    "identity": [
                        "provider",
                        "workspace_ref",
                        "provider_id",
                        "target_id",
                        "job_id"
                    ],
                    "execution": [
                        "job_name",
                        "job_input_format",
                        "job_output_format",
                        "shots_or_target_params",
                        "status",
                        "submission_timestamp"
                    ],
                    "result": [
                        "output_reference_or_storage_ref",
                        "result_payload_hash",
                        "result_format"
                    ],
                    "provenance": [
                        "job_input_hash",
                        "sdk_or_cli_name",
                        "sdk_or_cli_version",
                        "calibration_or_target_properties_reference"
                    ]
                },
                "source_anchors": [
                    "https://learn.microsoft.com/en-us/azure/quantum/how-to-submit-jobs",
                    "https://learn.microsoft.com/en-us/cli/azure/quantum/job?view=azure-cli-latest",
                    "https://github.com/MicrosoftDocs/quantum-docs/blob/main/articles/how-to-work-with-jobs.md",
                    "https://learn.microsoft.com/en-us/azure/quantum/intro-to-resource-estimation"
                ],
                "non_promotion_rules": [
                    "Resource-estimator output must remain separate from job execution output.",
                    "A provider target simulator must declare simulator identity and cannot be cited as QPU hardware.",
                    "A hardware claim is invalid without job id, target id, output reference, payload hash, and calibration/target-property reference."
                ]
            },
            {
                "profile_id": "cloud-quantum-profile-provider-simulator",
                "provider": "Provider Simulator",
                "schema": "CloudQuantumTaskReceiptProfile/v1",
                "branch": "CLOUD_SIMULATOR",
                "hardware_claim_allowed_requirements": [],
                "profile_required_fields": {
                    "identity": [
                        "provider",
                        "simulator_name",
                        "task_or_job_id"
                    ],
                    "execution": [
                        "shots_or_analytic_mode",
                        "status",
                        "noise_model_or_exact_mode"
                    ],
                    "result": [
                        "result_reference",
                        "result_payload_hash",
                        "result_format"
                    ],
                    "provenance": [
                        "source_program_hash",
                        "sdk_name",
                        "sdk_version"
                    ]
                },
                "source_anchors": [
                    "https://docs.aws.amazon.com/braket/latest/developerguide/braket-how-it-works.html",
                    "https://quantum.cloud.ibm.com/docs/en/guides/primitive-input-output",
                    "https://learn.microsoft.com/en-us/azure/quantum/how-to-submit-jobs"
                ],
                "non_promotion_rules": [
                    "Cloud simulator results are not cloud QPU hardware results.",
                    "Simulator results can support bounded execution evidence only within simulator branch."
                ]
            }
        ],
        "negative_fixtures": [
            {
                "fixture_id": "negative-braket-missing-result-payload-hash",
                "profile_ref": "cloud-quantum-profile-braket-task",
                "branch": "CLOUD_HARDWARE",
                "missing_fields": [
                    "result_payload_hash"
                ],
                "expected_validator_status": "REJECT"
            },
            {
                "fixture_id": "negative-ibm-missing-calibration-reference",
                "profile_ref": "cloud-quantum-profile-ibm-runtime-job",
                "branch": "CLOUD_HARDWARE",
                "missing_fields": [
                    "calibration_or_backend_properties_reference"
                ],
                "expected_validator_status": "REJECT"
            },
            {
                "fixture_id": "negative-azure-resource-estimator-promoted-to-execution",
                "profile_ref": "cloud-quantum-profile-azure-job",
                "branch": "CLOUD_HARDWARE",
                "attempted_claim": "execution_result_from_resource_estimate",
                "missing_fields": [
                    "job_id",
                    "output_reference_or_storage_ref",
                    "result_payload_hash"
                ],
                "expected_validator_status": "REJECT"
            },
            {
                "fixture_id": "negative-hardware-mock-promoted-to-cloud-hardware",
                "profile_ref": "cloud-quantum-profile-braket-task",
                "source_branch": "HARDWARE_MOCK",
                "attempted_target_branch": "CLOUD_HARDWARE",
                "expected_validator_status": "REJECT"
            }
        ],
        "sample_receipts": [
            {
                "receipt_id": "sample-braket-cloud-hardware-shape-pass-0015",
                "profile_ref": "cloud-quantum-profile-braket-task",
                "branch": "CLOUD_HARDWARE",
                "hardware_claim_allowed": False,
                "sample_status": "SHAPE_ONLY_NOT_EXECUTED",
                "identity": {
                    "provider": "Amazon Braket",
                    "region": "us-west-2",
                    "account_or_tenant_ref": "redacted-account-ref",
                    "device_arn": "arn:aws:braket:us-west-2::device/qpu/example/ExampleQPU",
                    "task_id": "arn:aws:braket:us-west-2:123412341234:quantum-task/example"
                },
                "execution": {
                    "device_kind": "QPU",
                    "shots": 1000,
                    "status": "COMPLETED",
                    "queue_or_submit_timestamp": "2026-07-01T00:00:00Z",
                    "completion_timestamp_or_provider_date": "2026-07-01T00:05:00Z"
                },
                "result": {
                    "result_reference": "s3://redacted-bucket/example/result.json",
                    "result_payload_hash": "sha256:sample-braket-result-payload",
                    "result_format": "QuantumTaskResult"
                },
                "provenance": {
                    "source_program_hash": "sha256:sample-source-program",
                    "sdk_name": "amazon-braket-sdk",
                    "sdk_version": "profile-only",
                    "calibration_or_device_properties_reference": "device-properties-ref"
                }
            },
            {
                "receipt_id": "sample-ibm-runtime-job-shape-pass-0015",
                "profile_ref": "cloud-quantum-profile-ibm-runtime-job",
                "branch": "CLOUD_HARDWARE",
                "hardware_claim_allowed": False,
                "sample_status": "SHAPE_ONLY_NOT_EXECUTED",
                "identity": {
                    "provider": "IBM Quantum Runtime",
                    "instance_ref": "redacted-instance-ref",
                    "backend_name": "ibm_example_backend",
                    "job_id": "example-runtime-job-id"
                },
                "execution": {
                    "primitive_name": "sampler",
                    "session_or_job_mode": "job",
                    "shots_or_precision": 4096,
                    "status": "DONE",
                    "created_or_retrieved_timestamp": "2026-07-01T00:00:00Z"
                },
                "result": {
                    "result_reference": "ibm-runtime://jobs/example-runtime-job-id/result",
                    "result_payload_hash": "sha256:sample-ibm-result-payload",
                    "result_format": "PrimitiveResult"
                },
                "provenance": {
                    "source_program_hash": "sha256:sample-source-program",
                    "sdk_name": "qiskit-ibm-runtime",
                    "sdk_version": "profile-only",
                    "pub_or_circuit_reference": "pub-ref",
                    "calibration_or_backend_properties_reference": "backend-properties-ref"
                }
            },
            {
                "receipt_id": "sample-azure-quantum-job-shape-pass-0015",
                "profile_ref": "cloud-quantum-profile-azure-job",
                "branch": "CLOUD_HARDWARE",
                "hardware_claim_allowed": False,
                "sample_status": "SHAPE_ONLY_NOT_EXECUTED",
                "identity": {
                    "provider": "Azure Quantum",
                    "workspace_ref": "redacted-workspace-ref",
                    "provider_id": "example-provider",
                    "target_id": "example.qpu",
                    "job_id": "00000000-0000-0000-0000-000000000000"
                },
                "execution": {
                    "job_name": "sample-job",
                    "job_input_format": "qir.v1",
                    "job_output_format": "provider.quantum-results.v1",
                    "shots_or_target_params": {
                        "shots": 100
                    },
                    "status": "succeeded",
                    "submission_timestamp": "2026-07-01T00:00:00Z"
                },
                "result": {
                    "output_reference_or_storage_ref": "azure-storage://redacted-workspace/example-output",
                    "result_payload_hash": "sha256:sample-azure-result-payload",
                    "result_format": "provider.quantum-results.v1"
                },
                "provenance": {
                    "job_input_hash": "sha256:sample-job-input",
                    "sdk_or_cli_name": "az quantum",
                    "sdk_or_cli_version": "profile-only",
                    "calibration_or_target_properties_reference": "target-properties-ref"
                }
            }
        ],
        "non_promotion_statement": "All sample receipts are shape-only, not executed, and do not promote any quantum hardware result."
    }
    profiles["seal"] = canonical_sha256(profiles)
    print(json.dumps(profiles, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
