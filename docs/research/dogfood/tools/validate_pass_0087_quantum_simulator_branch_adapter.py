"""Validate pass 0087 quantum simulator branch adapter."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "quantum-simulator-branch-adapter-pass-0087.json"
RESULT = ROOT / "schemas" / "pass-0087-quantum-simulator-branch-adapter-validator-result.json"


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
    sim = artifact.get("simulator_branch", {})
    comparison = artifact.get("comparison_to_exact", {})
    boundary = artifact.get("promotion_boundary", {})
    if artifact.get("schema") != "QuantumSimulatorBranchAdapterReceipt/v1":
        errors.append("schema")
    if artifact.get("status") != "QUANTUM_SIMULATOR_BRANCH_ADAPTER_MATCH":
        errors.append("status")
    if seal != sha256_obj(unsealed):
        errors.append("seal")
    if artifact.get("baseline_binding", {}).get("source_pass") != "0086":
        errors.append("baseline_binding")
    if sim.get("run_count") != 32 or sim.get("optimum_hit_count", 0) <= 0 or sim.get("best_feasible_count", 0) <= 0:
        errors.append("run_distribution")
    if sim.get("runs_sha256") != sha256_obj(sim.get("runs", [])):
        errors.append("run_digest")
    if comparison.get("status") != "MATCH" or comparison.get("exact_best_bits") != comparison.get("simulator_best_bits"):
        errors.append("baseline_comparison")
    if len(sim.get("source_anchors", [])) < 2:
        errors.append("source_anchors")
    if any(boundary.get(key) for key in ["quantum_hardware_claim", "quantum_advantage_claim", "new_physics_claim", "new_natural_law_claim"]):
        errors.append("promotion_boundary")
    if any(receipt.get("status") != "MATCH" for receipt in artifact.get("flagship_receipts", {}).values()):
        errors.append("flagship_receipts")
    if artifact.get("unsupported_claim_count") != 0 or artifact.get("current_promoted_natural_laws") != []:
        errors.append("unsupported_claims")
    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0087QuantumSimulatorBranchAdapterValidatorRun/v1",
        "pass": "0087",
        "status": status,
        "match": 1 if status == "MATCH" else 0,
        "drift": 0 if status == "MATCH" else 1,
        "checks": [{
            "artifact": "QuantumSimulatorBranchAdapterReceipt",
            "errors": errors,
            "path": "schemas/quantum-simulator-branch-adapter-pass-0087.json",
            "run_count": sim.get("run_count"),
            "optimum_hit_count": sim.get("optimum_hit_count"),
            "constraint_violation_rate": sim.get("constraint_violation_rate"),
            "comparison_status": comparison.get("status"),
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
