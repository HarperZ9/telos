"""Focused tests for pass 0106 stoichiometric invariant checker receipt."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPOSER = ROOT / "tools" / "compose_stoichiometric_invariant_checker_receipt.py"
ARTIFACT = ROOT / "schemas" / "stoichiometric-invariant-checker-receipt-pass-0106.json"


def load_module():
    spec = importlib.util.spec_from_file_location("compose_stoichiometric_invariant_checker_receipt", COMPOSER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_artifact() -> dict:
    if ARTIFACT.exists():
        return json.loads(ARTIFACT.read_text(encoding="utf-8"))
    return load_module().compose()


def test_stoichiometric_invariant_checker_receipt_shape() -> None:
    artifact = read_artifact()
    network = artifact["closed_network"]
    derived = artifact["derived_conservation_vectors"]
    vector = derived[0]
    probe = artifact["numerical_probe"]
    negative = artifact["negative_network"]
    youtube = artifact["youtube_signal_binding"]
    assert artifact["schema"] == "StoichiometricInvariantCheckerReceipt/v1"
    assert artifact["status"] == "STOICHIOMETRIC_INVARIANT_CHECKER_RECEIPT_MATCH"
    assert artifact["source_bindings"]["reaction_pass"] == "0105"
    assert artifact["source_bindings"]["ai4science_pass"] == "0104"
    assert youtube["roadmap_pass"] == "0102"
    assert youtube["youtube_pass"] == "0085"
    assert youtube["ai4science_video_count"] >= 1
    assert youtube["buildlang_scientific_runtime_video_count"] >= 10
    assert network["species"] == ["A", "B", "C"]
    assert len(network["reactions"]) == 3
    assert vector["vector"] == [1, 1, 1]
    assert vector["invariant"] == "A+B+C"
    assert vector["residual"] == [0, 0, 0]
    assert probe["grid_points"] >= 150
    assert probe["max_total_drift"] <= 1e-10
    assert negative["status"] == "DRIFT_EXPECTED"
    assert negative["candidate_residual"] != [0, 0, 0, 0]
    assert negative["breaks_invariant"] is True
    assert negative["max_total_drift"] > 0.01
    assert artifact["law_candidate"]["status"] == "LAW_CANDIDATE"
    assert artifact["unsupported_claim_count"] == 0
    assert artifact["current_promoted_natural_laws"] == []


if __name__ == "__main__":
    test_stoichiometric_invariant_checker_receipt_shape()
