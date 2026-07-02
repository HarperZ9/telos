"""Focused tests for pass 0075 BuildLang domain-envelope join."""
from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMPOSER = ROOT / "tools" / "compose_buildlang_domain_envelope_join.py"


def load_composer():
    spec = importlib.util.spec_from_file_location("compose_buildlang_domain_envelope_join", COMPOSER)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_buildlang_domain_envelope_join_shape() -> None:
    module = load_composer()
    artifact = module.compose()
    joined = artifact["joined_envelope"]
    source = artifact["buildlang_source_component"]

    assert artifact["schema"] == "BuildLangDomainEnvelopeJoin/v1"
    assert artifact["pass"] == "0075"
    assert artifact["status"] == "BUILDLANG_DOMAIN_ENVELOPE_JOIN_MATCH"
    assert artifact["domain_id"] == "buildlang_buildc"
    assert artifact["domain_source_ref_replaced"] is True
    assert joined["domain_id"] == "buildlang_buildc"
    assert joined["domain_source_ref_replaced"] is True
    assert joined["component_digests"]["source_intake"] == source["digest"]
    assert source["component_id"] == "buildlang.source-ref.receipt.0074"
    assert source["corpus_verify_status"] == "MATCH"
    assert source["production_backend_claim"] == "C backend only"
    assert joined["root_context_fallback"] is True
    assert joined["path_scoped_context"] is False
    assert artifact["unsupported_claim_count"] == 0
    assert len(artifact["negative_fixtures"]) >= 8


if __name__ == "__main__":
    test_buildlang_domain_envelope_join_shape()
