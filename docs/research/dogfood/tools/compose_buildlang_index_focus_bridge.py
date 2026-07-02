"""Compose pass 0076 BuildLang Index focus bridge experiment."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


SCHEMA = "BuildLangIndexFocusBridge/v1"
PASS_ID = "0076"
STATUS_MATCH = "BUILDLANG_INDEX_FOCUS_BRIDGE_REQUIRED"
STATUS_DRIFT = "BUILDLANG_INDEX_FOCUS_BRIDGE_DRIFT"
ROOT = Path(__file__).resolve().parents[1]
BUILDLANG_ROOT = Path("C:/dev/public/pubscan/quantalang")
REQUESTED_PATHS = ["buildlang", "compiler", "build-universe"]


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


def run_index(args: list[str]) -> dict[str, Any]:
    command = ["index", *args]
    result = subprocess.run(command, cwd=ROOT.parents[2], capture_output=True, text=True)
    parsed: dict[str, Any] | None = None
    if result.returncode == 0 and result.stdout.strip():
        parsed = json.loads(result.stdout)
    return {
        "command": " ".join(command),
        "exit_code": result.returncode,
        "stdout_sha256": sha256_text(result.stdout),
        "stderr_sha256": sha256_text(result.stderr),
        "stdout_excerpt": result.stdout.strip()[:160],
        "stderr_excerpt": result.stderr.strip()[:160],
        "parsed": parsed,
    }


def source_ref_summary(source_ref_receipt: dict[str, Any]) -> dict[str, Any]:
    return {
        "receipt_pass": source_ref_receipt["pass"],
        "receipt_seal": source_ref_receipt["seal"],
        "source_ref_count": source_ref_receipt["source_ref_count"],
        "corpus_verify_status": source_ref_receipt["corpus_verify"]["status"],
        "program_count": source_ref_receipt["program_count"],
        "production_backend_claim": source_ref_receipt["production_backend_claim"],
    }


def summarize_root_context(envelope: dict[str, Any] | None) -> dict[str, Any]:
    if not envelope:
        return {"status": "DRIFT", "source_ref_count": 0}
    retained = envelope.get("retained", [])
    source_refs = []
    for row in retained:
        source_refs.extend(row.get("source_refs", []))
    return {
        "status": envelope.get("verification_verdict"),
        "schema": envelope.get("schema"),
        "tool": envelope.get("tool"),
        "root": envelope.get("root"),
        "graph_pack_sha256": envelope.get("recheck", {}).get("graph_pack_sha256"),
        "freshness_root_sha256": envelope.get("recheck", {}).get("freshness_root_sha256"),
        "retained_names": envelope.get("selection", {}).get("retained_names", []),
        "selected_repos": envelope.get("selection", {}).get("selected_repos"),
        "source_ref_count": len(source_refs),
        "source_ref_paths": [ref.get("path") for ref in source_refs],
        "raw_source_included": envelope.get("privacy", {}).get("raw_source_included"),
        "source_refs_only": envelope.get("privacy", {}).get("source_refs_only"),
    }


def summarize_map(index_map: dict[str, Any] | None) -> dict[str, Any]:
    if not index_map:
        return {"status": "DRIFT", "requested_path_presence": {}}
    top_level = {row.get("name"): row for row in index_map.get("top_level", [])}
    return {
        "status": "MATCH",
        "schema_version": index_map.get("schema_version"),
        "tool_version": index_map.get("tool_version"),
        "repo_count": index_map.get("repo_count"),
        "dirty_count": index_map.get("dirty_count"),
        "requested_path_presence": {
            path: {
                "present": path in top_level,
                "kind": top_level.get(path, {}).get("kind"),
                "class": top_level.get(path, {}).get("class"),
            }
            for path in REQUESTED_PATHS
        },
    }


def focus_probe_summary(probe: dict[str, Any], expected_reject: bool) -> dict[str, Any]:
    text = f"{probe.get('stdout_excerpt', '')}\n{probe.get('stderr_excerpt', '')}".lower()
    rejected = probe["exit_code"] != 0
    expected = rejected if expected_reject else probe["exit_code"] == 0
    return {
        "command": probe["command"],
        "exit_code": probe["exit_code"],
        "expected_reject": expected_reject,
        "verdict": "EXPECTED_REJECT" if expected_reject and rejected else ("MATCH" if expected else "DRIFT"),
        "diagnostic_contains_unknown": "unknown" in text,
        "stdout_sha256": probe["stdout_sha256"],
        "stderr_sha256": probe["stderr_sha256"],
        "stdout_excerpt": probe["stdout_excerpt"],
        "stderr_excerpt": probe["stderr_excerpt"],
    }


def negative_fixtures() -> list[dict[str, str]]:
    return [
        {"fixture_id": "claims_path_scoped_context_match", "expected_status": "REJECT", "reject_reason": "focus_probes_rejected"},
        {"fixture_id": "missing_root_context_envelope", "expected_status": "REJECT", "reject_reason": "root_context_required"},
        {"fixture_id": "missing_focus_probe_rejections", "expected_status": "REJECT", "reject_reason": "negative_evidence_required"},
        {"fixture_id": "claims_build_universe_top_level_present", "expected_status": "REJECT", "reject_reason": "build_universe_absent_in_index_map"},
        {"fixture_id": "missing_buildlang_source_receipt", "expected_status": "REJECT", "reject_reason": "source_ref_receipt_required"},
        {"fixture_id": "raw_private_payload_required", "expected_status": "REJECT", "reject_reason": "source_refs_only_boundary"},
        {"fixture_id": "claims_bridge_implemented_in_index", "expected_status": "REJECT", "reject_reason": "bridge_plan_not_index_feature"},
        {"fixture_id": "unsupported_claim_promoted", "expected_status": "REJECT", "reject_reason": "unsupported_claim_count_nonzero"},
    ]


def validate_artifact(artifact: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if artifact.get("schema") != SCHEMA:
        errors.append("schema")
    if artifact.get("root_context", {}).get("status") != "MATCH":
        errors.append("root_context")
    if artifact.get("root_context", {}).get("source_refs_only") is not True:
        errors.append("source_refs_only")
    if artifact.get("path_scoped_context") is not False or artifact.get("bridge_required") is not True:
        errors.append("bridge_scope")
    focus = artifact.get("focus_probes", [])
    if len(focus) < 4 or any(row.get("verdict") != "EXPECTED_REJECT" for row in focus):
        errors.append("focus_rejections")
    presence = artifact.get("index_map", {}).get("requested_path_presence", {})
    if presence.get("buildlang", {}).get("present") is not True:
        errors.append("buildlang_presence")
    if presence.get("compiler", {}).get("present") is not True:
        errors.append("compiler_presence")
    if presence.get("build-universe", {}).get("present") is not False:
        errors.append("build_universe_absence")
    if artifact.get("unsupported_claim_count") != 0:
        errors.append("unsupported_claim_count")
    if len(artifact.get("negative_fixtures", [])) < 8:
        errors.append("negative_fixture_count")
    return errors


def compose() -> dict[str, Any]:
    source_receipt = read_json(ROOT / "schemas" / "buildlang-source-ref-receipt-pass-0074.json")
    root_probe = run_index(["context-envelope", "--root", str(BUILDLANG_ROOT), "--json", "--budget", "3000"])
    map_probe = run_index(["map", "--root", str(BUILDLANG_ROOT), "--json"])
    focus_probes = [
        focus_probe_summary(run_index(["context", "--root", str(BUILDLANG_ROOT), "--json", "--focus", path]), True)
        for path in REQUESTED_PATHS
    ]
    focus_probes.append(
        focus_probe_summary(run_index(["context-envelope", "--root", str(BUILDLANG_ROOT), "--json", "--focus", "buildlang", "--budget", "3000"]), True)
    )
    artifact: dict[str, Any] = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "generated_on": "2026-07-01",
        "buildlang_root": str(BUILDLANG_ROOT),
        "requested_paths": REQUESTED_PATHS,
        "source_ref_receipt": source_ref_summary(source_receipt),
        "root_context": summarize_root_context(root_probe["parsed"]),
        "index_map": summarize_map(map_probe["parsed"]),
        "focus_probes": focus_probes,
        "path_scoped_context": False,
        "root_context_fallback": True,
        "bridge_required": True,
        "bridge_strategy": {
            "name": "index_path_selector_source_ref_bridge",
            "purpose": "Convert explicit BuildLang path selections into source-ref manifests that can be joined into Telos domain envelopes.",
            "required_capabilities": [
                "Accept filesystem path selectors under --root without treating them as repo names.",
                "Emit source refs for selected directories and files without including raw private payloads.",
                "Reject missing requested paths such as build-universe until a concrete source root exists.",
                "Carry graph-pack and freshness receipts for selected path manifests.",
            ],
        },
        "advancement_vector": "Implement path-scoped Index source-ref expansion before promoting BuildLang domain envelopes beyond root-context fallback.",
        "negative_fixtures": negative_fixtures(),
        "unsupported_claim_count": 0,
        "non_promotion_statement": "Pass 0076 proves a bridge requirement, not a completed Index feature. It does not prove path-scoped context, Build Universe source coverage, market adoption, scientific discovery, or a natural law.",
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
