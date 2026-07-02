"""Join imported OpenTelemetry-style spans to Telos action receipts."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any


SCHEMA = "OTelTraceReceiptJoinSet/v1"
MATCH_STATUS = "OTEL_TRACE_RECEIPT_JOIN_MATCH"
DRIFT_STATUS = "OTEL_TRACE_RECEIPT_JOIN_DRIFT"


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_obj(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def span_rows(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict) and isinstance(payload.get("spans"), list):
        return payload["spans"]
    if isinstance(payload, dict):
        return [payload]
    raise ValueError("spans input must be a span object, span list, or {'spans': [...]}")


def span_ids(span: dict[str, Any]) -> tuple[str | None, str | None]:
    context = span.get("context", {})
    trace_id = context.get("trace_id") or span.get("trace_id_hex") or span.get("trace_id")
    span_id = context.get("span_id") or span.get("span_id_hex") or span.get("span_id")
    return trace_id, span_id


def span_ref(trace_id: str | None, span_id: str | None) -> str | None:
    if not trace_id or not span_id:
        return None
    return f"otel:trace/{trace_id}/span/{span_id}"


def index_spans(spans: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    indexed = {}
    for span in spans:
        ref = span_ref(*span_ids(span))
        if ref:
            indexed[ref] = span
    return indexed


def durable_identity(receipt: dict[str, Any], receipt_path: Path) -> dict[str, Any]:
    chain = receipt["action_chain"]
    first_event = chain["events"][0]
    return {
        "action_id": chain["action_id"],
        "action_intent_id": chain["action_intent_id"],
        "chain_head_hash": chain["chain_head_hash"],
        "event_count": chain["event_count"],
        "idempotency_key": chain["idempotency_key"],
        "receipt_hash": sha256_file(receipt_path),
        "receipt_is_trace_span": first_event["trace"].get("receipt_is_trace_span") is True,
        "receipt_ref": f"telos:action-receipt/{chain['action_id']}/chain/{chain['chain_head_hash']}",
    }


def validate_event_join(event: dict[str, Any], span: dict[str, Any] | None, identity: dict[str, Any]) -> dict[str, Any]:
    trace = event.get("trace", {})
    ref = span_ref(trace.get("trace_id_hex"), trace.get("span_id_hex"))
    if not span:
        status = "UNVERIFIABLE"
        failure = "missing_trace_span"
    elif trace.get("receipt_is_trace_span") is True:
        status = "DRIFT"
        failure = "trace_span_replaces_receipt"
    else:
        attrs = span.get("attributes", {})
        checks = {
            "action_id": attrs.get("telos.action_id") == identity["action_id"],
            "action_intent_id": attrs.get("telos.action_intent_id") == identity["action_intent_id"],
            "idempotency_key": attrs.get("telos.idempotency_key") == identity["idempotency_key"],
            "exporter_sink_hash": attrs.get("telos.exporter_sink_hash") == trace.get("exporter_sink_hash"),
        }
        if all(checks.values()):
            status = "MATCH"
            failure = None
        else:
            status = "DRIFT"
            failure = "trace_attribute_join_broken"
    return {
        "event_id": event.get("event_id"),
        "event_type": event.get("event_type"),
        "event_trace_join_status": status,
        "failure_code": failure,
        "receipt_is_trace_span": trace.get("receipt_is_trace_span") is True,
        "span_ref": ref,
    }


def validate_join(receipt: dict[str, Any], receipt_path: Path, spans: list[dict[str, Any]]) -> dict[str, Any]:
    identity = durable_identity(receipt, receipt_path)
    span_index = index_spans(spans)
    imported_ref = next(iter(span_index), None)
    joins = []
    for event in receipt["action_chain"]["events"]:
        ref = span_ref(event.get("trace", {}).get("trace_id_hex"), event.get("trace", {}).get("span_id_hex"))
        joins.append(validate_event_join(event, span_index.get(ref), identity))
    if identity["receipt_ref"] == imported_ref or identity["action_id"] == imported_ref:
        joins.append({
            "event_id": None,
            "event_type": "durable_identity",
            "event_trace_join_status": "DRIFT",
            "failure_code": "trace_id_substitutes_receipt_id",
            "receipt_is_trace_span": True,
            "span_ref": imported_ref,
        })
    joined_event_count = sum(1 for row in joins if row["event_trace_join_status"] == "MATCH")
    trace_replaces_count = sum(1 for row in joins if row["failure_code"] in {"trace_span_replaces_receipt", "trace_id_substitutes_receipt_id"})
    return {
        "durable_receipt_identity": identity,
        "imported_trace_ref": imported_ref,
        "join_summary": {
            "joined_event_count": joined_event_count,
            "trace_replaces_receipt_count": trace_replaces_count,
            "trace_span_count": len(spans),
        },
        "joins": joins,
        "status": MATCH_STATUS if joins and all(row["event_trace_join_status"] == "MATCH" for row in joins) else DRIFT_STATUS,
    }


def mutate_fixture(receipt: dict[str, Any], spans: list[dict[str, Any]], fixture_id: str) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    mutated_receipt = copy.deepcopy(receipt)
    mutated_spans = copy.deepcopy(spans)
    if fixture_id == "missing_trace_span":
        mutated_spans = []
    elif fixture_id == "trace_span_replaces_receipt":
        mutated_receipt["action_chain"]["events"][0]["trace"]["receipt_is_trace_span"] = True
    elif fixture_id == "trace_id_substitutes_receipt_id":
        trace_ref = span_ref(*span_ids(mutated_spans[0]))
        mutated_receipt["action_chain"]["action_id"] = trace_ref
        for event in mutated_receipt["action_chain"]["events"]:
            event["action_id"] = trace_ref
    elif fixture_id == "idempotency_key_unjoined":
        mutated_spans[0]["attributes"].pop("telos.idempotency_key", None)
    else:
        raise ValueError(f"unknown negative fixture: {fixture_id}")
    return mutated_receipt, mutated_spans


def negative_report(receipt: dict[str, Any], receipt_path: Path, spans: list[dict[str, Any]]) -> dict[str, Any]:
    expected = [
        ("missing_trace_span", "missing_trace_span", "UNVERIFIABLE"),
        ("trace_span_replaces_receipt", "trace_span_replaces_receipt", "DRIFT"),
        ("trace_id_substitutes_receipt_id", "trace_id_substitutes_receipt_id", "DRIFT"),
        ("idempotency_key_unjoined", "trace_attribute_join_broken", "DRIFT"),
    ]
    rows = []
    for fixture_id, failure_code, verdict in expected:
        mutated_receipt, mutated_spans = mutate_fixture(receipt, spans, fixture_id)
        result = validate_join(mutated_receipt, receipt_path, mutated_spans)
        observed_failures = {row["failure_code"] for row in result["joins"]}
        observed_verdicts = {row["event_trace_join_status"] for row in result["joins"]}
        status = "MATCH" if failure_code in observed_failures and verdict in observed_verdicts else "DRIFT"
        rows.append({
            "expected_failure_code": failure_code,
            "expected_verdict": verdict,
            "fixture_id": fixture_id,
            "observed_failures": sorted(code for code in observed_failures if code),
            "observed_verdicts": sorted(observed_verdicts),
            "status": status,
        })
    return {
        "negative_fixture_count": len(rows),
        "negative_match_count": sum(1 for row in rows if row["status"] == "MATCH"),
        "negative_pass_observed_count": sum(1 for row in rows if row["observed_verdicts"] == ["MATCH"]),
        "rows": rows,
    }


def build(receipt_path: Path, spans_path: Path) -> dict[str, Any]:
    receipt = read_json(receipt_path)
    spans = span_rows(read_json(spans_path))
    result = validate_join(receipt, receipt_path, spans)
    negatives = negative_report(receipt, receipt_path, spans)
    bundle = {
        "schema": SCHEMA,
        "current_promoted_natural_laws": [],
        "generated_on": "2026-07-01",
        "negative_fixture_count": negatives["negative_fixture_count"],
        "negative_match_count": negatives["negative_match_count"],
        "negative_pass_observed_count": negatives["negative_pass_observed_count"],
        "negative_report": negatives,
        "non_promotion_statement": "Pass 0054 proves only local OTel-style trace import joins to an existing action receipt fixture. It does not prove live runtime observability, buyer adoption, scientific truth, or any natural law.",
        "pass": "0054",
        "receipt_source": {"path": str(receipt_path), "sha256": sha256_file(receipt_path)},
        "span_source": {"path": str(spans_path), "sha256": sha256_file(spans_path), "span_count": len(spans)},
        "status": result["status"] if negatives["negative_match_count"] == negatives["negative_fixture_count"] else DRIFT_STATUS,
        **result,
    }
    bundle["seal"] = sha256_obj(bundle)
    return bundle


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", required=True)
    parser.add_argument("--spans", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    bundle = build(Path(args.receipt), Path(args.spans))
    write_json(Path(args.out), bundle)
    print(json.dumps({"out": args.out, "seal": bundle["seal"], "status": bundle["status"]}, indent=2, sort_keys=True))
    if bundle["status"] != MATCH_STATUS:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
