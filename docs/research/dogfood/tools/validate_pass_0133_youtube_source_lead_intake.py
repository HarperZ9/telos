"""Validate pass 0133 YouTube source-lead intake."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "youtube-source-lead-intake-pass-0133.json"
RESULT = ROOT / "schemas" / "pass-0133-youtube-source-lead-intake-validator-result.json"


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
    sources = artifact.get("source_receipts", [])
    leads = artifact.get("video_leads", [])
    routes = {row.get("route") for row in artifact.get("route_summary", [])}
    negatives = artifact.get("negative_fixtures", [])
    errors: list[str] = []

    require(artifact.get("schema") == "YouTubeSourceLeadIntakeReceipt/v1", errors, "schema")
    require(artifact.get("status") == "YOUTUBE_SOURCE_LEAD_INTAKE_MATCH", errors, "status")
    require(seal == sha256_obj(unsealed), errors, "seal")
    require(artifact.get("source_bindings", {}).get("proof_transfer_pass") == "0132", errors, "upstream_binding")
    require(len(sources) >= 19 and all(row.get("status") == "GATHER_VERIFIED" for row in sources), errors, "sources")
    require(all(row.get("raw_body_exported") is False for row in sources), errors, "raw_body_boundary")
    require(len(leads) >= 9 and all(row.get("status") == "SOURCE_LEAD_ONLY" for row in leads), errors, "video_leads")
    require("biology_evolution_geometry" in routes and "theoretical_computing_breakthrough" in routes, errors, "routes")
    require(len(negatives) >= 6 and all(row.get("status") == "REJECTED" for row in negatives), errors, "negative_fixtures")
    require(artifact.get("current_promoted_natural_laws") == [], errors, "natural_laws")
    require(all(row.get("status") == "MATCH" for row in artifact.get("flagship_receipts", {}).values()), errors, "flagships")

    status = "MATCH" if not errors else "DRIFT"
    return {"schema": "Pass0133YouTubeSourceLeadIntakeValidatorRun/v1", "pass": "0133", "status": status, "checks": [{"artifact": "YouTubeSourceLeadIntake", "errors": errors, "status": status, "source_count": len(sources), "video_count": len(leads), "route_count": len(routes)}]}


def main() -> None:
    result = validate()
    write_json(RESULT, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
