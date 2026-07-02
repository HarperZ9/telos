"""Focused tests for pass 0065 OpenTelemetry trace to Telos action receipt fixture."""
from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMPOSER = ROOT / "tools" / "compose_otel_trace_to_action_receipt_fixture.py"


def load_composer():
    spec = importlib.util.spec_from_file_location("compose_otel_trace_to_action_receipt_fixture", COMPOSER)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_otel_trace_to_action_receipt_fixture_shape() -> None:
    module = load_composer()
    packet = module.compose()

    assert packet["schema"] == "OtelTraceToTelosActionReceiptFixture/v1"
    assert packet["pass"] == "0065"
    assert packet["status"] == "OTEL_TRACE_TO_ACTION_RECEIPT_FIXTURE_MATCH"
    assert packet["trace_fixture"]["trace_id"]
    assert len(packet["trace_fixture"]["spans"]) == 4
    assert packet["action_receipt"]["schema"] == "project-telos.action-receipt/v1"

    required_fields = {
        "receipt_id",
        "source_refs",
        "workspace_state",
        "authority_scope",
        "action_admission",
        "tool_call",
        "side_effect_class",
        "trace_refs",
        "eval_refs",
        "verification_verdict",
        "stop_reason",
        "compensation_pointer",
        "privacy_boundary",
        "receipt_status",
    }
    assert required_fields.issubset(packet["action_receipt"].keys())
    assert packet["action_receipt"]["receipt_status"] == "MATCH"
    assert packet["action_receipt"]["verification_verdict"] == "MATCH"
    assert packet["action_receipt"]["side_effect_class"] == "local_read_only_fixture"
    assert packet["action_receipt"]["trace_refs"]["trace_id"] == packet["trace_fixture"]["trace_id"]
    assert len(packet["action_receipt"]["trace_refs"]["span_ids"]) == 4

    assert packet["negative_fixture"]["status"] == "FAIL_EXPECTED"
    assert "missing_authority_scope" in packet["negative_fixture"]["expected_failures"]
    assert packet["unsupported_claim_count"] == 0
    assert packet["non_promotion_statement"]


if __name__ == "__main__":
    test_otel_trace_to_action_receipt_fixture_shape()
