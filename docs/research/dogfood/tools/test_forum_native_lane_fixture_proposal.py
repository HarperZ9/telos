"""Focused tests for pass 0084 Forum native lane-fixture proposal."""
from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMPOSER = ROOT / "tools" / "compose_forum_native_lane_fixture_proposal.py"


def load_composer():
    spec = importlib.util.spec_from_file_location("compose_forum_native_lane_fixture_proposal", COMPOSER)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_forum_native_lane_fixture_proposal_shape() -> None:
    module = load_composer()
    artifact = module.compose()

    assert artifact["schema"] == "ForumNativeLaneFixtureProposal/v1"
    assert artifact["pass"] == "0084"
    assert artifact["status"] == "FORUM_NATIVE_LANE_FIXTURE_PROPOSAL_MATCH"
    assert artifact["promotion_state"] == "FIXTURE_PROPOSAL_NOT_FORUM_PATCH"
    assert artifact["upstream"]["pass"] == "0083"

    results = artifact["route_test_results"]
    assert results["positive_match"] == results["positive_count"] == 8
    assert results["negative_match"] == results["negative_count"] == 5
    assert len(artifact["lane_fixtures"]) >= 8
    assert len(artifact["migration_plan"]) >= 4
    assert artifact["acceptance_criteria"]["native_patch_required_before_production_claim"] is True
    assert artifact["unsupported_claim_count"] == 0
    assert artifact["current_promoted_natural_laws"] == []


if __name__ == "__main__":
    test_forum_native_lane_fixture_proposal_shape()
