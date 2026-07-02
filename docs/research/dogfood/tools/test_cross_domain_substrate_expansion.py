"""Focused tests for pass 0149 cross-domain substrate expansion."""
from __future__ import annotations

from compose_cross_domain_substrate_expansion import build_receipt


def test_substrate_breadth() -> None:
    receipt = build_receipt(live_tools=False)
    assert receipt["schema"] == "CrossDomainSubstrateExpansionReceipt/v1"
    assert receipt["summary"]["candidate_substrates"] >= 120
    assert receipt["summary"]["families"] >= 14
    assert receipt["summary"]["domains"] >= 20


def test_capture_policy_boundaries() -> None:
    receipt = build_receipt(live_tools=False)
    assert receipt["summary"]["capture_jobs"] == 39
    assert receipt["summary"]["gather_verified"] >= 20
    assert receipt["summary"]["capture_warnings"] >= 5
    assert any(row["status"] == "GATHER_EMPTY_WARNING" for row in receipt["capture_attempts"])
    assert any("WARNING" in row["status"] for row in receipt["capture_attempts"])


def test_candidate_shape_and_non_promotion() -> None:
    receipt = build_receipt(live_tools=False)
    assert all(row["url"].startswith("http") for row in receipt["candidate_substrates"])
    assert all(row["adapter"] for row in receipt["candidate_substrates"])
    assert len(receipt["negative_fixtures"]) == 12
    assert receipt["current_promoted_theorems"] == []
    assert receipt["current_promoted_natural_laws"] == []


if __name__ == "__main__":
    test_substrate_breadth()
    test_capture_policy_boundaries()
    test_candidate_shape_and_non_promotion()
