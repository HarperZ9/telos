"""Focused tests for pass 0143 registry adapter contracts."""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "compose_registry_adapter_contracts.py"
spec = importlib.util.spec_from_file_location("compose_registry_adapter_contracts", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


def test_contract_shape() -> None:
    receipt = module.build_receipt(live_tools=False)
    assert receipt["schema"] == "RegistryAdapterContractsReceipt/v1"
    assert len(receipt["contracts"]) == 2
    assert {row["adapter"] for row in receipt["contracts"]} == {"RepositoryDirectoryAdapter", "ScholarlyGraphAdapter"}
    assert len(receipt["repository_directory_records"]) >= 6
    assert len(receipt["scholarly_graph_records"]) >= 8


def test_controls_and_boundaries() -> None:
    receipt = module.build_receipt(live_tools=False)
    assert len(receipt["join_keys"]) >= 12
    assert len(receipt["negative_fixtures"]) == 10
    assert all(row["expected_status"] == "REJECT" for row in receipt["negative_fixtures"])
    assert receipt["current_promoted_theorems"] == []
    assert receipt["current_promoted_natural_laws"] == []


if __name__ == "__main__":
    test_contract_shape()
    test_controls_and_boundaries()
