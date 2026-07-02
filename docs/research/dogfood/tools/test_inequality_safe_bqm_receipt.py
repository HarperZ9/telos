"""Focused tests for pass 0101 inequality-safe BQM receipt."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPOSER = ROOT / "tools" / "compose_inequality_safe_bqm_receipt.py"
ARTIFACT = ROOT / "schemas" / "inequality-safe-bqm-receipt-pass-0101.json"


def load_composer():
    spec = importlib.util.spec_from_file_location("compose_inequality_safe_bqm_receipt", COMPOSER)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_inequality_safe_bqm_receipt_shape() -> None:
    module = load_composer()
    artifact = json.loads(ARTIFACT.read_text(encoding="utf-8")) if ARTIFACT.exists() else module.compose()
    results = artifact["results"]

    assert artifact["schema"] == "InequalitySafeBQMReceipt/v1"
    assert artifact["pass"] == "0101"
    assert artifact["status"] == "INEQUALITY_SAFE_BQM_RECEIPT_MATCH"
    assert artifact["source_bindings"]["ocean_pass"] == "0100"
    assert artifact["temp_venv"]["cleaned"] is True
    assert results["true_optimum"]["value"] == 10
    assert results["true_optimum"]["weight"] == 3
    assert results["equality_penalty"]["feasible"] is False
    assert results["equality_penalty"]["value"] == 19
    assert results["slack_penalty"]["feasible"] is True
    assert results["slack_penalty"]["value"] == 10
    assert results["slack_penalty"]["weight"] == 3
    assert artifact["law_candidate"]["status"] == "LAW_CANDIDATE"
    assert len(artifact["measurements"]) == 8
    assert all(row["status"] == "MATCH" for row in artifact["measurements"])
    assert all(tool["status"] == "MATCH" for tool in artifact["flagship_receipts"].values())
    assert artifact["unsupported_claim_count"] == 0
    assert artifact["current_promoted_natural_laws"] == []


if __name__ == "__main__":
    test_inequality_safe_bqm_receipt_shape()
