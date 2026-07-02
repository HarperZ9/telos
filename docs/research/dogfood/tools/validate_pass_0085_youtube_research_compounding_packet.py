"""Validate pass 0085 YouTube research compounding packet."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "youtube-research-compounding-packet-pass-0085.json"
RESULT = ROOT / "schemas" / "pass-0085-youtube-research-compounding-packet-validator-result.json"


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
    if artifact.get("schema") != "YouTubeResearchCompoundingPacket/v1":
        errors.append("schema")
    if artifact.get("status") != "YOUTUBE_RESEARCH_COMPOUNDING_PACKET_MATCH":
        errors.append("status")
    if seal != sha256_obj(unsealed):
        errors.append("seal")
    if artifact.get("valid_url_count") != 19 or artifact.get("valid_video_count") != 19 or artifact.get("metadata_match_count") != 19 or artifact.get("invalid_url_count") != 1:
        errors.append("source_counts")
    if artifact.get("gather_match_count", 0) < 15:
        errors.append("gather_receipts")
    if artifact.get("transcript_receipt_count", 0) < 15:
        errors.append("transcript_receipts")
    if len(artifact.get("research_clusters", [])) < 7 or len(artifact.get("compounding_vectors", [])) < 7:
        errors.append("clusters")
    if artifact.get("video_corpus_summary", {}).get("dominant_cluster_video_count") != 13:
        errors.append("video_corpus_summary")
    if sum(1 for row in artifact.get("source_cards", []) if row.get("source_weight") == "CRITICAL_DATA") != 19:
        errors.append("source_weights")
    if any(receipt.get("status") != "MATCH" for receipt in artifact.get("flagship_receipts", {}).values()):
        errors.append("flagship_receipts")
    if artifact.get("unsupported_claim_count") != 0 or artifact.get("current_promoted_natural_laws") != []:
        errors.append("promotion_boundary")
    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0085YouTubeResearchCompoundingPacketValidatorRun/v1",
        "pass": "0085",
        "status": status,
        "match": 1 if status == "MATCH" else 0,
        "drift": 0 if status == "MATCH" else 1,
        "checks": [{
            "artifact": "YouTubeResearchCompoundingPacket",
            "errors": errors,
            "path": "schemas/youtube-research-compounding-packet-pass-0085.json",
            "valid_url_count": artifact.get("valid_url_count"),
            "valid_video_count": artifact.get("valid_video_count"),
            "metadata_match_count": artifact.get("metadata_match_count"),
            "gather_match_count": artifact.get("gather_match_count"),
            "transcript_receipt_count": artifact.get("transcript_receipt_count"),
            "invalid_url_count": artifact.get("invalid_url_count"),
            "cluster_count": len(artifact.get("research_clusters", [])),
            "dominant_cluster": artifact.get("video_corpus_summary", {}).get("dominant_cluster"),
            "dominant_cluster_video_count": artifact.get("video_corpus_summary", {}).get("dominant_cluster_video_count"),
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
