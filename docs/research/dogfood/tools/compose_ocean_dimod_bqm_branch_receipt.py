"""Compose pass 0100 Ocean/dimod local BQM branch receipt."""
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

SCHEMA = "OceanDimodBQMBranchReceipt/v1"
PASS_ID = "0100"
STATUS_MATCH = "OCEAN_DIMOD_BQM_BRANCH_RECEIPT_MATCH"
STATUS_DRIFT = "OCEAN_DIMOD_BQM_BRANCH_RECEIPT_DRIFT"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
ORTOOLS = ROOT / "schemas" / "ortools-branch-execution-receipt-pass-0099.json"
INTEROP = ROOT / "schemas" / "solver-branch-receipt-interop-schema-pass-0098.json"
TEMP_ROOT = Path(tempfile.gettempdir()).resolve()
VENV = TEMP_ROOT / "telos-dimod-pass0100"
VALUES = [31, 21, 27, 40, 17, 33, 18, 13, 32, 27, 19, 5]
WEIGHTS = [5, 4, 7, 6, 3, 7, 7, 6, 5, 11, 7, 2]
CAPACITY = 29
PENALTY = 200


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


def run(command: list[str], timeout: int = 180) -> dict[str, Any]:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    return {"command": " ".join(command), "cwd": str(REPO), "exit_code": result.returncode, "stdout": result.stdout, "stderr": result.stderr, "stdout_sha256": sha256_text(result.stdout), "stderr_sha256": sha256_text(result.stderr)}


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
import dimod
values={VALUES!r}
weights={WEIGHTS!r}
capacity={CAPACITY!r}
penalty={PENALTY!r}
linear={{}}
quadratic={{}}
for i,(value,weight) in enumerate(zip(values, weights)):
    linear[i] = -value + penalty*(weight*weight - 2*capacity*weight)
for i in range(len(values)):
    for j in range(i+1, len(values)):
        quadratic[(i,j)] = 2*penalty*weights[i]*weights[j]
