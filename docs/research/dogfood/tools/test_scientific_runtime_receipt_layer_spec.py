"""Focused tests for pass 0122 scientific runtime receipt layer."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPOSER = ROOT / "tools" / "compose_scientific_runtime_receipt_layer_spec.py"
ARTIFACT = ROOT / "schemas" / "scientific-runtime-receipt-layer-spec-pass-0122.json"


def load_module():
    spec = importlib.util.spec_from_file_location("compose_scientific_runtime_receipt_layer_spec", COMPOSER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_artifact() -> dict:
    if ARTIFACT.exists():
        return json.loads(ARTIFACT.read_text(encoding="utf-8"))
    return load_module().compose()


def test_scientific_runtime_receipt_layer_shape() -> None:
    artifact = read_artifact()
    sources = artifact["source_matrix"]
    experiment = artifact["long_horizon_experiment"]

    assert artifact["schema"] == "ScientificRuntimeReceiptLayerSpec/v1"
    assert artifact["status"] == "SCIENTIFIC_RUNTIME_RECEIPT_LAYER_MATCH"
    assert artifact["source_bindings"]["growth_vector_pass"] == "0121"
    assert artifact["source_bindings"]["runtime_branch_pass"] == "0120"
    assert len(sources) >= 17
    assert sum(row["local_gather_status"].startswith("GATHER_VERIFIED") for row in sources) >= 14
    assert all(row["gap_status"] == "inferred" for row in sources)
    assert len(artifact["receipt_contract"]) >= 8
    assert len(experiment["exact_cases"]) == 3
    assert all(row["exact_invariant_for_all_steps_by_induction"] for row in experiment["exact_cases"])
    assert all(h["status"] == "MATCH" for row in experiment["exact_cases"] for h in row["float_horizons"])
    assert experiment["negative_fixture"]["status"] == "MATCH"
    assert experiment["promoted_law_status"] == "NOT_PROMOTED"
    assert artifact["unsupported_claim_count"] == 0
    assert artifact["current_promoted_natural_laws"] == []
    assert "does not prove BuildLang" in artifact["non_promotion_statement"]
    assert all(row["status"] == "MATCH" for row in artifact["flagship_receipts"].values())


if __name__ == "__main__":
    test_scientific_runtime_receipt_layer_shape()
