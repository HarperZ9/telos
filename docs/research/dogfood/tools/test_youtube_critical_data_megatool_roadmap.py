"""Focused tests for pass 0102 YouTube critical-data roadmap."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPOSER = ROOT / "tools" / "compose_youtube_critical_data_megatool_roadmap.py"
ARTIFACT = ROOT / "schemas" / "youtube-critical-data-megatool-roadmap-pass-0102.json"


def load_module():
    spec = importlib.util.spec_from_file_location("compose_youtube_critical_data_megatool_roadmap", COMPOSER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_artifact() -> dict:
    if ARTIFACT.exists():
        return json.loads(ARTIFACT.read_text(encoding="utf-8"))
    return load_module().compose()


def test_youtube_critical_data_megatool_roadmap_shape() -> None:
    artifact = read_artifact()
    source = artifact["source_summary"]
    nodes = artifact["roadmap_nodes"]
    assert artifact["schema"] == "YouTubeCriticalDataMegatoolRoadmap/v1"
    assert artifact["status"] == "YOUTUBE_CRITICAL_DATA_MEGATOOL_ROADMAP_MATCH"
    assert artifact["source_bindings"]["youtube_pass"] == "0085"
    assert artifact["source_bindings"]["inequality_pass"] == "0101"
    assert source["valid_video_count"] == 19
    assert source["invalid_url_count"] == 1
    assert source["transcript_receipt_count"] == 19
    assert source["raw_transcript_stored"] is False
    assert len(artifact["source_to_architecture_claims"]) == 7
    assert len(nodes) == 8
    assert nodes[0]["node_id"] == "optimization_proof_workbench"
    assert nodes[0]["source_video_count"] == 13
    assert any(isinstance(row, dict) and row["requirement_id"] == "constraint_encoding_receipt" for row in nodes[0]["requirements"])
    assert artifact["constraint_encoding_lesson"]["status"] == "LAW_CANDIDATE"
    assert artifact["current_promoted_natural_laws"] == []
    assert artifact["unsupported_claim_count"] == 0


if __name__ == "__main__":
    test_youtube_critical_data_megatool_roadmap_shape()
