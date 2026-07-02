"""Focused tests for pass 0074 BuildLang source-ref receipt."""
from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMPOSER = ROOT / "tools" / "compose_buildlang_source_ref_receipt.py"


def load_composer():
    spec = importlib.util.spec_from_file_location("compose_buildlang_source_ref_receipt", COMPOSER)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_buildlang_source_ref_receipt_shape() -> None:
    module = load_composer()
    artifact = module.compose()

    assert artifact["schema"] == "BuildLangSourceRefReceipt/v1"
    assert artifact["pass"] == "0074"
    assert artifact["status"] == "BUILDLANG_SOURCE_REF_RECEIPT_MATCH"
    assert artifact["source_ref_count"] == len(module.SOURCE_PATHS)
    assert all(ref["exists"] and ref["sha256"] for ref in artifact["source_refs"])
    assert artifact["corpus_verify"]["status"] == "MATCH"
    assert artifact["corpus_verify"]["drift"] == 0
    assert artifact["program_count"] == 8
    assert artifact["production_backend_claim"] == "C backend only"
    assert artifact["unsupported_claim_count"] == 0
    assert len(artifact["negative_fixtures"]) >= 8


if __name__ == "__main__":
    test_buildlang_source_ref_receipt_shape()
