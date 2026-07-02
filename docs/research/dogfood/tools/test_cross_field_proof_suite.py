"""Focused tests for pass 0128 cross-field proof suite."""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "tools" / "compose_cross_field_proof_suite.py"


def load_module():
    spec = importlib.util.spec_from_file_location("compose_cross_field_proof_suite", MODULE)
    if spec is None or spec.loader is None:
        raise AssertionError("module spec unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_cross_field_proof_suite() -> None:
    module = load_module()
    artifact = module.compose()
    fixtures = {row["fixture_id"]: row for row in artifact["fixtures"]}

    assert artifact["schema"] == "CrossFieldProofSuiteReceipt/v1"
    assert artifact["status"] == "CROSS_FIELD_PROOF_SUITE_MATCH"
    assert artifact["source_bindings"]["runtime_layer_pass"] == "0122"
    assert artifact["source_bindings"]["demotion_gate_pass"] == "0126"
    assert artifact["source_bindings"]["runtime_router_pass"] == "0127"
    assert len(artifact["source_receipts"]) >= 4
    assert all(row["status"] == "GATHER_VERIFIED" for row in artifact["source_receipts"])
    assert len(fixtures) == 4
    assert fixtures["formal_odd_sum_identity"]["runtime_branch"]["max_abs_error"] == 0
    assert fixtures["quantum_born_normalization"]["runtime_branch"]["status"] == "MATCH"
    assert fixtures["bounded_knapsack_exact_oracle"]["exact_oracle"]["optimum"]["chosen"] == ["B", "D"]
    assert fixtures["bounded_knapsack_exact_oracle"]["exact_oracle"]["optimum"]["value"] == 25
    assert fixtures["euler_prime_counterexample_revision"]["counterexample"]["n"] == 40
    assert all(row["status"] == "REJECTED" for row in artifact["negative_fixtures"])
    assert artifact["current_promoted_natural_laws"] == []


if __name__ == "__main__":
    test_cross_field_proof_suite()
