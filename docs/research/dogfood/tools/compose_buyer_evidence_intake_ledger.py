"""Compose pass 0061 buyer evidence intake ledger."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


SCHEMA = "BuyerEvidenceIntakeLedger/v1"
STATUS_MATCH = "BUYER_EVIDENCE_INTAKE_LEDGER_MATCH"
STATUS_DRIFT = "BUYER_EVIDENCE_INTAKE_LEDGER_DRIFT"
LANES = ["project-telos", "deep-research", "technical-writing"]
PRIVATE_FIELDS = [
    "contact_name",
    "contact_email",
    "phone_number",
    "private_organization_name",
    "private_calendar_link",
    "private_document_url",
    "private_slack_or_chat_handle",
]


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_obj(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def evidence_field(source: dict[str, Any], buyer_id: str) -> dict[str, Any]:
    field_id = source["field_id"]
    return {
        "capture_status": "pending_real_buyer_input",
        "evidence_hash": None,
        "evidence_ref": f"operator-local/{buyer_id}/{field_id}",
        "field_id": field_id,
        "label": source["label"],
        "model_context_value": "pending_redacted_summary",
        "required": source["required"],
        "verification_status": "unverified",
    }


def gates(buyer_id: str) -> list[str]:
    return [
        f"{buyer_id}: buyer role must be named as a role category, not as a private person.",
        f"{buyer_id}: budget path must be supported by buyer statement or operator-local evidence.",
        f"{buyer_id}: incumbent stack must include at least one tool, workflow, or manual process.",
        f"{buyer_id}: proof gap must name a source, action, verification, replay, or audit object.",
        f"{buyer_id}: acceptance criterion must be measurable and demo-bound.",
        f"{buyer_id}: negative disqualifier must be specific enough to stop the pilot.",
    ]


def falsifiers(buyer_id: str) -> list[str]:
    return [
        f"{buyer_id}: no buyer role or authority path can be identified.",
        f"{buyer_id}: buyer cannot name an incumbent workflow or proof gap.",
        f"{buyer_id}: requested outcome requires unsupported market, science, production, or uniqueness claims.",
        f"{buyer_id}: buyer evidence cannot be redacted into model-safe fields.",
    ]


def score_dimensions() -> list[dict[str, str]]:
    return [
        {"dimension": "urgency", "status": "UNSCORED", "requires": "real buyer pain statement"},
        {"dimension": "budget", "status": "UNSCORED", "requires": "budget path or explicit no-budget evidence"},
        {"dimension": "incumbent_gap", "status": "UNSCORED", "requires": "current stack and proof gap evidence"},
        {"dimension": "pilot_fit", "status": "UNSCORED", "requires": "measurable acceptance criterion"},
        {"dimension": "adoption_friction", "status": "UNSCORED", "requires": "security, privacy, integration, or procurement constraint"},
    ]


def intake_record(packet: dict[str, Any]) -> dict[str, Any]:
    buyer_id = packet["buyer_id"]
    fields = [evidence_field(field, buyer_id) for field in packet["evidence_intake_fields"]]
    return {
        "buyer_id": buyer_id,
        "counterparty_seed_id": packet["counterparty_seed"]["id"],
        "evidence_capture_fields": fields,
        "evidence_quality_gates": gates(buyer_id),
        "falsifiers": falsifiers(buyer_id),
        "model_boundary_allowed_fields": [
            "buyer_role_category",
            "sector",
            "workflow_pain_summary",
            "incumbent_stack_summary",
            "proof_gap_summary",
            "acceptance_criterion_summary",
            "negative_disqualifier_summary",
            "verification_status",
        ],
        "operator_local_only_fields": [
            "raw_buyer_notes",
            "raw_call_transcript",
            "raw_email_thread",
            "private_org_name",
            "private_contact_details",
            "private_procurement_documents",
        ],
        "private_fields_forbidden_in_model_context": PRIVATE_FIELDS,
        "privacy_boundary": "NO_PRIVATE_CONTACT_DATA_IN_MODEL_CONTEXT",
        "response_status": "AWAITING_REAL_RESPONSE",
        "route_lane_split": LANES,
        "score_dimensions": score_dimensions(),
        "score_status": "UNSCORED_PENDING_BUYER_EVIDENCE",
        "source_payload_ref": packet["payload_ref"],
    }


def compose(outreach_path: Path) -> dict[str, Any]:
    outreach = read_json(outreach_path)
    records = [intake_record(packet) for packet in outreach["outreach_packets"]]
    ledger = {
        "schema": SCHEMA,
        "buyer_response_status": "AWAITING_REAL_RESPONSES",
        "crm_write_status": "NOT_WRITTEN",
        "current_promoted_natural_laws": [],
        "generated_on": "2026-07-01",
        "intake_records": records,
        "market_claim_boundary": "HYPOTHESIS_ONLY",
        "next_pass": "0062",
        "non_promotion_statement": "Pass 0061 defines model-safe buyer evidence intake records. It does not collect real buyer responses, write CRM records, prove budget, prove demand, or promote any natural law.",
        "pass": "0061",
        "send_status": "NOT_SENT",
        "unsupported_claim_count": 0,
        "upstream_outreach": {
            "path": str(outreach_path),
            "seal": outreach["seal"],
            "sha256": sha256_file(outreach_path),
            "status": outreach["status"],
        },
    }
    errors = validate(ledger)
    ledger["validation_errors"] = errors
    ledger["status"] = STATUS_MATCH if not errors else STATUS_DRIFT
    ledger["seal"] = sha256_obj(ledger)
    return ledger


def validate(ledger: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    records = ledger.get("intake_records", [])
    if ledger.get("schema") != SCHEMA:
        errors.append("schema")
    if ledger.get("buyer_response_status") != "AWAITING_REAL_RESPONSES":
        errors.append("buyer_response_status")
    if ledger.get("crm_write_status") != "NOT_WRITTEN":
        errors.append("crm_write_status")
    if ledger.get("send_status") != "NOT_SENT":
        errors.append("send_status")
    if ledger.get("market_claim_boundary") != "HYPOTHESIS_ONLY":
        errors.append("market_boundary")
    if ledger.get("unsupported_claim_count") != 0:
        errors.append("unsupported_claims")
    if ledger.get("current_promoted_natural_laws") != []:
        errors.append("natural_laws")
    if {record.get("buyer_id") for record in records} != {"research_lab", "ai_infra", "regulated_agent"}:
        errors.append("buyer_ids")
    for record in records:
        buyer_id = record.get("buyer_id")
        if record.get("privacy_boundary") != "NO_PRIVATE_CONTACT_DATA_IN_MODEL_CONTEXT":
            errors.append(f"{buyer_id}_privacy")
        if record.get("response_status") != "AWAITING_REAL_RESPONSE":
            errors.append(f"{buyer_id}_response")
        if record.get("score_status") != "UNSCORED_PENDING_BUYER_EVIDENCE":
            errors.append(f"{buyer_id}_score")
        if len(record.get("evidence_capture_fields", [])) < 7:
            errors.append(f"{buyer_id}_fields")
        if "contact_email" not in record.get("private_fields_forbidden_in_model_context", []):
            errors.append(f"{buyer_id}_private_fields")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--outreach", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    ledger = compose(Path(args.outreach))
    write_json(Path(args.out), ledger)
    print(json.dumps({"out": args.out, "seal": ledger["seal"], "status": ledger["status"]}, indent=2, sort_keys=True))
    if ledger["status"] != STATUS_MATCH:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
