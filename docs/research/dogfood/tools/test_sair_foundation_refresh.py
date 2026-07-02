"""Focused tests for pass 0141 SAIR Foundation source-refresh composer."""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "compose_sair_foundation_refresh.py"

spec = importlib.util.spec_from_file_location("compose_sair_foundation_refresh", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


def test_receipt_shape() -> None:
    receipt = module.build_receipt()
    assert receipt["schema"] == "SAIRFoundationRefreshReceipt/v1"
    assert receipt["status"] == "SAIR_FOUNDATION_REFRESH_MATCH"
    assert receipt["gather_summary"]["items"] >= 11
    assert len(receipt["channel_leads"]) == 12
    assert len(receipt["megatool_routes"]) == 6


def test_boundaries() -> None:
    receipt = module.build_receipt()
    assert receipt["current_promoted_theorems"] == []
    assert receipt["current_promoted_natural_laws"] == []
    assert any("Auto-caption" in item for item in receipt["negative_fixtures"])
    assert any(row["evidence_status"] == "EMPTY_CAPTURE_SOURCE_LEAD" for row in receipt["source_receipts"])


if __name__ == "__main__":
    test_receipt_shape()
    test_boundaries()
