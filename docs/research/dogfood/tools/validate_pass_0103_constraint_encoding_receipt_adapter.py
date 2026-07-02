"""Validate pass 0103 constraint-encoding receipt adapter."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "constraint-encoding-receipt-adapter-pass-0103.json"
RESULT = ROOT / "schemas" / "pass-0103-constraint-encoding-receipt-adapter-validator-result.json"


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
    coverage = artifact.get("coverage", {})
    rows = artifact.get("constraint_encoding_receipts", [])
    unsealed = dict(artifact)
    seal = unsealed.pop("seal", None)
    errors: list[str] = []
    if artifact.get("schema") != "ConstraintEncodingReceiptAdapter/v1":
        errors.append("schema")
    if artifact.get("status") != "CONSTRAINT_ENCODING_RECEIPT_ADAPTER_MATCH":
        errors.append("status")
    if seal != sha256_obj(unsealed):
        errors.append("seal")
    if artifact.get("source_bindings", {}).get("inequality_pass") != "0101":
        errors.append("inequality_binding")
    if coverage.get("receipt_count") != 10 or coverage.get("executed_receipt_count") != 8:
        errors.append("coverage_counts")
    if coverage.get("unsafe_executed_branch_ids") != ["ocean_dimod_exact_bqm"]:
        errors.append("unsafe_branch")
    if coverage.get("promotion_blocked_executed_count") != 1:
        errors.append("promotion_blocked_count")
    if coverage.get("all_executed_have_feasibility_check") is not True:
        errors.append("feasibility_checks")
    if not any(row.get("branch_id") == "ocean_dimod_exact_bqm" and row.get("promotion_blocked") is True for row in rows):
        errors.append("ocean_block")
    if not any(row.get("branch_id") == "ortools_knapsack_dynamic_programming" and row.get("promotion_blocked") is False for row in rows):
        errors.append("ortools_safe")
    if any(row.get("status") != "MATCH" for row in artifact.get("measurements", [])):
        errors.append("measurements")
    if any(row.get("status") != "MATCH" for row in artifact.get("flagship_receipts", {}).values()):
        errors.append("flagships")
    if artifact.get("current_promoted_natural_laws") != [] or artifact.get("unsupported_claim_count") != 0:
        errors.append("promotion_boundary")
    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0103ConstraintEncodingReceiptAdapterValidatorRun/v1",
        "pass": "0103",
        "status": status,
        "match": 1 if status == "MATCH" else 0,
        "drift": 0 if status == "MATCH" else 1,
        "checks": [{
            "artifact": "ConstraintEncodingReceiptAdapter",
            "errors": errors,
            "path": "schemas/constraint-encoding-receipt-adapter-pass-0103.json",
            "receipt_count": coverage.get("receipt_count"),
            "unsafe_branch_ids": coverage.get("unsafe_executed_branch_ids"),
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
