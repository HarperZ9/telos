"""Validate pass 0135 biology/medicine/robotics nomenclature map."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "bio-med-robotics-nomenclature-map-pass-0135.json"
RESULT = ROOT / "schemas" / "pass-0135-bio-med-robotics-nomenclature-map-validator-result.json"


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
    errors: list[str] = []
    summary = artifact.get("gather_summary", {})
    require(artifact.get("schema") == "BioMedRoboticsNomenclatureMapReceipt/v1", errors, "schema")
    require(artifact.get("status") == "BIO_MED_ROBOTICS_NOMENCLATURE_MAP_MATCH", errors, "status")
    require(seal == sha256_obj(unsealed), errors, "seal")
    require(summary.get("source_count", 0) >= 30, errors, "source_count")
    require(summary.get("usable_source_count", 0) >= 25, errors, "usable_source_count")
    require(summary.get("client_challenge_count", 0) >= 3, errors, "client_challenge_count")
    require(summary.get("empty_capture_count", 0) >= 1, errors, "empty_capture_count")
    require(len(artifact.get("archive_substrate_catalog", [])) >= 12, errors, "archive_substrate_catalog")
    require(len(artifact.get("domain_expansion_queue", [])) >= 12, errors, "domain_expansion_queue")
    require(len(artifact.get("domain_lanes", [])) >= 8, errors, "domain_lanes")
    require(len(artifact.get("terminology_bridges", [])) >= 8, errors, "terminology_bridges")
    require(all(row.get("status") == "HYPOTHESIS_SOURCE_MAP" for row in artifact.get("domain_lanes", [])), errors, "lane_status")
    require(all(row.get("status") == "REJECTED" for row in artifact.get("negative_fixtures", [])), errors, "negative_fixtures")
    require(artifact.get("current_promoted_natural_laws") == [], errors, "natural_laws")
    require(all(row.get("status") == "MATCH" for row in artifact.get("flagship_receipts", {}).values()), errors, "flagship_receipts")
    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0135BioMedRoboticsNomenclatureMapValidatorRun/v1",
        "pass": "0135",
        "status": status,
        "checks": [{
            "artifact": "BioMedRoboticsNomenclatureMapReceipt",
            "status": status,
            "errors": errors,
            "source_count": summary.get("source_count"),
            "usable_source_count": summary.get("usable_source_count"),
            "lane_count": len(artifact.get("domain_lanes", [])),
            "bridge_count": len(artifact.get("terminology_bridges", [])),
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
