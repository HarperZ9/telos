"""Focused tests for pass 0142 source registry federation."""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "compose_source_registry_federation.py"
spec = importlib.util.spec_from_file_location("compose_source_registry_federation", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


def test_registry_federation_shape() -> None:
    receipt = module.build_receipt()
    assert receipt["schema"] == "SourceRegistryFederationReceipt/v1"
    assert receipt["status"] == "SOURCE_REGISTRY_FEDERATION_MATCH"
    assert receipt["gather_summary"]["total_source_rows"] >= 33
    assert receipt["gather_summary"]["usable_captures"] >= 20
    assert len(receipt["registry_layers"]) == 10
    assert len(receipt["adapter_requirements"]) == 15


def test_boundaries_and_warnings() -> None:
    receipt = module.build_receipt()
    assert receipt["source_quality_warnings"]
    assert len(receipt["world_problem_workbenches"]) == 8
    assert len(receipt["negative_fixtures"]) == 10
    assert receipt["current_promoted_theorems"] == []
    assert receipt["current_promoted_natural_laws"] == []


if __name__ == "__main__":
    test_registry_federation_shape()
    test_boundaries_and_warnings()
