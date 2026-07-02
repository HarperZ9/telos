import hashlib
import json


def canonical_sha256(value):
    body = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(body).hexdigest()


def main():
    fixture = {
        "schema": "QuantumReceiptHardeningFixture/v1",
        "pass": "0014",
        "generated_on": "2026-07-01",
        "status": "HARDENING_FIXTURE_MATCH",
        "negative_promotion_fixture": {
            "fixture_id": "negative-exact-simulator-to-cloud-hardware",
            "source_receipt_ref": "quantum-exp-pass-0013-exact-simulator",
            "source_branch": "EXACT_SIMULATOR",
            "source_hardware_claim_allowed": False,
            "attempted_target_branch": "CLOUD_HARDWARE",
            "attempted_claim": "hardware_result",
            "expected_validator_status": "REJECT",
            "rejection_reasons": [
                "branch_mismatch",
                "hardware_claim_allowed_false",
                "missing_cloud_task_metadata",
                "missing_calibration_reference",
                "missing_result_payload_hash"
            ]
        },
        "hardware_mock_receipt": {
            "receipt_id": "quantum-exp-pass-0014-hardware-mock",
            "schema": "QuantumExperimentReceipt/v1",
            "branch": "HARDWARE_MOCK",
            "hardware_claim_allowed": False,
            "theorem_claim_ref": "claim-no-cloning-inner-product-identity",
            "circuit": {
                "source_format": "OpenQASM 3 fixture",
                "source_hash": "sha256:0b3e3ff6fc5a0feec84d1f473cda20341e335a8f8ff3f72f62fd73f06d31cc65",
                "qubits": 2,
                "operations": [
                    "h q[0]",
                    "cx q[0], q[1]"
                ],
                "gate_count": 2,
                "two_qubit_gate_count": 1,
                "depth": 2
            },
            "backend": {
                "provider": "amazon-braket-shape",
                "device_kind": "mock-qpu",
                "device_arn": "arn:aws:braket:us-east-1::device/qpu/mock/MockQPU",
                "task_id": "mock-task-pass-0014",
                "shots": 1000,
                "queue_timestamp": "2026-07-01T00:00:00Z",
                "calibration_ref": "mock-calibration-sha256:6d6f636b",
                "result_payload_hash": "sha256:mock-result-payload-pass-0014",
                "cloud_task_shape_only": True
            },
            "resource_estimate": {
                "logical_qubits": 2,
                "physical_qubits": "not_applicable_mock",
                "gate_count": 2,
                "depth": 2,
                "qec_scheme": "none",
                "runtime_estimate": "mock-not-executed"
            },
            "result": {
                "measurement_histogram": {
                    "00": 0.5,
                    "01": 0.0,
                    "10": 0.0,
                    "11": 0.5
                },
                "status": "MOCK_TASK_SHAPE_ONLY"
            },
            "verdict": "MOCK_MATCH_NOT_HARDWARE"
        },
        "adapter_fixtures": [
            {
                "adapter": "qiskit-openqasm3-export-fixture",
                "source_format": "OpenQASM 3",
                "source_anchor": "https://quantum.cloud.ibm.com/docs/api/qiskit/qasm3",
                "program": "OPENQASM 3.0;\ninclude \"stdgates.inc\";\nqubit[2] q;\nh q[0];\ncx q[0], q[1];",
                "normalized_circuit": {
                    "qubits": 2,
                    "operations": [
                        "h q[0]",
                        "cx q[0], q[1]"
                    ],
                    "gate_count": 2,
                    "two_qubit_gate_count": 1,
                    "depth": 2
                },
                "adapter_status": "ADAPTER_FIXTURE_MATCH"
            },
            {
                "adapter": "cirq-json-shape-fixture",
                "source_format": "Cirq JSON shape",
                "source_anchor": "https://quantumai.google/cirq/build/interop",
                "program": {
                    "cirq_type": "Circuit",
                    "moments": [
                        {
                            "operations": [
                                "H(q(0))"
                            ]
                        },
                        {
                            "operations": [
                                "CNOT(q(0), q(1))"
                            ]
                        }
                    ]
                },
                "normalized_circuit": {
                    "qubits": 2,
                    "operations": [
                        "H(q0)",
                        "CNOT(q0,q1)"
                    ],
                    "gate_count": 2,
                    "two_qubit_gate_count": 1,
                    "depth": 2
                },
                "adapter_status": "ADAPTER_FIXTURE_MATCH"
            }
        ],
        "resource_estimate_receipt": {
            "receipt_id": "quantum-resource-estimate-pass-0014",
            "schema": "QuantumResourceEstimateReceipt/v1",
            "status": "ESTIMATE_ONLY_NOT_EXECUTION",
            "execution_claim_allowed": False,
            "source_anchor": "https://learn.microsoft.com/en-us/azure/quantum/intro-to-resource-estimation",
            "circuit_ref": "qiskit-openqasm3-export-fixture",
            "logical_estimate": {
                "logical_qubits": 2,
                "logical_depth": 2,
                "logical_gate_count": 2
            },
            "physical_estimate": {
                "physical_qubits": "not_computed_for_toy_fixture",
                "runtime": "not_computed_for_toy_fixture",
                "qec_scheme": "none"
            },
            "assumptions": [
                "toy no-cloning witness",
                "not a fault-tolerant workload",
                "resource-estimate receipt is a planning artifact only"
            ]
        },
        "metric_claim_bindings": [
            {
                "claim_id": "basis_histogram_claim",
                "sufficient_metrics": [
                    "measurement_histogram"
                ],
                "insufficient_metrics": [
                    "statevector_absent_for_phase_claims"
                ],
                "status": "BOUND"
            },
            {
                "claim_id": "phase_sensitive_clone_claim",
                "sufficient_metrics": [
                    "statevector_or_density_matrix",
                    "fidelity_to_desired_clone"
                ],
                "insufficient_metrics": [
                    "measurement_histogram_only"
                ],
                "status": "BOUND"
            },
            {
                "claim_id": "cloud_hardware_result_claim",
                "sufficient_metrics": [
                    "provider_device_identity",
                    "cloud_task_id",
                    "shots",
                    "calibration_reference",
                    "result_payload_hash"
                ],
                "insufficient_metrics": [
                    "simulator_histogram",
                    "hardware_mock_task_shape"
                ],
                "status": "BOUND"
            }
        ],
        "source_anchors": [
            {
                "source": "IBM Qiskit qasm3 API",
                "url": "https://quantum.cloud.ibm.com/docs/api/qiskit/qasm3"
            },
            {
                "source": "IBM Qiskit OpenQASM 3 interop guide",
                "url": "https://quantum.cloud.ibm.com/docs/guides/interoperate-qiskit-qasm3"
            },
            {
                "source": "Cirq import/export interop guide",
                "url": "https://quantumai.google/cirq/build/interop"
            },
            {
                "source": "Amazon Braket task monitoring",
                "url": "https://docs.aws.amazon.com/braket/latest/developerguide/braket-monitor-tasks-sdk.html"
            },
            {
                "source": "Amazon Braket task submission",
                "url": "https://docs.aws.amazon.com/braket/latest/developerguide/braket-submit-tasks-to-braket.html"
            },
            {
                "source": "Azure Quantum Resource Estimator",
                "url": "https://learn.microsoft.com/en-us/azure/quantum/intro-to-resource-estimation"
            }
        ]
    }
    fixture["seal"] = canonical_sha256(fixture)
    print(json.dumps(fixture, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
