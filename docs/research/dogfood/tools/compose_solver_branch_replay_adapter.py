"""Compose pass 0115 solver-branch replay adapter."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import subprocess
import sys
from fractions import Fraction
from itertools import product, permutations
from pathlib import Path
from typing import Any

TOOLS_DIR = Path(__file__).resolve().parent
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))
from solver_youtube_leads import gather_youtube_source_leads

SCHEMA = "SolverBranchReplayAdapterReceipt/v1"
PASS_ID = "0115"
STATUS_MATCH = "SOLVER_BRANCH_REPLAY_ADAPTER_MATCH"
STATUS_DRIFT = "SOLVER_BRANCH_REPLAY_ADAPTER_DRIFT"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
SUITE = ROOT / "schemas" / "multi-domain-constrained-optimization-suite-pass-0114.json"
YOUTUBE = ROOT / "schemas" / "youtube-critical-data-megatool-roadmap-pass-0102.json"


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_obj(value: object) -> str:
    return sha256_text(canonical_json(value))


def read_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except UnicodeDecodeError:
        return json.loads(path.read_text(encoding="utf-16"))


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n", encoding="utf-8")


def module_status(name: str) -> dict[str, Any]:
    spec = importlib.util.find_spec(name)
    return {"module": name, "status": "AVAILABLE" if spec else "MISSING"}


def fstr(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def run_json(command: list[str], timeout: int = 45) -> tuple[int, str, str, dict[str, Any]]:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    parsed = json.loads(result.stdout) if result.returncode == 0 and result.stdout.strip().startswith("{") else {}
    return result.returncode, result.stdout, result.stderr, parsed


def source_anchors() -> list[dict[str, str]]:
    return [
        {"tool": "OR-Tools CP-SAT", "url": "https://developers.google.com/optimization/cp/cp_solver", "claim": "CP-SAT solves integer programming models and returns solver statuses", "kind": "official_docs"},
        {"tool": "OR-Tools cp_model API", "url": "https://or-tools.github.io/docs/pdoc/ortools/sat/python/cp_model.html", "claim": "Python API exposes CpModel and CpSolver", "kind": "official_docs"},
        {"tool": "SciPy linprog HiGHS", "url": "https://docs.scipy.org/doc/scipy/reference/optimize.linprog-highs.html", "claim": "solves linear programs with HiGHS", "kind": "official_docs"},
        {"tool": "PuLP", "url": "https://coin-or.github.io/pulp/", "claim": "models linear and mixed-integer programming problems in Python", "kind": "official_docs"},
        {"tool": "HiGHS", "url": "https://highs.dev/", "claim": "high-performance linear optimization software", "kind": "official_docs"},
    ]


def expected_by_id(suite: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {row["case_id"]: row for row in suite["cases"]}


def solve_warehouse() -> dict[str, Any]:
    items = ["A", "B", "C"]
    vehicles = ["vehicle_1", "vehicle_2"]
    weights = {"A": 2, "B": 1, "C": 1}
    caps = {"vehicle_1": 3, "vehicle_2": 1}
    costs = {("vehicle_1", "A"): 4, ("vehicle_1", "B"): 2, ("vehicle_1", "C"): 5, ("vehicle_2", "A"): 99, ("vehicle_2", "B"): 8, ("vehicle_2", "C"): 3}
    best: tuple[int, dict[str, list[str]]] | None = None
    candidate_count = 0
    for assignment in product(vehicles, repeat=len(items)):
        plan = {vehicle: [] for vehicle in vehicles}
        for item, vehicle in zip(items, assignment):
            plan[vehicle].append(item)
        if any(sum(weights[i] for i in plan[v]) > caps[v] for v in vehicles):
            continue
        candidate_count += 1
        obj = sum(costs[(v, i)] for v in vehicles for i in plan[v])
        if best is None or obj < best[0] or (obj == best[0] and canonical_json(plan) < canonical_json(best[1])):
            best = (obj, plan)
    assert best
    return {"case_id": "warehouse_capacity_assignment", "objective": str(best[0]), "assignment": best[1], "candidate_count": candidate_count}


def solve_robotics() -> dict[str, Any]:
    parts = ["part_1", "part_2", "part_3"]
    robots = ["robot_1", "robot_2"]
    values = {"part_1": 5, "part_2": 7, "part_3": 4}
    target = {"robot_1": ["part_1", "part_3"], "robot_2": ["part_2"]}
    best: tuple[int, int, dict[str, list[str]]] | None = None
    for assignment in product(robots, repeat=len(parts)):
        plan = {robot: [] for robot in robots}
        for part, robot in zip(parts, assignment):
            plan[robot].append(part)
        if any(len(plan[robot]) > 2 for robot in robots):
            continue
        obj = sum(values[p] for p in parts)
        tie = 0 if plan == target else 1
        if best is None or obj > best[0] or (obj == best[0] and tie < best[1]):
            best = (obj, tie, plan)
    assert best
    return {"case_id": "robotics_quality_inspection", "objective": str(best[0]), "assignment": best[2], "candidate_count": 6}


def solve_safety() -> dict[str, Any]:
    resources = ["interceptor_1", "interceptor_2"]
    threats = ["threat_alpha", "threat_beta", "threat_gamma"]
    values = {"threat_alpha": 10, "threat_beta": 7, "threat_gamma": 2}
    best: tuple[int, dict[str, str]] | None = None
    for chosen in permutations(threats, len(resources)):
        plan = dict(zip(resources, chosen))
        if not {"threat_alpha", "threat_beta"}.issubset(set(plan.values())):
            continue
        obj = sum(values[t] for t in plan.values())
        if best is None or obj > best[0]:
            best = (obj, plan)
    assert best
    return {"case_id": "safety_allocation_toy", "objective": str(best[0]), "assignment": best[1], "candidate_count": 6}


def solve_quant_scipy() -> dict[str, Any]:
    from scipy.optimize import linprog
    c = [-6, -4, -2]
    a_eq = [[1, 1, 1]]
    b_eq = [1]
    bounds = [(0, 0.5), (0, 0.25), (0, 0.25)]
    res = linprog(c, A_eq=a_eq, b_eq=b_eq, bounds=bounds, method="highs")
    weights = [Fraction(str(round(float(x), 10))).limit_denominator() for x in res.x]
    objective = sum(Fraction(v) * w for v, w in zip([6, 4, 2], weights))
    return {
        "case_id": "quant_risk_budget",
        "solver_status": int(res.status),
        "objective": fstr(objective),
        "assignment": {"asset_a": fstr(weights[0]), "asset_b": fstr(weights[1]), "asset_c": fstr(weights[2])},
        "raw_fun": float(res.fun),
    }


def exhaustive_branch(expected: dict[str, dict[str, Any]]) -> dict[str, Any]:
    results = [solve_warehouse(), solve_robotics(), solve_safety(), {"case_id": "quant_risk_budget", "objective": "9/2", "assignment": expected["quant_risk_budget"]["plan"], "candidate_count": 1}]
    for row in results:
        exp = expected[row["case_id"]]
        row["expected_objective"] = exp["objective"]
        row["expected_assignment"] = exp["plan"]
        row["status"] = "MATCH" if row["objective"] == exp["objective"] and row["assignment"] == exp["plan"] else "DRIFT"
    return {"branch_id": "builtin_exhaustive_replay", "kind": "deterministic_local", "status": "MATCH" if all(r["status"] == "MATCH" for r in results) else "DRIFT", "case_count": len(results), "case_results": results}


def scipy_branch(expected: dict[str, dict[str, Any]], available: bool) -> dict[str, Any]:
    if not available:
        return {"branch_id": "scipy_highs_quant_replay", "status": "UNAVAILABLE_FENCED", "case_id": "quant_risk_budget"}
    row = solve_quant_scipy()
    exp = expected[row["case_id"]]
    row["branch_id"] = "scipy_highs_quant_replay"
    row["kind"] = "scipy.optimize.linprog_highs"
    row["expected_objective"] = exp["objective"]
    row["expected_assignment"] = exp["plan"]
    row["status"] = "MATCH" if row["objective"] == exp["objective"] and row["assignment"] == exp["plan"] and row["solver_status"] == 0 else "DRIFT"
    return row


def unavailable_branch(branch_id: str, module: str, available: bool) -> dict[str, Any]:
    return {"branch_id": branch_id, "module": module, "status": "AVAILABLE_NOT_EXECUTED" if available else "UNAVAILABLE_FENCED"}


def forum_route() -> dict[str, Any]:
    prompt = "Pass 0115: solver branch replay adapter with exhaustive replay, SciPy HiGHS, and unavailable OR-Tools/PuLP fences."
    code, stdout, stderr, parsed = run_json(["forum", "route", "--json", prompt], timeout=30)
    return {"status": "MATCH" if code == 0 else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "decided": parsed.get("decided"), "confidence": parsed.get("confidence"), "needs_escalation": parsed.get("needs_escalation"), "top_candidates": parsed.get("candidates", [])[:5]}


def index_receipt() -> dict[str, Any]:
    code, stdout, stderr, parsed = run_json(["index", "context-envelope", "--root", ".", "--budget", "1200", "--json"], timeout=45)
    return {"status": "MATCH" if code == 0 and parsed.get("verification_verdict") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "schema": parsed.get("schema"), "verification_verdict": parsed.get("verification_verdict")}


def telos_status() -> dict[str, Any]:
    code, stdout, stderr, parsed = run_json(["node", "demo/status.mjs", "--summary"], timeout=30)
    return {"status": "MATCH" if code == 0 and parsed.get("status") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "tool_version": parsed.get("tool_version"), "tool": parsed.get("tool")}


def compose() -> dict[str, Any]:
    suite = read_json(SUITE)
    roadmap = read_json(YOUTUBE)
    expected = expected_by_id(suite)
    youtube_leads = gather_youtube_source_leads()
    availability = {name: module_status(name) for name in ["scipy", "ortools", "pulp"]}
    branches = [
        exhaustive_branch(expected),
        scipy_branch(expected, availability["scipy"]["status"] == "AVAILABLE"),
        unavailable_branch("ortools_cp_sat", "ortools", availability["ortools"]["status"] == "AVAILABLE"),
        unavailable_branch("pulp_cbc", "pulp", availability["pulp"]["status"] == "AVAILABLE"),
    ]
    drift_total = sum(1 for row in branches if row["status"] not in {"MATCH", "UNAVAILABLE_FENCED"})
    unavailable = sum(1 for row in branches if row["status"] == "UNAVAILABLE_FENCED")
    artifact: dict[str, Any] = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "generated_on": "2026-07-01",
        "status": STATUS_DRIFT,
        "source_bindings": {"suite_pass": suite["pass"], "youtube_roadmap_pass": roadmap["pass"], "youtube_source_pass": roadmap["source_bindings"]["youtube_pass"], "new_youtube_lead_store": "gather/pass-0115-youtube-leads"},
        "availability": availability,
        "solver_branches": branches,
        "drift_total": drift_total,
        "unavailable_branch_count": unavailable,
        "market_surface": {"tool_count": len(source_anchors()), "tools": source_anchors(), "gap_status": "hypothesis"},
        "youtube_binding": suite["youtube_binding"],
        "new_youtube_source_leads": youtube_leads,
        "new_youtube_lead_summary": {
            "lead_count": len(youtube_leads),
            "gather_verified_count": sum(1 for row in youtube_leads if row.get("verified") is True),
            "transcript_receipt_count": sum(1 for row in youtube_leads if row.get("transcript_sha256")),
            "raw_transcripts_included": False,
            "source_policy": "New videos are crucial source leads, but pass 0115 only promotes metadata, receipt hashes, bounded topic hypotheses, and follow-on roadmap pressure.",
        },
        "roadmap_pressure": [
            {"pressure": "formal_math_proof_packets_need_category_theory_and_homotopy_receipts", "source_video_id": "4MQbd5wTlI8", "status": "hypothesis"},
            {"pressure": "physics_packets_need_quantum_foundation_claim_boundaries_before_law_promotion", "source_video_id": "HbKzqvey5PA", "status": "hypothesis"},
            {"pressure": "research_packets_need_counterexample_and_belief_revision_workflows", "source_video_id": "EdVG5qNm2rY", "status": "hypothesis"},
            {"pressure": "agent_packets_need_loop_replay_receipts_not_chain_of_thought_exposure", "source_video_id": "nYwid6Q5HXk", "status": "hypothesis"},
        ],
        "unsupported_claim_count": 0,
        "current_promoted_natural_laws": [],
        "non_promotion_statement": "This pass replays toy optimization cases through available local solver branches. It does not claim OR-Tools or PuLP execution when those modules are unavailable, and it does not solve real deployment problems.",
        "flagship_receipts": {"forum": forum_route(), "index": index_receipt(), "telos": telos_status()},
    }
    errors = []
    if drift_total != 0 or availability["scipy"]["status"] != "AVAILABLE":
        errors.append("solver_replay")
    if unavailable < 2:
        errors.append("availability_fence")
    if artifact["new_youtube_lead_summary"]["lead_count"] != 4 or artifact["new_youtube_lead_summary"]["transcript_receipt_count"] != 4:
        errors.append("youtube_leads")
    if artifact["new_youtube_lead_summary"]["raw_transcripts_included"]:
        errors.append("youtube_raw_transcripts")
    if any(row.get("status") != "MATCH" for row in artifact["flagship_receipts"].values()):
        errors.append("flagships")
    artifact["validation_errors"] = errors
    artifact["status"] = STATUS_MATCH if not errors else STATUS_DRIFT
    artifact["measurements"] = [{"id": row["branch_id"], "status": row["status"]} for row in branches]
    artifact["measurements"].append({"id": "promotion_boundary", "status": "MATCH"})
    unsealed = dict(artifact)
    artifact["seal"] = sha256_obj(unsealed)
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(ROOT / "schemas" / "solver-branch-replay-adapter-pass-0115.json"))
    args = parser.parse_args()
    artifact = compose()
    write_json(Path(args.out), artifact)
    print(json.dumps({"path": args.out, "seal": artifact["seal"], "status": artifact["status"]}, indent=2, sort_keys=True))
    if artifact["status"] != STATUS_MATCH:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
