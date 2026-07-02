"""Compose pass 0102 YouTube critical-data megatool roadmap."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

SCHEMA = "YouTubeCriticalDataMegatoolRoadmap/v1"
PASS_ID = "0102"
STATUS_MATCH = "YOUTUBE_CRITICAL_DATA_MEGATOOL_ROADMAP_MATCH"
STATUS_DRIFT = "YOUTUBE_CRITICAL_DATA_MEGATOOL_ROADMAP_DRIFT"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
YOUTUBE = ROOT / "schemas" / "youtube-research-compounding-packet-pass-0085.json"
SCORECARD = ROOT / "schemas" / "youtube-field-growth-vector-scorecard-pass-0096.json"
WORKBENCH = ROOT / "schemas" / "buildlang-optimization-proof-workbench-receipt-pass-0097.json"
INTEROP = ROOT / "schemas" / "solver-branch-receipt-interop-schema-pass-0098.json"
ORTOOLS = ROOT / "schemas" / "ortools-branch-execution-receipt-pass-0099.json"
OCEAN = ROOT / "schemas" / "ocean-dimod-bqm-branch-receipt-pass-0100.json"
INEQUALITY = ROOT / "schemas" / "inequality-safe-bqm-receipt-pass-0101.json"

def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_obj(value: object) -> str:
    return sha256_text(canonical_json(value))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n", encoding="utf-8")


def run_json(command: list[str], timeout: int = 45) -> tuple[int, str, str, dict[str, Any]]:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    parsed = json.loads(result.stdout) if result.returncode == 0 and result.stdout.strip().startswith("{") else {}
    return result.returncode, result.stdout, result.stderr, parsed

def cluster_lookup(youtube: dict[str, Any]) -> dict[str, dict[str, Any]]:
    lookup: dict[str, dict[str, Any]] = {}
    for cluster in youtube["research_clusters"]:
        for video_id in cluster["video_ids"]:
            lookup[video_id] = cluster
    return lookup

def video_cards(youtube: dict[str, Any]) -> list[dict[str, Any]]:
    lookup = cluster_lookup(youtube)
    cards: list[dict[str, Any]] = []
    for row in youtube["source_cards"]:
        if row.get("status") == "INVALID_URL":
            cards.append({
                "input_index": row["input_index"],
                "status": "INVALID_URL",
                "url": row["url"],
                "reason": row.get("reason", "missing_video_id"),
            })
            continue
        metadata = row["metadata"]
        gather = row["gather"]
        cluster = lookup.get(metadata["id"], {})
        cards.append({
            "input_index": row["input_index"],
            "status": row["status"],
            "video_id": metadata["id"],
            "url": row["url"],
            "title": metadata.get("title"),
            "channel": metadata.get("channel"),
            "duration": metadata.get("duration_string"),
            "cluster_id": cluster.get("cluster_id"),
            "cluster_signal": cluster.get("strategic_signal"),
            "metadata_sha256": gather.get("metadata_sha256"),
            "transcript_sha256": gather.get("transcript_sha256"),
            "raw_transcript_included": False,
            "claim_status": "SOURCE_LEAD",
        })
    return cards

def source_counts(youtube: dict[str, Any], cards: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "input_url_count": youtube["input_url_count"],
        "valid_video_count": youtube["valid_video_count"],
        "invalid_url_count": youtube["invalid_url_count"],
        "metadata_match_count": youtube["metadata_match_count"],
        "gather_match_count": youtube["gather_match_count"],
        "transcript_receipt_count": youtube["transcript_receipt_count"],
        "raw_transcript_stored": any(card.get("raw_transcript_included") for card in cards),
        "cluster_count": youtube["video_corpus_summary"]["cluster_count"],
        "dominant_cluster": youtube["video_corpus_summary"]["dominant_cluster"],
        "dominant_cluster_video_count": youtube["video_corpus_summary"]["dominant_cluster_video_count"],
        "source_policy": youtube["video_corpus_summary"]["source_policy"],
    }

def score(source: int, urgency: int, demo: int, proof: int, reuse: int, upside: int) -> dict[str, int]:
    return {
        "youtube_source_weight": source,
        "urgency": urgency,
        "demo_readiness": demo,
        "proof_advantage": proof,
        "reuse": reuse,
        "strategic_upside": upside,
        "total": source + urgency + demo + proof + reuse + upside,
    }

def roadmap_nodes(scorecard: dict[str, Any], inequality: dict[str, Any]) -> list[dict[str, Any]]:
    vector_by_id = {row["id"]: row for row in scorecard["field_vectors"]}
    encoding_rule = {
        "requirement_id": "constraint_encoding_receipt",
        "source_pass": "0101",
        "law_candidate": inequality["law_candidate"]["name"],
        "status": inequality["law_candidate"]["status"],
        "required_fields": ["constraint_type", "encoding_method", "slack_variables", "feasibility_check", "counterexample_fixture"],
    }
    specs = [
        ("optimization_proof_workbench", "OptimizationProofWorkbench/v1", 5, 5, 5, 5, 5, 5, ["Gather", "Index", "Forum", "Crucible", "Telos", "BuildLang/buildc", "OR-Tools", "Ocean/dimod"], [encoding_rule, "solver_branch_receipts", "business_objective_receipts"]),
        ("buildlang_scientific_runtime", "AccountableScientificRuntime/v1", 4, 5, 5, 5, 5, 5, ["BuildLang/buildc", "build-universe", "Crucible", "Telos"], ["typed_numeric_receipts", "target_runtime_receipts", encoding_rule]),
        ("ai4science_claim_to_experiment", "AI4ScienceClaimToExperimentReceipt/v1", 2, 5, 3, 5, 4, 5, ["Gather", "Index", "model foundry", "Crucible", "Telos"], ["claim_extraction", "simulation_or_assay_receipts", "negative_result_lane"]),
        ("agi_eval_attempt_lab", "EvalAttemptProofPacket/v1", 2, 5, 4, 5, 4, 5, ["Gather", "model foundry", "loop ledger", "Crucible"], ["task_authority", "contamination_check", "attempt_replay", "verifier_verdict"]),
        ("prover_verifier_search_engine", "SearchVerifierLoopLedger/v1", 2, 4, 4, 5, 4, 5, ["model foundry", "loop ledger", "Crucible", "BuildLang/buildc"], ["proposal_branch_receipts", "failed_branch_capture", "formal_checker_hooks"]),
        ("quant_finance_kernel_packets", "QuantKernelReceipt/v1", 2, 5, 4, 4, 4, 5, ["BuildLang/buildc", "Crucible", "Index", "Telos"], ["identity_receipts", "stress_receipts", "tolerance_receipts"]),
        ("risk_and_governance_receipts", "RiskGovernanceReceipt/v1", 2, 5, 3, 4, 4, 5, ["Forum", "Gather", "action receipts", "Crucible"], ["assumption_ledger", "authority_boundary", "review_appeal_lane"]),
        ("visual_truth_measurement_kit", "VisualTruthMeasurementKit/v1", 1, 4, 4, 5, 4, 5, ["color calibration", "browser evidence", "BuildLang/buildc", "Crucible"], ["measurement_receipts", "calibration_boundaries", "render_kernel_receipts"]),
    ]
    nodes = []
    for vector_id, product, *rest in specs:
        source, urgency, demo, proof, reuse, upside, tools, requirements = rest
        vector = vector_by_id.get(vector_id, {})
        nodes.append({
            "node_id": vector_id,
            "market_product": product,
            "source_clusters": vector.get("source_clusters", []),
            "source_video_count": vector.get("source_video_count", 0),
            "source_video_ids": vector.get("source_video_ids", []),
            "youtube_titles": vector.get("source_titles", []),
            "toolchain": tools,
            "requirements": requirements,
            "next_experiment": vector.get("next_experiment", "create receipt-backed fixture"),
            "gap_status": "inferred",
            "verification_status": "HYPOTHESIS_WITH_LOCAL_RECEIPTS",
            "wedge_score": score(source, urgency, demo, proof, reuse, upside),
        })
    return sorted(nodes, key=lambda row: row["wedge_score"]["total"], reverse=True)

def source_to_architecture_claims(youtube: dict[str, Any]) -> list[dict[str, Any]]:
    claims = []
    for cluster in youtube["research_clusters"]:
        claims.append({
            "cluster_id": cluster["cluster_id"],
            "video_count": cluster["source_count"],
            "source_titles": cluster["titles"],
            "video_ids": cluster["video_ids"],
            "observed_signal": cluster["strategic_signal"],
            "architecture_pull": cluster["product_response"],
            "evidence_status": "SOURCE_LEAD",
            "gap_status": "inferred",
        })
    return claims

def experiments() -> list[dict[str, Any]]:
    return [
        {
            "experiment_id": "constraint_safe_optimization_adapter",
            "source_nodes": ["optimization_proof_workbench", "buildlang_scientific_runtime"],
            "builds_on_passes": ["0097", "0098", "0099", "0100", "0101"],
            "acceptance": ["branch declares encoding method", "slack or inequality receipt exists", "infeasible counterexample rejected"],
            "status": "READY_NEXT",
        },
        {
            "experiment_id": "claim_to_experiment_minimum_packet",
            "source_nodes": ["ai4science_claim_to_experiment"],
            "builds_on_passes": ["0085", "0096"],
            "acceptance": ["claim has source receipt", "simulation_or_assay placeholder is explicit", "unsupported discovery claim is rejected"],
            "status": "READY_AFTER_SOURCE_SCHEMA",
        },
        {
            "experiment_id": "eval_attempt_contamination_packet",
            "source_nodes": ["agi_eval_attempt_lab", "prover_verifier_search_engine"],
            "builds_on_passes": ["0085", "0096"],
            "acceptance": ["task authority recorded", "attempt replay captured", "contamination fixture rejected"],
            "status": "READY_AFTER_SYNTHETIC_TASK",
        },
    ]

def forum_route() -> dict[str, Any]:
    prompt = "Pass 0102: use YouTube critical data to map Project Telos megatool architecture across quantum optimization, BuildLang, AI4Science, evals, quant, search, risk, governance, and visual truth."
    code, stdout, stderr, parsed = run_json(["forum", "route", "--json", prompt], timeout=30)
    return {"status": "MATCH" if code == 0 else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "decided": parsed.get("decided"), "confidence": parsed.get("confidence"), "needs_escalation": parsed.get("needs_escalation"), "top_candidates": parsed.get("candidates", [])[:5]}

def index_receipt() -> dict[str, Any]:
    code, stdout, stderr, parsed = run_json(["index", "context-envelope", "--root", ".", "--budget", "1200", "--json"], timeout=45)
    return {"status": "MATCH" if code == 0 and parsed.get("verification_verdict") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "schema": parsed.get("schema"), "verification_verdict": parsed.get("verification_verdict"), "graph_pack_sha256": parsed.get("recheck", {}).get("graph_pack_sha256"), "source_refs_only": parsed.get("privacy", {}).get("source_refs_only")}

def telos_status() -> dict[str, Any]:
    code, stdout, stderr, parsed = run_json(["node", "demo/status.mjs", "--summary"], timeout=30)
    return {"status": "MATCH" if code == 0 and parsed.get("status") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "tool_version": parsed.get("tool_version"), "tool": parsed.get("tool")}

def validate_artifact(artifact: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if artifact.get("schema") != SCHEMA:
        errors.append("schema")
    if artifact.get("source_summary", {}).get("valid_video_count") != 19:
        errors.append("valid_video_count")
    if artifact.get("source_summary", {}).get("transcript_receipt_count") != 19:
        errors.append("transcript_receipts")
    if len(artifact.get("source_to_architecture_claims", [])) != 7:
        errors.append("cluster_count")
    if artifact.get("roadmap_nodes", [{}])[0].get("node_id") != "optimization_proof_workbench":
        errors.append("primary_node")
    requirements = artifact.get("roadmap_nodes", [{}])[0].get("requirements", [])
    if not any(isinstance(row, dict) and row.get("requirement_id") == "constraint_encoding_receipt" for row in requirements):
        errors.append("encoding_requirement")
    if any(tool.get("status") != "MATCH" for tool in artifact.get("flagship_receipts", {}).values()):
        errors.append("flagships")
    if artifact.get("current_promoted_natural_laws") != [] or artifact.get("unsupported_claim_count") != 0:
        errors.append("promotion_boundary")
    return errors

def compose() -> dict[str, Any]:
    youtube = read_json(YOUTUBE)
    scorecard = read_json(SCORECARD)
    workbench = read_json(WORKBENCH)
    interop = read_json(INTEROP)
    ortools = read_json(ORTOOLS)
    ocean = read_json(OCEAN)
    inequality = read_json(INEQUALITY)
    cards = video_cards(youtube)
    nodes = roadmap_nodes(scorecard, inequality)
    artifact: dict[str, Any] = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "generated_on": "2026-07-01",
        "status": STATUS_DRIFT,
        "source_bindings": {
            "youtube_pass": youtube["pass"],
            "scorecard_pass": scorecard["pass"],
            "workbench_pass": workbench["pass"],
            "interop_pass": interop["pass"],
            "ortools_pass": ortools["pass"],
            "ocean_pass": ocean["pass"],
            "inequality_pass": inequality["pass"],
        },
        "source_summary": source_counts(youtube, cards),
        "video_cards": cards,
        "source_to_architecture_claims": source_to_architecture_claims(youtube),
        "roadmap_nodes": nodes,
        "top_priority": nodes[0]["node_id"],
        "experiments": experiments(),
        "constraint_encoding_lesson": inequality["law_candidate"],
        "current_promoted_natural_laws": [],
        "unsupported_claim_count": 0,
        "non_promotion_statement": "YouTube videos are critical source leads for architecture and market strategy, not proof of scientific, market, policy, or investment claims.",
        "flagship_receipts": {"forum": forum_route(), "index": index_receipt(), "telos": telos_status()},
    }
    artifact["validation_errors"] = validate_artifact(artifact)
    artifact["status"] = STATUS_MATCH if not artifact["validation_errors"] else STATUS_DRIFT
    artifact["measurements"] = [
        {"id": "valid_videos", "status": "MATCH" if artifact["source_summary"]["valid_video_count"] == 19 else "DRIFT"},
        {"id": "transcript_receipts", "status": "MATCH" if artifact["source_summary"]["transcript_receipt_count"] == 19 else "DRIFT"},
        {"id": "architecture_claims", "status": "MATCH" if len(artifact["source_to_architecture_claims"]) == 7 else "DRIFT"},
        {"id": "roadmap_nodes", "status": "MATCH" if len(nodes) == 8 else "DRIFT"},
        {"id": "top_priority", "status": "MATCH" if artifact["top_priority"] == "optimization_proof_workbench" else "DRIFT"},
        {"id": "encoding_lesson", "status": "MATCH" if inequality["law_candidate"]["status"] == "LAW_CANDIDATE" else "DRIFT"},
        {"id": "flagships", "status": "MATCH" if all(row["status"] == "MATCH" for row in artifact["flagship_receipts"].values()) else "DRIFT"},
        {"id": "promotion_boundary", "status": "MATCH" if artifact["current_promoted_natural_laws"] == [] else "DRIFT"},
    ]
    unsealed = dict(artifact)
    artifact["seal"] = sha256_obj(unsealed)
    return artifact

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(ROOT / "schemas" / "youtube-critical-data-megatool-roadmap-pass-0102.json"))
    args = parser.parse_args()
    artifact = compose()
    write_json(Path(args.out), artifact)
    print(json.dumps({"path": args.out, "seal": artifact["seal"], "status": artifact["status"]}, indent=2, sort_keys=True))
    if artifact["status"] != STATUS_MATCH:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
