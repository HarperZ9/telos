"""Focused tests for pass 0063 frontier problem-to-proof opportunity map."""
from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMPOSER = ROOT / "tools" / "compose_frontier_problem_to_proof_opportunity_map.py"


def load_composer():
    spec = importlib.util.spec_from_file_location("compose_frontier_problem_to_proof_opportunity_map", COMPOSER)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_frontier_problem_to_proof_opportunity_map_shape() -> None:
    module = load_composer()
    packet = module.compose()

    assert packet["schema"] == "FrontierProblemToProofOpportunityMap/v1"
    assert packet["pass"] == "0063"
    assert packet["status"] == "FRONTIER_PROBLEM_TO_PROOF_OPPORTUNITY_MAP_MATCH"
    assert packet["unsupported_uniqueness_claim_count"] == 0
    assert packet["current_promoted_natural_laws"] == []

    source_ids = {row["source_id"] for row in packet["source_anchors"]}
    assert len(source_ids) >= 16

    required_domains = {
        "formal_math_theoretical_cs",
        "agentic_ai4science",
        "quantum_hpc_algorithms",
        "biology_protein_drug_discovery",
        "materials_climate_energy",
        "buildlang_scientific_runtime",
        "agent_observability_action_receipts",
        "color_rendering_calibration",
    }
    domain_ids = {row["domain_id"] for row in packet["opportunity_rows"]}
    assert required_domains.issubset(domain_ids)

    for row in packet["opportunity_rows"]:
        assert set(row["source_ids"]).issubset(source_ids)
        assert row["gap_status"] in {"verified", "inferred", "unverified"}
        assert row["uniqueness_claim_status"] == "hypothesis"
        assert row["source_ids"]
        assert row["buyer"]
        assert row["primary_wedge_hypothesis"].startswith("Hypothesis:")
        assert row["proof_demo"]

    score_markets = {row["market"] for row in packet["wedge_scores"]}
    assert score_markets == domain_ids
    for score in packet["wedge_scores"]:
        for key in ("urgency", "budget", "differentiation", "feasibility", "proof_demo_readiness", "risk"):
            assert 1 <= score[key] <= 5
        assert score["weighted_total"] > 0

    nodes = {node["internal_tool"] for node in packet["megatool_nodes"]}
    for tool in (
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
    ):
        assert tool in nodes

    for node in packet["megatool_nodes"]:
        assert node["already_exists_state"] in {"present", "partial", "source_lead"}
        assert node["needed_integration"]
        assert node["market_facing_product"]

    assert len(packet["demo_recommendations"]) == 3
    assert all(demo["promotion_state"] == "DEMO_NOT_PRODUCT_MARKET_FIT" for demo in packet["demo_recommendations"])
    assert packet["forum_route_observation"]["status"] in {"MATCH", "ESCALATED", "UNVERIFIABLE"}


if __name__ == "__main__":
    test_frontier_problem_to_proof_opportunity_map_shape()
