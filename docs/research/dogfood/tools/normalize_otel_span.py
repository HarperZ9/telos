"""Normalize one OpenTelemetry-style span into a Telos action event."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def normalize(span: dict[str, Any]) -> dict[str, Any]:
    context = span.get("context", {})
    attributes = span.get("attributes", {})
    events = span.get("events", [])
    links = span.get("links", [])
    missing = []

    required_paths = {
        "name": span.get("name"),
        "context.trace_id": context.get("trace_id"),
        "context.span_id": context.get("span_id"),
        "start_time": span.get("start_time"),
        "end_time": span.get("end_time"),
    }
    for field, value in required_paths.items():
        if value in (None, "", []):
            missing.append(field)

    return {
        "schema": "TelosActionEvent/v1",
        "source_schema": "OpenTelemetrySpanLike/v1",
        "action_trace_id": context.get("trace_id"),
        "action_event_id": context.get("span_id"),
        "parent_action_event_id": span.get("parent_id"),
        "action_name": span.get("name"),
        "started_at": span.get("start_time"),
        "finished_at": span.get("end_time"),
        "runtime_attributes": attributes,
        "action_observations": events,
        "causal_links": links,
        "runtime_status": span.get("status", "Unset"),
        "proof_layer_status": "requires_authority_workspace_and_verification",
        "non_inferable_telos_fields": [
            "authority_receipts",
            "workspace_state",
            "verification_verdicts",
            "decision_summary",
        ],
        "normalization_status": "MATCH" if not missing else "DRIFT",
        "missing_required_source_fields": missing,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize one OTel span fixture.")
    parser.add_argument("span", help="Path to an OpenTelemetry-style span JSON file.")
    args = parser.parse_args()

    action = normalize(load_json(Path(args.span)))
    print(json.dumps(action, indent=2, sort_keys=True))
    return 0 if action["normalization_status"] == "MATCH" else 1


if __name__ == "__main__":
    raise SystemExit(main())
