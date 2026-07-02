"""Validate pass 0094 quantum optimization workflow receipt."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "quantum-optimization-workflow-receipt-pass-0094.json"
RESULT = ROOT / "schemas" / "pass-0094-quantum-optimization-workflow-receipt-validator-result.json"


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
    workflow = artifact.get("workflow", {})
    branches = workflow.get("solver_branches", {})
    objective = workflow.get("objective_measurements", {})
    if artifact.get("schema") != "QuantumOptimizationWorkflowReceipt/v1":
        errors.append("schema")
    if artifact.get("status") != "QUANTUM_OPTIMIZATION_WORKFLOW_RECEIPT_MATCH":
        errors.append("status")
    if seal != sha256_obj(unsealed):
        errors.append("seal")
    if artifact.get("source_binding", {}).get("dominant_cluster_video_count") != 13:
        errors.append("source_binding")
    if workflow.get("problem", {}).get("capacity") != 29 or objective.get("exact_value") != 162:
        errors.append("objective")
    if branches.get("networkx_capacity_dag_longest_path", {}).get("value") != 162:
        errors.append("networkx")
    if branches.get("ortools_knapsack", {}).get("status") != "NOT_EXECUTED_DEPENDENCY_MISSING":
        errors.append("ortools_boundary")
    if branches.get("dwave_ocean_sampler", {}).get("status") != "NOT_EXECUTED_DEPENDENCY_MISSING":
        errors.append("dwave_boundary")
    if artifact.get("buildlang_binding", {}).get("verify_check_count") != 18:
        errors.append("buildlang")
    if len(artifact.get("measurements", [])) != 10 or any(row.get("status") != "MATCH" for row in artifact.get("measurements", [])):
        errors.append("measurements")
    if any(tool.get("status") != "MATCH" for tool in artifact.get("flagship_receipts", {}).values()):
        errors.append("flagships")
    if artifact.get("unsupported_claim_count") != 0 or artifact.get("current_promoted_natural_laws") != []:
        errors.append("promotion_boundary")
    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0094QuantumOptimizationWorkflowReceiptValidatorRun/v1",
        "pass": "0094",
        "status": status,
        "match": 1 if status == "MATCH" else 0,
        "drift": 0 if status == "MATCH" else 1,
        "checks": [{
            "artifact": "QuantumOptimizationWorkflowReceipt",
            "errors": errors,
            "path": "schemas/quantum-optimization-workflow-receipt-pass-0094.json",
            "exact_value": objective.get("exact_value"),
            "networkx_value": branches.get("networkx_capacity_dag_longest_path", {}).get("value"),
            "buildc_verify_check_count": artifact.get("buildlang_binding", {}).get("verify_check_count"),
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
