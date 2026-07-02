"""Validate pass 0069 Telos multi-receipt joiner artifact."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "telos-multireceipt-joiner-pass-0069.json"
RESULT = ROOT / "schemas" / "pass-0069-telos-multireceipt-joiner-validator-result.json"
REQUIRED_CLASSES = {"source_intake", "workspace_context", "routing", "verification", "continuity", "action"}


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def sha256_obj(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def validate() -> dict:
    artifact = read_json(ARTIFACT)
    errors: list[str] = []
    unsealed = dict(artifact)
    seal = unsealed.pop("seal", None)
    components = artifact.get("component_receipts", [])
    kinds = {row.get("kind") for row in components}
    packet = artifact.get("product_packet", {})
    if artifact.get("schema") != "TelosMultiReceiptJoiner/v1":
        errors.append("schema")
    if artifact.get("status") != "TELOS_MULTIRECEIPT_JOINER_MATCH":
        errors.append("status")
    if seal != sha256_obj(unsealed):
        errors.append("seal")
    if kinds != REQUIRED_CLASSES:
        errors.append("required_classes")
    if packet.get("component_count") != len(components):
        errors.append("component_count")
    if packet.get("unsupported_claim_count") != 0 or artifact.get("unsupported_claim_count") != 0:
        errors.append("unsupported_claim_count")
    if packet.get("raw_private_payload_required") or packet.get("model_reasoning_required_for_replay"):
        errors.append("replay_boundary")
    for row in components:
        if row.get("verification_status") != "MATCH":
            errors.append(f"verification:{row.get('component_id')}")
        if row.get("raw_payload_included"):
            errors.append(f"raw_payload:{row.get('component_id')}")
        if len(row.get("digest", "")) != 64 or len(row.get("seal", "")) != 64:
            errors.append(f"digest_or_seal:{row.get('component_id')}")
    for item in artifact.get("negative_fixtures", []):
        if item.get("expected_status") != "REJECT" or not item.get("reject_reason"):
            errors.append(f"negative_fixture:{item.get('fixture_id')}")
    if len(artifact.get("negative_fixtures", [])) < 5:
        errors.append("negative_fixture_count")
    if len(artifact.get("ablation_results", [])) != 7:
        errors.append("ablation_count")
    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0069TelosMultiReceiptJoinerValidatorRun/v1",
        "pass": "0069",
        "status": status,
        "match": 1 if status == "MATCH" else 0,
        "drift": 0 if status == "MATCH" else 1,
        "checks": [{
            "artifact": "TelosMultiReceiptJoiner",
            "ablation_count": len(artifact.get("ablation_results", [])),
            "component_count": len(components),
            "errors": errors,
            "negative_fixture_count": len(artifact.get("negative_fixtures", [])),
            "path": "schemas/telos-multireceipt-joiner-pass-0069.json",
            "status": status,
        }],
    }


def main() -> None:
    result = validate()
    write_json(RESULT, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
