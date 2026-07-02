"""Focused tests for pass 0066 tool growth-vector experiment matrix."""
from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMPOSER = ROOT / "tools" / "compose_tool_growth_vector_experiment_matrix.py"


def load_composer():
    spec = importlib.util.spec_from_file_location("compose_tool_growth_vector_experiment_matrix", COMPOSER)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_tool_growth_vector_experiment_matrix_shape() -> None:
    module = load_composer()
    packet = module.compose()

    assert packet["schema"] == "ToolGrowthVectorExperimentMatrix/v1"
    assert packet["pass"] == "0066"
    assert packet["status"] == "TOOL_GROWTH_VECTOR_EXPERIMENT_MATRIX_MATCH"
    assert packet["unsupported_claim_count"] == 0
    assert packet["promotion_state"] == "EXPERIMENT_MATRIX_NOT_MARKET_PROOF"

    required_tools = {
        "Gather",
        "Index",
        "Forum",
        "Crucible",
        "Telos",
        "BuildLang/buildc",
        "build-universe",
        "color calibration",
        "browser evidence",
        "model foundry",
        "loop ledger",
        "action receipts",
    }
    assert required_tools == {tool["tool"] for tool in packet["internal_tools"]}
    assert len(packet["source_anchors"]) >= 12
    assert len(packet["growth_vectors"]) >= 36
    assert len(packet["cross_tool_experiments"]) >= 10

    source_ids = {source["source_id"] for source in packet["source_anchors"]}
    for vector in packet["growth_vectors"]:
        assert vector["tool"] in required_tools
        assert set(vector["source_ids"]).issubset(source_ids)
        assert vector["claim_status"] == "hypothesis"
        assert vector["gap_status"] in {"inferred", "verified", "unverified"}
        assert 1 <= vector["priority_score"] <= 5
        assert vector["success_metric"]
        assert vector["falsifier"]

    for experiment in packet["cross_tool_experiments"]:
        assert set(experiment["tools"]).issubset(required_tools)
        assert len(experiment["tools"]) >= 2
        assert experiment["expected_receipt"]
        assert experiment["falsifier"]

    centrality = packet["synergy_graph"]["centrality"]
    assert centrality["Telos"] >= 6
    assert centrality["Crucible"] >= 6
    assert packet["top_growth_bundles"][0]["bundle_id"] == "proof_os_core"
    assert packet["previous_pass_binding"]["pass"] == "0065"


if __name__ == "__main__":
    test_tool_growth_vector_experiment_matrix_shape()
