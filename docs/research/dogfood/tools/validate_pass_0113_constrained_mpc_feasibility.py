"""Validate pass 0113 constrained-MPC feasibility receipt."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "constrained-mpc-feasibility-receipt-pass-0113.json"
RESULT = ROOT / "schemas" / "pass-0113-constrained-mpc-feasibility-validator-result.json"


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)


def sha256_obj(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n", encoding="utf-8")


def validate() -> dict:
    artifact = read_json(ARTIFACT)
    unsealed = dict(artifact)
    seal = unsealed.pop("seal", None)
    feasible = artifact.get("feasible_case", {})
    neg = artifact.get("negative_fixtures", {})
    youtube = artifact.get("youtube_binding", {})
    requirements = artifact.get("youtube_requirements", {})
    errors: list[str] = []

    if artifact.get("schema") != "ConstrainedMPCFeasibilityReceipt/v1":
        errors.append("schema")
    if artifact.get("status") != "CONSTRAINED_MPC_FEASIBILITY_RECEIPT_MATCH":
        errors.append("status")
    if seal != sha256_obj(unsealed):
        errors.append("seal")
    if artifact.get("source_bindings", {}).get("lyapunov_pass") != "0112":
        errors.append("lyapunov_pass")
    if artifact.get("source_bindings", {}).get("youtube_roadmap_pass") != "0102":
        errors.append("youtube_roadmap_pass")
    if len(artifact.get("source_anchors", [])) < 8:
        errors.append("source_anchors")
    if feasible.get("states") != ["2", "1", "0", "0"] or feasible.get("controls") != ["-1", "-1", "0"]:
        errors.append("rollout")
    if feasible.get("objective") != "7" or feasible.get("terminal_residual") != "0":
        errors.append("objective_or_terminal")
    if feasible.get("constraint_status") != "MATCH":
        errors.append("constraint_status")
    infeasible = neg.get("infeasible_terminal_fixture", {})
    if infeasible.get("classification") != "INFEASIBLE_EXPECTED" or infeasible.get("minimum_terminal_abs_residual") != "1":
        errors.append("infeasible_fixture")
    bad = neg.get("bad_plan_fixture", {})
    if bad.get("classification") != "TERMINAL_VIOLATION_EXPECTED" or bad.get("terminal_residual") != "1":
        errors.append("bad_plan")
    if youtube.get("valid_video_count") != 19 or youtube.get("transcript_receipt_count") != 19:
        errors.append("youtube_counts")
    if youtube.get("raw_transcript_included") is not False:
        errors.append("raw_transcripts")
    if requirements.get("top_priority") != "optimization_proof_workbench" or requirements.get("dominant_cluster_video_count") != 13:
        errors.append("youtube_requirements")
    if requirements.get("required_receipt_fields", [None])[0] != "constraint_type":
        errors.append("required_fields")
    if artifact.get("market_surface", {}).get("tool_count", 0) < 8:
        errors.append("market")
    if any(row.get("status") != "MATCH" for row in artifact.get("measurements", [])):
        errors.append("measurements")
    if any(row.get("status") != "MATCH" for row in artifact.get("flagship_receipts", {}).values()):
        errors.append("flagships")
    if artifact.get("unsupported_claim_count") != 0 or artifact.get("current_promoted_natural_laws") != []:
        errors.append("promotion_boundary")

    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0113ConstrainedMPCFeasibilityValidatorRun/v1",
        "pass": "0113",
        "status": status,
        "match": 1 if status == "MATCH" else 0,
        "drift": 0 if status == "MATCH" else 1,
        "checks": [{
            "artifact": "ConstrainedMPCFeasibilityReceipt",
            "errors": errors,
            "path": "schemas/constrained-mpc-feasibility-receipt-pass-0113.json",
            "feasible_terminal_residual": feasible.get("terminal_residual"),
            "infeasible_min_terminal_residual": infeasible.get("minimum_terminal_abs_residual"),
            "youtube_valid_video_count": youtube.get("valid_video_count"),
            "dominant_cluster_video_count": requirements.get("dominant_cluster_video_count"),
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
