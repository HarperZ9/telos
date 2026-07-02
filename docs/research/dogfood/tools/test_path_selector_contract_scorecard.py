"""Focused tests for pass 0077 path-selector contract scorecard."""
from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMPOSER = ROOT / "tools" / "compose_path_selector_contract_scorecard.py"


def load_composer():
    spec = importlib.util.spec_from_file_location("compose_path_selector_contract_scorecard", COMPOSER)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_path_selector_contract_scorecard_shape() -> None:
    module = load_composer()
    artifact = module.compose()
    motions = artifact["product_motions"]

    assert artifact["schema"] == "PathSelectorContractGrowthScorecard/v1"
    assert artifact["pass"] == "0077"
    assert artifact["status"] == "PATH_SELECTOR_CONTRACT_SCORECARD_MATCH"
    assert artifact["contract"]["schema"] == "IndexPathSelectorReceipt/v1"
    assert len(artifact["evidence"]) >= 8
    assert len(artifact["growth_vectors"]) >= 5
    assert len(motions) == 3
    assert motions[0]["id"] == artifact["primary_30_day_push"]["motion"]
    assert all(row["uniqueness_status"] == "hypothesis" for row in motions)
    assert artifact["unsupported_claim_count"] == 0
    assert artifact["current_promoted_natural_laws"] == []


if __name__ == "__main__":
    test_path_selector_contract_scorecard_shape()
