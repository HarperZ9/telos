"""Focused tests for pass 0104 AI4Science claim-to-experiment receipt."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPOSER = ROOT / "tools" / "compose_ai4science_claim_to_experiment_receipt.py"
ARTIFACT = ROOT / "schemas" / "ai4science-claim-to-experiment-receipt-pass-0104.json"


def load_module():
    spec = importlib.util.spec_from_file_location("compose_ai4science_claim_to_experiment_receipt", COMPOSER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_artifact() -> dict:
    if ARTIFACT.exists():
        return json.loads(ARTIFACT.read_text(encoding="utf-8"))
    return load_module().compose()


def test_ai4science_claim_to_experiment_receipt_shape() -> None:
    artifact = read_artifact()
    fields = artifact["minimum_packet_fields"]
    gates = artifact["promotion_gates"]
    assert artifact["schema"] == "AI4ScienceClaimToExperimentReceipt/v1"
    assert artifact["status"] == "AI4SCIENCE_CLAIM_TO_EXPERIMENT_RECEIPT_MATCH"
    assert artifact["source_bindings"]["roadmap_pass"] == "0102"
    assert artifact["source_bindings"]["youtube_pass"] == "0085"
    assert artifact["source_summary"]["source_count"] >= 8
    assert artifact["source_summary"]["official_or_primary_count"] >= 8
    assert artifact["market_gap"]["gap_status"] == "inferred"
    assert "source_claim" in fields
    assert "experiment_or_simulation_protocol" in fields
    assert "measurement_receipt" in fields
    assert "negative_result_path" in fields
    assert gates["rejects_unmeasured_discovery_claim"] is True
    assert gates["requires_reproduction_status"] is True
    assert gates["requires_human_review"] is True
    assert len(artifact["source_to_receipt_map"]) >= 8
    assert len(artifact["next_experiments"]) == 3
    assert artifact["unsupported_claim_count"] == 0
    assert artifact["current_promoted_natural_laws"] == []


if __name__ == "__main__":
    test_ai4science_claim_to_experiment_receipt_shape()
