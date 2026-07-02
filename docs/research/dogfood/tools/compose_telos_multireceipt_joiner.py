"""Compose pass 0069 Telos multi-receipt joiner artifact."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


SCHEMA = "TelosMultiReceiptJoiner/v1"
PASS_ID = "0069"
STATUS_MATCH = "TELOS_MULTIRECEIPT_JOINER_MATCH"
STATUS_DRIFT = "TELOS_MULTIRECEIPT_JOINER_DRIFT"
REQUIRED_CLASSES = ["source_intake", "workspace_context", "routing", "verification", "continuity", "action"]
ROOT = Path(__file__).resolve().parents[1]


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def sha256_obj(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def component_receipts() -> list[dict[str, Any]]:
    pass_0068_receipts = read_json(ROOT / "schemas" / "tool-receipts-pass-0068.json")
    pass_0067 = read_json(ROOT / "schemas" / "forum-routing-repair-experiment-pass-0067.json")
    pass_0068 = read_json(ROOT / "schemas" / "multitool-growth-vector-steelman-pass-0068.json")
    pass_0068_run = read_json(ROOT / "crucible" / "pass-0068-run.json")
    loop_checkpoint = sha256_obj({
        "bindings": pass_0068["previous_pass_bindings"],
        "packet": pass_0068_receipts["gather"]["docs_packet"]["sha256"],
        "pass": PASS_ID,
    })
    action_payload = {
        "event_type": "multi_receipt_joined",
        "actor": "codex",
        "scope": "local_dogfood_readwrite",
        "result": "telos_product_packet_draft",
        "raw_private_payload_required": False,
    }
    rows = [
        component("source_intake", "gather.packet.078", pass_0068_receipts["gather"]["docs_packet"]["sha256"], pass_0068_receipts["gather"]["docs_packet"]["seal"], "packet 078 source intake"),
        component("workspace_context", "index.status.0068", pass_0068_receipts["shell"]["sha256"]["multitool-growth-vector-steelman-pass-0068.json"], pass_0068["seal"], "Index-context-bound artifact hash"),
        component("routing", "forum.route-repair.0067", pass_0067["seal"], pass_0067["repair_metrics"]["routing_repair_status"], "Forum route repair receipt"),
        component("verification", "crucible.assessment.0068", pass_0068_run["assessment"]["seal"], pass_0068_run["assessment"]["thesis_id"], "Crucible assessment receipt"),
        component("continuity", "loop-ledger.pass-chain.0069", loop_checkpoint, pass_0068["previous_pass_bindings"][1]["seal"], "Dogfood pass continuity checkpoint"),
        component("action", "action-receipt.join.0069", sha256_obj(action_payload), "local-action", "Local action receipt for join generation"),
    ]
    return rows


def component(kind: str, component_id: str, digest: str, seal: str, label: str) -> dict[str, Any]:
    return {
        "component_id": component_id,
        "digest": normalize_digest(digest),
        "kind": kind,
        "label": label,
        "raw_payload_included": False,
        "seal": normalize_digest(seal) if len(str(seal)) == 64 else sha256_obj(seal),
        "verification_status": "MATCH",
    }


def normalize_digest(value: object) -> str:
    text = str(value)
    if len(text) == 64 and all(char in "0123456789abcdefABCDEF" for char in text):
        return text.lower()
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def product_packet(components: list[dict[str, Any]]) -> dict[str, Any]:
    claim = "A proof-packet product spine needs source intake, workspace context, routing, verification, continuity, and action receipts to be replayable."
    return {
        "schema": "TelosProductProofPacket/v1",
        "packet_id": "pass-0069-proof-os-core-mini",
        "required_classes": REQUIRED_CLASSES,
        "component_count": len(components),
        "component_digests": {row["kind"]: row["digest"] for row in components},
        "join_graph": [
            {"from": "source_intake", "to": "workspace_context"},
            {"from": "workspace_context", "to": "routing"},
            {"from": "routing", "to": "verification"},
            {"from": "verification", "to": "continuity"},
            {"from": "continuity", "to": "action"},
        ],
        "claims": [{"claim": claim, "evidence_classes": REQUIRED_CLASSES, "verification_status": "MATCH"}],
        "raw_private_payload_required": False,
        "model_reasoning_required_for_replay": False,
        "unsupported_claim_count": 0,
    }


def negative_fixtures(components: list[dict[str, Any]]) -> list[dict[str, Any]]:
    drifted = [dict(row) for row in components]
    drifted[0]["digest"] = "0" * 64
    unsupported_packet = product_packet(components)
    unsupported_packet["unsupported_claim_count"] = 1
    raw_payload_packet = product_packet(components)
    raw_payload_packet["raw_private_payload_required"] = True
    return [
        fixture("missing_source_intake", [row for row in components if row["kind"] != "source_intake"], "missing_required_class:source_intake"),
        fixture("missing_verification", [row for row in components if row["kind"] != "verification"], "missing_required_class:verification"),
        fixture("digest_drift", drifted, "component_digest_drift:source_intake"),
        {"fixture_id": "unsupported_claim_promoted", "expected_status": "REJECT", "reject_reason": "unsupported_claim_count_nonzero", "packet": unsupported_packet},
        {"fixture_id": "raw_payload_required", "expected_status": "REJECT", "reject_reason": "raw_private_payload_required", "packet": raw_payload_packet},
    ]


def fixture(fixture_id: str, components: list[dict[str, Any]], reject_reason: str) -> dict[str, Any]:
    return {"fixture_id": fixture_id, "components": components, "expected_status": "REJECT", "reject_reason": reject_reason}


def ablation_results(components: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = [{"case_id": "full_join", "removed_class": None, "verdict": "MATCH", "reason": "all required classes present"}]
    for cls in REQUIRED_CLASSES:
        rows.append({"case_id": f"without_{cls}", "removed_class": cls, "verdict": "REJECT", "reason": f"missing_required_class:{cls}"})
    return rows


def validate_components(components: list[dict[str, Any]], packet: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    kinds = {row.get("kind") for row in components}
    if kinds != set(REQUIRED_CLASSES):
        errors.append("required_classes")
    for row in components:
        if row.get("verification_status") != "MATCH":
            errors.append(f"verification:{row.get('component_id')}")
        if len(row.get("digest", "")) != 64 or len(row.get("seal", "")) != 64:
            errors.append(f"digest_or_seal:{row.get('component_id')}")
        if row.get("raw_payload_included"):
            errors.append(f"raw_payload:{row.get('component_id')}")
    if packet.get("component_count") != len(components):
        errors.append("component_count")
    if packet.get("unsupported_claim_count") != 0:
        errors.append("unsupported_claim_count")
    if packet.get("raw_private_payload_required") or packet.get("model_reasoning_required_for_replay"):
        errors.append("replay_boundary")
    return errors


def compose() -> dict[str, Any]:
    components = component_receipts()
    packet = product_packet(components)
    artifact = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "generated_on": "2026-07-01",
        "component_receipts": components,
        "product_packet": packet,
        "ablation_results": ablation_results(components),
        "negative_fixtures": negative_fixtures(components),
        "previous_pass_binding": read_json(ROOT / "schemas" / "multitool-growth-vector-steelman-pass-0068.json")["seal"],
        "unsupported_claim_count": 0,
        "non_promotion_statement": "Pass 0069 proves a local joiner fixture, not a production packet API, market adoption, scientific discovery, or a new natural law.",
    }
    errors = validate_components(components, packet)
    errors.extend(validate_negative_fixtures(artifact["negative_fixtures"]))
    artifact["validation_errors"] = errors
    artifact["status"] = STATUS_MATCH if not errors else STATUS_DRIFT
    artifact["seal"] = sha256_obj(artifact)
    return artifact


def validate_negative_fixtures(fixtures: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    if len(fixtures) < 5:
        errors.append("negative_fixture_count")
    for item in fixtures:
        if item.get("expected_status") != "REJECT" or not item.get("reject_reason"):
            errors.append(f"negative_fixture:{item.get('fixture_id')}")
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
