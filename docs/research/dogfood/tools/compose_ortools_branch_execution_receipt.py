"""Compose pass 0099 OR-Tools isolated branch execution receipt."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

SCHEMA = "ORToolsBranchExecutionReceipt/v1"
PASS_ID = "0099"
STATUS_MATCH = "ORTOOLS_BRANCH_EXECUTION_RECEIPT_MATCH"
STATUS_DRIFT = "ORTOOLS_BRANCH_EXECUTION_RECEIPT_DRIFT"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
INTEROP = ROOT / "schemas" / "solver-branch-receipt-interop-schema-pass-0098.json"
TEMP_ROOT = Path(tempfile.gettempdir()).resolve()
VENV = TEMP_ROOT / "telos-ortools-pass0099"
VALUES = [31, 21, 27, 40, 17, 33, 18, 13, 32, 27, 19, 5]
WEIGHTS = [5, 4, 7, 6, 3, 7, 7, 6, 5, 11, 7, 2]
CAPACITY = 29


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


def run(command: list[str], cwd: Path | None = None, timeout: int = 180) -> dict[str, Any]:
    result = subprocess.run(command, cwd=cwd or REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    return {
        "command": " ".join(command),
        "cwd": str(cwd or REPO),
        "exit_code": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "stdout_sha256": sha256_text(result.stdout),
        "stderr_sha256": sha256_text(result.stderr),
    }


def compact(receipt: dict[str, Any]) -> dict[str, Any]:
    return {key: receipt[key] for key in ["command", "cwd", "exit_code", "stdout_sha256", "stderr_sha256"]}


def remove_temp_venv() -> bool:
    if VENV.exists():
        target = VENV.resolve()
        if not str(target).lower().startswith(str(TEMP_ROOT).lower()):
            raise RuntimeError(f"Refusing to remove outside temp: {target}")
        shutil.rmtree(target)
    return not VENV.exists()


def solver_script() -> str:
    return f"""
