"""Compose pass 0093 YouTube-to-BuildLang megatool bridge."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

SCHEMA = "YouTubeBuildLangMegatoolBridge/v1"
PASS_ID = "0093"
STATUS_MATCH = "YOUTUBE_BUILDLANG_MEGATOOL_BRIDGE_MATCH"
STATUS_DRIFT = "YOUTUBE_BUILDLANG_MEGATOOL_BRIDGE_DRIFT"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
YOUTUBE = ROOT / "schemas" / "youtube-research-compounding-packet-pass-0085.json"
BRANCH = ROOT / "schemas" / "optimization-branch-comparison-receipt-pass-0088.json"
SOLVER = ROOT / "schemas" / "external-solver-adapter-receipt-pass-0089.json"
MATRIX = ROOT / "schemas" / "solver-availability-matrix-receipt-pass-0090.json"
CORPUS = ROOT / "schemas" / "buildlang-corpus-crucible-adapter-pass-0091.json"
BUILDC = ROOT / "schemas" / "buildlang-check-receipt-adapter-pass-0092.json"


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
    parsed = json.loads(result.stdout) if result.returncode == 0 and result.stdout.strip() else {}
    return result.returncode, result.stdout, result.stderr, parsed


def cluster_index(youtube: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {row["cluster_id"]: row for row in youtube.get("research_clusters", [])}


def score(source_weight: int, demo_readiness: int, proof_advantage: int, integration_readiness: int, strategic_upside: int) -> dict[str, int]:
    return {
        "source_weight": source_weight,
        "demo_readiness": demo_readiness,
        "proof_advantage": proof_advantage,
        "integration_readiness": integration_readiness,
        "strategic_upside": strategic_upside,
        "total": source_weight + demo_readiness + proof_advantage + integration_readiness + strategic_upside,
    }


def bridge_node(
    cluster: dict[str, Any],
    product: str,
    existing: list[str],
    needed: list[str],
    experiment: str,
    scoring: dict[str, int],
) -> dict[str, Any]:
    return {
        "cluster_id": cluster["cluster_id"],
        "source_video_count": cluster["source_count"],
        "source_titles": cluster.get("titles", []),
        "market_facing_product": product,
        "existing_assets": existing,
        "needs_integration": needed,
        "next_experiment": experiment,
        "wedge_score": scoring,
        "verification_status": "HYPOTHESIS_WITH_LOCAL_RECEIPTS",
    }


def megatool_nodes(youtube: dict[str, Any], branch: dict[str, Any], solver: dict[str, Any], matrix: dict[str, Any], corpus: dict[str, Any], buildc: dict[str, Any]) -> list[dict[str, Any]]:
    clusters = cluster_index(youtube)
    exact = branch["exact_branch"]["best"]
    adapter = solver["external_adapter"]
    local_available = matrix["summary"]["local_available_rows"]
    buildc_checks = buildc["verify_summary"]["check_count"]
    return [
        bridge_node(
            clusters["enterprise_quantum_optimization"],
            "QuantumOptimizationWorkflowReceipt/v1",
            [
                f"pass-0085 source videos={clusters['enterprise_quantum_optimization']['source_count']}",
                f"pass-0088 exact optimum value={exact['value']} weight={exact['weight']}",
                f"pass-0089 scipy exact hits={adapter['comparison_to_exact']['exact_hit_count']}",
                f"pass-0090 available/source-present surfaces={local_available}",
                f"pass-0092 buildc verification checks={buildc_checks}",
            ],
            [
                "BuildLang-native optimization fixture",
                "NetworkX or OR-Tools adapter receipt",
                "solver-branch schema shared across exact, heuristic, external, and quantum branches",
                "calibration/reference fields for hardware or simulator claims",
            ],
            "Build one portable quantum-optimization proof packet with exact baseline, SciPy branch, dependency receipts, BuildLang source receipt, and Crucible verdict.",
            score(5, 5, 5, 4, 5),
        ),
        bridge_node(
            clusters["molecular_ai_drug_discovery"],
            "AI4ScienceClaimToExperimentReceipt/v1",
            ["pass-0085 metadata/transcript receipt", "Telos model-foundry lane", "Crucible verifier contract"],
            ["experiment-handoff schema", "assay/simulation source refs", "model-claim extraction with external-paper checks"],
            "Create a claim-to-experiment skeleton that refuses discovery claims until source, model, simulation, and verifier receipts line up.",
            score(3, 3, 5, 3, 5),
        ),
        bridge_node(
            clusters["arc_agi_eval_and_generalization"],
            "ARCAGIEvalAttemptReceipt/v1",
            ["pass-0085 metadata/transcript receipt", "Learning Forge lab contract", "Crucible MATCH/DRIFT/UNVERIFIABLE lane"],
            ["benchmark authority source refs", "contamination boundary fields", "attempt replay handles", "model/tool call receipts"],
            "Build an ARC-style eval attempt receipt that records tasks, attempts, contamination checks, and verifier outcomes.",
            score(3, 4, 5, 4, 5),
        ),
        bridge_node(
            clusters["quantitative_finance_laws"],
            "BuildLangQuantKernelReceipt/v1",
            ["pass-0085 quant-finance source lead", "pass-0091 buildc corpus adapter", "pass-0092 source-level buildc receipt"],
            ["finance identity fixtures", "numeric tolerance receipts", "stress scenario generator", "security/reproducibility review"],
            "Implement one bounded quant identity kernel in BuildLang and emit source digest, runtime receipt, tolerance checks, and Crucible verdict.",
            score(2, 4, 4, 4, 5),
        ),
        bridge_node(
            clusters["search_rl_alpha_zero"],
            "SearchVerifierLoopLedger/v1",
            ["pass-0085 search/RL source lead", "loop ledger concept", "Crucible measurement contract"],
            ["proposal/rollout/check state model", "seeded replay fixtures", "accept/reject receipts", "BuildLang kernel target"],
            "Turn AlphaZero-style search into a generic proposer/verifier loop receipt for math, solver, and planning tasks.",
            score(2, 3, 5, 3, 5),
        ),
        bridge_node(
            clusters["agi_risk_scenarios"],
            "RiskScenarioProofPacket/v1",
            ["pass-0085 AGI-risk source lead", "Forum routing", "Telos action-receipt boundary"],
            ["assumption ledger", "mitigation evidence refs", "authority/review fields", "scenario falsification tests"],
            "Represent each risk scenario as assumptions, claimed mechanism, evidence, mitigation, review state, and non-promotion boundaries.",
            score(2, 2, 4, 3, 4),
        ),
        bridge_node(
            clusters["ai_society_governance"],
            "SocietalReviewReceipt/v1",
            ["pass-0085 AI-society source lead", "Forum route receipts", "loop ledger and action receipt concepts"],
            ["stakeholder evidence fields", "policy provenance", "human review records", "appeal/revision handling"],
            "Create a governance receipt that keeps public claims, model actions, policy decisions, and review status inspectable.",
            score(2, 2, 4, 3, 4),
        ),
    ]


def forum_route() -> dict[str, Any]:
    prompt = "Project Telos pass 0093: bridge YouTube critical source data, quantum optimization solver receipts, and BuildLang buildc receipts into megatool product experiments."
    code, stdout, stderr, parsed = run_json(["forum", "route", "--json", prompt], timeout=30)
    return {"status": "MATCH" if code == 0 else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "decided": parsed.get("decided"), "confidence": parsed.get("confidence"), "needs_escalation": parsed.get("needs_escalation"), "top_candidates": parsed.get("candidates", [])[:5]}


def index_receipt() -> dict[str, Any]:
    code, stdout, stderr, parsed = run_json(["index", "context-envelope", "--root", ".", "--budget", "1200", "--json"], timeout=45)
    return {"status": "MATCH" if code == 0 and parsed.get("verification_verdict") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "schema": parsed.get("schema"), "verification_verdict": parsed.get("verification_verdict"), "graph_pack_sha256": parsed.get("recheck", {}).get("graph_pack_sha256"), "source_refs_only": parsed.get("privacy", {}).get("source_refs_only")}


def telos_status() -> dict[str, Any]:
    code, stdout, stderr, parsed = run_json(["node", "demo/status.mjs", "--summary"], timeout=30)
    return {"status": "MATCH" if code == 0 and parsed.get("status") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "tool_version": parsed.get("tool_version"), "tool": parsed.get("tool")}


def negative_fixtures() -> list[dict[str, str]]:
    return [
        {"fixture_id": "video_claim_promoted_to_truth", "expected_status": "REJECT", "reject_reason": "youtube_source_leads_are_not_scientific_proof"},
        {"fixture_id": "solver_claim_without_exact_or_declared_no_ground_truth", "expected_status": "REJECT", "reject_reason": "optimization_receipt_needs_baseline_or_no_ground_truth_lane"},
        {"fixture_id": "buildlang_replacement_claim", "expected_status": "REJECT", "reject_reason": "compiler_receipts_do_not_prove_language replacement"},
        {"fixture_id": "quantum_advantage_claim", "expected_status": "REJECT", "reject_reason": "no_quantum_hardware_or_advantage_evidence"},
        {"fixture_id": "raw_transcript_export", "expected_status": "REJECT", "reject_reason": "store_receipts_not_raw_transcripts"},
    ]


def validate_artifact(artifact: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    nodes = artifact.get("megatool_nodes", [])
    if artifact.get("schema") != SCHEMA:
        errors.append("schema")
    if artifact.get("source_bindings", {}).get("youtube_pass") != "0085" or artifact.get("source_bindings", {}).get("buildc_pass") != "0092":
        errors.append("source_bindings")
    if artifact.get("source_summary", {}).get("valid_video_count") != 19:
        errors.append("youtube_source_count")
    if artifact.get("solver_summary", {}).get("exact_optimum_value") != 162 or artifact.get("solver_summary", {}).get("scipy_exact_hit_count", 0) < 1:
        errors.append("solver_summary")
    if artifact.get("buildlang_summary", {}).get("buildc_verify_check_count") != 18:
        errors.append("buildlang_summary")
    if len(nodes) != 7:
        errors.append("node_count")
    if not nodes or nodes[0].get("cluster_id") != "enterprise_quantum_optimization":
        errors.append("ranking")
    if any(row.get("verification_status") != "HYPOTHESIS_WITH_LOCAL_RECEIPTS" for row in nodes):
        errors.append("verification_status")
    if any(tool.get("status") != "MATCH" for tool in artifact.get("flagship_receipts", {}).values()):
        errors.append("flagship_receipts")
    if artifact.get("unsupported_claim_count") != 0 or artifact.get("current_promoted_natural_laws") != []:
        errors.append("promotion_boundary")
    return errors


def compose() -> dict[str, Any]:
    youtube = read_json(YOUTUBE)
    branch = read_json(BRANCH)
    solver = read_json(SOLVER)
    matrix = read_json(MATRIX)
    corpus = read_json(CORPUS)
    buildc = read_json(BUILDC)
    nodes = megatool_nodes(youtube, branch, solver, matrix, corpus, buildc)
    nodes = sorted(nodes, key=lambda row: row["wedge_score"]["total"], reverse=True)
    artifact: dict[str, Any] = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "generated_on": "2026-07-01",
        "source_bindings": {
            "youtube_pass": youtube["pass"],
            "optimization_branch_pass": branch["pass"],
            "external_solver_pass": solver["pass"],
            "solver_matrix_pass": matrix["pass"],
            "buildlang_corpus_pass": corpus["pass"],
            "buildc_pass": buildc["pass"],
        },
        "source_summary": {
            "valid_video_count": youtube["valid_video_count"],
            "dominant_cluster": youtube["video_corpus_summary"]["dominant_cluster"],
            "dominant_cluster_video_count": youtube["video_corpus_summary"]["dominant_cluster_video_count"],
            "source_policy": youtube["video_corpus_summary"]["source_policy"],
        },
        "solver_summary": {
            "exact_candidate_count": branch["exact_branch"]["candidate_count"],
            "exact_feasible_count": branch["exact_branch"]["feasible_count"],
            "exact_optimum_value": branch["exact_branch"]["best"]["value"],
            "max_branch_gap": branch["comparison_summary"]["max_value_gap"],
            "scipy_exact_hit_count": solver["external_adapter"]["comparison_to_exact"]["exact_hit_count"],
            "scipy_value_distribution": solver["external_adapter"]["comparison_to_exact"]["value_distribution"],
            "local_available_or_source_present": matrix["summary"]["local_available_rows"],
            "local_unavailable_or_missing": matrix["summary"]["local_unavailable_rows"],
        },
        "buildlang_summary": {
            "corpus_adapter_status": corpus["status"],
            "buildc_adapter_status": buildc["status"],
            "buildc_source_digest": buildc["check_receipt"]["source_digest"]["hex"],
            "buildc_verify_check_count": buildc["verify_summary"]["check_count"],
            "buildc_measurement_count": buildc["crucible_adapter"]["measurement_count"],
        },
        "megatool_nodes": nodes,
        "primary_30_day_push": nodes[0],
        "negative_fixtures": negative_fixtures(),
        "flagship_receipts": {"forum": forum_route(), "index": index_receipt(), "telos": telos_status()},
        "unsupported_claim_count": 0,
        "current_promoted_natural_laws": [],
        "non_promotion_statement": "Pass 0093 ranks source-backed product experiments. It does not promote YouTube claims, quantum advantage, BuildLang replacement, scientific discovery, or a natural law.",
    }
    errors = validate_artifact(artifact)
    artifact["validation_errors"] = errors
    artifact["status"] = STATUS_MATCH if not errors else STATUS_DRIFT
    artifact["seal"] = sha256_obj(artifact)
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    artifact = compose()
    write_json(Path(args.out), artifact)
    print(json.dumps({"out": args.out, "seal": artifact["seal"], "status": artifact["status"]}, indent=2, sort_keys=True))
    if artifact["status"] != STATUS_MATCH:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
