"""Validate pass 0017 cloud quantum metadata parser fixtures."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "cloud-quantum-metadata-parsers-pass-0017.json"


def require(condition: bool, errors: list[str], message: str) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    data = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    errors: list[str] = []

    require(data.get("schema") == "CloudQuantumProviderMetadataParserSet/v1", errors, "wrong schema")
    require(data.get("pass") == "0017", errors, "wrong pass")
    require(data.get("status") == "PARSER_PROFILE_MATCH", errors, "wrong status")
    require(bool(data.get("seal")), errors, "missing seal")
    require("does not fetch live provider metadata" in data.get("non_promotion_statement", ""), errors, "missing non-promotion boundary")

    profiles = data.get("parser_profiles", [])
    require(len(profiles) >= 3, errors, "expected at least three parser profiles")
    expected_profiles = {
        "parser-braket-get-device",
        "parser-ibm-backend-properties",
        "parser-azure-target-list",
    }
    found_profiles = {profile.get("profile_id") for profile in profiles}
    require(expected_profiles <= found_profiles, errors, "missing required parser profile")

    for profile in profiles:
        require(profile.get("schema") == "CloudQuantumProviderMetadataParserProfile/v1", errors, f"{profile.get('profile_id')} wrong schema")
        require(profile.get("sample_payload", {}).get("payload_hash"), errors, f"{profile.get('profile_id')} missing sample payload hash")
        require(profile.get("normalized_output", {}).get("hardware_claim_allowed") is True, errors, f"{profile.get('profile_id')} expected allowed sample")
        require(len(profile.get("required_raw_fields", [])) >= 4, errors, f"{profile.get('profile_id')} too few required raw fields")
        require(profile.get("hardware_rejection_rules"), errors, f"{profile.get('profile_id')} missing rejection rules")
        require(all(str(anchor).startswith("https://") for anchor in profile.get("source_anchors", [])), errors, f"{profile.get('profile_id')} has non-HTTPS source")

    register_layout = data.get("register_layout_receipt", {})
    require(register_layout.get("schema") == "QuantumRegisterLayoutReceipt/v1", errors, "missing register layout schema")
    require(register_layout.get("layout_hash"), errors, "missing register layout hash")
    require(register_layout.get("measurement_map"), errors, "missing measurement map")
    require("bitstring_10" in register_layout.get("interpretation", {}), errors, "missing bitstring interpretation")
    require("rightmost" in json.dumps(register_layout), errors, "missing string-position convention")

    post_processing = data.get("post_processing_receipt", {})
    require(post_processing.get("schema") == "QuantumPostProcessingReceipt/v1", errors, "missing post-processing schema")
    require(post_processing.get("receipt_hash"), errors, "missing post-processing hash")
    require(post_processing.get("raw_result_hash_required") is True, errors, "raw result hash not required")
    require(post_processing.get("normalized_result_hash_required") is True, errors, "normalized result hash not required")
    require(post_processing.get("mitigation_applied") is False, errors, "baseline mitigation should be false")

    negatives = data.get("negative_fixtures", [])
    expected_negatives = {
        "negative-provider-metadata-without-payload-hash",
        "negative-azure-unknown-target-kind-promoted-to-hardware",
        "negative-register-layout-omitted",
        "negative-endian-convention-absent",
        "negative-duplicate-json-key-payload",
        "negative-binary-payload-treated-as-json",
        "negative-float-precision-policy-absent",
        "negative-post-processing-without-receipt",
    }
    found_negatives = {fixture.get("fixture_id") for fixture in negatives}
    require(expected_negatives <= found_negatives, errors, "missing required negative fixture")
    require(all(fixture.get("expected_validator_status") == "REJECT" for fixture in negatives), errors, "negative fixture not rejected")

    anchors = data.get("source_anchors", [])
    require(len(anchors) >= 7, errors, "expected at least seven source anchors")
    require(all(str(anchor.get("url", "")).startswith("https://") for anchor in anchors), errors, "source anchor missing HTTPS URL")

    result = {
        "schema": "Pass0017MetadataParserValidatorRun/v1",
        "pass": "0017",
        "status": "MATCH" if not errors else "DRIFT",
        "match": 1 if not errors else 0,
        "drift": 0 if not errors else 1,
        "checks": [
            {
                "artifact": "CloudQuantumProviderMetadataParserSet",
                "path": str(SCHEMA_PATH.relative_to(ROOT)),
                "status": "MATCH" if not errors else "DRIFT",
                "parser_profile_count": len(profiles),
                "negative_fixture_count": len(negatives),
                "source_anchor_count": len(anchors),
                "errors": errors,
            }
        ],
    }

    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
