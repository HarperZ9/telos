"""Validate pass 0101 inequality-safe BQM receipt."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "inequality-safe-bqm-receipt-pass-0101.json"
RESULT = ROOT / "schemas" / "pass-0101-inequality-safe-bqm-validator-result.json"


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
    results = artifact.get("results", {})
    if artifact.get("schema") != "InequalitySafeBQMReceipt/v1":
        errors.append("schema")
    if artifact.get("status") != "INEQUALITY_SAFE_BQM_RECEIPT_MATCH":
        errors.append("status")
    if seal != sha256_obj(unsealed):
        errors.append("seal")
    if artifact.get("source_bindings", {}).get("ocean_pass") != "0100":
        errors.append("source_binding")
    if artifact.get("temp_venv", {}).get("cleaned") is not True:
        errors.append("temp_cleanup")
    if results.get("equality_penalty", {}).get("feasible") is not False:
        errors.append("equality_counterexample")
    if results.get("slack_penalty", {}).get("feasible") is not True or results.get("slack_penalty", {}).get("value") != 10:
        errors.append("slack_fix")
    if artifact.get("law_candidate", {}).get("status") != "LAW_CANDIDATE":
        errors.append("law_candidate")
    if any(row.get("status") != "MATCH" for row in artifact.get("measurements", [])):
        errors.append("measurements")
    if any(tool.get("status") != "MATCH" for tool in artifact.get("flagship_receipts", {}).values()):
        errors.append("flagships")
    if artifact.get("current_promoted_natural_laws") != []:
        errors.append("promotion_boundary")
    status = "MATCH" if not errors else "DRIFT"
    return {"schema": "Pass0101InequalitySafeBQMValidatorRun/v1", "pass": "0101", "status": status, "match": 1 if status == "MATCH" else 0, "drift": 0 if status == "MATCH" else 1, "checks": [{"artifact": "InequalitySafeBQMReceipt", "errors": errors, "path": "schemas/inequality-safe-bqm-receipt-pass-0101.json", "status": status}]}


def main() -> None:
    result = validate()
    write_json(RESULT, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
