"""Compose pass 0063 frontier problem-to-proof opportunity map."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


SCHEMA = "FrontierProblemToProofOpportunityMap/v1"
STATUS_MATCH = "FRONTIER_PROBLEM_TO_PROOF_OPPORTUNITY_MAP_MATCH"
STATUS_DRIFT = "FRONTIER_PROBLEM_TO_PROOF_OPPORTUNITY_MAP_DRIFT"
PASS_ID = "0063"


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def sha256_obj(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def source_anchors() -> list[dict[str, str]]:
    return [
        src("microsoft_discovery", "https://azure.microsoft.com/en-us/solutions/discovery", "Microsoft Discovery", "Enterprise agentic AI platform for scientific research, R&D, and advanced scientific computing.", "high"),
        src("futurehouse", "https://www.futurehouse.org/", "FutureHouse", "Non-profit building AI agents to automate research in biology and other complex sciences.", "high"),
        src("sakana_ai_scientist", "https://sakana.ai/ai-scientist/", "Sakana AI Scientist", "System positioned as automating the research lifecycle from ideas through experiments and manuscript writing.", "high"),
        src("pipeline_math", "https://github.com/Pengbinghui/pipeline-math", "pipeline-math", "Public prover-verifier style math pipeline and proof-discovery repository.", "medium"),
        src("openai_unit_distance", "https://openai.com/index/model-disproves-discrete-geometry-conjecture/", "OpenAI unit-distance result", "OpenAI describes a model-discovered discrete geometry construction and companion proof material.", "high"),
        src("leandojo", "https://leandojo.org/leandojo.html", "LeanDojo", "Toolkit for training, evaluating, and deploying AI-assisted theorem provers for Lean 4.", "high"),
        src("cuda_q", "https://developer.nvidia.com/cuda-q", "NVIDIA CUDA-Q", "Open-source quantum development platform spanning CPU, GPU, and QPU resources.", "high"),
        src("alphafold", "https://deepmind.google/science/alphafold/", "Google DeepMind AlphaFold", "AlphaFold Server gives non-commercial researchers access to AlphaFold 3 structure prediction capabilities.", "high"),
        src("materials_project", "https://next-gen.materialsproject.org/api", "Materials Project API", "Open materials data access and API for computed information on known and predicted materials.", "high"),
        src("mlflow", "https://mlflow.org/docs/latest/ml/model-registry/", "MLflow Model Registry", "Centralized model store with lineage, versioning, aliases, metadata tagging, and annotation.", "high"),
        src("opentelemetry", "https://opentelemetry.io/docs/", "OpenTelemetry", "Vendor-neutral framework for telemetry such as traces, metrics, and logs.", "high"),
        src("julia", "https://julialang.org/", "Julia", "Fast, dynamic, open-source language with a scientific and data ecosystem.", "high"),
        src("mojo", "https://www.modular.com/blog/the-path-to-mojo-1-0", "Mojo", "Language vision for targeting CPUs, GPUs, and accelerators with Python-like syntax and systems capabilities.", "medium"),
        src("openxla", "https://openxla.org/", "OpenXLA", "Open ecosystem for performant, portable, extensible ML infrastructure components.", "high"),
        src("triton", "https://triton-lang.org/", "Triton", "Language and compiler for parallel programming on modern GPU hardware.", "high"),
        src("opencolorio", "https://opencolorio.org/", "OpenColorIO", "Color management solution for motion picture production, VFX, and computer animation.", "high"),
        src("aces", "https://docs.acescentral.com/", "ACES documentation", "Industry standard for managing color and digital files through media production lifecycles.", "high"),
        src("calman", "https://www.portrait.com/products/", "Calman", "Calibration and validation software with professional display workflows and reports.", "high"),
        src("colourspace", "https://lightillusion.com/colourspace.html", "ColourSpace", "3D LUT display calibration and color-management software for color-critical workflows.", "high"),
    ]


def src(source_id: str, url: str, label: str, summary: str, confidence: str) -> dict[str, str]:
    return {
        "confidence": confidence,
        "label": label,
        "retrieved_on": "2026-07-01",
        "source_id": source_id,
        "summary": summary,
        "url": url,
        "verification_status": "source_anchor",
    }


def opportunity_rows() -> list[dict[str, Any]]:
    return [
        row("formal_math_theoretical_cs", "Formal math and theoretical CS proof discovery", "math labs, theoretical CS groups, AI reasoning teams",
            ["pipeline-math", "LeanDojo", "OpenAI unit-distance result"], ["pipeline_math", "leandojo", "openai_unit_distance"],
            "Frontier proof work needs source provenance, conjecture state, prover-verifier traces, formalization status, and human review in one packet.",
            "Hypothesis: Telos can win by packaging a claim-to-proof object that connects source intake, workspace state, model attempts, Lean or checker status, Crucible verdicts, and publication artifacts.",
            "Pipeline-math++ proof packet with source anchors, solver attempts, verifier critiques, Lean status, negative cases, and Crucible claims.",
            ["Gather", "Index", "Forum", "Crucible", "Telos", "BuildLang/buildc", "model foundry", "loop ledger"], ["dogfood proof packets", "Crucible registry", "Forum routing", "Index context envelopes"], ["Lean adapter receipts", "formalization queue", "proof-attempt replay UI", "reviewer-facing packet export"], 5, 3, 5, 4, 5, 3),
        row("agentic_ai4science", "Agentic AI4Science R&D platforms", "research labs, industrial R&D, AI4Science teams",
            ["Microsoft Discovery", "FutureHouse", "Sakana AI Scientist"], ["microsoft_discovery", "futurehouse", "sakana_ai_scientist"],
            "AI4Science platforms automate fragments of research, but buyers still need accountable provenance from literature to hypothesis to experiment to verdict.",
            "Hypothesis: Telos can differentiate as the proof layer beneath AI scientist workflows rather than another closed research assistant.",
            "AI4Science claim packet joining literature receipts, hypothesis graph, experiment command, result digest, failed checks, and reviewer notes.",
            ["Gather", "Index", "Forum", "Crucible", "Telos", "browser evidence", "action receipts", "model foundry"], ["Learning Forge", "research seeds", "browser evidence packets", "action receipts"], ["domain-specific experiment adapters", "buyer-ready R&D dashboard", "permissioned lab data boundary", "benchmark suite"], 5, 4, 5, 3, 4, 4),
        row("quantum_hpc_algorithms", "Quantum, hybrid HPC, and accelerator algorithms", "quantum software teams, HPC labs, accelerator platform groups",
            ["CUDA-Q", "OpenXLA", "Triton"], ["cuda_q", "openxla", "triton"],
            "Hybrid CPU/GPU/QPU work needs reproducible kernel, compiler, backend, simulator, hardware, and measurement receipts.",
            "Hypothesis: BuildLang/buildc plus Telos receipts can make hybrid scientific kernels auditable across compilation and execution boundaries.",
            "Hybrid kernel proof packet with source hash, compiler flags, backend target, simulator or hardware class, numeric result, invariant check, and Crucible verdict.",
            ["BuildLang/buildc", "build-universe", "Telos", "Crucible", "Index", "action receipts"], ["Build runtime receipt schema", "action receipt fixtures", "compatibility doctor"], ["CUDA-Q/OpenXLA/Triton analog matrix", "compiler target receipts", "hardware benchmark harness", "numeric invariant library"], 4, 4, 5, 3, 3, 4),
        row("biology_protein_drug_discovery", "Biology, protein modeling, and drug discovery", "biology labs, biotech R&D, translational research teams",
            ["AlphaFold", "FutureHouse", "Microsoft Discovery"], ["alphafold", "futurehouse", "microsoft_discovery"],
            "Biology tools produce strong predictions and research assistance, but wet-lab, model, source, and review evidence often live in separate systems.",
            "Hypothesis: Telos can supply preclinical claim packets that do not claim lab truth, but bind model prediction, source evidence, assumptions, and validation status.",
            "Protein-claim proof packet with literature receipts, model output hash, structure source, uncertainty label, wet-lab status, and explicit non-clinical boundary.",
            ["Gather", "Index", "Forum", "Crucible", "Telos", "model foundry", "action receipts"], ["source receipt pattern", "non-promotion policies", "research packet ledgers"], ["biology ontology adapter", "wet-lab status schema", "safety review gates", "partner-data privacy envelope"], 5, 5, 4, 2, 3, 5),
        row("materials_climate_energy", "Materials, climate, and energy discovery", "materials labs, climate tech teams, energy R&D organizations",
            ["Materials Project", "Microsoft Discovery", "OpenXLA"], ["materials_project", "microsoft_discovery", "openxla"],
            "Materials and climate work depends on data provenance, simulation assumptions, units, model versions, and reproducibility across tools.",
            "Hypothesis: Telos can act as a receipt bus joining public datasets, simulation kernels, model forecasts, and verification gates.",
            "Materials candidate packet with dataset source, query digest, model/simulation command, units, uncertainty, falsifiers, and measurement plan.",
            ["Gather", "Index", "Crucible", "Telos", "BuildLang/buildc", "build-universe"], ["research seeds", "scientific runtime receipt schema", "Crucible measurement packets"], ["dataset adapters", "unit schema", "simulation runner", "open benchmark backlog"], 5, 4, 4, 3, 3, 4),
        row("buildlang_scientific_runtime", "Scientific compiler/runtime and accountable language layer", "scientific computing teams, quant teams, finance modeling, security engineering",
            ["Julia", "Mojo", "OpenXLA", "Triton"], ["julia", "mojo", "openxla", "triton"],
            "Scientific languages and compiler stacks optimize speed and expressiveness, but usually leave proof packets, receipts, and external verdicts outside the language runtime.",
            "Hypothesis: BuildLang/buildc can own accountable scientific computing by making source, compiler, runtime, measurement, and verifier receipts native.",
            "BuildLang runtime proof kit for a PDE, color transform, or quant kernel with compiler receipt, numeric invariant, failure fixture, and Crucible verdict.",
            ["BuildLang/buildc", "build-universe", "Crucible", "Telos", "Index", "action receipts"], ["Build runtime receipt schema", "Build color measurement receipts", "agent action composer contract"], ["native buildc execution harness", "stdlib proof receipt primitives", "benchmarks against Julia/Mojo/Triton", "package docs"], 5, 4, 5, 4, 4, 4),
        row("agent_observability_action_receipts", "AI infrastructure, observability, and accountable agent actions", "AI platform teams, regulated automation teams, internal developer platforms",
            ["OpenTelemetry", "MLflow", "LangSmith/Langfuse class tools"], ["opentelemetry", "mlflow"],
            "Observability and ML lifecycle tools capture traces, metrics, runs, and models, but action admission, authority, workspace state, and verifier verdicts are rarely bound as one portable object.",
            "Hypothesis: Telos can be the accountable execution layer above observability, producing action proof packets for high-stakes workflows.",
            "Agent action packet with source refs, tool authority, command/material digest, trace refs, stop reason, verification verdict, and compensation pointer.",
            ["Gather", "Index", "Forum", "Crucible", "Telos", "loop ledger", "action receipts", "browser evidence"], ["action receipt fixtures", "loop ledger", "browser evidence smoke", "Forum route ledgers"], ["OTel adapter", "MLflow/W&B adapter", "policy admission UI", "customer-ready SDK"], 5, 5, 5, 4, 5, 3),
        row("color_rendering_calibration", "Color, rendering, and calibration proof kits", "VFX teams, display QA teams, imaging labs, visual AI dataset reviewers",
            ["ACES", "OpenColorIO", "Calman", "ColourSpace"], ["aces", "opencolorio", "calman", "colourspace"],
            "Color pipelines have standards and calibration tools, but measured outputs, transform code, display state, and verifier receipts are not usually portable claim objects.",
            "Hypothesis: Telos plus Build Color can make color-critical outputs reviewable as proof packets instead of screenshots or tool-native reports alone.",
            "BuildLang/color measurement kit with transform source, ICC/LUT refs, display target, delta metrics, artifact hashes, and Crucible measurement gate.",
            ["BuildLang/buildc", "color calibration", "Crucible", "Telos", "Gather", "Index", "browser evidence"], ["display calibration contract", "color market map", "Build color proof kit", "measurement layers"], ["OCIO/ACES adapter", "Calman/ColourSpace report importer", "visual diff harness", "gallery-grade demo"], 4, 3, 5, 4, 5, 3),
    ]


def row(domain_id: str, category: str, buyer: str, analogs: list[str], source_ids: list[str], need: str,
        wedge: str, demo: str, internal: list[str], exists: list[str], integration: list[str],
        urgency: int, budget: int, differentiation: int, feasibility: int, readiness: int, risk: int) -> dict[str, Any]:
    return {
        "already_exists_in_monorepo": exists,
        "buyer": buyer,
        "category": category,
        "confidence": "moderate",
        "domain_id": domain_id,
        "external_analogs": analogs,
        "gap_status": "inferred",
        "integration_packaging_work": integration,
        "internal_tool_bundle": internal,
        "market_need": need,
        "primary_wedge_hypothesis": wedge,
        "proof_demo": demo,
        "score_inputs": {
            "budget": budget,
            "differentiation": differentiation,
            "feasibility": feasibility,
            "proof_demo_readiness": readiness,
            "risk": risk,
            "urgency": urgency,
        },
        "source_ids": source_ids,
        "uniqueness_claim_status": "hypothesis",
    }


def wedge_scores(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    scores = []
    for item in rows:
        s = item["score_inputs"]
        total = round((2 * s["urgency"]) + (1.5 * s["budget"]) + (2 * s["differentiation"]) + (1.5 * s["feasibility"]) + (1.5 * s["proof_demo_readiness"]) - s["risk"], 2)
        scores.append({"market": item["domain_id"], "primary_buyer": item["buyer"], "weighted_total": total, **s})
    scores.sort(key=lambda value: (-value["weighted_total"], value["risk"], value["market"]))
    for rank, score in enumerate(scores, start=1):
        score["rank"] = rank
    return scores


def megatool_nodes() -> list[dict[str, Any]]:
    data = [
        ("Gather", "present", ["sources", "papers", "docs", "browser captures"], ["source receipts", "hashes"], "Research intake and source provenance layer"),
        ("Index", "present", ["workspace roots", "source refs", "artifacts"], ["context envelopes", "workspace maps"], "Workspace atlas and context-pack layer"),
        ("Forum", "present", ["task request", "route vocabulary", "ledger state"], ["route receipts", "handoffs"], "Routing and operator-facing reasoning layer"),
        ("Crucible", "present", ["claims", "measurements", "criteria"], ["MATCH/DRIFT/UNVERIFIABLE verdicts"], "Verification pressure and proof gate"),
        ("Telos", "present", ["flagship outputs", "actions", "context packs"], ["action envelopes", "loop ledgers"], "Shared receipt room and product shell"),
        ("BuildLang/buildc", "partial", ["scientific kernels", "compiler inputs"], ["compiler/runtime receipts"], "Accountable scientific language and runtime"),
        ("build-universe", "source_lead", ["packages", "runtime targets", "domain adapters"], ["adapter receipts", "compatibility receipts"], "Package and domain-adapter universe"),
        ("color calibration", "present", ["ICC/LUT/report refs", "display targets"], ["measurement packets", "calibration contracts"], "Color/render proof kit"),
        ("browser evidence", "present", ["web pages", "screens", "DOM refs"], ["browser evidence packets"], "Inspectable evidence capture for demos and web research"),
        ("model foundry", "present", ["model configs", "evals", "training or tuning leads"], ["bounded foundry packets"], "Model-workflow improvement lane"),
        ("loop ledger", "present", ["attempts", "route changes", "verification events"], ["append-only loop records"], "Dogfood continuity and replay spine"),
        ("action receipts", "present", ["tool calls", "commands", "authority class", "materials"], ["portable action proof packets"], "Accountable agent execution layer"),
    ]
    return [
        {
            "already_exists_state": exists,
            "external_analogs": [],
            "inputs": inputs,
            "internal_tool": tool,
            "market_facing_product": product,
            "needed_integration": ["standardize schema bindings", "connect to public demo packet", "add buyer-facing summary"],
            "outputs": outputs,
            "receipts": outputs,
            "verification_layer": "Crucible plus local validators",
        }
        for tool, exists, inputs, outputs, product in data
    ]


def demo_recommendations() -> list[dict[str, str]]:
    return [
        {"demo_id": "pipeline_math_plus_plus", "name": "Pipeline-math++ formal research proof packet", "promotion_state": "DEMO_NOT_PRODUCT_MARKET_FIT", "success_metric": "one public theorem or bounded identity packet with source, solver, verifier, formalization, and Crucible verdicts"},
        {"demo_id": "agent_action_receipt", "name": "Agent observability-to-action-receipt proof packet", "promotion_state": "DEMO_NOT_PRODUCT_MARKET_FIT", "success_metric": "one agent run with OTel-style trace refs, source refs, admission decision, stop reason, verification, and compensation pointer"},
        {"demo_id": "build_color_measurement_kit", "name": "BuildLang/color/rendering measurement proof kit", "promotion_state": "DEMO_NOT_PRODUCT_MARKET_FIT", "success_metric": "one color transform or render measurement with source hash, runtime receipt, numeric threshold, visual artifact, and Crucible gate"},
    ]


def compose() -> dict[str, Any]:
    anchors = source_anchors()
    rows = opportunity_rows()
    packet = {
        "schema": SCHEMA,
        "current_promoted_natural_laws": [],
        "demo_recommendations": demo_recommendations(),
        "forum_route_observation": {
            "status": "ESCALATED",
            "finding": "A broad cross-domain pass spanning AI4Science, compiler systems, rendering, market strategy, and proof packets did not cleanly route to one Forum lane; record as vocabulary and lane-composition gap.",
        },
        "generated_on": "2026-07-01",
        "megatool_nodes": megatool_nodes(),
        "non_promotion_statement": "Pass 0063 is a market and architecture planning artifact. It does not prove product-market fit, scientific novelty, unique competitive absence, new physics, or buyer adoption.",
        "opportunity_rows": rows,
        "pass": PASS_ID,
        "source_anchors": anchors,
        "unsupported_uniqueness_claim_count": 0,
        "wedge_scores": wedge_scores(rows),
    }
    errors = validate(packet)
    packet["validation_errors"] = errors
    packet["status"] = STATUS_MATCH if not errors else STATUS_DRIFT
    packet["seal"] = sha256_obj(packet)
    return packet


def validate(packet: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    source_ids = {item.get("source_id") for item in packet.get("source_anchors", [])}
    if packet.get("schema") != SCHEMA:
        errors.append("schema")
    if len(source_ids) < 16:
        errors.append("source_anchor_count")
    if len(packet.get("opportunity_rows", [])) < 8:
        errors.append("opportunity_row_count")
    if len(packet.get("demo_recommendations", [])) != 3:
        errors.append("demo_recommendations")
    if packet.get("unsupported_uniqueness_claim_count") != 0:
        errors.append("unsupported_uniqueness_claim_count")
    if packet.get("current_promoted_natural_laws") != []:
        errors.append("natural_law_promotion")
    for item in packet.get("opportunity_rows", []):
        if not set(item.get("source_ids", [])).issubset(source_ids):
            errors.append(f"unknown_source:{item.get('domain_id')}")
        if item.get("uniqueness_claim_status") != "hypothesis":
            errors.append(f"uniqueness_status:{item.get('domain_id')}")
        if item.get("gap_status") not in {"verified", "inferred", "unverified"}:
            errors.append(f"gap_status:{item.get('domain_id')}")
    required_nodes = {"Gather", "Index", "Forum", "Crucible", "Telos", "BuildLang/buildc", "build-universe", "color calibration", "browser evidence", "model foundry", "loop ledger", "action receipts"}
    nodes = {node.get("internal_tool") for node in packet.get("megatool_nodes", [])}
    if not required_nodes.issubset(nodes):
        errors.append("megatool_nodes")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    packet = compose()
    write_json(Path(args.out), packet)
    print(json.dumps({"out": args.out, "seal": packet["seal"], "status": packet["status"]}, indent=2, sort_keys=True))
    if packet["status"] != STATUS_MATCH:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
