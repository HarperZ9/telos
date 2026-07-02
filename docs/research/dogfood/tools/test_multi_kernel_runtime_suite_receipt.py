"""Focused tests for pass 0111 multi-kernel runtime suite receipt."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPOSER = ROOT / "tools" / "compose_multi_kernel_runtime_suite_receipt.py"
ARTIFACT = ROOT / "schemas" / "multi-kernel-runtime-suite-receipt-pass-0111.json"


def load_module():
    spec = importlib.util.spec_from_file_location("compose_multi_kernel_runtime_suite_receipt", COMPOSER)
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


def test_multi_kernel_runtime_suite_shape() -> None:
    artifact = read_artifact()
    summary = artifact["suite_summary"]
    results = by_id(artifact["case_results"])
    youtube = artifact["youtube_binding"]

    assert artifact["schema"] == "MultiKernelRuntimeSuiteReceipt/v1"
    assert artifact["status"] == "MULTI_KERNEL_RUNTIME_SUITE_RECEIPT_MATCH"
    assert artifact["source_bindings"]["runtime_chain_pass"] == "0110"
    assert artifact["source_bindings"]["stochastic_kernel_corpus_pass"] == "0109"
    assert artifact["source_bindings"]["youtube_roadmap_pass"] == "0102"
    assert summary["case_count"] == 3
    assert summary["match_count"] == 1
    assert summary["drift_expected_count"] == 1
    assert summary["boundary_expected_count"] == 1
    assert summary["adapter_missing_field_total"] == 0

    reversible = results["reversible_detailed_balance"]
    assert reversible["classification"] == "MATCH"
    assert reversible["adapter_contract"]["missing_fields"] == []
    assert reversible["stationary_residual_check"]["status"] == "MATCH"
    assert reversible["detailed_balance_or_invariance_check"]["status"] == "MATCH"
    assert reversible["exact_distribution_l1_distance_to_declared_pi"] < 1e-9

    row_only = results["row_stochastic_not_stationary"]
    assert row_only["classification"] == "DRIFT_EXPECTED"
    assert row_only["row_sums"] == ["1", "1", "1"]
    assert row_only["stationary_residual_check"]["status"] == "DRIFT"
    assert row_only["exact_distribution_l1_distance_to_declared_pi"] > 0.1

    cycle = results["stationary_nonreversible_cycle"]
    assert cycle["classification"] == "BOUNDARY_EXPECTED"
    assert cycle["stationary_residual_check"]["status"] == "MATCH"
    assert cycle["detailed_balance_or_invariance_check"]["status"] == "BOUNDARY_EXPECTED"
    assert cycle["max_detailed_balance_residual"] == "1/3"

    assert artifact["source_boundary_receipts"]["uncalibrated_random_walk_source_boundary"]["status"] == "REQUIRES_CALIBRATION"
    assert artifact["market_binding"]["tool_count"] == 8
    assert youtube["valid_video_count"] == 19
    assert youtube["raw_transcript_included"] is False
    assert artifact["unsupported_claim_count"] == 0
    assert artifact["current_promoted_natural_laws"] == []


if __name__ == "__main__":
    test_multi_kernel_runtime_suite_shape()
