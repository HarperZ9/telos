"""Validate pass 0077 path-selector contract scorecard."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "path-selector-contract-scorecard-pass-0077.json"
RESULT = ROOT / "schemas" / "pass-0077-path-selector-contract-scorecard-validator-result.json"


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
    motions = artifact.get("product_motions", [])
    if artifact.get("schema") != "PathSelectorContractGrowthScorecard/v1":
        errors.append("schema")
    if artifact.get("status") != "PATH_SELECTOR_CONTRACT_SCORECARD_MATCH":
        errors.append("status")
    if seal != sha256_obj(unsealed):
        errors.append("seal")
    if artifact.get("contract", {}).get("schema") != "IndexPathSelectorReceipt/v1":
        errors.append("contract_schema")
    if len(artifact.get("evidence", [])) < 8:
        errors.append("evidence_count")
    if len(artifact.get("growth_vectors", [])) < 5:
        errors.append("growth_vector_count")
    if len(motions) != 3:
        errors.append("motion_count")
    if motions and motions[0].get("id") != artifact.get("primary_30_day_push", {}).get("motion"):
        errors.append("primary_push")
    if any(row.get("uniqueness_status") != "hypothesis" for row in motions):
        errors.append("uniqueness_status")
    if artifact.get("unsupported_claim_count") != 0 or artifact.get("current_promoted_natural_laws") != []:
        errors.append("promotion_boundary")
    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0077PathSelectorContractScorecardValidatorRun/v1",
        "pass": "0077",
        "status": status,
        "match": 1 if status == "MATCH" else 0,
        "drift": 0 if status == "MATCH" else 1,
        "checks": [{
            "artifact": "PathSelectorContractGrowthScorecard",
            "errors": errors,
            "path": "schemas/path-selector-contract-scorecard-pass-0077.json",
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
