"""Validate pass 0115 solver-branch replay adapter."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "solver-branch-replay-adapter-pass-0115.json"
RESULT = ROOT / "schemas" / "pass-0115-solver-branch-replay-validator-result.json"


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)


def sha256_obj(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n", encoding="utf-8")


def branch(branches: list[dict], branch_id: str) -> dict:
    return next((row for row in branches if row.get("branch_id") == branch_id), {})


def validate() -> dict:
    artifact = read_json(ARTIFACT)
    unsealed = dict(artifact)
    seal = unsealed.pop("seal", None)
    branches = artifact.get("solver_branches", [])
    exhaustive = branch(branches, "builtin_exhaustive_replay")
    scipy = branch(branches, "scipy_highs_quant_replay")
    ortools = branch(branches, "ortools_cp_sat")
    pulp = branch(branches, "pulp_cbc")
    youtube = artifact.get("new_youtube_lead_summary", {})
    lead_ids = {row.get("video_id") for row in artifact.get("new_youtube_source_leads", [])}
    errors: list[str] = []

    if artifact.get("schema") != "SolverBranchReplayAdapterReceipt/v1":
        errors.append("schema")
    if artifact.get("status") != "SOLVER_BRANCH_REPLAY_ADAPTER_MATCH":
        errors.append("status")
    if seal != sha256_obj(unsealed):
        errors.append("seal")
    if artifact.get("source_bindings", {}).get("suite_pass") != "0114":
        errors.append("suite_pass")
    if artifact.get("source_bindings", {}).get("youtube_roadmap_pass") != "0102":
        errors.append("youtube_roadmap_pass")
    if artifact.get("availability", {}).get("scipy", {}).get("status") != "AVAILABLE":
        errors.append("scipy")
    if artifact.get("availability", {}).get("ortools", {}).get("status") != "MISSING":
        errors.append("ortools")
    if artifact.get("availability", {}).get("pulp", {}).get("status") != "MISSING":
        errors.append("pulp")
    if exhaustive.get("status") != "MATCH" or exhaustive.get("case_count") != 4:
        errors.append("exhaustive")
    if any(row.get("status") != "MATCH" for row in exhaustive.get("case_results", [])):
        errors.append("exhaustive_cases")
    if scipy.get("status") != "MATCH" or scipy.get("objective") != "9/2":
        errors.append("scipy_branch")
    if scipy.get("assignment") != {"asset_a": "1/2", "asset_b": "1/4", "asset_c": "1/4"}:
        errors.append("scipy_assignment")
    if ortools.get("status") != "UNAVAILABLE_FENCED" or pulp.get("status") != "UNAVAILABLE_FENCED":
        errors.append("availability_fences")
    if artifact.get("drift_total") != 0 or artifact.get("unavailable_branch_count") != 2:
        errors.append("drift_counts")
    if youtube.get("lead_count") != 4 or youtube.get("gather_verified_count") != 4:
        errors.append("youtube_leads")
    if youtube.get("transcript_receipt_count") != 4 or youtube.get("raw_transcripts_included") is not False:
        errors.append("youtube_transcripts")
    if lead_ids != {"HbKzqvey5PA", "4MQbd5wTlI8", "EdVG5qNm2rY", "nYwid6Q5HXk"}:
        errors.append("youtube_ids")
    if any(row.get("raw_transcript_included") is not False for row in artifact.get("new_youtube_source_leads", [])):
        errors.append("raw_transcript_boundary")
    if any(row.get("status") != "MATCH" for row in artifact.get("flagship_receipts", {}).values()):
        errors.append("flagships")
    if artifact.get("unsupported_claim_count") != 0 or artifact.get("current_promoted_natural_laws") != []:
        errors.append("promotion_boundary")
    if any(row.get("status") not in {"MATCH", "UNAVAILABLE_FENCED"} for row in artifact.get("measurements", []) if row.get("id") != "promotion_boundary"):
        errors.append("measurements")

    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0115SolverBranchReplayValidatorRun/v1",
        "pass": "0115",
        "status": status,
        "match": 1 if status == "MATCH" else 0,
        "drift": 0 if status == "MATCH" else 1,
        "checks": [{
            "artifact": "SolverBranchReplayAdapterReceipt",
            "branch_count": len(branches),
            "errors": errors,
            "new_youtube_lead_count": youtube.get("lead_count"),
            "path": "schemas/solver-branch-replay-adapter-pass-0115.json",
            "status": status,
        }],
    }


def main() -> None:
    result = validate()
    write_json(RESULT, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
