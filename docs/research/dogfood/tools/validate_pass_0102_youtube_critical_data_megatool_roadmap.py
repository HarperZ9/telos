"""Validate pass 0102 YouTube critical-data roadmap."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "youtube-critical-data-megatool-roadmap-pass-0102.json"
RESULT = ROOT / "schemas" / "pass-0102-youtube-critical-data-megatool-roadmap-validator-result.json"


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)


def sha256_obj(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n", encoding="utf-8")


def validate() -> dict:
    artifact = read_json(ARTIFACT)
    source = artifact.get("source_summary", {})
    nodes = artifact.get("roadmap_nodes", [])
    unsealed = dict(artifact)
    seal = unsealed.pop("seal", None)
    errors: list[str] = []
    if artifact.get("schema") != "YouTubeCriticalDataMegatoolRoadmap/v1":
        errors.append("schema")
    if artifact.get("status") != "YOUTUBE_CRITICAL_DATA_MEGATOOL_ROADMAP_MATCH":
        errors.append("status")
    if seal != sha256_obj(unsealed):
        errors.append("seal")
    if artifact.get("source_bindings", {}).get("youtube_pass") != "0085":
        errors.append("youtube_binding")
    if artifact.get("source_bindings", {}).get("inequality_pass") != "0101":
        errors.append("inequality_binding")
    if source.get("valid_video_count") != 19 or source.get("invalid_url_count") != 1:
        errors.append("source_counts")
    if source.get("transcript_receipt_count") != 19 or source.get("raw_transcript_stored") is not False:
        errors.append("transcript_policy")
    if len(artifact.get("source_to_architecture_claims", [])) != 7:
        errors.append("architecture_claims")
    if len(nodes) != 8 or not nodes or nodes[0].get("node_id") != "optimization_proof_workbench":
        errors.append("roadmap_nodes")
    first_requirements = nodes[0].get("requirements", []) if nodes else []
    if not any(isinstance(row, dict) and row.get("requirement_id") == "constraint_encoding_receipt" for row in first_requirements):
        errors.append("encoding_requirement")
    if len(artifact.get("experiments", [])) != 3:
        errors.append("experiments")
    if any(row.get("status") != "MATCH" for row in artifact.get("measurements", [])):
        errors.append("measurements")
    if any(row.get("status") != "MATCH" for row in artifact.get("flagship_receipts", {}).values()):
        errors.append("flagships")
    if artifact.get("current_promoted_natural_laws") != [] or artifact.get("unsupported_claim_count") != 0:
        errors.append("promotion_boundary")
    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0102YouTubeCriticalDataMegatoolRoadmapValidatorRun/v1",
        "pass": "0102",
        "status": status,
        "match": 1 if status == "MATCH" else 0,
        "drift": 0 if status == "MATCH" else 1,
        "checks": [{
            "artifact": "YouTubeCriticalDataMegatoolRoadmap",
            "errors": errors,
            "path": "schemas/youtube-critical-data-megatool-roadmap-pass-0102.json",
            "valid_video_count": source.get("valid_video_count"),
            "top_priority": nodes[0].get("node_id") if nodes else None,
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
