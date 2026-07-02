import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_json(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def require(condition, message, errors):
    if not condition:
        errors.append(message)


def validate_fixture():
    path = Path("schemas/quantum-receipt-hardening-fixtures-pass-0014.json")
    fixture = load_json(path)
    errors = []
    require(fixture.get("schema") == "QuantumReceiptHardeningFixture/v1", "schema mismatch", errors)
    require(fixture.get("pass") == "0014", "pass mismatch", errors)
    require(fixture.get("status") == "HARDENING_FIXTURE_MATCH", "status mismatch", errors)
    require(bool(fixture.get("seal")), "missing seal", errors)

    negative = fixture.get("negative_promotion_fixture", {})
    require(negative.get("source_branch") == "EXACT_SIMULATOR", "negative source branch mismatch", errors)
    require(negative.get("attempted_target_branch") == "CLOUD_HARDWARE", "negative target branch mismatch", errors)
    require(negative.get("expected_validator_status") == "REJECT", "negative fixture must reject", errors)
    reasons = set(negative.get("rejection_reasons", []))
    for reason in [
        "branch_mismatch",
        "hardware_claim_allowed_false",
        "missing_cloud_task_metadata",
        "missing_calibration_reference",
        "missing_result_payload_hash",
    ]:
        require(reason in reasons, f"missing rejection reason: {reason}", errors)

    mock = fixture.get("hardware_mock_receipt", {})
    require(mock.get("schema") == "QuantumExperimentReceipt/v1", "mock receipt schema mismatch", errors)
    require(mock.get("branch") == "HARDWARE_MOCK", "mock receipt branch mismatch", errors)
    require(mock.get("hardware_claim_allowed") is False, "mock receipt must not allow hardware claims", errors)
    require(mock.get("verdict") == "MOCK_MATCH_NOT_HARDWARE", "mock verdict mismatch", errors)
    backend = mock.get("backend", {})
    for field in ["provider", "device_arn", "task_id", "shots", "queue_timestamp", "calibration_ref", "result_payload_hash"]:
        require(field in backend, f"mock backend missing {field}", errors)

    adapters = fixture.get("adapter_fixtures", [])
    require(len(adapters) >= 2, "expected at least two adapter fixtures", errors)
    adapter_names = {adapter.get("adapter") for adapter in adapters}
    require("qiskit-openqasm3-export-fixture" in adapter_names, "missing qiskit adapter fixture", errors)
    require("cirq-json-shape-fixture" in adapter_names, "missing cirq adapter fixture", errors)
    for adapter in adapters:
        require(adapter.get("adapter_status") == "ADAPTER_FIXTURE_MATCH", f"adapter not matched: {adapter.get('adapter')}", errors)
        require(adapter.get("source_anchor", "").startswith("https://"), f"adapter source is not https: {adapter.get('adapter')}", errors)
        circuit = adapter.get("normalized_circuit", {})
        require(circuit.get("qubits") == 2, f"adapter qubit count mismatch: {adapter.get('adapter')}", errors)
        require(circuit.get("gate_count") == 2, f"adapter gate count mismatch: {adapter.get('adapter')}", errors)

    qiskit = next((adapter for adapter in adapters if adapter.get("adapter") == "qiskit-openqasm3-export-fixture"), {})
    require("OPENQASM 3.0" in qiskit.get("program", ""), "qiskit fixture missing OPENQASM 3.0", errors)

    estimate = fixture.get("resource_estimate_receipt", {})
    require(estimate.get("schema") == "QuantumResourceEstimateReceipt/v1", "resource estimate schema mismatch", errors)
    require(estimate.get("status") == "ESTIMATE_ONLY_NOT_EXECUTION", "resource estimate status mismatch", errors)
    require(estimate.get("execution_claim_allowed") is False, "resource estimate must not allow execution claim", errors)
    require(estimate.get("source_anchor", "").startswith("https://"), "resource estimate source must be https", errors)

    bindings = {binding.get("claim_id"): binding for binding in fixture.get("metric_claim_bindings", [])}
    phase = bindings.get("phase_sensitive_clone_claim", {})
    require("measurement_histogram_only" in phase.get("insufficient_metrics", []), "phase claim must reject histogram-only metric", errors)
    hardware = bindings.get("cloud_hardware_result_claim", {})
    for metric in ["provider_device_identity", "cloud_task_id", "shots", "calibration_reference", "result_payload_hash"]:
        require(metric in hardware.get("sufficient_metrics", []), f"hardware claim missing sufficient metric: {metric}", errors)

    anchors = fixture.get("source_anchors", [])
    require(len(anchors) >= 6, "expected at least six source anchors", errors)
    for anchor in anchors:
        require(anchor.get("url", "").startswith("https://"), f"source anchor is not https: {anchor}", errors)

    return {
        "artifact": "QuantumReceiptHardeningFixture",
        "path": str(path),
        "status": "MATCH" if not errors else "DRIFT",
        "errors": errors,
        "adapter_count": len(adapters),
        "source_anchor_count": len(anchors),
    }


def main():
    checks = [validate_fixture()]
    drift = sum(1 for check in checks if check["status"] != "MATCH")
    result = {
        "schema": "Pass0014QuantumHardeningValidatorRun/v1",
        "pass": "0014",
        "status": "MATCH" if drift == 0 else "DRIFT",
        "match": len(checks) - drift,
        "drift": drift,
        "checks": checks,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if drift == 0 else 1)


if __name__ == "__main__":
    main()
