"""Behavior test for the pass 0054 OTel trace-to-receipt join adapter."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
ADAPTER = ROOT / "tools" / "import_otel_trace_receipts.py"
RECEIPT = ROOT / "schemas" / "telos-action-receipt-fixture-pass-0024.json"


def write_spans(path: Path) -> None:
    span = {
        "schema": "OpenTelemetrySpanLike/v1",
        "name": "telos.action.receipt.fixture",
        "context": {
            "trace_id": "aaa76491660d7a56086f69d1be94debe",
            "span_id": "1424d4ca9a6c5b58",
        },
        "parent_id": None,
        "start_time": "2026-07-01T12:00:00Z",
        "end_time": "2026-07-01T12:03:00Z",
        "status": "OK",
        "attributes": {
            "telos.action_id": "act_dogfood_0024_001",
            "telos.action_intent_id": "intent_dogfood_0024_001",
            "telos.idempotency_key": "idem_dogfood_0024_001",
            "telos.exporter_sink_hash": "f2e9f33d12e261457731f6eedbe62c3c6d04d574c2c8274870da4eee0c2c2fc0",
        },
        "events": [
            {"name": "action_proposed"},
            {"name": "execution_completed"},
            {"name": "verification_recorded"},
        ],
        "links": [],
    }
    path.write_text(json.dumps({"spans": [span]}, indent=2) + "\n", encoding="utf-8")


def test_imported_trace_references_join_without_replacing_receipts() -> None:
    with tempfile.TemporaryDirectory(prefix="telos-pass-0054-") as tmp:
        tmp_path = Path(tmp)
        spans_path = tmp_path / "otel-spans.json"
        out_path = tmp_path / "trace-join.json"
        write_spans(spans_path)

        result = subprocess.run(
            [
                sys.executable,
                str(ADAPTER),
                "--receipt",
                str(RECEIPT),
                "--spans",
                str(spans_path),
                "--out",
                str(out_path),
            ],
            cwd=REPO,
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0, result.stderr or result.stdout
        data = json.loads(out_path.read_text(encoding="utf-8"))

    assert data["schema"] == "OTelTraceReceiptJoinSet/v1"
    assert data["status"] == "OTEL_TRACE_RECEIPT_JOIN_MATCH"
    assert data["durable_receipt_identity"]["action_id"] == "act_dogfood_0024_001"
    assert data["durable_receipt_identity"]["receipt_is_trace_span"] is False
    assert data["durable_receipt_identity"]["receipt_ref"] != data["imported_trace_ref"]
    assert data["join_summary"]["trace_span_count"] == 1
    assert data["join_summary"]["joined_event_count"] == 4
    assert data["join_summary"]["trace_replaces_receipt_count"] == 0
    assert all(row["event_trace_join_status"] == "MATCH" for row in data["joins"])
    assert data["negative_fixture_count"] == 4
    assert data["negative_match_count"] == 4
    assert data["negative_pass_observed_count"] == 0
    assert data["current_promoted_natural_laws"] == []


if __name__ == "__main__":
    test_imported_trace_references_join_without_replacing_receipts()
    print("PASS otel trace receipt join adapter verified")
