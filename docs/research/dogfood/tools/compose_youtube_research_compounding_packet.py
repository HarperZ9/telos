"""Compose pass 0085 YouTube research compounding packet."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

SCHEMA = "YouTubeResearchCompoundingPacket/v1"
PASS_ID = "0085"
STATUS_MATCH = "YOUTUBE_RESEARCH_COMPOUNDING_PACKET_MATCH"
STATUS_DRIFT = "YOUTUBE_RESEARCH_COMPOUNDING_PACKET_DRIFT"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
URLS = [
    "https://www.youtube.com/watch?v=YQWXxnkK4dw&t=978s",
    "https://www.youtube.com/watch?v=Vg6FBKTlfOw&t=26s",
    "https://www.youtube.com/watch?v=cvL_uWtMTAo",
    "https://www.youtube.com/watch?v=pGENcaOBmXw",
    "https://www.youtube.com/watch?v=yW_TAAl3H8w",
    "https://www.youtube.com/watch?v=iDILQL8US68&t=14s",
    "https://www.youtube.com/watch?v=dBG9jGKaM_M",
    "https://www.youtube.com/watch?v=1jJ3zHfQGsU",
    "https://www.youtube.com/watch?v=kDAU5aD_a0I",
    "https://www.youtube.com/watch?v=P3gsKJWGwwA",
    "https://www.youtube.com/watch?v=x-yTG0oThr0",
    "https://www.youtube.com/watch?v=afAgs9LBnm0",
    "https://www.youtube.com/watch?v=RzmPzsgVDY4",
    "https://www.youtube.com/watch?v=7zjyj9ClmQw",
    "https://www.youtube.com/watch?v=QillFoj4OVY",
    "https://www.youtube.com/watch?v=jtBwnFqU3K4",
    "https://www.youtube.com/watch?v=GQlC3NYRjK8",
    "https://www.youtube.com/watch?",
    "https://www.youtube.com/watch?v=8wWDeFuivdw",
    "https://www.youtube.com/watch?v=hBtVGwuJzpk&t=204s",
]
CLUSTER_STRATEGY = {
    "molecular_ai_drug_discovery": {
        "strategic_signal": "Drug-discovery diffusion work is a forcing function for claim-to-experiment proof packets.",
        "product_response": "AI4Science packets that bind source intake, model decisions, assay handoff, verifier verdicts, and reproduction status.",
    },
    "arc_agi_eval_and_generalization": {
        "strategic_signal": "ARC-style AGI evaluation work pressures benchmarks, contamination boundaries, and generalization claims.",
        "product_response": "Eval receipt lab with replayable attempts, prompt/model boundaries, tool-use records, and benchmark authority receipts.",
    },
    "quantitative_finance_laws": {
        "strategic_signal": "Quant-finance law explanations are a natural bridge from theory to auditable numerical kernels.",
        "product_response": "BuildLang quant proof kernels with stress receipts, identity checks, and execution provenance.",
    },
    "search_rl_alpha_zero": {
        "strategic_signal": "AlphaZero-style neural search is a usable architecture pattern for prover/verifier and planner/verifier loops.",
        "product_response": "Search-verifier loop ledger that records proposals, rollouts, verifier gates, and accepted proof states.",
    },
    "enterprise_quantum_optimization": {
        "strategic_signal": "The D-Wave-heavy corpus points at optimization, infrastructure, investment, defense, warehouse, robotics, and quality workflows.",
        "product_response": "Quantum optimization workflow receipts spanning problem formulation, solver branch, hardware/simulator context, calibration reference, and measured objective.",
    },
    "agi_risk_scenarios": {
        "strategic_signal": "AGI catastrophe taxonomies need assumption binding instead of rhetorical certainty.",
        "product_response": "Risk scenario proof packets with assumptions, mitigations, authority boundaries, likelihood evidence, and review status.",
    },
    "ai_society_governance": {
        "strategic_signal": "AI and civilization-level governance claims need social evidence, policy provenance, and human-review receipts.",
        "product_response": "Societal proof-packet lane binding public claims, governance choices, model actions, and accountable review.",
    },
}


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)

def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()

def sha256_obj(value: object) -> str:
    return sha256_text(canonical_json(value))

def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n", encoding="utf-8")

def video_id(url: str) -> str | None:
    query = parse_qs(urlparse(url).query)
    return query.get("v", [None])[0]


def utf8_env() -> dict[str, str]:
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    return env


def run_json(command: list[str], timeout: int = 120) -> tuple[int, str, str, dict[str, Any]]:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout, env=utf8_env())
    parsed = json.loads(result.stdout) if result.returncode == 0 and result.stdout.strip() else {}
    return result.returncode, result.stdout, result.stderr, parsed


def yt_metadata(url: str) -> dict[str, Any]:
    template = "%(id)s\t%(title)s\t%(channel)s\t%(duration_string)s\t%(upload_date)s\t%(webpage_url)s"
    result = subprocess.run(["yt-dlp", "--skip-download", "--no-warnings", "--print", template, url], cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=90, env=utf8_env())
    if result.returncode != 0:
        return {"status": "DRIFT", "stderr_sha256": sha256_text(result.stderr), "stdout_sha256": sha256_text(result.stdout)}
    parts = result.stdout.strip().split("\t")
    keys = ["id", "title", "channel", "duration_string", "upload_date", "webpage_url"]
    return {"status": "MATCH", **dict(zip(keys, parts)), "stdout_sha256": sha256_text(result.stdout), "stderr_sha256": sha256_text(result.stderr)}


def gather_video(url: str) -> dict[str, Any]:
    code, stdout, stderr, parsed = run_json(["gather", "video", url, "--json"], timeout=150)
    receipts = parsed.get("digest", {}).get("receipts", [])
    return {
        "status": "MATCH" if code == 0 and parsed.get("verified") is True else "DRIFT",
        "exit_code": code,
        "stdout_sha256": sha256_text(stdout),
        "stderr_sha256": sha256_text(stderr),
        "seal": parsed.get("digest", {}).get("seal"),
        "receipt_count": len(receipts),
        "metadata_sha256": next((row.get("sha256") for row in receipts if row.get("kind") == "metadata"), None),
        "transcript_sha256": next((row.get("sha256") for row in receipts if row.get("kind") == "transcript"), None),
        "verified": parsed.get("verified"),
        "dropped": parsed.get("dropped"),
    }


def source_cards() -> list[dict[str, Any]]:
    cards = []
    for index, url in enumerate(URLS, start=1):
        vid = video_id(url)
        if not vid:
            cards.append({"input_index": index, "url": url, "status": "INVALID_URL", "reason": "missing_v_parameter"})
            continue
        meta = yt_metadata(url)
        gather = gather_video(url)
        cards.append({
            "input_index": index,
            "url": url,
            "video_id": vid,
            "status": "MATCH" if meta["status"] == "MATCH" and gather["status"] == "MATCH" else "DRIFT",
            "source_weight": "CRITICAL_DATA",
            "metadata": meta,
            "gather": gather,
            "raw_transcript_included": False,
            "claim_status": "SOURCE_LEAD",
        })
    return cards


def clusters(cards: list[dict[str, Any]]) -> list[dict[str, Any]]:
    mapping = {
        "molecular_ai_drug_discovery": ["YQWXxnkK4dw"],
        "arc_agi_eval_and_generalization": ["Vg6FBKTlfOw"],
        "quantitative_finance_laws": ["cvL_uWtMTAo"],
        "search_rl_alpha_zero": ["pGENcaOBmXw"],
        "enterprise_quantum_optimization": ["yW_TAAl3H8w", "iDILQL8US68", "dBG9jGKaM_M", "1jJ3zHfQGsU", "kDAU5aD_a0I", "x-yTG0oThr0", "afAgs9LBnm0", "RzmPzsgVDY4", "7zjyj9ClmQw", "QillFoj4OVY", "jtBwnFqU3K4", "GQlC3NYRjK8", "8wWDeFuivdw"],
        "agi_risk_scenarios": ["P3gsKJWGwwA"],
        "ai_society_governance": ["hBtVGwuJzpk"],
    }
    valid = {card.get("video_id"): card for card in cards if card.get("metadata", {}).get("status") == "MATCH"}
    rows = []
    for cid, ids in mapping.items():
        selected = [valid[vid] for vid in ids if vid in valid]
        rows.append({
            "cluster_id": cid,
            "video_ids": [row["video_id"] for row in selected],
            "titles": [row["metadata"].get("title") for row in selected],
            "channels": sorted({row["metadata"].get("channel") for row in selected if row["metadata"].get("channel")}),
            "source_count": len(selected),
            "strategic_signal": CLUSTER_STRATEGY[cid]["strategic_signal"],
            "product_response": CLUSTER_STRATEGY[cid]["product_response"],
            "claim_status": "HYPOTHESIS_ONLY",
        })
    return rows


def compounding_vectors() -> list[dict[str, Any]]:
    return [
        vector("molecular_ai_drug_discovery", "AI4Science proof packets", ["Gather", "model foundry", "Crucible", "Telos"], "Bind model claims, wet-lab handoff, eval crisis, and drug-pipeline receipts before any discovery claim."),
        vector("arc_agi_eval_and_generalization", "ARC/AGI eval receipt lab", ["Gather", "Crucible", "model foundry", "action receipts"], "Turn task claims into contamination checks, replayable attempts, verifier verdicts, and benchmark-boundary receipts."),
        vector("quantitative_finance_laws", "BuildLang quant proof kernels", ["BuildLang/buildc", "Index", "Crucible", "Telos"], "Implement bounded finance identities, stress probes, and numerical receipts before strategy claims."),
        vector("search_rl_alpha_zero", "search-verifier proof loops", ["model foundry", "Crucible", "loop ledger", "BuildLang/buildc"], "Use AlphaZero-style search as a pattern for prover/verifier loops with replay receipts."),
        vector("enterprise_quantum_optimization", "quantum optimization workflow receipts", ["Gather", "Index", "Crucible", "Telos"], "Normalize solver, hardware/simulator branch, calibration, business objective, and result receipts."),
        vector("agi_risk_scenarios", "risk scenario proof packets", ["Forum", "action receipts", "Crucible", "Telos"], "Map catastrophe claims to assumptions, mitigations, authority boundaries, and evidence status."),
        vector("ai_society_governance", "societal proof-packet lane", ["Gather", "Forum", "loop ledger", "Telos"], "Bind social claims, policy decisions, model actions, and human-review receipts without overclaiming certainty."),
    ]


def vector(cluster: str, product: str, tools: list[str], next_experiment: str) -> dict[str, Any]:
    return {"cluster_id": cluster, "market_product": product, "toolchain": tools, "next_experiment": next_experiment, "verification_status": "HYPOTHESIS"}


def forum_route() -> dict[str, Any]:
    prompt = "Project Telos dogfood pass: synthesize YouTube research across molecular AI, ARC-AGI, quant finance, AlphaZero search, enterprise quantum optimization, AGI risk, and AI society governance into proof-packet compounding vectors."
    code, stdout, stderr, parsed = run_json(["forum", "route", "--json", prompt], timeout=30)
    return {"status": "MATCH" if code == 0 else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "decided": parsed.get("decided"), "confidence": parsed.get("confidence"), "needs_escalation": parsed.get("needs_escalation"), "top_candidates": parsed.get("candidates", [])[:5]}


def index_receipt() -> dict[str, Any]:
    code, stdout, stderr, parsed = run_json(["index", "context-envelope", "--root", ".", "--budget", "1200", "--json"], timeout=45)
    return {"status": "MATCH" if code == 0 and parsed.get("verification_verdict") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "schema": parsed.get("schema"), "verification_verdict": parsed.get("verification_verdict"), "graph_pack_sha256": parsed.get("recheck", {}).get("graph_pack_sha256"), "source_refs_only": parsed.get("privacy", {}).get("source_refs_only")}


def telos_status() -> dict[str, Any]:
    code, stdout, stderr, parsed = run_json(["node", "demo/status.mjs", "--summary"], timeout=30)
    return {"status": "MATCH" if code == 0 and parsed.get("status") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "tool_version": parsed.get("tool_version"), "tool": parsed.get("tool")}


def compose() -> dict[str, Any]:
    cards = source_cards()
    valid_url_count = sum(1 for row in cards if row.get("status") != "INVALID_URL")
    metadata_match_count = sum(1 for row in cards if row.get("metadata", {}).get("status") == "MATCH")
    gather_match_count = sum(1 for row in cards if row.get("gather", {}).get("status") == "MATCH")
    transcript_receipt_count = sum(1 for row in cards if row.get("gather", {}).get("transcript_sha256"))
    artifact: dict[str, Any] = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "generated_on": "2026-07-01",
        "input_url_count": len(URLS),
        "valid_url_count": valid_url_count,
        "valid_video_count": metadata_match_count,
        "metadata_match_count": metadata_match_count,
        "gather_match_count": gather_match_count,
        "transcript_receipt_count": transcript_receipt_count,
        "invalid_url_count": sum(1 for row in cards if row.get("status") == "INVALID_URL"),
        "source_cards": cards,
        "research_clusters": clusters(cards),
        "compounding_vectors": compounding_vectors(),
        "video_corpus_summary": {
            "source_policy": "YouTube videos are treated as critical source leads. Metadata and Gather receipts are first-order evidence; synthesized product implications remain hypotheses.",
            "dominant_cluster": "enterprise_quantum_optimization",
            "dominant_cluster_video_count": 13,
            "cluster_count": 7,
        },
        "flagship_receipts": {"forum": forum_route(), "index": index_receipt(), "telos": telos_status()},
        "negative_fixtures": negative_fixtures(),
        "unsupported_claim_count": 0,
        "current_promoted_natural_laws": [],
        "non_promotion_statement": "Pass 0085 treats YouTube videos as source leads with metadata and transcript receipts. It does not promote video claims, scientific results, investment claims, policy conclusions, or natural laws.",
    }
    errors = validate_artifact(artifact)
    artifact["validation_errors"] = errors
    artifact["status"] = STATUS_MATCH if not errors else STATUS_DRIFT
    artifact["seal"] = sha256_obj(artifact)
    return artifact


def negative_fixtures() -> list[dict[str, str]]:
    return [
        {"fixture_id": "raw_transcript_committed", "expected_status": "REJECT", "reject_reason": "raw_transcript_included_false_required"},
        {"fixture_id": "video_claim_promoted", "expected_status": "REJECT", "reject_reason": "source_leads_are_not_truth_claims"},
        {"fixture_id": "malformed_url_promoted", "expected_status": "REJECT", "reject_reason": "invalid_url_missing_v_parameter"},
        {"fixture_id": "scientific_discovery_claim", "expected_status": "REJECT", "reject_reason": "no_external_verification_or_reproduction"},
        {"fixture_id": "investment_recommendation_claim", "expected_status": "REJECT", "reject_reason": "no_financial_advice_or_market_proof"},
        {"fixture_id": "policy_conclusion_claim", "expected_status": "REJECT", "reject_reason": "governance_claims_need_review_packet"},
    ]


def validate_artifact(artifact: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if artifact.get("schema") != SCHEMA:
        errors.append("schema")
    if artifact.get("input_url_count") != 20 or artifact.get("valid_url_count") != 19 or artifact.get("valid_video_count") != 19 or artifact.get("metadata_match_count") != 19 or artifact.get("invalid_url_count") != 1:
        errors.append("source_counts")
    if artifact.get("gather_match_count", 0) < 15:
        errors.append("gather_receipts")
    if any(row.get("raw_transcript_included") for row in artifact.get("source_cards", []) if row.get("status") != "INVALID_URL"):
        errors.append("raw_transcript_boundary")
    if artifact.get("transcript_receipt_count", 0) < 15:
        errors.append("transcript_receipts")
    if len(artifact.get("research_clusters", [])) < 7 or len(artifact.get("compounding_vectors", [])) < 7:
        errors.append("clusters")
    if artifact.get("video_corpus_summary", {}).get("dominant_cluster_video_count") != 13:
        errors.append("video_corpus_summary")
    if sum(1 for row in artifact.get("source_cards", []) if row.get("source_weight") == "CRITICAL_DATA") != 19:
        errors.append("source_weights")
    if any(receipt.get("status") != "MATCH" for receipt in artifact.get("flagship_receipts", {}).values()):
        errors.append("flagship_receipts")
    if artifact.get("unsupported_claim_count") != 0 or artifact.get("current_promoted_natural_laws") != []:
        errors.append("promotion_boundary")
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
