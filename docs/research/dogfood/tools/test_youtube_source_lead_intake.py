"""Focused tests for pass 0133 YouTube source-lead intake."""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "tools" / "compose_youtube_source_lead_intake.py"


def load_module():
    spec = importlib.util.spec_from_file_location("compose_youtube_source_lead_intake", MODULE)
    if spec is None or spec.loader is None:
        raise AssertionError("module spec unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_youtube_source_lead_intake() -> None:
    module = load_module()
    artifact = module.compose()
    routes = {row["route"] for row in artifact["route_summary"]}

    assert artifact["schema"] == "YouTubeSourceLeadIntakeReceipt/v1"
    assert artifact["status"] == "YOUTUBE_SOURCE_LEAD_INTAKE_MATCH"
    assert artifact["source_bindings"]["proof_transfer_pass"] == "0132"
    assert len(artifact["source_receipts"]) >= 19
    assert all(row["raw_body_exported"] is False for row in artifact["source_receipts"])
    assert len(artifact["video_leads"]) >= 9
    assert all(row["status"] == "SOURCE_LEAD_ONLY" for row in artifact["video_leads"])
    assert "biology_evolution_geometry" in routes
    assert "theoretical_computing_breakthrough" in routes
    assert all(row["status"] == "REJECTED" for row in artifact["negative_fixtures"])
    assert artifact["current_promoted_natural_laws"] == []


if __name__ == "__main__":
    test_youtube_source_lead_intake()
