"""Focused tests for pass 0081 visual-truth proof-packet refresh."""
from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMPOSER = ROOT / "tools" / "compose_visual_truth_proof_packet_refresh.py"


def load_composer():
    spec = importlib.util.spec_from_file_location("compose_visual_truth_proof_packet_refresh", COMPOSER)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_visual_truth_proof_packet_refresh_shape() -> None:
    module = load_composer()
    artifact = module.compose()
    boundary = artifact["calibration_boundary"]

    assert artifact["schema"] == "VisualTruthProofPacketRefresh/v1"
    assert artifact["pass"] == "0081"
    assert artifact["status"] == "VISUAL_TRUTH_PROOF_PACKET_REFRESH_MATCH"
    assert artifact["proof_kit_source"]["metric_count"] == 4
    assert all(status == "PASS" for status in artifact["proof_kit_source"]["metric_statuses"])
    assert artifact["market_map"]["row_count"] == 8
    assert artifact["source_ref_count"] == 8
    assert artifact["targeted_regression"]["status"] == "MATCH"
    assert artifact["forum_route"]["status"] == "MATCH"
    assert all(boundary[key] is False for key in ["hardware_measurement_used", "display_state_mutated", "icc_profile_installed", "lut_written", "physical_calibration_claim"])
    assert artifact["unsupported_claim_count"] == 0
    assert artifact["current_promoted_natural_laws"] == []


if __name__ == "__main__":
    test_visual_truth_proof_packet_refresh_shape()
