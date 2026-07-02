"""Focused tests for pass 0126 source-lead demotion gate."""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "tools" / "compose_source_lead_demotion_gate.py"


def load_module():
    spec = importlib.util.spec_from_file_location("compose_source_lead_demotion_gate", MODULE)
    if spec is None or spec.loader is None:
        raise AssertionError("module spec unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_source_lead_demotion_gate() -> None:
    module = load_module()
    artifact = module.compose()
    fixtures = {row["fixture_id"]: row for row in artifact["gate_fixtures"]}

    assert artifact["schema"] == "SourceLeadDemotionGateReceipt/v1"
    assert artifact["status"] == "SOURCE_LEAD_DEMOTION_GATE_MATCH"
    assert artifact["source_bindings"]["youtube_router_pass"] == "0125"
    assert artifact["accepted_count"] == 3
    assert artifact["rejected_count"] == 4
    assert all(row["matches_expected"] for row in artifact["gate_fixtures"])
    assert fixtures["source_lead_only_ok"]["gate_status"] == "ACCEPTED"
    assert fixtures["hypothesis_routing_ok"]["gate_status"] == "ACCEPTED"
    assert fixtures["independent_probe_ok"]["gate_status"] == "ACCEPTED"
    assert "video_only_promotion" in fixtures["video_only_fact_rejected"]["failures"]
    assert "law_promotion_forbidden" in fixtures["video_law_rejected"]["failures"]
    assert "raw_transcript_included" in fixtures["raw_transcript_rejected"]["failures"]
    assert "keyword_count_not_proof" in fixtures["keyword_count_as_proof_rejected"]["failures"]
    assert artifact["unsupported_claim_count"] == 0
    assert artifact["current_promoted_natural_laws"] == []


if __name__ == "__main__":
    test_source_lead_demotion_gate()
