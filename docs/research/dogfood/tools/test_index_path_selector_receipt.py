"""Focused tests for pass 0078 Index path-selector receipt."""
from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMPOSER = ROOT / "tools" / "compose_index_path_selector_receipt.py"


def load_composer():
    spec = importlib.util.spec_from_file_location("compose_index_path_selector_receipt", COMPOSER)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_index_path_selector_receipt_shape() -> None:
    module = load_composer()
    artifact = module.compose()
    results = {row["selector"]: row for row in artifact["selector_results"]}

    assert artifact["schema"] == "IndexPathSelectorReceipt/v1"
    assert artifact["pass"] == "0078"
    assert artifact["status"] == "INDEX_PATH_SELECTOR_RECEIPT_FIXTURE_MATCH"
    assert results["buildlang"]["status"] == "MATCH"
    assert results["compiler"]["status"] == "MATCH"
    assert results["build-universe"]["status"] == "REJECT"
    assert artifact["selected_selector_count"] == 2
    assert artifact["rejected_selector_count"] == 1
    assert artifact["source_ref_count"] >= 2
    assert artifact["raw_source_included"] is False
    assert artifact["source_refs_only"] is True
    assert "target" in artifact["excluded_dirs"]
    assert artifact["contract_schema"] == "IndexPathSelectorReceipt/v1"
    assert artifact["unsupported_claim_count"] == 0


if __name__ == "__main__":
    test_index_path_selector_receipt_shape()
