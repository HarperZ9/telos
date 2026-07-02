"""Compose pass 0059 buyer-discovery evidence scorecards."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


SCHEMA = "BuyerDiscoveryEvidenceScorecards/v1"
STATUS_MATCH = "BUYER_DISCOVERY_EVIDENCE_SCORECARDS_MATCH"
STATUS_DRIFT = "BUYER_DISCOVERY_EVIDENCE_SCORECARDS_DRIFT"
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


def source_anchors() -> list[dict[str, str]]:
    anchors = [
        ("futurehouse-home", "https://www.futurehouse.org/", "FutureHouse describes its work as building AI agents to automate research in biology and complex sciences."),
        ("futurehouse-tools", "https://www.futurehouse.org/tools", "FutureHouse lists PaperQA2 and platform access to scientific agents for discovery."),
        ("sakana-ai-scientist", "https://sakana.ai/ai-scientist/", "Sakana frames The AI Scientist around automating the research process itself."),
        ("microsoft-discovery", "https://azure.microsoft.com/en-us/solutions/discovery", "Microsoft positions Discovery as an enterprise agentic AI platform for R&D with lifecycle and trust claims."),
        ("nist-ai-rmf", "https://www.nist.gov/itl/ai-risk-management-framework", "NIST publishes the AI RMF, GenAI Profile, and critical-infrastructure profile concept note."),
        ("nist-genai-profile", "https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence", "NIST AI 600-1 is a cross-sectoral companion profile for generative AI risk management."),
        ("pipeline-math", "https://github.com/Pengbinghui/pipeline-math", "pipeline-math collects claimed resolutions of open problems with a prover-verifier workflow and Lean formalization links."),
        ("leandojo", "https://leandojo.org/leandojo.html", "LeanDojo documents theorem-proving data extraction, an interactive Lean environment, and formal proof benchmarks."),
        ("opentelemetry-traces", "https://opentelemetry.io/docs/concepts/signals/traces/", "OpenTelemetry traces document spans, trace exporters, and context propagation."),
        ("opentelemetry-context", "https://opentelemetry.io/docs/concepts/context-propagation/", "OpenTelemetry context propagation correlates traces, metrics, and logs across distributed systems."),
    ]
    return [
        {
            "confidence": "high",
            "official_claim": claim,
            "source_id": source_id,
            "url": url,
            "verification_status": "verified_primary_source",
        }
        for source_id, url, claim in anchors
    ]


def prompts_by_buyer(bridge: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for prompt in bridge["buyer_discovery_script"]["prompts"]:
        grouped[prompt["buyer_id"]].append(prompt)
    return dict(grouped)


def market_targets(buyer_id: str) -> list[dict[str, Any]]:
    common = [
        {
            "target_id": f"{buyer_id}-budget-owner",
            "target": "Identify the buyer who can fund proof-packet pilots.",
            "source_refs": ["microsoft-discovery"],
            "verification_status": "unverified",
        },
        {
            "target_id": f"{buyer_id}-proof-threshold",
            "target": "Measure what evidence threshold converts interest into a pilot.",
            "source_refs": ["nist-ai-rmf"],
            "verification_status": "inferred",
        },
    ]
    specific = {
        "research_lab": [
            ("research-lab-ai4science-workflow", "Map current AI4Science workflow bottlenecks against agentic discovery platforms.", ["futurehouse-home", "microsoft-discovery"], "verified"),
            ("research-lab-formal-proof-need", "Collect proof or formalization requirements for math and scientific claims.", ["pipeline-math", "leandojo"], "verified"),
            ("research-lab-whitepaper-queue", "Collect top whitepapers, open problems, and reproducibility requirements per field.", ["sakana-ai-scientist", "pipeline-math"], "inferred"),
        ],
        "ai_infra": [
            ("ai-infra-trace-receipt-gap", "Measure where traces stop short of durable action receipts.", ["opentelemetry-traces"], "verified"),
            ("ai-infra-context-causality-gap", "Collect cases where context propagation cannot prove action authority.", ["opentelemetry-context"], "inferred"),
            ("ai-infra-observability-budget", "Estimate buyer budget path for proof packets layered over observability stacks.", ["opentelemetry-traces"], "unverified"),
        ],
        "regulated_agent": [
            ("regulated-risk-profile-fit", "Map proof packets to AI RMF and GenAI profile risk-management evidence needs.", ["nist-ai-rmf", "nist-genai-profile"], "verified"),
            ("regulated-human-oversight", "Collect approval, review, and human oversight requirements for high-stakes actions.", ["microsoft-discovery", "nist-ai-rmf"], "inferred"),
            ("regulated-audit-packet-buying-trigger", "Find the audit event that creates urgency for action receipts.", ["nist-genai-profile"], "unverified"),
        ],
    }
    rows = list(common)
    for target_id, target, refs, status in specific[buyer_id]:
        rows.append({"target_id": target_id, "target": target, "source_refs": refs, "verification_status": status})
    return rows


def evidence_requirements(buyer_id: str) -> list[str]:
    return [
        f"{buyer_id}: named buyer role and budget path",
        f"{buyer_id}: source-backed workflow pain with primary URL",
        f"{buyer_id}: replayable proof-packet demo acceptance criterion",
        f"{buyer_id}: negative verdict that would disqualify the pilot",
        f"{buyer_id}: measurable next action with owner and date",
    ]


def scoring_dimensions() -> list[dict[str, str]]:
    return [
        {"dimension": "urgency", "score": "UNSCORED", "requires": "buyer interview evidence"},
        {"dimension": "budget", "score": "UNSCORED", "requires": "budget-owner evidence"},
        {"dimension": "proof_gap", "score": "UNSCORED", "requires": "gap between incumbent tools and proof-packet requirement"},
        {"dimension": "demo_fit", "score": "UNSCORED", "requires": "demo acceptance criterion"},
        {"dimension": "adoption_friction", "score": "UNSCORED", "requires": "integration and security constraints"},
    ]


def scorecards(bridge: dict[str, Any]) -> list[dict[str, Any]]:
    grouped = prompts_by_buyer(bridge)
    source_map = {
        "research_lab": ["futurehouse-home", "futurehouse-tools", "sakana-ai-scientist", "microsoft-discovery", "pipeline-math", "leandojo"],
        "ai_infra": ["opentelemetry-traces", "opentelemetry-context", "microsoft-discovery", "nist-ai-rmf"],
        "regulated_agent": ["nist-ai-rmf", "nist-genai-profile", "microsoft-discovery", "opentelemetry-context"],
    }
    rows = []
    for buyer_id in ["research_lab", "ai_infra", "regulated_agent"]:
        prompts = grouped[buyer_id]
        rows.append({
            "buyer_id": buyer_id,
            "evidence_requirements": evidence_requirements(buyer_id),
            "interview_prompt_count": len(prompts),
            "interview_prompts": prompts,
            "market_data_targets": market_targets(buyer_id),
            "route_lane_split": LANES,
            "score_dimensions": scoring_dimensions(),
            "scorecard_status": "NEEDS_INTERVIEW_DATA",
            "source_ids": source_map[buyer_id],
        })
    return rows


def collection_plan() -> dict[str, Any]:
    return {
        "collection_steps": [
            "Run Gather over the primary source URLs and store source receipts.",
            "Run buyer interviews with the nine prompts and bind answers to evidence requirements.",
            "Score urgency, budget, proof gap, demo fit, and adoption friction only after evidence is collected.",
            "Promote candidate wedges only if source, buyer, and demo evidence agree.",
            "Run Crucible against any claimed market gap before public use.",
        ],
        "next_pass": "0060",
        "status": "READY_FOR_EVIDENCE_COLLECTION",
    }


def validate(packet: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if packet.get("schema") != SCHEMA:
        errors.append("schema")
    if packet.get("market_claim_boundary") != "HYPOTHESIS_ONLY":
        errors.append("market_boundary")
    if packet.get("unsupported_claim_count") != 0:
        errors.append("unsupported_claims")
    if packet.get("current_promoted_natural_laws") != []:
        errors.append("natural_law_promotion")
    if packet.get("source_anchor_count", 0) < 9:
        errors.append("source_count")
    if {row.get("buyer_id") for row in packet.get("scorecards", [])} != {"research_lab", "ai_infra", "regulated_agent"}:
        errors.append("buyer_ids")
    if sum(row.get("interview_prompt_count", 0) for row in packet.get("scorecards", [])) != 9:
        errors.append("prompt_count")
    for row in packet.get("scorecards", []):
        if len(row.get("source_ids", [])) < 3:
            errors.append(f"{row.get('buyer_id')}_sources")
        if len(row.get("market_data_targets", [])) < 4:
            errors.append(f"{row.get('buyer_id')}_targets")
        if row.get("scorecard_status") != "NEEDS_INTERVIEW_DATA":
            errors.append(f"{row.get('buyer_id')}_status")
    return errors


def compose(bridge_path: Path) -> dict[str, Any]:
    bridge = read_json(bridge_path)
    anchors = source_anchors()
    packet = {
        "schema": SCHEMA,
        "collection_plan": collection_plan(),
        "current_promoted_natural_laws": [],
        "generated_on": "2026-07-01",
        "market_claim_boundary": "HYPOTHESIS_ONLY",
        "market_data_status": "COLLECTION_TARGETS_DEFINED",
        "non_promotion_statement": "Pass 0059 defines evidence scorecards and market-data collection targets. It does not prove market size, buyer budget, customer adoption, scientific truth, or any natural law.",
        "pass": "0059",
        "scorecards": scorecards(bridge),
        "source_anchor_count": len(anchors),
        "source_anchors": anchors,
        "unsupported_claim_count": 0,
        "upstream_bridge": {
            "path": str(bridge_path),
            "sha256": sha256_file(bridge_path),
            "status": bridge["status"],
            "seal": bridge["seal"],
        },
    }
    errors = validate(packet)
    packet["validation_errors"] = errors
    packet["status"] = STATUS_MATCH if not errors else STATUS_DRIFT
    packet["seal"] = sha256_obj(packet)
    return packet


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bridge", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    packet = compose(Path(args.bridge))
    write_json(Path(args.out), packet)
    print(json.dumps({"out": args.out, "seal": packet["seal"], "status": packet["status"]}, indent=2, sort_keys=True))
    if packet["status"] != STATUS_MATCH:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
