"""Behavior test for the pass 0058 Forum route-vocabulary bridge."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_forum_route_vocabulary_bridge.py"
BRIEF = ROOT / "schemas" / "buyer-objection-brief-pass-0057.json"
RECEIPTS = ROOT / "schemas" / "tool-receipts-pass-0057.json"


def test_route_bridge_converts_market_language_into_split_lane_prompts() -> None:
    with tempfile.TemporaryDirectory(prefix="telos-pass-0058-") as tmp:
        out_path = Path(tmp) / "route-bridge.json"
        result = subprocess.run(
            [
                sys.executable,
                str(COMPOSER),
                "--brief",
                str(BRIEF),
                "--receipts",
                str(RECEIPTS),
                "--out",
                str(out_path),
            ],
            cwd=REPO,
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0, result.stderr or result.stdout
        packet = json.loads(out_path.read_text(encoding="utf-8"))

    lane_ids = {lane["lane_id"] for lane in packet["lane_taxonomy"]}
    rewrite_splits = [row["target_lane_split"] for row in packet["rewrite_fixtures"]]

    assert packet["schema"] == "ForumRouteVocabularyBridge/v1"
    assert packet["status"] == "FORUM_ROUTE_VOCABULARY_BRIDGE_MATCH"
    assert packet["market_claim_boundary"] == "HYPOTHESIS_ONLY"
    assert packet["current_promoted_natural_laws"] == []
    assert packet["unsupported_claim_count"] == 0
    assert packet["upstream_brief"]["status"] == "BUYER_OBJECTION_BRIEF_MATCH"
    assert packet["observed_forum_gap"]["status"] == "ROUTE_ESCALATION_OBSERVED"
    assert lane_ids == {"project-telos", "deep-research", "technical-writing"}
    assert len(packet["rewrite_fixtures"]) >= 5
    assert all({"project-telos", "deep-research", "technical-writing"}.issubset(set(split)) for split in rewrite_splits)
    assert all("Project Telos proof-packet" in row["bridge_prompt"] for row in packet["rewrite_fixtures"])
    assert packet["buyer_discovery_script"]["prompt_count"] == 9
    assert packet["buyer_discovery_script"]["source_objection_count"] == 9
    assert all(row["evidence_refs"] for row in packet["buyer_discovery_script"]["prompts"])
    assert all(row["target_lane_split"] == ["project-telos", "deep-research", "technical-writing"] for row in packet["buyer_discovery_script"]["prompts"])
    assert packet["integration_gaps"][0]["verification_status"] in {"verified", "inferred", "unverified"}
    assert packet["route_readiness"]["ready_for_forum_patch"] is False
    assert packet["route_readiness"]["ready_for_operator_use"] is True


if __name__ == "__main__":
    test_route_bridge_converts_market_language_into_split_lane_prompts()
    print("PASS Forum route vocabulary bridge verified")
