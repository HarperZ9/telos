"""Compose pass 0091 BuildLang corpus-to-Crucible adapter receipt."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

SCHEMA = "BuildLangCorpusCrucibleAdapterReceipt/v1"
PASS_ID = "0091"
STATUS_MATCH = "BUILDLANG_CORPUS_CRUCIBLE_ADAPTER_MATCH"
STATUS_DRIFT = "BUILDLANG_CORPUS_CRUCIBLE_ADAPTER_DRIFT"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
BASELINE = ROOT / "schemas" / "solver-availability-matrix-receipt-pass-0090.json"
PROOF_SURFACE = ROOT / "schemas" / "buildlang-proof-packet-demo-surface-pass-0080.json"
BUILDLANG_ROOT = Path(r"C:\dev\public\pubscan\quantalang")
BUILDLANG_COMPILER = BUILDLANG_ROOT / "compiler"
EXPECTED_LINES = [
    ("manifest_programs", "manifest: 8 program(s)"),
    ("c_receipt", "c receipt: ok"),
    ("rust_receipt", "rust receipt: ok"),
    ("substrate_receipt", "substrate receipt: ok"),
    ("mir_representation_receipt", "mir representation receipt: ok"),
    ("memory_layout_receipt", "memory layout receipt: ok"),
    ("module_graph_receipt", "module graph receipt: ok"),
    ("symbol_graph_receipt", "symbol graph receipt: ok"),
    ("lsp_dispatch_receipt", "lsp dispatch receipt: ok"),
    ("c_execution", "c execution: 8 passed"),
]
SOURCE_ANCHORS = [
    {"source_id": "buildlang-readme", "url": r"C:\dev\public\pubscan\quantalang\README.md", "verification_status": "LOCAL_SOURCE"},
    {"source_id": "pass-0090-solver-matrix", "url": "docs/research/dogfood/pass-0090-ledger.md", "verification_status": "LOCAL_BASELINE"},
    {"source_id": "pass-0080-buildlang-proof-surface", "url": "docs/research/dogfood/pass-0080-ledger.md", "verification_status": "LOCAL_BASELINE"},
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
    return {"command": " ".join(command), "cwd": str(cwd), "exit_code": result.returncode, "stdout": result.stdout, "stderr": result.stderr, "stdout_sha256": sha256_text(result.stdout), "stderr_sha256": sha256_text(result.stderr)}


def repo_state() -> dict[str, Any]:
    if not BUILDLANG_ROOT.exists():
        return {"exists": False, "path": str(BUILDLANG_ROOT), "dirty_count": None, "branch_line": None}
    result = subprocess.run(["git", "-C", str(BUILDLANG_ROOT), "status", "--short", "--branch"], cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=20)
    lines = [line for line in result.stdout.splitlines() if line.strip()]
    return {"exists": True, "path": str(BUILDLANG_ROOT), "exit_code": result.returncode, "branch_line": lines[0] if lines else None, "dirty_count": max(0, len(lines) - 1), "status_sha256": sha256_text(result.stdout)}


def buildc_corpus_run() -> dict[str, Any]:
    if not BUILDLANG_COMPILER.exists():
        return {"status": "UNAVAILABLE", "exit_code": None, "line_checks": {key: False for key, _ in EXPECTED_LINES}, "match": 0, "drift": len(EXPECTED_LINES)}
    receipt = run_text(["cargo", "run", "--quiet", "--bin", "buildc", "--", "corpus", "verify"], BUILDLANG_COMPILER, timeout=120)
    checks = {key: text in receipt["stdout"] for key, text in EXPECTED_LINES}
    receipt["line_checks"] = checks
    receipt["match"] = sum(checks.values())
    receipt["drift"] = len(checks) - receipt["match"]
    receipt["status"] = "MATCH" if receipt["exit_code"] == 0 and receipt["drift"] == 0 else "DRIFT"
    receipt.pop("stdout")
    receipt.pop("stderr")
    return receipt


def measurement_templates(corpus: dict[str, Any]) -> list[dict[str, Any]]:
    templates = []
    for key, expected in EXPECTED_LINES:
        matched = corpus["line_checks"].get(key) is True
        templates.append({
            "measurement_id": f"buildc_corpus.{key}",
            "claim": f"BuildLang corpus verification includes expected line: {expected}",
            "method": "stdout-line-presence",
            "expected_line": expected,
            "deviation": 0.0 if matched else 1.0,
            "tolerance": 0.5,
            "status": "MATCH" if matched else "DRIFT",
            "evidence": [f"stdout_sha256={corpus.get('stdout_sha256')}", f"exit_code={corpus.get('exit_code')}", f"line_key={key}"],
        })
    return templates


def run_json(command: list[str], timeout: int = 45) -> tuple[int, str, str, dict[str, Any]]:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    parsed = json.loads(result.stdout) if result.returncode == 0 and result.stdout.strip() else {}
    return result.returncode, result.stdout, result.stderr, parsed


def forum_route() -> dict[str, Any]:
    prompt = "Project Telos pass 0091: BuildLang buildc corpus verify output converted into Crucible-ready measurement templates."
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
        {"fixture_id": "missing_corpus_stdout_digest", "expected_status": "REJECT", "reject_reason": "adapter_requires_stdout_digest"},
        {"fixture_id": "missing_expected_line", "expected_status": "REJECT", "reject_reason": "every_corpus_line_becomes_measurement"},
        {"fixture_id": "unrecorded_repo_dirty_state", "expected_status": "REJECT", "reject_reason": "repo_state_must_be_recorded"},
        {"fixture_id": "claims_julia_replacement", "expected_status": "REJECT", "reject_reason": "corpus_adapter_does_not_prove_language_replacement"},
        {"fixture_id": "claims_new_law", "expected_status": "REJECT", "reject_reason": "verification_adapter_is_not_a_natural_law"},
    ]


def validate_artifact(artifact: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    adapter = artifact.get("crucible_adapter", {})
    if artifact.get("schema") != SCHEMA:
        errors.append("schema")
    if artifact.get("prior_binding", {}).get("source_pass") != "0090":
        errors.append("prior_binding")
    if artifact.get("proof_surface_binding", {}).get("source_pass") != "0080":
        errors.append("proof_surface_binding")
    if artifact.get("buildc_corpus_run", {}).get("status") != "MATCH":
        errors.append("buildc_corpus")
    if artifact.get("repo_state", {}).get("exists") is not True:
        errors.append("repo_state")
    if adapter.get("measurement_count") != len(EXPECTED_LINES) or adapter.get("drift") != 0:
        errors.append("adapter_measurements")
    if any(item.get("status") != "MATCH" for item in adapter.get("measurements", [])):
        errors.append("measurement_status")
    if any(receipt.get("status") != "MATCH" for receipt in artifact.get("flagship_receipts", {}).values()):
        errors.append("flagship_receipts")
    if artifact.get("unsupported_claim_count") != 0 or artifact.get("current_promoted_natural_laws") != []:
        errors.append("unsupported_claims")
    return errors


def compose() -> dict[str, Any]:
    baseline = read_json(BASELINE)
    proof = read_json(PROOF_SURFACE)
    corpus = buildc_corpus_run()
    measurements = measurement_templates(corpus)
    adapter = {
        "adapter_id": "buildc_corpus_to_crucible_measurements",
        "measurement_count": len(measurements),
        "match": sum(item["status"] == "MATCH" for item in measurements),
        "drift": sum(item["status"] != "MATCH" for item in measurements),
        "measurements": measurements,
    }
    artifact: dict[str, Any] = {
        "schema": SCHEMA, "pass": PASS_ID, "generated_on": "2026-07-01",
        "prior_binding": {"source_pass": "0090", "source_schema": baseline["schema"], "source_seal": baseline["seal"]},
        "proof_surface_binding": {"source_pass": "0080", "source_schema": proof["schema"], "source_seal": proof["seal"], "market_motion": proof["market_motion"]},
        "source_anchors": SOURCE_ANCHORS,
        "repo_state": repo_state(),
        "buildc_corpus_run": corpus,
        "crucible_adapter": adapter,
        "negative_fixtures": negative_fixtures(),
        "flagship_receipts": {"forum": forum_route(), "index": index_receipt(), "telos": telos_status()},
        "promotion_boundary": {"adapter_only": True, "julia_replacement_claim": False, "scientific_discovery_claim": False, "new_natural_law_claim": False},
        "unsupported_claim_count": 0,
        "current_promoted_natural_laws": [],
        "non_promotion_statement": "Pass 0091 converts live buildc corpus verification into Crucible-ready measurements. It does not prove language-market replacement, scientific discovery, or a natural law.",
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
