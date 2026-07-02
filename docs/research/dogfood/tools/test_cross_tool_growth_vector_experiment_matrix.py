"""Focused tests for pass 0082 cross-tool growth-vector experiment matrix."""
from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMPOSER = ROOT / "tools" / "compose_cross_tool_growth_vector_experiment_matrix.py"


def load_composer():
    spec = importlib.util.spec_from_file_location("compose_cross_tool_growth_vector_experiment_matrix", COMPOSER)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_cross_tool_growth_vector_experiment_matrix_shape() -> None:
    module = load_composer()
    artifact = module.compose()

    assert artifact["schema"] == "CrossToolGrowthVectorExperimentMatrix/v1"
    assert artifact["pass"] == "0082"
    assert artifact["status"] == "CROSS_TOOL_GROWTH_VECTOR_EXPERIMENT_MATRIX_MATCH"
    assert artifact["promotion_state"] == "EXPERIMENT_MATRIX_NOT_MARKET_PROOF"
    assert artifact["unsupported_claim_count"] == 0
    assert artifact["current_promoted_natural_laws"] == []

    assert len(artifact["live_forum_routes"]) >= 8
    assert all(route["status"] == "MATCH" for route in artifact["live_forum_routes"])
    assert artifact["live_experiment_summary"]["route_probe_count"] == len(artifact["live_forum_routes"])
    assert artifact["live_experiment_summary"]["needs_escalation_count"] >= 1

    required_tools = set(module.TOOLS)
    assert {row["tool"] for row in artifact["tool_improvements"]} == required_tools
    assert len(artifact["ranked_product_lanes"]) >= 8
    for lane in artifact["ranked_product_lanes"]:
        assert set(lane["tools"]).issubset(required_tools)
        assert lane["claim_status"] == "hypothesis"
        assert lane["gap_status"] == "inferred"
        assert 1 <= lane["scores"]["composite"] <= 5
        assert lane["next_experiment"]
        assert lane["falsifier"]

    assert "buildlang_demo_0080" in artifact["prior_bindings"]
    assert "visual_truth_0081" in artifact["prior_bindings"]
    assert len(artifact["negative_fixtures"]) >= 8


if __name__ == "__main__":
    test_cross_tool_growth_vector_experiment_matrix_shape()
