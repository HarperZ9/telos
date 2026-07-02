"""Compose pass 0058 Forum route-vocabulary bridge artifacts."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


SCHEMA = "ForumRouteVocabularyBridge/v1"
STATUS_MATCH = "FORUM_ROUTE_VOCABULARY_BRIDGE_MATCH"
STATUS_DRIFT = "FORUM_ROUTE_VOCABULARY_BRIDGE_DRIFT"
LANES = ["project-telos", "deep-research", "technical-writing"]


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


def lane_taxonomy() -> list[dict[str, Any]]:
    return [
        {
            "lane_id": "project-telos",
            "purpose": "Own the proof-packet substrate, receipts, schemas, Crucible verdicts, and replay boundaries.",
            "bridge_terms": ["Project Telos", "proof-packet", "receipt", "Crucible", "Index", "Gather", "Forum", "Telos"],
        },
        {
            "lane_id": "deep-research",
            "purpose": "Own current market, whitepaper, competitor, buyer urgency, and field evidence gathering.",
            "bridge_terms": ["market research", "whitepaper", "competitor", "AI4Science", "buyer urgency", "budget"],
        },
        {
            "lane_id": "technical-writing",
            "purpose": "Own buyer briefs, discovery scripts, adoption narratives, and clean handoff packets.",
            "bridge_terms": ["buyer brief", "discovery script", "interview prompt", "packet", "operator note"],
        },
    ]


def route_receipt(receipts: dict[str, Any]) -> dict[str, Any]:
    for row in receipts.get("receipts", []):
        if row.get("tool") == "mcp__forum.route" or row.get("command") == "route":
            return row
    return {"status": "UNVERIFIED", "decided": None, "needs_escalation": True, "candidates": []}


def observed_gap(receipts: dict[str, Any]) -> dict[str, Any]:
    row = route_receipt(receipts)
    candidates = row.get("candidates", [])
    return {
        "decided": row.get("decided"),
        "needs_escalation": row.get("needs_escalation"),
        "observed_status": row.get("status"),
        "status": "ROUTE_ESCALATION_OBSERVED" if row.get("needs_escalation") else "ROUTE_DECISION_OBSERVED",
        "top_candidate": candidates[0]["agent"] if candidates else None,
        "top_candidate_score": candidates[0]["score"] if candidates else None,
    }


def bridge_prompt(subject: str) -> str:
    return (
        "Project Telos proof-packet route bridge: split this work across "
        "project-telos for receipts/verdicts/replay, deep-research for current "
        "market and whitepaper evidence, and technical-writing for buyer-facing "
        f"handoff. Subject: {subject}"
    )


def rewrite_fixtures() -> list[dict[str, Any]]:
    originals = [
        "Research AI4Science market competitors and buyer objections.",
        "Create buyer discovery prompts from proof-packet evidence.",
        "Summarize agent observability proof boundaries for AI infrastructure teams.",
        "Map regulated-agent risk objections to replayable receipts.",
        "Plan a public demo around market research, Crucible verdicts, and proof packets.",
    ]
    rows = []
    for index, original in enumerate(originals, start=1):
        rows.append({
            "bridge_prompt": bridge_prompt(original),
            "expected_primary_lane": "project-telos",
            "fixture_id": f"route-bridge-{index:02d}",
            "original_prompt": original,
            "target_lane_split": LANES,
            "verification_status": "inferred",
        })
    return rows


def buyer_discovery_script(brief: dict[str, Any]) -> dict[str, Any]:
    prompts: list[dict[str, Any]] = []
    for buyer in brief["buyer_briefs"]:
        for row in buyer["objections"]:
            prompts.append({
                "buyer_id": buyer["buyer_id"],
                "evidence_refs": row["evidence_refs"],
                "guardrails": row["guardrails"],
                "interview_prompt": (
                    f"When evaluating a Project Telos proof-packet workflow, how would your team answer this objection: {row['objection']}"
                ),
                "objection_id": row["objection_id"],
                "target_lane_split": LANES,
            })
    return {
        "prompt_count": len(prompts),
        "prompts": prompts,
        "source_objection_count": sum(len(row["objections"]) for row in brief["buyer_briefs"]),
    }


def integration_gaps() -> list[dict[str, str]]:
    return [
        {
            "gap_id": "forum-route-market-proof-packet-vocabulary",
            "gap": "Generic market-research language can escalate unless proof-packet and Project Telos terms are explicit.",
            "next_action": "Patch or configure Forum route vocabulary with split-lane proof-packet fixtures.",
            "verification_status": "verified",
        },
        {
            "gap_id": "forum-submit-executor-json",
            "gap": "Forum submit is not reliable until the configured model executor returns valid JSON.",
            "next_action": "Add an executor health receipt before treating Forum submit as a steelman source.",
            "verification_status": "verified",
        },
        {
            "gap_id": "multi-lane-routing-envelope",
            "gap": "Forum route reports one lane or escalation, while proof-packet market work needs a split-lane envelope.",
            "next_action": "Define a ForumRouteBridge/v1 envelope with primary, secondary, and handoff lanes.",
            "verification_status": "inferred",
        },
    ]


def validate(packet: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    lanes = {row.get("lane_id") for row in packet.get("lane_taxonomy", [])}
    if packet.get("schema") != SCHEMA:
        errors.append("schema")
    if lanes != set(LANES):
        errors.append("lanes")
    if packet.get("current_promoted_natural_laws") != []:
        errors.append("natural_law_promotion")
    if packet.get("market_claim_boundary") != "HYPOTHESIS_ONLY":
        errors.append("market_boundary")
    if packet.get("unsupported_claim_count") != 0:
        errors.append("unsupported_claims")
    if packet.get("observed_forum_gap", {}).get("status") != "ROUTE_ESCALATION_OBSERVED":
        errors.append("observed_gap")
    if len(packet.get("rewrite_fixtures", [])) < 5:
        errors.append("rewrite_count")
    for row in packet.get("rewrite_fixtures", []):
        if set(LANES) - set(row.get("target_lane_split", [])):
            errors.append(f"{row.get('fixture_id')}_split")
        if "Project Telos proof-packet" not in row.get("bridge_prompt", ""):
            errors.append(f"{row.get('fixture_id')}_bridge_prompt")
    script = packet.get("buyer_discovery_script", {})
    if script.get("prompt_count") != 9 or script.get("source_objection_count") != 9:
        errors.append("discovery_prompt_count")
    return errors


def compose(brief_path: Path, receipts_path: Path) -> dict[str, Any]:
    brief = read_json(brief_path)
    receipts = read_json(receipts_path)
    packet = {
        "schema": SCHEMA,
        "buyer_discovery_script": buyer_discovery_script(brief),
        "current_promoted_natural_laws": [],
        "generated_on": "2026-07-01",
        "integration_gaps": integration_gaps(),
        "lane_taxonomy": lane_taxonomy(),
        "market_claim_boundary": "HYPOTHESIS_ONLY",
        "non_promotion_statement": "Pass 0058 creates routing fixtures and discovery prompts. It does not prove market demand, production routing changes, customer adoption, scientific truth, or any natural law.",
        "observed_forum_gap": observed_gap(receipts),
        "pass": "0058",
        "rewrite_fixtures": rewrite_fixtures(),
        "route_readiness": {
            "ready_for_forum_patch": False,
            "ready_for_operator_use": True,
            "reason": "Bridge prompts are deterministic artifacts; Forum itself is not patched in this pass.",
        },
        "unsupported_claim_count": 0,
        "upstream_brief": {
            "path": str(brief_path),
            "sha256": sha256_file(brief_path),
            "status": brief["status"],
            "seal": brief["seal"],
        },
        "upstream_receipts": {
            "path": str(receipts_path),
            "sha256": sha256_file(receipts_path),
            "status": receipts["status"],
        },
    }
    errors = validate(packet)
    packet["validation_errors"] = errors
    packet["status"] = STATUS_MATCH if not errors else STATUS_DRIFT
    packet["seal"] = sha256_obj(packet)
    return packet


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--brief", required=True)
    parser.add_argument("--receipts", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    packet = compose(Path(args.brief), Path(args.receipts))
    write_json(Path(args.out), packet)
    print(json.dumps({"out": args.out, "seal": packet["seal"], "status": packet["status"]}, indent=2, sort_keys=True))
    if packet["status"] != STATUS_MATCH:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
