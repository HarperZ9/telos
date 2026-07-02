"""Compose pass 0088 optimization branch comparison receipt."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import subprocess
from itertools import product
from pathlib import Path
from typing import Any

SCHEMA = "OptimizationBranchComparisonReceipt/v1"
PASS_ID = "0088"
STATUS_MATCH = "OPTIMIZATION_BRANCH_COMPARISON_RECEIPT_MATCH"
STATUS_DRIFT = "OPTIMIZATION_BRANCH_COMPARISON_RECEIPT_DRIFT"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
BASELINE = ROOT / "schemas" / "quantum-simulator-branch-adapter-pass-0087.json"
YOUTUBE_BASELINE = ROOT / "schemas" / "youtube-research-compounding-packet-pass-0085.json"
ITEMS = [
    ("A", 31, 5), ("B", 21, 4), ("C", 27, 7), ("D", 40, 6),
    ("E", 17, 3), ("F", 33, 7), ("G", 18, 7), ("H", 13, 6),
    ("I", 32, 5), ("J", 27, 11), ("K", 19, 7), ("L", 5, 2),
]
CAPACITY = 29
PENALTY = 20
SA_SEEDS = list(range(8800, 8864))
RS_SEEDS = list(range(18800, 18864))
BETAS = [0.03, 0.06, 0.12, 0.25, 0.5, 1.0, 2.0, 4.0, 8.0]
SOURCE_ANCHORS = [
    {"source_id": "or-tools-knapsack", "url": "https://developers.google.com/optimization/pack/knapsack", "verification_status": "SOURCE_LEAD"},
    {"source_id": "or-tools-mip", "url": "https://developers.google.com/optimization/mip/mip_example", "verification_status": "SOURCE_LEAD"},
    {"source_id": "scipy-dual-annealing", "url": "https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.dual_annealing.html", "verification_status": "SOURCE_LEAD"},
    {"source_id": "dwave-samplers", "url": "https://docs.dwavequantum.com/en/latest/ocean/api_ref_samplers/index.html", "verification_status": "SOURCE_LEAD"},
]


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


def score(bits: list[int]) -> tuple[int, int, int, int]:
    value = sum(bit * item[1] for bit, item in zip(bits, ITEMS))
    weight = sum(bit * item[2] for bit, item in zip(bits, ITEMS))
    violation = max(0, weight - CAPACITY)
    energy = -value + PENALTY * violation * violation
    return energy, value, weight, violation


def row(bits: list[int]) -> dict[str, Any]:
    energy, value, weight, violation = score(bits)
    return {"bits": bits, "selected": [item[0] for bit, item in zip(bits, ITEMS) if bit], "value": value, "weight": weight, "capacity_violation": violation, "energy": energy, "feasible": violation == 0}


def exact_branch() -> dict[str, Any]:
    candidates = [row(list(bits)) for bits in product([0, 1], repeat=len(ITEMS))]
    feasible = [candidate for candidate in candidates if candidate["feasible"]]
    best = max(feasible, key=lambda candidate: (candidate["value"], -candidate["weight"], candidate["selected"]))
    return {"branch": "exact_enumeration", "candidate_count": len(candidates), "feasible_count": len(feasible), "infeasible_count": len(candidates) - len(feasible), "candidate_digest": sha256_obj(candidates), "best": best, "top_feasible": sorted(feasible, key=lambda candidate: (-candidate["value"], candidate["weight"], candidate["selected"]))[:8]}


def greedy_branch() -> dict[str, Any]:
    bits = [0] * len(ITEMS)
    remaining = CAPACITY
    for _, index in sorted(((item[1] / item[2], i) for i, item in enumerate(ITEMS)), reverse=True):
        weight = ITEMS[index][2]
        if weight <= remaining:
            bits[index] = 1
            remaining -= weight
    return {"branch": "value_density_greedy", "run_count": 1, "best": row(bits), "policy": "sort_by_value_per_weight_desc_then_pack_if_fits"}


def anneal_once(seed: int) -> dict[str, Any]:
    rng = random.Random(seed)
    bits = [rng.randrange(2) for _ in ITEMS]
    best = row(list(bits))
    accepted = 0
    proposals = 0
    for beta in BETAS:
        for _ in range(18):
            for index in rng.sample(range(len(bits)), len(bits)):
                current = score(bits)[0]
                trial = list(bits)
                trial[index] = 1 - trial[index]
                trial_row = row(trial)
                delta = trial_row["energy"] - current
                proposals += 1
                if delta <= 0 or rng.random() < math.exp(-beta * delta):
                    bits = trial
                    accepted += 1
                    if (trial_row["energy"], -trial_row["value"], trial_row["weight"]) < (best["energy"], -best["value"], best["weight"]):
                        best = trial_row
    return {"seed": seed, "best": best, "accepted_moves": accepted, "proposal_count": proposals}


def annealing_branch() -> dict[str, Any]:
    runs = [anneal_once(seed) for seed in SA_SEEDS]
    best = min((run["best"] for run in runs), key=lambda candidate: (candidate["energy"], -candidate["value"], candidate["weight"]))
    return {"branch": "seeded_simulated_annealing", "run_count": len(runs), "seed_range": [SA_SEEDS[0], SA_SEEDS[-1]], "beta_schedule": BETAS, "runs_sha256": sha256_obj(runs), "runs": runs, "best": best}


def random_search_branch() -> dict[str, Any]:
    runs = []
    for seed in RS_SEEDS:
        rng = random.Random(seed)
        samples = [row([rng.randrange(2) for _ in ITEMS]) for _ in range(512)]
        runs.append({"seed": seed, "sample_count": len(samples), "best": min(samples, key=lambda candidate: (candidate["energy"], -candidate["value"], candidate["weight"]))})
    best = min((run["best"] for run in runs), key=lambda candidate: (candidate["energy"], -candidate["value"], candidate["weight"]))
    return {"branch": "seeded_random_search", "run_count": len(runs), "seed_range": [RS_SEEDS[0], RS_SEEDS[-1]], "samples_per_seed": 512, "runs_sha256": sha256_obj(runs), "runs": runs, "best": best}


def compare_branches(exact: dict[str, Any], branches: list[dict[str, Any]]) -> list[dict[str, Any]]:
    exact_bits = exact["best"]["bits"]
    exact_value = exact["best"]["value"]
    return [{"branch": branch["branch"], "best_value": branch["best"]["value"], "best_weight": branch["best"]["weight"], "best_energy": branch["best"]["energy"], "exact_value_gap": exact_value - branch["best"]["value"], "hit_exact_bits": branch["best"]["bits"] == exact_bits, "feasible": branch["best"]["feasible"]} for branch in branches]


def run_json(command: list[str], timeout: int = 45) -> tuple[int, str, str, dict[str, Any]]:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    parsed = json.loads(result.stdout) if result.returncode == 0 and result.stdout.strip() else {}
    return result.returncode, result.stdout, result.stderr, parsed


def forum_route() -> dict[str, Any]:
    prompt = "Project Telos pass 0088: exact-enumerable optimization branch comparison receipt for exact, simulated annealing, greedy, and random-search baselines."
    code, stdout, stderr, parsed = run_json(["forum", "route", "--json", prompt], timeout=30)
    return {"status": "MATCH" if code == 0 else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "decided": parsed.get("decided"), "confidence": parsed.get("confidence"), "needs_escalation": parsed.get("needs_escalation"), "top_candidates": parsed.get("candidates", [])[:5]}


def index_receipt() -> dict[str, Any]:
    code, stdout, stderr, parsed = run_json(["index", "context-envelope", "--root", ".", "--budget", "1200", "--json"], timeout=45)
    return {"status": "MATCH" if code == 0 and parsed.get("verification_verdict") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "schema": parsed.get("schema"), "verification_verdict": parsed.get("verification_verdict"), "graph_pack_sha256": parsed.get("recheck", {}).get("graph_pack_sha256"), "source_refs_only": parsed.get("privacy", {}).get("source_refs_only")}


def telos_status() -> dict[str, Any]:
    code, stdout, stderr, parsed = run_json(["node", "demo/status.mjs", "--summary"], timeout=30)
    return {"status": "MATCH" if code == 0 and parsed.get("status") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "tool_version": parsed.get("tool_version"), "tool": parsed.get("tool")}


def compose() -> dict[str, Any]:
    prior = read_json(BASELINE)
    youtube = read_json(YOUTUBE_BASELINE)
    youtube_summary = youtube["video_corpus_summary"]
    exact = exact_branch()
    branches = [annealing_branch(), greedy_branch(), random_search_branch()]
    comparisons = compare_branches(exact, branches)
    artifact: dict[str, Any] = {
        "schema": SCHEMA, "pass": PASS_ID, "generated_on": "2026-07-01",
        "prior_binding": {"source_pass": "0087", "source_schema": prior["schema"], "source_seal": prior["seal"], "replay_gate": prior["comparison_to_exact"]["status"]},
        "upstream_research_binding": {
            "source_pass": "0085",
            "source_schema": youtube["schema"],
            "source_seal": youtube["seal"],
            "dominant_cluster": youtube_summary["dominant_cluster"],
            "dominant_cluster_video_count": youtube_summary["dominant_cluster_video_count"],
            "source_policy": youtube_summary["source_policy"],
        },
        "source_anchors": SOURCE_ANCHORS,
        "problem": {"problem_id": "branch_comparison_knapsack_12_binary", "items": [{"id": i, "value": v, "weight": w} for i, v, w in ITEMS], "capacity": CAPACITY, "penalty": PENALTY},
        "exact_branch": exact, "branches": branches, "comparisons": comparisons,
        "comparison_summary": {"branch_count": len(branches) + 1, "all_branches_feasible": all(row["feasible"] for row in comparisons), "exact_hit_branches": [row["branch"] for row in comparisons if row["hit_exact_bits"]], "max_value_gap": max(row["exact_value_gap"] for row in comparisons)},
        "promotion_boundary": {"benchmark_only": True, "solver_superiority_claim": False, "quantum_hardware_claim": False, "quantum_advantage_claim": False, "new_natural_law_claim": False},
        "flagship_receipts": {"forum": forum_route(), "index": index_receipt(), "telos": telos_status()},
        "negative_fixtures": negative_fixtures(), "unsupported_claim_count": 0, "current_promoted_natural_laws": [],
        "non_promotion_statement": "Pass 0088 compares bounded local optimization branches against exact enumeration; it does not claim solver superiority, hardware execution, quantum advantage, or a natural law.",
    }
    errors = validate_artifact(artifact)
    artifact["validation_errors"] = errors
    artifact["status"] = STATUS_MATCH if not errors else STATUS_DRIFT
    artifact["seal"] = sha256_obj(artifact)
    return artifact


def negative_fixtures() -> list[dict[str, str]]:
    return [
        {"fixture_id": "missing_exact_branch", "expected_status": "REJECT", "reject_reason": "branch_comparison_requires_ground_truth"},
        {"fixture_id": "unsealed_branch_runs", "expected_status": "REJECT", "reject_reason": "stochastic_branch_runs_require_digest"},
        {"fixture_id": "single_branch_only", "expected_status": "REJECT", "reject_reason": "comparison_requires_multiple_branches"},
        {"fixture_id": "solver_superiority_claim", "expected_status": "REJECT", "reject_reason": "toy_benchmark_does_not_prove_general_superiority"},
        {"fixture_id": "quantum_advantage_claim", "expected_status": "REJECT", "reject_reason": "no_quantum_hardware_or_scaling_evidence"},
        {"fixture_id": "natural_law_claim", "expected_status": "REJECT", "reject_reason": "optimization_benchmark_is_not_a_natural_law"},
    ]


def validate_artifact(artifact: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    exact = artifact.get("exact_branch", {})
    branches = artifact.get("branches", [])
    boundary = artifact.get("promotion_boundary", {})
    if artifact.get("schema") != SCHEMA:
        errors.append("schema")
    if artifact.get("prior_binding", {}).get("source_pass") != "0087":
        errors.append("prior_binding")
    if artifact.get("upstream_research_binding", {}).get("dominant_cluster") != "enterprise_quantum_optimization":
        errors.append("upstream_research_binding")
    if exact.get("candidate_count") != 4096 or exact.get("best", {}).get("feasible") is not True:
        errors.append("exact_branch")
    if len(branches) != 3 or len(artifact.get("comparisons", [])) != 3:
        errors.append("branch_count")
    if any(row.get("exact_value_gap", -1) < 0 for row in artifact.get("comparisons", [])):
        errors.append("comparison_gap")
    if not artifact.get("comparison_summary", {}).get("exact_hit_branches"):
        errors.append("exact_hits")
    if any(boundary.get(key) for key in ["solver_superiority_claim", "quantum_hardware_claim", "quantum_advantage_claim", "new_natural_law_claim"]):
        errors.append("promotion_boundary")
    if any(receipt.get("status") != "MATCH" for receipt in artifact.get("flagship_receipts", {}).values()):
        errors.append("flagship_receipts")
    if artifact.get("unsupported_claim_count") != 0 or artifact.get("current_promoted_natural_laws") != []:
        errors.append("unsupported_claims")
    return errors


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
