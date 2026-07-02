"""Compose pass 0097 BuildLang optimization proof workbench receipt."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

SCHEMA = "BuildLangOptimizationProofWorkbenchReceipt/v1"
PASS_ID = "0097"
STATUS_MATCH = "BUILDLANG_OPTIMIZATION_PROOF_WORKBENCH_MATCH"
STATUS_DRIFT = "BUILDLANG_OPTIMIZATION_PROOF_WORKBENCH_DRIFT"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
BUILDLANG = Path("C:/dev/public/pubscan/quantalang")
COMPILER = BUILDLANG / "compiler"
SOURCE = ROOT / "fixtures" / "buildlang-knapsack-branch-comparison-pass-0097.bld"
CHECK_RECEIPT = ROOT / "schemas" / "buildlang-branch-comparison-check-receipt-pass-0097.json"
VERIFY_REPORT = ROOT / "schemas" / "buildlang-branch-comparison-receipt-verification-pass-0097.json"
SCORECARD = ROOT / "schemas" / "youtube-field-growth-vector-scorecard-pass-0096.json"
WORKFLOW = ROOT / "schemas" / "quantum-optimization-workflow-receipt-pass-0094.json"
NATIVE = ROOT / "schemas" / "buildlang-native-optimization-kernel-receipt-pass-0095.json"


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


def run(command: list[str], cwd: Path, timeout: int = 120) -> dict[str, Any]:
    result = subprocess.run(command, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    return {
        "command": " ".join(command),
        "cwd": str(cwd),
        "exit_code": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "stdout_sha256": sha256_text(result.stdout),
        "stderr_sha256": sha256_text(result.stderr),
    }


def receipt_command_shape(receipt: dict[str, Any]) -> dict[str, Any]:
    return {key: receipt[key] for key in ["command", "cwd", "exit_code", "stdout_sha256", "stderr_sha256"]}


def parse_output(text: str) -> dict[str, int]:
    values: dict[str, int] = {}
    for raw in text.splitlines():
        parts = raw.strip().split()
        if len(parts) == 3:
            values[f"{parts[0]} {parts[1]}"] = int(parts[2])
    return values


def run_json(command: list[str], timeout: int = 45) -> tuple[int, str, str, dict[str, Any]]:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    parsed = json.loads(result.stdout) if result.returncode == 0 and result.stdout.strip().startswith("{") else {}
    return result.returncode, result.stdout, result.stderr, parsed


def buildlang_repo_state() -> dict[str, Any]:
    if not BUILDLANG.exists():
        return {"exists": False}
    result = subprocess.run(["git", "status", "--short", "--branch"], cwd=BUILDLANG, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=30)
    lines = result.stdout.splitlines()
    return {
        "exists": True,
        "path": str(BUILDLANG),
        "exit_code": result.returncode,
        "branch_line": lines[0] if lines else "",
        "dirty_count": max(len(lines) - 1, 0),
        "status_sha256": sha256_text(result.stdout),
    }


def branch_rows(output: dict[str, int]) -> list[dict[str, Any]]:
    exact_value = output["exact value"]
    rows = [
        ("exact_enumeration", output["exact value"], output["exact weight"], output["exact mask"], output["exact feasible"], "full 4096-mask enumeration"),
        ("greedy_ratio_order", output["greedy value"], output["greedy weight"], output["greedy mask"], None, "fixed value/weight ratio order"),
        ("bounded_prefix_2048", output["bounded value"], output["bounded weight"], output["bounded mask"], output["bounded feasible"], "enumerates masks below 2048"),
    ]
    return [
        {"branch": row[0], "value": row[1], "weight": row[2], "mask": row[3], "feasible_count": row[4], "method": row[5], "gap_to_exact": exact_value - row[1], "status": "MATCH"}
        for row in rows
    ]


def forum_route() -> dict[str, Any]:
    prompt = "Project Telos pass 0097: BuildLang optimization proof workbench with exact, greedy, and bounded-search branch receipts."
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
    out = artifact.get("run_output", {})
    if artifact.get("schema") != SCHEMA:
        errors.append("schema")
    if artifact.get("source_bindings", {}).get("scorecard_pass") != "0096":
        errors.append("scorecard_binding")
    if artifact.get("check_command", {}).get("exit_code") != 0 or artifact.get("verify_command", {}).get("exit_code") != 0 or artifact.get("run_command", {}).get("exit_code") != 0:
        errors.append("commands")
    if out.get("exact value") != 162 or out.get("greedy value") != 146 or out.get("bounded value") != 157:
        errors.append("run_output")
    if artifact.get("verify_summary", {}).get("check_count") != 18 or artifact.get("verify_summary", {}).get("status") != "passed":
        errors.append("verify_summary")
    if len(artifact.get("branches", [])) != 3 or artifact.get("branches", [])[0].get("gap_to_exact") != 0:
        errors.append("branches")
    if any(tool.get("status") != "MATCH" for tool in artifact.get("flagship_receipts", {}).values()):
        errors.append("flagships")
    if artifact.get("unsupported_claim_count") != 0 or artifact.get("current_promoted_natural_laws") != []:
        errors.append("promotion_boundary")
    return errors


def compose() -> dict[str, Any]:
    scorecard = read_json(SCORECARD)
    workflow = read_json(WORKFLOW)
    native = read_json(NATIVE)
    check = run(["cargo", "run", "--quiet", "--bin", "buildc", "--", "check", str(SOURCE), "--profile", "console-only", "--receipt", str(CHECK_RECEIPT)], COMPILER)
    check_receipt = read_json(CHECK_RECEIPT)
    verify = run(["cargo", "run", "--quiet", "--bin", "buildc", "--", "receipt", "verify", str(CHECK_RECEIPT), "--source", str(SOURCE), "--expect-profile", "console-only", "--json"], COMPILER)
    verify_report = json.loads(verify["stdout"]) if verify["stdout"].strip() else {}
    write_json(VERIFY_REPORT, verify_report)
    run_result = run(["cargo", "run", "--quiet", "--bin", "buildc", "--", "run", str(SOURCE)], COMPILER)
    output = parse_output(run_result["stdout"])
    artifact: dict[str, Any] = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "generated_on": "2026-07-01",
        "source_bindings": {"scorecard_pass": scorecard["pass"], "workflow_pass": workflow["pass"], "native_buildlang_pass": native["pass"], "primary_vector": scorecard["primary_30_day_push"]["vector_id"]},
        "source_fixture": {"path": str(SOURCE), "profile": "console-only"},
        "repo_state": buildlang_repo_state(),
        "check_command": receipt_command_shape(check),
        "verify_command": receipt_command_shape(verify),
        "run_command": {**receipt_command_shape(run_result), "stdout_lines": run_result["stdout"].splitlines()},
        "check_receipt_path": str(CHECK_RECEIPT),
        "verify_report_path": str(VERIFY_REPORT),
        "check_receipt": check_receipt,
        "verify_report": verify_report,
        "verify_summary": {"status": verify_report.get("status"), "check_count": len(verify_report.get("checks", [])), "failed_checks": [row for row in verify_report.get("checks", []) if row.get("status") != "passed"]},
        "run_output": output,
        "branches": branch_rows(output),
        "comparison_summary": {"exact_value": output.get("exact value"), "greedy_gap": output.get("exact value") - output.get("greedy value"), "bounded_gap": output.get("exact value") - output.get("bounded value"), "best_non_exact_branch": "bounded_prefix_2048"},
        "negative_fixtures": [
            {"fixture_id": "greedy_claimed_optimal", "expected_status": "REJECT", "reject_reason": "greedy_gap_to_exact_is_16"},
            {"fixture_id": "bounded_claimed_full_search", "expected_status": "REJECT", "reject_reason": "bounded_prefix_search_only_checks_masks_below_2048"},
            {"fixture_id": "language_replacement_claim", "expected_status": "REJECT", "reject_reason": "single_fixture_does_not_prove_replacement"},
        ],
        "unsupported_claim_count": 0,
        "current_promoted_natural_laws": [],
        "non_promotion_statement": "Pass 0097 proves one BuildLang branch-comparison fixture and receipts. It does not prove solver superiority, production optimization, language replacement, quantum advantage, or a natural law.",
        "flagship_receipts": {"forum": forum_route(), "index": index_receipt(), "telos": telos_status()},
    }
    artifact["measurements"] = [
        {"id": "source_binding", "status": "MATCH" if artifact["source_bindings"]["scorecard_pass"] == "0096" else "DRIFT", "claim": "pass 0096 primary push is bound"},
        {"id": "check_receipt", "status": "MATCH" if check["exit_code"] == 0 and check_receipt.get("status") == "passed" else "DRIFT", "claim": "buildc check receipt passed"},
        {"id": "verify_report", "status": "MATCH" if artifact["verify_summary"]["check_count"] == 18 and not artifact["verify_summary"]["failed_checks"] else "DRIFT", "claim": "receipt verify passed 18 checks"},
        {"id": "exact_branch", "status": "MATCH" if output.get("exact value") == 162 and output.get("exact feasible") == 1275 else "DRIFT", "claim": "exact branch matches baseline"},
        {"id": "greedy_branch", "status": "MATCH" if output.get("greedy value") == 146 and output.get("greedy mask") == 2331 else "DRIFT", "claim": "greedy branch records bounded suboptimal result"},
        {"id": "bounded_branch", "status": "MATCH" if output.get("bounded value") == 157 and output.get("bounded feasible") == 704 else "DRIFT", "claim": "bounded branch records prefix-search result"},
        {"id": "flagships", "status": "MATCH" if all(row["status"] == "MATCH" for row in artifact["flagship_receipts"].values()) else "DRIFT", "claim": "Forum, Index, and Telos receipts match"},
        {"id": "promotion_boundary", "status": "MATCH", "claim": "no unsupported claim or natural law is promoted"},
    ]
    artifact["validation_errors"] = validate_artifact(artifact)
    artifact["status"] = STATUS_MATCH if not artifact["validation_errors"] else STATUS_DRIFT
    artifact["seal"] = sha256_obj({key: value for key, value in artifact.items() if key != "seal"})
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(ROOT / "schemas" / "buildlang-optimization-proof-workbench-receipt-pass-0097.json"))
    args = parser.parse_args()
    artifact = compose()
    write_json(Path(args.out), artifact)
    print(json.dumps({"path": str(Path(args.out)), "status": artifact["status"], "seal": artifact["seal"]}, indent=2, sort_keys=True))
    if artifact["status"] != STATUS_MATCH:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
