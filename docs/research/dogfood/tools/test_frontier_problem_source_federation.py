"""Focused tests for pass 0151 frontier problem source federation."""
from __future__ import annotations

from compose_frontier_problem_source_federation import build_receipt


def test_source_breadth_and_context() -> None:
    receipt = build_receipt(live_tools=False)
    summary = receipt["summary"]
    assert receipt["schema"] == "FrontierProblemSourceFederationReceipt/v1"
    assert summary["candidate_sources"] >= 80
    assert summary["families"] >= 14
    assert summary["domains"] >= 25
    assert summary["combined_nondeduplicated_substrate_context"] >= 200


def test_capture_accounting_and_warning_policy() -> None:
    receipt = build_receipt(live_tools=False)
    summary = receipt["summary"]
    assert summary["capture_jobs"] == 28
    assert summary["gather_verified"] >= 20
    assert summary["capture_warnings"] >= 4
    assert any(row["status"] == "HTTP_429_RATE_LIMIT_WARNING" for row in receipt["capture_attempts"])
    assert any(row["status"] == "HTTP_503_WARNING" for row in receipt["capture_attempts"])


def test_required_source_classes_and_problem_lanes() -> None:
    receipt = build_receipt(live_tools=False)
    summary = receipt["summary"]
    assert summary["college_database_sources"] >= 10
    assert summary["preprint_sources"] >= 8
    assert summary["scholarly_graph_sources"] >= 8
    assert summary["problem_lanes"] == 12
    assert summary["admission_gates"] == 8
    assert summary["negative_fixtures"] == 12


def test_no_problem_solution_promotion() -> None:
    receipt = build_receipt(live_tools=False)
    assert receipt["current_promoted_theorems"] == []
    assert receipt["current_promoted_natural_laws"] == []
    assert receipt["current_promoted_world_solutions"] == []


if __name__ == "__main__":
    test_source_breadth_and_context()
    test_capture_accounting_and_warning_policy()
    test_required_source_classes_and_problem_lanes()
    test_no_problem_solution_promotion()
