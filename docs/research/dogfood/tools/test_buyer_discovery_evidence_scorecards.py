"""Behavior test for pass 0059 buyer-discovery evidence scorecards."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_buyer_discovery_evidence_scorecards.py"
BRIDGE = ROOT / "schemas" / "forum-route-vocabulary-bridge-pass-0058.json"


def test_buyer_discovery_scorecards_attach_sources_and_market_targets() -> None:
    with tempfile.TemporaryDirectory(prefix="telos-pass-0059-") as tmp:
        out_path = Path(tmp) / "scorecards.json"
        result = subprocess.run(
            [sys.executable, str(COMPOSER), "--bridge", str(BRIDGE), "--out", str(out_path)],
            cwd=REPO,
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0, result.stderr or result.stdout
        packet = json.loads(out_path.read_text(encoding="utf-8"))

    buyer_ids = {row["buyer_id"] for row in packet["scorecards"]}
    source_urls = {row["url"] for row in packet["source_anchors"]}
    prompt_count = sum(row["interview_prompt_count"] for row in packet["scorecards"])

    assert packet["schema"] == "BuyerDiscoveryEvidenceScorecards/v1"
    assert packet["status"] == "BUYER_DISCOVERY_EVIDENCE_SCORECARDS_MATCH"
    assert packet["market_claim_boundary"] == "HYPOTHESIS_ONLY"
    assert packet["market_data_status"] == "COLLECTION_TARGETS_DEFINED"
    assert packet["unsupported_claim_count"] == 0
    assert packet["current_promoted_natural_laws"] == []
    assert packet["upstream_bridge"]["status"] == "FORUM_ROUTE_VOCABULARY_BRIDGE_MATCH"
    assert buyer_ids == {"research_lab", "ai_infra", "regulated_agent"}
    assert packet["source_anchor_count"] >= 9
    assert prompt_count == 9
    assert all(row["verification_status"] == "verified_primary_source" for row in packet["source_anchors"])
    assert all(row["confidence"] == "high" for row in packet["source_anchors"])
    assert "https://www.futurehouse.org/" in source_urls
    assert "https://azure.microsoft.com/en-us/solutions/discovery" in source_urls
    assert "https://www.nist.gov/itl/ai-risk-management-framework" in source_urls
    assert "https://github.com/Pengbinghui/pipeline-math" in source_urls
    assert "https://leandojo.org/leandojo.html" in source_urls
    assert "https://opentelemetry.io/docs/concepts/signals/traces/" in source_urls
    for scorecard in packet["scorecards"]:
        assert len(scorecard["source_ids"]) >= 3
        assert len(scorecard["market_data_targets"]) >= 4
        assert len(scorecard["evidence_requirements"]) >= 4
        assert scorecard["scorecard_status"] == "NEEDS_INTERVIEW_DATA"
        assert scorecard["route_lane_split"] == ["project-telos", "deep-research", "technical-writing"]
        assert all(target["verification_status"] in {"verified", "inferred", "unverified"} for target in scorecard["market_data_targets"])
    assert packet["collection_plan"]["next_pass"] == "0060"
    assert len(packet["collection_plan"]["collection_steps"]) >= 5


if __name__ == "__main__":
    test_buyer_discovery_scorecards_attach_sources_and_market_targets()
    print("PASS buyer discovery evidence scorecards verified")
