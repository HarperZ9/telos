"""Focused tests for pass 0089 external solver adapter receipt."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPOSER = ROOT / "tools" / "compose_external_solver_adapter_receipt.py"
ARTIFACT = ROOT / "schemas" / "external-solver-adapter-receipt-pass-0089.json"


def load_composer():
    spec = importlib.util.spec_from_file_location("compose_external_solver_adapter_receipt", COMPOSER)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_external_solver_adapter_receipt_shape() -> None:
    module = load_composer()
    artifact = json.loads(ARTIFACT.read_text(encoding="utf-8")) if ARTIFACT.exists() else module.compose()
    adapter = artifact["external_adapter"]
    comparison = adapter["comparison_to_exact"]

    assert artifact["schema"] == "ExternalSolverAdapterReceipt/v1"
    assert artifact["pass"] == "0089"
    assert artifact["status"] == "EXTERNAL_SOLVER_ADAPTER_RECEIPT_MATCH"
    assert artifact["prior_binding"]["source_pass"] == "0088"
    assert artifact["upstream_research_binding"]["dominant_cluster"] == "enterprise_quantum_optimization"
    assert artifact["dependency_receipts"]["scipy"]["available"] is True
    assert artifact["dependency_receipts"]["scipy"]["version"]
    assert artifact["dependency_receipts"]["numpy"]["available"] is True
    assert artifact["dependency_receipts"]["ortools"]["available"] is False
    assert adapter["adapter"] == "scipy.optimize.dual_annealing"
    assert adapter["adapter_status"] == "MATCH"
    assert adapter["run_count"] == 16
    assert adapter["runs_sha256"]
    assert adapter["best"]["feasible"] is True
    assert comparison["hit_exact_bits"] is True
    assert comparison["exact_value_gap"] == 0
    assert comparison["exact_hit_count"] > 0
    assert all(run["seed"] for run in adapter["runs"])
    assert all(receipt["status"] == "MATCH" for receipt in artifact["flagship_receipts"].values())
    assert artifact["promotion_boundary"]["solver_superiority_claim"] is False
    assert artifact["promotion_boundary"]["quantum_advantage_claim"] is False
    assert artifact["unsupported_claim_count"] == 0
    assert artifact["current_promoted_natural_laws"] == []


if __name__ == "__main__":
    test_external_solver_adapter_receipt_shape()
