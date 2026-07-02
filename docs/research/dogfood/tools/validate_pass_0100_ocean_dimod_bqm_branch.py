"""Validate pass 0100 Ocean/dimod BQM branch receipt."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "ocean-dimod-bqm-branch-receipt-pass-0100.json"
RESULT = ROOT / "schemas" / "pass-0100-ocean-dimod-bqm-branch-validator-result.json"


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
    branch = artifact.get("solver_branch_receipt", {})
    if artifact.get("schema") != "OceanDimodBQMBranchReceipt/v1":
        errors.append("schema")
    if artifact.get("status") != "OCEAN_DIMOD_BQM_BRANCH_RECEIPT_MATCH":
        errors.append("status")
    if seal != sha256_obj(unsealed):
        errors.append("seal")
    if artifact.get("source_bindings", {}).get("ortools_pass") != "0099":
        errors.append("source_binding")
    if artifact.get("global_availability", {}).get("dimod_available") is not False or artifact.get("global_availability", {}).get("dwave_available") is not False:
        errors.append("global_availability")
    if artifact.get("install_command", {}).get("exit_code") != 0 or artifact.get("run_command", {}).get("exit_code") != 0:
        errors.append("commands")
    if artifact.get("temp_venv", {}).get("cleaned") is not True:
        errors.append("temp_cleanup")
    if branch.get("value") != 162 or branch.get("weight") != 29 or branch.get("mask") != 2347 or branch.get("gap_to_exact") != 0:
        errors.append("branch_result")
    if artifact.get("bqm_summary", {}).get("linear_terms") != 12 or artifact.get("bqm_summary", {}).get("quadratic_terms") != 66:
        errors.append("bqm_shape")
    if any(row.get("status") != "MATCH" for row in artifact.get("measurements", [])):
        errors.append("measurements")
    if any(tool.get("status") != "MATCH" for tool in artifact.get("flagship_receipts", {}).values()):
        errors.append("flagships")
    if artifact.get("unsupported_claim_count") != 0 or artifact.get("current_promoted_natural_laws") != []:
        errors.append("promotion_boundary")
    status = "MATCH" if not errors else "DRIFT"
    return {"schema": "Pass0100OceanDimodBQMBranchValidatorRun/v1", "pass": "0100", "status": status, "match": 1 if status == "MATCH" else 0, "drift": 0 if status == "MATCH" else 1, "checks": [{"artifact": "OceanDimodBQMBranchReceipt", "errors": errors, "path": "schemas/ocean-dimod-bqm-branch-receipt-pass-0100.json", "value": branch.get("value"), "dimod_version": artifact.get("dimod_version"), "status": status}]}


def main() -> None:
    result = validate()
    write_json(RESULT, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
