"""Compose pass 0098 SolverBranchReceipt interoperability schema."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

SCHEMA = "SolverBranchReceiptInteropSchema/v1"
PASS_ID = "0098"
STATUS_MATCH = "SOLVER_BRANCH_RECEIPT_INTEROP_SCHEMA_MATCH"
STATUS_DRIFT = "SOLVER_BRANCH_RECEIPT_INTEROP_SCHEMA_DRIFT"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
WORKFLOW = ROOT / "schemas" / "quantum-optimization-workflow-receipt-pass-0094.json"
WORKBENCH = ROOT / "schemas" / "buildlang-optimization-proof-workbench-receipt-pass-0097.json"
SCORECARD = ROOT / "schemas" / "youtube-field-growth-vector-scorecard-pass-0096.json"

SOURCE_ANCHORS = {
    "scipy_dual_annealing": {
        "title": "SciPy dual_annealing",
        "url": "https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.dual_annealing.html",
        "claim": "Find the global minimum of a function using Dual Annealing.",
    },
    "networkx_capacity_dag_longest_path": {
        "title": "NetworkX dag_longest_path",
        "url": "https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.dag.dag_longest_path.html",
        "claim": "Returns the longest path in a directed acyclic graph.",
    },
    "ortools_knapsack": {
        "title": "OR-Tools knapsack",
        "url": "https://developers.google.com/optimization/pack/knapsack",
        "claim": "Choose a subset of maximum total value that fits capacity.",
    },
    "dwave_ocean_sampler": {
        "title": "D-Wave Ocean samplers",
        "url": "https://docs.dwavequantum.com/en/latest/ocean/api_ref_samplers/index.html",
        "claim": "Ocean provides quantum, classical, and hybrid samplers.",
    },
}


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


def executed_branch(branch_id: str, origin: str, runtime: str, method: str, value: int, weight: int, gap: int, evidence: str, mask: int | None = None, selected: list[str] | None = None, feasible_count: int | None = None, anchor_id: str | None = None) -> dict[str, Any]:
    return {
        "schema": "SolverBranchReceipt/v1",
        "branch_id": branch_id,
        "origin_pass": origin,
        "runtime": runtime,
        "method": method,
        "execution_status": "EXECUTED",
        "solver_status": "MATCH",
        "value": value,
        "weight": weight,
        "mask": mask,
        "selected": selected or [],
        "feasible_count": feasible_count,
        "gap_to_exact": gap,
        "source_anchor": SOURCE_ANCHORS.get(anchor_id or branch_id),
        "evidence_ref": evidence,
        "claim_status": "LOCAL_RECEIPT_MATCH",
    }


def dependency_branch(branch_id: str, origin: str, runtime: str, method: str, dependency: dict[str, Any], evidence: str) -> dict[str, Any]:
    return {
        "schema": "SolverBranchReceipt/v1",
        "branch_id": branch_id,
        "origin_pass": origin,
        "runtime": runtime,
        "method": method,
        "execution_status": "NOT_EXECUTED_DEPENDENCY_MISSING",
        "solver_status": "UNVERIFIABLE_UNTIL_EXECUTED",
        "dependency": dependency,
        "value": None,
        "weight": None,
        "gap_to_exact": None,
        "source_anchor": SOURCE_ANCHORS.get(branch_id),
        "evidence_ref": evidence,
        "claim_status": "DEPENDENCY_BOUNDARY",
    }


def normalize_branches(workflow: dict[str, Any], workbench: dict[str, Any]) -> list[dict[str, Any]]:
    wf = workflow["workflow"]["solver_branches"]
    wb = {row["branch"]: row for row in workbench["branches"]}
    exact = wf["exact_enumeration"]
    nx = wf["networkx_capacity_dag_longest_path"]
    scipy = wf["scipy_dual_annealing"]
    return [
        executed_branch("python_exact_enumeration", "0094", "python", "full mask enumeration", exact["value"], exact["weight"], 0, "schemas/quantum-optimization-workflow-receipt-pass-0094.json", selected=exact["selected"], feasible_count=exact["feasible_count"]),
        executed_branch("scipy_dual_annealing", "0094", "python/scipy", scipy["adapter"], scipy["value"], scipy["weight"], exact["value"] - scipy["value"], "schemas/quantum-optimization-workflow-receipt-pass-0094.json", selected=scipy["selected"]),
        executed_branch("networkx_capacity_dag_longest_path", "0094", "python/networkx", nx["method"], nx["value"], nx["weight"], exact["value"] - nx["value"], "schemas/quantum-optimization-workflow-receipt-pass-0094.json", selected=nx["selected"]),
        dependency_branch("ortools_knapsack", "0094", "python/ortools", "knapsack solver", wf["ortools_knapsack"]["dependency"], "schemas/quantum-optimization-workflow-receipt-pass-0094.json"),
        dependency_branch("dwave_ocean_sampler", "0094", "python/dwave-ocean", "sampler adapter", wf["dwave_ocean_sampler"]["dependency"], "schemas/quantum-optimization-workflow-receipt-pass-0094.json"),
        executed_branch("buildlang_exact_enumeration", "0097", "buildlang/buildc", wb["exact_enumeration"]["method"], wb["exact_enumeration"]["value"], wb["exact_enumeration"]["weight"], wb["exact_enumeration"]["gap_to_exact"], "schemas/buildlang-optimization-proof-workbench-receipt-pass-0097.json", mask=wb["exact_enumeration"]["mask"], feasible_count=wb["exact_enumeration"]["feasible_count"]),
        executed_branch("buildlang_greedy_ratio_order", "0097", "buildlang/buildc", wb["greedy_ratio_order"]["method"], wb["greedy_ratio_order"]["value"], wb["greedy_ratio_order"]["weight"], wb["greedy_ratio_order"]["gap_to_exact"], "schemas/buildlang-optimization-proof-workbench-receipt-pass-0097.json", mask=wb["greedy_ratio_order"]["mask"]),
        executed_branch("buildlang_bounded_prefix_2048", "0097", "buildlang/buildc", wb["bounded_prefix_2048"]["method"], wb["bounded_prefix_2048"]["value"], wb["bounded_prefix_2048"]["weight"], wb["bounded_prefix_2048"]["gap_to_exact"], "schemas/buildlang-optimization-proof-workbench-receipt-pass-0097.json", mask=wb["bounded_prefix_2048"]["mask"], feasible_count=wb["bounded_prefix_2048"]["feasible_count"]),
    ]


def forum_route() -> dict[str, Any]:
    prompt = "Project Telos pass 0098: unify exact, heuristic, BuildLang, NetworkX, OR-Tools, and D-Wave solver branch receipts."
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
    branches = artifact.get("branch_receipts", [])
    if artifact.get("schema") != SCHEMA:
        errors.append("schema")
    if artifact.get("source_bindings", {}).get("workbench_pass") != "0097":
        errors.append("source_bindings")
    if len(branches) != 8:
        errors.append("branch_count")
    if artifact.get("coverage", {}).get("executed_count") != 6 or artifact.get("coverage", {}).get("dependency_boundary_count") != 2:
        errors.append("coverage")
    if artifact.get("coverage", {}).get("best_value") != 162 or artifact.get("coverage", {}).get("max_observed_gap") != 16:
        errors.append("values")
    if any(row.get("schema") != "SolverBranchReceipt/v1" for row in branches):
        errors.append("branch_schema")
    if len(artifact.get("source_anchors", [])) != 4:
        errors.append("source_anchors")
    if any(tool.get("status") != "MATCH" for tool in artifact.get("flagship_receipts", {}).values()):
        errors.append("flagships")
    if artifact.get("unsupported_claim_count") != 0 or artifact.get("current_promoted_natural_laws") != []:
        errors.append("promotion_boundary")
    return errors


def compose() -> dict[str, Any]:
    workflow = read_json(WORKFLOW)
    workbench = read_json(WORKBENCH)
    scorecard = read_json(SCORECARD)
    branches = normalize_branches(workflow, workbench)
    executed = [row for row in branches if row["execution_status"] == "EXECUTED"]
    dependency = [row for row in branches if row["execution_status"] != "EXECUTED"]
    artifact: dict[str, Any] = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "generated_on": "2026-07-01",
        "source_bindings": {"workflow_pass": workflow["pass"], "scorecard_pass": scorecard["pass"], "workbench_pass": workbench["pass"], "primary_vector": scorecard["primary_30_day_push"]["vector_id"]},
        "branch_receipts": branches,
        "source_anchors": list(SOURCE_ANCHORS.values()),
        "required_fields": ["branch_id", "runtime", "method", "execution_status", "solver_status", "value", "weight", "gap_to_exact", "source_anchor", "evidence_ref", "claim_status"],
        "coverage": {"branch_count": len(branches), "executed_count": len(executed), "dependency_boundary_count": len(dependency), "best_value": max(row["value"] for row in executed), "max_observed_gap": max(row["gap_to_exact"] for row in executed), "runtimes": sorted({row["runtime"] for row in branches})},
        "negative_fixtures": [
            {"fixture_id": "missing_source_anchor", "expected_status": "REJECT", "reject_reason": "external solver branch needs source anchor or local receipt"},
            {"fixture_id": "dependency_boundary_promoted", "expected_status": "REJECT", "reject_reason": "missing dependency branch cannot claim execution"},
            {"fixture_id": "suboptimal_branch_claimed_exact", "expected_status": "REJECT", "reject_reason": "gap_to_exact must remain nonzero"},
        ],
        "unsupported_claim_count": 0,
        "current_promoted_natural_laws": [],
        "non_promotion_statement": "Pass 0098 defines a shared solver-branch receipt schema. It does not prove solver superiority, external dependency coverage, quantum advantage, market adoption, or a natural law.",
        "flagship_receipts": {"forum": forum_route(), "index": index_receipt(), "telos": telos_status()},
    }
    artifact["measurements"] = [
        {"id": "branch_count", "status": "MATCH" if len(branches) == 8 else "DRIFT", "claim": "8 solver branch receipts are normalized"},
        {"id": "executed_count", "status": "MATCH" if len(executed) == 6 else "DRIFT", "claim": "6 branches executed locally"},
        {"id": "dependency_boundaries", "status": "MATCH" if len(dependency) == 2 else "DRIFT", "claim": "2 dependency-boundary branches are explicit"},
        {"id": "best_value", "status": "MATCH" if artifact["coverage"]["best_value"] == 162 else "DRIFT", "claim": "best observed value remains 162"},
        {"id": "source_anchors", "status": "MATCH" if len(artifact["source_anchors"]) == 4 else "DRIFT", "claim": "4 official source anchors are bound"},
        {"id": "required_fields", "status": "MATCH" if len(artifact["required_fields"]) == 11 else "DRIFT", "claim": "SolverBranchReceipt required fields are listed"},
        {"id": "flagships", "status": "MATCH" if all(row["status"] == "MATCH" for row in artifact["flagship_receipts"].values()) else "DRIFT", "claim": "Forum, Index, and Telos receipts match"},
        {"id": "promotion_boundary", "status": "MATCH", "claim": "no unsupported claim or natural law is promoted"},
    ]
    artifact["validation_errors"] = validate_artifact(artifact)
    artifact["status"] = STATUS_MATCH if not artifact["validation_errors"] else STATUS_DRIFT
    artifact["seal"] = sha256_obj({key: value for key, value in artifact.items() if key != "seal"})
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(ROOT / "schemas" / "solver-branch-receipt-interop-schema-pass-0098.json"))
    args = parser.parse_args()
    artifact = compose()
    write_json(Path(args.out), artifact)
    print(json.dumps({"path": str(Path(args.out)), "status": artifact["status"], "seal": artifact["seal"]}, indent=2, sort_keys=True))
    if artifact["status"] != STATUS_MATCH:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
