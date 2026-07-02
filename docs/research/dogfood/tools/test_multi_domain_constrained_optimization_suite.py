"""Focused tests for pass 0114 multi-domain constrained optimization suite."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPOSER = ROOT / "tools" / "compose_multi_domain_constrained_optimization_suite.py"
ARTIFACT = ROOT / "schemas" / "multi-domain-constrained-optimization-suite-pass-0114.json"


def load_module():
    spec = importlib.util.spec_from_file_location("compose_multi_domain_constrained_optimization_suite", COMPOSER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_artifact() -> dict:
    if ARTIFACT.exists():
        return json.loads(ARTIFACT.read_text(encoding="utf-8"))
    return load_module().compose()


def by_id(cases: list[dict], case_id: str) -> dict:
    return next(row for row in cases if row["case_id"] == case_id)


def test_multi_domain_constrained_optimization_suite_shape() -> None:
    artifact = read_artifact()
    cases = artifact["cases"]
    warehouse = by_id(cases, "warehouse_capacity_assignment")
    robotics = by_id(cases, "robotics_quality_inspection")
    defense = by_id(cases, "safety_allocation_toy")
    quant = by_id(cases, "quant_risk_budget")

    assert artifact["schema"] == "MultiDomainConstrainedOptimizationSuiteReceipt/v1"
    assert artifact["status"] == "MULTI_DOMAIN_CONSTRAINED_OPTIMIZATION_SUITE_MATCH"
    assert artifact["source_bindings"]["mpc_pass"] == "0113"
    assert artifact["source_bindings"]["youtube_roadmap_pass"] == "0102"
    assert len(cases) == 4
    assert all(row["classification"] == "MATCH" for row in cases)
    assert all(row["negative_fixture"]["classification"].endswith("_EXPECTED") for row in cases)
    assert warehouse["objective"] == "9"
    assert warehouse["constraint_checks"]["capacity_ok"] is True
    assert warehouse["negative_fixture"]["classification"] == "CAPACITY_VIOLATION_EXPECTED"
    assert robotics["objective"] == "16"
    assert robotics["constraint_checks"]["coverage_ok"] is True
    assert robotics["negative_fixture"]["classification"] == "COVERAGE_VIOLATION_EXPECTED"
    assert defense["objective"] == "17"
    assert defense["constraint_checks"]["high_priority_covered"] is True
    assert defense["negative_fixture"]["classification"] == "INFEASIBLE_EXPECTED"
    assert quant["objective"] == "9/2"
    assert quant["constraint_checks"]["risk_budget_ok"] is True
    assert quant["negative_fixture"]["classification"] == "RISK_BUDGET_VIOLATION_EXPECTED"
    assert artifact["youtube_binding"]["valid_video_count"] == 19
    assert artifact["youtube_binding"]["dominant_cluster_video_count"] == 13
    assert artifact["domain_coverage"]["case_count"] == 4
    assert artifact["domain_coverage"]["youtube_cluster_count"] >= 3
    assert artifact["market_surface"]["tool_count"] >= 10
    assert artifact["unsupported_claim_count"] == 0
    assert artifact["current_promoted_natural_laws"] == []


if __name__ == "__main__":
    test_multi_domain_constrained_optimization_suite_shape()
