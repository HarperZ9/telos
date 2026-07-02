"""Focused tests for pass 0113 constrained-MPC feasibility receipt."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPOSER = ROOT / "tools" / "compose_constrained_mpc_feasibility_receipt.py"
ARTIFACT = ROOT / "schemas" / "constrained-mpc-feasibility-receipt-pass-0113.json"


def load_module():
    spec = importlib.util.spec_from_file_location("compose_constrained_mpc_feasibility_receipt", COMPOSER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_artifact() -> dict:
    if ARTIFACT.exists():
        return json.loads(ARTIFACT.read_text(encoding="utf-8"))
    return load_module().compose()


def test_constrained_mpc_feasibility_shape() -> None:
    artifact = read_artifact()
    feasible = artifact["feasible_case"]
    infeasible = artifact["negative_fixtures"]["infeasible_terminal_fixture"]
    bad_plan = artifact["negative_fixtures"]["bad_plan_fixture"]
    youtube = artifact["youtube_binding"]

    assert artifact["schema"] == "ConstrainedMPCFeasibilityReceipt/v1"
    assert artifact["status"] == "CONSTRAINED_MPC_FEASIBILITY_RECEIPT_MATCH"
    assert artifact["source_bindings"]["lyapunov_pass"] == "0112"
    assert artifact["source_bindings"]["youtube_roadmap_pass"] == "0102"
    assert len(artifact["source_anchors"]) >= 8
    assert feasible["system"] == "x[k+1] = x[k] + u[k]"
    assert feasible["x0"] == "2"
    assert feasible["horizon"] == 3
    assert feasible["controls"] == ["-1", "-1", "0"]
    assert feasible["states"] == ["2", "1", "0", "0"]
    assert feasible["terminal_residual"] == "0"
    assert feasible["constraint_status"] == "MATCH"
    assert feasible["objective"] == "7"
    assert infeasible["classification"] == "INFEASIBLE_EXPECTED"
    assert infeasible["minimum_terminal_abs_residual"] == "1"
    assert bad_plan["classification"] == "TERMINAL_VIOLATION_EXPECTED"
    assert bad_plan["terminal_residual"] == "1"
    assert artifact["youtube_requirements"]["top_priority"] == "optimization_proof_workbench"
    assert artifact["youtube_requirements"]["dominant_cluster"] == "enterprise_quantum_optimization"
    assert artifact["youtube_requirements"]["dominant_cluster_video_count"] == 13
    assert artifact["youtube_requirements"]["required_receipt_fields"][0] == "constraint_type"
    assert youtube["valid_video_count"] == 19
    assert youtube["transcript_receipt_count"] == 19
    assert youtube["raw_transcript_included"] is False
    assert artifact["unsupported_claim_count"] == 0
    assert artifact["current_promoted_natural_laws"] == []


if __name__ == "__main__":
    test_constrained_mpc_feasibility_shape()
