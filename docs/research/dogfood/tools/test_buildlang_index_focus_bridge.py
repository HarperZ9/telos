"""Focused tests for pass 0076 BuildLang Index focus bridge."""
from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMPOSER = ROOT / "tools" / "compose_buildlang_index_focus_bridge.py"


def load_composer():
    spec = importlib.util.spec_from_file_location("compose_buildlang_index_focus_bridge", COMPOSER)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_buildlang_index_focus_bridge_shape() -> None:
    module = load_composer()
    artifact = module.compose()
    presence = artifact["index_map"]["requested_path_presence"]

    assert artifact["schema"] == "BuildLangIndexFocusBridge/v1"
    assert artifact["pass"] == "0076"
    assert artifact["status"] == "BUILDLANG_INDEX_FOCUS_BRIDGE_REQUIRED"
    assert artifact["root_context"]["status"] == "MATCH"
    assert artifact["root_context"]["source_refs_only"] is True
    assert artifact["root_context"]["source_ref_count"] >= 1
    assert artifact["path_scoped_context"] is False
    assert artifact["root_context_fallback"] is True
    assert artifact["bridge_required"] is True
    assert presence["buildlang"]["present"] is True
    assert presence["compiler"]["present"] is True
    assert presence["build-universe"]["present"] is False
    assert len(artifact["focus_probes"]) >= 4
    assert all(row["verdict"] == "EXPECTED_REJECT" for row in artifact["focus_probes"])
    assert artifact["unsupported_claim_count"] == 0
    assert len(artifact["negative_fixtures"]) >= 8


if __name__ == "__main__":
    test_buildlang_index_focus_bridge_shape()
