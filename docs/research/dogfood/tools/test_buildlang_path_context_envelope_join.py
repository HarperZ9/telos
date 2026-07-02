"""Focused tests for pass 0079 BuildLang path-context envelope join."""
from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMPOSER = ROOT / "tools" / "compose_buildlang_path_context_envelope_join.py"


def load_composer():
    spec = importlib.util.spec_from_file_location("compose_buildlang_path_context_envelope_join", COMPOSER)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_buildlang_path_context_envelope_join_shape() -> None:
    module = load_composer()
    artifact = module.compose()
    context = artifact["path_context_component"]
    joined = artifact["joined_envelope"]

    assert artifact["schema"] == "BuildLangPathContextEnvelopeJoin/v1"
    assert artifact["pass"] == "0079"
    assert artifact["status"] == "BUILDLANG_PATH_CONTEXT_ENVELOPE_JOIN_MATCH"
    assert context["component_id"] == "index.path-selector.receipt.0078"
    assert context["source_ref_count"] == 128
    assert "build-universe" in context["missing_selector_rejections"]
    assert joined["component_digests"]["workspace_context"] == context["digest"]
    assert joined["root_context_fallback"] is False
    assert joined["path_scoped_context"] is True
    assert joined["adapter_fixture"] is True
    assert joined["native_index_path_selector"] is False
    assert artifact["unsupported_claim_count"] == 0


if __name__ == "__main__":
    test_buildlang_path_context_envelope_join_shape()
