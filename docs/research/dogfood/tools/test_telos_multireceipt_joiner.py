"""Focused tests for pass 0069 Telos multi-receipt joiner."""
from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMPOSER = ROOT / "tools" / "compose_telos_multireceipt_joiner.py"


def load_composer():
    spec = importlib.util.spec_from_file_location("compose_telos_multireceipt_joiner", COMPOSER)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_telos_multireceipt_joiner_shape() -> None:
    module = load_composer()
    artifact = module.compose()
    required = set(module.REQUIRED_CLASSES)
    components = artifact["component_receipts"]
    packet = artifact["product_packet"]

    assert artifact["schema"] == "TelosMultiReceiptJoiner/v1"
    assert artifact["pass"] == "0069"
    assert artifact["status"] == "TELOS_MULTIRECEIPT_JOINER_MATCH"
    assert {row["kind"] for row in components} == required
    assert packet["schema"] == "TelosProductProofPacket/v1"
    assert packet["component_count"] == len(components)
    assert packet["unsupported_claim_count"] == 0
    assert packet["raw_private_payload_required"] is False
    assert packet["model_reasoning_required_for_replay"] is False

    for row in components:
        assert row["verification_status"] == "MATCH"
        assert row["raw_payload_included"] is False
        assert len(row["digest"]) == 64
        assert len(row["seal"]) == 64

    assert len(artifact["negative_fixtures"]) >= 5
    assert all(item["expected_status"] == "REJECT" for item in artifact["negative_fixtures"])
    assert {row["verdict"] for row in artifact["ablation_results"]} == {"MATCH", "REJECT"}
    assert artifact["unsupported_claim_count"] == 0


if __name__ == "__main__":
    test_telos_multireceipt_joiner_shape()
