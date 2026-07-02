"""Focused tests for pass 0085 YouTube research compounding packet."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMPOSER = ROOT / "tools" / "compose_youtube_research_compounding_packet.py"
ARTIFACT = ROOT / "schemas" / "youtube-research-compounding-packet-pass-0085.json"


def load_composer():
    spec = importlib.util.spec_from_file_location("compose_youtube_research_compounding_packet", COMPOSER)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_youtube_research_compounding_packet_shape() -> None:
    module = load_composer()
    artifact = json.loads(ARTIFACT.read_text(encoding="utf-8")) if ARTIFACT.exists() else module.compose()

    assert artifact["schema"] == "YouTubeResearchCompoundingPacket/v1"
    assert artifact["pass"] == "0085"
    assert artifact["status"] == "YOUTUBE_RESEARCH_COMPOUNDING_PACKET_MATCH"
    assert artifact["input_url_count"] == 20
    assert artifact["valid_url_count"] == 19
    assert artifact["valid_video_count"] == 19
    assert artifact["metadata_match_count"] == 19
    assert artifact["gather_match_count"] >= 15
    assert artifact["transcript_receipt_count"] >= 15
    assert artifact["invalid_url_count"] == 1
    assert len(artifact["research_clusters"]) >= 7
    assert len(artifact["compounding_vectors"]) >= 7
    assert artifact["video_corpus_summary"]["dominant_cluster"] == "enterprise_quantum_optimization"
    assert artifact["video_corpus_summary"]["dominant_cluster_video_count"] == 13
    assert sum(1 for row in artifact["source_cards"] if row.get("source_weight") == "CRITICAL_DATA") == 19
    assert all(row["raw_transcript_included"] is False for row in artifact["source_cards"] if row["status"] != "INVALID_URL")
    assert all(receipt["status"] == "MATCH" for receipt in artifact["flagship_receipts"].values())
    assert artifact["unsupported_claim_count"] == 0
    assert artifact["current_promoted_natural_laws"] == []


if __name__ == "__main__":
    test_youtube_research_compounding_packet_shape()
