"""Focused tests for pass 0144 one-institution claim graph."""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "compose_one_institution_claim_graph.py"
spec = importlib.util.spec_from_file_location("compose_one_institution_claim_graph", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


def test_live_graph_shape() -> None:
    receipt = module.build_receipt(live_tools=False)
    assert receipt["schema"] == "OneInstitutionClaimGraphReceipt/v1"
    assert receipt["institution"]["expected_ror"] == receipt["organization_identity"]["ror"]["id"]
    assert receipt["organization_identity"]["openalex"]["ror"] == receipt["organization_identity"]["ror"]["id"]
    assert receipt["gather_summary"]["live_captures"] >= 6
    assert receipt["gather_summary"]["protocol_docs"] >= 5


def test_boundaries_and_warnings() -> None:
    receipt = module.build_receipt(live_tools=False)
    statuses = {row["join"]: row["status"] for row in receipt["join_verdicts"]}
    assert statuses["datacite_dataset_relation"] == "SOURCE_LEAD_ONLY"
    assert len(receipt["negative_fixtures"]) == 10
    assert len(receipt["source_warnings"]) == 3
    assert receipt["current_promoted_theorems"] == []
    assert receipt["current_promoted_natural_laws"] == []


if __name__ == "__main__":
    test_live_graph_shape()
    test_boundaries_and_warnings()
