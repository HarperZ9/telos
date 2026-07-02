"""Focused tests for pass 0090 solver availability matrix receipt."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPOSER = ROOT / "tools" / "compose_solver_availability_matrix_receipt.py"
ARTIFACT = ROOT / "schemas" / "solver-availability-matrix-receipt-pass-0090.json"


def load_composer():
    spec = importlib.util.spec_from_file_location("compose_solver_availability_matrix_receipt", COMPOSER)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_solver_availability_matrix_receipt_shape() -> None:
    module = load_composer()
    artifact = json.loads(ARTIFACT.read_text(encoding="utf-8")) if ARTIFACT.exists() else module.compose()
    rows = {row["row_id"]: row for row in artifact["matrix_rows"]}

    assert artifact["schema"] == "SolverAvailabilityMatrixReceipt/v1"
    assert artifact["pass"] == "0090"
    assert artifact["status"] == "SOLVER_AVAILABILITY_MATRIX_RECEIPT_MATCH"
    assert artifact["prior_binding"]["source_pass"] == "0089"
    assert artifact["upstream_research_binding"]["dominant_cluster"] == "enterprise_quantum_optimization"
    assert artifact["summary"]["row_count"] >= 24
    assert artifact["summary"]["local_available_rows"] + artifact["summary"]["local_unavailable_rows"] == artifact["summary"]["row_count"]
    assert artifact["summary"]["local_available_rows"] < artifact["summary"]["row_count"]
    assert artifact["package_receipts"]["scipy"]["available"] is True
    assert artifact["package_receipts"]["numpy"]["available"] is True
    assert artifact["package_receipts"]["ortools"]["available"] is False
    assert artifact["package_receipts"]["dwave_system"]["available"] is False
    assert artifact["buildc_corpus_receipt"]["status"] == "MATCH"
    assert rows["buildlang_buildc"]["local_status"] == "SOURCE_AVAILABLE_CORPUS_MATCH"
    assert rows["ortools"]["local_status"] == "LOCAL_UNAVAILABLE"
    assert rows["networkx"]["local_status"] == "LOCAL_AVAILABLE"
    assert len(artifact["source_anchors"]) >= 10
    assert all(receipt["status"] == "MATCH" for receipt in artifact["flagship_receipts"].values())
    assert artifact["promotion_boundary"]["availability_matrix_only"] is True
    assert artifact["promotion_boundary"]["world_problem_solved_claim"] is False
    assert artifact["promotion_boundary"]["new_natural_law_claim"] is False
    assert artifact["unsupported_claim_count"] == 0
    assert artifact["current_promoted_natural_laws"] == []


if __name__ == "__main__":
    test_solver_availability_matrix_receipt_shape()
