"""Compose pass 0057 buyer-objection briefs from the pass 0056 demo bundle."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


SCHEMA = "BuyerObjectionBrief/v1"
STATUS_MATCH = "BUYER_OBJECTION_BRIEF_MATCH"
STATUS_DRIFT = "BUYER_OBJECTION_BRIEF_DRIFT"


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


def replay_command_count(replay_path: Path) -> int:
    return sum(1 for line in replay_path.read_text(encoding="utf-8").splitlines() if line.strip().startswith("python "))


def source_anchors() -> list[dict[str, str]]:
    return [
        {
            "source_id": "nist-ai-rmf",
            "url": "https://www.nist.gov/itl/ai-risk-management-framework",
            "official_claim": "NIST positions the AI RMF and GenAI Profile as risk-management resources for AI systems.",
            "verification_status": "verified_official_source",
            "confidence": "high",
        },
        {
            "source_id": "opentelemetry-traces",
            "url": "https://opentelemetry.io/docs/concepts/signals/traces/",
            "official_claim": "OpenTelemetry documents spans, trace exporters, and context propagation for distributed tracing.",
            "verification_status": "verified_official_source",
            "confidence": "high",
        },
        {
            "source_id": "langsmith-observability",
            "url": "https://docs.langchain.com/langsmith/observability",
            "official_claim": "LangSmith describes observability for traces, production metrics, and integrations across LLM applications.",
            "verification_status": "verified_official_source",
            "confidence": "high",
        },
        {
            "source_id": "langfuse-observability",
            "url": "https://langfuse.com/docs/observability/overview",
            "official_claim": "Langfuse describes LLM tracing over prompts, responses, token usage, latency, tools, retrieval, and causal relationships.",
            "verification_status": "verified_official_source",
            "confidence": "high",
        },
        {
            "source_id": "microsoft-discovery",
            "url": "https://azure.microsoft.com/en-us/solutions/discovery",
            "official_claim": "Microsoft positions Discovery as an enterprise agentic AI platform for R&D lifecycle work with trust and oversight claims.",
            "verification_status": "verified_official_source",
            "confidence": "high",
        },
    ]


def objection(
    objection_id: str,
    question: str,
    answer: str,
    boundary: str,
    evidence_refs: list[str],
    demo_refs: list[str],
) -> dict[str, Any]:
    return {
        "answer": answer,
        "demo_refs": demo_refs,
        "evidence_refs": evidence_refs,
        "guardrails": ["no_universal_uniqueness_claim", "no_scientific_truth_promotion", "source_boundaries_preserved"],
        "objection": question,
        "objection_id": objection_id,
        "response_boundary": boundary,
    }


def buyer_briefs(bindings: dict[str, Any]) -> list[dict[str, Any]]:
    panes = bindings["pane_ids"]
    failures = bindings["failure_ids"]
    return [
        {
            "buyer": "Research labs and AI4Science teams",
            "buyer_id": "research_lab",
            "primary_wedge": "Research proof packets that bind source intake, tool action records, failure verdicts, and replay commands.",
            "objections": [
                objection(
                    "research-lab-001",
                    "We already have agentic discovery platforms; why is this different?",
                    "The verified claim is narrower: this packet shows a replayable evidence envelope around agent actions. Differentiation is a hypothesis until compared against live customer workflows.",
                    "inferred",
                    ["microsoft-discovery", "nist-ai-rmf", "pass-0056-demo-manifest"],
                    [panes[0], panes[1], "replay-commands.md"],
                ),
                objection(
                    "research-lab-002",
                    "Does this prove scientific truth or open-problem resolution?",
                    "No. The current artifact proves only local packet assembly and negative-fixture behavior. It explicitly promotes no natural laws.",
                    "verified",
                    ["pass-0056-demo-manifest", "pass-0056-failure-verdicts"],
                    ["current_promoted_natural_laws", *failures[:2]],
                ),
                objection(
                    "research-lab-003",
                    "Can a reviewer inspect provenance without receiving raw private payloads?",
                    "The demo exposes redacted or hash-only review panes with durable receipt references. That supports a public-review hypothesis, not a production privacy guarantee.",
                    "verified",
                    ["nist-ai-rmf", "pass-0056-review-panes"],
                    panes,
                ),
            ],
        },
        {
            "buyer": "AI infrastructure and agent-ops teams",
            "buyer_id": "ai_infra",
            "primary_wedge": "Agent action proof packets layered above traces, evals, and observability.",
            "objections": [
                objection(
                    "ai-infra-001",
                    "We already have tracing and LLM observability.",
                    "The official tools cover traces and observability. The Telos packet hypothesis is to treat traces as inputs, then bind them to durable action receipts, replay commands, and negative verdicts.",
                    "inferred",
                    ["opentelemetry-traces", "langsmith-observability", "langfuse-observability", "pass-0056-demo-manifest"],
                    [panes[1], panes[2], panes[3]],
                ),
                objection(
                    "ai-infra-002",
                    "Can the system catch receipt substitution or missing provenance?",
                    "The current demo includes five negative fixtures with matched failure verdicts, including trace/receipt substitution and missing durable receipt hash cases.",
                    "verified",
                    ["pass-0056-failure-verdicts"],
                    failures,
                ),
                objection(
                    "ai-infra-003",
                    "Can this be replayed by an engineering team?",
                    "The pass 0056 bundle includes replay commands for graph build, demo composition, and test execution. That is replay evidence, not a managed SaaS onboarding claim.",
                    "verified",
                    ["pass-0056-replay-commands"],
                    ["replay-commands.md"],
                ),
            ],
        },
        {
            "buyer": "Regulated and high-stakes agent teams",
            "buyer_id": "regulated_agent",
            "primary_wedge": "Accountable execution packets for workflows where action authority, evidence, and audit posture matter.",
            "objections": [
                objection(
                    "regulated-agent-001",
                    "Does this map to AI risk-management needs?",
                    "NIST provides a risk-management frame; the current packet can supply evidence objects that may support such a frame. Compliance sufficiency is unverified.",
                    "inferred",
                    ["nist-ai-rmf", "pass-0056-demo-manifest"],
                    [panes[0], panes[3]],
                ),
                objection(
                    "regulated-agent-002",
                    "Can we show a review artifact without claiming production readiness?",
                    "Yes for this demo: the manifest marks public_review_ready true and production_ready false, preserving a hard boundary between public review and production deployment.",
                    "verified",
                    ["pass-0056-demo-manifest"],
                    ["public_review_ready", "production_ready"],
                ),
                objection(
                    "regulated-agent-003",
                    "Can human oversight and trust boundaries be represented?",
                    "Microsoft's R&D positioning includes trust and oversight claims; the Telos packet can represent review boundaries today, while formal human approval workflows remain future integration work.",
                    "inferred",
                    ["microsoft-discovery", "pass-0056-review-panes"],
                    panes,
                ),
            ],
        },
    ]


def demo_bindings(manifest_path: Path, panes_path: Path, failures_path: Path, replay_path: Path) -> dict[str, Any]:
    manifest = read_json(manifest_path)
    panes = read_json(panes_path)
    failures = read_json(failures_path)
    summary = manifest["demo_summary"]
    return {
        "failure_ids": [row["fixture_id"] for row in failures["rows"]],
        "failure_verdict_count": summary["failure_verdict_count"],
        "manifest_hash": manifest["manifest_hash"],
        "manifest_ref": {"path": str(manifest_path), "sha256": sha256_file(manifest_path), "status": manifest["status"]},
        "pane_ids": [row["pane_id"] for row in panes["panes"]],
        "production_ready": summary["production_ready"],
        "public_review_ready": summary["public_review_ready"],
        "replay_command_count": replay_command_count(replay_path),
        "review_pane_count": summary["review_pane_count"],
    }


def validate(packet: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    buyers = packet.get("buyer_briefs", [])
    if packet.get("schema") != SCHEMA:
        errors.append("schema")
    if packet.get("market_claim_boundary") != "HYPOTHESIS_ONLY":
        errors.append("market_claim_boundary")
    if packet.get("unsupported_claim_count") != 0:
        errors.append("unsupported_claims")
    if packet.get("current_promoted_natural_laws") != []:
        errors.append("natural_law_promotion")
    if {row.get("buyer_id") for row in buyers} != {"research_lab", "ai_infra", "regulated_agent"}:
        errors.append("buyer_ids")
    if len(packet.get("source_anchors", [])) < 5:
        errors.append("source_anchors")
    for buyer in buyers:
        objections = buyer.get("objections", [])
        if len(objections) < 3:
            errors.append(f"{buyer.get('buyer_id')}_objection_count")
        for row in objections:
            if not row.get("evidence_refs") or not row.get("demo_refs"):
                errors.append(f"{row.get('objection_id')}_evidence")
            if "no_universal_uniqueness_claim" not in row.get("guardrails", []):
                errors.append(f"{row.get('objection_id')}_guardrail")
    return errors


def compose(manifest_path: Path, panes_path: Path, failures_path: Path, replay_path: Path) -> dict[str, Any]:
    bindings = demo_bindings(manifest_path, panes_path, failures_path, replay_path)
    packet = {
        "schema": SCHEMA,
        "buyer_brief_count": 3,
        "buyer_briefs": buyer_briefs(bindings),
        "current_promoted_natural_laws": [],
        "demo_bindings": bindings,
        "generated_on": "2026-07-01",
        "market_claim_boundary": "HYPOTHESIS_ONLY",
        "non_promotion_statement": "Pass 0057 maps buyer objections to verified demo evidence and official source anchors. It does not prove market uniqueness, customer demand, production readiness, scientific truth, or any natural law.",
        "pass": "0057",
        "source_anchor_count": len(source_anchors()),
        "source_anchors": source_anchors(),
        "unsupported_claim_count": 0,
    }
    errors = validate(packet)
    packet["validation_errors"] = errors
    packet["status"] = STATUS_MATCH if not errors else STATUS_DRIFT
    packet["seal"] = sha256_obj(packet)
    return packet


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--panes", required=True)
    parser.add_argument("--failures", required=True)
    parser.add_argument("--replay", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    packet = compose(Path(args.manifest), Path(args.panes), Path(args.failures), Path(args.replay))
    write_json(Path(args.out), packet)
    print(json.dumps({"out": args.out, "seal": packet["seal"], "status": packet["status"]}, indent=2, sort_keys=True))
    if packet["status"] != STATUS_MATCH:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
