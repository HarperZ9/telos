"""Focused tests for pass 0124 agent action proof-packet adapter."""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "tools" / "compose_agent_action_proof_packet_factory_adapter.py"


def load_module():
    spec = importlib.util.spec_from_file_location("compose_agent_action_proof_packet_factory_adapter", MODULE)
    if spec is None or spec.loader is None:
        raise AssertionError("module spec unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_agent_action_adapter_spec() -> None:
    module = load_module()
    artifact = module.compose()
    receipts = artifact["action_receipts"]
    negatives = artifact["negative_fixtures"]
    required = set(artifact["adapter_contract_fields"])

    assert artifact["schema"] == "AgentActionProofPacketFactoryAdapter/v1"
    assert artifact["status"] == "AGENT_ACTION_PROOF_PACKET_FACTORY_ADAPTER_MATCH"
    assert artifact["source_bindings"]["factory_pass"] == "0123"
    assert artifact["source_bindings"]["adapter_matrix_pass"] == "0064"
    assert len(artifact["source_matrix"]) >= 7
    assert len(receipts) == 5
    assert all(required.issubset(receipt) for receipt in receipts)
    assert all(receipt["adapter_status"] == "MATCH" for receipt in receipts)
    assert all(receipt["verification_verdict"] == "MATCH" for receipt in receipts)
    assert all(receipt["action_admission"]["decision"] == "admit" for receipt in receipts)
    assert len(negatives) == 4
    assert all(row["status"] == "REJECTED" and row["failures"] for row in negatives)
    assert artifact["adapter_claim_status"] == "HYPOTHESIS_WITH_EXECUTABLE_FIXTURES"
    assert artifact["unsupported_claim_count"] == 0
    assert artifact["current_promoted_natural_laws"] == []


if __name__ == "__main__":
    test_agent_action_adapter_spec()