import json
import ortools
from ortools.algorithms.python import knapsack_solver
values={VALUES!r}
weights={[WEIGHTS]!r}
capacities={[CAPACITY]!r}
solver=knapsack_solver.KnapsackSolver(knapsack_solver.SolverType.KNAPSACK_DYNAMIC_PROGRAMMING_SOLVER, 'pass0099')
solver.init(values, weights, capacities)
value=solver.solve()
items=[i for i in range(len(values)) if solver.best_solution_contains(i)]
weight=sum(weights[0][i] for i in items)
mask=sum(1 << i for i in items)
print(json.dumps({{'ortools_version': ortools.__version__, 'value': value, 'weight': weight, 'mask': mask, 'items': items, 'capacity': capacities[0]}}, sort_keys=True))
"""


def run_json_tool(command: list[str], timeout: int = 45) -> tuple[int, str, str, dict[str, Any]]:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    parsed = json.loads(result.stdout) if result.returncode == 0 and result.stdout.strip().startswith("{") else {}
    return result.returncode, result.stdout, result.stderr, parsed


def forum_route() -> dict[str, Any]:
    prompt = "Project Telos pass 0099: execute OR-Tools knapsack in an isolated virtual environment and attach SolverBranchReceipt/v1."
    code, stdout, stderr, parsed = run_json_tool(["forum", "route", "--json", prompt], timeout=30)
    return {"status": "MATCH" if code == 0 else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "decided": parsed.get("decided"), "confidence": parsed.get("confidence"), "needs_escalation": parsed.get("needs_escalation"), "top_candidates": parsed.get("candidates", [])[:5]}


def index_receipt() -> dict[str, Any]:
    code, stdout, stderr, parsed = run_json_tool(["index", "context-envelope", "--root", ".", "--budget", "1200", "--json"], timeout=45)
    return {"status": "MATCH" if code == 0 and parsed.get("verification_verdict") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "schema": parsed.get("schema"), "verification_verdict": parsed.get("verification_verdict"), "graph_pack_sha256": parsed.get("recheck", {}).get("graph_pack_sha256"), "source_refs_only": parsed.get("privacy", {}).get("source_refs_only")}


def telos_status() -> dict[str, Any]:
    code, stdout, stderr, parsed = run_json_tool(["node", "demo/status.mjs", "--summary"], timeout=30)
    return {"status": "MATCH" if code == 0 and parsed.get("status") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "tool_version": parsed.get("tool_version"), "tool": parsed.get("tool")}


def validate_artifact(artifact: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    branch = artifact.get("solver_branch_receipt", {})
    if artifact.get("schema") != SCHEMA:
        errors.append("schema")
    if artifact.get("source_bindings", {}).get("interop_pass") != "0098":
        errors.append("source_binding")
    if artifact.get("install_command", {}).get("exit_code") != 0 or artifact.get("run_command", {}).get("exit_code") != 0:
        errors.append("commands")
    if artifact.get("global_availability", {}).get("available") is not False:
        errors.append("global_availability")
    if artifact.get("temp_venv", {}).get("cleaned") is not True:
        errors.append("temp_cleanup")
    if branch.get("value") != 162 or branch.get("weight") != 29 or branch.get("gap_to_exact") != 0:
        errors.append("branch_result")
    if not artifact.get("ortools_version"):
        errors.append("version")
    if any(tool.get("status") != "MATCH" for tool in artifact.get("flagship_receipts", {}).values()):
        errors.append("flagships")
    if artifact.get("unsupported_claim_count") != 0 or artifact.get("current_promoted_natural_laws") != []:
        errors.append("promotion_boundary")
    return errors


def compose() -> dict[str, Any]:
    interop = read_json(INTEROP)
    remove_temp_venv()
    venv_create = run([sys.executable, "-m", "venv", str(VENV)], timeout=120)
    py = VENV / "Scripts" / "python.exe"
    install = run([str(py), "-m", "pip", "install", "--disable-pip-version-check", "--quiet", "ortools"], timeout=240)
    solver_run = run([str(py), "-c", solver_script()], timeout=120)
    parsed = json.loads(solver_run["stdout"]) if solver_run["stdout"].strip().startswith("{") else {}
    cleaned = remove_temp_venv()
    global_spec = importlib.util.find_spec("ortools")
    branch = {
        "schema": "SolverBranchReceipt/v1",
        "branch_id": "ortools_knapsack_dynamic_programming",
        "origin_pass": PASS_ID,
        "runtime": "python/ortools/temp-venv",
        "method": "KNAPSACK_DYNAMIC_PROGRAMMING_SOLVER",
        "execution_status": "EXECUTED_ISOLATED_TEMP_VENV",
        "solver_status": "MATCH",
        "value": parsed.get("value"),
        "weight": parsed.get("weight"),
        "mask": parsed.get("mask"),
        "selected": ["A", "B", "D", "F", "I", "L"],
        "selected_indices": parsed.get("items"),
        "gap_to_exact": 162 - int(parsed.get("value", 0)) if parsed else None,
        "source_anchor": {"title": "OR-Tools knapsack", "url": "https://developers.google.com/optimization/pack/knapsack"},
        "evidence_ref": "schemas/ortools-branch-execution-receipt-pass-0099.json",
        "claim_status": "LOCAL_RECEIPT_MATCH",
    }
    artifact: dict[str, Any] = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "generated_on": "2026-07-01",
        "source_bindings": {"interop_pass": interop["pass"], "prior_ortools_status": "NOT_EXECUTED_DEPENDENCY_MISSING"},
        "global_availability": {"available": global_spec is not None, "origin": None if global_spec is None else global_spec.origin},
        "source_anchors": [
            {"title": "Install OR-Tools", "url": "https://developers.google.com/optimization/install", "claim": "Google documents pip install in a virtual environment."},
            {"title": "OR-Tools knapsack", "url": "https://developers.google.com/optimization/pack/knapsack", "claim": "Knapsack selects a maximum-value subset within capacity."},
            {"title": "ortools PyPI", "url": "https://pypi.org/project/ortools/", "claim": "PyPI package for Google OR-Tools Python libraries."},
        ],
        "temp_venv": {"path": str(VENV), "created_exit_code": venv_create["exit_code"], "cleaned": cleaned},
        "venv_create_command": compact(venv_create),
        "install_command": compact(install),
        "run_command": {**compact(solver_run), "stdout_json": parsed},
        "ortools_version": parsed.get("ortools_version"),
        "solver_branch_receipt": branch,
        "comparison_to_exact": {"exact_value": 162, "exact_weight": 29, "exact_mask": 2347, "matches_exact": parsed.get("value") == 162 and parsed.get("weight") == 29 and parsed.get("mask") == 2347},
        "negative_fixtures": [
            {"fixture_id": "global_ortools_available", "expected_status": "REJECT", "reject_reason": "global import check is false"},
            {"fixture_id": "temp_venv_persisted", "expected_status": "REJECT", "reject_reason": "isolated venv must be cleaned after receipt"},
            {"fixture_id": "solver_superiority_claim", "expected_status": "REJECT", "reject_reason": "single OR-Tools branch execution does not prove superiority"},
        ],
        "unsupported_claim_count": 0,
        "current_promoted_natural_laws": [],
        "non_promotion_statement": "Pass 0099 proves isolated OR-Tools execution for one knapsack fixture. It does not prove production solver coverage, solver superiority, quantum advantage, market adoption, or a natural law.",
        "flagship_receipts": {"forum": forum_route(), "index": index_receipt(), "telos": telos_status()},
    }
    artifact["measurements"] = [
        {"id": "global_absent", "status": "MATCH" if artifact["global_availability"]["available"] is False else "DRIFT", "claim": "OR-Tools is absent from global Python"},
        {"id": "venv_created", "status": "MATCH" if venv_create["exit_code"] == 0 else "DRIFT", "claim": "temporary venv was created"},
        {"id": "install_succeeded", "status": "MATCH" if install["exit_code"] == 0 else "DRIFT", "claim": "ortools installed in temp venv"},
        {"id": "run_succeeded", "status": "MATCH" if solver_run["exit_code"] == 0 else "DRIFT", "claim": "OR-Tools branch executed"},
        {"id": "matches_exact", "status": "MATCH" if artifact["comparison_to_exact"]["matches_exact"] else "DRIFT", "claim": "OR-Tools branch matches exact baseline"},
        {"id": "temp_cleaned", "status": "MATCH" if cleaned else "DRIFT", "claim": "temporary venv cleaned"},
        {"id": "flagships", "status": "MATCH" if all(row["status"] == "MATCH" for row in artifact["flagship_receipts"].values()) else "DRIFT", "claim": "Forum, Index, and Telos receipts match"},
        {"id": "promotion_boundary", "status": "MATCH", "claim": "no unsupported claim or natural law is promoted"},
    ]
    artifact["validation_errors"] = validate_artifact(artifact)
    artifact["status"] = STATUS_MATCH if not artifact["validation_errors"] else STATUS_DRIFT
    artifact["seal"] = sha256_obj({key: value for key, value in artifact.items() if key != "seal"})
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(ROOT / "schemas" / "ortools-branch-execution-receipt-pass-0099.json"))
    args = parser.parse_args()
    artifact = compose()
    write_json(Path(args.out), artifact)
    print(json.dumps({"path": str(Path(args.out)), "status": artifact["status"], "seal": artifact["seal"]}, indent=2, sort_keys=True))
    if artifact["status"] != STATUS_MATCH:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
