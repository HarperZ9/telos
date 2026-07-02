"""Focused tests for pass 0103 constraint-encoding receipt adapter."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPOSER = ROOT / "tools" / "compose_constraint_encoding_receipt_adapter.py"
ARTIFACT = ROOT / "schemas" / "constraint-encoding-receipt-adapter-pass-0103.json"


def load_module():
    spec = importlib.util.spec_from_file_location("compose_constraint_encoding_receipt_adapter", COMPOSER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_artifact() -> dict:
    if ARTIFACT.exists():
        return json.loads(ARTIFACT.read_text(encoding="utf-8"))
    return load_module().compose()


def test_constraint_encoding_receipt_adapter_shape() -> None:
    artifact = read_artifact()
    coverage = artifact["coverage"]
    rows = artifact["constraint_encoding_receipts"]
    ocean = next(row for row in rows if row["branch_id"] == "ocean_dimod_exact_bqm")
    ortools = next(row for row in rows if row["branch_id"] == "ortools_knapsack_dynamic_programming")
    assert artifact["schema"] == "ConstraintEncodingReceiptAdapter/v1"
    assert artifact["status"] == "CONSTRAINT_ENCODING_RECEIPT_ADAPTER_MATCH"
    assert artifact["source_bindings"]["inequality_pass"] == "0101"
    assert coverage["receipt_count"] == 10
    assert coverage["executed_receipt_count"] == 8
    assert coverage["promotion_blocked_executed_count"] == 1
    assert coverage["unsafe_executed_branch_ids"] == ["ocean_dimod_exact_bqm"]
    assert coverage["all_executed_have_feasibility_check"] is True
    assert ocean["encoding_method"] == "bqm_equality_penalty_to_capacity"
    assert ocean["promotion_blocked"] is True
    assert ocean["adapter_status"] == "MATCH_WITH_PROMOTION_BLOCK"
    assert ortools["encoding_method"] == "solver_native_knapsack_capacity"
    assert ortools["promotion_blocked"] is False
    assert artifact["current_promoted_natural_laws"] == []
    assert artifact["unsupported_claim_count"] == 0


if __name__ == "__main__":
    test_constraint_encoding_receipt_adapter_shape()
