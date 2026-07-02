"""Validate pass 0134 all-video author/theory index."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "all-video-author-theory-index-pass-0134.json"
RESULT = ROOT / "schemas" / "pass-0134-all-video-author-theory-index-validator-result.json"


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
    videos = artifact.get("video_sources", [])
    authors = artifact.get("author_nodes", [])
    lanes = artifact.get("theory_lanes", [])
    errors: list[str] = []

    require(artifact.get("schema") == "AllVideoAuthorTheoryIndexReceipt/v1", errors, "schema")
    require(artifact.get("status") == "ALL_VIDEO_AUTHOR_THEORY_INDEX_MATCH", errors, "status")
    require(seal == sha256_obj(unsealed), errors, "seal")
    require(len(videos) >= 50, errors, "video_count")
    require(len(authors) >= 20, errors, "author_count")
    require(len(lanes) >= 8, errors, "lane_count")
    require(all(row.get("claim_status") == "SOURCE_LEAD_ONLY" for row in videos), errors, "source_lead_boundary")
    require(all(row.get("status") == "HYPOTHESIS_SOURCE_LEAD" for row in lanes), errors, "lane_status")
    require(len(artifact.get("reference_expansion_queue", [])) >= 15, errors, "reference_queue")
    require(all(row.get("status") == "REJECTED" for row in artifact.get("negative_fixtures", [])), errors, "negative_fixtures")
    require(artifact.get("current_promoted_natural_laws") == [], errors, "natural_laws")
    require(all(row.get("status") == "MATCH" for row in artifact.get("flagship_receipts", {}).values()), errors, "flagship_receipts")

    status = "MATCH" if not errors else "DRIFT"
    result = {
        "schema": "Pass0134AllVideoAuthorTheoryIndexValidatorRun/v1",
        "pass": "0134",
        "status": status,
        "checks": [{
            "artifact": "AllVideoAuthorTheoryIndexReceipt",
            "errors": errors,
            "status": status,
            "video_count": len(videos),
            "author_count": len(authors),
            "lane_count": len(lanes),
            "reference_queue_count": len(artifact.get("reference_expansion_queue", [])),
        }],
    }
    return result


def main() -> None:
    result = validate()
    write_json(RESULT, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
