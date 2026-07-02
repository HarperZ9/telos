"""Focused tests for pass 0105 reaction mass-conservation receipt."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPOSER = ROOT / "tools" / "compose_reaction_mass_conservation_receipt.py"
ARTIFACT = ROOT / "schemas" / "reaction-mass-conservation-receipt-pass-0105.json"


def load_module():
    spec = importlib.util.spec_from_file_location("compose_reaction_mass_conservation_receipt", COMPOSER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_artifact() -> dict:
    if ARTIFACT.exists():
        return json.loads(ARTIFACT.read_text(encoding="utf-8"))
    return load_module().compose()


def test_reaction_mass_conservation_receipt_shape() -> None:
    artifact = read_artifact()
    proof = artifact["proof"]
    probe = artifact["numerical_probe"]
    negative = artifact["negative_fixture"]
    assert artifact["schema"] == "ReactionMassConservationReceipt/v1"
    assert artifact["status"] == "REACTION_MASS_CONSERVATION_RECEIPT_MATCH"
    assert artifact["source_bindings"]["ai4science_pass"] == "0104"
    assert artifact["reaction"]["stoichiometry"] == {"A": -1, "B": 1}
    assert proof["symbolic_derivative_total"] == "0"
    assert proof["invariant"] == "A+B"
    assert probe["grid_points"] >= 80
    assert probe["max_exact_invariant_drift"] <= 1e-12
    assert probe["max_euler_invariant_drift"] <= 1e-10
    assert negative["status"] == "DRIFT_EXPECTED"
    assert negative["breaks_invariant"] is True
    assert artifact["law_candidate"]["status"] == "LAW_CANDIDATE"
    assert artifact["unsupported_claim_count"] == 0
    assert artifact["current_promoted_natural_laws"] == []


if __name__ == "__main__":
    test_reaction_mass_conservation_receipt_shape()
