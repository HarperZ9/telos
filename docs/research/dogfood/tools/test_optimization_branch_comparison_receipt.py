"""Focused tests for pass 0088 optimization branch comparison receipt."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMPOSER = ROOT / "tools" / "compose_optimization_branch_comparison_receipt.py"
ARTIFACT = ROOT / "schemas" / "optimization-branch-comparison-receipt-pass-0088.json"


def load_composer():
    spec = importlib.util.spec_from_file_location("compose_optimization_branch_comparison_receipt", COMPOSER)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_optimization_branch_comparison_receipt_shape() -> None:
    module = load_composer()
    artifact = json.loads(ARTIFACT.read_text(encoding="utf-8")) if ARTIFACT.exists() else module.compose()
    exact = artifact["exact_branch"]

    assert artifact["schema"] == "OptimizationBranchComparisonReceipt/v1"
    assert artifact["pass"] == "0088"
    assert artifact["status"] == "OPTIMIZATION_BRANCH_COMPARISON_RECEIPT_MATCH"
    assert artifact["prior_binding"]["source_pass"] == "0087"
    assert artifact["upstream_research_binding"]["source_pass"] == "0085"
    assert artifact["upstream_research_binding"]["dominant_cluster"] == "enterprise_quantum_optimization"
    assert artifact["upstream_research_binding"]["dominant_cluster_video_count"] == 13
    assert exact["candidate_count"] == 4096
    assert exact["feasible_count"] > 0
    assert exact["best"]["feasible"] is True
    assert len(artifact["branches"]) == 3
    assert len(artifact["comparisons"]) == 3
    assert all(row["exact_value_gap"] >= 0 for row in artifact["comparisons"])
    assert artifact["comparison_summary"]["branch_count"] == 4
    assert artifact["comparison_summary"]["exact_hit_branches"]
    assert len(artifact["source_anchors"]) >= 4
    assert artifact["promotion_boundary"]["benchmark_only"] is True
    assert artifact["promotion_boundary"]["solver_superiority_claim"] is False
    assert artifact["promotion_boundary"]["quantum_advantage_claim"] is False
    assert artifact["promotion_boundary"]["new_natural_law_claim"] is False
    assert all(receipt["status"] == "MATCH" for receipt in artifact["flagship_receipts"].values())
    assert artifact["unsupported_claim_count"] == 0
    assert artifact["current_promoted_natural_laws"] == []


if __name__ == "__main__":
    test_optimization_branch_comparison_receipt_shape()
