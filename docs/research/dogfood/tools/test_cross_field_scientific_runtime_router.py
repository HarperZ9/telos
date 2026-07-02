"""Focused tests for pass 0127 cross-field runtime router."""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "tools" / "compose_cross_field_scientific_runtime_router.py"


def load_module():
    spec = importlib.util.spec_from_file_location("compose_cross_field_scientific_runtime_router", MODULE)
    if spec is None or spec.loader is None:
        raise AssertionError("module spec unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_cross_field_runtime_router() -> None:
    module = load_module()
    artifact = module.compose()

    assert artifact["schema"] == "CrossFieldScientificRuntimeRouterReceipt/v1"
    assert artifact["status"] == "CROSS_FIELD_SCIENTIFIC_RUNTIME_ROUTER_MATCH"
    assert artifact["source_bindings"]["demotion_gate_pass"] == "0126"
    assert artifact["source_bindings"]["runtime_layer_pass"] == "0122"
    assert artifact["source_lead"]["video_id"] == "HbKzqvey5PA"
    assert artifact["demotion_gate_result"]["gate_status"] == "ACCEPTED"
    assert artifact["exact_oracle"]["probability_sum"] == "1"
    assert artifact["exact_oracle"]["probabilities"] == ["9/25", "16/25", "0"]
    assert artifact["runtime_branch"]["status"] == "MATCH"
    assert artifact["runtime_branch"]["probability_sum_abs_drift"] <= artifact["runtime_branch"]["tolerance"]
    assert len(artifact["negative_fixtures"]) == 3
    assert all(row["status"] == "REJECTED" for row in artifact["negative_fixtures"])
    assert artifact["interpretation_claim_status"] == "SOURCE_LEAD_ONLY"
    assert artifact["market_claim_status"] == "UNVERIFIED"
    assert artifact["current_promoted_natural_laws"] == []


if __name__ == "__main__":
    test_cross_field_runtime_router()
