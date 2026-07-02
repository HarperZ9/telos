import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_json(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def require(condition, message, errors):
    if not condition:
        errors.append(message)


def validate_packet():
    path = Path("schemas/cloud-quantum-canonicalization-pass-0016.json")
    packet = load_json(path)
    errors = []

    require(packet.get("schema") == "CloudQuantumCanonicalizationSet/v1", "schema mismatch", errors)
    require(packet.get("pass") == "0016", "pass mismatch", errors)
    require(packet.get("status") == "CANONICALIZATION_MATCH", "status mismatch", errors)
    require(bool(packet.get("seal")), "missing seal", errors)
    require("does not run a cloud job" in packet.get("non_promotion_statement", ""), "missing non-promotion statement", errors)

    policy = packet.get("canonicalization_policy", {})
    require(policy.get("schema") == "CloudQuantumResultCanonicalization/v1", "canonicalization schema mismatch", errors)
    require(policy.get("raw_payload_hash_required") is True, "raw hash must be required", errors)
    require(policy.get("normalized_result_hash_required") is True, "normalized hash must be required", errors)
    require(bool(policy.get("canonicalization_policy_hash")), "missing canonicalization policy hash", errors)
    required_hashes = set(policy.get("required_hashes", []))
    for field in ["raw_payload_hash", "normalized_result_hash", "canonicalization_policy_hash"]:
        require(field in required_hashes, f"missing required hash: {field}", errors)

    fixture = packet.get("raw_payload_order_fixture", {})
    require(fixture.get("expected_status") == "RAW_HASH_DRIFT_NORMALIZED_HASH_MATCH", "raw-order fixture status mismatch", errors)
    require(fixture.get("raw_payload_a_hash") != fixture.get("raw_payload_b_hash"), "raw payload hashes should differ", errors)
    require(fixture.get("normalized_result_hash_a") == fixture.get("normalized_result_hash_b"), "normalized hashes should match", errors)
    require(fixture.get("parsed_payloads_equal") is True, "parsed payloads should be equal", errors)

    calibration_profiles = packet.get("calibration_reference_profiles", [])
    require(len(calibration_profiles) >= 3, "expected at least three calibration profiles", errors)
    calibration_ids = {profile.get("profile_id") for profile in calibration_profiles}
    for profile_id in [
        "calibration-ref-braket-device-properties",
        "calibration-ref-ibm-backend-properties",
        "calibration-ref-azure-target-properties",
    ]:
        require(profile_id in calibration_ids, f"missing calibration profile: {profile_id}", errors)
    for profile in calibration_profiles:
        require(profile.get("schema") == "CloudQuantumCalibrationReferenceProfile/v1", f"calibration profile schema mismatch: {profile.get('profile_id')}", errors)
        require("retrieval_timestamp" in profile.get("required_fields", []), f"calibration profile missing retrieval timestamp: {profile.get('profile_id')}", errors)
        require(profile.get("unavailable_policy", "").endswith("UNVERIFIABLE."), f"calibration unavailable policy must end UNVERIFIABLE: {profile.get('profile_id')}", errors)
        for url in profile.get("source_anchors", []):
            require(url.startswith("https://"), f"non-https calibration source: {url}", errors)

    backend_mapping = packet.get("backend_kind_mapping", [])
    require(len(backend_mapping) >= 3, "expected at least three backend-kind mappings", errors)
    for mapping in backend_mapping:
        require(mapping.get("qpu_indicators"), f"missing qpu indicators: {mapping.get('provider')}", errors)
        require(mapping.get("simulator_indicators"), f"missing simulator indicators: {mapping.get('provider')}", errors)
        require("Reject hardware claims" in mapping.get("hardware_claim_rule", ""), f"missing rejection rule: {mapping.get('provider')}", errors)

    resource = packet.get("resource_estimator_profile", {})
    require(resource.get("schema") == "CloudQuantumResourceEstimateReceiptProfile/v1", "resource estimator schema mismatch", errors)
    require(resource.get("execution_claim_allowed") is False, "resource estimator must not allow execution claim", errors)
    require(resource.get("hardware_claim_allowed") is False, "resource estimator must not allow hardware claim", errors)
    for field in ["physical_qubits", "runtime", "estimate_payload_hash", "normalized_estimate_hash"]:
        require(field in resource.get("required_fields", []), f"resource estimator missing field: {field}", errors)

    negatives = packet.get("negative_fixtures", [])
    require(len(negatives) >= 5, "expected at least five negative fixtures", errors)
    for negative in negatives:
        require(negative.get("expected_validator_status") == "REJECT", f"negative fixture must reject: {negative.get('fixture_id')}", errors)
    negative_ids = {negative.get("fixture_id") for negative in negatives}
    for fixture_id in [
        "negative-raw-only-hash-for-normalized-claim",
        "negative-normalized-only-hash-for-forensic-claim",
        "negative-nondeterministic-payload-order-without-canonicalization",
        "negative-simulator-backend-cited-as-qpu",
        "negative-resource-estimator-cited-as-execution",
    ]:
        require(fixture_id in negative_ids, f"missing negative fixture: {fixture_id}", errors)

    anchors = packet.get("source_anchors", [])
    require(len(anchors) >= 7, "expected at least seven source anchors", errors)
    for anchor in anchors:
        require(anchor.get("url", "").startswith("https://"), f"non-https source anchor: {anchor}", errors)

    return {
        "artifact": "CloudQuantumCanonicalizationSet",
        "path": str(path),
        "status": "MATCH" if not errors else "DRIFT",
        "errors": errors,
        "calibration_profile_count": len(calibration_profiles),
        "backend_mapping_count": len(backend_mapping),
        "negative_fixture_count": len(negatives),
        "source_anchor_count": len(anchors),
    }


def main():
    checks = [validate_packet()]
    drift = sum(1 for check in checks if check["status"] != "MATCH")
    result = {
        "schema": "Pass0016CloudQuantumCanonicalizationValidatorRun/v1",
        "pass": "0016",
        "status": "MATCH" if drift == 0 else "DRIFT",
        "match": len(checks) - drift,
        "drift": drift,
        "checks": checks,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if drift == 0 else 1)


if __name__ == "__main__":
    main()
