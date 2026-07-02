"""Focused tests for pass 0071 live workspace-context replacement."""
from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMPOSER = ROOT / "tools" / "compose_live_workspace_context_replacement.py"


def load_composer():
    spec = importlib.util.spec_from_file_location("compose_live_workspace_context_replacement", COMPOSER)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_live_workspace_context_replacement_shape() -> None:
    module = load_composer()
    artifact = module.compose()
    required = set(module.REQUIRED_CLASSES)
    workspace_rows = [row for row in artifact["component_receipts"] if row["kind"] == "workspace_context"]
    action_rows = [row for row in artifact["component_receipts"] if row["kind"] == "action"]

    assert artifact["schema"] == "LiveWorkspaceContextReplacement/v1"
    assert artifact["pass"] == "0071"
    assert artifact["status"] == "LIVE_WORKSPACE_CONTEXT_REPLACEMENT_MATCH"
    assert artifact["live_surface"]["status"] == "MATCH"
    assert artifact["live_surface"]["summary"]["schema"] == "project-telos.context-envelope/v1"
    assert artifact["live_surface"]["summary"]["verification_verdict"] == "MATCH"
    assert artifact["index_surface_checks"]["drift"] == 0
    assert {row["kind"] for row in artifact["component_receipts"]} == required
    assert len(workspace_rows) == 1
    assert workspace_rows[0]["component_id"].startswith("index.context-envelope.live")
    assert workspace_rows[0]["retained_count"] >= 1
    assert workspace_rows[0]["receipt_count"] >= 1
    assert len(action_rows) == 1
    assert action_rows[0]["component_id"].startswith("telos.action.receipt.live")
    assert artifact["product_packet"]["component_count"] == 6
    assert artifact["product_packet"]["unsupported_claim_count"] == 0
    assert len(artifact["negative_fixtures"]) >= 7
    assert all(item["expected_status"] == "REJECT" for item in artifact["negative_fixtures"])


if __name__ == "__main__":
    test_live_workspace_context_replacement_shape()
