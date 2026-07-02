"""Focused tests for pass 0107 reaction-network corpus harness receipt."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPOSER = ROOT / "tools" / "compose_reaction_network_corpus_harness_receipt.py"
ARTIFACT = ROOT / "schemas" / "reaction-network-corpus-harness-receipt-pass-0107.json"


def load_module():
    spec = importlib.util.spec_from_file_location("compose_reaction_network_corpus_harness_receipt", COMPOSER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_artifact() -> dict:
    if ARTIFACT.exists():
        return json.loads(ARTIFACT.read_text(encoding="utf-8"))
    return load_module().compose()


def result_by_id(artifact: dict) -> dict:
    return {row["network_id"]: row for row in artifact["network_results"]}


def test_reaction_network_corpus_harness_receipt_shape() -> None:
    artifact = read_artifact()
    results = result_by_id(artifact)
    buildlang = artifact["buildlang_runtime_bridge"]
    youtube = artifact["youtube_signal_binding"]
    summary = artifact["corpus_summary"]
    assert artifact["schema"] == "ReactionNetworkCorpusHarnessReceipt/v1"
    assert artifact["status"] == "REACTION_NETWORK_CORPUS_HARNESS_RECEIPT_MATCH"
    assert artifact["source_bindings"]["stoichiometric_pass"] == "0106"
    assert artifact["source_bindings"]["buildlang_native_pass"] == "0095"
    assert artifact["source_bindings"]["youtube_scorecard_pass"] == "0096"
    assert summary["network_count"] == 4
    assert summary["match_count"] == 3
    assert summary["drift_expected_count"] == 1
    assert summary["derived_invariant_count"] >= 4
    assert results["closed_cycle_abc"]["candidate_checks"][0]["residual"] == [0, 0, 0]
    assert results["reversible_dimerization"]["candidate_checks"][0]["vector"] == [1, 2]
    assert results["reversible_dimerization"]["candidate_checks"][0]["residual"] == [0, 0]
    assert results["enzyme_product_skeleton"]["basis_dimension"] == 2
    assert all(check["residual_zero"] for check in results["enzyme_product_skeleton"]["candidate_checks"])
    assert results["open_degradation"]["status"] == "DRIFT_EXPECTED"
    assert results["open_degradation"]["candidate_checks"][0]["residual"] == [-1]
    assert results["open_degradation"]["candidate_checks"][0]["residual_zero"] is False
    assert buildlang["status"] == "TARGET_SPECIFIED_WITH_EXISTING_BUILDC_RECEIPT"
    assert buildlang["compiler"] == "buildc"
    assert buildlang["native_pass"] == "0095"
    assert buildlang["verify_check_count"] == 18
    assert "residual_zero_check" in buildlang["required_kernel_receipts"]
    assert youtube["buildlang_scientific_runtime_video_count"] == 14
    assert youtube["valid_video_count"] == 19
    assert artifact["unsupported_claim_count"] == 0
    assert artifact["current_promoted_natural_laws"] == []


if __name__ == "__main__":
    test_reaction_network_corpus_harness_receipt_shape()
