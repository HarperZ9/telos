"""Focused tests for pass 0140 research archive substrate atlas."""
from __future__ import annotations

import importlib.util
from pathlib import Path

MODULE = Path(__file__).with_name("compose_research_archive_substrate_atlas.py")
spec = importlib.util.spec_from_file_location("compose_research_archive_substrate_atlas", MODULE)
mod = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(mod)


def test_catalog_ingestion_states() -> None:
    systems = mod.read_catalog()
    statuses = {row["evidence_status"] for row in systems}
    assert len(systems) >= 30
    assert "GATHER_VERIFIED" in statuses
    assert "GATHER_VERIFIED_EMPTY_CAPTURE" in statuses
    assert "STATIC_CAPTURE_FAILED_SOURCE_LEAD" in statuses


def test_static_maps_cover_domains() -> None:
    assert len(mod.substrate_families()) >= 14
    assert len(mod.domain_queue()) >= 18
    assert len(mod.megatool_routes()) >= 6
    assert len(mod.negative_fixtures()) >= 10


def test_composed_artifact_gates() -> None:
    artifact = mod.compose()
    assert artifact["status"] == mod.STATUS_MATCH
    assert artifact["gather_summary"]["captured_sources"] >= 28
    assert artifact["gather_summary"]["usable_captures"] >= 26
    assert len(artifact["source_quality_warnings"]) >= 4
    assert artifact["current_promoted_natural_laws"] == []


if __name__ == "__main__":
    test_catalog_ingestion_states()
    test_static_maps_cover_domains()
    test_composed_artifact_gates()
