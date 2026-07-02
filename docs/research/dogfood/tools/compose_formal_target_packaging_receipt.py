"""Compose pass 0118 formal target packaging receipt."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from formal_target_sources_pass_0118 import source_specs  # noqa: E402

SCHEMA = "FormalTargetPackagingReceipt/v1"
PASS_ID = "0118"
STATUS_MATCH = "FORMAL_TARGET_PACKAGING_MATCH"
STATUS_DRIFT = "FORMAL_TARGET_PACKAGING_DRIFT"
ADAPTER = ROOT / "schemas" / "theorem-prover-adapter-receipt-pass-0117.json"
TARGET_DIR = ROOT / "formal-targets" / "pass-0118"


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_obj(value: object) -> str:
    return sha256_text(canonical_json(value))


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.encode("ascii", "ignore").decode("ascii"), encoding="utf-8", newline="\n")


def write_json(path: Path, value: object) -> None:
    write_text(path, json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n")


def run_json(command: list[str], timeout: int = 45) -> tuple[int, str, str, dict[str, Any]]:
    result = subprocess.run(
        command,
        cwd=REPO,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
    )
    parsed = json.loads(result.stdout) if result.returncode == 0 and result.stdout.strip().startswith("{") else {}
    return result.returncode, result.stdout, result.stderr, parsed


def availability() -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for exe in ["lean", "lake", "coqc", "isabelle", "agda"]:
        path = shutil.which(exe)
        result[exe] = {"executable": exe, "status": "AVAILABLE" if path else "MISSING", "path": path}
    return result


def adapter_target_ids(adapter: dict[str, Any]) -> list[str]:
    return [row["proposition"] for row in adapter["theorem_targets"]]


def emit_sources(ids: list[str], avail: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in source_specs(TARGET_DIR):
        write_text(spec["path"], spec["source"])
        text = spec["path"].read_text(encoding="utf-8")
        present = [target_id for target_id in ids if target_id in text]
        ok = len(present) == len(ids) and text.isascii()
        rows.append({
            "language": spec["language"],
            "path": str(spec["path"].relative_to(ROOT)).replace("\\", "/"),
            "sha256": sha256_file(spec["path"]),
            "bytes": spec["path"].stat().st_size,
            "ascii": text.isascii(),
            "proposition_ids_present": present,
            "expected_proposition_count": len(ids),
            "toolchain_executable": spec["executable"],
            "toolchain_status": avail[spec["executable"]]["status"],
            "parser_command": spec["command"],
            "execution_status": "NOT_EXECUTED",
            "status": "SOURCE_EMITTED_NOT_EXECUTED" if ok else "SOURCE_EMIT_DRIFT",
        })
    return rows


def write_manifest(sources: list[dict[str, Any]], ids: list[str]) -> dict[str, Any]:
    manifest = {
        "schema": "FormalTargetSourceManifest/v1",
        "pass": PASS_ID,
        "target_ids": ids,
        "source_count": len(sources),
        "sources": sources,
    }
    path = TARGET_DIR / "manifest.json"
    write_json(path, manifest)
    manifest["path"] = str(path.relative_to(ROOT)).replace("\\", "/")
    manifest["sha256"] = sha256_file(path)
    return manifest


def forum_route() -> dict[str, Any]:
    prompt = "Pass 0118: formal theorem prover source packaging receipt with parser/prover execution fenced."
    code, stdout, stderr, parsed = run_json(["forum", "route", "--json", prompt], timeout=30)
    return {
        "status": "MATCH" if code == 0 else "DRIFT",
        "exit_code": code,
        "stdout_sha256": sha256_text(stdout),
        "stderr_sha256": sha256_text(stderr),
        "decided": parsed.get("decided"),
        "confidence": parsed.get("confidence"),
        "needs_escalation": parsed.get("needs_escalation"),
        "top_candidates": parsed.get("candidates", [])[:5],
    }


def index_receipt() -> dict[str, Any]:
    code, stdout, stderr, parsed = run_json(["index", "context-envelope", "--root", ".", "--budget", "1200", "--json"], timeout=45)
    return {
        "status": "MATCH" if code == 0 and parsed.get("verification_verdict") == "MATCH" else "DRIFT",
        "exit_code": code,
        "stdout_sha256": sha256_text(stdout),
        "stderr_sha256": sha256_text(stderr),
        "schema": parsed.get("schema"),
        "verification_verdict": parsed.get("verification_verdict"),
    }


def telos_status() -> dict[str, Any]:
    code, stdout, stderr, parsed = run_json(["node", "demo/status.mjs", "--summary"], timeout=30)
    return {
        "status": "MATCH" if code == 0 and parsed.get("status") == "MATCH" else "DRIFT",
        "exit_code": code,
        "stdout_sha256": sha256_text(stdout),
        "stderr_sha256": sha256_text(stderr),
        "tool_version": parsed.get("tool_version"),
        "tool": parsed.get("tool"),
    }


def telos_catalog() -> dict[str, Any]:
    code, stdout, stderr, _parsed = run_json(["node", "demo/catalog.mjs", "--summary"], timeout=30)
    return {
        "status": "MATCH" if code == 0 and "Project Telos MCP Catalog" in stdout else "DRIFT",
        "exit_code": code,
        "stdout_sha256": sha256_text(stdout),
        "stderr_sha256": sha256_text(stderr),
        "summary_detected": "Project Telos MCP Catalog" in stdout,
    }


def compose() -> dict[str, Any]:
    adapter = read_json(ADAPTER)
    ids = adapter_target_ids(adapter)
    avail = availability()
    sources = emit_sources(ids, avail)
    manifest = write_manifest(sources, ids)
    artifact: dict[str, Any] = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "generated_on": "2026-07-01",
        "status": STATUS_DRIFT,
        "source_bindings": {"theorem_prover_adapter_pass": adapter["pass"], "adapter_artifact_seal": adapter["seal"]},
        "availability": avail,
        "target_ids": ids,
        "source_targets": sources,
        "manifest": manifest,
        "execution_boundary": "Generated formal source files were emitted and hashed, but no Lean/Rocq/Isabelle/Agda parser or prover was executed in this pass.",
        "negative_fixtures": [{"fixture_id": "missing_associativity_source_target", "expected_status": "REJECT", "reject_reason": "source_file_must_contain_all_adapter_target_ids"}],
        "market_gap_hypothesis": "A proof packet needs source-level prover targets, execution receipts, replay witnesses, and negative fixtures in one portable object; pass 0118 only implements the source packaging slice.",
        "unsupported_claim_count": 0,
        "current_promoted_natural_laws": [],
        "flagship_receipts": {"forum": forum_route(), "index": index_receipt(), "telos": telos_status(), "telos_catalog": telos_catalog()},
    }
    errors = []
    if any(row["status"] != "SOURCE_EMITTED_NOT_EXECUTED" for row in sources):
        errors.append("source_targets")
    if any(row["execution_status"] != "NOT_EXECUTED" for row in sources):
        errors.append("execution_boundary")
    if manifest["source_count"] != 4:
        errors.append("manifest_source_count")
    if any(row.get("status") != "MATCH" for row in artifact["flagship_receipts"].values()):
        errors.append("flagships")
    artifact["validation_errors"] = errors
    artifact["status"] = STATUS_MATCH if not errors else STATUS_DRIFT
    artifact["measurements"] = [{"id": row["language"], "status": row["status"], "sha256": row["sha256"]} for row in sources]
    unsealed = dict(artifact)
    artifact["seal"] = sha256_obj(unsealed)
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(ROOT / "schemas" / "formal-target-packaging-receipt-pass-0118.json"))
    args = parser.parse_args()
    artifact = compose()
    write_json(Path(args.out), artifact)
    print(json.dumps({"path": args.out, "seal": artifact["seal"], "status": artifact["status"]}, indent=2, sort_keys=True))
    if artifact["status"] != STATUS_MATCH:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
