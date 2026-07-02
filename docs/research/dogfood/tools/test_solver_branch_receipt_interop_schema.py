"""Focused tests for pass 0098 solver branch receipt interop schema."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPOSER = ROOT / "tools" / "compose_solver_branch_receipt_interop_schema.py"
ARTIFACT = ROOT / "schemas" / "solver-branch-receipt-interop-schema-pass-0098.json"


def load_composer():
    spec = importlib.util.spec_from_file_location("compose_solver_branch_receipt_interop_schema", COMPOSER)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_solver_branch_receipt_interop_schema_shape() -> None:
    module = load_composer()
    artifact = json.loads(ARTIFACT.read_text(encoding="utf-8")) if ARTIFACT.exists() else module.compose()
    branches = artifact["branch_receipts"]
    coverage = artifact["coverage"]
    by_id = {row["branch_id"]: row for row in branches}

    assert artifact["schema"] == "SolverBranchReceiptInteropSchema/v1"
    assert artifact["pass"] == "0098"
    assert artifact["status"] == "SOLVER_BRANCH_RECEIPT_INTEROP_SCHEMA_MATCH"
    assert artifact["source_bindings"]["workbench_pass"] == "0097"
    assert len(branches) == 8
    assert coverage["executed_count"] == 6
    assert coverage["dependency_boundary_count"] == 2
    assert coverage["best_value"] == 162
    assert coverage["max_observed_gap"] == 16
    assert by_id["buildlang_greedy_ratio_order"]["gap_to_exact"] == 16
    assert by_id["buildlang_bounded_prefix_2048"]["gap_to_exact"] == 5
    assert by_id["ortools_knapsack"]["execution_status"] == "NOT_EXECUTED_DEPENDENCY_MISSING"
    assert by_id["dwave_ocean_sampler"]["claim_status"] == "DEPENDENCY_BOUNDARY"
    assert len(artifact["source_anchors"]) == 4
    assert len(artifact["required_fields"]) == 11
    assert len(artifact["measurements"]) == 8
    assert all(row["status"] == "MATCH" for row in artifact["measurements"])
    assert all(tool["status"] == "MATCH" for tool in artifact["flagship_receipts"].values())
    assert artifact["unsupported_claim_count"] == 0
    assert artifact["current_promoted_natural_laws"] == []


if __name__ == "__main__":
    test_solver_branch_receipt_interop_schema_shape()
