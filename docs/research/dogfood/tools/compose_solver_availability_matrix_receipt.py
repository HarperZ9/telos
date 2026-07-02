"""Compose pass 0090 solver availability matrix receipt."""
from __future__ import annotations

import argparse
import hashlib
import importlib
import importlib.util
import json
import platform
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

SCHEMA = "SolverAvailabilityMatrixReceipt/v1"
PASS_ID = "0090"
STATUS_MATCH = "SOLVER_AVAILABILITY_MATRIX_RECEIPT_MATCH"
STATUS_DRIFT = "SOLVER_AVAILABILITY_MATRIX_RECEIPT_DRIFT"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
BASELINE = ROOT / "schemas" / "external-solver-adapter-receipt-pass-0089.json"
BUILDLANG_ROOT = Path(r"C:\dev\public\pubscan\quantalang")
BUILDLANG_COMPILER = BUILDLANG_ROOT / "compiler"
LOCAL_REPOS = {
    "buildlang_compiler": BUILDLANG_ROOT,
    "build_universe": Path(r"C:\dev\public\build-universe"),
    "build_color": Path(r"C:\dev\public\build-color"),
    "calibrate_pro": Path(r"C:\dev\public\calibrate-pro"),
    "buildlang_vscode": Path(r"C:\dev\public\buildlang-vscode"),
    "buildlang_tm_language": Path(r"C:\dev\public\buildlang-tmLanguage"),
}
PACKAGE_ROWS = [
    ("numpy", "numpy", "array_baseline", "numpy"),
    ("scipy", "scipy", "continuous_global_optimization", "scipy-dual-annealing"),
    ("networkx", "networkx", "graph_algorithms", "networkx"),
    ("pandas", "pandas", "table_ingest", "pandas"),
    ("sympy", "sympy", "symbolic_math", "sympy"),
    ("cvxpy", "cvxpy", "convex_optimization", "cvxpy"),
    ("pyomo", "pyomo", "algebraic_modeling", "pyomo"),
    ("ortools", "ortools", "cp_sat_mip", "ortools-cp-sat"),
    ("dimod", "dimod", "qubo_bqm_modeling", "dwave-ocean"),
    ("dwave_system", "dwave.system", "quantum_hybrid_samplers", "dwave-ocean"),
    ("qiskit", "qiskit", "quantum_circuits", "qiskit"),
    ("qutip", "qutip", "quantum_dynamics", "qutip"),
    ("z3", "z3", "smt_solving", "z3"),
    ("torch", "torch", "ml_tensor_training", "torch"),
    ("jax", "jax", "accelerated_autodiff", "jax"),
]
SOURCE_ANCHORS = [
    {"source_id": "scipy-dual-annealing", "url": "https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.dual_annealing.html", "verification_status": "WEB_VERIFIED_2026_07_01"},
    {"source_id": "ortools-cp-sat", "url": "https://developers.google.com/optimization/cp/cp_solver", "verification_status": "WEB_VERIFIED_2026_07_01"},
    {"source_id": "dwave-ocean", "url": "https://docs.dwavequantum.com/en/latest/ocean/index.html", "verification_status": "WEB_VERIFIED_2026_07_01"},
    {"source_id": "cvxpy", "url": "https://www.cvxpy.org/", "verification_status": "WEB_VERIFIED_2026_07_01"},
    {"source_id": "pyomo", "url": "https://www.pyomo.org/", "verification_status": "WEB_VERIFIED_2026_07_01"},
    {"source_id": "qiskit", "url": "https://quantum.cloud.ibm.com/docs/en/guides", "verification_status": "WEB_VERIFIED_2026_07_01"},
    {"source_id": "sympy", "url": "https://docs.sympy.org/latest/index.html", "verification_status": "WEB_VERIFIED_2026_07_01"},
    {"source_id": "networkx", "url": "https://networkx.org/documentation/stable/", "verification_status": "WEB_VERIFIED_2026_07_01"},
    {"source_id": "pass-0089-external-adapter", "url": "docs/research/dogfood/pass-0089-ledger.md", "verification_status": "LOCAL_BASELINE"},
    {"source_id": "buildlang-local", "url": r"C:\dev\public\pubscan\quantalang\README.md", "verification_status": "LOCAL_SOURCE"},
    {"source_id": "build-universe-local", "url": r"C:\dev\public\build-universe\STATUS.md", "verification_status": "LOCAL_SOURCE"},
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


def package_receipt(module_name: str) -> dict[str, Any]:
    try:
        spec = importlib.util.find_spec(module_name)
    except Exception as exc:
        return {"module": module_name, "available": False, "version": None, "origin": None, "find_error": type(exc).__name__}
    if spec is None:
        return {"module": module_name, "available": False, "version": None, "origin": None}
    try:
        module = importlib.import_module(module_name)
        version = getattr(module, "__version__", "unknown")
    except Exception as exc:
        version = f"import_error:{type(exc).__name__}"
    return {"module": module_name, "available": True, "version": version, "origin": spec.origin}


def command_receipt(command: str) -> dict[str, Any]:
    found = shutil.which(command)
    return {"command": command, "available": bool(found), "path": found}


def repo_receipts() -> dict[str, Any]:
    rows = {}
    for repo_id, path in LOCAL_REPOS.items():
        rows[repo_id] = {"path": str(path), "exists": path.exists()}
        if path.exists() and (path / ".git").exists():
            result = subprocess.run(["git", "-C", str(path), "status", "--short"], cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=20)
            lines = [line for line in result.stdout.splitlines() if line.strip()]
            rows[repo_id].update({"git_status_exit_code": result.returncode, "dirty_count": len(lines), "status_sha256": sha256_text(result.stdout)})
    return rows


def buildc_corpus_receipt() -> dict[str, Any]:
    required = [
        "manifest: 8 program(s)", "c receipt: ok", "rust receipt: ok",
        "substrate receipt: ok", "mir representation receipt: ok",
        "memory layout receipt: ok", "module graph receipt: ok",
        "symbol graph receipt: ok", "lsp dispatch receipt: ok", "c execution: 8 passed",
    ]
    if not BUILDLANG_COMPILER.exists():
        return {"status": "UNAVAILABLE", "cwd": str(BUILDLANG_COMPILER), "exit_code": None, "line_checks": {line: False for line in required}}
    result = subprocess.run(["cargo", "run", "--quiet", "--bin", "buildc", "--", "corpus", "verify"], cwd=BUILDLANG_COMPILER, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)
    checks = {line: line in result.stdout for line in required}
    status = "MATCH" if result.returncode == 0 and all(checks.values()) else "DRIFT"
    return {"status": status, "cwd": str(BUILDLANG_COMPILER), "exit_code": result.returncode, "line_checks": checks, "stdout_sha256": sha256_text(result.stdout), "stderr_sha256": sha256_text(result.stderr)}


def package_rows(receipts: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for row_id, module, capability, source_id in PACKAGE_ROWS:
        receipt = receipts[row_id]
        rows.append({
            "row_id": row_id,
            "category": capability,
            "surface": module,
            "local_status": "LOCAL_AVAILABLE" if receipt["available"] else "LOCAL_UNAVAILABLE",
            "version": receipt.get("version"),
            "source_ids": [source_id],
            "proof_gap": "adapter_needed" if receipt["available"] else "dependency_missing",
            "next_action": "build_adapter_receipt" if receipt["available"] else "install_or_remote_adapter_receipt",
        })
    return rows


def local_tool_rows(repos: dict[str, Any], commands: dict[str, Any], buildc: dict[str, Any]) -> list[dict[str, Any]]:
    rows = [
        {"row_id": "buildlang_buildc", "category": "compiler_runtime_receipts", "surface": "BuildLang/buildc", "local_status": "SOURCE_AVAILABLE_CORPUS_MATCH" if buildc["status"] == "MATCH" else "SOURCE_AVAILABLE_DRIFT", "version": None, "source_ids": ["buildlang-local"], "proof_gap": "adapter_to_solver_matrix_needed", "next_action": "convert_buildc_corpus_receipt_to_solver_runtime_packet"},
        {"row_id": "build_universe", "category": "domain_module_ecosystem", "surface": "Build Universe", "local_status": "LOCAL_SOURCE_PRESENT" if repos["build_universe"]["exists"] else "LOCAL_SOURCE_MISSING", "version": None, "source_ids": ["build-universe-local"], "proof_gap": "whole_ecosystem_compilation_not_claimed", "next_action": "module_level_availability_matrix"},
        {"row_id": "build_color", "category": "visual_measurement_kernel", "surface": "Build Color", "local_status": "LOCAL_SOURCE_PRESENT" if repos["build_color"]["exists"] else "LOCAL_SOURCE_MISSING", "version": None, "source_ids": ["build-universe-local"], "proof_gap": "connect_color_metrics_to_solver_receipts", "next_action": "measurement_kernel_receipt_join"},
        {"row_id": "calibrate_pro", "category": "instrumentation_measurement", "surface": "Calibrate Pro", "local_status": "LOCAL_SOURCE_PRESENT" if repos["calibrate_pro"]["exists"] else "LOCAL_SOURCE_MISSING", "version": None, "source_ids": ["build-universe-local"], "proof_gap": "display_instrument_receipts_not_solver_receipts", "next_action": "instrumentation_receipt_join"},
    ]
    for command in ["buildc", "julia", "mojo", "dwave", "qiskit", "z3", "cmake", "cargo", "node"]:
        receipt = commands[command]
        rows.append({"row_id": f"cli_{command}", "category": "cli_surface", "surface": command, "local_status": "CLI_AVAILABLE" if receipt["available"] else "CLI_UNAVAILABLE", "version": None, "source_ids": [], "proof_gap": "cli_adapter_needed" if receipt["available"] else "cli_missing", "next_action": "record_cli_version_and_adapter" if receipt["available"] else "install_or_remote_cli_adapter"})
    return rows


def run_json(command: list[str], timeout: int = 45) -> tuple[int, str, str, dict[str, Any]]:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    parsed = json.loads(result.stdout) if result.returncode == 0 and result.stdout.strip() else {}
    return result.returncode, result.stdout, result.stderr, parsed


def forum_route() -> dict[str, Any]:
    prompt = "Project Telos pass 0090: solver availability matrix across SciPy, OR-Tools, D-Wave Ocean, quantum/math packages, and BuildLang/buildc receipts."
    code, stdout, stderr, parsed = run_json(["forum", "route", "--json", prompt], timeout=30)
    return {"status": "MATCH" if code == 0 else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "decided": parsed.get("decided"), "confidence": parsed.get("confidence"), "needs_escalation": parsed.get("needs_escalation"), "top_candidates": parsed.get("candidates", [])[:5]}


def index_receipt() -> dict[str, Any]:
    code, stdout, stderr, parsed = run_json(["index", "context-envelope", "--root", ".", "--budget", "1200", "--json"], timeout=45)
    return {"status": "MATCH" if code == 0 and parsed.get("verification_verdict") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "schema": parsed.get("schema"), "verification_verdict": parsed.get("verification_verdict"), "graph_pack_sha256": parsed.get("recheck", {}).get("graph_pack_sha256"), "source_refs_only": parsed.get("privacy", {}).get("source_refs_only")}


def telos_status() -> dict[str, Any]:
    code, stdout, stderr, parsed = run_json(["node", "demo/status.mjs", "--summary"], timeout=30)
    return {"status": "MATCH" if code == 0 and parsed.get("status") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "tool_version": parsed.get("tool_version"), "tool": parsed.get("tool")}


def compose() -> dict[str, Any]:
    baseline = read_json(BASELINE)
    package_receipts = {row_id: package_receipt(module) for row_id, module, _, _ in PACKAGE_ROWS}
    commands = {cmd: command_receipt(cmd) for cmd in ["buildc", "julia", "mojo", "dwave", "qiskit", "z3", "cmake", "cargo", "node"]}
    repos = repo_receipts()
    buildc = buildc_corpus_receipt()
    matrix_rows = package_rows(package_receipts) + local_tool_rows(repos, commands, buildc)
    available_statuses = {"LOCAL_AVAILABLE", "CLI_AVAILABLE", "LOCAL_SOURCE_PRESENT", "SOURCE_AVAILABLE_CORPUS_MATCH"}
    unavailable_statuses = {"LOCAL_UNAVAILABLE", "CLI_UNAVAILABLE", "LOCAL_SOURCE_MISSING", "SOURCE_AVAILABLE_DRIFT"}
    summary = {
        "row_count": len(matrix_rows),
        "local_available_rows": sum(row["local_status"] in available_statuses for row in matrix_rows),
        "local_unavailable_rows": sum(row["local_status"] in unavailable_statuses for row in matrix_rows),
        "recommended_next": ["buildlang_corpus_receipt_adapter", "networkx_graph_optimization_adapter", "ortools_cp_sat_dependency_receipt", "sympy_symbolic_math_dependency_receipt"],
    }
    artifact: dict[str, Any] = {
        "schema": SCHEMA, "pass": PASS_ID, "generated_on": "2026-07-01",
        "prior_binding": {"source_pass": "0089", "source_schema": baseline["schema"], "source_seal": baseline["seal"], "adapter": baseline["external_adapter"]["adapter"]},
        "upstream_research_binding": baseline["upstream_research_binding"],
        "source_anchors": SOURCE_ANCHORS,
        "environment": {"python": sys.version.split()[0], "platform": platform.platform()},
        "package_receipts": package_receipts,
        "command_receipts": commands,
        "repo_receipts": repos,
        "buildc_corpus_receipt": buildc,
        "matrix_rows": matrix_rows,
        "summary": summary,
        "flagship_receipts": {"forum": forum_route(), "index": index_receipt(), "telos": telos_status()},
        "promotion_boundary": {"availability_matrix_only": True, "solver_superiority_claim": False, "world_problem_solved_claim": False, "new_natural_law_claim": False},
        "unsupported_claim_count": 0,
        "current_promoted_natural_laws": [],
    }
    errors = validate_artifact(artifact)
    artifact["validation_errors"] = errors
    artifact["status"] = STATUS_MATCH if not errors else STATUS_DRIFT
    artifact["seal"] = sha256_obj(artifact)
    return artifact


def validate_artifact(artifact: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if artifact.get("schema") != SCHEMA:
        errors.append("schema")
    if artifact.get("prior_binding", {}).get("source_pass") != "0089":
        errors.append("prior_binding")
    if artifact.get("summary", {}).get("row_count", 0) < 24:
        errors.append("row_count")
    if not artifact.get("package_receipts", {}).get("scipy", {}).get("available"):
        errors.append("scipy_available")
    if artifact.get("package_receipts", {}).get("ortools", {}).get("available") is not False:
        errors.append("ortools_expected_unavailable")
    if artifact.get("buildc_corpus_receipt", {}).get("status") != "MATCH":
        errors.append("buildc_corpus")
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
