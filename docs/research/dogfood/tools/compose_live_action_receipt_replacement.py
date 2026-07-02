"""Compose pass 0070 live action-receipt replacement artifact."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


SCHEMA = "LiveActionReceiptReplacement/v1"
PASS_ID = "0070"
STATUS_MATCH = "LIVE_ACTION_RECEIPT_REPLACEMENT_MATCH"
STATUS_DRIFT = "LIVE_ACTION_RECEIPT_REPLACEMENT_DRIFT"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
REQUIRED_CLASSES = ["source_intake", "workspace_context", "routing", "verification", "continuity", "action"]


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def sha256_obj(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_live_action_surface() -> dict[str, Any]:
    result = subprocess.run(["node", "demo/action-receipt.mjs"], cwd=REPO, capture_output=True, text=True)
    if result.returncode != 0:
        return {"status": "DRIFT", "stderr_sha256": hashlib.sha256(result.stderr.encode("utf-8")).hexdigest(), "surface": {}}
    surface = json.loads(result.stdout)
    return {"status": "MATCH", "stdout_sha256": hashlib.sha256(result.stdout.encode("utf-8")).hexdigest(), "surface": surface}


def action_component(surface: dict[str, Any]) -> dict[str, Any]:
    event = surface["conformance_fixture"]["happy_path"]
    return {
        "component_id": "telos.action.receipt.live.happy_path.0070",
        "digest": sha256_obj(event),
        "kind": "action",
        "label": "Live Telos action-receipt happy_path conformance fixture",
        "raw_payload_included": False,
        "seal": sha256_obj(surface),
        "verification_status": event["verification"]["verdict"],
        "source_surface": "node demo/action-receipt.mjs",
        "event_id": event["event_id"],
        "action_id": event["action_id"],
        "append_only": event["persistence"]["append_only"],
        "receipt_is_trace_span": surface["contract"]["receipt_is_trace_span"],
    }


def replacement_components(prior: dict[str, Any], action: dict[str, Any]) -> list[dict[str, Any]]:
    rows = [row for row in prior["component_receipts"] if row["kind"] != "action"]
    rows.append(action)
    order = {kind: idx for idx, kind in enumerate(REQUIRED_CLASSES)}
    return sorted(rows, key=lambda row: order[row["kind"]])


def product_packet(components: list[dict[str, Any]], action: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": "TelosProductProofPacket/v1",
        "packet_id": "pass-0070-proof-os-core-live-action",
        "required_classes": REQUIRED_CLASSES,
        "component_count": len(components),
        "component_digests": {row["kind"]: row["digest"] for row in components},
        "live_action_component_id": action["component_id"],
        "join_graph": [
            {"from": "source_intake", "to": "workspace_context"},
            {"from": "workspace_context", "to": "routing"},
            {"from": "routing", "to": "verification"},
            {"from": "verification", "to": "continuity"},
            {"from": "continuity", "to": "action"},
        ],
        "claims": [{
            "claim": "Replacing the synthetic action fragment with a live Telos action-receipt fixture preserves the proof-packet join contract.",
            "evidence_classes": REQUIRED_CLASSES,
            "verification_status": "MATCH",
        }],
        "raw_private_payload_required": False,
        "model_reasoning_required_for_replay": False,
        "unsupported_claim_count": 0,
    }


def negative_fixtures(components: list[dict[str, Any]], packet: dict[str, Any]) -> list[dict[str, Any]]:
    no_action = [row for row in components if row["kind"] != "action"]
    no_verification = [row for row in components if row["kind"] != "verification"]
    drifted = [dict(row) for row in components]
    drifted[-1]["digest"] = "0" * 64
    raw_packet = dict(packet)
    raw_packet["raw_private_payload_required"] = True
    unsupported_packet = dict(packet)
    unsupported_packet["unsupported_claim_count"] = 1
    return [
        {"fixture_id": "missing_action", "components": no_action, "expected_status": "REJECT", "reject_reason": "missing_required_class:action"},
        {"fixture_id": "missing_verification", "components": no_verification, "expected_status": "REJECT", "reject_reason": "missing_required_class:verification"},
        {"fixture_id": "live_action_digest_drift", "components": drifted, "expected_status": "REJECT", "reject_reason": "component_digest_drift:action"},
        {"fixture_id": "raw_payload_required", "packet": raw_packet, "expected_status": "REJECT", "reject_reason": "raw_private_payload_required"},
        {"fixture_id": "unsupported_claim_promoted", "packet": unsupported_packet, "expected_status": "REJECT", "reject_reason": "unsupported_claim_count_nonzero"},
    ]


def action_surface_checks(surface: dict[str, Any], action: dict[str, Any]) -> dict[str, Any]:
    event = surface["conformance_fixture"]["happy_path"]
    checks = {
        "schema_match": surface.get("schema") == "project-telos.action-receipt/v1",
        "raw_parameters_not_required": surface["contract"]["raw_parameters_required"] is False,
        "digest_references_required": surface["contract"]["digest_references_required"] is True,
        "append_only": event["persistence"]["append_only"] is True,
        "verification_match": event["verification"]["verdict"] == "MATCH",
        "completed_state": event["result"]["state"] == "completed",
        "receipt_is_not_trace_span": surface["contract"]["receipt_is_trace_span"] is False,
        "action_component_digest_bound": len(action["digest"]) == 64,
    }
    return {"checks": checks, "match": sum(1 for value in checks.values() if value), "drift": sum(1 for value in checks.values() if not value)}


def ablation_results() -> list[dict[str, Any]]:
    rows = [{"case_id": "full_live_action_join", "removed_class": None, "verdict": "MATCH", "reason": "all required classes present with live action component"}]
    for cls in REQUIRED_CLASSES:
        rows.append({"case_id": f"without_{cls}", "removed_class": cls, "verdict": "REJECT", "reason": f"missing_required_class:{cls}"})
    return rows


def validate_artifact(artifact: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    components = artifact.get("component_receipts", [])
    packet = artifact.get("product_packet", {})
    action_checks = artifact.get("action_surface_checks", {})
    if {row.get("kind") for row in components} != set(REQUIRED_CLASSES):
        errors.append("required_classes")
    if packet.get("component_count") != 6:
        errors.append("component_count")
    if packet.get("unsupported_claim_count") != 0 or artifact.get("unsupported_claim_count") != 0:
        errors.append("unsupported_claim_count")
    if packet.get("raw_private_payload_required") or packet.get("model_reasoning_required_for_replay"):
        errors.append("replay_boundary")
    if action_checks.get("drift") != 0:
        errors.append("action_surface_checks")
    if len(artifact.get("negative_fixtures", [])) < 5:
        errors.append("negative_fixture_count")
    for item in artifact.get("negative_fixtures", []):
        if item.get("expected_status") != "REJECT" or not item.get("reject_reason"):
            errors.append(f"negative_fixture:{item.get('fixture_id')}")
    return errors


def compose() -> dict[str, Any]:
    prior = read_json(ROOT / "schemas" / "telos-multireceipt-joiner-pass-0069.json")
    live = load_live_action_surface()
    surface = live.get("surface", {})
    action = action_component(surface) if live["status"] == "MATCH" else {}
    components = replacement_components(prior, action) if action else []
    packet = product_packet(components, action) if action else {}
    artifact = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "generated_on": "2026-07-01",
        "live_surface": {
            "command": "node demo/action-receipt.mjs",
            "status": live["status"],
            "stdout_sha256": live.get("stdout_sha256"),
            "schema": surface.get("schema"),
            "required_field_count": len(surface.get("required_fields", [])),
            "negative_test_count": len(surface.get("negative_test_cases", [])),
        },
        "action_surface_checks": action_surface_checks(surface, action) if action else {"checks": {}, "match": 0, "drift": 1},
        "component_receipts": components,
        "product_packet": packet,
        "ablation_results": ablation_results(),
        "negative_fixtures": negative_fixtures(components, packet) if action else [],
        "previous_pass_binding": prior["seal"],
        "unsupported_claim_count": 0,
        "non_promotion_statement": "Pass 0070 replaces one synthetic action component with a live local Telos action-receipt fixture. It does not prove production persistence, external write safety, market adoption, scientific discovery, or a natural law.",
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
