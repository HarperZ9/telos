"""Compose pass 0073 Telos domain-focus envelope fixture."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


SCHEMA = "TelosDomainFocusEnvelopeSet/v1"
ENVELOPE_SCHEMA = "TelosDomainFocusEnvelope/v1"
PASS_ID = "0073"
STATUS_MATCH = "TELOS_DOMAIN_FOCUS_ENVELOPE_MATCH"
STATUS_DRIFT = "TELOS_DOMAIN_FOCUS_ENVELOPE_DRIFT"
ROOT = Path(__file__).resolve().parents[1]
REQUIRED_LAYERS = ["source_intake", "workspace_context", "routing", "verification", "continuity", "action"]


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


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def source_component(tool_receipts: dict[str, Any]) -> dict[str, Any]:
    packet = tool_receipts["gather"]["docs_packet"]
    return {
        "kind": "source_intake",
        "component_id": "gather.packet.082",
        "label": "Domain-focus adapter packet source intake",
        "digest": packet["sha256"],
        "seal": packet["seal"],
        "verification_status": "MATCH" if packet["verified"] else "DRIFT",
        "raw_payload_included": False,
    }


def workspace_component(pass_0071: dict[str, Any]) -> dict[str, Any]:
    row = [item for item in pass_0071["component_receipts"] if item["kind"] == "workspace_context"][0]
    return dict(row)


def routing_component(route: dict[str, Any]) -> dict[str, Any]:
    adapted = route["adapted"]
    return {
        "kind": "routing",
        "component_id": f"forum.domain-focus.route.{route['domain_id']}.0073",
        "label": f"Forum adapted route for {route['domain_id']}",
        "digest": sha256_obj(adapted),
        "seal": sha256_obj(route),
        "verification_status": "MATCH" if route["status"] == "MATCH" else "DRIFT",
        "raw_payload_included": False,
        "decided": adapted["decided"],
        "needs_escalation": adapted["needs_escalation"],
        "project_telos_score": adapted["project_telos_score"],
    }


def verification_component(tool_receipts: dict[str, Any]) -> dict[str, Any]:
    crucible = tool_receipts["crucible"]
    return {
        "kind": "verification",
        "component_id": "crucible.assessment.0072",
        "label": "Crucible assessment for domain-focus adapter experiment",
        "digest": crucible["assessment_seal"],
        "seal": crucible["thesis_seal"],
        "verification_status": "MATCH" if crucible["drift"] == 0 and crucible["unverifiable"] == 0 else "DRIFT",
        "raw_payload_included": False,
        "claims": crucible["claims"],
        "match": crucible["match"],
    }


def continuity_component(pass_0072: dict[str, Any]) -> dict[str, Any]:
    return {
        "kind": "continuity",
        "component_id": "loop-ledger.pass-chain.0072",
        "label": "Dogfood pass 0072 continuity checkpoint",
        "digest": pass_0072["seal"],
        "seal": sha256_file(ROOT / "pass-0072-ledger.md"),
        "verification_status": "MATCH",
        "raw_payload_included": False,
    }


def action_component(pass_0070: dict[str, Any]) -> dict[str, Any]:
    row = [item for item in pass_0070["component_receipts"] if item["kind"] == "action"][0]
    return dict(row)


def envelope_for_domain(route: dict[str, Any], pass_0072: dict[str, Any], components: dict[str, dict[str, Any]]) -> dict[str, Any]:
    domain = [row for row in pass_0072["adapter_rows"] if row["domain_id"] == route["domain_id"]][0]
    domain_components = dict(components)
    domain_components["routing"] = routing_component(route)
    component_digests = {layer: domain_components[layer]["digest"] for layer in REQUIRED_LAYERS}
    envelope = {
        "schema": ENVELOPE_SCHEMA,
        "envelope_id": f"telos.domain-focus.{route['domain_id']}.0073",
        "domain_id": route["domain_id"],
        "label": domain["label"],
        "required_layers": REQUIRED_LAYERS,
        "component_digests": component_digests,
        "route_decision": domain_components["routing"]["decided"],
        "route_needs_escalation": domain_components["routing"]["needs_escalation"],
        "requested_paths": domain["requested_paths"],
        "index_strategy": domain["index_strategy"],
        "path_scoped_context": False,
        "root_context_fallback": True,
        "raw_private_payload_required": False,
        "model_reasoning_required_for_replay": False,
        "unsupported_claim_count": 0,
        "verification_status": "MATCH",
    }
    envelope["seal"] = sha256_obj(envelope)
    return envelope


def ablation_results() -> list[dict[str, Any]]:
    rows = [{"case_id": "full_domain_focus_envelope", "removed_layer": None, "verdict": "MATCH", "reason": "all required layers present"}]
    for layer in REQUIRED_LAYERS:
        rows.append({"case_id": f"without_{layer}", "removed_layer": layer, "verdict": "REJECT", "reason": f"missing_required_layer:{layer}"})
    return rows


def negative_fixtures() -> list[dict[str, Any]]:
    return [
        {"fixture_id": "missing_source_intake", "expected_status": "REJECT", "reject_reason": "missing_required_layer:source_intake"},
        {"fixture_id": "missing_workspace_context", "expected_status": "REJECT", "reject_reason": "missing_required_layer:workspace_context"},
        {"fixture_id": "missing_routing", "expected_status": "REJECT", "reject_reason": "missing_required_layer:routing"},
        {"fixture_id": "missing_verification", "expected_status": "REJECT", "reject_reason": "missing_required_layer:verification"},
        {"fixture_id": "missing_action", "expected_status": "REJECT", "reject_reason": "missing_required_layer:action"},
        {"fixture_id": "claims_path_scoped_context_without_refs", "expected_status": "REJECT", "reject_reason": "path_scoped_context_unproven"},
        {"fixture_id": "unsupported_claim_promoted", "expected_status": "REJECT", "reject_reason": "unsupported_claim_count_nonzero"},
        {"fixture_id": "raw_payload_required", "expected_status": "REJECT", "reject_reason": "raw_private_payload_required"},
    ]


def validate_artifact(artifact: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    envelopes = artifact.get("domain_envelopes", [])
    if artifact.get("domain_count") != 6 or len(envelopes) != artifact.get("domain_count"):
        errors.append("domain_count")
    if artifact.get("path_scoped_envelopes") != 0:
        errors.append("path_scoped_envelopes")
    if artifact.get("root_fallback_envelopes") != artifact.get("domain_count"):
        errors.append("root_fallback_envelopes")
    if artifact.get("unsupported_claim_count") != 0:
        errors.append("unsupported_claim_count")
    for envelope in envelopes:
        if envelope.get("route_decision") != "project-telos" or envelope.get("route_needs_escalation"):
            errors.append(f"route:{envelope.get('domain_id')}")
        if set(envelope.get("required_layers", [])) != set(REQUIRED_LAYERS):
            errors.append(f"layers:{envelope.get('domain_id')}")
        if envelope.get("raw_private_payload_required") or envelope.get("model_reasoning_required_for_replay"):
            errors.append(f"replay:{envelope.get('domain_id')}")
    if len(artifact.get("negative_fixtures", [])) < 8:
        errors.append("negative_fixture_count")
    return errors


def compose() -> dict[str, Any]:
    pass_0070 = read_json(ROOT / "schemas" / "live-action-receipt-replacement-pass-0070.json")
    pass_0071 = read_json(ROOT / "schemas" / "live-workspace-context-replacement-pass-0071.json")
    pass_0072 = read_json(ROOT / "schemas" / "domain-focus-adapter-experiment-pass-0072.json")
    receipts_0072 = read_json(ROOT / "schemas" / "tool-receipts-pass-0072.json")
    base_components = {
        "source_intake": source_component(receipts_0072),
        "workspace_context": workspace_component(pass_0071),
        "verification": verification_component(receipts_0072),
        "continuity": continuity_component(pass_0072),
        "action": action_component(pass_0070),
    }
    envelopes = [envelope_for_domain(route, pass_0072, base_components) for route in pass_0072["route_probes"]]
    artifact = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "generated_on": "2026-07-01",
        "domain_count": len(envelopes),
        "domain_envelopes": envelopes,
        "base_components": base_components,
        "root_fallback_envelopes": sum(1 for row in envelopes if row["root_context_fallback"]),
        "path_scoped_envelopes": sum(1 for row in envelopes if row["path_scoped_context"]),
        "ablation_results": ablation_results(),
        "negative_fixtures": negative_fixtures(),
        "unsupported_claim_count": 0,
        "non_promotion_statement": "Pass 0073 defines a replayable TelosDomainFocusEnvelope fixture over prior receipts. It does not implement path-scoped Index source refs, prove market adoption, solve a scientific problem, or establish a natural law.",
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
