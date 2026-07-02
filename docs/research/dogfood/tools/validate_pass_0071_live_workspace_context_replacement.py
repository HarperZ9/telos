"""Validate pass 0071 live workspace-context replacement."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "live-workspace-context-replacement-pass-0071.json"
RESULT = ROOT / "schemas" / "pass-0071-live-workspace-context-replacement-validator-result.json"
REQUIRED_CLASSES = {"source_intake", "workspace_context", "routing", "verification", "continuity", "action"}


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def sha256_obj(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def validate() -> dict:
    artifact = read_json(ARTIFACT)
    errors: list[str] = []
    unsealed = dict(artifact)
    seal = unsealed.pop("seal", None)
    components = artifact.get("component_receipts", [])
    workspace_rows = [row for row in components if row.get("kind") == "workspace_context"]
    action_rows = [row for row in components if row.get("kind") == "action"]
    packet = artifact.get("product_packet", {})
    live = artifact.get("live_surface", {})
    summary = live.get("summary", {})
    if artifact.get("schema") != "LiveWorkspaceContextReplacement/v1":
        errors.append("schema")
    if artifact.get("status") != "LIVE_WORKSPACE_CONTEXT_REPLACEMENT_MATCH":
        errors.append("status")
    if seal != sha256_obj(unsealed):
        errors.append("seal")
    if live.get("status") != "MATCH" or summary.get("schema") != "project-telos.context-envelope/v1":
        errors.append("live_surface")
    if summary.get("verification_verdict") != "MATCH":
        errors.append("verification_verdict")
    if artifact.get("index_surface_checks", {}).get("drift") != 0:
        errors.append("index_surface_checks")
    if {row.get("kind") for row in components} != REQUIRED_CLASSES:
        errors.append("required_classes")
    if len(workspace_rows) != 1 or not workspace_rows[0].get("component_id", "").startswith("index.context-envelope.live"):
        errors.append("live_workspace_component")
    if len(action_rows) != 1 or not action_rows[0].get("component_id", "").startswith("telos.action.receipt.live"):
        errors.append("live_action_component")
    if packet.get("component_count") != 6:
        errors.append("component_count")
    if packet.get("unsupported_claim_count") != 0 or artifact.get("unsupported_claim_count") != 0:
        errors.append("unsupported_claim_count")
    if packet.get("raw_private_payload_required") or packet.get("model_reasoning_required_for_replay"):
        errors.append("replay_boundary")
    if len(artifact.get("negative_fixtures", [])) < 7:
        errors.append("negative_fixture_count")
    for item in artifact.get("negative_fixtures", []):
        if item.get("expected_status") != "REJECT" or not item.get("reject_reason"):
            errors.append(f"negative_fixture:{item.get('fixture_id')}")
    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0071LiveWorkspaceContextReplacementValidatorRun/v1",
        "pass": "0071",
        "status": status,
        "match": 1 if status == "MATCH" else 0,
        "drift": 0 if status == "MATCH" else 1,
        "checks": [{
            "artifact": "LiveWorkspaceContextReplacement",
            "component_count": len(components),
            "errors": errors,
            "index_surface_status": live.get("status"),
            "negative_fixture_count": len(artifact.get("negative_fixtures", [])),
            "path": "schemas/live-workspace-context-replacement-pass-0071.json",
            "status": status,
        }],
    }


def main() -> None:
    result = validate()
    write_json(RESULT, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
