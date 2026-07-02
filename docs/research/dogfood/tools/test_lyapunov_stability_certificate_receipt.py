"""Focused tests for pass 0112 Lyapunov stability certificate receipt."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPOSER = ROOT / "tools" / "compose_lyapunov_stability_certificate_receipt.py"
ARTIFACT = ROOT / "schemas" / "lyapunov-stability-certificate-receipt-pass-0112.json"


def load_module():
    spec = importlib.util.spec_from_file_location("compose_lyapunov_stability_certificate_receipt", COMPOSER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_artifact() -> dict:
    if ARTIFACT.exists():
        return json.loads(ARTIFACT.read_text(encoding="utf-8"))
    return load_module().compose()


def test_lyapunov_stability_certificate_shape() -> None:
    artifact = read_artifact()
    stable = artifact["stable_certificate"]
    unstable = artifact["negative_fixtures"]["unstable_spectral_fixture"]
    bad = artifact["negative_fixtures"]["bad_certificate_fixture"]
    youtube = artifact["youtube_binding"]

    assert artifact["schema"] == "LyapunovStabilityCertificateReceipt/v1"
    assert artifact["status"] == "LYAPUNOV_STABILITY_CERTIFICATE_RECEIPT_MATCH"
    assert artifact["source_bindings"]["runtime_suite_pass"] == "0111"
    assert artifact["source_bindings"]["youtube_roadmap_pass"] == "0102"
    assert len(artifact["source_anchors"]) >= 8
    assert stable["A"] == [["1/2", "0"], ["0", "1/3"]]
    assert stable["Q"] == [["1", "0"], ["0", "1"]]
    assert stable["P"] == [["4/3", "0"], ["0", "9/8"]]
    assert stable["max_spectral_radius_abs"] == "1/2"
    assert stable["positive_definite"] is True
    assert stable["lyapunov_residual"] == [["0", "0"], ["0", "0"]]
    assert stable["max_identity_residual"] == "0"
    assert all(row["status"] == "MATCH" for row in stable["energy_samples"])
    assert unstable["classification"] == "PD_FAIL_EXPECTED"
    assert unstable["positive_definite"] is False
    assert unstable["candidate_P"][0][0] == "-25/11"
    assert bad["classification"] == "RESIDUAL_DRIFT_EXPECTED"
    assert bad["max_identity_residual"] != "0"
    assert artifact["market_surface"]["tool_count"] >= 8
    assert artifact["market_surface"]["gap_status"] == "hypothesis"
    assert youtube["valid_video_count"] == 19
    assert youtube["raw_transcript_included"] is False
    assert artifact["unsupported_claim_count"] == 0
    assert artifact["current_promoted_natural_laws"] == []


if __name__ == "__main__":
    test_lyapunov_stability_certificate_shape()
