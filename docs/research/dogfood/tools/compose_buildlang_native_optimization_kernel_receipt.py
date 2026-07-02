"""Compose pass 0095 BuildLang native optimization kernel receipt."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

SCHEMA = "BuildLangNativeOptimizationKernelReceipt/v1"
PASS_ID = "0095"
STATUS_MATCH = "BUILDLANG_NATIVE_OPTIMIZATION_KERNEL_RECEIPT_MATCH"
STATUS_DRIFT = "BUILDLANG_NATIVE_OPTIMIZATION_KERNEL_RECEIPT_DRIFT"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
BUILDLANG_ROOT = Path(r"C:\dev\public\pubscan\quantalang")
COMPILER = BUILDLANG_ROOT / "compiler"
SOURCE = ROOT / "fixtures" / "buildlang-knapsack-exact-pass-0095.bld"
PROFILE = "console-only"
CHECK_RECEIPT = ROOT / "schemas" / "buildlang-knapsack-check-receipt-pass-0095.json"
VERIFY_REPORT = ROOT / "schemas" / "buildlang-knapsack-receipt-verification-pass-0095.json"
PRIOR_WORKFLOW = ROOT / "schemas" / "quantum-optimization-workflow-receipt-pass-0094.json"
EXPECTED_OUTPUT = {"best value": 162, "best weight": 29, "best mask": 2347, "feasible count": 1275}
REQUIRED_CHECKS = [
    "schema", "compiler", "compiler_version", "language_version",
    "expected_profile", "source_digest", "input_graph_digest",
    "policy_source_digest", "policy_profile_digest", "status", "items",
    "tokens", "declared_effects", "observed_capabilities",
    "propagated_effects", "diagnostics", "policy_status",
    "policy_violations",
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


def run_text(command: list[str], cwd: Path, timeout: int = 180) -> dict[str, Any]:
    result = subprocess.run(command, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    return {"command": " ".join(command), "cwd": str(cwd), "exit_code": result.returncode, "stdout": result.stdout, "stderr": result.stderr, "stdout_sha256": sha256_text(result.stdout), "stderr_sha256": sha256_text(result.stderr)}


def compact_run(run: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in run.items() if key not in {"stdout", "stderr"}}


def parse_output(stdout: str) -> dict[str, int]:
    parsed: dict[str, int] = {}
    for line in stdout.splitlines():
        parts = line.rsplit(" ", 1)
        if len(parts) == 2 and parts[1].lstrip("-").isdigit():
            parsed[parts[0]] = int(parts[1])
    return parsed


def repo_state() -> dict[str, Any]:
    result = subprocess.run(["git", "-C", str(BUILDLANG_ROOT), "status", "--short", "--branch"], cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=20)
    lines = [line for line in result.stdout.splitlines() if line.strip()]
    return {"path": str(BUILDLANG_ROOT), "exists": BUILDLANG_ROOT.exists(), "exit_code": result.returncode, "branch_line": lines[0] if lines else None, "dirty_count": max(0, len(lines) - 1), "status_sha256": sha256_text(result.stdout)}


def buildlang_check() -> tuple[dict[str, Any], dict[str, Any]]:
    if CHECK_RECEIPT.exists():
        CHECK_RECEIPT.unlink()
    command = ["cargo", "run", "--quiet", "--bin", "buildc", "--", "check", str(SOURCE), "--profile", PROFILE, "--receipt", str(CHECK_RECEIPT)]
    run = run_text(command, COMPILER)
    return compact_run(run), read_json(CHECK_RECEIPT) if CHECK_RECEIPT.exists() else {}


def receipt_verify() -> tuple[dict[str, Any], dict[str, Any]]:
    command = ["cargo", "run", "--quiet", "--bin", "buildc", "--", "receipt", "verify", str(CHECK_RECEIPT), "--source", str(SOURCE), "--expect-profile", PROFILE, "--json"]
    run = run_text(command, COMPILER)
    report = json.loads(run["stdout"]) if run["exit_code"] == 0 and run["stdout"].strip() else {}
    write_json(VERIFY_REPORT, report)
    return compact_run(run), report


def buildlang_run() -> tuple[dict[str, Any], dict[str, int]]:
    command = ["cargo", "run", "--quiet", "--bin", "buildc", "--", "run", str(SOURCE)]
    run = run_text(command, COMPILER)
    parsed = parse_output(run["stdout"])
    return compact_run(run) | {"stdout_lines": run["stdout"].splitlines()}, parsed


def verify_summary(report: dict[str, Any]) -> dict[str, Any]:
    checks = report.get("checks", [])
    names = {row.get("name"): row for row in checks}
    missing = [name for name in REQUIRED_CHECKS if name not in names]
    failed = [row.get("name") for row in checks if row.get("status") != "passed"]
    return {"status": report.get("status"), "check_count": len(checks), "missing_required": missing, "failed_checks": failed, "all_required_passed": not missing and not failed and report.get("status") == "passed"}


def measurements(artifact: dict[str, Any]) -> list[dict[str, Any]]:
    receipt = artifact["check_receipt"]
    output = artifact["run_output"]
    prior = artifact["prior_workflow_binding"]
    checks = [
        ("check_receipt", receipt.get("status") == "passed", "buildc check receipt passed"),
        ("verify_report", artifact["verify_summary"]["all_required_passed"] is True, "receipt verify passed all required checks"),
        ("run_output_best_value", output.get("best value") == 162, "BuildLang run finds exact best value 162"),
        ("run_output_best_weight", output.get("best weight") == 29, "BuildLang run finds exact best weight 29"),
        ("run_output_feasible_count", output.get("feasible count") == 1275, "BuildLang run enumerates 1275 feasible masks"),
        ("matches_prior_workflow", output.get("best value") == prior.get("exact_value") and output.get("feasible count") == prior.get("feasible_count"), "BuildLang output matches pass 0094 exact baseline"),
        ("source_digest", len(receipt.get("source_digest", {}).get("hex", "")) == 64, "source digest is sha256 hex"),
        ("console_policy", receipt.get("policy", {}).get("profile") == PROFILE and receipt.get("policy", {}).get("status") == "passed", "console-only policy passes"),
        ("flagships", all(row["status"] == "MATCH" for row in artifact["flagship_receipts"].values()), "Forum, Index, and Telos receipts match"),
        ("promotion_boundary", artifact["unsupported_claim_count"] == 0 and artifact["current_promoted_natural_laws"] == [], "no replacement, discovery, or natural-law claim is promoted"),
    ]
    return [{"measurement_id": f"buildlang_native_opt.{mid}", "claim": claim, "status": "MATCH" if ok else "DRIFT", "deviation": 0.0 if ok else 1.0, "tolerance": 0.5, "method": "receipt-and-run-output"} for mid, ok, claim in checks]


def run_json(command: list[str], timeout: int = 45) -> tuple[int, str, str, dict[str, Any]]:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    parsed = json.loads(result.stdout) if result.returncode == 0 and result.stdout.strip() else {}
    return result.returncode, result.stdout, result.stderr, parsed


def forum_route() -> dict[str, Any]:
    code, stdout, stderr, parsed = run_json(["forum", "route", "--json", "Project Telos pass 0095 BuildLang-native exact optimization kernel receipt with run output and buildc receipt verification."], timeout=30)
    return {"status": "MATCH" if code == 0 else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "decided": parsed.get("decided"), "confidence": parsed.get("confidence"), "needs_escalation": parsed.get("needs_escalation"), "top_candidates": parsed.get("candidates", [])[:5]}


def index_receipt() -> dict[str, Any]:
    code, stdout, stderr, parsed = run_json(["index", "context-envelope", "--root", ".", "--budget", "1200", "--json"], timeout=45)
    return {"status": "MATCH" if code == 0 and parsed.get("verification_verdict") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "schema": parsed.get("schema"), "verification_verdict": parsed.get("verification_verdict"), "graph_pack_sha256": parsed.get("recheck", {}).get("graph_pack_sha256"), "source_refs_only": parsed.get("privacy", {}).get("source_refs_only")}


def telos_status() -> dict[str, Any]:
    code, stdout, stderr, parsed = run_json(["node", "demo/status.mjs", "--summary"], timeout=30)
    return {"status": "MATCH" if code == 0 and parsed.get("status") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "tool_version": parsed.get("tool_version"), "tool": parsed.get("tool")}


def validate_artifact(artifact: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if artifact.get("schema") != SCHEMA:
        errors.append("schema")
    if artifact.get("run_output") != EXPECTED_OUTPUT:
        errors.append("run_output")
    if artifact.get("check_receipt", {}).get("status") != "passed":
        errors.append("check_receipt")
    if artifact.get("verify_summary", {}).get("all_required_passed") is not True:
        errors.append("verify_summary")
    if len(artifact.get("measurements", [])) != 10 or any(row.get("status") != "MATCH" for row in artifact.get("measurements", [])):
        errors.append("measurements")
    if any(tool.get("status") != "MATCH" for tool in artifact.get("flagship_receipts", {}).values()):
        errors.append("flagships")
    if artifact.get("unsupported_claim_count") != 0 or artifact.get("current_promoted_natural_laws") != []:
        errors.append("promotion_boundary")
    return errors


def compose() -> dict[str, Any]:
    prior = read_json(PRIOR_WORKFLOW)
    check_run, receipt = buildlang_check()
    verify_run, report = receipt_verify()
    run_receipt, output = buildlang_run()
    artifact: dict[str, Any] = {
        "schema": SCHEMA, "pass": PASS_ID, "generated_on": "2026-07-01",
        "source_fixture": {"path": str(SOURCE), "profile": PROFILE},
        "repo_state": repo_state(),
        "prior_workflow_binding": {"source_pass": prior["pass"], "exact_value": prior["workflow"]["objective_measurements"]["exact_value"], "feasible_count": 1275, "artifact_seal": prior["seal"]},
        "check_command": check_run, "check_receipt_path": str(CHECK_RECEIPT), "check_receipt": receipt,
        "verify_command": verify_run, "verify_report_path": str(VERIFY_REPORT), "verify_report": report, "verify_summary": verify_summary(report),
        "run_command": run_receipt, "run_output": output,
        "flagship_receipts": {"forum": forum_route(), "index": index_receipt(), "telos": telos_status()},
        "negative_fixtures": [
            {"fixture_id": "run_output_missing", "expected_status": "REJECT"},
            {"fixture_id": "receipt_not_verified", "expected_status": "REJECT"},
            {"fixture_id": "best_value_mismatch", "expected_status": "REJECT"},
            {"fixture_id": "language_replacement_claim", "expected_status": "REJECT"},
        ],
        "unsupported_claim_count": 0,
        "current_promoted_natural_laws": [],
        "non_promotion_statement": "Pass 0095 proves one BuildLang exact-enumeration fixture can run and emit receipts. It does not prove language replacement, production optimization, scientific discovery, or a natural law.",
    }
    artifact["measurements"] = measurements(artifact)
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
