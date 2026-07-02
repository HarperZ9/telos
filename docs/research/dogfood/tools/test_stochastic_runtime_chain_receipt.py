"""Focused tests for pass 0110 stochastic-runtime chain receipt."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPOSER = ROOT / "tools" / "compose_stochastic_runtime_chain_receipt.py"
ARTIFACT = ROOT / "schemas" / "stochastic-runtime-chain-receipt-pass-0110.json"


def load_module():
    spec = importlib.util.spec_from_file_location("compose_stochastic_runtime_chain_receipt", COMPOSER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_artifact() -> dict:
    if ARTIFACT.exists():
        return json.loads(ARTIFACT.read_text(encoding="utf-8"))
    return load_module().compose()


def test_stochastic_runtime_chain_receipt_shape() -> None:
    artifact = read_artifact()
    runtime = artifact["runtime_receipt"]
    adapter = artifact["adapter_contract"]
    diagnostics = runtime["diagnostics_receipt"]
    negative = runtime["negative_fixture_receipt"]
    youtube = artifact["youtube_binding"]

    assert artifact["schema"] == "StochasticRuntimeChainReceipt/v1"
    assert artifact["status"] == "STOCHASTIC_RUNTIME_CHAIN_RECEIPT_MATCH"
    assert artifact["source_bindings"]["stochastic_kernel_corpus_pass"] == "0109"
    assert artifact["source_bindings"]["youtube_roadmap_pass"] == "0102"
    assert adapter["missing_fields"] == []
    assert adapter["required_fields_satisfied"] == adapter["required_field_count"]
    assert runtime["kernel_family"] == "finite_markov_kernel"
    assert runtime["target_log_prob_digest"]
    assert runtime["transition_kernel_digest"] == artifact["selected_case"]["transition_kernel_digest"]
    assert runtime["calibration_layer"] == "exact_reversible_fixture"
    assert runtime["acceptance_correction"] == "identity"
    assert runtime["chain_seed_receipt"]["seed"] == 1109
    assert runtime["warmup_schedule_receipt"]["warmup_steps"] == 50
    assert diagnostics["exact_distribution_l1_distance_to_pi"] < 1e-9
    assert diagnostics["empirical_l1_distance_to_pi"] < 0.08
    assert diagnostics["stationary_residual_check"]["status"] == "MATCH"
    assert diagnostics["detailed_balance_or_invariance_check"]["status"] == "MATCH"
    assert negative["row_stochastic_not_stationary"]["status"] == "DRIFT_EXPECTED"
    assert negative["uncalibrated_random_walk_source_boundary"]["status"] == "REQUIRES_CALIBRATION"
    assert artifact["buildlang_target"]["status"] == "TARGET_INTERFACE_NOT_COMPILED"
    assert youtube["valid_video_count"] == 19
    assert youtube["raw_transcript_included"] is False
    assert artifact["unsupported_claim_count"] == 0
    assert artifact["current_promoted_natural_laws"] == []


if __name__ == "__main__":
    test_stochastic_runtime_chain_receipt_shape()
