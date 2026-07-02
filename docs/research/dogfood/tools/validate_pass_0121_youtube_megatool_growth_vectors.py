"""Validate pass 0121 YouTube megatool growth-vector receipt."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "youtube-megatool-growth-vector-receipt-pass-0121.json"
RESULT = ROOT / "schemas" / "pass-0121-youtube-megatool-growth-vector-validator-result.json"


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)


def sha256_obj(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n", encoding="utf-8")


def require(condition: bool, errors: list[str], label: str) -> None:
    if not condition:
        errors.append(label)


def validate() -> dict:
    artifact = read_json(ARTIFACT)
    unsealed = dict(artifact)
    seal = unsealed.pop("seal", None)
    leads = artifact.get("youtube_source_leads", [])
    vectors = artifact.get("growth_vectors", [])
    ids = {row.get("video_id") for row in leads}
    errors: list[str] = []

    require(artifact.get("schema") == "YoutubeMegatoolGrowthVectorReceipt/v1", errors, "schema")
    require(artifact.get("status") == "YOUTUBE_MEGATOOL_GROWTH_VECTOR_MATCH", errors, "status")
    require(seal == sha256_obj(unsealed), errors, "seal")
    require(artifact.get("source_bindings", {}).get("formal_physics_bridge_pass") == "0116", errors, "bridge_binding")
    require(artifact.get("source_bindings", {}).get("runtime_branch_pass") == "0120", errors, "runtime_binding")
    require(ids == {"HbKzqvey5PA", "4MQbd5wTlI8", "EdVG5qNm2rY", "nYwid6Q5HXk"}, errors, "video_ids")
    require(all(row.get("transcript_object_present") is True for row in leads), errors, "transcript_objects")
    require(all(row.get("raw_transcript_included") is False for row in leads), errors, "raw_transcript_boundary")
    require(all(row.get("claim_status") == "SOURCE_LEAD_ONLY" for row in leads), errors, "lead_claim_status")
    require(all(sum(row.get("signal_counts", {}).values()) > 0 for row in leads), errors, "signal_counts")
    require(len(vectors) >= 6, errors, "growth_vector_count")
    require(all(row.get("claim_status") == "HYPOTHESIS" for row in vectors), errors, "growth_status")
    require(all(row.get("next_experiments") for row in vectors), errors, "experiments")
    require(artifact.get("primary_30_day_push") == vectors[0].get("vector_id") if vectors else False, errors, "primary_push")
    require(any(row.get("node") == "BuildLang/buildc" for row in artifact.get("integration_map", [])), errors, "buildlang_node")
    require(artifact.get("unsupported_claim_count") == 0, errors, "unsupported_claim_count")
    require(artifact.get("current_promoted_natural_laws") == [], errors, "natural_laws")
    require(all(row.get("status") == "MATCH" for row in artifact.get("flagship_receipts", {}).values()), errors, "flagships")

    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0121YoutubeMegatoolGrowthVectorValidatorRun/v1",
        "pass": "0121",
        "status": status,
        "checks": [{"artifact": "YoutubeMegatoolGrowthVectorReceipt", "errors": errors, "status": status, "video_count": len(leads), "growth_vector_count": len(vectors)}],
    }


def main() -> None:
    result = validate()
    write_json(RESULT, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
