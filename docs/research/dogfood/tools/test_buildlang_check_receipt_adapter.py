"""Focused tests for pass 0092 BuildLang check receipt adapter."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPOSER = ROOT / "tools" / "compose_buildlang_check_receipt_adapter.py"
ARTIFACT = ROOT / "schemas" / "buildlang-check-receipt-adapter-pass-0092.json"


def load_composer():
    spec = importlib.util.spec_from_file_location("compose_buildlang_check_receipt_adapter", COMPOSER)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_buildlang_check_receipt_adapter_shape() -> None:
    module = load_composer()
    artifact = json.loads(ARTIFACT.read_text(encoding="utf-8")) if ARTIFACT.exists() else module.compose()
    receipt = artifact["check_receipt"]
    adapter = artifact["crucible_adapter"]

    assert artifact["schema"] == "BuildLangCheckReceiptAdapter/v1"
    assert artifact["pass"] == "0092"
    assert artifact["status"] == "BUILDLANG_CHECK_RECEIPT_ADAPTER_MATCH"
    assert artifact["prior_binding"]["source_pass"] == "0091"
    assert artifact["check_command"]["exit_code"] == 0
    assert artifact["verify_command"]["exit_code"] == 0
    assert receipt["schema"] == "buildlang-check-receipt/v1"
    assert receipt["compiler"] == "buildc"
    assert receipt["status"] == "passed"
    assert receipt["source_digest"]["algorithm"] == "sha256"
    assert len(receipt["source_digest"]["hex"]) == 64
    assert receipt["declared_effects"]["main"] == ["Console"]
    assert receipt["observed_capabilities"]["main"]["Console"] == ["println!"]
    assert receipt["policy"]["profile"] == "console-only"
    assert receipt["policy"]["status"] == "passed"
    assert artifact["verify_report"]["schema"] == "buildlang-receipt-verification/v1"
    assert artifact["verify_report"]["status"] == "passed"
    assert artifact["verify_summary"]["all_required_passed"] is True
    assert adapter["measurement_count"] == 10
    assert adapter["match"] == 10
    assert adapter["drift"] == 0
    assert all(row["status"] == "MATCH" for row in adapter["measurements"])
    assert all(tool["status"] == "MATCH" for tool in artifact["flagship_receipts"].values())
    assert artifact["promotion_boundary"]["source_receipt_adapter_only"] is True
    assert artifact["promotion_boundary"]["language_replacement_claim"] is False
    assert artifact["promotion_boundary"]["scientific_discovery_claim"] is False
    assert artifact["promotion_boundary"]["new_natural_law_claim"] is False
    assert artifact["unsupported_claim_count"] == 0
    assert artifact["current_promoted_natural_laws"] == []


if __name__ == "__main__":
    test_buildlang_check_receipt_adapter_shape()
