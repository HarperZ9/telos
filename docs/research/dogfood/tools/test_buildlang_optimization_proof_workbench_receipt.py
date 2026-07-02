"""Focused tests for pass 0097 BuildLang optimization proof workbench."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPOSER = ROOT / "tools" / "compose_buildlang_optimization_proof_workbench_receipt.py"
ARTIFACT = ROOT / "schemas" / "buildlang-optimization-proof-workbench-receipt-pass-0097.json"


def load_composer():
    spec = importlib.util.spec_from_file_location("compose_buildlang_optimization_proof_workbench_receipt", COMPOSER)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_buildlang_optimization_proof_workbench_shape() -> None:
    module = load_composer()
    artifact = json.loads(ARTIFACT.read_text(encoding="utf-8")) if ARTIFACT.exists() else module.compose()
    output = artifact["run_output"]

    assert artifact["schema"] == "BuildLangOptimizationProofWorkbenchReceipt/v1"
    assert artifact["pass"] == "0097"
    assert artifact["status"] == "BUILDLANG_OPTIMIZATION_PROOF_WORKBENCH_MATCH"
    assert artifact["source_bindings"]["scorecard_pass"] == "0096"
    assert artifact["source_bindings"]["primary_vector"] == "optimization_proof_workbench"
    assert artifact["check_command"]["exit_code"] == 0
    assert artifact["verify_command"]["exit_code"] == 0
    assert artifact["run_command"]["exit_code"] == 0
    assert output["exact value"] == 162
    assert output["exact weight"] == 29
    assert output["exact mask"] == 2347
    assert output["exact feasible"] == 1275
    assert output["greedy value"] == 146
    assert output["greedy weight"] == 25
    assert output["greedy mask"] == 2331
    assert output["bounded value"] == 157
    assert output["bounded weight"] == 27
    assert output["bounded mask"] == 299
    assert output["bounded feasible"] == 704
    assert artifact["verify_summary"]["check_count"] == 18
    assert artifact["comparison_summary"]["greedy_gap"] == 16
    assert artifact["comparison_summary"]["bounded_gap"] == 5
    assert len(artifact["branches"]) == 3
    assert len(artifact["measurements"]) == 8
    assert all(row["status"] == "MATCH" for row in artifact["measurements"])
    assert all(tool["status"] == "MATCH" for tool in artifact["flagship_receipts"].values())
    assert artifact["unsupported_claim_count"] == 0
    assert artifact["current_promoted_natural_laws"] == []


if __name__ == "__main__":
    test_buildlang_optimization_proof_workbench_shape()
