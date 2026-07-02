"""Focused tests for pass 0109 stochastic-kernel corpus harness receipt."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPOSER = ROOT / "tools" / "compose_stochastic_kernel_corpus_harness_receipt.py"
ARTIFACT = ROOT / "schemas" / "stochastic-kernel-corpus-harness-receipt-pass-0109.json"


def load_module():
    spec = importlib.util.spec_from_file_location("compose_stochastic_kernel_corpus_harness_receipt", COMPOSER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_artifact() -> dict:
    if ARTIFACT.exists():
        return json.loads(ARTIFACT.read_text(encoding="utf-8"))
    return load_module().compose()


def by_id(rows: list[dict]) -> dict[str, dict]:
    return {row["case_id"]: row for row in rows}


def test_stochastic_kernel_corpus_harness_shape() -> None:
    artifact = read_artifact()
    summary = artifact["corpus_summary"]
    cases = by_id(artifact["kernel_cases"])
    adapter = artifact["adapter_spec"]
    youtube = artifact["youtube_binding"]
    market = artifact["market_binding"]

    assert artifact["schema"] == "StochasticKernelCorpusHarnessReceipt/v1"
    assert artifact["status"] == "STOCHASTIC_KERNEL_CORPUS_HARNESS_RECEIPT_MATCH"
    assert artifact["source_bindings"]["detailed_balance_pass"] == "0108"
    assert artifact["source_bindings"]["youtube_roadmap_pass"] == "0102"
    assert summary["case_count"] == 4
    assert summary["match_count"] == 1
    assert summary["drift_expected_count"] == 1
    assert summary["boundary_expected_count"] == 2
    assert summary["exact_kernel_count"] == 3

    reversible = cases["reversible_detailed_balance"]
    assert reversible["status"] == "MATCH"
    assert reversible["stationary_residual"] == ["0", "0", "0"]
    assert reversible["max_detailed_balance_residual"] == "0"

    cycle = cases["stationary_nonreversible_cycle"]
    assert cycle["status"] == "BOUNDARY_EXPECTED"
    assert cycle["stationary_residual"] == ["0", "0", "0"]
    assert cycle["max_detailed_balance_residual"] != "0"

    row_only = cases["row_stochastic_not_stationary"]
    assert row_only["status"] == "DRIFT_EXPECTED"
    assert row_only["row_sums"] == ["1", "1", "1"]
    assert row_only["stationary_residual"] != ["0", "0", "0"]

    uncalibrated = cases["uncalibrated_random_walk_source_boundary"]
    assert uncalibrated["status"] == "REQUIRES_CALIBRATION"
    assert "UncalibratedRandomWalk" in uncalibrated["source_url"]
    assert uncalibrated["calibration_required"] is True

    assert adapter["required_field_count"] >= 10
    for field in ["target_log_prob_digest", "transition_kernel_digest", "diagnostics_receipt", "negative_fixture_receipt"]:
        assert field in adapter["required_fields"]
    assert market["tool_count"] == 8
    assert youtube["valid_video_count"] == 19
    assert youtube["transcript_receipt_count"] == 19
    assert youtube["raw_transcript_included"] is False
    assert artifact["unsupported_claim_count"] == 0
    assert artifact["current_promoted_natural_laws"] == []


if __name__ == "__main__":
    test_stochastic_kernel_corpus_harness_shape()
