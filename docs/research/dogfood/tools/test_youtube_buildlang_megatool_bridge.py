"""Focused tests for pass 0093 YouTube-to-BuildLang megatool bridge."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPOSER = ROOT / "tools" / "compose_youtube_buildlang_megatool_bridge.py"
ARTIFACT = ROOT / "schemas" / "youtube-buildlang-megatool-bridge-pass-0093.json"


def load_composer():
    spec = importlib.util.spec_from_file_location("compose_youtube_buildlang_megatool_bridge", COMPOSER)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_youtube_buildlang_megatool_bridge_shape() -> None:
    module = load_composer()
    artifact = json.loads(ARTIFACT.read_text(encoding="utf-8")) if ARTIFACT.exists() else module.compose()
    nodes = artifact["megatool_nodes"]

    assert artifact["schema"] == "YouTubeBuildLangMegatoolBridge/v1"
    assert artifact["pass"] == "0093"
    assert artifact["status"] == "YOUTUBE_BUILDLANG_MEGATOOL_BRIDGE_MATCH"
    assert artifact["source_bindings"]["youtube_pass"] == "0085"
    assert artifact["source_bindings"]["buildc_pass"] == "0092"
    assert artifact["source_summary"]["valid_video_count"] == 19
    assert artifact["source_summary"]["dominant_cluster"] == "enterprise_quantum_optimization"
    assert artifact["solver_summary"]["exact_optimum_value"] == 162
    assert artifact["solver_summary"]["scipy_exact_hit_count"] >= 1
    assert artifact["buildlang_summary"]["buildc_verify_check_count"] == 18
    assert artifact["buildlang_summary"]["buildc_measurement_count"] == 10
    assert len(nodes) == 7
    assert nodes[0]["cluster_id"] == "enterprise_quantum_optimization"
    assert artifact["primary_30_day_push"]["market_facing_product"] == "QuantumOptimizationWorkflowReceipt/v1"
    assert all(row["verification_status"] == "HYPOTHESIS_WITH_LOCAL_RECEIPTS" for row in nodes)
    assert all(tool["status"] == "MATCH" for tool in artifact["flagship_receipts"].values())
    assert artifact["unsupported_claim_count"] == 0
    assert artifact["current_promoted_natural_laws"] == []


if __name__ == "__main__":
    test_youtube_buildlang_megatool_bridge_shape()
