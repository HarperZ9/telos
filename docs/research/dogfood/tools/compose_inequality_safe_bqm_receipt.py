"""Compose pass 0101 inequality-safe BQM counterexample receipt."""
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

SCHEMA = "InequalitySafeBQMReceipt/v1"
PASS_ID = "0101"
STATUS_MATCH = "INEQUALITY_SAFE_BQM_RECEIPT_MATCH"
STATUS_DRIFT = "INEQUALITY_SAFE_BQM_RECEIPT_DRIFT"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
OCEAN = ROOT / "schemas" / "ocean-dimod-bqm-branch-receipt-pass-0100.json"
TEMP_ROOT = Path(tempfile.gettempdir()).resolve()
VENV = TEMP_ROOT / "telos-inequality-bqm-pass0101"


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
    return r"""
import json
import dimod
values=[10,9]
weights=[3,2]
capacity=4
penalty=100

def result_from_sample(sample):
    items=[i for i in range(len(values)) if sample.get(f'x{i}', 0) == 1]
    value=sum(values[i] for i in items)
    weight=sum(weights[i] for i in items)
    return {'items': items, 'value': value, 'weight': weight, 'feasible': weight <= capacity}

def equality_bqm():
    linear={}
    quadratic={}
    for i,(value,weight) in enumerate(zip(values, weights)):
        linear[f'x{i}'] = -value + penalty*(weight*weight - 2*capacity*weight)
    for i in range(len(values)):
        for j in range(i+1, len(values)):
            quadratic[(f'x{i}', f'x{j}')] = 2*penalty*weights[i]*weights[j]
    return dimod.BinaryQuadraticModel(linear, quadratic, penalty*capacity*capacity, dimod.BINARY)

def slack_bqm():
    terms={'x0': weights[0], 'x1': weights[1], 's0': 1, 's1': 2, 's2': 4}
    linear={name: penalty*(coeff*coeff - 2*capacity*coeff) for name, coeff in terms.items()}
    linear['x0'] -= values[0]
    linear['x1'] -= values[1]
    names=list(terms)
    quadratic={}
    for idx,a in enumerate(names):
        for b in names[idx+1:]:
            quadratic[(a,b)] = 2*penalty*terms[a]*terms[b]
    return dimod.BinaryQuadraticModel(linear, quadratic, penalty*capacity*capacity, dimod.BINARY)

def solve(bqm):
    sampleset=dimod.ExactSolver().sample(bqm)
    sample=sampleset.first.sample
    result=result_from_sample(sample)
    result.update({'energy': float(sampleset.first.energy), 'sample': {k: int(v) for k, v in sample.items()}})
    return result

def true_optimum():
    best=None
    for mask in range(1 << len(values)):
        items=[i for i in range(len(values)) if (mask >> i) & 1]
        value=sum(values[i] for i in items)
        weight=sum(weights[i] for i in items)
        feasible=weight <= capacity
        if feasible and (best is None or value > best['value']):
            best={'items': items, 'value': value, 'weight': weight, 'mask': mask}
    return best

print(json.dumps({'dimod_version': dimod.__version__, 'problem': {'values': values, 'weights': weights, 'capacity': capacity, 'penalty': penalty}, 'true_optimum': true_optimum(), 'equality_penalty': solve(equality_bqm()), 'slack_penalty': solve(slack_bqm())}, sort_keys=True))
"""


def run_json_tool(command: list[str], timeout: int = 45) -> tuple[int, str, str, dict[str, Any]]:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    parsed = json.loads(result.stdout) if result.returncode == 0 and result.stdout.strip().startswith("{") else {}
    return result.returncode, result.stdout, result.stderr, parsed


def forum_route() -> dict[str, Any]:
    prompt = "Project Telos pass 0101: prove equality-capacity BQM penalty counterexample and slack-variable inequality-safe fix."
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
    eq = artifact.get("results", {}).get("equality_penalty", {})
    slack = artifact.get("results", {}).get("slack_penalty", {})
    optimum = artifact.get("results", {}).get("true_optimum", {})
    if artifact.get("schema") != SCHEMA:
        errors.append("schema")
    if artifact.get("source_bindings", {}).get("ocean_pass") != "0100":
        errors.append("source_binding")
    if artifact.get("install_command", {}).get("exit_code") != 0 or artifact.get("run_command", {}).get("exit_code") != 0:
        errors.append("commands")
    if artifact.get("temp_venv", {}).get("cleaned") is not True:
        errors.append("temp_cleanup")
    if optimum.get("value") != 10 or optimum.get("weight") != 3:
        errors.append("true_optimum")
    if eq.get("feasible") is not False or eq.get("value") != 19:
        errors.append("equality_counterexample")
    if slack.get("feasible") is not True or slack.get("value") != 10 or slack.get("weight") != 3:
        errors.append("slack_fix")
    if any(tool.get("status") != "MATCH" for tool in artifact.get("flagship_receipts", {}).values()):
        errors.append("flagships")
    if artifact.get("current_promoted_natural_laws") != []:
        errors.append("promotion_boundary")
    return errors


