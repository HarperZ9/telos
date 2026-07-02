"""Focused tests for pass 0145 multi-institution claim graph."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "compose_multi_institution_claim_graph.py"
sys.path.insert(0, str(SCRIPT.parent))
spec = importlib.util.spec_from_file_location("compose_multi_institution_claim_graph", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


def test_multi_institution_shape() -> None:
    receipt = module.build_receipt(live_tools=False)
    assert receipt["schema"] == "MultiInstitutionClaimGraphReceipt/v1"
    assert receipt["summary"]["institutions"] == 4
    assert receipt["summary"]["stored_captures"] >= 18
    assert receipt["summary"]["identity_matches"] == 4
    assert receipt["summary"]["repository_matches"] == 4
    assert receipt["summary"]["crossref_matches"] >= 3


def test_boundaries_and_warnings() -> None:
    receipt = module.build_receipt(live_tools=False)
    by_id = {item["id"]: item for item in receipt["institutions"]}
    assert by_id["cornell"]["crossref_status"] == "SOURCE_LEAD_ONLY"
    assert by_id["caltech"]["repository_status"] == "MATCH"
    assert len(receipt["negative_fixtures"]) == 10
    assert len(receipt["source_warnings"]) == 3
    assert receipt["current_promoted_theorems"] == []
    assert receipt["current_promoted_natural_laws"] == []


if __name__ == "__main__":
    test_multi_institution_shape()
    test_boundaries_and_warnings()
