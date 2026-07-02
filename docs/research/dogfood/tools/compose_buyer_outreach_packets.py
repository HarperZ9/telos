"""Compose pass 0060 CRM-ready buyer outreach packets."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


SCHEMA = "BuyerOutreachPacketSet/v1"
STATUS_MATCH = "BUYER_OUTREACH_PACKETS_MATCH"
STATUS_DRIFT = "BUYER_OUTREACH_PACKETS_DRIFT"
LANES = ["project-telos", "deep-research", "technical-writing"]


BUYER_COPY = {
    "research_lab": {
        "counterparty_id": "prospect-research-lab-proof-packets",
        "name": "Research Lab Proof-Packet Prospect",
        "sector": "research-ai4science",
        "subject": "Proof-packet pilot for replayable AI4Science claims",
        "opening": "We are testing whether research teams need claim-to-proof packets that bind sources, model actions, verification verdicts, and reproducibility evidence.",
        "ask": "Run one bounded pilot around a math, physics, biology, or AI4Science workflow where the acceptance criterion is replayable evidence rather than a claim of discovery.",
        "demo": "Pipeline-math++ style formal research proof packet.",
    },
    "ai_infra": {
        "counterparty_id": "prospect-ai-infra-action-receipts",
        "name": "AI Infrastructure Action-Receipt Prospect",
        "sector": "ai-infrastructure-agent-ops",
        "subject": "Action-receipt layer for agent tracing and replay",
        "opening": "We are testing whether AI infrastructure teams need a proof layer that connects traces, workspace state, tool authority, verification verdicts, and durable receipts.",
        "ask": "Evaluate one agent workflow where existing traces are converted into action receipts with replay and negative-verdict handling.",
        "demo": "Agent observability-to-action-receipt proof packet.",
    },
    "regulated_agent": {
        "counterparty_id": "prospect-regulated-agent-audit-packets",
        "name": "Regulated Agent Audit-Packet Prospect",
        "sector": "regulated-agent-governance",
        "subject": "Audit-ready proof packets for high-stakes agent actions",
        "opening": "We are testing whether regulated teams need reviewable proof packets that expose source provenance, human oversight, admission records, and verification boundaries without leaking private payloads.",
        "ask": "Score one high-stakes workflow against an audit packet that can show evidence without claiming production readiness.",
        "demo": "Regulated agent action proof packet.",
    },
}


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


def evidence_fields(buyer_id: str) -> list[dict[str, Any]]:
    base = [
        ("buyer_role", "Named buyer role and authority path"),
        ("budget_path", "Budget owner, procurement path, or explicit no-budget signal"),
        ("workflow_pain", "Current workflow pain stated by the buyer"),
        ("incumbent_stack", "Existing tools, platforms, observability, notebooks, or lab systems"),
        ("proof_gap", "What evidence current tools fail to bind"),
        ("acceptance_criterion", "Concrete demo condition that would justify a pilot"),
        ("negative_disqualifier", "One result that should stop the pilot"),
    ]
    if buyer_id == "research_lab":
        base.append(("reproducibility_requirement", "Formalization, replay, or experiment reproducibility requirement"))
    elif buyer_id == "ai_infra":
        base.append(("trace_boundary", "Where tracing ends and action authority evidence is missing"))
    else:
        base.append(("audit_boundary", "Review artifact boundary that avoids private payload disclosure"))
    return [{"field_id": field_id, "label": label, "required": True} for field_id, label in base]


def acceptance_criteria(buyer_id: str) -> list[str]:
    criteria = [
        "Buyer names one workflow where a proof packet would be reviewed by a real stakeholder.",
        "Buyer identifies a source, action, verification, or replay gap in the current workflow.",
        "Buyer names a concrete artifact that would move the conversation from interest to pilot.",
    ]
    if buyer_id == "research_lab":
        criteria.append("Pilot candidate can be bounded to a falsifiable research claim or reproduction task.")
    elif buyer_id == "ai_infra":
        criteria.append("Pilot candidate can ingest traces or agent logs and produce durable action receipts.")
    else:
        criteria.append("Pilot candidate has an audit or governance review event that needs a compact evidence packet.")
    return criteria


def negative_disqualifiers(buyer_id: str) -> list[str]:
    disqualifiers = [
        "Buyer only wants a generic chatbot, dashboard, or prose report.",
        "Buyer cannot name any evidence artifact that current tools fail to provide.",
        "Buyer expects unsupported claims of scientific discovery, market dominance, or production certification.",
    ]
    if buyer_id == "research_lab":
        disqualifiers.append("Research workflow cannot be bounded to replay, formalization, or reproducibility checks.")
    elif buyer_id == "ai_infra":
        disqualifiers.append("Agent workflow has no accessible traces, logs, tool calls, or state receipts.")
    else:
        disqualifiers.append("Governance workflow forbids any reviewable artifact or redacted receipt.")
    return disqualifiers


def follow_up_schedule(buyer_id: str) -> list[dict[str, str]]:
    return [
        {
            "touch_id": f"{buyer_id}-day-0",
            "offset_days": "0",
            "reason": "Send draft proof-packet pilot note and request a 25-minute evidence-fit call.",
        },
        {
            "touch_id": f"{buyer_id}-day-3",
            "offset_days": "3",
            "reason": "Ask for one current workflow artifact or incumbent-tool screenshot equivalent.",
        },
        {
            "touch_id": f"{buyer_id}-day-10",
            "offset_days": "10",
            "reason": "Close loop with a go/no-go proof-demo acceptance criterion.",
        },
    ]


def outreach_body(copy: dict[str, str], scorecard: dict[str, Any]) -> str:
    prompt_line = scorecard["interview_prompts"][0]["interview_prompt"]
    return (
        f"{copy['opening']}\n\n"
        f"Pilot ask: {copy['ask']}\n\n"
        f"Demo anchor: {copy['demo']}\n\n"
        f"Discovery question: {prompt_line}\n\n"
        "Boundary: this is a hypothesis-only market probe. It does not claim market proof, scientific truth, production readiness, or unique capability."
    )


def outreach_packet(scorecard: dict[str, Any], source_map: dict[str, dict[str, str]]) -> dict[str, Any]:
    buyer_id = scorecard["buyer_id"]
    copy = BUYER_COPY[buyer_id]
    template_id = f"pass-0060-{buyer_id}-outreach"
    source_refs = scorecard["source_ids"]
    return {
        "acceptance_criteria": acceptance_criteria(buyer_id),
        "buyer_id": buyer_id,
        "counterparty_seed": {
            "id": copy["counterparty_id"],
            "name": copy["name"],
            "notes": "Pass 0060 generated seed row; prospect identity is a placeholder until buyer discovery names a real organization.",
            "sector": copy["sector"],
            "status": "prospect_unverified",
        },
        "evidence_intake_fields": evidence_fields(buyer_id),
        "follow_up_schedule": follow_up_schedule(buyer_id),
        "market_data_targets": scorecard["market_data_targets"],
        "negative_disqualifiers": negative_disqualifiers(buyer_id),
        "outreach_event": {
            "counterparty_id": copy["counterparty_id"],
            "direction": "outbound",
            "event_type": "proposal_draft",
            "payload_ref": f"docs/research/dogfood/packets/070-{buyer_id}-outreach.md",
        },
        "payload_ref": f"docs/research/dogfood/packets/070-{buyer_id}-outreach.md",
        "route_lane_split": LANES,
        "source_refs": [
            {
                "source_id": source_id,
                "url": source_map[source_id]["url"],
                "verification_status": source_map[source_id]["verification_status"],
            }
            for source_id in source_refs
        ],
        "subject": copy["subject"],
        "template_body": outreach_body(copy, scorecard),
        "template_id": template_id,
        "verification_status": "draft_ready_not_sent",
    }


def compose(scorecards_path: Path) -> dict[str, Any]:
    upstream = read_json(scorecards_path)
    source_map = {row["source_id"]: row for row in upstream["source_anchors"]}
    packets = [outreach_packet(row, source_map) for row in upstream["scorecards"]]
    packet_set = {
        "schema": SCHEMA,
        "crm_import": {
            "counterparty_seed_count": len(packets),
            "next_touch_count": len(packets),
            "outreach_event_count": len(packets),
            "write_instruction": "Use warden-crm counterparty_upsert, outreach_emit, and next_touch_set only after operator approval.",
        },
        "crm_write_status": "NOT_WRITTEN",
        "current_promoted_natural_laws": [],
        "generated_on": "2026-07-01",
        "market_claim_boundary": "HYPOTHESIS_ONLY",
        "non_promotion_statement": "Pass 0060 drafts outreach packets and CRM import shapes. It does not send outreach, write CRM records, prove buyer demand, prove budget, or promote any natural law.",
        "outreach_packets": packets,
        "pass": "0060",
        "send_status": "NOT_SENT",
        "unsupported_claim_count": 0,
        "upstream_scorecards": {
            "path": str(scorecards_path),
            "seal": upstream["seal"],
            "sha256": sha256_file(scorecards_path),
            "status": upstream["status"],
        },
    }
    errors = validate(packet_set)
    packet_set["validation_errors"] = errors
    packet_set["status"] = STATUS_MATCH if not errors else STATUS_DRIFT
    packet_set["seal"] = sha256_obj(packet_set)
    return packet_set


def validate(packet_set: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    packets = packet_set.get("outreach_packets", [])
    if packet_set.get("schema") != SCHEMA:
        errors.append("schema")
    if packet_set.get("crm_write_status") != "NOT_WRITTEN":
        errors.append("crm_write_status")
    if packet_set.get("send_status") != "NOT_SENT":
        errors.append("send_status")
    if packet_set.get("market_claim_boundary") != "HYPOTHESIS_ONLY":
        errors.append("market_boundary")
    if packet_set.get("unsupported_claim_count") != 0:
        errors.append("unsupported_claims")
    if packet_set.get("current_promoted_natural_laws") != []:
        errors.append("natural_laws")
    if {row.get("buyer_id") for row in packets} != set(BUYER_COPY):
        errors.append("buyer_ids")
    for row in packets:
        buyer_id = row.get("buyer_id")
        if row.get("route_lane_split") != LANES:
            errors.append(f"{buyer_id}_lanes")
        if len(row.get("evidence_intake_fields", [])) < 7:
            errors.append(f"{buyer_id}_fields")
        if len(row.get("follow_up_schedule", [])) != 3:
            errors.append(f"{buyer_id}_followups")
        if not row.get("acceptance_criteria") or not row.get("negative_disqualifiers"):
            errors.append(f"{buyer_id}_criteria")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scorecards", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    packet_set = compose(Path(args.scorecards))
    write_json(Path(args.out), packet_set)
    print(json.dumps({"out": args.out, "seal": packet_set["seal"], "status": packet_set["status"]}, indent=2, sort_keys=True))
    if packet_set["status"] != STATUS_MATCH:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
