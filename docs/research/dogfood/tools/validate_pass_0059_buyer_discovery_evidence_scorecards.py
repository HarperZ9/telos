"""Validate pass 0059 buyer-discovery evidence scorecards."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "buyer-discovery-evidence-scorecards-pass-0059.json"
BRIDGE = ROOT / "schemas" / "forum-route-vocabulary-bridge-pass-0058.json"
RESULT = ROOT / "schemas" / "pass-0059-buyer-discovery-evidence-scorecards-validator-result.json"
LANES = ["project-telos", "deep-research", "technical-writing"]


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
    bridge = read_json(BRIDGE)
    errors: list[str] = []
    unsealed = dict(artifact)
    seal = unsealed.pop("seal", None)
    scorecards = artifact.get("scorecards", [])
    prompt_count = sum(row.get("interview_prompt_count", 0) for row in scorecards)
    target_count = sum(len(row.get("market_data_targets", [])) for row in scorecards)
    if artifact.get("schema") != "BuyerDiscoveryEvidenceScorecards/v1":
        errors.append("schema")
    if artifact.get("status") != "BUYER_DISCOVERY_EVIDENCE_SCORECARDS_MATCH":
        errors.append("status")
    if seal != sha256_obj(unsealed):
        errors.append("seal")
    if artifact.get("upstream_bridge", {}).get("seal") != bridge.get("seal"):
        errors.append("upstream_bridge")
    if artifact.get("source_anchor_count", 0) < 9:
        errors.append("source_count")
    if {row.get("buyer_id") for row in scorecards} != {"research_lab", "ai_infra", "regulated_agent"}:
        errors.append("buyer_ids")
    if prompt_count != 9:
        errors.append("prompt_count")
    if target_count < 12:
        errors.append("target_count")
    if artifact.get("market_data_status") != "COLLECTION_TARGETS_DEFINED":
        errors.append("market_data_status")
    if artifact.get("market_claim_boundary") != "HYPOTHESIS_ONLY":
        errors.append("market_boundary")
    if artifact.get("unsupported_claim_count") != 0:
        errors.append("unsupported_claim_count")
    if artifact.get("current_promoted_natural_laws") != []:
        errors.append("natural_law_promotion")
    for row in scorecards:
        if row.get("route_lane_split") != LANES:
            errors.append(f"{row.get('buyer_id')}_lanes")
        if row.get("scorecard_status") != "NEEDS_INTERVIEW_DATA":
            errors.append(f"{row.get('buyer_id')}_status")
    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0059BuyerDiscoveryEvidenceScorecardsValidatorRun/v1",
        "pass": "0059",
        "status": status,
        "match": 1 if status == "MATCH" else 0,
        "drift": 0 if status == "MATCH" else 1,
        "checks": [
            {
                "artifact": "BuyerDiscoveryEvidenceScorecards",
                "errors": errors,
                "path": "schemas/buyer-discovery-evidence-scorecards-pass-0059.json",
                "prompt_count": prompt_count,
                "scorecard_count": len(scorecards),
                "source_anchor_count": artifact.get("source_anchor_count"),
                "status": status,
                "target_count": target_count,
            }
        ],
    }


def main() -> None:
    result = validate()
    write_json(RESULT, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
