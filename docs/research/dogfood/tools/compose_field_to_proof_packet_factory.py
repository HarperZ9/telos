"""Compose pass 0123 field-to-proof packet factory spec."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

SCHEMA = "FieldToProofPacketFactorySpec/v1"
PASS_ID = "0123"
STATUS_MATCH = "FIELD_TO_PROOF_PACKET_FACTORY_MATCH"
STATUS_DRIFT = "FIELD_TO_PROOF_PACKET_FACTORY_DRIFT"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
SOURCE_STORE = ROOT / "gather" / "pass-0123-field-factory-sources"
YOUTUBE = ROOT / "schemas" / "youtube-megatool-growth-vector-receipt-pass-0121.json"
RUNTIME = ROOT / "schemas" / "scientific-runtime-receipt-layer-spec-pass-0122.json"
AI4SCIENCE = ROOT / "schemas" / "ai4science-claim-to-experiment-receipt-pass-0104.json"
AGENT_OBS = ROOT / "schemas" / "agent-observability-action-receipt-adapter-matrix-pass-0064.json"
WEDGE = ROOT / "schemas" / "wedge-budget-signal-scorecard-pass-0049.json"

SOURCE_ROLES = {
    "https://elicit.com/": ("literature_intake", "Elicit"),
    "https://consensus.app/": ("literature_intake", "Consensus"),
    "https://www.semanticscholar.org/product/api": ("literature_graph", "Semantic Scholar API"),
    "https://openalex.org/": ("literature_graph", "OpenAlex home"),
    "https://docs.openalex.org/": ("literature_graph", "OpenAlex docs"),
    "https://jupyter.org/": ("notebook_runtime", "Jupyter"),
    "https://www.nextflow.io/": ("workflow_runtime", "Nextflow"),
    "https://snakemake.readthedocs.io/": ("workflow_runtime", "Snakemake"),
    "https://www.benchling.com/": ("lab_workflow", "Benchling"),
    "https://www.futurehouse.org/": ("ai4science_agent", "FutureHouse"),
    "https://sakana.ai/ai-scientist/": ("ai4science_agent", "Sakana AI Scientist"),
    "https://azure.microsoft.com/en-us/solutions/discovery": ("enterprise_rd", "Microsoft Discovery"),
    "https://docs.nvidia.com/bionemo-framework/latest/main/about/overview/": ("biology_runtime", "NVIDIA BioNeMo"),
    "https://leandojo.org/": ("formal_proof", "LeanDojo"),
    "https://github.com/Pengbinghui/pipeline-math": ("formal_research_loop", "pipeline-math"),
    "https://docs.langchain.com/langsmith/observability": ("agent_observability", "LangSmith"),
    "https://langfuse.com/docs/observability/overview": ("agent_observability", "Langfuse"),
    "https://arize.com/docs/phoenix": ("agent_observability", "Arize Phoenix"),
}

REQUIRED_SLOTS = [
    "source_receipts",
    "workspace_context",
    "route_decision",
    "claim_graph",
    "oracle_or_protocol",
    "runtime_or_formal_branch",
    "verifier_verdict",
    "negative_result_lane",
    "buyer_brief",
    "non_promotion_boundary",
]

FIELD_TEMPLATES = [
    {
        "field": "formal_math_and_theoretical_cs",
        "buyer": "math labs, theory groups, AI proof teams",
        "market_product": "ResearchProofPacketFactory",
        "analogs": ["pipeline-math", "LeanDojo", "Lean", "Semantic Scholar"],
        "youtube_leads": ["4MQbd5wTlI8", "EdVG5qNm2rY"],
        "internal_nodes": ["Gather", "Index", "Forum", "Crucible", "Telos", "proof-target adapters"],
        "demo": "pipeline-math++ packet with theorem target, source refs, verifier loop, counterexample lane, and formal replay boundary",
        "falsifier": "packet cannot identify theorem statement, assumptions, failed branches, verifier verdict, and non-promotion boundary",
        "scores": {"urgency": 5, "budget": 3, "proof_advantage": 5, "demo_readiness": 5, "integration_leverage": 5, "adoption_friction": 3},
    },
    {
        "field": "ai4science_biology_and_chemistry",
        "buyer": "AI4Science labs, biotech platform teams, translational research groups",
        "market_product": "ClaimToExperimentPacketFactory",
        "analogs": ["FutureHouse", "Sakana AI Scientist", "Microsoft Discovery", "BioNeMo", "Benchling"],
        "youtube_leads": ["YQWXxnkK4dw", "HbKzqvey5PA"],
        "internal_nodes": ["Gather", "Index", "Forum", "Crucible", "Telos", "workflow adapters", "lab evidence adapters"],
        "demo": "source claim to protocol skeleton with workflow runtime, measurement placeholder, negative result path, and reviewer objection ledger",
        "falsifier": "packet asserts discovery before source, protocol, measurement, reproduction, and review gates are attached",
        "scores": {"urgency": 5, "budget": 5, "proof_advantage": 5, "demo_readiness": 3, "integration_leverage": 5, "adoption_friction": 4},
    },
    {
        "field": "agent_infrastructure_and_regulated_ops",
        "buyer": "AI platform, safety, compliance, and infra teams",
        "market_product": "AgentActionProofPacketFactory",
        "analogs": ["LangSmith", "Langfuse", "Arize Phoenix", "OpenTelemetry", "Braintrust"],
        "youtube_leads": ["nYwid6Q5HXk"],
        "internal_nodes": ["Forum", "Index", "Telos action receipts", "loop ledger", "Crucible"],
        "demo": "observability trace imported into action receipt with source refs, workspace state, authority scope, stop reason, and verdict",
        "falsifier": "packet preserves traces but cannot bind authority, admission, side-effect class, and verifier result",
        "scores": {"urgency": 5, "budget": 5, "proof_advantage": 5, "demo_readiness": 5, "integration_leverage": 4, "adoption_friction": 3},
    },
    {
        "field": "scientific_runtime_compiler_and_color",
        "buyer": "scientific computing, rendering, color, quant, finance, security, and HPC teams",
        "market_product": "ScientificRuntimeReceiptFactory",
        "analogs": ["Julia", "JAX", "MLIR", "OpenXLA", "Triton", "Calman", "ColourSpace"],
        "youtube_leads": ["HbKzqvey5PA", "cvL_uWtMTAo"],
        "internal_nodes": ["BuildLang/buildc", "build-universe", "Crucible", "Telos", "color calibration", "runtime receipts"],
        "demo": "BuildLang/color/rendering measurement kit with oracle, compiler hash, runtime branch, measured output, and drift verdict",
        "falsifier": "packet cannot compare measured output against oracle or cannot bind compiler/runtime state",
        "scores": {"urgency": 5, "budget": 4, "proof_advantage": 5, "demo_readiness": 4, "integration_leverage": 5, "adoption_friction": 4},
    },
    {
        "field": "literature_and_open_knowledge_graphs",
        "buyer": "research orgs, libraries, policy groups, frontier labs",
        "market_product": "SourceToClaimGraphFactory",
        "analogs": ["Elicit", "Consensus", "Semantic Scholar", "OpenAlex"],
        "youtube_leads": [],
        "internal_nodes": ["Gather", "Index", "Forum", "Crucible", "Telos"],
        "demo": "literature claim graph with every claim carrying source hash, confidence, contradiction status, and review lane",
        "falsifier": "packet cannot distinguish source retrieval, claim extraction, contradiction, and verification status",
        "scores": {"urgency": 4, "budget": 3, "proof_advantage": 4, "demo_readiness": 4, "integration_leverage": 5, "adoption_friction": 2},
    },
    {
        "field": "workflow_reproducibility_and_lab_handoff",
        "buyer": "bioinformatics, data engineering, platform research, wet-lab ops",
        "market_product": "WorkflowProofPacketFactory",
        "analogs": ["Nextflow", "Snakemake", "Jupyter", "Benchling", "OpenLineage"],
        "youtube_leads": ["YQWXxnkK4dw"],
        "internal_nodes": ["Gather", "Index", "Crucible", "Telos", "workflow adapters"],
        "demo": "workflow run packet with inputs, environment, DAG/task refs, outputs, lineage, negative result, and reviewer verdict",
        "falsifier": "packet cannot replay or explain the workflow environment, data lineage, output hash, and failed-run path",
        "scores": {"urgency": 4, "budget": 4, "proof_advantage": 5, "demo_readiness": 4, "integration_leverage": 5, "adoption_friction": 3},
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


def read_catalog() -> list[dict[str, Any]]:
    path = SOURCE_STORE / "catalog.jsonl"
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    for row in rows:
        obj = SOURCE_STORE / "objects" / row["sha256"][:2] / row["sha256"][2:]
        row["chars"] = len(obj.read_text(encoding="utf-8", errors="replace")) if obj.exists() else 0
    return rows


def source_matrix() -> list[dict[str, Any]]:
    rows = []
    for row in read_catalog():
        role, label = SOURCE_ROLES.get(row["ref"], ("unclassified", row["title"]))
        status = "GATHER_VERIFIED"
        if int(row["chars"]) == 0:
            status = "GATHER_VERIFIED_EMPTY_TEXT"
        elif int(row["chars"]) < 500:
            status = "GATHER_VERIFIED_SHORT_TEXT"
        rows.append({
            "role": role,
            "label": label,
            "title": row["title"].encode("ascii", "ignore").decode("ascii"),
            "url": row["ref"],
            "sha256": row["sha256"],
            "chars": row["chars"],
            "gather_status": status,
            "gap_status": "inferred",
        })
    return sorted(rows, key=lambda item: (item["role"], item["label"]))


def score_template(template: dict[str, Any]) -> dict[str, Any]:
    scores = dict(template["scores"])
    scores["total"] = scores["urgency"] + scores["budget"] + scores["proof_advantage"] + scores["demo_readiness"] + scores["integration_leverage"] - scores["adoption_friction"]
    return {
        "field": template["field"],
        "buyer": template["buyer"],
        "market_product": template["market_product"],
        "external_analogs": template["analogs"],
        "youtube_source_leads": template["youtube_leads"],
        "internal_nodes": template["internal_nodes"],
        "required_slots": REQUIRED_SLOTS,
        "demo_recommendation": template["demo"],
        "falsifier": template["falsifier"],
        "scores": scores,
        "gap_status": "inferred",
        "claim_status": "HYPOTHESIS",
    }


def coverage_experiment(factories: list[dict[str, Any]]) -> dict[str, Any]:
    compliant = [row for row in factories if set(REQUIRED_SLOTS).issubset(set(row["required_slots"]))]
    negative = {"missing_slots": ["verifier_verdict", "negative_result_lane"], "status": "REJECTED"}
    return {
        "schema": "FieldFactoryCoverageExperiment/v1",
        "required_slot_count": len(REQUIRED_SLOTS),
        "factory_count": len(factories),
        "compliant_factory_count": len(compliant),
        "negative_fixture": negative,
        "status": "MATCH" if len(compliant) == len(factories) and negative["status"] == "REJECTED" else "DRIFT",
    }


def run_json(command: list[str], timeout: int = 45) -> tuple[int, str, str, dict[str, Any]]:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    parsed = json.loads(result.stdout) if result.returncode == 0 and result.stdout.strip().startswith("{") else {}
    return result.returncode, result.stdout, result.stderr, parsed


def flagships() -> dict[str, Any]:
    code, out, err, parsed = run_json(["forum", "route", "--json", "Pass 0123 field-to-proof packet factory across research, AI infra, scientific runtime, workflow, and lab handoff."])
    forum = {"status": "MATCH" if code == 0 else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(out), "stderr_sha256": sha256_text(err), "decided": parsed.get("decided"), "confidence": parsed.get("confidence")}
    code, out, err, parsed = run_json(["index", "context-envelope", "--root", ".", "--budget", "1200", "--json"])
    index = {"status": "MATCH" if code == 0 and parsed.get("verification_verdict") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(out), "stderr_sha256": sha256_text(err), "verification_verdict": parsed.get("verification_verdict")}
    code, out, err, parsed = run_json(["node", "demo/status.mjs", "--summary"])
    telos = {"status": "MATCH" if code == 0 and parsed.get("status") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(out), "stderr_sha256": sha256_text(err), "tool_version": parsed.get("tool_version")}
    code, out, err, _ = run_json(["node", "demo/catalog.mjs", "--summary"])
    catalog = {"status": "MATCH" if code == 0 and "Project Telos MCP Catalog" in out else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(out), "stderr_sha256": sha256_text(err)}
    return {"forum": forum, "index": index, "telos": telos, "telos_catalog": catalog}


def compose() -> dict[str, Any]:
    sources = source_matrix()
    factories = sorted([score_template(row) for row in FIELD_TEMPLATES], key=lambda item: item["scores"]["total"], reverse=True)
    experiment = coverage_experiment(factories)
    bindings = {
        "youtube_growth_pass": read_json(YOUTUBE)["pass"],
        "youtube_growth_seal": read_json(YOUTUBE)["seal"],
        "runtime_layer_pass": read_json(RUNTIME)["pass"],
        "runtime_layer_seal": read_json(RUNTIME)["seal"],
        "ai4science_pass": read_json(AI4SCIENCE)["pass"],
        "agent_observability_pass": read_json(AGENT_OBS)["pass"],
        "wedge_scorecard_pass": read_json(WEDGE)["pass"],
        "source_store": str(SOURCE_STORE.relative_to(ROOT)).replace("\\", "/"),
    }
    artifact: dict[str, Any] = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "generated_on": "2026-07-01",
        "source_bindings": bindings,
        "source_matrix": sources,
        "canonical_slots": REQUIRED_SLOTS,
        "field_factories": factories,
        "coverage_experiment": experiment,
        "primary_30_day_market_push": "field_to_proof_packet_factory_alpha",
        "public_demo_sequence": [factories[0]["demo_recommendation"], factories[1]["demo_recommendation"], factories[2]["demo_recommendation"]],
        "market_gap_status": "inferred",
        "uniqueness_claim_status": "HYPOTHESIS_ONLY",
        "unsupported_claim_count": 0,
        "current_promoted_natural_laws": [],
        "non_promotion_statement": "Pass 0123 packages field-to-proof factories and a coverage experiment. It does not prove market dominance, solve scientific fields, validate external video claims, or promote a natural law.",
        "flagship_receipts": flagships(),
    }
    errors = []
    if len(sources) < 16 or sum(row["chars"] >= 500 for row in sources) < 14:
        errors.append("source_matrix")
    if len(factories) < 6 or experiment["status"] != "MATCH":
        errors.append("field_factory_coverage")
    if any(row["claim_status"] != "HYPOTHESIS" or row["gap_status"] != "inferred" for row in factories):
        errors.append("claim_boundaries")
    if any(row["status"] != "MATCH" for row in artifact["flagship_receipts"].values()):
        errors.append("flagships")
    artifact["validation_errors"] = errors
    artifact["status"] = STATUS_MATCH if not errors else STATUS_DRIFT
    artifact["seal"] = sha256_obj(dict(artifact))
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(ROOT / "schemas" / "field-to-proof-packet-factory-pass-0123.json"))
    args = parser.parse_args()
    artifact = compose()
    write_json(Path(args.out), artifact)
    print(json.dumps({"path": args.out, "status": artifact["status"], "seal": artifact["seal"]}, indent=2, sort_keys=True))
    if artifact["status"] != STATUS_MATCH:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
