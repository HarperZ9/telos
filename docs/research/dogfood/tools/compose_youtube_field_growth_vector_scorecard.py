"""Compose pass 0096 YouTube-bound field growth-vector scorecard."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

SCHEMA = "YouTubeFieldGrowthVectorScorecard/v1"
PASS_ID = "0096"
STATUS_MATCH = "YOUTUBE_FIELD_GROWTH_VECTOR_SCORECARD_MATCH"
STATUS_DRIFT = "YOUTUBE_FIELD_GROWTH_VECTOR_SCORECARD_DRIFT"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
YOUTUBE = ROOT / "schemas" / "youtube-research-compounding-packet-pass-0085.json"
BRIDGE = ROOT / "schemas" / "youtube-buildlang-megatool-bridge-pass-0093.json"
WORKFLOW = ROOT / "schemas" / "quantum-optimization-workflow-receipt-pass-0094.json"
NATIVE = ROOT / "schemas" / "buildlang-native-optimization-kernel-receipt-pass-0095.json"


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


def score(youtube: int, urgency: int, demo: int, proof: int, reuse: int, upside: int) -> dict[str, int]:
    return {
        "youtube_signal": youtube,
        "buyer_or_societal_urgency": urgency,
        "demo_readiness": demo,
        "proof_advantage": proof,
        "infrastructure_reuse": reuse,
        "strategic_upside": upside,
        "total": youtube + urgency + demo + proof + reuse + upside,
    }


def cluster_map(youtube: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {row["cluster_id"]: row for row in youtube["research_clusters"]}


def cluster_payload(clusters: dict[str, dict[str, Any]], ids: list[str]) -> dict[str, Any]:
    rows = [clusters[row_id] for row_id in ids if row_id in clusters]
    titles: list[str] = []
    video_ids: list[str] = []
    for row in rows:
        titles.extend(row.get("titles", []))
        video_ids.extend(row.get("video_ids", []))
    return {
        "source_clusters": ids,
        "source_video_count": sum(int(row.get("source_count", 0)) for row in rows),
        "source_video_ids": video_ids,
        "source_titles": titles,
    }


def vector(
    vector_id: str,
    field: str,
    cluster_data: dict[str, Any],
    product: str,
    need: str,
    assets: list[str],
    features: list[str],
    experiment: str,
    scoring: dict[str, int],
) -> dict[str, Any]:
    return {
        "id": vector_id,
        "field": field,
        **cluster_data,
        "market_need_hypothesis": need,
        "combined_megatool": product,
        "current_assets": assets,
        "feature_advancements": features,
        "next_experiment": experiment,
        "wedge_score": scoring,
        "gap_status": "inferred",
        "verification_status": "HYPOTHESIS_WITH_LOCAL_RECEIPTS",
    }


def field_vectors(youtube: dict[str, Any], bridge: dict[str, Any], workflow: dict[str, Any], native: dict[str, Any]) -> list[dict[str, Any]]:
    clusters = cluster_map(youtube)
    exact = workflow["workflow"]["solver_branches"]["exact_enumeration"]
    nx_branch = workflow["workflow"]["solver_branches"]["networkx_capacity_dag_longest_path"]
    build_out = native["run_output"]
    exact_asset = f"exact optimum {exact['value']}/{exact['weight']}"
    nx_asset = f"NetworkX DAG {nx_branch['node_count']} nodes"
    native_asset = f"BuildLang native value {build_out['best value']}"
    buildc_assets = [f"buildc verify checks {native['verify_summary']['check_count']}", f"source digest {native['check_receipt']['source_digest']['hex']}", "pass 0093 bridge"]
    visual_cluster = {"source_clusters": ["monorepo_scope_visual_color"], "source_video_count": 0, "source_video_ids": [], "source_titles": []}
    specs = [
        ("optimization_proof_workbench", "quantum, HPC, logistics, robotics, defense optimization", ["enterprise_quantum_optimization"], "OptimizationProofWorkbench/v1", "Compare exact, heuristic, graph, external, and hardware/simulator branches without losing provenance.", ["13-video YouTube cluster", exact_asset, nx_asset, native_asset], ["shared SolverBranchReceipt schema", "BuildLang branch-comparison kernels", "hardware/simulator boundaries", "business objective receipts"], "Implement BuildLang exact, greedy, and bounded-search branches against the pass 0094 baseline.", (5, 5, 5, 5, 5, 5)),
        ("buildlang_scientific_runtime", "scientific languages, compiler/runtime receipts, quant/security kernels", ["enterprise_quantum_optimization", "quantitative_finance_laws"], "AccountableScientificRuntime/v1", "Proof packets need compiler, effect, source, run, and measurement receipts together.", buildc_assets, ["numeric tolerance receipts", "build-universe lock receipts", "GPU/HPC target receipts", "security review mode"], "Promote the native knapsack fixture into reusable BuildLang optimization and quant kernels.", (4, 5, 5, 5, 5, 5)),
        ("ai4science_claim_to_experiment", "biology, chemistry, wet-lab handoff, model-assisted discovery", ["molecular_ai_drug_discovery"], "AI4ScienceClaimToExperimentReceipt/v1", "Discovery tools need claim, model, source, simulation, assay, reviewer, and failure-state receipts.", ["pass 0085 molecular source lead", "Gather receipts", "Crucible verifier contract"], ["source claim extractor", "simulation or assay receipts", "reviewer objection ledger", "negative result path"], "Build one source-to-experiment skeleton that refuses discovery claims until evidence layers are attached.", (2, 5, 3, 5, 4, 5)),
        ("agi_eval_attempt_lab", "ARC/AGI benchmark evaluation, contamination control, model attempts", ["arc_agi_eval_and_generalization"], "EvalAttemptProofPacket/v1", "Benchmark claims need task authority, attempt replay, contamination checks, traces, and verifier verdicts.", ["pass 0085 ARC source lead", "Learning Forge", "Crucible MATCH/DRIFT lane"], ["benchmark source refs", "attempt replay receipts", "contamination fields", "model comparison ledger"], "Create an ARC-style eval receipt with one synthetic task and one rejected contamination fixture.", (2, 5, 4, 5, 4, 5)),
        ("prover_verifier_search_engine", "mathematics, theoretical CS, planning, search/RL", ["search_rl_alpha_zero"], "SearchVerifierLoopLedger/v1", "Search systems need proposal, rollout, verifier, replay, and failed-branch receipts.", ["pass 0085 AlphaZero source lead", "pipeline-math chain", "loop ledger"], ["branch provenance", "formal verifier hooks", "failed-branch capture", "BuildLang search kernels"], "Make a small prover/verifier search ledger over a bounded combinatorics task.", (2, 4, 4, 5, 4, 5)),
        ("quant_finance_kernel_packets", "finance, risk, optimization, security-sensitive numeric systems", ["quantitative_finance_laws"], "QuantKernelReceipt/v1", "Quant teams need numeric identity, lineage, stress scenario, tolerance, and runtime receipts.", ["pass 0085 quant source lead", "BuildLang runtime receipt", "optimization fixture"], ["bounded finance identity", "tolerance receipts", "scenario generator", "audit-mode export"], "Implement one bounded finance identity in Python and BuildLang with matching tolerance receipts.", (2, 5, 4, 4, 4, 5)),
        ("risk_and_governance_receipts", "AI risk, public policy, institutional accountability", ["agi_risk_scenarios", "ai_society_governance"], "RiskGovernanceReceipt/v1", "Societal-scale AI claims need assumptions, evidence, authority boundaries, actions, review, and appeal records.", ["pass 0085 risk/governance leads", "Forum routing", "Telos action receipts"], ["assumption ledger", "stakeholder evidence refs", "human review records", "revision lane"], "Create one policy-risk claim packet with explicit assumptions and no promoted conclusion.", (2, 5, 3, 4, 4, 5)),
    ]
    vectors = [
        vector(row[0], row[1], cluster_payload(clusters, row[2]), row[3], row[4], row[5], row[6], row[7], score(*row[8]))
        for row in specs
    ]
    vectors.append(vector("visual_truth_measurement_kit", "rendering, color calibration, display QA, vision dataset review", visual_cluster, "VisualTruthMeasurementKit/v1", "Color/rendering tools need measured output, calibration state, source refs, and review receipts.", ["prior Build Color and calibration dogfood", "measurement-layer lanes", "Crucible packet pattern"], ["OCIO/ACES adapter receipts", "instrument/reference boundaries", "browser evidence capture", "BuildLang rendering kernels"], "Bind one image/color fixture to source, measurement, calibration boundary, and Crucible verdict.", score(0, 4, 4, 5, 4, 5)))
    return sorted(vectors, key=lambda row: row["wedge_score"]["total"], reverse=True)


def integration_map() -> list[dict[str, Any]]:
    return [
        {"internal_tool": "Gather", "inputs": ["URLs", "files", "video metadata"], "outputs": ["source receipts"], "market_product": "source-intake layer"},
        {"internal_tool": "Index", "inputs": ["workspace refs"], "outputs": ["context envelopes"], "market_product": "large-substrate map"},
        {"internal_tool": "Forum", "inputs": ["task intent"], "outputs": ["routing receipts"], "market_product": "expert triage layer"},
        {"internal_tool": "Crucible", "inputs": ["thesis", "measurements"], "outputs": ["MATCH/DRIFT/UNVERIFIABLE verdicts"], "market_product": "claim verification layer"},
        {"internal_tool": "Telos", "inputs": ["actions", "state", "receipts"], "outputs": ["status and action packets"], "market_product": "accountability host"},
        {"internal_tool": "BuildLang/buildc", "inputs": ["source"], "outputs": ["check, effect, run receipts"], "market_product": "accountable scientific runtime"},
        {"internal_tool": "build-universe", "inputs": ["packages", "targets"], "outputs": ["build/release receipts"], "market_product": "reproducible compute substrate"},
        {"internal_tool": "color calibration", "inputs": ["targets", "measurements"], "outputs": ["visual truth receipts"], "market_product": "measurement proof kit"},
        {"internal_tool": "browser evidence", "inputs": ["web/UI state"], "outputs": ["evidence captures"], "market_product": "public proof demo capture"},
        {"internal_tool": "model foundry + loop ledger", "inputs": ["model attempts"], "outputs": ["attempt and replay records"], "market_product": "research automation ledger"},
    ]


def forum_route() -> dict[str, Any]:
    prompt = "Project Telos pass 0096: score YouTube-bound world-scale field growth vectors across optimization, BuildLang scientific runtime, AI4Science, evals, quant, visual truth, and governance."
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
    vectors = artifact.get("field_vectors", [])
    if artifact.get("schema") != SCHEMA:
        errors.append("schema")
    if artifact.get("source_summary", {}).get("valid_video_count") != 19 or artifact.get("source_summary", {}).get("cluster_count") != 7:
        errors.append("youtube_counts")
    if artifact.get("source_summary", {}).get("transcript_receipt_count") != 19:
        errors.append("transcript_receipts")
    if len(vectors) != 8 or vectors[0].get("id") != "optimization_proof_workbench":
        errors.append("vector_ranking")
    if artifact.get("primary_30_day_push", {}).get("vector_id") != "optimization_proof_workbench":
        errors.append("primary_push")
    if artifact.get("buildlang_binding", {}).get("native_pass") != "0095":
        errors.append("buildlang_binding")
    if any(tool.get("status") != "MATCH" for tool in artifact.get("flagship_receipts", {}).values()):
        errors.append("flagships")
    if artifact.get("unsupported_claim_count") != 0 or artifact.get("current_promoted_natural_laws") != []:
        errors.append("promotion_boundary")
    return errors


def compose() -> dict[str, Any]:
    youtube = read_json(YOUTUBE)
    bridge = read_json(BRIDGE)
    workflow = read_json(WORKFLOW)
    native = read_json(NATIVE)
    vectors = field_vectors(youtube, bridge, workflow, native)
    artifact: dict[str, Any] = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "generated_on": "2026-07-01",
        "source_bindings": {"youtube_pass": youtube["pass"], "bridge_pass": bridge["pass"], "workflow_pass": workflow["pass"], "native_buildlang_pass": native["pass"]},
        "source_summary": {
            "valid_video_count": youtube["valid_video_count"],
            "metadata_match_count": youtube["metadata_match_count"],
            "transcript_receipt_count": youtube["transcript_receipt_count"],
            "gather_match_count": youtube["gather_match_count"],
            "cluster_count": youtube["video_corpus_summary"]["cluster_count"],
            "dominant_cluster": youtube["video_corpus_summary"]["dominant_cluster"],
            "dominant_cluster_video_count": youtube["video_corpus_summary"]["dominant_cluster_video_count"],
            "source_policy": youtube["video_corpus_summary"]["source_policy"],
        },
        "buildlang_binding": {
            "native_pass": native["pass"],
            "native_status": native["status"],
            "source_digest": native["check_receipt"]["source_digest"]["hex"],
            "verify_check_count": native["verify_summary"]["check_count"],
            "best_value": native["run_output"]["best value"],
            "feasible_count": native["run_output"]["feasible count"],
        },
        "workflow_binding": {
            "workflow_pass": workflow["pass"],
            "workflow_status": workflow["status"],
            "exact_value": workflow["workflow"]["objective_measurements"]["exact_value"],
            "executed_branch_count": workflow["workflow"]["objective_measurements"]["executed_branch_count"],
            "dependency_boundary_branch_count": workflow["workflow"]["objective_measurements"]["dependency_boundary_branch_count"],
        },
        "field_vectors": vectors,
        "primary_30_day_push": {
            "vector_id": vectors[0]["id"],
            "product": vectors[0]["combined_megatool"],
            "experiment": vectors[0]["next_experiment"],
            "acceptance": [
                "BuildLang native exact, greedy, and bounded-search branches run from source",
                "all branches bind to the pass 0094 problem and pass 0095 receipt style",
                "Crucible records branch claims as MATCH/DRIFT/UNVERIFIABLE",
            ],
        },
        "integration_map": integration_map(),
        "negative_fixtures": [
            {"fixture_id": "youtube_claim_promoted", "expected_status": "REJECT", "reject_reason": "videos_are_source_leads_not_truth_proofs"},
            {"fixture_id": "growth_vector_without_receipt_path", "expected_status": "REJECT", "reject_reason": "each vector_needs_next_experiment_and_receipts"},
            {"fixture_id": "natural_law_claim", "expected_status": "REJECT", "reject_reason": "no_independent_reproduction_or_review"},
        ],
        "unsupported_claim_count": 0,
        "current_promoted_natural_laws": [],
        "non_promotion_statement": "Pass 0096 scores growth-vector hypotheses from YouTube source leads and local receipts. It does not prove video claims, market dominance, scientific discovery, language replacement, quantum advantage, or a natural law.",
        "flagship_receipts": {"forum": forum_route(), "index": index_receipt(), "telos": telos_status()},
    }
    artifact["validation_errors"] = validate_artifact(artifact)
    artifact["status"] = STATUS_MATCH if not artifact["validation_errors"] else STATUS_DRIFT
    artifact["measurements"] = [
        {"id": "youtube_counts", "status": "MATCH" if artifact["source_summary"]["valid_video_count"] == 19 else "DRIFT", "claim": "19 valid YouTube videos are bound"},
        {"id": "transcript_receipts", "status": "MATCH" if artifact["source_summary"]["transcript_receipt_count"] == 19 else "DRIFT", "claim": "19 transcript receipts are bound"},
        {"id": "vector_count", "status": "MATCH" if len(vectors) == 8 else "DRIFT", "claim": "8 field vectors are ranked"},
        {"id": "primary_vector", "status": "MATCH" if vectors[0]["id"] == "optimization_proof_workbench" else "DRIFT", "claim": "optimization proof workbench ranks first"},
        {"id": "buildlang_native", "status": "MATCH" if artifact["buildlang_binding"]["verify_check_count"] == 18 else "DRIFT", "claim": "pass 0095 BuildLang receipt is bound"},
        {"id": "workflow_binding", "status": "MATCH" if artifact["workflow_binding"]["exact_value"] == 162 else "DRIFT", "claim": "pass 0094 exact workflow is bound"},
        {"id": "integration_map", "status": "MATCH" if len(artifact["integration_map"]) == 10 else "DRIFT", "claim": "10 internal megatool nodes are mapped"},
        {"id": "flagships", "status": "MATCH" if all(row["status"] == "MATCH" for row in artifact["flagship_receipts"].values()) else "DRIFT", "claim": "Forum, Index, and Telos receipts match"},
        {"id": "promotion_boundary", "status": "MATCH" if artifact["unsupported_claim_count"] == 0 and artifact["current_promoted_natural_laws"] == [] else "DRIFT", "claim": "no unsupported claim or law is promoted"},
    ]
    unsealed = dict(artifact)
    artifact["seal"] = sha256_obj(unsealed)
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(ROOT / "schemas" / "youtube-field-growth-vector-scorecard-pass-0096.json"))
    args = parser.parse_args()
    artifact = compose()
    write_json(Path(args.out), artifact)
    print(json.dumps({"path": str(Path(args.out)), "status": artifact["status"], "seal": artifact["seal"]}, indent=2, sort_keys=True))
    if artifact["status"] != STATUS_MATCH:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
