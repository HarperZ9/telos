"""Compose pass 0120 Hamiltonian runtime branch receipt."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

SCHEMA = "HamiltonianRuntimeBranchReceipt/v1"
PASS_ID = "0120"
STATUS_MATCH = "HAMILTONIAN_RUNTIME_BRANCH_MATCH"
STATUS_DRIFT = "HAMILTONIAN_RUNTIME_BRANCH_DRIFT"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
BASELINE = ROOT / "schemas" / "hamiltonian-symplectic-receipt-pass-0119.json"
DRIFT_TOLERANCE = 1e-12
DET_TOLERANCE = 1e-12


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


def availability() -> dict[str, dict[str, Any]]:
    return {
        "python": {"status": "AVAILABLE" if shutil.which("python") else "MISSING", "path": shutil.which("python")},
        "buildc": {"status": "AVAILABLE" if shutil.which("buildc") else "MISSING", "path": shutil.which("buildc")},
        "build": {"status": "AVAILABLE" if shutil.which("build") else "MISSING", "path": shutil.which("build")},
        "julia": {"status": "AVAILABLE" if shutil.which("julia") else "MISSING", "path": shutil.which("julia")},
        "numpy": {"status": "AVAILABLE" if importlib.util.find_spec("numpy") else "MISSING"},
        "scipy": {"status": "AVAILABLE" if importlib.util.find_spec("scipy") else "MISSING"},
        "jax": {"status": "AVAILABLE" if importlib.util.find_spec("jax") else "MISSING"},
    }


def matrix_float(matrix: list[list[str]]) -> list[list[float]]:
    return [[float(eval_fraction(value)) for value in row] for row in matrix]


def eval_fraction(value: str) -> float:
    num, _, den = value.partition("/")
    return float(num) / float(den) if den else float(num)


def numpy_branch(case: dict[str, Any]) -> dict[str, Any]:
    import numpy as np

    m = np.array(matrix_float(case["matrix"]), dtype=np.float64)
    s = np.array(matrix_float(case["invariant_matrix"]), dtype=np.float64)
    x = np.array([1.0, 0.0], dtype=np.float64)
    modified = [float(x @ s @ x)]
    standard = [float(0.5 * (x @ x))]
    for _ in range(int(case["steps"])):
        x = m @ x
        modified.append(float(x @ s @ x))
        standard.append(float(0.5 * (x @ x)))
    modified_drift = max(abs(value - modified[0]) for value in modified)
    det = float(np.linalg.det(m))
    return {
        "branch_id": f"numpy_float64_h_{case['h']}",
        "runtime": "numpy",
        "h": case["h"],
        "status": "MATCH" if modified_drift <= DRIFT_TOLERANCE and abs(det - 1.0) <= DET_TOLERANCE else "DRIFT",
        "determinant_float64": det,
        "determinant_abs_drift": abs(det - 1.0),
        "modified_initial_float64": modified[0],
        "modified_final_float64": modified[-1],
        "modified_max_abs_drift": modified_drift,
        "standard_initial_float64": standard[0],
        "standard_final_float64": standard[-1],
        "steps": case["steps"],
        "tolerance": DRIFT_TOLERANCE,
    }


def scipy_branch(case: dict[str, Any]) -> dict[str, Any]:
    import numpy as np
    from scipy import linalg

    m = np.array(matrix_float(case["matrix"]), dtype=np.float64)
    det = float(linalg.det(m))
    return {
        "branch_id": f"scipy_linalg_det_h_{case['h']}",
        "runtime": "scipy.linalg.det",
        "h": case["h"],
        "status": "MATCH" if abs(det - 1.0) <= DET_TOLERANCE else "DRIFT",
        "determinant_float64": det,
        "determinant_abs_drift": abs(det - 1.0),
        "tolerance": DET_TOLERANCE,
    }


def numpy_negative(negative: dict[str, Any]) -> dict[str, Any]:
    import numpy as np

    m = np.array(matrix_float(negative["matrix"]), dtype=np.float64)
    x = np.array([1.0, 0.0], dtype=np.float64)
    e0 = float(0.5 * (x @ x))
    for _ in range(int(negative["steps"])):
        x = m @ x
    e1 = float(0.5 * (x @ x))
    det = float(np.linalg.det(m))
    return {
        "branch_id": "numpy_explicit_euler_negative",
        "runtime": "numpy",
        "status": "MATCH" if det > 1.0 and e1 > e0 else "DRIFT",
        "determinant_float64": det,
        "energy_initial_float64": e0,
        "energy_final_float64": e1,
        "energy_growth": e1 > e0,
    }


def fenced_branches(avail: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for branch_id, key in [("jax_runtime_branch", "jax"), ("buildlang_runtime_branch", "buildc"), ("julia_sciml_branch", "julia")]:
        rows.append({"branch_id": branch_id, "runtime": key, "status": "AVAILABLE_NOT_EXECUTED" if avail[key]["status"] == "AVAILABLE" else "UNAVAILABLE_FENCED"})
    return rows


def source_anchors() -> list[dict[str, str]]:
    return [
        {"tool": "NumPy linalg", "url": "https://numpy.org/doc/stable/reference/generated/numpy.linalg.det.html", "gap_status": "inferred"},
        {"tool": "SciPy linalg.det", "url": "https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.det.html", "gap_status": "inferred"},
        {"tool": "JAX Quickstart", "url": "https://docs.jax.dev/en/latest/quickstart.html", "gap_status": "inferred"},
        {"tool": "Python decimal", "url": "https://docs.python.org/3/library/decimal.html", "gap_status": "inferred"},
    ]


def forum_route() -> dict[str, Any]:
    prompt = "Pass 0120 Hamiltonian runtime branch receipt with NumPy/SciPy execution and JAX/BuildLang fences."
    code, stdout, stderr, parsed = run_json(["forum", "route", "--json", prompt], timeout=30)
    return {"status": "MATCH" if code == 0 else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "decided": parsed.get("decided"), "confidence": parsed.get("confidence"), "needs_escalation": parsed.get("needs_escalation"), "top_candidates": parsed.get("candidates", [])[:5]}


def index_receipt() -> dict[str, Any]:
    code, stdout, stderr, parsed = run_json(["index", "context-envelope", "--root", ".", "--budget", "1200", "--json"], timeout=45)
    return {"status": "MATCH" if code == 0 and parsed.get("verification_verdict") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "schema": parsed.get("schema"), "verification_verdict": parsed.get("verification_verdict")}


def telos_status() -> dict[str, Any]:
    code, stdout, stderr, parsed = run_json(["node", "demo/status.mjs", "--summary"], timeout=30)
    return {"status": "MATCH" if code == 0 and parsed.get("status") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "tool_version": parsed.get("tool_version"), "tool": parsed.get("tool")}


def telos_catalog() -> dict[str, Any]:
    code, stdout, stderr, _parsed = run_json(["node", "demo/catalog.mjs", "--summary"], timeout=30)
    return {"status": "MATCH" if code == 0 and "Project Telos MCP Catalog" in stdout else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "summary_detected": "Project Telos MCP Catalog" in stdout}


def compose() -> dict[str, Any]:
    baseline = read_json(BASELINE)
    avail = availability()
    branches = []
    if avail["numpy"]["status"] == "AVAILABLE":
        branches.extend(numpy_branch(case) for case in baseline["symplectic_cases"])
        branches.append(numpy_negative(baseline["negative_fixtures"][0]))
    if avail["scipy"]["status"] == "AVAILABLE":
        branches.extend(scipy_branch(case) for case in baseline["symplectic_cases"])
    branches.extend(fenced_branches(avail))
    artifact: dict[str, Any] = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "generated_on": "2026-07-01",
        "status": STATUS_DRIFT,
        "source_bindings": {"hamiltonian_symplectic_pass": baseline["pass"], "hamiltonian_symplectic_seal": baseline["seal"]},
        "availability": avail,
        "exact_oracle": {"law_candidate": baseline["law_candidate"], "positive_case_count": len(baseline["symplectic_cases"]), "negative_fixture_count": len(baseline["negative_fixtures"])},
        "runtime_branches": branches,
        "source_surface": {"anchor_count": len(source_anchors()), "anchors": source_anchors()},
        "unsupported_claim_count": 0,
        "current_promoted_natural_laws": [],
        "non_promotion_statement": "Pass 0120 measures runtime replay drift against pass 0119's exact oracle. It does not prove BuildLang, JAX, GPU, or Julia execution when those branches are unavailable.",
        "flagship_receipts": {"forum": forum_route(), "index": index_receipt(), "telos": telos_status(), "telos_catalog": telos_catalog()},
    }
    errors = []
    if not any(row["branch_id"].startswith("numpy_float64") and row["status"] == "MATCH" for row in branches):
        errors.append("numpy_positive_branches")
    if not any(row["branch_id"] == "numpy_explicit_euler_negative" and row["status"] == "MATCH" for row in branches):
        errors.append("numpy_negative_branch")
    if avail["scipy"]["status"] == "AVAILABLE" and not any(row["branch_id"].startswith("scipy_linalg") and row["status"] == "MATCH" for row in branches):
        errors.append("scipy_branch")
    if any(row.get("status") != "MATCH" for row in artifact["flagship_receipts"].values()):
        errors.append("flagships")
    artifact["validation_errors"] = errors
    artifact["status"] = STATUS_MATCH if not errors else STATUS_DRIFT
    artifact["measurements"] = [{"id": row["branch_id"], "status": row["status"]} for row in branches]
    artifact["seal"] = sha256_obj(dict(artifact))
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(ROOT / "schemas" / "hamiltonian-runtime-branch-receipt-pass-0120.json"))
    args = parser.parse_args()
    artifact = compose()
    write_json(Path(args.out), artifact)
    print(json.dumps({"path": args.out, "seal": artifact["seal"], "status": artifact["status"]}, indent=2, sort_keys=True))
    if artifact["status"] != STATUS_MATCH:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
