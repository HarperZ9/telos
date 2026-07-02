"""Focused tests for pass 0091 BuildLang corpus-to-Crucible adapter."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPOSER = ROOT / "tools" / "compose_buildlang_corpus_crucible_adapter.py"
ARTIFACT = ROOT / "schemas" / "buildlang-corpus-crucible-adapter-pass-0091.json"


def load_composer():
    spec = importlib.util.spec_from_file_location("compose_buildlang_corpus_crucible_adapter", COMPOSER)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_buildlang_corpus_crucible_adapter_shape() -> None:
    module = load_composer()
    artifact = json.loads(ARTIFACT.read_text(encoding="utf-8")) if ARTIFACT.exists() else module.compose()
    adapter = artifact["crucible_adapter"]

    assert artifact["schema"] == "BuildLangCorpusCrucibleAdapterReceipt/v1"
    assert artifact["pass"] == "0091"
    assert artifact["status"] == "BUILDLANG_CORPUS_CRUCIBLE_ADAPTER_MATCH"
    assert artifact["prior_binding"]["source_pass"] == "0090"
    assert artifact["proof_surface_binding"]["source_pass"] == "0080"
    assert artifact["repo_state"]["exists"] is True
    assert artifact["buildc_corpus_run"]["status"] == "MATCH"
    assert artifact["buildc_corpus_run"]["exit_code"] == 0
    assert artifact["buildc_corpus_run"]["match"] == 10
    assert artifact["buildc_corpus_run"]["drift"] == 0
    assert adapter["adapter_id"] == "buildc_corpus_to_crucible_measurements"
    assert adapter["measurement_count"] == 10
    assert adapter["match"] == 10
    assert adapter["drift"] == 0
    assert all(item["status"] == "MATCH" for item in adapter["measurements"])
    assert all(item["deviation"] == 0.0 for item in adapter["measurements"])
    assert all(receipt["status"] == "MATCH" for receipt in artifact["flagship_receipts"].values())
    assert artifact["promotion_boundary"]["adapter_only"] is True
    assert artifact["promotion_boundary"]["julia_replacement_claim"] is False
    assert artifact["promotion_boundary"]["scientific_discovery_claim"] is False
    assert artifact["promotion_boundary"]["new_natural_law_claim"] is False
    assert artifact["unsupported_claim_count"] == 0
    assert artifact["current_promoted_natural_laws"] == []


if __name__ == "__main__":
    test_buildlang_corpus_crucible_adapter_shape()