def compose() -> dict[str, Any]:
    ocean = read_json(OCEAN)
    remove_temp_venv()
    venv_create = run([sys.executable, "-m", "venv", str(VENV)], timeout=120)
    py = VENV / "Scripts" / "python.exe"
    install = run([str(py), "-m", "pip", "install", "--disable-pip-version-check", "--quiet", "dimod"], timeout=240)
    solver_run = run([str(py), "-c", solver_script()], timeout=120)
    parsed = json.loads(solver_run["stdout"]) if solver_run["stdout"].strip().startswith("{") else {}
    cleaned = remove_temp_venv()
    dimod_spec = importlib.util.find_spec("dimod")
    artifact: dict[str, Any] = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "generated_on": "2026-07-01",
        "source_bindings": {"ocean_pass": ocean["pass"], "prior_bqm_status": ocean["status"]},
        "global_availability": {"dimod_available": dimod_spec is not None, "dimod_origin": None if dimod_spec is None else dimod_spec.origin},
        "temp_venv": {"path": str(VENV), "created_exit_code": venv_create["exit_code"], "cleaned": cleaned},
        "venv_create_command": compact(venv_create),
        "install_command": compact(install),
        "run_command": {**compact(solver_run), "stdout_json": parsed},
        "results": parsed,
        "law_candidate": {
            "name": "knapsack_inequality_bqm_requires_slack_or_inequality_encoding",
            "status": "LAW_CANDIDATE",
            "claim": "A squared equality-to-capacity penalty is not a valid general encoding of <= capacity knapsack; slack or another inequality encoding is required.",
            "counterexample": "values=[10,9], weights=[3,2], capacity=4",
        },
        "negative_fixtures": [
            {"fixture_id": "equality_penalty_claimed_general", "expected_status": "REJECT", "reject_reason": "counterexample selects infeasible overweight set"},
            {"fixture_id": "law_promoted", "expected_status": "REJECT", "reject_reason": "single counterexample plus fix is law-candidate only"},
            {"fixture_id": "qpu_claim", "expected_status": "REJECT", "reject_reason": "dimod ExactSolver is local CPU execution"},
        ],
        "unsupported_claim_count": 0,
        "current_promoted_natural_laws": [],
        "non_promotion_statement": "Pass 0101 proves a bounded counterexample and slack-variable fix for one BQM encoding. It promotes a law candidate, not a natural law.",
        "flagship_receipts": {"forum": forum_route(), "index": index_receipt(), "telos": telos_status()},
    }
    artifact["measurements"] = [
        {"id": "global_absent", "status": "MATCH" if not artifact["global_availability"]["dimod_available"] else "DRIFT", "claim": "global dimod import is absent"},
        {"id": "install_succeeded", "status": "MATCH" if install["exit_code"] == 0 else "DRIFT", "claim": "dimod installed in temp venv"},
        {"id": "true_optimum", "status": "MATCH" if parsed.get("true_optimum", {}).get("value") == 10 else "DRIFT", "claim": "true feasible optimum is value 10"},
        {"id": "equality_counterexample", "status": "MATCH" if parsed.get("equality_penalty", {}).get("feasible") is False else "DRIFT", "claim": "equality penalty selects infeasible set"},
        {"id": "slack_fix", "status": "MATCH" if parsed.get("slack_penalty", {}).get("value") == 10 and parsed.get("slack_penalty", {}).get("feasible") is True else "DRIFT", "claim": "slack BQM recovers feasible optimum"},
        {"id": "temp_cleaned", "status": "MATCH" if cleaned else "DRIFT", "claim": "temporary venv cleaned"},
        {"id": "flagships", "status": "MATCH" if all(row["status"] == "MATCH" for row in artifact["flagship_receipts"].values()) else "DRIFT", "claim": "Forum, Index, and Telos receipts match"},
        {"id": "promotion_boundary", "status": "MATCH", "claim": "law remains candidate only"},
    ]
    artifact["validation_errors"] = validate_artifact(artifact)
    artifact["status"] = STATUS_MATCH if not artifact["validation_errors"] else STATUS_DRIFT
    artifact["seal"] = sha256_obj({key: value for key, value in artifact.items() if key != "seal"})
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(ROOT / "schemas" / "inequality-safe-bqm-receipt-pass-0101.json"))
    args = parser.parse_args()
    artifact = compose()
    write_json(Path(args.out), artifact)
    print(json.dumps({"path": str(Path(args.out)), "status": artifact["status"], "seal": artifact["seal"]}, indent=2, sort_keys=True))
    if artifact["status"] != STATUS_MATCH:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
