"""Validate pass 0096 YouTube field growth-vector scorecard."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "youtube-field-growth-vector-scorecard-pass-0096.json"
RESULT = ROOT / "schemas" / "pass-0096-youtube-field-growth-vector-scorecard-validator-result.json"


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
    vectors = artifact.get("field_vectors", [])
    source = artifact.get("source_summary", {})
    if artifact.get("schema") != "YouTubeFieldGrowthVectorScorecard/v1":
        errors.append("schema")
    if artifact.get("status") != "YOUTUBE_FIELD_GROWTH_VECTOR_SCORECARD_MATCH":
        errors.append("status")
    if seal != sha256_obj(unsealed):
        errors.append("seal")
    if artifact.get("source_bindings") != {"youtube_pass": "0085", "bridge_pass": "0093", "workflow_pass": "0094", "native_buildlang_pass": "0095"}:
        errors.append("source_bindings")
    if source.get("valid_video_count") != 19 or source.get("cluster_count") != 7:
        errors.append("youtube_counts")
    if source.get("metadata_match_count") != 19 or source.get("transcript_receipt_count") != 19:
        errors.append("receipt_counts")
    if not vectors or vectors[0].get("id") != "optimization_proof_workbench" or vectors[0].get("source_video_count") != 13:
        errors.append("primary_vector")
    if len(vectors) != 8:
        errors.append("vector_count")
    if artifact.get("primary_30_day_push", {}).get("vector_id") != "optimization_proof_workbench":
        errors.append("primary_push")
    if artifact.get("buildlang_binding", {}).get("verify_check_count") != 18 or artifact.get("buildlang_binding", {}).get("best_value") != 162:
        errors.append("buildlang_binding")
    if artifact.get("workflow_binding", {}).get("exact_value") != 162:
        errors.append("workflow_binding")
    if len(artifact.get("integration_map", [])) != 10:
        errors.append("integration_map")
    if len(artifact.get("measurements", [])) != 9 or any(row.get("status") != "MATCH" for row in artifact.get("measurements", [])):
        errors.append("measurements")
    if any(tool.get("status") != "MATCH" for tool in artifact.get("flagship_receipts", {}).values()):
        errors.append("flagships")
    if artifact.get("unsupported_claim_count") != 0 or artifact.get("current_promoted_natural_laws") != []:
        errors.append("promotion_boundary")
    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0096YouTubeFieldGrowthVectorScorecardValidatorRun/v1",
        "pass": "0096",
        "status": status,
        "match": 1 if status == "MATCH" else 0,
        "drift": 0 if status == "MATCH" else 1,
        "checks": [{
            "artifact": "YouTubeFieldGrowthVectorScorecard",
            "errors": errors,
            "path": "schemas/youtube-field-growth-vector-scorecard-pass-0096.json",
            "primary_vector": vectors[0].get("id") if vectors else None,
            "valid_video_count": source.get("valid_video_count"),
            "vector_count": len(vectors),
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
