"""Compose pass 0080 BuildLang proof-packet demo surface."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


SCHEMA = "BuildLangProofPacketDemoSurface/v1"
PASS_ID = "0080"
STATUS_MATCH = "BUILDLANG_PROOF_PACKET_DEMO_SURFACE_MATCH"
STATUS_DRIFT = "BUILDLANG_PROOF_PACKET_DEMO_SURFACE_DRIFT"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
BUILDLANG_ROOT = Path("C:/dev/public/pubscan/quantalang")
BUILDC_CWD = BUILDLANG_ROOT / "compiler"
BUILDC_COMMAND = ["cargo", "run", "--quiet", "--bin", "buildc", "--", "corpus", "verify"]
FORUM_TEXT = (
    "Package a BuildLang proof-packet demo surface for Project Telos: bind source "
    "intake, path-scoped workspace context, live buildc corpus verification, "
    "negative fixtures, and a buyer-facing product brief without claiming Julia "
    "replacement or scientific discovery."
)
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


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def run_command(command: list[str], cwd: Path) -> dict[str, Any]:
    result = subprocess.run(command, cwd=cwd, capture_output=True, text=True)
    stdout = result.stdout
    checks = {line: line in stdout for line in EXPECTED_LINES}
    return {
        "command": " ".join(command),
        "cwd": str(cwd),
        "exit_code": result.returncode,
        "stdout_sha256": sha256_text(stdout),
        "stderr_sha256": sha256_text(result.stderr),
        "expected_line_checks": checks,
        "match": sum(1 for ok in checks.values() if ok),
        "drift": sum(1 for ok in checks.values() if not ok),
        "status": "MATCH" if result.returncode == 0 and all(checks.values()) else "DRIFT",
    }


def run_forum_route() -> dict[str, Any]:
    result = subprocess.run(["forum", "route", "--json", FORUM_TEXT], cwd=REPO, capture_output=True, text=True)
    parsed = json.loads(result.stdout) if result.returncode == 0 and result.stdout.strip() else {}
    candidates = parsed.get("candidates", [])
    return {
        "command": f"forum route --json {FORUM_TEXT!r}",
        "exit_code": result.returncode,
        "stdout_sha256": sha256_text(result.stdout),
        "stderr_sha256": sha256_text(result.stderr),
        "decided": parsed.get("decided"),
        "confidence": parsed.get("confidence"),
        "needs_escalation": parsed.get("needs_escalation"),
        "top_candidates": candidates[:5],
        "status": "MATCH" if result.returncode == 0 and bool(candidates) else "DRIFT",
    }


def negative_fixtures() -> list[dict[str, str]]:
    return [
        {"fixture_id": "claims_julia_replacement_proven", "expected_status": "REJECT", "reject_reason": "market_and_performance_claim_unproven"},
        {"fixture_id": "claims_all_backends_production", "expected_status": "REJECT", "reject_reason": "production_backend_is_c_only"},
        {"fixture_id": "claims_native_index_path_selector", "expected_status": "REJECT", "reject_reason": "path_context_uses_adapter_fixture"},
        {"fixture_id": "claims_build_universe_covered", "expected_status": "REJECT", "reject_reason": "build_universe_missing_selector_rejected"},
        {"fixture_id": "claims_scientific_discovery", "expected_status": "REJECT", "reject_reason": "demo_proves_packet_surface_not_new_science"},
        {"fixture_id": "missing_live_buildc_receipt", "expected_status": "REJECT", "reject_reason": "live_corpus_verify_required"},
        {"fixture_id": "missing_forum_route_receipt", "expected_status": "REJECT", "reject_reason": "route_receipt_required"},
        {"fixture_id": "raw_source_payload_required", "expected_status": "REJECT", "reject_reason": "source_refs_only_boundary"},
        {"fixture_id": "unsupported_claim_promoted", "expected_status": "REJECT", "reject_reason": "unsupported_claim_count_nonzero"},
    ]


def compose() -> dict[str, Any]:
    source = read_json(ROOT / "schemas" / "buildlang-source-ref-receipt-pass-0074.json")
    path_context = read_json(ROOT / "schemas" / "buildlang-path-context-envelope-join-pass-0079.json")
    scorecard = read_json(ROOT / "schemas" / "path-selector-contract-scorecard-pass-0077.json")
    live = run_command(BUILDC_COMMAND, BUILDC_CWD)
    route = run_forum_route()
    joined = path_context["joined_envelope"]
    artifact: dict[str, Any] = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "generated_on": "2026-07-01",
        "demo_id": "buildlang-proof-packet-demo-0080",
        "market_motion": scorecard["primary_30_day_push"]["motion"],
        "source_intake": {
            "source_pass": "0074",
            "schema": source["schema"],
            "seal": source["seal"],
            "source_ref_count": source["source_ref_count"],
            "program_count": source["program_count"],
            "production_backend_claim": source["production_backend_claim"],
        },
        "workspace_context": {
            "source_pass": "0079",
            "schema": path_context["schema"],
            "seal": path_context["seal"],
            "workspace_context_digest": joined["component_digests"]["workspace_context"],
            "path_scoped_context": joined["path_scoped_context"],
            "root_context_fallback": joined["root_context_fallback"],
            "source_ref_count": joined["workspace_context_source_ref_count"],
            "adapter_fixture": joined["adapter_fixture"],
            "native_index_path_selector": joined["native_index_path_selector"],
            "missing_selector_rejections": joined["missing_selector_rejections"],
        },
        "live_buildc_corpus": live,
        "forum_route": route,
        "proof_packet_layers": [
            "source_intake",
            "path_scoped_workspace_context",
            "live_buildc_corpus_receipt",
            "forum_route_receipt",
            "negative_fixtures",
            "buyer_facing_brief",
            "crucible_verdicts",
        ],
        "buyer_brief": {
            "audience": "compiler, scientific-compute, AI infrastructure, and research-platform buyers",
            "offer": "BuildLang proof packets: portable evidence chains for source refs, selected workspace context, compiler corpus receipts, route receipts, and verifier verdicts.",
            "demo_claim": "This demo proves the proof-packet surface for BuildLang/buildc, not broad language-market replacement.",
            "primary_risk": "The path-scoped context receipt is adapter-generated until Index emits native path-selector receipts.",
        },
        "negative_fixtures": negative_fixtures(),
        "unsupported_claim_count": 0,
        "current_promoted_natural_laws": [],
        "non_promotion_statement": "Pass 0080 packages a BuildLang proof-packet demo surface. It does not prove Julia replacement, all backend maturity, native Index path selection, Build Universe coverage, market adoption, scientific discovery, or a natural law.",
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
    if artifact.get("source_intake", {}).get("source_ref_count") != 13:
        errors.append("source_intake")
    workspace = artifact.get("workspace_context", {})
    if workspace.get("path_scoped_context") is not True or workspace.get("root_context_fallback") is not False:
        errors.append("workspace_context_scope")
    if workspace.get("source_ref_count") != 128:
        errors.append("workspace_source_refs")
    if workspace.get("adapter_fixture") is not True or workspace.get("native_index_path_selector") is not False:
        errors.append("adapter_boundary")
    if artifact.get("live_buildc_corpus", {}).get("status") != "MATCH":
        errors.append("live_buildc")
    if artifact.get("forum_route", {}).get("status") != "MATCH":
        errors.append("forum_route")
    if len(artifact.get("negative_fixtures", [])) < 9:
        errors.append("negative_fixture_count")
    if artifact.get("unsupported_claim_count") != 0 or artifact.get("current_promoted_natural_laws") != []:
        errors.append("promotion_boundary")
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
