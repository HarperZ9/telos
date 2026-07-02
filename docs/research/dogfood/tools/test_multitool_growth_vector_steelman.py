"""Focused tests for pass 0068 multi-tool growth-vector steelman."""
from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMPOSER = ROOT / "tools" / "compose_multitool_growth_vector_steelman.py"


def load_composer():
    spec = importlib.util.spec_from_file_location("compose_multitool_growth_vector_steelman", COMPOSER)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_multitool_growth_vector_steelman_shape() -> None:
    module = load_composer()
    artifact = module.compose()
    required_tools = set(module.TOOLS)
    source_ids = {source["source_id"] for source in artifact["source_anchors"]}

    assert artifact["schema"] == "MultiToolGrowthVectorSteelman/v1"
    assert artifact["pass"] == "0068"
    assert artifact["status"] == "MULTITOOL_GROWTH_VECTOR_STEELMAN_MATCH"
    assert artifact["unsupported_claim_count"] == 0
    assert len(artifact["source_anchors"]) >= 16
    assert {row["tool"] for row in artifact["tool_rows"]} == required_tools
    assert len(artifact["synergy_edges"]) >= 15
    assert len(artifact["steelman_objections"]) >= 8
    assert len(artifact["experiment_queue"]) >= 12

    for row in artifact["tool_rows"]:
        assert row["claim_status"] == "hypothesis"
        assert row["gap_status"] == "inferred"
        assert set(row["source_ids"]).issubset(source_ids)
        assert row["primary_experiment"].startswith("p0068-")
        assert row["success_metric"]
        assert row["falsifier"]
        assert 1 <= row["scores"]["priority"] <= 5

    assert {row["pass"] for row in artifact["previous_pass_bindings"]} == {"0066", "0067"}
    assert artifact["tool_rows"][0]["scores"]["priority"] >= artifact["tool_rows"][-1]["scores"]["priority"]


if __name__ == "__main__":
    test_multitool_growth_vector_steelman_shape()
