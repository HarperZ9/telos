"""Focused tests for pass 0108 detailed-balance Markov receipt."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPOSER = ROOT / "tools" / "compose_detailed_balance_markov_receipt.py"
ARTIFACT = ROOT / "schemas" / "detailed-balance-markov-receipt-pass-0108.json"


def load_module():
    spec = importlib.util.spec_from_file_location("compose_detailed_balance_markov_receipt", COMPOSER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_artifact() -> dict:
    if ARTIFACT.exists():
        return json.loads(ARTIFACT.read_text(encoding="utf-8"))
    return load_module().compose()


def test_detailed_balance_markov_receipt_shape() -> None:
    artifact = read_artifact()
    proof = artifact["proof"]
    positive = artifact["reversible_kernel"]
    row_only = artifact["negative_fixtures"]["row_stochastic_not_stationary"]
    circulation = artifact["negative_fixtures"]["stationary_not_reversible"]
    market = artifact["market_surface"]
    assert artifact["schema"] == "DetailedBalanceMarkovReceipt/v1"
    assert artifact["status"] == "DETAILED_BALANCE_MARKOV_RECEIPT_MATCH"
    assert artifact["source_bindings"]["reaction_corpus_pass"] == "0107"
    assert proof["symbolic_step"] == "sum_i pi_i P_ij = sum_i pi_j P_ji = pi_j"
    assert positive["pi"] == ["1/2", "1/3", "1/6"]
    assert positive["max_detailed_balance_residual"] == "0"
    assert positive["stationary_residual"] == ["0", "0", "0"]
    assert positive["simulation_probe"]["steps"] >= 100
    assert positive["simulation_probe"]["l1_distance_to_pi"] < 1e-6
    assert row_only["row_sums"] == ["1", "1", "1"]
    assert row_only["stationary_residual"] != ["0", "0", "0"]
    assert row_only["status"] == "DRIFT_EXPECTED"
    assert circulation["stationary_residual"] == ["0", "0", "0"]
    assert circulation["max_detailed_balance_residual"] != "0"
    assert circulation["status"] == "BOUNDARY_EXPECTED"
    assert market["tool_count"] >= 8
    assert market["gap_status"] == "hypothesis"
    assert artifact["law_candidate"]["status"] == "LAW_CANDIDATE"
    assert artifact["unsupported_claim_count"] == 0
    assert artifact["current_promoted_natural_laws"] == []


if __name__ == "__main__":
    test_detailed_balance_markov_receipt_shape()
