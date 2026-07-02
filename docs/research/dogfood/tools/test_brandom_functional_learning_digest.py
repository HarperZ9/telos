"""Focused tests for pass 0129 Brandom functional-learning digest."""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "tools" / "compose_brandom_functional_learning_digest.py"


def load_module():
    spec = importlib.util.spec_from_file_location("compose_brandom_functional_learning_digest", MODULE)
    if spec is None or spec.loader is None:
        raise AssertionError("module spec unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_brandom_functional_learning_digest() -> None:
    module = load_module()
    artifact = module.compose()
    terms = {row["term"]: row for row in artifact["term_signals"]}

    assert artifact["schema"] == "BrandomFunctionalLearningDigestReceipt/v1"
    assert artifact["status"] == "BRANDOM_FUNCTIONAL_LEARNING_DIGEST_MATCH"
    assert artifact["source_bindings"]["proof_suite_pass"] == "0128"
    assert len(artifact["source_receipts"]) >= 7
    assert any(row["kind"] == "transcript" for row in artifact["source_receipts"])
    assert all(row["raw_body_exported"] is False for row in artifact["source_receipts"])
    assert terms["Sellars"]["hits"] > 0
    assert terms["Kant"]["hits"] > 0
    assert terms["Hegel"]["hits"] > 0
    assert artifact["scorekeeping_fixture"]["status"] == "MATCH"
    assert "q" in artifact["scorekeeping_fixture"]["final_entitlements"]
    assert len(artifact["tool_hypotheses"]) >= 5
    assert all(row["status"] == "REJECTED" for row in artifact["negative_fixtures"])
    assert artifact["current_promoted_natural_laws"] == []


if __name__ == "__main__":
    test_brandom_functional_learning_digest()
