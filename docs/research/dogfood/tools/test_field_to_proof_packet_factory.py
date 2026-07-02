"""Focused tests for pass 0123 field-to-proof packet factory."""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "tools" / "compose_field_to_proof_packet_factory.py"


def load_module():
    spec = importlib.util.spec_from_file_location("compose_field_to_proof_packet_factory", MODULE)
    if spec is None or spec.loader is None:
        raise AssertionError("module spec unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_field_factory_spec() -> None:
    module = load_module()
    artifact = module.compose()
    sources = artifact["source_matrix"]
    factories = artifact["field_factories"]
    experiment = artifact["coverage_experiment"]

    assert artifact["schema"] == "FieldToProofPacketFactorySpec/v1"
    assert artifact["status"] == "FIELD_TO_PROOF_PACKET_FACTORY_MATCH"
    assert artifact["source_bindings"]["youtube_growth_pass"] == "0121"
    assert artifact["source_bindings"]["runtime_layer_pass"] == "0122"
    assert len(sources) >= 16
    assert sum(row["chars"] >= 500 for row in sources) >= 14
    assert len(factories) >= 6
    assert factories[0]["market_product"] in {"AgentActionProofPacketFactory", "ResearchProofPacketFactory"}
    assert all(row["claim_status"] == "HYPOTHESIS" for row in factories)
    assert all(row["gap_status"] == "inferred" for row in factories)
    assert experiment["status"] == "MATCH"
    assert experiment["negative_fixture"]["status"] == "REJECTED"
    assert artifact["uniqueness_claim_status"] == "HYPOTHESIS_ONLY"
    assert artifact["unsupported_claim_count"] == 0
    assert artifact["current_promoted_natural_laws"] == []


if __name__ == "__main__":
    test_field_factory_spec()
