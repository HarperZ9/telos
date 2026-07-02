"""Focused tests for pass 0080 BuildLang proof-packet demo surface."""
from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMPOSER = ROOT / "tools" / "compose_buildlang_proof_packet_demo_surface.py"


def load_composer():
    spec = importlib.util.spec_from_file_location("compose_buildlang_proof_packet_demo_surface", COMPOSER)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_buildlang_proof_packet_demo_surface_shape() -> None:
    module = load_composer()
    artifact = module.compose()

    assert artifact["schema"] == "BuildLangProofPacketDemoSurface/v1"
    assert artifact["pass"] == "0080"
    assert artifact["status"] == "BUILDLANG_PROOF_PACKET_DEMO_SURFACE_MATCH"
    assert artifact["source_intake"]["source_ref_count"] == 13
    assert artifact["workspace_context"]["path_scoped_context"] is True
    assert artifact["workspace_context"]["root_context_fallback"] is False
    assert artifact["workspace_context"]["source_ref_count"] == 128
    assert artifact["workspace_context"]["adapter_fixture"] is True
    assert artifact["workspace_context"]["native_index_path_selector"] is False
    assert artifact["live_buildc_corpus"]["status"] == "MATCH"
    assert artifact["forum_route"]["status"] == "MATCH"
    assert len(artifact["negative_fixtures"]) >= 9
    assert artifact["unsupported_claim_count"] == 0
    assert artifact["current_promoted_natural_laws"] == []


if __name__ == "__main__":
    test_buildlang_proof_packet_demo_surface_shape()
