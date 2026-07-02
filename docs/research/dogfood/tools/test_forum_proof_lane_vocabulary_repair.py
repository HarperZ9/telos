"""Focused tests for pass 0083 Forum proof-lane vocabulary repair."""
from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMPOSER = ROOT / "tools" / "compose_forum_proof_lane_vocabulary_repair.py"


def load_composer():
    spec = importlib.util.spec_from_file_location("compose_forum_proof_lane_vocabulary_repair", COMPOSER)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_forum_proof_lane_vocabulary_repair_shape() -> None:
    module = load_composer()
    artifact = module.compose()

    assert artifact["schema"] == "ForumProofLaneVocabularyRepair/v1"
    assert artifact["pass"] == "0083"
    assert artifact["status"] == "FORUM_PROOF_LANE_VOCABULARY_REPAIR_MATCH"
    assert artifact["promotion_state"] == "PROMPT_BRIDGE_NOT_FORUM_PATCH"
    assert artifact["baseline"]["source_pass"] == "0082"
    assert artifact["baseline"]["non_escalated_count"] == 1

    summary = artifact["repair_summary"]
    assert summary["route_probe_count"] == 8
    assert summary["route_match_count"] == 8
    assert summary["repair_status"] == "MATCH"
    assert summary["non_escalated_count"] >= 5
    assert summary["improvement_over_baseline"] >= 4

    assert len(artifact["taxonomy_patch_candidates"]) >= 7
    assert len(artifact["negative_fixtures"]) >= 6
    assert artifact["unsupported_claim_count"] == 0
    assert artifact["current_promoted_natural_laws"] == []
    assert artifact["repair_caveats"]


if __name__ == "__main__":
    test_forum_proof_lane_vocabulary_repair_shape()
