"""Compose pass 0104 AI4Science claim-to-experiment receipt."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

SCHEMA = "AI4ScienceClaimToExperimentReceipt/v1"
PASS_ID = "0104"
STATUS_MATCH = "AI4SCIENCE_CLAIM_TO_EXPERIMENT_RECEIPT_MATCH"
STATUS_DRIFT = "AI4SCIENCE_CLAIM_TO_EXPERIMENT_RECEIPT_DRIFT"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
YOUTUBE = ROOT / "schemas" / "youtube-research-compounding-packet-pass-0085.json"
ROADMAP = ROOT / "schemas" / "youtube-critical-data-megatool-roadmap-pass-0102.json"


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


def run_json(command: list[str], timeout: int = 45) -> tuple[int, str, str, dict[str, Any]]:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    parsed = json.loads(result.stdout) if result.returncode == 0 and result.stdout.strip().startswith("{") else {}
    return result.returncode, result.stdout, result.stderr, parsed


def source_anchors() -> list[dict[str, str]]:
    return [
        src("FutureHouse", "https://www.futurehouse.org/", "AI agents for research in biology and complex sciences", "official"),
        src("FutureHouse Platform", "https://www.futurehouse.org/research-announcements/launching-futurehouse-platform-ai-agents", "scientific agents via web interface and API", "official"),
        src("Sakana AI Scientist", "https://sakana.ai/ai-scientist/", "automated pipeline for idea generation, literature search, experiments, writing, and review", "official"),
        src("Sakana AI Scientist paper", "https://arxiv.org/abs/2408.06292", "framework for automated open-ended scientific discovery", "primary_paper"),
        src("Microsoft Discovery blog", "https://azure.microsoft.com/en-us/blog/microsoft-discovery-advancing-agentic-rd-at-scale/", "agentic R&D loop for hypotheses, tests, validation, and iteration", "official"),
        src("Microsoft Discovery product", "https://azure.microsoft.com/en-us/solutions/discovery", "enterprise R&D platform spanning idea, execution, analysis, and iteration", "official"),
        src("NVIDIA BioNeMo", "https://docs.nvidia.com/bionemo-framework/latest/main/about/overview/", "biomolecular models and workflows for training, fine-tuning, and inference", "official_docs"),
        src("AlphaFold 3 Nature", "https://www.nature.com/articles/s41586-024-07487-w", "biomolecular interaction structure prediction model", "primary_paper"),
        src("Nextflow", "https://www.nextflow.io/", "scalable, reproducible, portable scientific workflows", "official"),
        src("Snakemake", "https://snakemake.readthedocs.io/", "reproducible and scalable data analysis workflows", "official_docs"),
        src("Benchling", "https://www.benchling.com/", "cloud platform for biotech R&D data, collaboration, and workflows", "official"),
    ]


def src(name: str, url: str, claim: str, kind: str) -> dict[str, str]:
    return {"name": name, "url": url, "source_kind": kind, "direct_claim": claim, "confidence": "high"}


def minimum_fields() -> list[str]:
    return [
        "source_claim",
        "source_receipts",
        "model_or_agent_actions",
        "experiment_or_simulation_protocol",
        "workflow_runtime_receipt",
        "measurement_receipt",
        "statistical_or_scoring_plan",
        "reproduction_status",
        "negative_result_path",
        "reviewer_objections",
        "promotion_verdict",
    ]


def source_to_receipt_map(sources: list[dict[str, str]]) -> list[dict[str, Any]]:
    mapping = {
        "FutureHouse": ["source_claim", "agent_action_receipt", "reviewer_objections"],
        "FutureHouse Platform": ["agent_action_receipt", "workflow_runtime_receipt"],
        "Sakana AI Scientist": ["model_or_agent_actions", "experiment_or_simulation_protocol", "reviewer_objections"],
        "Sakana AI Scientist paper": ["source_claim", "measurement_receipt", "promotion_verdict"],
        "Microsoft Discovery blog": ["hypothesis_receipt", "validation_loop_receipt", "iteration_receipt"],
        "Microsoft Discovery product": ["enterprise_context_receipt", "human_review_receipt"],
        "NVIDIA BioNeMo": ["model_checkpoint_receipt", "training_or_inference_receipt"],
        "AlphaFold 3 Nature": ["primary_paper_receipt", "prediction_measurement_receipt", "experimental_validation_boundary"],
        "Nextflow": ["workflow_runtime_receipt", "container_or_environment_receipt"],
        "Snakemake": ["workflow_runtime_receipt", "reproducibility_receipt"],
        "Benchling": ["lab_record_receipt", "sample_or_entity_lineage_receipt"],
    }
    return [{**source, "required_receipts": mapping[source["name"]], "gap_status": "inferred"} for source in sources]


def next_experiments() -> list[dict[str, Any]]:
    return [
        {
            "experiment_id": "source_claim_to_unverified_protocol",
            "acceptance": ["one biological claim has source receipt", "protocol placeholder is explicit", "promotion verdict remains UNVERIFIABLE"],
            "status": "READY_NEXT",
        },
        {
            "experiment_id": "workflow_runtime_bridge",
            "acceptance": ["Nextflow/Snakemake analog fields map to Telos receipts", "environment and output hashes are required"],
            "status": "READY_AFTER_SCHEMA",
        },
        {
            "experiment_id": "negative_result_and_review_lane",
            "acceptance": ["failed experiment is first-class", "reviewer objections block promotion", "human review is required"],
            "status": "READY_AFTER_MINIMUM_PACKET",
        },
    ]


def forum_route() -> dict[str, Any]:
    prompt = "Pass 0104: AI4Science claim-to-experiment receipt across FutureHouse, Sakana AI Scientist, Microsoft Discovery, BioNeMo, AlphaFold, Nextflow, Snakemake, and Benchling."
    code, stdout, stderr, parsed = run_json(["forum", "route", "--json", prompt], timeout=30)
    return {"status": "MATCH" if code == 0 else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "decided": parsed.get("decided"), "confidence": parsed.get("confidence"), "needs_escalation": parsed.get("needs_escalation"), "top_candidates": parsed.get("candidates", [])[:5]}


def index_receipt() -> dict[str, Any]:
    code, stdout, stderr, parsed = run_json(["index", "context-envelope", "--root", ".", "--budget", "1200", "--json"], timeout=45)
    return {"status": "MATCH" if code == 0 and parsed.get("verification_verdict") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "schema": parsed.get("schema"), "verification_verdict": parsed.get("verification_verdict"), "graph_pack_sha256": parsed.get("recheck", {}).get("graph_pack_sha256"), "source_refs_only": parsed.get("privacy", {}).get("source_refs_only")}


def telos_status() -> dict[str, Any]:
    code, stdout, stderr, parsed = run_json(["node", "demo/status.mjs", "--summary"], timeout=30)
    return {"status": "MATCH" if code == 0 and parsed.get("status") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "tool_version": parsed.get("tool_version"), "tool": parsed.get("tool")}


def validate_artifact(artifact: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if artifact.get("schema") != SCHEMA:
        errors.append("schema")
    if artifact.get("source_summary", {}).get("source_count", 0) < 8:
        errors.append("source_count")
    for field in ["source_claim", "experiment_or_simulation_protocol", "measurement_receipt", "negative_result_path"]:
        if field not in artifact.get("minimum_packet_fields", []):
            errors.append(f"missing_{field}")
    if artifact.get("market_gap", {}).get("gap_status") != "inferred":
        errors.append("gap_status")
    if len(artifact.get("next_experiments", [])) != 3:
        errors.append("next_experiments")
    if any(row.get("status") != "MATCH" for row in artifact.get("flagship_receipts", {}).values()):
        errors.append("flagships")
    if artifact.get("unsupported_claim_count") != 0 or artifact.get("current_promoted_natural_laws") != []:
        errors.append("promotion_boundary")
    return errors


def compose() -> dict[str, Any]:
    youtube = read_json(YOUTUBE)
    roadmap = read_json(ROADMAP)
    sources = source_anchors()
    official_count = sum(1 for row in sources if row["source_kind"] in {"official", "official_docs", "primary_paper"})
    artifact: dict[str, Any] = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "generated_on": "2026-07-01",
        "status": STATUS_DRIFT,
        "source_bindings": {"youtube_pass": youtube["pass"], "roadmap_pass": roadmap["pass"], "roadmap_top_priority": roadmap["top_priority"]},
        "source_summary": {"source_count": len(sources), "official_or_primary_count": official_count, "youtube_ai4science_video_count": 1},
        "source_anchors": sources,
        "minimum_packet_fields": minimum_fields(),
        "source_to_receipt_map": source_to_receipt_map(sources),
        "market_gap": {
            "claim": "AI4Science tools cover agents, models, workflows, and lab records, but the unified claim-to-experiment proof packet remains a Telos wedge hypothesis.",
            "gap_status": "inferred",
            "missing_proof_layers": ["claim provenance", "agent action receipts", "protocol receipts", "measurement receipts", "negative results", "review verdicts"],
        },
        "promotion_gates": {"rejects_unmeasured_discovery_claim": True, "requires_reproduction_status": True, "requires_human_review": True},
        "next_experiments": next_experiments(),
        "negative_fixtures": [
            {"fixture_id": "discovery_claim_without_measurement", "expected_status": "REJECT"},
            {"fixture_id": "prediction_without_experimental_boundary", "expected_status": "REJECT"},
            {"fixture_id": "paper_without_reproduction_status", "expected_status": "REJECT"},
        ],
        "unsupported_claim_count": 0,
        "current_promoted_natural_laws": [],
        "non_promotion_statement": "Pass 0104 maps AI4Science source anchors into receipt requirements. It does not prove biological discovery, drug efficacy, benchmark superiority, or a natural law.",
        "flagship_receipts": {"forum": forum_route(), "index": index_receipt(), "telos": telos_status()},
    }
    artifact["validation_errors"] = validate_artifact(artifact)
    artifact["status"] = STATUS_MATCH if not artifact["validation_errors"] else STATUS_DRIFT
    artifact["measurements"] = [
        {"id": "source_count", "status": "MATCH" if len(sources) >= 8 else "DRIFT"},
        {"id": "official_sources", "status": "MATCH" if official_count >= 8 else "DRIFT"},
        {"id": "minimum_fields", "status": "MATCH" if len(artifact["minimum_packet_fields"]) == 11 else "DRIFT"},
        {"id": "promotion_gates", "status": "MATCH" if all(artifact["promotion_gates"].values()) else "DRIFT"},
        {"id": "flagships", "status": "MATCH" if all(row["status"] == "MATCH" for row in artifact["flagship_receipts"].values()) else "DRIFT"},
        {"id": "promotion_boundary", "status": "MATCH" if artifact["current_promoted_natural_laws"] == [] else "DRIFT"},
    ]
    unsealed = dict(artifact)
    artifact["seal"] = sha256_obj(unsealed)
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(ROOT / "schemas" / "ai4science-claim-to-experiment-receipt-pass-0104.json"))
    args = parser.parse_args()
    artifact = compose()
    write_json(Path(args.out), artifact)
    print(json.dumps({"path": args.out, "seal": artifact["seal"], "status": artifact["status"]}, indent=2, sort_keys=True))
    if artifact["status"] != STATUS_MATCH:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
