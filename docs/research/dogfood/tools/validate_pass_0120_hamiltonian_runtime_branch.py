"""Validate pass 0120 Hamiltonian runtime branch receipt."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "hamiltonian-runtime-branch-receipt-pass-0120.json"
RESULT = ROOT / "schemas" / "pass-0120-hamiltonian-runtime-branch-validator-result.json"


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)


def sha256_obj(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n", encoding="utf-8")


def require(condition: bool, errors: list[str], label: str) -> None:
    if not condition:
        errors.append(label)


def branch(rows: list[dict], branch_id: str) -> dict:
    return next((row for row in rows if row.get("branch_id") == branch_id), {})


def validate() -> dict:
    artifact = read_json(ARTIFACT)
    unsealed = dict(artifact)
    seal = unsealed.pop("seal", None)
    branches = artifact.get("runtime_branches", [])
    numpy_rows = [row for row in branches if str(row.get("branch_id", "")).startswith("numpy_float64")]
    scipy_rows = [row for row in branches if str(row.get("branch_id", "")).startswith("scipy_linalg")]
    negative = branch(branches, "numpy_explicit_euler_negative")
    errors: list[str] = []

    require(artifact.get("schema") == "HamiltonianRuntimeBranchReceipt/v1", errors, "schema")
    require(artifact.get("status") == "HAMILTONIAN_RUNTIME_BRANCH_MATCH", errors, "status")
    require(seal == sha256_obj(unsealed), errors, "seal")
    require(artifact.get("source_bindings", {}).get("hamiltonian_symplectic_pass") == "0119", errors, "source_binding")
    require(artifact.get("availability", {}).get("numpy", {}).get("status") == "AVAILABLE", errors, "numpy_available")
    require(artifact.get("availability", {}).get("scipy", {}).get("status") == "AVAILABLE", errors, "scipy_available")
    require(len(numpy_rows) == 3, errors, "numpy_count")
    require(len(scipy_rows) == 3, errors, "scipy_count")
    require(all(row.get("status") == "MATCH" for row in numpy_rows + scipy_rows), errors, "runtime_match")
    require(all(float(row.get("modified_max_abs_drift", 0.0)) <= float(row.get("tolerance", 0.0)) for row in numpy_rows), errors, "numpy_modified_drift")
    require(all(float(row.get("determinant_abs_drift", 0.0)) <= float(row.get("tolerance", 0.0)) for row in numpy_rows + scipy_rows), errors, "determinant_drift")
    require(negative.get("status") == "MATCH", errors, "negative_status")
    require(float(negative.get("determinant_float64", 0.0)) > 1.0, errors, "negative_determinant")
    require(negative.get("energy_growth") is True, errors, "negative_energy")
    require(branch(branches, "jax_runtime_branch").get("status") == "UNAVAILABLE_FENCED", errors, "jax_fence")
    require(branch(branches, "buildlang_runtime_branch").get("status") == "UNAVAILABLE_FENCED", errors, "buildlang_fence")
    require(branch(branches, "julia_sciml_branch").get("status") == "UNAVAILABLE_FENCED", errors, "julia_fence")
    require(artifact.get("source_surface", {}).get("anchor_count", 0) >= 4, errors, "source_anchors")
    require(artifact.get("unsupported_claim_count") == 0, errors, "unsupported_claim_count")
    require(artifact.get("current_promoted_natural_laws") == [], errors, "natural_laws")
    require(all(row.get("status") == "MATCH" for row in artifact.get("flagship_receipts", {}).values()), errors, "flagships")

    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0120HamiltonianRuntimeBranchValidatorRun/v1",
        "pass": "0120",
        "status": status,
        "match": 1 if status == "MATCH" else 0,
        "drift": 0 if status == "MATCH" else 1,
        "checks": [{"artifact": "HamiltonianRuntimeBranchReceipt", "branch_count": len(branches), "errors": errors, "status": status}],
    }


def main() -> None:
    result = validate()
    write_json(RESULT, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
