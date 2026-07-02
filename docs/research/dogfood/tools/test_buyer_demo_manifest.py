"""Behavior test for the pass 0056 buyer-facing demo manifest composer."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_buyer_demo_manifest.py"
GRAPH = ROOT / "schemas" / "multitrace-causality-graph-pass-0055.json"


def test_buyer_demo_manifest_maps_receipts_to_review_panes() -> None:
    with tempfile.TemporaryDirectory(prefix="telos-pass-0056-") as tmp:
        out_dir = Path(tmp) / "demo"
        result = subprocess.run(
            [
                sys.executable,
                str(COMPOSER),
                "--graph",
                str(GRAPH),
                "--out",
                str(out_dir),
            ],
            cwd=REPO,
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0, result.stderr or result.stdout
        manifest = json.loads((out_dir / "manifest.json").read_text(encoding="utf-8"))
        panes = json.loads((out_dir / "review-panes.json").read_text(encoding="utf-8"))
        failures = json.loads((out_dir / "failure-verdicts.json").read_text(encoding="utf-8"))
        receipts = json.loads((out_dir / "receipts.json").read_text(encoding="utf-8"))
        html = (out_dir / "index.html").read_text(encoding="utf-8")
        replay = (out_dir / "replay-commands.md").read_text(encoding="utf-8")

    expected_outputs = {
        "manifest.json",
        "review-panes.json",
        "failure-verdicts.json",
        "replay-commands.md",
        "index.html",
        "receipts.json",
    }
    assert manifest["schema"] == "BuyerDemoManifest/v1"
    assert manifest["status"] == "BUYER_DEMO_MANIFEST_MATCH"
    assert manifest["demo_summary"]["review_pane_count"] == 4
    assert manifest["demo_summary"]["failure_verdict_count"] == 5
    assert manifest["demo_summary"]["replay_command_count"] >= 3
    assert manifest["demo_summary"]["public_review_ready"] is True
    assert manifest["demo_summary"]["production_ready"] is False
    assert manifest["current_promoted_natural_laws"] == []
    assert {pane["tool_class"] for pane in panes["panes"]} == {
        "gather",
        "browser_evidence",
        "command_execution",
        "action_receipt",
    }
    assert all(pane["durable_receipt_ref"] != pane["span_ref"] for pane in panes["panes"])
    assert all(pane["display_redaction"] in {"hash_only", "redacted"} for pane in panes["panes"])
    assert failures["negative_fixture_count"] == 5
    assert failures["negative_match_count"] == 5
    assert failures["negative_pass_observed_count"] == 0
    assert set(receipt["path"] for receipt in receipts["outputs"]) == expected_outputs - {"receipts.json"}
    assert all(receipt["sha256"] for receipt in receipts["outputs"])
    assert "Multi-Trace Causality Demo" in html
    assert "python docs\\research\\dogfood\\tools\\build_multitrace_causality_graph.py" in replay


if __name__ == "__main__":
    test_buyer_demo_manifest_maps_receipts_to_review_panes()
    print("PASS buyer demo manifest verified")
