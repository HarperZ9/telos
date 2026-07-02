"""Validate pass 0083 Forum proof-lane vocabulary repair."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "forum-proof-lane-vocabulary-repair-pass-0083.json"
RESULT = ROOT / "schemas" / "pass-0083-forum-proof-lane-vocabulary-repair-validator-result.json"


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)


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
    summary = artifact.get("repair_summary", {})
    if artifact.get("schema") != "ForumProofLaneVocabularyRepair/v1":
        errors.append("schema")
    if artifact.get("status") != "FORUM_PROOF_LANE_VOCABULARY_REPAIR_MATCH":
        errors.append("status")
    if seal != sha256_obj(unsealed):
        errors.append("seal")
    if artifact.get("baseline", {}).get("source_pass") != "0082":
        errors.append("baseline")
    if summary.get("route_probe_count") != 8 or summary.get("route_match_count") != 8:
        errors.append("routes")
    if summary.get("repair_status") != "MATCH":
        errors.append("repair_status")
    if summary.get("improvement_over_baseline", 0) < 4:
        errors.append("improvement")
    if len(artifact.get("taxonomy_patch_candidates", [])) < 7:
        errors.append("taxonomy_patch_candidates")
    if artifact.get("unsupported_claim_count") != 0 or artifact.get("current_promoted_natural_laws") != []:
        errors.append("promotion_boundary")
    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0083ForumProofLaneVocabularyRepairValidatorRun/v1",
        "pass": "0083",
        "status": status,
        "match": 1 if status == "MATCH" else 0,
        "drift": 0 if status == "MATCH" else 1,
        "checks": [{
            "artifact": "ForumProofLaneVocabularyRepair",
            "errors": errors,
            "path": "schemas/forum-proof-lane-vocabulary-repair-pass-0083.json",
            "baseline_non_escalated": artifact.get("baseline", {}).get("non_escalated_count"),
            "repaired_non_escalated": summary.get("non_escalated_count"),
            "persistent_escalation_lanes": summary.get("persistent_escalation_lanes", []),
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
