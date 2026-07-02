"""Compose pass 0121 YouTube megatool growth-vector receipt."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

SCHEMA = "YoutubeMegatoolGrowthVectorReceipt/v1"
PASS_ID = "0121"
STATUS_MATCH = "YOUTUBE_MEGATOOL_GROWTH_VECTOR_MATCH"
STATUS_DRIFT = "YOUTUBE_MEGATOOL_GROWTH_VECTOR_DRIFT"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
STORE = ROOT / "gather" / "pass-0121-youtube-refresh"
BRIDGE = ROOT / "schemas" / "formal-physics-source-lead-bridge-pass-0116.json"
RUNTIME = ROOT / "schemas" / "hamiltonian-runtime-branch-receipt-pass-0120.json"

URLS = {
    "HbKzqvey5PA": "https://www.youtube.com/watch?v=HbKzqvey5PA",
    "4MQbd5wTlI8": "https://www.youtube.com/watch?v=4MQbd5wTlI8",
    "EdVG5qNm2rY": "https://www.youtube.com/watch?v=EdVG5qNm2rY&t=337s",
    "nYwid6Q5HXk": "https://www.youtube.com/watch?v=nYwid6Q5HXk",
}

SIGNALS = {
    "formal_math": ["category", "homotopy", "proof", "theorem", "mathematics", "axiom", "type", "lean"],
    "quantum_physics": ["born", "entropy", "quantum", "measurement", "probability", "state", "wave", "physics"],
    "counterexample_research": ["counterexample", "disprove", "belief", "computing", "complexity", "problem", "hard", "algorithm"],
    "agent_looping": ["loop", "chain", "thought", "reasoning", "verify", "verifier", "attempt", "feedback"],
    "runtime_compute": ["runtime", "compute", "compiler", "simulation", "branch", "kernel", "optimization", "execute"],
}

PRODUCTS = [
    {
        "vector_id": "formal_homotopy_proof_os",
        "source_video_ids": ["4MQbd5wTlI8"],
        "hypothesis": "Formal math videos point toward a proof OS that carries notation, theorem targets, proof objects, countermodels, and cross-prover receipts.",
        "tools": ["Gather", "Index", "Forum", "Crucible", "Telos", "formal-targets", "BuildLang/buildc"],
        "experiments": [
            "compile the pass 0118 finite-category targets in Lean/Rocq/Isabelle/Agda when available",
            "add proof-object and countermodel slots to every theorem-target packet",
            "score theorem-target portability across proof assistants",
        ],
        "scores": {"urgency": 4, "proof_advantage": 5, "demo_readiness": 4, "integration_leverage": 5, "societal_scale": 4, "risk": 3},
    },
    {
        "vector_id": "quantum_foundation_claim_boundary",
        "source_video_ids": ["HbKzqvey5PA"],
        "hypothesis": "Quantum-foundation claims need packets that separate normalized-state arithmetic, entropy functional choices, measurement models, and interpretation claims.",
        "tools": ["Gather", "Crucible", "Telos", "BuildLang/buildc", "quantum adapters", "loop ledger"],
        "experiments": [
            "build a Born-rule normalization receipt with non-normalized negative fixtures",
            "add entropy-functional receipts that keep interpretation claims as hypotheses",
            "connect simulator and future hardware branches through canonical measurement receipts",
        ],
        "scores": {"urgency": 4, "proof_advantage": 5, "demo_readiness": 4, "integration_leverage": 4, "societal_scale": 5, "risk": 4},
    },
    {
        "vector_id": "counterexample_revision_workbench",
        "source_video_ids": ["EdVG5qNm2rY"],
        "hypothesis": "Research breakthroughs often turn on counterexamples; Telos should make initial claim, search space, counterexample, and revised claim a first-class workflow.",
        "tools": ["Gather", "Index", "Forum", "Crucible", "Telos", "model-foundry", "BuildLang/buildc"],
        "experiments": [
            "run a counterexample-search benchmark over finite combinatorics and optimization claims",
            "record claim lineage from source lead to failed proof to revised theorem target",
            "add falsifier-first scoring to research packets before promotion",
        ],
        "scores": {"urgency": 5, "proof_advantage": 5, "demo_readiness": 5, "integration_leverage": 5, "societal_scale": 5, "risk": 3},
    },
    {
        "vector_id": "looped_agent_verifier_os",
        "source_video_ids": ["nYwid6Q5HXk"],
        "hypothesis": "Looped reasoning should become an accountable verifier loop: attempts, external verdicts, tool authority, and action receipts without exposing hidden reasoning.",
        "tools": ["Forum", "Crucible", "Telos", "loop ledger", "action receipts", "model-foundry"],
        "experiments": [
            "run prover-verifier loops on bounded math and code tasks with hidden reasoning excluded",
            "require every loop iteration to emit candidate, verifier, verdict, and next-action receipt",
            "compare loop policies by final MATCH rate and unsupported-claim count",
        ],
        "scores": {"urgency": 5, "proof_advantage": 5, "demo_readiness": 5, "integration_leverage": 5, "societal_scale": 5, "risk": 4},
    },
    {
        "vector_id": "scientific_runtime_receipt_layer",
        "source_video_ids": ["HbKzqvey5PA", "4MQbd5wTlI8", "EdVG5qNm2rY", "nYwid6Q5HXk"],
        "hypothesis": "The missing bridge across fields is a runtime receipt layer that binds exact oracle, executable branch, numerical drift, compiler state, and verifier verdict.",
        "tools": ["BuildLang/buildc", "build-universe", "Crucible", "Telos", "Hamiltonian runtime bridge", "color calibration"],
        "experiments": [
            "add BuildLang/buildc execution to the pass 0120 Hamiltonian branch when available",
            "add interval/decimal long-horizon drift receipts for symplectic and stochastic kernels",
            "generalize the same branch receipt to color calibration and financial/security kernels",
        ],
        "scores": {"urgency": 5, "proof_advantage": 5, "demo_readiness": 4, "integration_leverage": 5, "societal_scale": 5, "risk": 3},
    },
    {
        "vector_id": "field_to_proof_packet_factory",
        "source_video_ids": ["HbKzqvey5PA", "4MQbd5wTlI8", "EdVG5qNm2rY", "nYwid6Q5HXk"],
        "hypothesis": "Every frontier field should enter through a field-specific proof-packet factory instead of an ad hoc research note.",
        "tools": ["Gather", "Index", "Forum", "Telos", "Crucible", "browser evidence", "model-foundry"],
        "experiments": [
            "define packet templates for math, physics, biology, AI/ML, compute, climate, finance, and security",
            "route each template through Forum and require Crucible claims before roadmap promotion",
            "publish three public demos: formal proof, agent action receipt, and runtime measurement kit",
        ],
        "scores": {"urgency": 4, "proof_advantage": 5, "demo_readiness": 4, "integration_leverage": 5, "societal_scale": 5, "risk": 3},
    },
]


def clean(value: str) -> str:
    return value.encode("ascii", "ignore").decode("ascii").replace("  ", " ").strip()


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


def object_path(sha: str) -> Path:
    return STORE / "objects" / sha[:2] / sha[2:]


def read_catalog() -> list[dict[str, Any]]:
    return [json.loads(line) for line in (STORE / "catalog.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]


def signal_counts(text: str) -> dict[str, int]:
    lowered = text.lower()
    counts: dict[str, int] = {}
    for name, terms in SIGNALS.items():
        counts[name] = sum(len(re.findall(r"\b" + re.escape(term) + r"s?\b", lowered)) for term in terms)
    return counts


def source_leads() -> list[dict[str, Any]]:
    rows = read_catalog()
    by_id: dict[str, dict[str, Any]] = {}
    for row in rows:
        by_id.setdefault(row["id"], {})[row["kind"]] = row
    leads = []
    for video_id in URLS:
        meta = by_id[video_id]["metadata"]
        transcript = by_id[video_id]["transcript"]
        path = object_path(transcript["sha256"])
        text = path.read_text(encoding="utf-8", errors="replace")
        obj_sha = hashlib.sha256(path.read_bytes()).hexdigest()
        counts = signal_counts(text)
        leads.append({
            "video_id": video_id,
            "url": URLS[video_id],
            "title": clean(meta["title"]),
            "uploader": clean(meta.get("meta", {}).get("uploader", "")),
            "metadata_sha256": meta["sha256"],
            "transcript_sha256": transcript["sha256"],
            "stored_object_sha256": obj_sha,
            "transcript_object_present": path.exists(),
            "transcript_chars": len(text),
            "transcript_method": transcript["method"],
            "raw_transcript_included": False,
            "claim_status": "SOURCE_LEAD_ONLY",
            "gap_status": "inferred",
            "signal_counts": counts,
            "dominant_signal": max(counts, key=counts.get),
        })
    return leads


def run_json(command: list[str], timeout: int = 45) -> tuple[int, str, str, dict[str, Any]]:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    parsed = json.loads(result.stdout) if result.returncode == 0 and result.stdout.strip().startswith("{") else {}
    return result.returncode, result.stdout, result.stderr, parsed


def flagship_receipts() -> dict[str, Any]:
    code, out, err, parsed = run_json(["forum", "route", "--json", "Pass 0121 YouTube source-lead megatool growth-vector synthesis."])
    forum = {"status": "MATCH" if code == 0 else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(out), "stderr_sha256": sha256_text(err), "decided": parsed.get("decided"), "confidence": parsed.get("confidence")}
    code, out, err, parsed = run_json(["index", "context-envelope", "--root", ".", "--budget", "1200", "--json"])
    index = {"status": "MATCH" if code == 0 and parsed.get("verification_verdict") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(out), "stderr_sha256": sha256_text(err), "verification_verdict": parsed.get("verification_verdict")}
    code, out, err, parsed = run_json(["node", "demo/status.mjs", "--summary"])
    telos = {"status": "MATCH" if code == 0 and parsed.get("status") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(out), "stderr_sha256": sha256_text(err), "tool_version": parsed.get("tool_version")}
    code, out, err, _ = run_json(["node", "demo/catalog.mjs", "--summary"])
    catalog = {"status": "MATCH" if code == 0 and "Project Telos MCP Catalog" in out else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(out), "stderr_sha256": sha256_text(err)}
    return {"forum": forum, "index": index, "telos": telos, "telos_catalog": catalog}


def scored_products(leads: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_id = {lead["video_id"]: lead for lead in leads}
    products = []
    for row in PRODUCTS:
        signal_total = sum(sum(by_id[vid]["signal_counts"].values()) for vid in row["source_video_ids"])
        scores = dict(row["scores"])
        scores["transcript_signal_strength"] = min(5, max(1, signal_total // 25))
        scores["total"] = sum(value for key, value in scores.items() if key != "risk") - scores["risk"]
        products.append({
            "vector_id": row["vector_id"],
            "source_video_ids": row["source_video_ids"],
            "claim_status": "HYPOTHESIS",
            "gap_status": "inferred",
            "product_hypothesis": row["hypothesis"],
            "internal_tools_combined": row["tools"],
            "next_experiments": [{"experiment": item, "success_receipt": "measured packet with MATCH/DRIFT verdict", "falsifier": "missing receipt, unsupported claim, or branch drift"} for item in row["experiments"]],
            "scores": scores,
        })
    return sorted(products, key=lambda item: item["scores"]["total"], reverse=True)


def integration_map() -> list[dict[str, Any]]:
    return [
        {"node": "Gather", "inputs": ["YouTube URLs", "official docs", "papers"], "outputs": ["source receipts", "content hashes"], "market_product": "source intake ledger"},
        {"node": "Index", "inputs": ["repo", "dogfood artifacts"], "outputs": ["context envelope"], "market_product": "workspace substrate map"},
        {"node": "Forum", "inputs": ["growth vector", "field"], "outputs": ["route candidates"], "market_product": "expert routing layer"},
        {"node": "Crucible", "inputs": ["claims", "measurements"], "outputs": ["MATCH/DRIFT/UNVERIFIABLE verdict"], "market_product": "proof gate"},
        {"node": "Telos", "inputs": ["actions", "loops", "receipts"], "outputs": ["action ledger", "catalog", "status"], "market_product": "accountable agent OS"},
        {"node": "BuildLang/buildc", "inputs": ["proof kernels", "scientific kernels"], "outputs": ["compiler/runtime receipts"], "market_product": "accountable scientific runtime"},
        {"node": "Color calibration", "inputs": ["display measurements", "render outputs"], "outputs": ["measurement truth receipts"], "market_product": "visual truth kit"},
    ]


def compose() -> dict[str, Any]:
    bridge = read_json(BRIDGE)
    runtime = read_json(RUNTIME)
    leads = source_leads()
    products = scored_products(leads)
    artifact: dict[str, Any] = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "generated_on": "2026-07-01",
        "source_bindings": {"youtube_refresh_store": str(STORE.relative_to(ROOT)).replace("\\", "/"), "formal_physics_bridge_pass": bridge["pass"], "formal_physics_bridge_seal": bridge["seal"], "runtime_branch_pass": runtime["pass"], "runtime_branch_seal": runtime["seal"]},
        "youtube_source_leads": leads,
        "growth_vectors": products,
        "primary_30_day_push": products[0]["vector_id"],
        "integration_map": integration_map(),
        "source_policy": "YouTube videos are critical source leads. Metadata, transcript hashes, and derived signal counts are evidence; product implications remain hypotheses until independently verified.",
        "non_promotion_statement": "Pass 0121 does not validate the truth of video claims, expose raw transcripts, solve research problems, or promote a natural law.",
        "unsupported_claim_count": 0,
        "current_promoted_natural_laws": [],
        "flagship_receipts": flagship_receipts(),
    }
    errors = []
    if len(leads) != 4 or not all(row["transcript_object_present"] for row in leads):
        errors.append("youtube_receipts")
    if len(products) < 6 or any(row["claim_status"] != "HYPOTHESIS" for row in products):
        errors.append("growth_vectors")
    if any(row["raw_transcript_included"] for row in leads):
        errors.append("raw_transcript_boundary")
    if any(row["status"] != "MATCH" for row in artifact["flagship_receipts"].values()):
        errors.append("flagships")
    artifact["validation_errors"] = errors
    artifact["status"] = STATUS_MATCH if not errors else STATUS_DRIFT
    artifact["seal"] = sha256_obj(dict(artifact))
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(ROOT / "schemas" / "youtube-megatool-growth-vector-receipt-pass-0121.json"))
    args = parser.parse_args()
    artifact = compose()
    write_json(Path(args.out), artifact)
    print(json.dumps({"path": args.out, "seal": artifact["seal"], "status": artifact["status"]}, indent=2, sort_keys=True))
    if artifact["status"] != STATUS_MATCH:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
