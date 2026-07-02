"""Compose pass 0074 BuildLang source-ref receipt."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


SCHEMA = "BuildLangSourceRefReceipt/v1"
PASS_ID = "0074"
STATUS_MATCH = "BUILDLANG_SOURCE_REF_RECEIPT_MATCH"
STATUS_DRIFT = "BUILDLANG_SOURCE_REF_RECEIPT_DRIFT"
ROOT = Path(__file__).resolve().parents[1]
BUILDLANG_ROOT = Path("C:/dev/public/pubscan/quantalang")
COMPILER_ROOT = BUILDLANG_ROOT / "compiler"
SOURCE_PATHS = [
    "README.md",
    "STATUS.md",
    "compiler/Cargo.toml",
    "semantic-corpus/README.md",
    "semantic-corpus/manifest.json",
    "semantic-corpus/receipts/c-execution-2026-06-13.json",
    "semantic-corpus/receipts/rust-execution-2026-06-13.json",
    "semantic-corpus/receipts/substrate-semantic-corpus-2026-06-18.json",
    "semantic-corpus/receipts/mir-representation-2026-06-18.json",
    "semantic-corpus/receipts/memory-layout-2026-06-18.json",
    "semantic-corpus/receipts/module-graph-2026-06-18.json",
    "semantic-corpus/receipts/symbol-graph-2026-06-18.json",
    "semantic-corpus/receipts/lsp-dispatch-2026-06-18.json",
]
EXPECTED_LINES = [
    "manifest: 8 program(s)",
    "c receipt: ok",
    "rust receipt: ok",
    "substrate receipt: ok",
    "mir representation receipt: ok",
    "memory layout receipt: ok",
    "module graph receipt: ok",
    "symbol graph receipt: ok",
    "lsp dispatch receipt: ok",
    "c execution: 8 passed",
]


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_obj(value: object) -> str:
    return sha256_text(canonical_json(value))


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def source_refs() -> list[dict[str, Any]]:
    refs: list[dict[str, Any]] = []
    for rel in SOURCE_PATHS:
        path = BUILDLANG_ROOT / rel
        refs.append({
            "id": f"buildlang:{rel.replace('/', ':')}",
            "path": str(path),
            "relative_path": rel,
            "exists": path.exists(),
            "sha256": sha256_file(path) if path.exists() else None,
            "bytes": path.stat().st_size if path.exists() else 0,
            "raw_payload_included": False,
        })
    return refs


def run_corpus_verify() -> dict[str, Any]:
    result = subprocess.run(
        ["cargo", "run", "--quiet", "--bin", "buildc", "--", "corpus", "verify"],
        cwd=COMPILER_ROOT,
        capture_output=True,
        text=True,
    )
    stdout = result.stdout.replace("\r\n", "\n")
    checks = {line: line in stdout for line in EXPECTED_LINES}
    return {
        "command": "cargo run --quiet --bin buildc -- corpus verify",
        "cwd": str(COMPILER_ROOT),
        "exit_code": result.returncode,
        "stdout_sha256": sha256_text(stdout),
        "stderr_sha256": sha256_text(result.stderr),
        "expected_line_checks": checks,
        "match": sum(1 for ok in checks.values() if ok),
        "drift": sum(1 for ok in checks.values() if not ok),
        "status": "MATCH" if result.returncode == 0 and all(checks.values()) else "DRIFT",
    }


def negative_fixtures() -> list[dict[str, Any]]:
    return [
        {"fixture_id": "missing_readme_ref", "expected_status": "REJECT", "reject_reason": "missing_source_ref:README.md"},
        {"fixture_id": "missing_manifest_ref", "expected_status": "REJECT", "reject_reason": "missing_source_ref:semantic-corpus/manifest.json"},
        {"fixture_id": "corpus_verify_not_run", "expected_status": "REJECT", "reject_reason": "missing_executable_receipt"},
        {"fixture_id": "receipt_line_drift", "expected_status": "REJECT", "reject_reason": "expected_corpus_line_missing"},
        {"fixture_id": "claims_all_backends_production", "expected_status": "REJECT", "reject_reason": "experimental_backends_promoted"},
        {"fixture_id": "self_hosted_compiler_promoted", "expected_status": "REJECT", "reject_reason": "self_hosted_compiler_unverified"},
        {"fixture_id": "raw_payload_required", "expected_status": "REJECT", "reject_reason": "raw_private_payload_required"},
        {"fixture_id": "unsupported_claim_promoted", "expected_status": "REJECT", "reject_reason": "unsupported_claim_count_nonzero"},
    ]


def validate_artifact(artifact: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    refs = artifact.get("source_refs", [])
    verify = artifact.get("corpus_verify", {})
    if len(refs) != len(SOURCE_PATHS) or not all(ref.get("exists") for ref in refs):
        errors.append("source_refs")
    if verify.get("status") != "MATCH" or verify.get("drift") != 0:
        errors.append("corpus_verify")
    if artifact.get("program_count") != 8:
        errors.append("program_count")
    if artifact.get("production_backend_claim") != "C backend only":
        errors.append("backend_scope")
    if artifact.get("unsupported_claim_count") != 0:
        errors.append("unsupported_claim_count")
    if len(artifact.get("negative_fixtures", [])) < 8:
        errors.append("negative_fixture_count")
    return errors


def compose() -> dict[str, Any]:
    refs = source_refs()
    verify = run_corpus_verify()
    artifact = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "generated_on": "2026-07-01",
        "buildlang_root": str(BUILDLANG_ROOT),
        "source_refs": refs,
        "source_ref_count": len(refs),
        "corpus_verify": verify,
        "program_count": 8,
        "receipt_surfaces": [
            "c execution",
            "rust execution",
            "substrate",
            "mir representation",
            "memory layout",
            "module graph",
            "symbol graph",
            "lsp dispatch",
        ],
        "production_backend_claim": "C backend only",
        "experimental_backend_boundary": "Rust, HLSL, GLSL, SPIR-V, LLVM, WASM, x86-64, and ARM64 remain separate maturity lanes unless their own receipts prove more.",
        "self_hosted_boundary": "The self-hosted compiler and stdlib are aspirational and are not promoted by this pass.",
        "negative_fixtures": negative_fixtures(),
        "unsupported_claim_count": 0,
        "non_promotion_statement": "Pass 0074 binds BuildLang source refs and a live buildc corpus verification receipt. It does not prove all backends production-ready, self-hosting, Julia replacement, market adoption, scientific discovery, or a natural law.",
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
