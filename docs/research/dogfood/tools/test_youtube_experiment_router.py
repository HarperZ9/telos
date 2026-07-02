"""Focused tests for pass 0125 YouTube experiment router."""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "tools" / "compose_youtube_experiment_router.py"


def load_module():
    spec = importlib.util.spec_from_file_location("compose_youtube_experiment_router", MODULE)
    if spec is None or spec.loader is None:
        raise AssertionError("module spec unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_youtube_experiment_router() -> None:
    module = load_module()
    artifact = module.compose()
    leads = artifact["youtube_source_leads"]
    experiments = artifact["routed_experiments"]

    assert artifact["schema"] == "YoutubeExperimentRouterReceipt/v1"
    assert artifact["status"] == "YOUTUBE_EXPERIMENT_ROUTER_MATCH"
    assert len(leads) == 4
    assert {row["video_id"] for row in leads} == set(module.VIDEOS)
    assert all(row["claim_status"] == "SOURCE_LEAD_ONLY" for row in leads)
    assert all(row["raw_transcript_included"] is False for row in leads)
    assert all(row["transcript_object_present"] for row in leads)
    assert len(experiments) >= 6
    assert all(row["claim_status"] == "HYPOTHESIS" for row in experiments)
    assert experiments[0]["experiment_id"] in {"cross_field_scientific_runtime_router", "source_lead_demotion_gate"}
    assert artifact["upstream_receipts"]["youtube_growth"]["pass"] == "0121"
    assert artifact["upstream_receipts"]["field_factory"]["pass"] == "0123"
    assert artifact["upstream_receipts"]["agent_action_adapter"]["pass"] == "0124"
    assert artifact["unsupported_claim_count"] == 0
    assert artifact["current_promoted_natural_laws"] == []


if __name__ == "__main__":
    test_youtube_experiment_router()
