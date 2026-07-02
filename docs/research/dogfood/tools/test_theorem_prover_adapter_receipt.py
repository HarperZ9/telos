"""Focused tests for pass 0117 theorem-prover adapter receipt."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPOSER = ROOT / "tools" / "compose_theorem_prover_adapter_receipt.py"
ARTIFACT = ROOT / "schemas" / "theorem-prover-adapter-receipt-pass-0117.json"


def load_module():
    spec = importlib.util.spec_from_file_location("compose_theorem_prover_adapter_receipt", COMPOSER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_artifact() -> dict:
    if ARTIFACT.exists():
        return json.loads(ARTIFACT.read_text(encoding="utf-8"))
    return load_module().compose()


def branch(branches: list[dict], branch_id: str) -> dict:
    return next(row for row in branches if row["branch_id"] == branch_id)


def test_theorem_prover_adapter_shape() -> None:
    artifact = read_artifact()
    branches = artifact["prover_branches"]
    python_branch = branch(branches, "python_finite_model_replay")
    lean_branch = branch(branches, "lean4_target")

    assert artifact["schema"] == "TheoremProverAdapterReceipt/v1"
    assert artifact["status"] == "THEOREM_PROVER_ADAPTER_MATCH"
    assert artifact["source_bindings"]["formal_physics_bridge_pass"] == "0116"
    assert artifact["availability"]["lean"]["status"] == "MISSING"
    assert artifact["availability"]["lake"]["status"] == "MISSING"
    assert artifact["availability"]["coqc"]["status"] == "MISSING"
    assert artifact["availability"]["isabelle"]["status"] == "MISSING"
    assert artifact["availability"]["agda"]["status"] == "MISSING"
    assert len(artifact["theorem_targets"]) == 3
    assert {row["target_id"] for row in artifact["theorem_targets"]} == {"left_identity", "right_identity", "associativity"}
    assert all(row["claim_status"] == "FINITE_MODEL_VERIFIED" for row in artifact["theorem_targets"])
    assert python_branch["status"] == "MATCH"
    assert python_branch["target_count"] == 3
    assert lean_branch["status"] == "UNAVAILABLE_FENCED"
    assert all(row["status"] in {"MATCH", "UNAVAILABLE_FENCED"} for row in branches)
    assert artifact["countermodel"]["status"] == "MATCH"
    assert artifact["countermodel"]["classification"] == "BAD_IDENTITY_DRIFT"
    assert artifact["source_surface"]["anchor_count"] >= 6
    assert artifact["unsupported_claim_count"] == 0
    assert artifact["current_promoted_natural_laws"] == []
    assert all(row["status"] == "MATCH" for row in artifact["flagship_receipts"].values())


if __name__ == "__main__":
    test_theorem_prover_adapter_shape()
