"""Validate pass 0090 solver availability matrix receipt."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "solver-availability-matrix-receipt-pass-0090.json"
RESULT = ROOT / "schemas" / "pass-0090-solver-availability-matrix-receipt-validator-result.json"


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
    rows = {row.get("row_id"): row for row in artifact.get("matrix_rows", [])}
    boundary = artifact.get("promotion_boundary", {})
    if artifact.get("schema") != "SolverAvailabilityMatrixReceipt/v1":
        errors.append("schema")
    if artifact.get("status") != "SOLVER_AVAILABILITY_MATRIX_RECEIPT_MATCH":
        errors.append("status")
    if seal != sha256_obj(unsealed):
        errors.append("seal")
    if artifact.get("prior_binding", {}).get("source_pass") != "0089":
        errors.append("prior_binding")
    if artifact.get("summary", {}).get("row_count", 0) < 24:
        errors.append("row_count")
    if artifact.get("summary", {}).get("local_available_rows", 0) + artifact.get("summary", {}).get("local_unavailable_rows", 0) != artifact.get("summary", {}).get("row_count", -1):
        errors.append("summary_counts")
    if not artifact.get("package_receipts", {}).get("scipy", {}).get("available"):
        errors.append("scipy")
    if artifact.get("package_receipts", {}).get("ortools", {}).get("available") is not False:
        errors.append("ortools")
    if artifact.get("package_receipts", {}).get("dwave_system", {}).get("available") is not False:
        errors.append("dwave")
    if artifact.get("buildc_corpus_receipt", {}).get("status") != "MATCH":
        errors.append("buildc")
    for row_id in ["buildlang_buildc", "build_universe", "scipy", "ortools", "networkx"]:
        if row_id not in rows:
            errors.append(f"missing_{row_id}")
    if any(receipt.get("status") != "MATCH" for receipt in artifact.get("flagship_receipts", {}).values()):
        errors.append("flagship_receipts")
    if any(boundary.get(key) for key in ["solver_superiority_claim", "world_problem_solved_claim", "new_natural_law_claim"]):
        errors.append("promotion_boundary")
    if artifact.get("unsupported_claim_count") != 0 or artifact.get("current_promoted_natural_laws") != []:
        errors.append("unsupported_claims")
    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0090SolverAvailabilityMatrixReceiptValidatorRun/v1",
        "pass": "0090",
        "status": status,
        "match": 1 if status == "MATCH" else 0,
        "drift": 0 if status == "MATCH" else 1,
        "checks": [{
            "artifact": "SolverAvailabilityMatrixReceipt",
            "errors": errors,
            "path": "schemas/solver-availability-matrix-receipt-pass-0090.json",
            "row_count": artifact.get("summary", {}).get("row_count"),
            "local_available_rows": artifact.get("summary", {}).get("local_available_rows"),
            "local_unavailable_rows": artifact.get("summary", {}).get("local_unavailable_rows"),
            "buildc_status": artifact.get("buildc_corpus_receipt", {}).get("status"),
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
