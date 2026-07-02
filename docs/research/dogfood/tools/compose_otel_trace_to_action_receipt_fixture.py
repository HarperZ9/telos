"""Compose pass 0065 OpenTelemetry trace to Telos action receipt fixture."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


SCHEMA = "OtelTraceToTelosActionReceiptFixture/v1"
STATUS_MATCH = "OTEL_TRACE_TO_ACTION_RECEIPT_FIXTURE_MATCH"
STATUS_DRIFT = "OTEL_TRACE_TO_ACTION_RECEIPT_FIXTURE_DRIFT"
PASS_ID = "0065"


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def sha256_obj(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def trace_fixture() -> dict[str, Any]:
    trace_id = "4f7e65b0c6c34c2aa1d6f64e08b03a65"
    spans = [
        span("0f1a", None, "agent.run", "root", {"intent": "verify source-backed adapter matrix"}),
        span("0f1b", "0f1a", "gather.docs", "tool", {"source_ref": "packets/074-agent-observability-action-receipt-adapter-matrix.md"}),
        span("0f1c", "0f1a", "validator.run", "tool", {"validator": "validate_pass_0064_agent_observability_action_receipt_adapter_matrix.py"}),
        span("0f1d", "0f1a", "crucible.run", "verifier", {"verdict": "MATCH", "claims": 8}),
    ]
    return {
        "schema": "OpenTelemetryTraceFixture/v1",
        "trace_id": trace_id,
        "spans": spans,
        "source": "synthetic_fixture",
        "status": "MATCH",
    }


def span(span_id: str, parent_span_id: str | None, name: str, kind: str, attributes: dict[str, Any]) -> dict[str, Any]:
    return {
        "attributes": attributes,
        "duration_ms": 12,
        "kind": kind,
        "name": name,
        "parent_span_id": parent_span_id,
        "span_id": span_id,
        "status": "OK",
    }


def action_receipt(trace: dict[str, Any]) -> dict[str, Any]:
    span_ids = [span["span_id"] for span in trace["spans"]]
    receipt = {
        "receipt_id": "telos-action-receipt-pass-0065-otel-fixture",
        "schema": "project-telos.action-receipt/v1",
        "action_admission": {"decision": "admit", "reason": "local read-only fixture with no external side effects"},
        "authority_scope": {"scope": "local_dogfood_fixture", "write_scope": "docs/research/dogfood"},
        "compensation_pointer": {"required": False, "reason": "read-only synthetic fixture"},
        "eval_refs": [{"kind": "validator", "ref": "schemas/pass-0064-agent-observability-action-receipt-adapter-matrix-validator-result.json"}],
        "materials_digest": sha256_obj(trace),
        "model_refs": [],
        "privacy_boundary": "fixture contains no private payload, tokens, PII, or external side effects",
        "receipt_status": "MATCH",
        "runtime_refs": [{"kind": "python", "ref": "local interpreter"}],
        "side_effect_class": "local_read_only_fixture",
        "source_refs": [{"kind": "packet", "ref": "packets/074-agent-observability-action-receipt-adapter-matrix.md"}],
        "stop_reason": "completed_with_match_verdict",
        "tool_call": {"name": "otel_trace_to_action_receipt", "mode": "synthetic_fixture"},
        "trace_refs": {"native_schema": trace["schema"], "span_ids": span_ids, "trace_id": trace["trace_id"]},
        "verification_verdict": "MATCH",
        "workspace_state": {"repo": "telos", "path": "docs/research/dogfood", "dirty_allowed": True},
    }
    receipt["receipt_digest"] = sha256_obj(receipt)
    return receipt


def negative_fixture() -> dict[str, Any]:
    bad_receipt = {
        "receipt_id": "negative-missing-authority-scope",
        "schema": "project-telos.action-receipt/v1",
        "trace_refs": {"trace_id": "negative"},
        "receipt_status": "UNVERIFIABLE",
    }
    return {
        "fixture": bad_receipt,
        "expected_failures": ["missing_authority_scope", "missing_action_admission", "missing_verification_verdict", "missing_side_effect_class"],
        "status": "FAIL_EXPECTED",
    }


def compose() -> dict[str, Any]:
    trace = trace_fixture()
    packet = {
        "schema": SCHEMA,
        "action_receipt": action_receipt(trace),
        "current_promoted_natural_laws": [],
        "generated_on": "2026-07-01",
        "negative_fixture": negative_fixture(),
        "non_promotion_statement": "Pass 0065 is a local synthetic adapter fixture. It does not claim live OpenTelemetry ingestion, production integration, product-market fit, or scientific discovery.",
        "pass": PASS_ID,
        "source_binding": {
            "previous_pass": "0064",
            "previous_schema": "AgentObservabilityActionReceiptAdapterMatrix/v1",
            "purpose": "turn the adapter matrix into an executable receipt fixture",
        },
        "trace_fixture": trace,
        "unsupported_claim_count": 0,
    }
    errors = validate(packet)
    packet["validation_errors"] = errors
    packet["status"] = STATUS_MATCH if not errors else STATUS_DRIFT
    packet["seal"] = sha256_obj(packet)
    return packet


def validate(packet: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    receipt = packet.get("action_receipt", {})
    trace = packet.get("trace_fixture", {})
    required = {"receipt_id", "source_refs", "workspace_state", "authority_scope", "action_admission", "tool_call", "side_effect_class", "trace_refs", "eval_refs", "verification_verdict", "stop_reason", "compensation_pointer", "privacy_boundary", "receipt_status"}
    if packet.get("schema") != SCHEMA:
        errors.append("schema")
    if trace.get("schema") != "OpenTelemetryTraceFixture/v1":
        errors.append("trace_schema")
    if len(trace.get("spans", [])) != 4:
        errors.append("span_count")
    if not required.issubset(receipt):
        errors.append("receipt_fields")
    if receipt.get("trace_refs", {}).get("trace_id") != trace.get("trace_id"):
        errors.append("trace_link")
    if receipt.get("verification_verdict") != "MATCH" or receipt.get("receipt_status") != "MATCH":
        errors.append("receipt_status")
    if packet.get("negative_fixture", {}).get("status") != "FAIL_EXPECTED":
        errors.append("negative_fixture")
    if packet.get("unsupported_claim_count") != 0:
        errors.append("unsupported_claim_count")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    packet = compose()
    write_json(Path(args.out), packet)
    print(json.dumps({"out": args.out, "seal": packet["seal"], "status": packet["status"]}, indent=2, sort_keys=True))
    if packet["status"] != STATUS_MATCH:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
