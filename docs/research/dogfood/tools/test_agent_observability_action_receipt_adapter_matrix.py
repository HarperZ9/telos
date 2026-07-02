"""Focused tests for pass 0064 agent observability action-receipt adapter matrix."""
from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMPOSER = ROOT / "tools" / "compose_agent_observability_action_receipt_adapter_matrix.py"


def load_composer():
    spec = importlib.util.spec_from_file_location("compose_agent_observability_action_receipt_adapter_matrix", COMPOSER)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_agent_observability_adapter_matrix_shape() -> None:
    module = load_composer()
    packet = module.compose()

    assert packet["schema"] == "AgentObservabilityActionReceiptAdapterMatrix/v1"
    assert packet["pass"] == "0064"
    assert packet["status"] == "AGENT_OBSERVABILITY_ACTION_RECEIPT_ADAPTER_MATRIX_MATCH"
    assert packet["unsupported_uniqueness_claim_count"] == 0
    assert packet["non_replacement_claim"] is True

    source_ids = {row["source_id"] for row in packet["source_anchors"]}
    assert len(source_ids) >= 10

    row_tools = {row["tool"] for row in packet["adapter_rows"]}
    for tool in ("LangSmith", "Langfuse", "Arize Phoenix", "Braintrust", "OpenTelemetry", "MLflow", "W&B Weave", "DVC", "promptfoo", "Helicone"):
        assert tool in row_tools

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
    assert required_fields.issubset(set(packet["action_receipt_fields"]))

    for row in packet["adapter_rows"]:
        assert row["source_id"] in source_ids
        assert row["gap_status"] in {"verified", "inferred", "unverified"}
        assert row["proof_layer_gap_status"] == "inferred"
        assert 1 <= row["adapter_priority"] <= 5
        assert row["telos_adapter_outputs"]

    priorities = [row["adapter_priority"] for row in packet["adapter_rows"]]
    assert max(priorities) == 5
    assert len(packet["demo_slices"]) == 3
    assert all(slice_["promotion_state"] == "DEMO_NOT_PRODUCT_MARKET_FIT" for slice_ in packet["demo_slices"])


if __name__ == "__main__":
    test_agent_observability_adapter_matrix_shape()
