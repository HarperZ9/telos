"""Focused tests for pass 0119 Hamiltonian/symplectic receipt."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPOSER = ROOT / "tools" / "compose_hamiltonian_symplectic_receipt.py"
ARTIFACT = ROOT / "schemas" / "hamiltonian-symplectic-receipt-pass-0119.json"


def load_module():
    spec = importlib.util.spec_from_file_location("compose_hamiltonian_symplectic_receipt", COMPOSER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_artifact() -> dict:
    if ARTIFACT.exists():
        return json.loads(ARTIFACT.read_text(encoding="utf-8"))
    return load_module().compose()


def test_hamiltonian_symplectic_shape() -> None:
    artifact = read_artifact()
    cases = artifact["symplectic_cases"]
    negative = artifact["negative_fixtures"][0]

    assert artifact["schema"] == "HamiltonianSymplecticReceipt/v1"
    assert artifact["status"] == "HAMILTONIAN_SYMPLECTIC_MATCH"
    assert artifact["source_bindings"]["formal_target_packaging_pass"] == "0118"
    assert artifact["law_candidate"]["status"] == "LAW_CANDIDATE"
    assert len(cases) == 3
    assert {row["h"] for row in cases} == {"1/3", "1/2", "2/3"}
    assert all(row["status"] == "MATCH" for row in cases)
    assert all(row["determinant"] == "1" for row in cases)
    assert all(row["phase_space_area_preserved"] is True for row in cases)
    assert all(row["symplectic_form_preserved"] is True for row in cases)
    assert all(row["modified_quadratic_invariant_preserved"] is True for row in cases)
    assert all(row["modified_initial"] == row["modified_final"] for row in cases)
    assert any(row["standard_energy_exactly_preserved"] is False for row in cases)

    assert negative["fixture_id"] == "explicit_euler_area_energy_growth"
    assert negative["status"] == "MATCH"
    assert negative["phase_space_area_preserved"] is False
    assert negative["standard_energy_growth"] is True
    assert negative["determinant"] == "10/9"

    assert artifact["source_surface"]["anchor_count"] >= 12
    assert len(artifact["source_surface"]["market_rows"]) == artifact["source_surface"]["anchor_count"]
    assert artifact["unsupported_claim_count"] == 0
    assert artifact["current_promoted_natural_laws"] == []
    assert "does not claim new natural law" in artifact["non_promotion_statement"]
    assert all(row["status"] == "MATCH" for row in artifact["flagship_receipts"].values())


if __name__ == "__main__":
    test_hamiltonian_symplectic_shape()
