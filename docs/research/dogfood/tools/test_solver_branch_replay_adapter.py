"""Focused tests for pass 0115 solver-branch replay adapter."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPOSER = ROOT / "tools" / "compose_solver_branch_replay_adapter.py"
ARTIFACT = ROOT / "schemas" / "solver-branch-replay-adapter-pass-0115.json"


def load_module():
    spec = importlib.util.spec_from_file_location("compose_solver_branch_replay_adapter", COMPOSER)
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


def test_solver_branch_replay_adapter_shape() -> None:
    artifact = read_artifact()
    branches = artifact["solver_branches"]
    exhaustive = branch(branches, "builtin_exhaustive_replay")
    scipy = branch(branches, "scipy_highs_quant_replay")
    ortools = branch(branches, "ortools_cp_sat")
    pulp = branch(branches, "pulp_cbc")

    assert artifact["schema"] == "SolverBranchReplayAdapterReceipt/v1"
    assert artifact["status"] == "SOLVER_BRANCH_REPLAY_ADAPTER_MATCH"
    assert artifact["source_bindings"]["suite_pass"] == "0114"
    assert artifact["source_bindings"]["youtube_roadmap_pass"] == "0102"
    assert artifact["source_bindings"]["new_youtube_lead_store"] == "gather/pass-0115-youtube-leads"
    assert artifact["availability"]["scipy"]["status"] == "AVAILABLE"
    assert artifact["availability"]["ortools"]["status"] == "MISSING"
    assert artifact["availability"]["pulp"]["status"] == "MISSING"
    assert exhaustive["status"] == "MATCH"
    assert exhaustive["case_count"] == 4
    assert all(row["status"] == "MATCH" for row in exhaustive["case_results"])
    assert scipy["status"] == "MATCH"
    assert scipy["case_id"] == "quant_risk_budget"
    assert scipy["objective"] == "9/2"
    assert scipy["assignment"] == {"asset_a": "1/2", "asset_b": "1/4", "asset_c": "1/4"}
    assert ortools["status"] == "UNAVAILABLE_FENCED"
    assert pulp["status"] == "UNAVAILABLE_FENCED"
    assert artifact["drift_total"] == 0
    assert artifact["unavailable_branch_count"] == 2
    assert artifact["market_surface"]["tool_count"] >= 4
    assert artifact["new_youtube_lead_summary"]["lead_count"] == 4
    assert artifact["new_youtube_lead_summary"]["gather_verified_count"] == 4
    assert artifact["new_youtube_lead_summary"]["transcript_receipt_count"] == 4
    assert artifact["new_youtube_lead_summary"]["raw_transcripts_included"] is False
    assert {row["video_id"] for row in artifact["new_youtube_source_leads"]} == {
        "HbKzqvey5PA",
        "4MQbd5wTlI8",
        "EdVG5qNm2rY",
        "nYwid6Q5HXk",
    }
    assert all(row["source_status"] == "GATHER_VERIFIED_RECEIPT" for row in artifact["new_youtube_source_leads"])
    assert all(row["claim_status"] == "SOURCE_LEAD_ONLY" for row in artifact["new_youtube_source_leads"])
    assert all(row["raw_transcript_included"] is False for row in artifact["new_youtube_source_leads"])
    assert len(artifact["roadmap_pressure"]) == 4
    assert artifact["unsupported_claim_count"] == 0
    assert artifact["current_promoted_natural_laws"] == []


if __name__ == "__main__":
    test_solver_branch_replay_adapter_shape()
