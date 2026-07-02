"""Behavior test for the pass 0055 multi-trace causality graph adapter."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
ADAPTER = ROOT / "tools" / "build_multitrace_causality_graph.py"
SOURCE_BINDING = ROOT / "schemas" / "source-evidence-binding-pass-0028.json"
TRACE_JOIN = ROOT / "schemas" / "otel-trace-receipt-join-pass-0054.json"
TOOL_RECEIPTS = ROOT / "schemas" / "tool-receipts-pass-0054.json"


def write_spans(path: Path) -> None:
    spans = [
        {
            "name": "gather.docs.packet",
            "context": {"trace_id": "00550000000000000000000000000001", "span_id": "0055000000000001"},
            "links": [],
            "attributes": {
                "telos.tool_class": "gather",
                "telos.receipt_kind": "GatherDocumentReceipt/v1",
                "telos.receipt_ref": "gather:docs/packets/064-otel-trace-receipt-join-adapter.md",
                "telos.receipt_hash": "71b39e899e143294fb810a2d335bb11cbeff43abf26114cdda22573dd2502952",
                "telos.raw_payload_included": False,
            },
        },
        {
            "name": "browser.evidence.redacted",
            "context": {"trace_id": "00550000000000000000000000000002", "span_id": "0055000000000002"},
            "links": [{"trace_id": "00550000000000000000000000000001", "span_id": "0055000000000001", "kind": "source"}],
            "attributes": {
                "telos.tool_class": "browser_evidence",
                "telos.receipt_kind": "project-telos.browser-evidence/v1",
                "telos.receipt_ref": "artifact:fixtures/browser-evidence-redacted-pass-0028.json",
                "telos.receipt_hash": "d30289cfdcaf8630e7fb7b3ba911cbac485a62f5306e3b5c37338768dbfe9e7a",
                "telos.redaction_status": "redacted",
                "telos.raw_payload_required": False,
            },
        },
        {
            "name": "shell.command.validation",
            "context": {"trace_id": "00550000000000000000000000000003", "span_id": "0055000000000003"},
            "links": [{"trace_id": "00550000000000000000000000000002", "span_id": "0055000000000002", "kind": "evidence"}],
            "attributes": {
                "telos.tool_class": "command_execution",
                "telos.receipt_kind": "ShellCommandReceipt/v1",
                "telos.receipt_ref": "command:python docs/research/dogfood/tools/validate_pass_0054_otel_trace_receipt_join_adapter.py",
                "telos.receipt_hash": "validator-pass-0054-match",
                "telos.exit_code": 0,
            },
        },
        {
            "name": "telos.action.receipt.fixture",
            "context": {"trace_id": "aaa76491660d7a56086f69d1be94debe", "span_id": "1424d4ca9a6c5b58"},
            "links": [{"trace_id": "00550000000000000000000000000003", "span_id": "0055000000000003", "kind": "execution"}],
            "attributes": {
                "telos.tool_class": "action_receipt",
                "telos.receipt_kind": "TelosActionReceiptFixtureChain/v1",
                "telos.receipt_ref": "telos:action-receipt/act_dogfood_0024_001/chain/0617602eed957e0bc6c2e4a21548528f6defc542c4468433bde85df76cb51b3a",
                "telos.receipt_hash": "9c6402f98774170311d78ea3f6983cae71a665dd38ab2ee7e88d413398990ff4",
                "telos.action_id": "act_dogfood_0024_001",
            },
        },
    ]
    path.write_text(json.dumps({"schema": "OpenTelemetrySpanExportFixture/v1", "spans": spans}, indent=2) + "\n", encoding="utf-8")


def test_multitrace_graph_preserves_independent_receipts() -> None:
    with tempfile.TemporaryDirectory(prefix="telos-pass-0055-") as tmp:
        tmp_path = Path(tmp)
        spans_path = tmp_path / "spans.json"
        out_path = tmp_path / "graph.json"
        write_spans(spans_path)
        result = subprocess.run(
            [
                sys.executable,
                str(ADAPTER),
                "--spans",
                str(spans_path),
                "--source-binding",
                str(SOURCE_BINDING),
                "--trace-join",
                str(TRACE_JOIN),
                "--tool-receipts",
                str(TOOL_RECEIPTS),
                "--out",
                str(out_path),
            ],
            cwd=REPO,
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0, result.stderr or result.stdout
        graph = json.loads(out_path.read_text(encoding="utf-8"))

    assert graph["schema"] == "MultiTraceCausalityGraph/v1"
    assert graph["status"] == "MULTITRACE_CAUSALITY_GRAPH_MATCH"
    assert graph["graph_summary"]["node_count"] == 4
    assert graph["graph_summary"]["edge_count"] == 3
    assert graph["graph_summary"]["independent_receipt_count"] == 4
    assert graph["graph_summary"]["trace_identity_substitution_count"] == 0
    assert graph["graph_summary"]["matched_required_tool_classes"] == 4
    assert {node["tool_class"] for node in graph["nodes"]} == {
        "gather",
        "browser_evidence",
        "command_execution",
        "action_receipt",
    }
    assert all(node["span_ref"] != node["durable_receipt_ref"] for node in graph["nodes"])
    assert all(node["durable_receipt_hash"] for node in graph["nodes"])
    assert graph["negative_fixture_count"] == 5
    assert graph["negative_match_count"] == 5
    assert graph["negative_pass_observed_count"] == 0
    assert graph["current_promoted_natural_laws"] == []


if __name__ == "__main__":
    test_multitrace_graph_preserves_independent_receipts()
    print("PASS multitrace causality graph verified")
