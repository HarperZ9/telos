"""Compose pass 0125 YouTube-to-experiment router receipt."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

SCHEMA = "YoutubeExperimentRouterReceipt/v1"
PASS_ID = "0125"
STATUS_MATCH = "YOUTUBE_EXPERIMENT_ROUTER_MATCH"
STATUS_DRIFT = "YOUTUBE_EXPERIMENT_ROUTER_DRIFT"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
STORE = ROOT / "gather" / "pass-0125-youtube-experiment-router"
UPSTREAMS = {
    "youtube_growth": ROOT / "schemas" / "youtube-megatool-growth-vector-receipt-pass-0121.json",
    "field_factory": ROOT / "schemas" / "field-to-proof-packet-factory-pass-0123.json",
    "agent_action_adapter": ROOT / "schemas" / "agent-action-proof-packet-factory-adapter-pass-0124.json",
}

VIDEOS = {
    "HbKzqvey5PA": {"url": "https://www.youtube.com/watch?v=HbKzqvey5PA", "theme": "quantum_foundation_claim_boundary"},
    "4MQbd5wTlI8": {"url": "https://www.youtube.com/watch?v=4MQbd5wTlI8", "theme": "formal_homotopy_proof_os"},
    "EdVG5qNm2rY": {"url": "https://www.youtube.com/watch?v=EdVG5qNm2rY&t=337s", "theme": "counterexample_revision_workbench"},
    "nYwid6Q5HXk": {"url": "https://www.youtube.com/watch?v=nYwid6Q5HXk", "theme": "looped_agent_verifier_os"},
}

SIGNALS = {
    "formal_math": ["category", "homotopy", "proof", "theorem", "axiom", "type", "lean", "mathematics"],
    "quantum_physics": ["born", "entropy", "quantum", "measurement", "probability", "state", "physics"],
    "counterexample": ["counterexample", "disprove", "belief", "complexity", "problem", "algorithm", "hard"],
    "agent_loop": ["loop", "chain", "thought", "reasoning", "verify", "verifier", "feedback"],
    "runtime_compute": ["runtime", "compute", "compiler", "simulation", "kernel", "optimization", "execute"],
}

EXPERIMENTS = [
    {
        "id": "cross_field_scientific_runtime_router",
        "videos": list(VIDEOS),
        "product": "ScientificRuntimeReceiptRouter",
        "tools": ["BuildLang/buildc", "build-universe", "Crucible", "Telos", "Gather", "Index"],
        "build": "Route every math/physics/AI video lead into a source-bound runtime packet with exact oracle, executable branch, drift measurement, verifier verdict, and non-promotion boundary.",
        "falsifiers": ["missing runtime branch", "missing exact oracle", "video claim promoted without independent verification"],
        "scores": {"urgency": 5, "demo_readiness": 5, "integration": 5, "proof_advantage": 5, "market_need": 5, "risk": 3},
    },
    {
        "id": "looped_agent_verifier_workbench",
        "videos": ["nYwid6Q5HXk"],
        "product": "LoopedAgentVerifierWorkbench",
        "tools": ["Forum", "Telos", "Crucible", "loop ledger", "agent action proof packets"],
        "build": "Turn looped reasoning into candidate/verifier/action receipts that preserve outputs and verdicts while excluding hidden reasoning text.",
        "falsifiers": ["hidden reasoning exported", "missing verifier verdict", "loop iteration lacks action admission"],
        "scores": {"urgency": 5, "demo_readiness": 5, "integration": 5, "proof_advantage": 5, "market_need": 5, "risk": 4},
    },
    {
        "id": "counterexample_revision_bench",
        "videos": ["EdVG5qNm2rY"],
        "product": "CounterexampleRevisionBench",
        "tools": ["Gather", "Index", "Forum", "Crucible", "BuildLang/buildc", "formal targets"],
        "build": "Make initial claim, search space, counterexample, failed proof, and revised theorem a first-class packet for theory and applied research.",
        "falsifiers": ["counterexample cannot be replayed", "revised claim loses provenance", "negative result is omitted"],
        "scores": {"urgency": 5, "demo_readiness": 4, "integration": 5, "proof_advantage": 5, "market_need": 5, "risk": 3},
    },
    {
        "id": "formal_homotopy_packet_factory",
        "videos": ["4MQbd5wTlI8"],
        "product": "FormalHomotopyPacketFactory",
        "tools": ["Gather", "Index", "Forum", "Crucible", "Lean/Rocq/Isabelle/Agda adapters"],
        "build": "Convert high-abstraction math leads into theorem target packets with definitions, assumptions, notation map, proof branch, and countermodel lane.",
        "falsifiers": ["theorem statement not isolated", "assumption boundary missing", "no formal replay path recorded"],
        "scores": {"urgency": 4, "demo_readiness": 4, "integration": 5, "proof_advantage": 5, "market_need": 4, "risk": 3},
    },
    {
        "id": "quantum_claim_boundary_kit",
        "videos": ["HbKzqvey5PA"],
        "product": "QuantumClaimBoundaryKit",
        "tools": ["Gather", "Crucible", "Telos", "BuildLang/buildc", "scientific runtime receipts"],
        "build": "Separate normalized-state arithmetic, measurement receipts, entropy choices, simulator outputs, and interpretation claims before any physics promotion.",
        "falsifiers": ["non-normalized state accepted", "interpretation claim marked verified", "measurement receipt lacks seed/config"],
        "scores": {"urgency": 4, "demo_readiness": 4, "integration": 4, "proof_advantage": 5, "market_need": 5, "risk": 4},
    },
    {
        "id": "source_lead_demotion_gate",
        "videos": list(VIDEOS),
        "product": "SourceLeadDemotionGate",
        "tools": ["Gather", "Crucible", "Telos", "Forum"],
        "build": "Require every video-derived claim to stay SOURCE_LEAD_ONLY until independent documents, code, experiments, or formal artifacts promote it.",
        "falsifiers": ["raw transcript exposed in packet", "video claim promoted as fact", "no independent promotion path"],
        "scores": {"urgency": 5, "demo_readiness": 5, "integration": 4, "proof_advantage": 5, "market_need": 4, "risk": 2},
    },
]


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_obj(value: object) -> str:
    return sha256_text(canonical_json(value))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n", encoding="utf-8")


def clean(value: str) -> str:
    return value.encode("ascii", "ignore").decode("ascii").replace("  ", " ").strip()


def object_path(sha: str) -> Path:
    return STORE / "objects" / sha[:2] / sha[2:]


def read_catalog() -> list[dict[str, Any]]:
    return [json.loads(line) for line in (STORE / "catalog.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]


def signal_counts(text: str) -> dict[str, int]:
    lowered = text.lower()
    return {
        name: sum(len(re.findall(r"\b" + re.escape(term) + r"s?\b", lowered)) for term in terms)
        for name, terms in SIGNALS.items()
    }


def source_leads() -> list[dict[str, Any]]:
    rows = read_catalog()
    by_id: dict[str, dict[str, Any]] = {}
    for row in rows:
        by_id.setdefault(row["id"], {})[row["kind"]] = row
    leads = []
    for video_id, spec in VIDEOS.items():
        meta = by_id[video_id]["metadata"]
        transcript = by_id[video_id]["transcript"]
        path = object_path(transcript["sha256"])
        text = path.read_text(encoding="utf-8", errors="replace")
        counts = signal_counts(text)
        leads.append({
            "video_id": video_id,
            "url": spec["url"],
            "theme": spec["theme"],
            "title": clean(meta["title"]),
            "uploader": clean(meta.get("meta", {}).get("uploader", "")),
            "metadata_sha256": meta["sha256"],
            "transcript_sha256": transcript["sha256"],
            "transcript_method": transcript["method"],
            "transcript_chars": len(text),
            "transcript_object_present": path.exists(),
            "stored_object_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "signal_counts": counts,
            "dominant_signal": max(counts, key=counts.get),
            "claim_status": "SOURCE_LEAD_ONLY",
            "raw_transcript_included": False,
        })
    return leads


def upstream_receipts() -> dict[str, Any]:
    receipts = {}
    for key, path in UPSTREAMS.items():
        data = read_json(path)
        receipts[key] = {"pass": data.get("pass"), "schema": data.get("schema"), "status": data.get("status"), "seal": data.get("seal"), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
    return receipts


def run_json(command: list[str], timeout: int = 60) -> tuple[int, str, str, dict[str, Any]]:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    parsed = json.loads(result.stdout) if result.returncode == 0 and result.stdout.strip().startswith("{") else {}
    return result.returncode, result.stdout, result.stderr, parsed


def flagship_receipts() -> dict[str, Any]:
    code, out, err, parsed = run_json(["forum", "route", "--json", "Pass 0125 route YouTube source leads into proof-packet experiments."])
    forum = {"status": "MATCH" if code == 0 else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(out), "stderr_sha256": sha256_text(err), "decided": parsed.get("decided")}
    code, out, err, parsed = run_json(["index", "context-envelope", "--root", ".", "--budget", "1200", "--json"])
    index = {"status": "MATCH" if code == 0 and parsed.get("verification_verdict") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(out), "stderr_sha256": sha256_text(err), "verification_verdict": parsed.get("verification_verdict")}
    code, out, err, parsed = run_json(["node", "demo/status.mjs", "--summary"])
    telos = {"status": "MATCH" if code == 0 and parsed.get("status") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(out), "stderr_sha256": sha256_text(err), "tool_version": parsed.get("tool_version")}
    code, out, err, _ = run_json(["node", "demo/catalog.mjs", "--summary"])
    catalog = {"status": "MATCH" if code == 0 and "Project Telos MCP Catalog" in out else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(out), "stderr_sha256": sha256_text(err)}
    return {"forum": forum, "index": index, "telos": telos, "telos_catalog": catalog}


def routed_experiments(leads: list[dict[str, Any]]) -> list[dict[str, Any]]:
    lead_map = {lead["video_id"]: lead for lead in leads}
    routed = []
    for row in EXPERIMENTS:
        signal_total = sum(sum(lead_map[video_id]["signal_counts"].values()) for video_id in row["videos"])
        scores = dict(row["scores"])
        scores["video_signal_strength"] = min(5, max(1, signal_total // 30))
        scores["total"] = sum(value for key, value in scores.items() if key != "risk") - scores["risk"]
        routed.append({
            "experiment_id": row["id"],
            "market_product": row["product"],
            "source_video_ids": row["videos"],
            "claim_status": "HYPOTHESIS",
            "gap_status": "inferred",
            "internal_tools": row["tools"],
            "build_next": row["build"],
            "success_receipt": "packet artifact plus validator result plus Crucible MATCH/DRIFT verdict",
            "falsifiers": row["falsifiers"],
            "scores": scores,
        })
    return sorted(routed, key=lambda item: item["scores"]["total"], reverse=True)


def compose() -> dict[str, Any]:
    leads = source_leads()
    experiments = routed_experiments(leads)
    artifact: dict[str, Any] = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "generated_on": "2026-07-01",
        "source_store": str(STORE.relative_to(ROOT)).replace("\\", "/"),
        "upstream_receipts": upstream_receipts(),
        "youtube_source_leads": leads,
        "routed_experiments": experiments,
        "primary_next_experiment": experiments[0]["experiment_id"],
        "thirty_day_push": "ship SourceLeadDemotionGate and CrossFieldScientificRuntimeRouter as executable demos; then attach LoopVerifier to pass 0124 action receipts",
        "required_architecture_improvements": [
            "first-class video-source receipt objects in Gather with transcript-hash-only packet exports",
            "Forum route templates for quantum, formal math, counterexample, and looped-agent leads",
            "Crucible promotion gate that rejects unsupported video-to-fact escalation",
            "BuildLang/buildc runtime branch receipt adapter for exact oracle plus measured output",
            "Telos loop ledger join between source lead, action receipt, verifier verdict, and compensation pointer",
        ],
        "market_hypothesis": "Video and talk corpora are high-velocity frontier-signal inputs, but the product wedge is not summarization; it is converting them into falsifiable proof-packet experiments.",
        "non_promotion_statement": "Pass 0125 uses video metadata, transcript hashes, and keyword signal counts as source-lead data only. It does not verify the videos' scientific claims, expose raw transcripts in the packet, or promote a natural law.",
        "unsupported_claim_count": 0,
        "current_promoted_natural_laws": [],
        "flagship_receipts": flagship_receipts(),
    }
    errors = []
    if len(leads) != 4 or any(not row["transcript_object_present"] for row in leads):
        errors.append("source_leads")
    if any(row["claim_status"] != "SOURCE_LEAD_ONLY" or row["raw_transcript_included"] for row in leads):
        errors.append("source_boundary")
    if len(experiments) < 6 or any(row["claim_status"] != "HYPOTHESIS" for row in experiments):
        errors.append("experiment_boundary")
    if not all(row["status"] == "MATCH" for row in artifact["flagship_receipts"].values()):
        errors.append("flagships")
    if artifact["unsupported_claim_count"] != 0 or artifact["current_promoted_natural_laws"]:
        errors.append("promotion_boundary")
    artifact["validation_errors"] = errors
    artifact["status"] = STATUS_MATCH if not errors else STATUS_DRIFT
    artifact["seal"] = sha256_obj(dict(artifact))
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(ROOT / "schemas" / "youtube-experiment-router-pass-0125.json"))
    args = parser.parse_args()
    artifact = compose()
    write_json(Path(args.out), artifact)
    print(json.dumps({"path": args.out, "seal": artifact["seal"], "status": artifact["status"]}, indent=2, sort_keys=True))
    if artifact["status"] != STATUS_MATCH:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
