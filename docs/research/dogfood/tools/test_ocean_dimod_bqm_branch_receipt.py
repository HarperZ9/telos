"""Focused tests for pass 0100 Ocean/dimod BQM branch receipt."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPOSER = ROOT / "tools" / "compose_ocean_dimod_bqm_branch_receipt.py"
ARTIFACT = ROOT / "schemas" / "ocean-dimod-bqm-branch-receipt-pass-0100.json"


def load_composer():
    spec = importlib.util.spec_from_file_location("compose_ocean_dimod_bqm_branch_receipt", COMPOSER)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_ocean_dimod_bqm_branch_receipt_shape() -> None:
    module = load_composer()
    artifact = json.loads(ARTIFACT.read_text(encoding="utf-8")) if ARTIFACT.exists() else module.compose()
    branch = artifact["solver_branch_receipt"]

    assert artifact["schema"] == "OceanDimodBQMBranchReceipt/v1"
    assert artifact["pass"] == "0100"
    assert artifact["status"] == "OCEAN_DIMOD_BQM_BRANCH_RECEIPT_MATCH"
    assert artifact["source_bindings"]["ortools_pass"] == "0099"
    assert artifact["global_availability"]["dimod_available"] is False
    assert artifact["global_availability"]["dwave_available"] is False
    assert artifact["install_command"]["exit_code"] == 0
    assert artifact["run_command"]["exit_code"] == 0
    assert artifact["temp_venv"]["cleaned"] is True
    assert artifact["dimod_version"]
    assert artifact["bqm_summary"]["linear_terms"] == 12
    assert artifact["bqm_summary"]["quadratic_terms"] == 66
    assert branch["schema"] == "SolverBranchReceipt/v1"
    assert branch["execution_status"] == "EXECUTED_LOCAL_CPU_EXACT_SOLVER"
    assert branch["value"] == 162
    assert branch["weight"] == 29
    assert branch["mask"] == 2347
    assert branch["gap_to_exact"] == 0
    assert artifact["comparison_to_exact"]["matches_exact"] is True
    assert len(artifact["source_anchors"]) == 3
    assert len(artifact["measurements"]) == 9
    assert all(row["status"] == "MATCH" for row in artifact["measurements"])
    assert all(tool["status"] == "MATCH" for tool in artifact["flagship_receipts"].values())
    assert artifact["unsupported_claim_count"] == 0
    assert artifact["current_promoted_natural_laws"] == []


if __name__ == "__main__":
    test_ocean_dimod_bqm_branch_receipt_shape()
