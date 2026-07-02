"""Focused tests for pass 0148 live source router probes."""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "compose_live_source_router_probes.py"
spec = importlib.util.spec_from_file_location("compose_live_source_router_probes", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


def test_router_shape() -> None:
    receipt = module.build_receipt(live_tools=False)
    assert receipt["schema"] == "LiveSourceRouterProbeReceipt/v1"
    assert receipt["summary"]["routes"] == 25
    assert receipt["summary"]["families"] >= 7
    assert receipt["summary"]["live_query_matches"] >= 17
    assert receipt["summary"]["negative_fixtures"] == 10


def test_failure_policy() -> None:
    receipt = module.build_receipt(live_tools=False)
    rows = {row["id"]: row for row in receipt["routes"]}
    assert rows["openalex_works"]["warning"] == "HTTP_503_RETRYABLE"
    assert rows["base_oai"]["status"] == "FALLBACK_DOCS_MATCH_WITH_PRIMARY_WARNING"
    assert rows["chemrxiv_public_api"]["status"] == "SOURCE_LEAD_ONLY_WARNING"
    assert rows["cambridge_apollo_oai"]["status"] == "FALLBACK_DOCS_MATCH_WITH_PRIMARY_WARNING"
    assert receipt["current_promoted_theorems"] == []
    assert receipt["current_promoted_natural_laws"] == []


if __name__ == "__main__":
    test_router_shape()
    test_failure_policy()
