"""Validate pass 0086 quantum optimization workflow receipt."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "quantum-optimization-workflow-receipt-pass-0086.json"
RESULT = ROOT / "schemas" / "pass-0086-quantum-optimization-workflow-receipt-validator-result.json"


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
    measurement = artifact.get("measurement", {})
    best = measurement.get("best_feasible", {})
    proof = artifact.get("proof_obligation", {})
    boundary = artifact.get("promotion_boundary", {})
    if artifact.get("schema") != "QuantumOptimizationWorkflowReceipt/v1":
        errors.append("schema")
    if artifact.get("status") != "QUANTUM_OPTIMIZATION_WORKFLOW_RECEIPT_MATCH":
        errors.append("status")
    if seal != sha256_obj(unsealed):
        errors.append("seal")
    if artifact.get("source_binding", {}).get("dominant_cluster_video_count") != 13:
        errors.append("source_binding")
    if measurement.get("candidate_count") != 64 or measurement.get("feasible_count", 0) <= 0 or measurement.get("infeasible_count", 0) <= 0:
        errors.append("candidate_space")
    if best.get("selected") != ["C", "D", "E", "F"] or best.get("value") != 36 or best.get("resource") != 10:
        errors.append("best_solution")
    if proof.get("status") != "MATCH" or proof.get("best_solution_equals_best_qubo_energy") is not True:
        errors.append("proof_obligation")
    if any(boundary.get(key) for key in boundary):
        errors.append("promotion_boundary")
    if any(receipt.get("status") != "MATCH" for receipt in artifact.get("flagship_receipts", {}).values()):
        errors.append("flagship_receipts")
    if artifact.get("unsupported_claim_count") != 0 or artifact.get("current_promoted_natural_laws") != []:
        errors.append("unsupported_claims")
    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0086QuantumOptimizationWorkflowReceiptValidatorRun/v1",
        "pass": "0086",
        "status": status,
        "match": 1 if status == "MATCH" else 0,
        "drift": 0 if status == "MATCH" else 1,
        "checks": [{
            "artifact": "QuantumOptimizationWorkflowReceipt",
            "errors": errors,
            "path": "schemas/quantum-optimization-workflow-receipt-pass-0086.json",
            "candidate_count": measurement.get("candidate_count"),
            "feasible_count": measurement.get("feasible_count"),
            "best_selected": best.get("selected"),
            "best_value": best.get("value"),
            "best_resource": best.get("resource"),
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
