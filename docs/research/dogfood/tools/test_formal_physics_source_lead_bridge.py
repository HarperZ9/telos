"""Focused tests for pass 0116 formal/physics source-lead bridge."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPOSER = ROOT / "tools" / "compose_formal_physics_source_lead_bridge.py"
ARTIFACT = ROOT / "schemas" / "formal-physics-source-lead-bridge-pass-0116.json"


def load_module():
    spec = importlib.util.spec_from_file_location("compose_formal_physics_source_lead_bridge", COMPOSER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_artifact() -> dict:
    if ARTIFACT.exists():
        return json.loads(ARTIFACT.read_text(encoding="utf-8"))
    return load_module().compose()


def case(cases: list[dict], case_id: str) -> dict:
    return next(row for row in cases if row["case_id"] == case_id)


def test_formal_physics_source_lead_bridge_shape() -> None:
    artifact = read_artifact()
    cases = artifact["bridge_cases"]
    category = case(cases, "category_set_identity_associativity")
    born = case(cases, "born_rule_normalization_toy")
    counterexample = case(cases, "counterexample_revision_toy")
    loop = case(cases, "loop_replay_receipt_toy")

    assert artifact["schema"] == "FormalPhysicsSourceLeadBridgeReceipt/v1"
    assert artifact["status"] == "FORMAL_PHYSICS_SOURCE_LEAD_BRIDGE_MATCH"
    assert artifact["source_bindings"]["solver_replay_pass"] == "0115"
    assert artifact["source_bindings"]["youtube_roadmap_pass"] == "0102"
    assert artifact["source_bindings"]["new_youtube_lead_count"] == 4
    assert len(cases) == 4
    assert all(row["status"] == "MATCH" for row in cases)
    assert category["checks"] == {"left_identity": True, "right_identity": True, "associativity": True}
    assert category["negative_fixture"]["classification"] == "BAD_IDENTITY_DRIFT"
    assert born["probability_sum"] == "1"
    assert born["negative_fixture"]["classification"] == "NON_NORMALIZED_STATE_REJECTED"
    assert counterexample["initial_claim_status"] == "REFUTED_BY_COUNTEREXAMPLE"
    assert counterexample["revised_claim_status"] == "MATCH"
    assert loop["final_status"] == "MATCH"
    assert loop["reasoning_trace_exposed"] is False
    assert loop["attempt_count"] == 2
    assert artifact["source_surface"]["anchor_count"] >= 12
    assert len(artifact["roadmap_requirements"]) == 4
    assert all(row["claim_status"] == "HYPOTHESIS" for row in artifact["roadmap_requirements"])
    assert artifact["unsupported_claim_count"] == 0
    assert artifact["current_promoted_natural_laws"] == []
    assert all(row["status"] == "MATCH" for row in artifact["flagship_receipts"].values())


if __name__ == "__main__":
    test_formal_physics_source_lead_bridge_shape()
