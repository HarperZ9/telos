"""Focused tests for pass 0096 YouTube field growth-vector scorecard."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPOSER = ROOT / "tools" / "compose_youtube_field_growth_vector_scorecard.py"
ARTIFACT = ROOT / "schemas" / "youtube-field-growth-vector-scorecard-pass-0096.json"


def load_composer():
    spec = importlib.util.spec_from_file_location("compose_youtube_field_growth_vector_scorecard", COMPOSER)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_youtube_field_growth_vector_scorecard_shape() -> None:
    module = load_composer()
    artifact = json.loads(ARTIFACT.read_text(encoding="utf-8")) if ARTIFACT.exists() else module.compose()
    vectors = artifact["field_vectors"]
    source = artifact["source_summary"]

    assert artifact["schema"] == "YouTubeFieldGrowthVectorScorecard/v1"
    assert artifact["pass"] == "0096"
    assert artifact["status"] == "YOUTUBE_FIELD_GROWTH_VECTOR_SCORECARD_MATCH"
    assert artifact["source_bindings"] == {"youtube_pass": "0085", "bridge_pass": "0093", "workflow_pass": "0094", "native_buildlang_pass": "0095"}
    assert source["valid_video_count"] == 19
    assert source["metadata_match_count"] == 19
    assert source["transcript_receipt_count"] == 19
    assert source["cluster_count"] == 7
    assert "source leads" in source["source_policy"]
    assert len(vectors) == 8
    assert vectors[0]["id"] == "optimization_proof_workbench"
    assert vectors[0]["source_video_count"] == 13
    assert artifact["primary_30_day_push"]["vector_id"] == "optimization_proof_workbench"
    assert artifact["buildlang_binding"]["native_pass"] == "0095"
    assert artifact["buildlang_binding"]["verify_check_count"] == 18
    assert artifact["buildlang_binding"]["best_value"] == 162
    assert artifact["workflow_binding"]["exact_value"] == 162
    assert len(artifact["integration_map"]) == 10
    assert len(artifact["measurements"]) == 9
    assert all(row["status"] == "MATCH" for row in artifact["measurements"])
    assert all(tool["status"] == "MATCH" for tool in artifact["flagship_receipts"].values())
    assert artifact["unsupported_claim_count"] == 0
    assert artifact["current_promoted_natural_laws"] == []


if __name__ == "__main__":
    test_youtube_field_growth_vector_scorecard_shape()
