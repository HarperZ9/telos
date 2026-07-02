"""Focused tests for pass 0094 quantum optimization workflow receipt."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPOSER = ROOT / "tools" / "compose_quantum_optimization_workflow_receipt.py"
ARTIFACT = ROOT / "schemas" / "quantum-optimization-workflow-receipt-pass-0094.json"


def load_composer():
    spec = importlib.util.spec_from_file_location("compose_quantum_optimization_workflow_receipt", COMPOSER)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_quantum_optimization_workflow_receipt_shape() -> None:
    module = load_composer()
    artifact = json.loads(ARTIFACT.read_text(encoding="utf-8")) if ARTIFACT.exists() else module.compose()
    workflow = artifact["workflow"]
    branches = workflow["solver_branches"]
    objective = workflow["objective_measurements"]

    assert artifact["schema"] == "QuantumOptimizationWorkflowReceipt/v1"
    assert artifact["pass"] == "0094"
    assert artifact["status"] == "QUANTUM_OPTIMIZATION_WORKFLOW_RECEIPT_MATCH"
    assert artifact["source_binding"]["source_pass"] == "0085"
    assert artifact["source_binding"]["dominant_cluster_video_count"] == 13
    assert artifact["buildlang_binding"]["source_pass"] == "0092"
    assert artifact["buildlang_binding"]["verify_check_count"] == 18
    assert workflow["problem"]["capacity"] == 29
    assert objective["exact_value"] == 162
    assert objective["all_executed_branches_feasible"] is True
    assert branches["exact_enumeration"]["value"] == 162
    assert branches["scipy_dual_annealing"]["exact_hit_count"] == 10
    assert branches["networkx_capacity_dag_longest_path"]["status"] == "MATCH"
    assert branches["networkx_capacity_dag_longest_path"]["value"] == 162
    assert branches["ortools_knapsack"]["status"] == "NOT_EXECUTED_DEPENDENCY_MISSING"
    assert branches["dwave_ocean_sampler"]["status"] == "NOT_EXECUTED_DEPENDENCY_MISSING"
    assert len(artifact["measurements"]) == 10
    assert all(row["status"] == "MATCH" for row in artifact["measurements"])
    assert all(tool["status"] == "MATCH" for tool in artifact["flagship_receipts"].values())
    assert artifact["unsupported_claim_count"] == 0
    assert artifact["current_promoted_natural_laws"] == []


if __name__ == "__main__":
    test_quantum_optimization_workflow_receipt_shape()
