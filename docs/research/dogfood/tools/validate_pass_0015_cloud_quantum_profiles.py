import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_json(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def require(condition, message, errors):
    if not condition:
        errors.append(message)


def validate_profiles():
    path = Path("schemas/cloud-quantum-task-receipt-profiles-pass-0015.json")
    packet = load_json(path)
    errors = []
    require(packet.get("schema") == "CloudQuantumTaskReceiptProfileSet/v1", "schema mismatch", errors)
    require(packet.get("pass") == "0015", "pass mismatch", errors)
    require(packet.get("status") == "PROFILE_SET_MATCH", "status mismatch", errors)
    require(bool(packet.get("seal")), "missing seal", errors)
    require("shape-only" in packet.get("non_promotion_statement", ""), "missing shape-only non-promotion statement", errors)

    profiles = packet.get("profiles", [])
    require(len(profiles) >= 4, "expected at least four profiles", errors)
    by_id = {profile.get("profile_id"): profile for profile in profiles}
    for profile_id in [
        "cloud-quantum-profile-braket-task",
        "cloud-quantum-profile-ibm-runtime-job",
        "cloud-quantum-profile-azure-job",
        "cloud-quantum-profile-provider-simulator",
    ]:
        require(profile_id in by_id, f"missing profile {profile_id}", errors)

    for profile in profiles:
        require(profile.get("schema") == "CloudQuantumTaskReceiptProfile/v1", f"profile schema mismatch: {profile.get('profile_id')}", errors)
        require(profile.get("source_anchors"), f"profile missing source anchors: {profile.get('profile_id')}", errors)
        for url in profile.get("source_anchors", []):
            require(url.startswith("https://"), f"non-https source anchor: {url}", errors)
        fields = profile.get("profile_required_fields", {})
        for section in ["identity", "execution", "result", "provenance"]:
            require(section in fields and fields[section], f"profile missing {section}: {profile.get('profile_id')}", errors)
        require(profile.get("non_promotion_rules"), f"profile missing non-promotion rules: {profile.get('profile_id')}", errors)

    braket = by_id.get("cloud-quantum-profile-braket-task", {})
    braket_requirements = set(braket.get("hardware_claim_allowed_requirements", []))
    for field in ["device_arn", "task_id", "shots", "status", "result_payload_hash", "calibration_or_device_properties_reference"]:
        require(field in braket_requirements, f"Braket missing hardware requirement: {field}", errors)

    ibm = by_id.get("cloud-quantum-profile-ibm-runtime-job", {})
    ibm_requirements = set(ibm.get("hardware_claim_allowed_requirements", []))
    for field in ["backend_name", "job_id", "primitive_name", "result_payload_hash", "session_or_job_mode", "calibration_or_backend_properties_reference"]:
        require(field in ibm_requirements, f"IBM missing hardware requirement: {field}", errors)

    azure = by_id.get("cloud-quantum-profile-azure-job", {})
    azure_requirements = set(azure.get("hardware_claim_allowed_requirements", []))
    for field in ["workspace_ref", "provider_id", "target_id", "job_id", "job_input_hash", "result_payload_hash", "calibration_or_target_properties_reference"]:
        require(field in azure_requirements, f"Azure missing hardware requirement: {field}", errors)
    azure_rules = " ".join(azure.get("non_promotion_rules", []))
    require("Resource-estimator output must remain separate" in azure_rules, "Azure resource-estimator separation rule missing", errors)

    simulator = by_id.get("cloud-quantum-profile-provider-simulator", {})
    require(simulator.get("branch") == "CLOUD_SIMULATOR", "provider simulator branch mismatch", errors)
    require(simulator.get("hardware_claim_allowed_requirements") == [], "provider simulator must not allow hardware requirements", errors)

    negatives = packet.get("negative_fixtures", [])
    require(len(negatives) >= 4, "expected at least four negative fixtures", errors)
    for negative in negatives:
        require(negative.get("expected_validator_status") == "REJECT", f"negative fixture must reject: {negative.get('fixture_id')}", errors)
    negative_ids = {negative.get("fixture_id") for negative in negatives}
    for fixture_id in [
        "negative-braket-missing-result-payload-hash",
        "negative-ibm-missing-calibration-reference",
        "negative-azure-resource-estimator-promoted-to-execution",
        "negative-hardware-mock-promoted-to-cloud-hardware",
    ]:
        require(fixture_id in negative_ids, f"missing negative fixture: {fixture_id}", errors)

    samples = packet.get("sample_receipts", [])
    require(len(samples) >= 3, "expected at least three sample receipts", errors)
    for sample in samples:
        require(sample.get("hardware_claim_allowed") is False, f"sample must not allow hardware claim: {sample.get('receipt_id')}", errors)
        require(sample.get("sample_status") == "SHAPE_ONLY_NOT_EXECUTED", f"sample must be shape-only: {sample.get('receipt_id')}", errors)
        require(sample.get("profile_ref") in by_id, f"sample references missing profile: {sample.get('receipt_id')}", errors)
        result = sample.get("result", {})
        require(any(key in result for key in ["result_reference", "output_reference_or_storage_ref"]), f"sample missing result reference: {sample.get('receipt_id')}", errors)
        require(bool(result.get("result_payload_hash")), f"sample missing payload hash: {sample.get('receipt_id')}", errors)

    return {
        "artifact": "CloudQuantumTaskReceiptProfileSet",
        "path": str(path),
        "status": "MATCH" if not errors else "DRIFT",
        "errors": errors,
        "profile_count": len(profiles),
        "negative_fixture_count": len(negatives),
        "sample_receipt_count": len(samples),
    }


def main():
    checks = [validate_profiles()]
    drift = sum(1 for check in checks if check["status"] != "MATCH")
    result = {
        "schema": "Pass0015CloudQuantumProfileValidatorRun/v1",
        "pass": "0015",
        "status": "MATCH" if drift == 0 else "DRIFT",
        "match": len(checks) - drift,
        "drift": drift,
        "checks": checks,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if drift == 0 else 1)


if __name__ == "__main__":
    main()
