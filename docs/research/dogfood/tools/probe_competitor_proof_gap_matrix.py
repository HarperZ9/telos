"""Generate pass 0048 competitor proof-gap market matrix receipts."""
from __future__ import annotations

import hashlib
import json
import urllib.request
from collections import Counter
from pathlib import Path


PASS = "0048"
ROOT = Path(__file__).resolve().parents[1]
PREVIOUS_PACKET = ROOT / "schemas" / "ai4science-proof-market-sources-pass-0047.json"
OUT_PATH = ROOT / "schemas" / "competitor-proof-gap-matrix-pass-0048.json"
FIXTURE_PATH = ROOT / "fixtures" / "competitor-proof-gap-matrix-pass-0048.json"
PACKET_PATH = ROOT / "packets" / "058-competitor-proof-gap-matrix.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0048-competitor-proof-gap-matrix-steelman.md"


ROWS = [
    ("research_ai4science", "pipeline_math", "Research labs and formal math teams", "formal math", "https://github.com/Pengbinghui/pipeline-math", ["prover", "verifier", "Lean"], ["prover-verifier loop", "Lean formalization"], "portable source-to-action-to-verdict packet remains a Telos wedge hypothesis", "inferred"),
    ("research_ai4science", "FutureHouse", "AI4Science labs", "scientific agents", "https://www.futurehouse.org/", ["FutureHouse", "scientific", "agents"], ["scientific agents", "research automation"], "claim provenance and external reproducibility packet are not verified from source", "inferred"),
    ("research_ai4science", "Sakana AI Scientist", "AI research teams", "automated research", "https://sakana.ai/ai-scientist/", ["AI Scientist", "scientific discovery", "peer review"], ["automated discovery", "automated review"], "workspace and action receipts are not verified from source", "inferred"),
    ("research_ai4science", "Microsoft Discovery", "Enterprise R&D organizations", "agentic R&D", "https://azure.microsoft.com/en-us/blog/transforming-rd-with-agentic-ai-introducing-microsoft-discovery/", ["Microsoft Discovery", "agentic AI", "research"], ["agentic research", "enterprise integration"], "portable cross-tool proof packet is not verified from source", "inferred"),
    ("research_ai4science", "NVIDIA BioNeMo", "Bio/pharma AI teams", "bio platform", "https://www.nvidia.com/en-us/industries/healthcare-life-sciences/", ["BioNeMo", "healthcare", "life sciences"], ["bio foundation models", "healthcare/life sciences platform"], "formal claim-to-experiment proof packet is not verified from source", "inferred"),
    ("research_ai4science", "Elicit", "Researchers and analysts", "literature review", "https://elicit.com/", ["Elicit", "research", "papers"], ["paper search", "research assistant"], "execution/action receipts are not verified from source", "inferred"),
    ("research_ai4science", "Consensus", "Researchers and evidence consumers", "scientific search", "https://consensus.app/", ["Consensus", "research", "scientific"], ["scientific search", "evidence summaries"], "workspace-state proof packet is not verified from source", "inferred"),
    ("research_ai4science", "Semantic Scholar API", "Literature graph builders", "literature API", "https://www.semanticscholar.org/product/api", ["Semantic Scholar", "API", "paper"], ["paper metadata API", "literature graph"], "tool/action verification receipts are not verified from source", "inferred"),
    ("research_ai4science", "OpenAlex", "Bibliometrics and research graph teams", "literature graph", "https://docs.openalex.org/", ["OpenAlex", "works", "authors"], ["open scholarly graph", "works/authors metadata"], "model reasoning and proof verdicts are outside the verified source scope", "verified"),
    ("research_ai4science", "Benchling", "Biotech R&D teams", "lab data platform", "https://www.benchling.com/", ["Benchling", "biotech", "research"], ["R&D data platform", "biotech workflows"], "formal proof/replay receipts are not verified from source", "inferred"),
    ("research_ai4science", "Nextflow", "Bioinformatics and data workflow teams", "workflow engine", "https://www.nextflow.io/", ["Nextflow", "workflows", "data"], ["scientific workflows", "pipeline reproducibility"], "LLM action provenance is not verified from source", "inferred"),
    ("research_ai4science", "Snakemake", "Computational biology teams", "workflow engine", "https://snakemake.github.io/", ["Snakemake", "workflow", "data"], ["workflow management", "data analysis"], "model/tool authority receipts are not verified from source", "inferred"),
    ("research_ai4science", "LeanDojo", "Formal methods and theorem proving teams", "formal proving", "https://leandojo.org/", ["LeanDojo", "theorem proving", "Lean"], ["Lean theorem proving", "machine learning interface"], "market-facing research proof packet packaging is not verified from source", "inferred"),
    ("research_ai4science", "DeepMind AlphaProof", "Mathematical AI teams", "formal math", "https://deepmind.google/discover/blog/ai-solves-imo-problems-at-silver-medal-level/", ["AlphaProof", "AlphaGeometry", "International Mathematical Olympiad"], ["formal math reasoning", "IMO benchmark"], "general buyer-facing provenance packet is not verified from source", "inferred"),
    ("research_ai4science", "Jupyter", "Scientific computing teams", "research notebook", "https://jupyter.org/", ["Jupyter", "notebook", "interactive"], ["interactive notebooks", "scientific computing"], "tamper-evident action receipts are not verified from source", "inferred"),
    ("ai_infra_agent_ops", "LangSmith", "AI application teams", "LLM observability", "https://www.langchain.com/langsmith/observability", ["LangSmith", "observability", "traces"], ["observability", "tracing"], "source/workspace/action admission as one proof object is not verified from source", "inferred"),
    ("ai_infra_agent_ops", "Langfuse", "LLM product teams", "LLM observability", "https://langfuse.com/", ["Langfuse", "tracing", "LLM"], ["LLM tracing", "prompt/eval workflows"], "compiler/runtime receipts are not verified from source", "inferred"),
    ("ai_infra_agent_ops", "Arize Phoenix", "AI engineering teams", "AI observability", "https://arize.com/docs/phoenix", ["Phoenix", "tracing", "evaluation"], ["tracing", "evaluation"], "tool authority and action admission proof are not verified from source", "inferred"),
    ("ai_infra_agent_ops", "Braintrust", "AI product teams", "evals and observability", "https://www.braintrust.dev/", ["Braintrust", "evals", "traces"], ["evals", "traces"], "cross-workspace signed action receipt is not verified from source", "inferred"),
    ("ai_infra_agent_ops", "OpenTelemetry", "Platform engineering teams", "observability standard", "https://opentelemetry.io/", ["OpenTelemetry", "observability", "traces"], ["telemetry standard", "traces/metrics/logs"], "domain proof verdict layer is outside verified source scope", "verified"),
    ("ai_infra_agent_ops", "MLflow", "ML platform teams", "ML lifecycle", "https://mlflow.org/", ["MLflow", "machine learning", "models"], ["ML lifecycle", "model tracking"], "agent action authority receipts are not verified from source", "inferred"),
    ("ai_infra_agent_ops", "Weights & Biases", "ML teams", "experiment tracking", "https://docs.wandb.ai/", ["models", "experiments", "artifacts"], ["experiment tracking", "artifact tracking"], "formal source-to-verdict proof packet is not verified from source", "inferred"),
    ("ai_infra_agent_ops", "DVC", "ML/data teams", "data versioning", "https://dvc.org/", ["DVC", "data", "models"], ["data versioning", "model/data pipelines"], "LLM action admission is not verified from source", "inferred"),
    ("ai_infra_agent_ops", "LlamaIndex", "RAG and agent builders", "data/agent framework", "https://www.llamaindex.ai/", ["LlamaIndex", "data", "agents"], ["data framework", "agents"], "durable proof verdict receipts are not verified from source", "inferred"),
    ("ai_infra_agent_ops", "LangGraph", "Agent application teams", "agent orchestration", "https://www.langchain.com/langgraph", ["LangGraph", "agents", "stateful"], ["stateful agents", "orchestration"], "external verification packet is not verified from source", "inferred"),
    ("ai_infra_agent_ops", "Humanloop", "AI product teams", "prompt/eval platform", "https://humanloop.com/docs", ["Humanloop", "evaluations", "prompts"], ["prompt management", "evaluations"], "workspace and tool authority receipts are not verified from source", "inferred"),
    ("ai_infra_agent_ops", "Helicone", "LLM application teams", "LLM observability", "https://www.helicone.ai/", ["Helicone", "observability", "LLM"], ["LLM observability", "requests"], "formal verification receipts are not verified from source", "inferred"),
    ("ai_infra_agent_ops", "promptfoo", "AI safety/eval teams", "LLM evals", "https://www.promptfoo.dev/", ["promptfoo", "LLM", "eval"], ["LLM evals", "red-team testing"], "full source/workspace/action proof object is not verified from source", "inferred"),
    ("ai_infra_agent_ops", "OpenLLMetry", "AI observability teams", "LLM telemetry", "https://www.traceloop.com/openllmetry", ["OpenLLMetry", "LLM", "observability"], ["LLM telemetry", "OpenTelemetry alignment"], "domain verdict and runtime receipts are not verified from source", "inferred"),
    ("ai_infra_agent_ops", "Evidently", "ML monitoring teams", "ML monitoring", "https://www.evidentlyai.com/", ["Evidently", "AI", "monitoring"], ["AI monitoring", "evaluation"], "tool authority and compiler receipts are not verified from source", "inferred"),
    ("visual_compiler_compute", "Julia", "Scientific computing teams", "technical computing language", "https://julialang.org/", ["Julia", "language", "technical computing"], ["technical computing language", "scientific packages"], "action receipts and portable proof packets are not verified from source", "inferred"),
    ("visual_compiler_compute", "Mojo", "AI/performance engineers", "performance language", "https://www.modular.com/mojo", ["Mojo", "Python", "performance"], ["Python-like performance language", "AI systems"], "research proof packet layer is not verified from source", "inferred"),
    ("visual_compiler_compute", "OpenXLA", "ML compiler teams", "ML compiler", "https://openxla.org/", ["OpenXLA", "machine learning", "compiler"], ["ML compiler ecosystem", "accelerated execution"], "source-to-claim verification packet is not verified from source", "inferred"),
    ("visual_compiler_compute", "Chapel", "HPC teams", "parallel programming language", "https://chapel-lang.org/", ["Chapel", "parallel", "programming"], ["parallel programming", "HPC"], "model/tool action provenance is not verified from source", "inferred"),
    ("visual_compiler_compute", "MLIR", "Compiler infrastructure teams", "compiler infrastructure", "https://mlir.llvm.org/", ["MLIR", "compiler", "infrastructure"], ["compiler infrastructure", "intermediate representation"], "buyer-facing proof packet packaging is not verified from source", "inferred"),
    ("visual_compiler_compute", "Triton", "GPU kernel teams", "GPU programming", "https://triton-lang.org/main/index.html", ["Triton", "language", "GPU"], ["GPU programming", "kernels"], "runtime measurement-to-proof packet is not verified from source", "inferred"),
    ("visual_compiler_compute", "ACES", "Color pipeline teams", "color management", "https://docs.acescentral.com/", ["ACES", "Academy", "color"], ["color encoding", "production color pipeline"], "compiler/runtime receipts are not verified from source", "inferred"),
    ("visual_compiler_compute", "OpenColorIO", "VFX/color pipeline teams", "color management", "https://opencolorio.org/", ["OpenColorIO", "color", "management"], ["color management", "configurable pipelines"], "model reasoning/action receipts are not verified from source", "inferred"),
    ("visual_compiler_compute", "Calman", "Display calibration teams", "calibration", "https://www.portrait.com/products/", ["Calman", "color", "calibration"], ["display calibration", "color measurement"], "source-to-runtime proof packet is not verified from source", "inferred"),
    ("visual_compiler_compute", "ColourSpace", "Display calibration teams", "calibration", "https://lightillusion.com/colourspace.html", ["ColourSpace", "colour", "calibration"], ["display profiling", "calibration"], "compiler/action receipts are not verified from source", "inferred"),
    ("visual_compiler_compute", "DaVinci Resolve Color", "Colorists and post teams", "color grading", "https://www.blackmagicdesign.com/products/davinciresolve/color", ["DaVinci Resolve", "color", "grading"], ["color grading", "post-production"], "formal measured-output proof packet is not verified from source", "inferred"),
    ("visual_compiler_compute", "ParaView", "Scientific visualization teams", "visualization", "https://www.paraview.org/", ["ParaView", "visualization", "data"], ["scientific visualization", "large data"], "LLM/tool provenance packet is not verified from source", "inferred"),
    ("visual_compiler_compute", "VTK", "Visualization developers", "visualization toolkit", "https://vtk.org/", ["VTK", "visualization", "data"], ["visualization toolkit", "data processing"], "action-verification receipt layer is not verified from source", "inferred"),
    ("visual_compiler_compute", "CUDA", "GPU computing teams", "GPU computing", "https://developer.nvidia.com/cuda-zone", ["CUDA", "computing"], ["GPU computing", "accelerated software"], "portable proof packet layer is not verified from source", "inferred"),
    ("visual_compiler_compute", "OpenFOAM", "Engineering simulation teams", "CFD simulation", "https://www.openfoam.com/", ["OpenFOAM", "CFD", "fluid"], ["CFD", "simulation"], "model/source/action receipt layer is not verified from source", "inferred"),
]


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def sha256_obj(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def write_json(path: Path, value: object) -> None:
    write_text(path, json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


def with_seal(value: dict) -> dict:
    sealed = dict(value)
    sealed["seal"] = sha256_obj(value)
    return sealed


def fetch_source(row: tuple) -> dict:
    track, tool, _buyer, category, url, needles, _capabilities, _gap, _gap_status = row
    request = urllib.request.Request(url, headers={"User-Agent": "telos-dogfood/0048"})
    with urllib.request.urlopen(request, timeout=35) as response:
        body = response.read()
    text = body.decode("utf-8", errors="replace").lower()
    contains = {needle: needle.lower() in text for needle in needles}
    return {
        "bytes": len(body),
        "category": category,
        "contains": contains,
        "id": tool.lower().replace(" ", "_").replace("/", "_").replace("&", "and"),
        "sha256": sha256_bytes(body),
        "status": "MATCH" if all(contains.values()) else "DRIFT",
        "tool": tool,
        "track": track,
        "url": url,
    }


def market_rows() -> list[dict]:
    rows = []
    for track, tool, buyer, category, url, _needles, capabilities, gap, gap_status in ROWS:
        rows.append({
            "buyer": buyer,
            "capabilities": capabilities,
            "category": category,
            "company_tool": tool,
            "confidence": "moderate",
            "gap_hypothesis": gap,
            "gap_status": gap_status,
            "official_claim": f"Official source positions {tool} around {category}.",
            "sources": [url],
            "track": track,
        })
    return rows


def wedge_scores() -> list[dict]:
    return [
        {"market": "research_proof_packets", "urgency": 5, "budget": 4, "differentiation": 5, "feasibility": 4, "proof_demo_readiness": 4, "risk": 3},
        {"market": "agent_action_proof_packets", "urgency": 5, "budget": 5, "differentiation": 4, "feasibility": 4, "proof_demo_readiness": 5, "risk": 3},
        {"market": "buildlang_scientific_runtime_receipts", "urgency": 4, "budget": 4, "differentiation": 5, "feasibility": 3, "proof_demo_readiness": 3, "risk": 4},
    ]


def megatool_nodes() -> list[dict]:
    return [
        {"internal_tool": "Gather", "external_analogs": ["Elicit", "Consensus", "OpenAlex"], "inputs": ["URLs", "papers", "docs"], "outputs": ["source packets"], "receipts": ["content hash"], "verification_layer": "source reachability", "market_facing_product": "research source intake"},
        {"internal_tool": "Index", "external_analogs": ["Semantic Scholar", "OpenTelemetry"], "inputs": ["workspace", "repo", "docs"], "outputs": ["context envelope"], "receipts": ["graph hash"], "verification_layer": "scope map", "market_facing_product": "workspace provenance"},
        {"internal_tool": "Forum", "external_analogs": ["Humanloop", "Braintrust"], "inputs": ["claims", "routes"], "outputs": ["agent routing", "ledger"], "receipts": ["ledger verification"], "verification_layer": "routing accountability", "market_facing_product": "review board for agent work"},
        {"internal_tool": "Crucible", "external_analogs": ["promptfoo", "Phoenix", "Braintrust"], "inputs": ["thesis", "measurements"], "outputs": ["verdict"], "receipts": ["assessment seal"], "verification_layer": "claim falsification", "market_facing_product": "proof verdict engine"},
        {"internal_tool": "Telos", "external_analogs": ["LangSmith", "Langfuse", "OpenTelemetry"], "inputs": ["action events", "tool use"], "outputs": ["operator receipts"], "receipts": ["doctor/check results"], "verification_layer": "execution accountability", "market_facing_product": "agent action proof packets"},
        {"internal_tool": "BuildLang/buildc", "external_analogs": ["Julia", "Mojo", "MLIR", "OpenXLA"], "inputs": ["source code", "compute kernels"], "outputs": ["compiled artifacts", "runtime measurements"], "receipts": ["compiler/runtime seals"], "verification_layer": "scientific compute replay", "market_facing_product": "accountable scientific runtime"},
        {"internal_tool": "Color calibration", "external_analogs": ["ACES", "OpenColorIO", "Calman", "ColourSpace"], "inputs": ["measurements", "LUTs", "renders"], "outputs": ["calibration packets"], "receipts": ["measured-output hashes"], "verification_layer": "visual output replay", "market_facing_product": "render/color proof kit"},
        {"internal_tool": "build-universe", "external_analogs": ["Nextflow", "Snakemake", "DVC"], "inputs": ["pipelines", "datasets", "jobs"], "outputs": ["workflow receipts"], "receipts": ["run graph seal"], "verification_layer": "workflow reproducibility", "market_facing_product": "science workflow proof fabric"},
    ]


def render_packet(contract: dict) -> str:
    rows = contract["market_rows"]
    lines = [
        "# Packet 058: Competitor Proof-Gap Matrix",
        "",
        "Date: 2026-07-01",
        "",
        f"Status: `{contract['status']}`",
        "",
        "This pass creates a 45-row source-backed market matrix across three tracks.",
        "Gap claims are hypothesis labels unless directly verified by source text.",
        "",
        "```text",
        f"market_row_count = {contract['verifier_measurements']['market_row_count']}",
        f"source_match_count = {contract['verifier_measurements']['source_match_count']}",
        f"research_ai4science_rows = {contract['track_counts']['research_ai4science']}",
        f"ai_infra_agent_ops_rows = {contract['track_counts']['ai_infra_agent_ops']}",
        f"visual_compiler_compute_rows = {contract['track_counts']['visual_compiler_compute']}",
        "uniqueness_claim_status = HYPOTHESIS_ONLY",
        "```",
        "",
        "| Track | Tool | Buyer | Gap status |",
        "| --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(f"| `{row['track']}` | {row['company_tool']} | {row['buyer']} | `{row['gap_status']}` |")
    lines.extend([
        "",
        "Primary 30-day push: publish the agent-action proof packet demo first,",
        "then use it as the execution substrate for pipeline-math++ and BuildLang/color demos.",
        "",
        "Current promoted natural laws: none.",
    ])
    return "\n".join(lines) + "\n"


def render_steelman() -> str:
    return """# Pass 0048 Steelman: Competitor Proof-Gap Matrix

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

This matrix verifies that official source pages are reachable and contain
classification keywords. It does not prove a competitor lacks a capability.
Most gap rows are `inferred` because absence from public positioning is not
evidence of absence. The right use is prioritization: decide which proof packet
demos are worth building and then test them against buyers and deeper product
docs.
"""


def main() -> None:
    previous = read_json(PREVIOUS_PACKET)
    previous_sha = sha256_file(PREVIOUS_PACKET)
    receipts = [fetch_source(row) for row in ROWS]
    rows = market_rows()
    track_counts = dict(Counter(row["track"] for row in rows))
    gap_status_counts = dict(Counter(row["gap_status"] for row in rows))
    all_match = all(row["status"] == "MATCH" for row in receipts)
    fixture = with_seal({
        "generated_on": "2026-07-01",
        "market_rows": rows,
        "pass": PASS,
        "schema": "CompetitorProofGapMatrixFixture/v1",
        "source_receipts": receipts,
    })
    write_json(FIXTURE_PATH, fixture)
    fixture_sha = sha256_file(FIXTURE_PATH)
    contract = with_seal({
        "action_receipt_proposal": {
            "action_id": "act_dogfood_0048_competitor_proof_gap_matrix",
            "authority_class": "read_only_external_source_fetch",
            "event_id": "evt_dogfood_0048_competitor_proof_gap_matrix",
            "event_type": "competitor_proof_gap_matrix_verified",
            "external_call_performed": True,
            "external_write_performed": False,
            "verification_verdict": "MATCH" if all_match else "DRIFT",
        },
        "current_promoted_natural_laws": [],
        "fixture": {"path": "fixtures/competitor-proof-gap-matrix-pass-0048.json", "schema": fixture["schema"], "seal": fixture["seal"], "sha256": fixture_sha},
        "gap_status_counts": gap_status_counts,
        "generated_on": "2026-07-01",
        "market_rows": rows,
        "megatool_nodes": megatool_nodes(),
        "non_promotion_statement": "Pass 0048 is a market research and product strategy artifact. It does not prove market demand, technical uniqueness, scientific truth, or any natural law.",
        "pass": PASS,
        "previous_pass_binding": {"path": "schemas/ai4science-proof-market-sources-pass-0047.json", "seal": previous["seal"], "sha256": previous_sha, "source_status": previous["status"]},
        "public_demo_recommendations": [
            "agent observability-to-action-receipt proof packet",
            "pipeline-math++ formal research proof packet",
            "BuildLang/color/rendering measurement proof kit",
        ],
        "research_claims": [
            {"claim": "45 official source anchors were fetched and keyword-checked.", "confidence": "high", "evidence_url": "local source_receipts", "notes": "Network reachability and keyword presence only.", "verification_status": "verified"},
            {"claim": "Proof-layer gaps represent market hypotheses, not proven absence.", "confidence": "high", "evidence_url": "local gap_status_counts", "notes": "Most rows are inferred by design.", "verification_status": "verified"},
        ],
        "schema": "CompetitorProofGapMatrixSet/v1",
        "source_receipts": receipts,
        "status": "COMPETITOR_PROOF_GAP_MATRIX_MATCH" if all_match else "COMPETITOR_PROOF_GAP_MATRIX_DRIFT",
        "track_counts": track_counts,
        "uniqueness_claim_status": "HYPOTHESIS_ONLY",
        "verifier_measurements": {"market_row_count": len(rows), "source_count": len(receipts), "source_match_count": sum(1 for row in receipts if row["status"] == "MATCH"), "wedge_score_count": 3},
        "wedge_scores": wedge_scores(),
    })
    write_json(OUT_PATH, contract)
    write_text(PACKET_PATH, render_packet(contract))
    write_text(STEELMAN_PATH, render_steelman())
    print(json.dumps({
        "market_row_count": len(rows),
        "path": str(OUT_PATH),
        "seal": contract["seal"],
        "source_match_count": contract["verifier_measurements"]["source_match_count"],
        "status": contract["status"],
        "track_counts": track_counts,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
