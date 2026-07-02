"""Focused tests for pass 0121 YouTube megatool growth-vector receipt."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPOSER = ROOT / "tools" / "compose_youtube_megatool_growth_vector_receipt.py"
ARTIFACT = ROOT / "schemas" / "youtube-megatool-growth-vector-receipt-pass-0121.json"


def load_module():
    spec = importlib.util.spec_from_file_location("compose_youtube_megatool_growth_vector_receipt", COMPOSER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_artifact() -> dict:
    if ARTIFACT.exists():
        return json.loads(ARTIFACT.read_text(encoding="utf-8"))
    return load_module().compose()


def test_youtube_growth_vector_shape() -> None:
    artifact = read_artifact()
    leads = artifact["youtube_source_leads"]
    vectors = artifact["growth_vectors"]
    ids = {row["video_id"] for row in leads}

    assert artifact["schema"] == "YoutubeMegatoolGrowthVectorReceipt/v1"
    assert artifact["status"] == "YOUTUBE_MEGATOOL_GROWTH_VECTOR_MATCH"
    assert artifact["source_bindings"]["formal_physics_bridge_pass"] == "0116"
    assert artifact["source_bindings"]["runtime_branch_pass"] == "0120"
    assert ids == {"HbKzqvey5PA", "4MQbd5wTlI8", "EdVG5qNm2rY", "nYwid6Q5HXk"}
    assert all(row["transcript_object_present"] for row in leads)
    assert all(row["raw_transcript_included"] is False for row in leads)
    assert all(row["claim_status"] == "SOURCE_LEAD_ONLY" for row in leads)
    assert all(sum(row["signal_counts"].values()) > 0 for row in leads)
    assert len(vectors) >= 6
    assert all(row["claim_status"] == "HYPOTHESIS" for row in vectors)
    assert all(row["next_experiments"] for row in vectors)
    assert artifact["primary_30_day_push"] == vectors[0]["vector_id"]
    assert any(row["node"] == "BuildLang/buildc" for row in artifact["integration_map"])
    assert artifact["unsupported_claim_count"] == 0
    assert artifact["current_promoted_natural_laws"] == []
    assert "does not validate" in artifact["non_promotion_statement"]
    assert all(row["status"] == "MATCH" for row in artifact["flagship_receipts"].values())


if __name__ == "__main__":
    test_youtube_growth_vector_shape()
