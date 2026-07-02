"""Compose pass 0092 BuildLang source-level check receipt adapter."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

SCHEMA = "BuildLangCheckReceiptAdapter/v1"
PASS_ID = "0092"
STATUS_MATCH = "BUILDLANG_CHECK_RECEIPT_ADAPTER_MATCH"
STATUS_DRIFT = "BUILDLANG_CHECK_RECEIPT_ADAPTER_DRIFT"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
BASELINE = ROOT / "schemas" / "buildlang-corpus-crucible-adapter-pass-0091.json"
BUILDLANG_ROOT = Path(r"C:\dev\public\pubscan\quantalang")
BUILDLANG_COMPILER = BUILDLANG_ROOT / "compiler"
SOURCE = BUILDLANG_ROOT / "examples" / "quickstart" / "hello.bld"
PROFILE = "console-only"
CHECK_RECEIPT_PATH = ROOT / "schemas" / "buildlang-check-receipt-pass-0092.json"
VERIFY_REPORT_PATH = ROOT / "schemas" / "buildlang-receipt-verification-pass-0092.json"
SOURCE_ANCHORS = [
    {"source_id": "buildlang-usage", "url": r"C:\dev\public\pubscan\quantalang\USAGE.md", "verification_status": "LOCAL_SOURCE"},
    {"source_id": "buildlang-readme", "url": r"C:\dev\public\pubscan\quantalang\README.md", "verification_status": "LOCAL_SOURCE"},
    {"source_id": "pass-0091-corpus-adapter", "url": "docs/research/dogfood/pass-0091-ledger.md", "verification_status": "LOCAL_BASELINE"},
]
REQUIRED_VERIFY_CHECKS = [
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


def run_text(command: list[str], cwd: Path, timeout: int = 120) -> dict[str, Any]:
    result = subprocess.run(command, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    return {"command": " ".join(command), "cwd": str(cwd), "exit_code": result.returncode, "stdout_sha256": sha256_text(result.stdout), "stderr_sha256": sha256_text(result.stderr), "stdout": result.stdout, "stderr": result.stderr}


def repo_state() -> dict[str, Any]:
    result = subprocess.run(["git", "-C", str(BUILDLANG_ROOT), "status", "--short", "--branch"], cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=20)
    lines = [line for line in result.stdout.splitlines() if line.strip()]
    return {"path": str(BUILDLANG_ROOT), "exists": BUILDLANG_ROOT.exists(), "exit_code": result.returncode, "branch_line": lines[0] if lines else None, "dirty_count": max(0, len(lines) - 1), "status_sha256": sha256_text(result.stdout)}


def run_check_receipt() -> tuple[dict[str, Any], dict[str, Any]]:
    CHECK_RECEIPT_PATH.parent.mkdir(parents=True, exist_ok=True)
    if CHECK_RECEIPT_PATH.exists():
        CHECK_RECEIPT_PATH.unlink()
    command = ["cargo", "run", "--quiet", "--bin", "buildc", "--", "check", str(SOURCE), "--profile", PROFILE, "--receipt", str(CHECK_RECEIPT_PATH)]
    run = run_text(command, BUILDLANG_COMPILER, timeout=180)
    receipt = read_json(CHECK_RECEIPT_PATH) if CHECK_RECEIPT_PATH.exists() else {}
    run.pop("stdout")
    run.pop("stderr")
    return run, receipt


def run_receipt_verify() -> tuple[dict[str, Any], dict[str, Any]]:
    command = ["cargo", "run", "--quiet", "--bin", "buildc", "--", "receipt", "verify", str(CHECK_RECEIPT_PATH), "--source", str(SOURCE), "--expect-profile", PROFILE, "--json"]
    run = run_text(command, BUILDLANG_COMPILER, timeout=180)
    report = json.loads(run["stdout"]) if run["exit_code"] == 0 and run["stdout"].strip() else {}
    write_json(VERIFY_REPORT_PATH, report)
    run.pop("stdout")
    run.pop("stderr")
    return run, report


def verify_summary(report: dict[str, Any]) -> dict[str, Any]:
    checks = report.get("checks", [])
    names = {row.get("name"): row for row in checks}
    missing = [name for name in REQUIRED_VERIFY_CHECKS if name not in names]
    failed = [row.get("name") for row in checks if row.get("status") != "passed"]
    return {"status": report.get("status"), "check_count": len(checks), "required_count": len(REQUIRED_VERIFY_CHECKS), "missing_required": missing, "failed_checks": failed, "all_required_passed": not missing and not failed and report.get("status") == "passed"}


def adapter_measurements(receipt: dict[str, Any], report: dict[str, Any], summary: dict[str, Any]) -> list[dict[str, Any]]:
    checks = {row["name"]: row for row in report.get("checks", []) if "name" in row}
    rows = [
        ("receipt_schema", "schema", receipt.get("schema") == "buildlang-check-receipt/v1", "receipt schema is buildlang-check-receipt/v1"),
        ("receipt_status", "status", receipt.get("status") == "passed", "check receipt status is passed"),
        ("source_digest", "source_digest", len(receipt.get("source_digest", {}).get("hex", "")) == 64, "source digest is sha256 hex"),
        ("input_graph_digest", "input_graph_digest", len(receipt.get("input_graph_digest", {}).get("hex", "")) == 64, "input graph digest is sha256 hex"),
        ("policy_profile", "expected_profile", receipt.get("policy", {}).get("profile") == PROFILE, "policy profile is console-only"),
        ("policy_status", "policy_status", receipt.get("policy", {}).get("status") == "passed", "policy status is passed"),
        ("declared_effects", "declared_effects", receipt.get("declared_effects", {}).get("main") == ["Console"], "main declares Console effect"),
        ("observed_capabilities", "observed_capabilities", receipt.get("observed_capabilities", {}).get("main", {}).get("Console") == ["println!"], "main observes Console println! capability"),
        ("diagnostics", "diagnostics", receipt.get("diagnostics") == [], "diagnostics are empty"),
        ("verify_report", "schema", summary.get("all_required_passed") is True, "receipt verify required checks all passed"),
    ]
    measurements = []
    for measurement_id, check_name, matched, claim in rows:
        measurements.append({
            "measurement_id": f"buildc_check.{measurement_id}",
            "claim": claim,
            "status": "MATCH" if matched else "DRIFT",
            "deviation": 0.0 if matched else 1.0,
            "tolerance": 0.5,
            "method": "receipt-field-and-verify-report",
            "evidence": [f"receipt_sha256={sha256_obj(receipt)}", f"verify_status={report.get('status')}", f"verify_check={check_name}", f"verify_check_status={checks.get(check_name, {}).get('status')}"],
        })
    return measurements


def run_json(command: list[str], timeout: int = 45) -> tuple[int, str, str, dict[str, Any]]:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    parsed = json.loads(result.stdout) if result.returncode == 0 and result.stdout.strip() else {}
    return result.returncode, result.stdout, result.stderr, parsed


def forum_route() -> dict[str, Any]:
    prompt = "Project Telos pass 0092: source-level BuildLang buildc check receipt adapter with policy, effects, source digest, and receipt verification."
    code, stdout, stderr, parsed = run_json(["forum", "route", "--json", prompt], timeout=30)
    return {"status": "MATCH" if code == 0 else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "decided": parsed.get("decided"), "confidence": parsed.get("confidence"), "needs_escalation": parsed.get("needs_escalation"), "top_candidates": parsed.get("candidates", [])[:5]}


def index_receipt() -> dict[str, Any]:
    code, stdout, stderr, parsed = run_json(["index", "context-envelope", "--root", ".", "--budget", "1200", "--json"], timeout=45)
    return {"status": "MATCH" if code == 0 and parsed.get("verification_verdict") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "schema": parsed.get("schema"), "verification_verdict": parsed.get("verification_verdict"), "graph_pack_sha256": parsed.get("recheck", {}).get("graph_pack_sha256"), "source_refs_only": parsed.get("privacy", {}).get("source_refs_only")}


def telos_status() -> dict[str, Any]:
    code, stdout, stderr, parsed = run_json(["node", "demo/status.mjs", "--summary"], timeout=30)
    return {"status": "MATCH" if code == 0 and parsed.get("status") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "tool_version": parsed.get("tool_version"), "tool": parsed.get("tool")}


def negative_fixtures() -> list[dict[str, str]]:
    return [
        {"fixture_id": "missing_source_digest", "expected_status": "REJECT", "reject_reason": "source_digest_required"},
        {"fixture_id": "missing_receipt_verify_report", "expected_status": "REJECT", "reject_reason": "receipt_verify_required"},
        {"fixture_id": "policy_not_console_only", "expected_status": "REJECT", "reject_reason": "expected_profile_required"},
        {"fixture_id": "observed_capability_missing", "expected_status": "REJECT", "reject_reason": "capability_evidence_required"},
        {"fixture_id": "claims_language_replacement", "expected_status": "REJECT", "reject_reason": "single_receipt_does_not_prove_language_market_replacement"},
    ]


def validate_artifact(artifact: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    receipt = artifact.get("check_receipt", {})
    verify = artifact.get("verify_report", {})
    adapter = artifact.get("crucible_adapter", {})
    if artifact.get("schema") != SCHEMA:
        errors.append("schema")
    if artifact.get("prior_binding", {}).get("source_pass") != "0091":
        errors.append("prior_binding")
    if artifact.get("check_command", {}).get("exit_code") != 0 or artifact.get("verify_command", {}).get("exit_code") != 0:
        errors.append("commands")
    if receipt.get("schema") != "buildlang-check-receipt/v1" or receipt.get("status") != "passed":
        errors.append("check_receipt")
    if receipt.get("policy", {}).get("profile") != PROFILE or receipt.get("policy", {}).get("status") != "passed":
        errors.append("policy")
    if receipt.get("observed_capabilities", {}).get("main", {}).get("Console") != ["println!"]:
        errors.append("observed_capabilities")
    if verify.get("status") != "passed" or artifact.get("verify_summary", {}).get("all_required_passed") is not True:
        errors.append("verify_report")
    if adapter.get("measurement_count") != 10 or adapter.get("drift") != 0:
        errors.append("adapter")
    if any(row.get("status") != "MATCH" for row in adapter.get("measurements", [])):
        errors.append("measurements")
    if any(tool.get("status") != "MATCH" for tool in artifact.get("flagship_receipts", {}).values()):
        errors.append("flagship_receipts")
    if artifact.get("unsupported_claim_count") != 0 or artifact.get("current_promoted_natural_laws") != []:
        errors.append("unsupported_claims")
    return errors


def compose() -> dict[str, Any]:
    baseline = read_json(BASELINE)
    check_command, receipt = run_check_receipt()
    verify_command, report = run_receipt_verify()
    summary = verify_summary(report)
    measurements = adapter_measurements(receipt, report, summary)
    adapter = {"adapter_id": "buildc_check_receipt_to_crucible_measurements", "measurement_count": len(measurements), "match": sum(row["status"] == "MATCH" for row in measurements), "drift": sum(row["status"] != "MATCH" for row in measurements), "measurements": measurements}
    artifact: dict[str, Any] = {
        "schema": SCHEMA, "pass": PASS_ID, "generated_on": "2026-07-01",
        "prior_binding": {"source_pass": "0091", "source_schema": baseline["schema"], "source_seal": baseline["seal"]},
        "source_anchors": SOURCE_ANCHORS,
        "source_fixture": {"path": str(SOURCE), "profile": PROFILE},
        "repo_state": repo_state(),
        "check_command": check_command,
        "check_receipt_path": str(CHECK_RECEIPT_PATH),
        "check_receipt": receipt,
        "verify_command": verify_command,
        "verify_report_path": str(VERIFY_REPORT_PATH),
        "verify_report": report,
        "verify_summary": summary,
        "crucible_adapter": adapter,
        "negative_fixtures": negative_fixtures(),
        "flagship_receipts": {"forum": forum_route(), "index": index_receipt(), "telos": telos_status()},
        "promotion_boundary": {"source_receipt_adapter_only": True, "language_replacement_claim": False, "scientific_discovery_claim": False, "new_natural_law_claim": False},
        "unsupported_claim_count": 0,
        "current_promoted_natural_laws": [],
        "non_promotion_statement": "Pass 0092 converts one buildc check receipt into Crucible-ready measurements. It does not prove language replacement, scientific discovery, full compiler correctness, or a natural law.",
    }
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
