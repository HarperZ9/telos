"""Validate pass 0114 multi-domain constrained optimization suite."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "multi-domain-constrained-optimization-suite-pass-0114.json"
RESULT = ROOT / "schemas" / "pass-0114-multi-domain-constrained-optimization-validator-result.json"


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
    unsealed = dict(artifact)
    seal = unsealed.pop("seal", None)
    rows = artifact.get("cases", [])
    by_id = {row.get("case_id"): row for row in rows}
    y = artifact.get("youtube_binding", {})
    coverage = artifact.get("domain_coverage", {})
    errors: list[str] = []

    if artifact.get("schema") != "MultiDomainConstrainedOptimizationSuiteReceipt/v1":
        errors.append("schema")
    if artifact.get("status") != "MULTI_DOMAIN_CONSTRAINED_OPTIMIZATION_SUITE_MATCH":
        errors.append("status")
    if seal != sha256_obj(unsealed):
        errors.append("seal")
    if artifact.get("source_bindings", {}).get("mpc_pass") != "0113":
        errors.append("mpc_pass")
    if artifact.get("source_bindings", {}).get("youtube_roadmap_pass") != "0102":
        errors.append("youtube_roadmap_pass")
    if len(rows) != 4 or any(row.get("classification") != "MATCH" for row in rows):
        errors.append("case_count")
    if by_id.get("warehouse_capacity_assignment", {}).get("negative_fixture", {}).get("classification") != "CAPACITY_VIOLATION_EXPECTED":
        errors.append("warehouse")
    if by_id.get("robotics_quality_inspection", {}).get("negative_fixture", {}).get("classification") != "COVERAGE_VIOLATION_EXPECTED":
        errors.append("robotics")
    if by_id.get("safety_allocation_toy", {}).get("negative_fixture", {}).get("classification") != "INFEASIBLE_EXPECTED":
        errors.append("safety")
    if by_id.get("quant_risk_budget", {}).get("negative_fixture", {}).get("classification") != "RISK_BUDGET_VIOLATION_EXPECTED":
        errors.append("quant")
    if by_id.get("quant_risk_budget", {}).get("objective") != "9/2":
        errors.append("quant_objective")
    if coverage.get("case_count") != 4 or coverage.get("youtube_cluster_count", 0) < 3:
        errors.append("coverage")
    if artifact.get("market_surface", {}).get("tool_count", 0) < 10:
        errors.append("market")
    if y.get("valid_video_count") != 19 or y.get("dominant_cluster_video_count") != 13:
        errors.append("youtube")
    if any(row.get("status") != "MATCH" for row in artifact.get("measurements", [])):
        errors.append("measurements")
    if any(row.get("status") != "MATCH" for row in artifact.get("flagship_receipts", {}).values()):
        errors.append("flagships")
    if artifact.get("unsupported_claim_count") != 0 or artifact.get("current_promoted_natural_laws") != []:
        errors.append("promotion_boundary")

    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0114MultiDomainConstrainedOptimizationValidatorRun/v1",
        "pass": "0114",
        "status": status,
        "match": 1 if status == "MATCH" else 0,
        "drift": 0 if status == "MATCH" else 1,
        "checks": [{
            "artifact": "MultiDomainConstrainedOptimizationSuiteReceipt",
            "case_count": len(rows),
            "errors": errors,
            "path": "schemas/multi-domain-constrained-optimization-suite-pass-0114.json",
            "youtube_cluster_count": coverage.get("youtube_cluster_count"),
            "market_tool_count": artifact.get("market_surface", {}).get("tool_count"),
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