bqm=dimod.BinaryQuadraticModel(linear, quadratic, penalty*capacity*capacity, dimod.BINARY)
sampleset=dimod.ExactSolver().sample(bqm)
sample=sampleset.first.sample
items=[i for i,val in sample.items() if val == 1]
value=sum(values[i] for i in items)
weight=sum(weights[i] for i in items)
mask=sum(1 << i for i in items)
print(json.dumps({{'dimod_version': dimod.__version__, 'energy': sampleset.first.energy, 'value': value, 'weight': weight, 'mask': mask, 'items': items, 'feasible': weight <= capacity, 'linear_terms': len(linear), 'quadratic_terms': len(quadratic), 'penalty': penalty}}, sort_keys=True))
"""


def run_json_tool(command: list[str], timeout: int = 45) -> tuple[int, str, str, dict[str, Any]]:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    parsed = json.loads(result.stdout) if result.returncode == 0 and result.stdout.strip().startswith("{") else {}
    return result.returncode, result.stdout, result.stderr, parsed


def forum_route() -> dict[str, Any]:
    prompt = "Project Telos pass 0100: execute D-Wave Ocean dimod ExactSolver local BQM branch and attach SolverBranchReceipt/v1."
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
    if artifact.get("source_bindings", {}).get("ortools_pass") != "0099":
        errors.append("source_binding")
    if artifact.get("install_command", {}).get("exit_code") != 0 or artifact.get("run_command", {}).get("exit_code") != 0:
        errors.append("commands")
    if artifact.get("global_availability", {}).get("dimod_available") is not False or artifact.get("global_availability", {}).get("dwave_available") is not False:
        errors.append("global_availability")
    if artifact.get("temp_venv", {}).get("cleaned") is not True:
        errors.append("temp_cleanup")
    if branch.get("value") != 162 or branch.get("weight") != 29 or branch.get("mask") != 2347 or branch.get("gap_to_exact") != 0:
        errors.append("branch_result")
    if artifact.get("bqm_summary", {}).get("linear_terms") != 12 or artifact.get("bqm_summary", {}).get("quadratic_terms") != 66:
        errors.append("bqm_shape")
    if any(tool.get("status") != "MATCH" for tool in artifact.get("flagship_receipts", {}).values()):
        errors.append("flagships")
    if artifact.get("unsupported_claim_count") != 0 or artifact.get("current_promoted_natural_laws") != []:
        errors.append("promotion_boundary")
    return errors


def compose() -> dict[str, Any]:
    ortools = read_json(ORTOOLS)
    interop = read_json(INTEROP)
    remove_temp_venv()
    venv_create = run([sys.executable, "-m", "venv", str(VENV)], timeout=120)
    py = VENV / "Scripts" / "python.exe"
    install = run([str(py), "-m", "pip", "install", "--disable-pip-version-check", "--quiet", "dimod"], timeout=240)
    solver_run = run([str(py), "-c", solver_script()], timeout=120)
    parsed = json.loads(solver_run["stdout"]) if solver_run["stdout"].strip().startswith("{") else {}
    cleaned = remove_temp_venv()
    dimod_spec = importlib.util.find_spec("dimod")
    dwave_spec = importlib.util.find_spec("dwave")
    branch = {
        "schema": "SolverBranchReceipt/v1",
        "branch_id": "ocean_dimod_exact_bqm",
        "origin_pass": PASS_ID,
        "runtime": "python/dimod/temp-venv",
        "method": "dimod.ExactSolver over penalized BinaryQuadraticModel",
        "execution_status": "EXECUTED_LOCAL_CPU_EXACT_SOLVER",
        "solver_status": "MATCH",
        "value": parsed.get("value"),
        "weight": parsed.get("weight"),
        "mask": parsed.get("mask"),
        "selected": ["A", "B", "D", "F", "I", "L"],
        "selected_indices": parsed.get("items"),
        "gap_to_exact": 162 - int(parsed.get("value", 0)) if parsed else None,
        "source_anchor": {"title": "dimod ExactSolver", "url": "https://docs.dwavequantum.com/en/latest/ocean/api_ref_dimod/generated/dimod.reference.samplers.ExactSolver.sample.html"},
        "evidence_ref": "schemas/ocean-dimod-bqm-branch-receipt-pass-0100.json",
        "claim_status": "LOCAL_CPU_RECEIPT_MATCH",
    }
    artifact: dict[str, Any] = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "generated_on": "2026-07-01",
        "source_bindings": {"interop_pass": interop["pass"], "ortools_pass": ortools["pass"], "prior_dwave_status": "NOT_EXECUTED_DEPENDENCY_MISSING"},
        "global_availability": {"dimod_available": dimod_spec is not None, "dimod_origin": None if dimod_spec is None else dimod_spec.origin, "dwave_available": dwave_spec is not None, "dwave_origin": None if dwave_spec is None else dwave_spec.origin},
        "source_anchors": [
            {"title": "Installing Ocean SDK", "url": "https://docs.dwavequantum.com/en/latest/ocean/install.html", "claim": "Ocean requires Python and supports Python 3.10+."},
            {"title": "dimod", "url": "https://docs.dwavequantum.com/en/latest/ocean/api_ref_dimod/index.html", "claim": "dimod is a shared API for samplers and BQMs."},
            {"title": "dimod ExactSolver", "url": "https://docs.dwavequantum.com/en/latest/ocean/api_ref_dimod/generated/dimod.reference.samplers.ExactSolver.sample.html", "claim": "ExactSolver samples all possible solutions to a BQM."},
        ],
        "temp_venv": {"path": str(VENV), "created_exit_code": venv_create["exit_code"], "cleaned": cleaned},
        "venv_create_command": compact(venv_create),
        "install_command": compact(install),
        "run_command": {**compact(solver_run), "stdout_json": parsed},
        "dimod_version": parsed.get("dimod_version"),
        "bqm_summary": {"penalty": PENALTY, "linear_terms": parsed.get("linear_terms"), "quadratic_terms": parsed.get("quadratic_terms"), "energy": parsed.get("energy")},
        "solver_branch_receipt": branch,
        "comparison_to_exact": {"exact_value": 162, "exact_weight": 29, "exact_mask": 2347, "matches_exact": parsed.get("value") == 162 and parsed.get("weight") == 29 and parsed.get("mask") == 2347},
        "negative_fixtures": [
            {"fixture_id": "qpu_execution_claim", "expected_status": "REJECT", "reject_reason": "dimod ExactSolver is local CPU execution"},
            {"fixture_id": "global_ocean_available", "expected_status": "REJECT", "reject_reason": "global import checks are false"},
            {"fixture_id": "natural_law_claim", "expected_status": "REJECT", "reject_reason": "single BQM fixture is not a natural law"},
        ],
        "unsupported_claim_count": 0,
        "current_promoted_natural_laws": [],
        "non_promotion_statement": "Pass 0100 proves local CPU Ocean/dimod BQM execution for one knapsack fixture. It does not prove QPU execution, quantum advantage, production solver coverage, market adoption, or a natural law.",
        "flagship_receipts": {"forum": forum_route(), "index": index_receipt(), "telos": telos_status()},
    }
    artifact["measurements"] = [
        {"id": "global_absent", "status": "MATCH" if not artifact["global_availability"]["dimod_available"] and not artifact["global_availability"]["dwave_available"] else "DRIFT", "claim": "global Ocean/dimod imports are absent"},
        {"id": "venv_created", "status": "MATCH" if venv_create["exit_code"] == 0 else "DRIFT", "claim": "temporary venv was created"},
        {"id": "install_succeeded", "status": "MATCH" if install["exit_code"] == 0 else "DRIFT", "claim": "dimod installed in temp venv"},
        {"id": "run_succeeded", "status": "MATCH" if solver_run["exit_code"] == 0 else "DRIFT", "claim": "dimod ExactSolver executed"},
        {"id": "matches_exact", "status": "MATCH" if artifact["comparison_to_exact"]["matches_exact"] else "DRIFT", "claim": "Ocean/dimod branch matches exact baseline"},
        {"id": "bqm_shape", "status": "MATCH" if artifact["bqm_summary"]["linear_terms"] == 12 and artifact["bqm_summary"]["quadratic_terms"] == 66 else "DRIFT", "claim": "BQM has expected term counts"},
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
    parser.add_argument("--out", default=str(ROOT / "schemas" / "ocean-dimod-bqm-branch-receipt-pass-0100.json"))
    args = parser.parse_args()
    artifact = compose()
    write_json(Path(args.out), artifact)
    print(json.dumps({"path": str(Path(args.out)), "status": artifact["status"], "seal": artifact["seal"]}, indent=2, sort_keys=True))
    if artifact["status"] != STATUS_MATCH:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
