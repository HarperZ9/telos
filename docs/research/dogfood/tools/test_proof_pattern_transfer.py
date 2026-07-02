"""Focused tests for pass 0132 proof pattern transfer."""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "tools" / "compose_proof_pattern_transfer.py"


def load_module():
    spec = importlib.util.spec_from_file_location("compose_proof_pattern_transfer", MODULE)
    if spec is None or spec.loader is None:
        raise AssertionError("module spec unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_proof_pattern_transfer() -> None:
    module = load_module()
    artifact = module.compose()
    fixtures = artifact["positive_fixtures"]
    counterexamples = artifact["counterexample_fixtures"]

    assert artifact["schema"] == "ProofPatternTransferReceipt/v1"
    assert artifact["status"] == "PROOF_PATTERN_TRANSFER_MATCH"
    assert artifact["source_bindings"]["tradition_atlas_pass"] == "0131"
    assert len(artifact["source_receipts"]) >= 6
    assert all(row["raw_body_exported"] is False for row in artifact["source_receipts"])
    assert len(fixtures) >= 2 and all(row["status"] == "MATCH" for row in fixtures)
    assert fixtures[0]["derivative_residual"] == 0.0
    assert fixtures[0]["orthogonal_residual"] < 1e-12
    assert fixtures[0]["norm_delta"] < 1e-12
    assert len(counterexamples) >= 2
    assert all(row["status"] == "REJECTED" for row in counterexamples)
    assert artifact["law_candidate"]["status"] == "LAW_CANDIDATE"
    assert artifact["law_candidate"]["promotion_status"] == "NOT_PROMOTED"
    assert all(row["status"] == "REJECTED" for row in artifact["negative_fixtures"])
    assert artifact["current_promoted_natural_laws"] == []


if __name__ == "__main__":
    test_proof_pattern_transfer()
