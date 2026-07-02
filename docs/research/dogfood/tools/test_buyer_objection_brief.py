"""Behavior test for the pass 0057 buyer-objection brief composer."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_buyer_objection_brief.py"
BUNDLE = ROOT / "demo-bundles" / "multitrace-causality-demo-pass-0056"


def test_buyer_objection_brief_maps_demo_evidence_to_buyer_questions() -> None:
    with tempfile.TemporaryDirectory(prefix="telos-pass-0057-") as tmp:
        out_path = Path(tmp) / "brief.json"
        result = subprocess.run(
            [
                sys.executable,
                str(COMPOSER),
                "--manifest",
                str(BUNDLE / "manifest.json"),
                "--panes",
                str(BUNDLE / "review-panes.json"),
                "--failures",
                str(BUNDLE / "failure-verdicts.json"),
                "--replay",
                str(BUNDLE / "replay-commands.md"),
                "--out",
                str(out_path),
            ],
            cwd=REPO,
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0, result.stderr or result.stdout
        brief = json.loads(out_path.read_text(encoding="utf-8"))

    buyer_ids = {row["buyer_id"] for row in brief["buyer_briefs"]}
    source_urls = {row["url"] for row in brief["source_anchors"]}
    objection_count = sum(len(row["objections"]) for row in brief["buyer_briefs"])

    assert brief["schema"] == "BuyerObjectionBrief/v1"
    assert brief["status"] == "BUYER_OBJECTION_BRIEF_MATCH"
    assert brief["market_claim_boundary"] == "HYPOTHESIS_ONLY"
    assert brief["unsupported_claim_count"] == 0
    assert brief["current_promoted_natural_laws"] == []
    assert brief["demo_bindings"]["review_pane_count"] == 4
    assert brief["demo_bindings"]["failure_verdict_count"] == 5
    assert brief["demo_bindings"]["replay_command_count"] >= 3
    assert brief["demo_bindings"]["public_review_ready"] is True
    assert brief["demo_bindings"]["production_ready"] is False
    assert buyer_ids == {"research_lab", "ai_infra", "regulated_agent"}
    assert objection_count >= 9
    assert len(brief["source_anchors"]) >= 5
    assert all(row["verification_status"] == "verified_official_source" for row in brief["source_anchors"])
    assert all(row["confidence"] == "high" for row in brief["source_anchors"])
    assert "https://www.nist.gov/itl/ai-risk-management-framework" in source_urls
    assert "https://opentelemetry.io/docs/concepts/signals/traces/" in source_urls
    assert "https://docs.langchain.com/langsmith/observability" in source_urls
    assert "https://langfuse.com/docs/observability/overview" in source_urls
    assert "https://azure.microsoft.com/en-us/solutions/discovery" in source_urls
    for buyer in brief["buyer_briefs"]:
        assert len(buyer["objections"]) >= 3
        for objection in buyer["objections"]:
            assert objection["evidence_refs"]
            assert objection["demo_refs"]
            assert objection["response_boundary"] in {"verified", "inferred", "unverified"}
            assert "no_universal_uniqueness_claim" in objection["guardrails"]


if __name__ == "__main__":
    test_buyer_objection_brief_maps_demo_evidence_to_buyer_questions()
    print("PASS buyer objection brief verified")
