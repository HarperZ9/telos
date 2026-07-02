"""Build a multi-trace causality graph over durable Telos receipts."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any


SCHEMA = "MultiTraceCausalityGraph/v1"
MATCH_STATUS = "MULTITRACE_CAUSALITY_GRAPH_MATCH"
DRIFT_STATUS = "MULTITRACE_CAUSALITY_GRAPH_DRIFT"
REQUIRED_TOOL_CLASSES = ["gather", "browser_evidence", "command_execution", "action_receipt"]


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
    if isinstance(payload, dict) and isinstance(payload.get("spans"), list):
        return payload["spans"]
    if isinstance(payload, list):
        return payload
    raise ValueError("spans input must be a list or {'spans': [...]}")


def span_ref(span: dict[str, Any]) -> str:
    context = span.get("context", {})
    trace_id = context.get("trace_id") or span.get("trace_id")
    span_id = context.get("span_id") or span.get("span_id")
    if not trace_id or not span_id:
        return ""
    return f"otel:trace/{trace_id}/span/{span_id}"


def link_ref(link: dict[str, Any]) -> str:
    trace_id = link.get("trace_id")
    span_id = link.get("span_id")
    if not trace_id or not span_id:
        return ""
    return f"otel:trace/{trace_id}/span/{span_id}"


def build_nodes(spans: list[dict[str, Any]]) -> list[dict[str, Any]]:
    nodes = []
    for span in spans:
        attrs = span.get("attributes", {})
        nodes.append({
            "durable_receipt_hash": attrs.get("telos.receipt_hash"),
            "durable_receipt_kind": attrs.get("telos.receipt_kind"),
            "durable_receipt_ref": attrs.get("telos.receipt_ref"),
            "name": span.get("name"),
            "raw_payload_included": attrs.get("telos.raw_payload_included", False),
            "raw_payload_required": attrs.get("telos.raw_payload_required", False),
            "redaction_status": attrs.get("telos.redaction_status"),
            "span_ref": span_ref(span),
            "tool_class": attrs.get("telos.tool_class"),
        })
    return nodes


def build_edges(spans: list[dict[str, Any]], node_by_span: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    edges = []
    for span in spans:
        target = span_ref(span)
        for link in span.get("links", []):
            source = link_ref(link)
            edges.append({
                "causal_kind": link.get("kind", "linked"),
                "source_span_ref": source,
                "source_tool_class": node_by_span.get(source, {}).get("tool_class"),
                "status": "MATCH" if source in node_by_span and target in node_by_span else "DRIFT",
                "target_span_ref": target,
                "target_tool_class": node_by_span.get(target, {}).get("tool_class"),
            })
    return edges


def required_tool_match_count(nodes: list[dict[str, Any]]) -> int:
    present = {node.get("tool_class") for node in nodes}
    return sum(1 for tool_class in REQUIRED_TOOL_CLASSES if tool_class in present)


def graph_failures(nodes: list[dict[str, Any]], edges: list[dict[str, Any]]) -> list[str]:
    failures = []
    present = {node.get("tool_class") for node in nodes}
    for tool_class in REQUIRED_TOOL_CLASSES:
        if tool_class not in present:
            failures.append(f"missing_tool_class:{tool_class}")
    if len(edges) < max(0, len(nodes) - 1):
        failures.append("missing_trace_link")
    if any(edge["status"] != "MATCH" for edge in edges):
        failures.append("broken_trace_link")
    for node in nodes:
        if not node.get("durable_receipt_ref") or not node.get("durable_receipt_hash"):
            failures.append("missing_durable_receipt")
        if node.get("durable_receipt_ref") == node.get("span_ref"):
            failures.append("trace_id_substitutes_receipt_id")
        if node.get("tool_class") == "browser_evidence":
            if node.get("redaction_status") != "redacted":
                failures.append("browser_not_redacted")
            if node.get("raw_payload_required") is True:
                failures.append("raw_browser_payload_required")
    return sorted(set(failures))


def summarize(nodes: list[dict[str, Any]], edges: list[dict[str, Any]], failures: list[str]) -> dict[str, Any]:
    return {
        "edge_count": len(edges),
        "independent_receipt_count": sum(
            1 for node in nodes if node.get("durable_receipt_ref") and node.get("durable_receipt_ref") != node.get("span_ref")
        ),
        "matched_required_tool_classes": required_tool_match_count(nodes),
        "node_count": len(nodes),
        "trace_identity_substitution_count": sum(1 for node in nodes if node.get("durable_receipt_ref") == node.get("span_ref")),
        "valid_edge_count": sum(1 for edge in edges if edge["status"] == "MATCH"),
    }


def mutate_spans(spans: list[dict[str, Any]], fixture_id: str) -> list[dict[str, Any]]:
    mutated = copy.deepcopy(spans)
    if fixture_id == "missing_trace_link":
        mutated[-1]["links"] = []
    elif fixture_id == "trace_id_substitutes_receipt_id":
        mutated[-1]["attributes"]["telos.receipt_ref"] = span_ref(mutated[-1])
    elif fixture_id == "missing_durable_receipt_hash":
        mutated[0]["attributes"].pop("telos.receipt_hash", None)
    elif fixture_id == "missing_gather_node":
        mutated = [span for span in mutated if span.get("attributes", {}).get("telos.tool_class") != "gather"]
    elif fixture_id == "raw_browser_payload_required":
        for span in mutated:
            if span.get("attributes", {}).get("telos.tool_class") == "browser_evidence":
                span["attributes"]["telos.raw_payload_required"] = True
    else:
        raise ValueError(f"unknown fixture: {fixture_id}")
    return mutated


def evaluate(spans: list[dict[str, Any]]) -> dict[str, Any]:
    nodes = build_nodes(spans)
    by_span = {node["span_ref"]: node for node in nodes if node.get("span_ref")}
    edges = build_edges(spans, by_span)
    failures = graph_failures(nodes, edges)
    summary = summarize(nodes, edges, failures)
    return {
        "edges": edges,
        "failure_codes": failures,
        "graph_summary": summary,
        "nodes": nodes,
        "status": MATCH_STATUS if not failures else DRIFT_STATUS,
    }


def negative_report(spans: list[dict[str, Any]]) -> dict[str, Any]:
    expected = [
        ("missing_trace_link", "missing_trace_link"),
        ("trace_id_substitutes_receipt_id", "trace_id_substitutes_receipt_id"),
        ("missing_durable_receipt_hash", "missing_durable_receipt"),
        ("missing_gather_node", "missing_tool_class:gather"),
        ("raw_browser_payload_required", "raw_browser_payload_required"),
    ]
    rows = []
    for fixture_id, failure_code in expected:
        observed = evaluate(mutate_spans(spans, fixture_id))
        rows.append({
            "expected_failure_code": failure_code,
            "fixture_id": fixture_id,
            "observed_failure_codes": observed["failure_codes"],
            "observed_status": observed["status"],
            "status": "MATCH" if failure_code in observed["failure_codes"] and observed["status"] != MATCH_STATUS else "DRIFT",
        })
    return {
        "negative_fixture_count": len(rows),
        "negative_match_count": sum(1 for row in rows if row["status"] == "MATCH"),
        "negative_pass_observed_count": sum(1 for row in rows if row["observed_status"] == MATCH_STATUS),
        "rows": rows,
    }


def build(spans_path: Path, source_binding_path: Path, trace_join_path: Path, tool_receipts_path: Path) -> dict[str, Any]:
    spans = span_rows(read_json(spans_path))
    result = evaluate(spans)
    negatives = negative_report(spans)
    sources = {
        "source_binding": {"path": str(source_binding_path), "sha256": sha256_file(source_binding_path)},
        "spans": {"path": str(spans_path), "sha256": sha256_file(spans_path), "span_count": len(spans)},
        "tool_receipts": {"path": str(tool_receipts_path), "sha256": sha256_file(tool_receipts_path)},
        "trace_join": {"path": str(trace_join_path), "sha256": sha256_file(trace_join_path)},
    }
    status = result["status"] if negatives["negative_match_count"] == negatives["negative_fixture_count"] else DRIFT_STATUS
    bundle = {
        "schema": SCHEMA,
        "current_promoted_natural_laws": [],
        "generated_on": "2026-07-01",
        "negative_fixture_count": negatives["negative_fixture_count"],
        "negative_match_count": negatives["negative_match_count"],
        "negative_pass_observed_count": negatives["negative_pass_observed_count"],
        "negative_report": negatives,
        "non_promotion_statement": "Pass 0055 proves only a local multi-trace causality graph over synthetic span links and existing dogfood receipts. It does not prove live collector ingestion, complete distributed causality, buyer adoption, scientific truth, or any natural law.",
        "pass": "0055",
        "sources": sources,
        "status": status,
        **result,
    }
    bundle["seal"] = sha256_obj(bundle)
    return bundle


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--spans", required=True)
    parser.add_argument("--source-binding", required=True)
    parser.add_argument("--trace-join", required=True)
    parser.add_argument("--tool-receipts", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    bundle = build(Path(args.spans), Path(args.source_binding), Path(args.trace_join), Path(args.tool_receipts))
    write_json(Path(args.out), bundle)
    print(json.dumps({"out": args.out, "seal": bundle["seal"], "status": bundle["status"]}, indent=2, sort_keys=True))
    if bundle["status"] != MATCH_STATUS:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
