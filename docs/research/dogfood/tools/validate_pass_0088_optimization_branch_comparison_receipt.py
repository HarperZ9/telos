"""Validate pass 0088 optimization branch comparison receipt."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "optimization-branch-comparison-receipt-pass-0088.json"
RESULT = ROOT / "schemas" / "pass-0088-optimization-branch-comparison-receipt-validator-result.json"


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
    exact = artifact.get("exact_branch", {})
    summary = artifact.get("comparison_summary", {})
    boundary = artifact.get("promotion_boundary", {})
    if artifact.get("schema") != "OptimizationBranchComparisonReceipt/v1":
        errors.append("schema")
    if artifact.get("status") != "OPTIMIZATION_BRANCH_COMPARISON_RECEIPT_MATCH":
        errors.append("status")
    if seal != sha256_obj(unsealed):
        errors.append("seal")
    if artifact.get("prior_binding", {}).get("source_pass") != "0087":
        errors.append("prior_binding")
    upstream = artifact.get("upstream_research_binding", {})
    if upstream.get("source_pass") != "0085" or upstream.get("dominant_cluster") != "enterprise_quantum_optimization":
        errors.append("upstream_research_binding")
    if exact.get("candidate_count") != 4096 or exact.get("best", {}).get("feasible") is not True:
        errors.append("exact_branch")
    if len(artifact.get("branches", [])) != 3 or len(artifact.get("comparisons", [])) != 3:
        errors.append("branches")
    if any(row.get("exact_value_gap", -1) < 0 for row in artifact.get("comparisons", [])):
        errors.append("comparison_gap")
    if not summary.get("exact_hit_branches"):
        errors.append("exact_hits")
    if len(artifact.get("source_anchors", [])) < 4:
        errors.append("source_anchors")
    if any(boundary.get(key) for key in ["solver_superiority_claim", "quantum_hardware_claim", "quantum_advantage_claim", "new_natural_law_claim"]):
        errors.append("promotion_boundary")
    if any(receipt.get("status") != "MATCH" for receipt in artifact.get("flagship_receipts", {}).values()):
        errors.append("flagship_receipts")
    if artifact.get("unsupported_claim_count") != 0 or artifact.get("current_promoted_natural_laws") != []:
        errors.append("unsupported_claims")
    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0088OptimizationBranchComparisonReceiptValidatorRun/v1",
        "pass": "0088",
        "status": status,
        "match": 1 if status == "MATCH" else 0,
        "drift": 0 if status == "MATCH" else 1,
        "checks": [{
            "artifact": "OptimizationBranchComparisonReceipt",
            "errors": errors,
            "path": "schemas/optimization-branch-comparison-receipt-pass-0088.json",
            "candidate_count": exact.get("candidate_count"),
            "exact_value": exact.get("best", {}).get("value"),
            "branch_count": summary.get("branch_count"),
            "exact_hit_branches": summary.get("exact_hit_branches"),
            "max_value_gap": summary.get("max_value_gap"),
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
