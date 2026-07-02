"""Focused tests for pass 0120 Hamiltonian runtime branch receipt."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPOSER = ROOT / "tools" / "compose_hamiltonian_runtime_branch_receipt.py"
ARTIFACT = ROOT / "schemas" / "hamiltonian-runtime-branch-receipt-pass-0120.json"


def load_module():
    spec = importlib.util.spec_from_file_location("compose_hamiltonian_runtime_branch_receipt", COMPOSER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_artifact() -> dict:
    if ARTIFACT.exists():
        return json.loads(ARTIFACT.read_text(encoding="utf-8"))
    return load_module().compose()


def by_id(rows: list[dict], branch_id: str) -> dict:
    return next(row for row in rows if row["branch_id"] == branch_id)


def test_hamiltonian_runtime_branch_shape() -> None:
    artifact = read_artifact()
    branches = artifact["runtime_branches"]
    numpy_rows = [row for row in branches if row["branch_id"].startswith("numpy_float64")]
    scipy_rows = [row for row in branches if row["branch_id"].startswith("scipy_linalg")]
    negative = by_id(branches, "numpy_explicit_euler_negative")

    assert artifact["schema"] == "HamiltonianRuntimeBranchReceipt/v1"
    assert artifact["status"] == "HAMILTONIAN_RUNTIME_BRANCH_MATCH"
    assert artifact["source_bindings"]["hamiltonian_symplectic_pass"] == "0119"
    assert artifact["availability"]["numpy"]["status"] == "AVAILABLE"
    assert artifact["availability"]["scipy"]["status"] == "AVAILABLE"
    assert artifact["availability"]["jax"]["status"] == "MISSING"
    assert artifact["availability"]["buildc"]["status"] == "MISSING"
    assert len(numpy_rows) == 3
    assert len(scipy_rows) == 3
    assert all(row["status"] == "MATCH" for row in numpy_rows + scipy_rows)
    assert all(row["modified_max_abs_drift"] <= row["tolerance"] for row in numpy_rows)
    assert all(row["determinant_abs_drift"] <= row["tolerance"] for row in numpy_rows + scipy_rows)
    assert negative["status"] == "MATCH"
    assert negative["determinant_float64"] > 1.0
    assert negative["energy_growth"] is True
    assert by_id(branches, "jax_runtime_branch")["status"] == "UNAVAILABLE_FENCED"
    assert by_id(branches, "buildlang_runtime_branch")["status"] == "UNAVAILABLE_FENCED"
    assert by_id(branches, "julia_sciml_branch")["status"] == "UNAVAILABLE_FENCED"
    assert artifact["source_surface"]["anchor_count"] >= 4
    assert artifact["unsupported_claim_count"] == 0
    assert artifact["current_promoted_natural_laws"] == []
    assert "does not prove BuildLang" in artifact["non_promotion_statement"]
    assert all(row["status"] == "MATCH" for row in artifact["flagship_receipts"].values())


if __name__ == "__main__":
    test_hamiltonian_runtime_branch_shape()
