"""Validate pass 0098 solver branch receipt interop schema."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "solver-branch-receipt-interop-schema-pass-0098.json"
RESULT = ROOT / "schemas" / "pass-0098-solver-branch-receipt-interop-validator-result.json"


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
    branches = artifact.get("branch_receipts", [])
    coverage = artifact.get("coverage", {})
    ids = {row.get("branch_id"): row for row in branches}
    if artifact.get("schema") != "SolverBranchReceiptInteropSchema/v1":
        errors.append("schema")
    if artifact.get("status") != "SOLVER_BRANCH_RECEIPT_INTEROP_SCHEMA_MATCH":
        errors.append("status")
    if seal != sha256_obj(unsealed):
        errors.append("seal")
    if artifact.get("source_bindings", {}).get("workbench_pass") != "0097":
        errors.append("source_bindings")
    if len(branches) != 8 or coverage.get("branch_count") != 8:
        errors.append("branch_count")
    if coverage.get("executed_count") != 6 or coverage.get("dependency_boundary_count") != 2:
        errors.append("coverage")
    if coverage.get("best_value") != 162 or coverage.get("max_observed_gap") != 16:
        errors.append("values")
    if ids.get("ortools_knapsack", {}).get("execution_status") != "NOT_EXECUTED_DEPENDENCY_MISSING":
        errors.append("ortools_boundary")
    if ids.get("buildlang_greedy_ratio_order", {}).get("gap_to_exact") != 16:
        errors.append("greedy_gap")
    if len(artifact.get("source_anchors", [])) != 4 or len(artifact.get("required_fields", [])) != 11:
        errors.append("schema_contract")
    if any(row.get("status") != "MATCH" for row in artifact.get("measurements", [])):
        errors.append("measurements")
    if any(tool.get("status") != "MATCH" for tool in artifact.get("flagship_receipts", {}).values()):
        errors.append("flagships")
    if artifact.get("unsupported_claim_count") != 0 or artifact.get("current_promoted_natural_laws") != []:
        errors.append("promotion_boundary")
    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0098SolverBranchReceiptInteropValidatorRun/v1",
        "pass": "0098",
        "status": status,
        "match": 1 if status == "MATCH" else 0,
        "drift": 0 if status == "MATCH" else 1,
        "checks": [{"artifact": "SolverBranchReceiptInteropSchema", "errors": errors, "path": "schemas/solver-branch-receipt-interop-schema-pass-0098.json", "branch_count": len(branches), "executed_count": coverage.get("executed_count"), "status": status}],
    }


def main() -> None:
    result = validate()
    write_json(RESULT, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
