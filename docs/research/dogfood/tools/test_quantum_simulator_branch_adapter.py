"""Focused tests for pass 0087 simulator branch adapter."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMPOSER = ROOT / "tools" / "compose_quantum_simulator_branch_adapter.py"
ARTIFACT = ROOT / "schemas" / "quantum-simulator-branch-adapter-pass-0087.json"


def load_composer():
    spec = importlib.util.spec_from_file_location("compose_quantum_simulator_branch_adapter", COMPOSER)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_quantum_simulator_branch_adapter_shape() -> None:
    module = load_composer()
    artifact = json.loads(ARTIFACT.read_text(encoding="utf-8")) if ARTIFACT.exists() else module.compose()
    sim = artifact["simulator_branch"]
    comparison = artifact["comparison_to_exact"]

    assert artifact["schema"] == "QuantumSimulatorBranchAdapterReceipt/v1"
    assert artifact["pass"] == "0087"
    assert artifact["status"] == "QUANTUM_SIMULATOR_BRANCH_ADAPTER_MATCH"
    assert artifact["baseline_binding"]["source_pass"] == "0086"
    assert sim["run_count"] == 32
    assert sim["optimum_hit_count"] > 0
    assert sim["best_feasible_count"] > 0
    assert sim["runs_sha256"] == module.sha256_obj(sim["runs"])
    assert comparison["status"] == "MATCH"
    assert comparison["exact_best_bits"] == comparison["simulator_best_bits"]
    assert comparison["exact_best_energy"] == comparison["simulator_best_energy"]
    assert len(sim["source_anchors"]) >= 2
    assert artifact["promotion_boundary"]["simulator_only"] is True
    assert artifact["promotion_boundary"]["quantum_hardware_claim"] is False
    assert artifact["promotion_boundary"]["quantum_advantage_claim"] is False
    assert artifact["promotion_boundary"]["new_natural_law_claim"] is False
    assert all(receipt["status"] == "MATCH" for receipt in artifact["flagship_receipts"].values())
    assert artifact["unsupported_claim_count"] == 0
    assert artifact["current_promoted_natural_laws"] == []


if __name__ == "__main__":
    test_quantum_simulator_branch_adapter_shape()
