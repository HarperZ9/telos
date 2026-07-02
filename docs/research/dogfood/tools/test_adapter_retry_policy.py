"""Focused tests for pass 0146 adapter retry policy."""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "compose_adapter_retry_policy.py"
spec = importlib.util.spec_from_file_location("compose_adapter_retry_policy", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


def test_policy_shape() -> None:
    receipt = module.build_receipt(live_tools=False)
    assert receipt["schema"] == "AdapterRetryPolicyReceipt/v1"
    assert receipt["source_captures"] == 11
    assert receipt["summary"]["policy_rules"] == 12
    assert receipt["summary"]["scenario_fixtures"] == 10
    assert receipt["summary"]["negative_fixtures"] == 10


def test_retry_boundaries() -> None:
    receipt = module.build_receipt(live_tools=False)
    rules = {row["id"]: row for row in receipt["policy_rules"]}
    scenarios = {row["id"]: row for row in receipt["scenario_fixtures"]}
    assert rules["OPENALEX_API_KEY_CURRENT"]["status"] == "AUTH_POLICY"
    assert rules["NO_AUTO_RETRY_ON_HEADERLESS_503"]["status"] == "HALT_OR_OPERATOR_POLICY"
    assert scenarios["crossref_429_no_retry_after"]["promotion_allowed"] is False
    assert scenarios["openalex_mailto_only"]["rule"] == "OPENALEX_API_KEY_CURRENT"
    assert receipt["current_promoted_theorems"] == []
    assert receipt["current_promoted_natural_laws"] == []


if __name__ == "__main__":
    test_policy_shape()
    test_retry_boundaries()
