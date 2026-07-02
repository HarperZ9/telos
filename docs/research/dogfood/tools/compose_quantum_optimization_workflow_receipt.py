"""Compose pass 0094 quantum optimization workflow receipt."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import subprocess
from pathlib import Path
from typing import Any

SCHEMA = "QuantumOptimizationWorkflowReceipt/v1"
PASS_ID = "0094"
STATUS_MATCH = "QUANTUM_OPTIMIZATION_WORKFLOW_RECEIPT_MATCH"
STATUS_DRIFT = "QUANTUM_OPTIMIZATION_WORKFLOW_RECEIPT_DRIFT"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
YOUTUBE = ROOT / "schemas" / "youtube-research-compounding-packet-pass-0085.json"
BRANCH = ROOT / "schemas" / "optimization-branch-comparison-receipt-pass-0088.json"
SOLVER = ROOT / "schemas" / "external-solver-adapter-receipt-pass-0089.json"
MATRIX = ROOT / "schemas" / "solver-availability-matrix-receipt-pass-0090.json"
BUILDC = ROOT / "schemas" / "buildlang-check-receipt-adapter-pass-0092.json"
BRIDGE = ROOT / "schemas" / "youtube-buildlang-megatool-bridge-pass-0093.json"

SOURCE_ANCHORS = [
    {"source_id": "networkx-dag-longest-path", "url": "https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.dag.dag_longest_path.html", "verification_status": "OFFICIAL_WEB_SOURCE_2026_07_01"},
    {"source_id": "scipy-dual-annealing", "url": "https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.dual_annealing.html", "verification_status": "OFFICIAL_WEB_SOURCE_2026_07_01"},
    {"source_id": "ortools-knapsack", "url": "https://developers.google.com/optimization/pack/knapsack", "verification_status": "OFFICIAL_WEB_SOURCE_2026_07_01"},
    {"source_id": "dwave-ocean-samplers", "url": "https://docs.dwavequantum.com/en/latest/ocean/api_ref_samplers/index.html", "verification_status": "OFFICIAL_WEB_SOURCE_2026_07_01"},
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


def package_receipt(name: str) -> dict[str, Any]:
    try:
        spec = importlib.util.find_spec(name)
    except ModuleNotFoundError:
        spec = None
    return {"package": name, "available": spec is not None, "origin": spec.origin if spec else None}


def row_by_id(matrix: dict[str, Any], row_id: str) -> dict[str, Any]:
    return next((row for row in matrix["matrix_rows"] if row["row_id"] == row_id), {})


def networkx_dp_branch(problem: dict[str, Any], exact: dict[str, Any]) -> dict[str, Any]:
    receipt = package_receipt("networkx")
    if not receipt["available"]:
        return {"branch": "networkx_capacity_dag_longest_path", "status": "UNAVAILABLE", "dependency": receipt}
    import networkx as nx  # type: ignore

    items = problem["items"]
    capacity = problem["capacity"]
    graph = nx.DiGraph()
    for idx in range(len(items) + 1):
        for weight in range(capacity + 1):
            graph.add_node((idx, weight))
    for idx, item in enumerate(items):
        for weight in range(capacity + 1):
            graph.add_edge((idx, weight), (idx + 1, weight), value=0, action="skip", item_id=item["id"])
            next_weight = weight + item["weight"]
            if next_weight <= capacity:
                graph.add_edge((idx, weight), (idx + 1, next_weight), value=item["value"], action="take", item_id=item["id"])
    path = nx.algorithms.dag.dag_longest_path(graph, weight="value", default_weight=0)
    value = 0
    selected: list[str] = []
    final_weight = path[-1][1] if path else 0
    for left, right in zip(path, path[1:]):
        edge = graph.edges[left, right]
        value += int(edge.get("value", 0))
        if edge.get("action") == "take":
            selected.append(str(edge["item_id"]))
    return {
        "branch": "networkx_capacity_dag_longest_path",
        "status": "MATCH" if value == exact["value"] and final_weight <= capacity else "DRIFT",
        "dependency": receipt,
        "node_count": graph.number_of_nodes(),
        "edge_count": graph.number_of_edges(),
        "path_length": len(path),
        "value": value,
        "weight": final_weight,
        "selected": selected,
        "matches_exact_value": value == exact["value"],
        "feasible": final_weight <= capacity,
        "method": "capacity-layered DAG longest path",
    }


def unavailable_branch(row: dict[str, Any], package_name: str, branch_name: str) -> dict[str, Any]:
    return {
        "branch": branch_name,
        "status": "NOT_EXECUTED_DEPENDENCY_MISSING" if row.get("local_status") == "LOCAL_UNAVAILABLE" else "AVAILABLE_NOT_EXECUTED",
        "matrix_status": row.get("local_status"),
        "next_action": row.get("next_action"),
        "dependency": package_receipt(package_name),
        "non_execution_reason": "Local dependency is unavailable; this pass records a dependency receipt instead of implying coverage.",
    }


def measurement_rows(artifact: dict[str, Any]) -> list[dict[str, Any]]:
    workflow = artifact["workflow"]
    objective = workflow["objective_measurements"]
    branches = workflow["solver_branches"]
    checks = [
        ("source_corpus", artifact["source_binding"]["dominant_cluster_video_count"] == 13, "YouTube source corpus binds dominant quantum-optimization cluster"),
        ("exact_baseline", objective["exact_value"] == 162 and objective["exact_weight"] == 29, "exact baseline value and weight match prior branch receipt"),
        ("scipy_branch", branches["scipy_dual_annealing"]["value"] == 162 and branches["scipy_dual_annealing"]["exact_hit_count"] == 10, "SciPy adapter preserves exact best value and hit count"),
        ("networkx_branch", branches["networkx_capacity_dag_longest_path"]["status"] == "MATCH", "NetworkX DAG branch reproduces exact optimum"),
        ("constraint_status", objective["capacity_violation"] == 0 and objective["all_executed_branches_feasible"], "executed branches satisfy capacity constraints"),
        ("dependency_boundaries", branches["ortools_knapsack"]["status"] == "NOT_EXECUTED_DEPENDENCY_MISSING" and branches["dwave_ocean_sampler"]["status"] == "NOT_EXECUTED_DEPENDENCY_MISSING", "missing OR-Tools and D-Wave branches are explicit dependency receipts"),
        ("buildlang_receipt", artifact["buildlang_binding"]["verify_check_count"] == 18 and artifact["buildlang_binding"]["measurement_count"] == 10, "BuildLang source receipt is attached with verification checks"),
        ("source_anchors", len(artifact["source_anchors"]) == 4, "official source anchors are attached"),
        ("flagships", all(row["status"] == "MATCH" for row in artifact["flagship_receipts"].values()), "Forum, Index, and Telos receipts match"),
        ("promotion_boundary", artifact["unsupported_claim_count"] == 0 and artifact["current_promoted_natural_laws"] == [], "no quantum advantage, discovery, replacement, or natural-law claim is promoted"),
    ]
    rows = []
    for mid, matched, claim in checks:
        rows.append({"measurement_id": f"quantum_workflow.{mid}", "claim": claim, "status": "MATCH" if matched else "DRIFT", "deviation": 0.0 if matched else 1.0, "tolerance": 0.5, "method": "artifact-field-review"})
    return rows


def run_json(command: list[str], timeout: int = 45) -> tuple[int, str, str, dict[str, Any]]:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    parsed = json.loads(result.stdout) if result.returncode == 0 and result.stdout.strip() else {}
    return result.returncode, result.stdout, result.stderr, parsed


def forum_route() -> dict[str, Any]:
    code, stdout, stderr, parsed = run_json(["forum", "route", "--json", "Project Telos pass 0094 QuantumOptimizationWorkflowReceipt with exact, SciPy, NetworkX, BuildLang receipt, and dependency-boundary branches."], timeout=30)
    return {"status": "MATCH" if code == 0 else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "decided": parsed.get("decided"), "confidence": parsed.get("confidence"), "needs_escalation": parsed.get("needs_escalation"), "top_candidates": parsed.get("candidates", [])[:5]}


def index_receipt() -> dict[str, Any]:
    code, stdout, stderr, parsed = run_json(["index", "context-envelope", "--root", ".", "--budget", "1200", "--json"], timeout=45)
    return {"status": "MATCH" if code == 0 and parsed.get("verification_verdict") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "schema": parsed.get("schema"), "verification_verdict": parsed.get("verification_verdict"), "graph_pack_sha256": parsed.get("recheck", {}).get("graph_pack_sha256"), "source_refs_only": parsed.get("privacy", {}).get("source_refs_only")}


def telos_status() -> dict[str, Any]:
    code, stdout, stderr, parsed = run_json(["node", "demo/status.mjs", "--summary"], timeout=30)
    return {"status": "MATCH" if code == 0 and parsed.get("status") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "tool_version": parsed.get("tool_version"), "tool": parsed.get("tool")}


def validate_artifact(artifact: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    workflow = artifact.get("workflow", {})
    branches = workflow.get("solver_branches", {})
    measurements = artifact.get("measurements", [])
    if artifact.get("schema") != SCHEMA:
        errors.append("schema")
    if artifact.get("source_binding", {}).get("source_pass") != "0085" or artifact.get("buildlang_binding", {}).get("source_pass") != "0092":
        errors.append("bindings")
    if workflow.get("objective_measurements", {}).get("exact_value") != 162:
        errors.append("objective")
    if branches.get("networkx_capacity_dag_longest_path", {}).get("status") != "MATCH":
        errors.append("networkx_branch")
    if branches.get("ortools_knapsack", {}).get("status") != "NOT_EXECUTED_DEPENDENCY_MISSING":
        errors.append("ortools_boundary")
    if branches.get("dwave_ocean_sampler", {}).get("status") != "NOT_EXECUTED_DEPENDENCY_MISSING":
        errors.append("dwave_boundary")
    if len(measurements) != 10 or any(row.get("status") != "MATCH" for row in measurements):
        errors.append("measurements")
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
    buildc = read_json(BUILDC)
    bridge = read_json(BRIDGE)
    problem = branch["problem"]
    exact = branch["exact_branch"]["best"]
    nx_branch = networkx_dp_branch(problem, exact)
    scipy = solver["external_adapter"]
    branches = {
        "exact_enumeration": {"status": "MATCH", "value": exact["value"], "weight": exact["weight"], "selected": exact["selected"], "candidate_count": branch["exact_branch"]["candidate_count"], "feasible_count": branch["exact_branch"]["feasible_count"]},
        "scipy_dual_annealing": {"status": "MATCH", "adapter": scipy["adapter"], "value": scipy["best"]["value"], "weight": scipy["best"]["weight"], "selected": scipy["best"]["selected"], "exact_hit_count": scipy["comparison_to_exact"]["exact_hit_count"], "value_distribution": scipy["comparison_to_exact"]["value_distribution"]},
        "networkx_capacity_dag_longest_path": nx_branch,
        "ortools_knapsack": unavailable_branch(row_by_id(matrix, "ortools"), "ortools", "ortools_knapsack"),
        "dwave_ocean_sampler": unavailable_branch(row_by_id(matrix, "dwave_system"), "dwave.system", "dwave_ocean_sampler"),
    }
    executed = [branches["exact_enumeration"], branches["scipy_dual_annealing"], branches["networkx_capacity_dag_longest_path"]]
    artifact: dict[str, Any] = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "generated_on": "2026-07-01",
        "source_binding": {"source_pass": youtube["pass"], "dominant_cluster": youtube["video_corpus_summary"]["dominant_cluster"], "dominant_cluster_video_count": youtube["video_corpus_summary"]["dominant_cluster_video_count"], "bridge_pass": bridge["pass"]},
        "source_anchors": SOURCE_ANCHORS,
        "workflow": {
            "workflow_id": "quantum_optimization_knapsack_12_binary_fixture",
            "problem": problem,
            "solver_branches": branches,
            "objective_measurements": {"exact_value": exact["value"], "exact_weight": exact["weight"], "capacity_violation": exact["capacity_violation"], "all_executed_branches_feasible": all(row.get("weight", 0) <= problem["capacity"] for row in executed), "executed_branch_count": len(executed), "dependency_boundary_branch_count": 2},
        },
        "buildlang_binding": {"source_pass": buildc["pass"], "source_digest": buildc["check_receipt"]["source_digest"]["hex"], "verify_check_count": buildc["verify_summary"]["check_count"], "measurement_count": buildc["crucible_adapter"]["measurement_count"], "adapter_status": buildc["status"]},
        "flagship_receipts": {"forum": forum_route(), "index": index_receipt(), "telos": telos_status()},
        "negative_fixtures": [
            {"fixture_id": "quantum_advantage_claim", "expected_status": "REJECT"},
            {"fixture_id": "missing_dependency_implies_coverage", "expected_status": "REJECT"},
            {"fixture_id": "branch_without_constraint_measurement", "expected_status": "REJECT"},
            {"fixture_id": "buildlang_replacement_claim", "expected_status": "REJECT"},
        ],
        "unsupported_claim_count": 0,
        "current_promoted_natural_laws": [],
        "non_promotion_statement": "Pass 0094 is a toy optimization workflow receipt. It does not prove quantum advantage, production solver coverage, BuildLang replacement, scientific discovery, or a natural law.",
    }
    artifact["measurements"] = measurement_rows(artifact)
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
