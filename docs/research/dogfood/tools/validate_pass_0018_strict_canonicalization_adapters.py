"""Validate pass 0018 strict canonicalization and layout adapter fixtures."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "quantum-strict-canonicalization-adapters-pass-0018.json"


def require(condition: bool, errors: list[str], message: str) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    data = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    errors: list[str] = []

    require(data.get("schema") == "QuantumStrictCanonicalizationAdapterSet/v1", errors, "wrong schema")
    require(data.get("pass") == "0018", errors, "wrong pass")
    require(data.get("status") == "STRICT_ADAPTER_MATCH", errors, "wrong status")
    require(bool(data.get("seal")), errors, "missing seal")
    require("does not run a quantum job" in data.get("non_promotion_statement", ""), errors, "missing non-promotion")

    policy = data.get("strict_policy", {})
    require(policy.get("schema") == "StrictQuantumCanonicalizationPolicy/v1", errors, "missing strict policy")
    require(policy.get("duplicate_json_key_detection_required") is True, errors, "duplicate key detection not required")
    require(policy.get("duplicate_key_fixture", {}).get("detected_duplicate_keys") == ["00"], errors, "duplicate key fixture did not detect 00")
    require(policy.get("binary_payload_policy", {}).get("parsed_json_allowed") is False, errors, "binary JSON parsing not rejected")
    require(policy.get("binary_payload_policy", {}).get("content_hash_required") is True, errors, "binary content hash not required")
    require("content_hash" in policy.get("object_storage_reference_policy", {}).get("required_fields", []), errors, "object storage content hash missing")
    require(policy.get("floating_point_policy", {}).get("precision_policy_required") is True, errors, "float policy not required")
    require(bool(policy.get("policy_hash")), errors, "missing policy hash")

    adapters = data.get("adapter_profiles", [])
    expected_adapters = {
        "layout-adapter-qiskit",
        "layout-adapter-amazon-braket",
        "layout-adapter-cirq",
        "layout-adapter-pennylane",
        "layout-adapter-qir",
    }
    found_adapters = {adapter.get("adapter_id") for adapter in adapters}
    require(expected_adapters <= found_adapters, errors, "missing required adapter")
    require(len(adapters) >= 5, errors, "expected at least five adapters")
    for adapter in adapters:
        require(adapter.get("schema") == "QuantumRegisterLayoutAdapter/v1", errors, f"{adapter.get('adapter_id')} wrong schema")
        require(adapter.get("source_anchor", "").startswith("https://"), errors, f"{adapter.get('adapter_id')} missing HTTPS source")
        require(adapter.get("required_receipt_fields"), errors, f"{adapter.get('adapter_id')} missing required fields")
        require(bool(adapter.get("adapter_hash")), errors, f"{adapter.get('adapter_id')} missing hash")

    op = data.get("post_processing_operation", {})
    require(op.get("schema") == "QuantumPostProcessingOperation/v1", errors, "missing post-processing op")
    require(op.get("input_hash"), errors, "missing post-processing input hash")
    require(op.get("output_hash"), errors, "missing post-processing output hash")
    require(op.get("parameters_hash"), errors, "missing post-processing parameter hash")
    require(op.get("deterministic") is True, errors, "noop operation should be deterministic")

    negatives = data.get("negative_fixtures", [])
    expected_negatives = {
        "negative-duplicate-json-key-accepted",
        "negative-binary-payload-parsed-as-json",
        "negative-object-storage-uri-without-content-hash",
        "negative-float-result-without-precision-policy",
        "negative-qiskit-counts-using-braket-layout",
        "negative-cirq-histogram-without-fold-func",
        "negative-pennylane-counts-without-wire-order",
        "negative-qir-result-without-record-map",
        "negative-post-processing-operation-without-hashes",
    }
    found_negatives = {fixture.get("fixture_id") for fixture in negatives}
    require(expected_negatives <= found_negatives, errors, "missing negative fixture")
    require(all(fixture.get("expected_validator_status") == "REJECT" for fixture in negatives), errors, "negative fixture not rejected")

    anchors = data.get("source_anchors", [])
    require(len(anchors) >= 8, errors, "expected at least eight source anchors")
    require(all(anchor.get("url", "").startswith("https://") for anchor in anchors), errors, "source anchor missing HTTPS")

    result = {
        "schema": "Pass0018StrictCanonicalizationAdapterValidatorRun/v1",
        "pass": "0018",
        "status": "MATCH" if not errors else "DRIFT",
        "match": 1 if not errors else 0,
        "drift": 0 if not errors else 1,
        "checks": [
            {
                "artifact": "QuantumStrictCanonicalizationAdapterSet",
                "path": str(SCHEMA_PATH.relative_to(ROOT)),
                "status": "MATCH" if not errors else "DRIFT",
                "adapter_profile_count": len(adapters),
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
