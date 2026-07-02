"""Focused tests for pass 0147 policy-aware institution queue."""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "compose_policy_aware_institution_queue.py"
spec = importlib.util.spec_from_file_location("compose_policy_aware_institution_queue", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


def test_queue_shape() -> None:
    receipt = module.build_receipt(live_tools=False)
    assert receipt["schema"] == "PolicyAwareInstitutionQueueReceipt/v1"
    assert receipt["summary"]["institutions"] == 4
    assert receipt["summary"]["source_captures"] == 16
    assert receipt["summary"]["crossref_samples"] == 4
    assert receipt["summary"]["negative_fixtures"] == 10


def test_policy_warnings() -> None:
    receipt = module.build_receipt(live_tools=False)
    by_id = {row["id"]: row for row in receipt["institutions"]}
    assert by_id["university-of-tokyo"]["identity"]["status"] == "RANKED_ALIAS_MATCH_WITH_WARNING"
    assert by_id["university-of-tokyo"]["identity"]["ror_rank_for_openalex"] == 2
    assert by_id["universidade-de-sao-paulo"]["repository"]["status"] == "SOURCE_LEAD_ONLY_ENDPOINT_DRIFT"
    assert by_id["universidade-de-sao-paulo"]["repository"]["sample_page_warning"] is True
    assert receipt["current_promoted_theorems"] == []
    assert receipt["current_promoted_natural_laws"] == []


if __name__ == "__main__":
    test_queue_shape()
    test_policy_warnings()
