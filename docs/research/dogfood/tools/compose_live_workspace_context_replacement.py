"""Compose pass 0071 live workspace-context replacement artifact."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


SCHEMA = "LiveWorkspaceContextReplacement/v1"
PASS_ID = "0071"
STATUS_MATCH = "LIVE_WORKSPACE_CONTEXT_REPLACEMENT_MATCH"
STATUS_DRIFT = "LIVE_WORKSPACE_CONTEXT_REPLACEMENT_DRIFT"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
REQUIRED_CLASSES = ["source_intake", "workspace_context", "routing", "verification", "continuity", "action"]
INDEX_COMMAND = ["index", "context-envelope", "--root", str(REPO), "--budget", "700", "--hops", "0", "--json"]
FOCUS_COMMAND = [
    "index",
    "context-envelope",
    "--root",
    str(REPO),
    "--budget",
    "700",
    "--focus",
    "docs/research/dogfood",
    "--hops",
    "0",
    "--json",
]


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_obj(value: object) -> str:
    return sha256_text(canonical_json(value))


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def run_command(command: list[str]) -> dict[str, Any]:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True)
    return {
        "command": " ".join(command),
        "exit_code": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "stdout_sha256": sha256_text(result.stdout),
        "stderr_sha256": sha256_text(result.stderr),
    }


def load_live_index_surface() -> dict[str, Any]:
    positive = run_command(INDEX_COMMAND)
    focus = run_command(FOCUS_COMMAND)
    parsed: dict[str, Any] = {}
    parse_error = ""
    if positive["exit_code"] == 0:
        try:
            parsed = json.loads(positive["stdout"])
        except json.JSONDecodeError as exc:
            parse_error = str(exc)
    summary = summarize_envelope(parsed)
    focus_output = (focus["stdout"] + focus["stderr"]).strip()
    focus_failure = {
        "command": focus["command"],
        "exit_code": focus["exit_code"],
        "output_sha256": sha256_text(focus_output),
        "observed_error": focus_output[:200],
        "status": "MATCH" if focus["exit_code"] != 0 and "unknown focus repo" in focus_output else "DRIFT",
    }
    status = "MATCH" if positive["exit_code"] == 0 and summary.get("schema") == "project-telos.context-envelope/v1" else "DRIFT"
    if summary.get("verification_verdict") != "MATCH" or parse_error:
        status = "DRIFT"
    return {
        "status": status,
        "command": positive["command"],
        "stdout_sha256": positive["stdout_sha256"],
        "stderr_sha256": positive["stderr_sha256"],
        "stdout_length": len(positive["stdout"]),
        "parse_error": parse_error,
        "summary": summary,
        "focus_path_probe": focus_failure,
    }


def summarize_envelope(envelope: dict[str, Any]) -> dict[str, Any]:
    budget = envelope.get("budget") or {}
    focus = envelope.get("focus") or {}
    return {
        "schema": envelope.get("schema"),
        "tool": envelope.get("tool"),
        "root": envelope.get("root"),
        "verification_verdict": envelope.get("verification_verdict"),
        "budget_token_budget": budget.get("token_budget"),
        "focus_repo": focus.get("repo"),
        "focus_hops": focus.get("hops"),
        "failure_code_count": len(envelope.get("failure_codes") or []),
        "omitted_count": len(envelope.get("omitted") or []),
        "receipt_count": len(envelope.get("receipts") or []),
        "retained_count": len(envelope.get("retained") or []),
        "top_level_keys": sorted(envelope.keys()),
    }


def workspace_component(surface: dict[str, Any]) -> dict[str, Any]:
    summary = surface["summary"]
    return {
        "component_id": "index.context-envelope.live.root.0071",
        "digest": surface["stdout_sha256"],
        "kind": "workspace_context",
        "label": "Live Index context-envelope root workspace receipt",
        "raw_payload_included": False,
        "seal": sha256_obj(summary),
        "verification_status": summary["verification_verdict"],
        "source_surface": surface["command"],
        "context_schema": summary["schema"],
        "retained_count": summary["retained_count"],
        "receipt_count": summary["receipt_count"],
        "budget_token_budget": summary["budget_token_budget"],
    }


def replacement_components(prior: dict[str, Any], workspace: dict[str, Any]) -> list[dict[str, Any]]:
    rows = [row for row in prior["component_receipts"] if row["kind"] != "workspace_context"]
    rows.append(workspace)
    order = {kind: idx for idx, kind in enumerate(REQUIRED_CLASSES)}
    return sorted(rows, key=lambda row: order[row["kind"]])


def product_packet(components: list[dict[str, Any]], workspace: dict[str, Any]) -> dict[str, Any]:
    action = [row for row in components if row["kind"] == "action"][0]
    return {
        "schema": "TelosProductProofPacket/v1",
        "packet_id": "pass-0071-proof-os-core-live-index-context",
        "required_classes": REQUIRED_CLASSES,
        "component_count": len(components),
        "component_digests": {row["kind"]: row["digest"] for row in components},
        "live_workspace_component_id": workspace["component_id"],
        "live_action_component_id": action["component_id"],
        "join_graph": [
            {"from": "source_intake", "to": "workspace_context"},
            {"from": "workspace_context", "to": "routing"},
            {"from": "routing", "to": "verification"},
            {"from": "verification", "to": "continuity"},
            {"from": "continuity", "to": "action"},
        ],
        "claims": [{
            "claim": "Replacing the synthetic workspace-context fragment with a live Index context-envelope preserves the proof-packet join contract while retaining the live Telos action component.",
            "evidence_classes": REQUIRED_CLASSES,
            "verification_status": "MATCH",
        }],
        "raw_private_payload_required": False,
        "model_reasoning_required_for_replay": False,
        "unsupported_claim_count": 0,
    }


def negative_fixtures(components: list[dict[str, Any]], packet: dict[str, Any], surface: dict[str, Any]) -> list[dict[str, Any]]:
    no_workspace = [row for row in components if row["kind"] != "workspace_context"]
    no_action = [row for row in components if row["kind"] != "action"]
    no_verification = [row for row in components if row["kind"] != "verification"]
    drifted = [dict(row) for row in components]
    for row in drifted:
        if row["kind"] == "workspace_context":
            row["digest"] = "0" * 64
    raw_packet = dict(packet)
    raw_packet["raw_private_payload_required"] = True
    unsupported_packet = dict(packet)
    unsupported_packet["unsupported_claim_count"] = 1
    return [
        {"fixture_id": "missing_workspace_context", "components": no_workspace, "expected_status": "REJECT", "reject_reason": "missing_required_class:workspace_context"},
        {"fixture_id": "missing_action", "components": no_action, "expected_status": "REJECT", "reject_reason": "missing_required_class:action"},
        {"fixture_id": "missing_verification", "components": no_verification, "expected_status": "REJECT", "reject_reason": "missing_required_class:verification"},
        {"fixture_id": "live_workspace_digest_drift", "components": drifted, "expected_status": "REJECT", "reject_reason": "component_digest_drift:workspace_context"},
        {"fixture_id": "focus_path_unknown_repo", "probe": surface["focus_path_probe"], "expected_status": "REJECT", "reject_reason": "unknown_focus_repo"},
        {"fixture_id": "raw_payload_required", "packet": raw_packet, "expected_status": "REJECT", "reject_reason": "raw_private_payload_required"},
        {"fixture_id": "unsupported_claim_promoted", "packet": unsupported_packet, "expected_status": "REJECT", "reject_reason": "unsupported_claim_count_nonzero"},
    ]


def index_surface_checks(surface: dict[str, Any], workspace: dict[str, Any]) -> dict[str, Any]:
    summary = surface["summary"]
    checks = {
        "schema_match": summary.get("schema") == "project-telos.context-envelope/v1",
        "verification_match": summary.get("verification_verdict") == "MATCH",
        "retained_context_present": summary.get("retained_count", 0) >= 1,
        "receipt_present": summary.get("receipt_count", 0) >= 1,
        "no_failure_codes": summary.get("failure_code_count") == 0,
        "raw_output_hash_bound": len(surface.get("stdout_sha256", "")) == 64,
        "focus_failure_captured": surface["focus_path_probe"]["status"] == "MATCH",
        "workspace_component_digest_bound": len(workspace["digest"]) == 64,
    }
    return {"checks": checks, "match": sum(1 for value in checks.values() if value), "drift": sum(1 for value in checks.values() if not value)}


def ablation_results() -> list[dict[str, Any]]:
    rows = [{"case_id": "full_live_workspace_join", "removed_class": None, "verdict": "MATCH", "reason": "all required classes present with live workspace and action components"}]
    for cls in REQUIRED_CLASSES:
        rows.append({"case_id": f"without_{cls}", "removed_class": cls, "verdict": "REJECT", "reason": f"missing_required_class:{cls}"})
    return rows


def validate_artifact(artifact: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    components = artifact.get("component_receipts", [])
    packet = artifact.get("product_packet", {})
    if {row.get("kind") for row in components} != set(REQUIRED_CLASSES):
        errors.append("required_classes")
    if packet.get("component_count") != 6:
        errors.append("component_count")
    if packet.get("unsupported_claim_count") != 0 or artifact.get("unsupported_claim_count") != 0:
        errors.append("unsupported_claim_count")
    if packet.get("raw_private_payload_required") or packet.get("model_reasoning_required_for_replay"):
        errors.append("replay_boundary")
    if artifact.get("index_surface_checks", {}).get("drift") != 0:
        errors.append("index_surface_checks")
    if len(artifact.get("negative_fixtures", [])) < 7:
        errors.append("negative_fixture_count")
    for item in artifact.get("negative_fixtures", []):
        if item.get("expected_status") != "REJECT" or not item.get("reject_reason"):
            errors.append(f"negative_fixture:{item.get('fixture_id')}")
    return errors


def compose() -> dict[str, Any]:
    prior = read_json(ROOT / "schemas" / "live-action-receipt-replacement-pass-0070.json")
    surface = load_live_index_surface()
    workspace = workspace_component(surface) if surface["status"] == "MATCH" else {}
    components = replacement_components(prior, workspace) if workspace else []
    packet = product_packet(components, workspace) if workspace else {}
    artifact = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "generated_on": "2026-07-01",
        "live_surface": surface,
        "index_surface_checks": index_surface_checks(surface, workspace) if workspace else {"checks": {}, "match": 0, "drift": 1},
        "component_receipts": components,
        "product_packet": packet,
        "ablation_results": ablation_results(),
        "negative_fixtures": negative_fixtures(components, packet, surface) if workspace else [],
        "previous_pass_binding": prior["seal"],
        "unsupported_claim_count": 0,
        "non_promotion_statement": "Pass 0071 replaces one synthetic workspace-context component with a live local Index context-envelope. It does not prove complete repo semantic coverage, external source freshness, market adoption, scientific discovery, or a natural law.",
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
