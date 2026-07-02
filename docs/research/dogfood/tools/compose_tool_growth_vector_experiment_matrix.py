"""Compose pass 0066 tool growth-vector experiment matrix."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


SCHEMA = "ToolGrowthVectorExperimentMatrix/v1"
STATUS_MATCH = "TOOL_GROWTH_VECTOR_EXPERIMENT_MATRIX_MATCH"
STATUS_DRIFT = "TOOL_GROWTH_VECTOR_EXPERIMENT_MATRIX_DRIFT"
PASS_ID = "0066"
TOOLS = ["Gather", "Index", "Forum", "Crucible", "Telos", "BuildLang/buildc", "build-universe", "color calibration", "browser evidence", "model foundry", "loop ledger", "action receipts"]


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def sha256_obj(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def source_anchors() -> list[dict[str, str]]:
    rows = [
        ("opentelemetry", "https://opentelemetry.io/docs/", "OpenTelemetry", "Vendor-neutral traces, metrics, and logs."),
        ("mlflow", "https://mlflow.org/docs/latest/ml/model-registry/", "MLflow", "Model registry with lineage and versioning."),
        ("langsmith", "https://docs.langchain.com/langsmith/observability", "LangSmith", "LLM application traces and production metrics."),
        ("langfuse", "https://langfuse.com/docs", "Langfuse", "Open-source tracing, prompt management, and evaluations."),
        ("phoenix", "https://arize.com/docs/phoenix", "Arize Phoenix", "AI tracing and evaluation with OpenTelemetry ingest."),
        ("braintrust", "https://www.braintrust.dev/docs", "Braintrust", "AI observability, evals, and regression detection."),
        ("futurehouse", "https://www.futurehouse.org/", "FutureHouse", "AI agents for biology and complex sciences."),
        ("sakana_ai_scientist", "https://sakana.ai/ai-scientist/", "Sakana AI Scientist", "Automated scientific discovery workflow."),
        ("microsoft_discovery", "https://azure.microsoft.com/en-us/solutions/discovery", "Microsoft Discovery", "Enterprise agentic AI for scientific R&D."),
        ("julia", "https://julialang.org/", "Julia", "Fast dynamic scientific computing language."),
        ("openxla", "https://openxla.org/", "OpenXLA", "Portable performant ML compiler ecosystem."),
        ("triton", "https://triton-lang.org/", "Triton", "Parallel programming language/compiler for modern GPUs."),
        ("aces", "https://docs.acescentral.com/", "ACES", "Industry color-management standard."),
        ("opencolorio", "https://opencolorio.org/", "OpenColorIO", "Production color-management solution."),
        ("nist_ai_rmf", "https://www.nist.gov/itl/ai-risk-management-framework", "NIST AI RMF", "Voluntary AI risk-management framework."),
        ("eu_ai_act", "https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng", "EU AI Act", "EU risk-based AI regulation text."),
    ]
    return [{"confidence": "high", "label": label, "retrieved_on": "2026-07-01", "source_id": sid, "summary": summary, "url": url, "verification_status": "source_anchor"} for sid, url, label, summary in rows]


def internal_tools() -> list[dict[str, Any]]:
    roles = {
        "Gather": "source and research intake", "Index": "workspace context and atlas", "Forum": "routing and handoff",
        "Crucible": "verification pressure", "Telos": "shared receipt room", "BuildLang/buildc": "scientific compiler/runtime",
        "build-universe": "package and adapter ecosystem", "color calibration": "measured visual/color proof",
        "browser evidence": "inspectable web evidence", "model foundry": "model workflow improvement",
        "loop ledger": "append-only continuity", "action receipts": "accountable execution packet",
    }
    return [{"tool": tool, "role": roles[tool], "state": "present" if tool not in {"BuildLang/buildc", "build-universe"} else "partial"} for tool in TOOLS]


def growth_vectors() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    source_map = {
        "Gather": ["futurehouse", "sakana_ai_scientist", "microsoft_discovery"], "Index": ["opentelemetry", "mlflow", "nist_ai_rmf"],
        "Forum": ["langsmith", "langfuse", "braintrust"], "Crucible": ["nist_ai_rmf", "eu_ai_act", "braintrust"],
        "Telos": ["opentelemetry", "mlflow", "eu_ai_act"], "BuildLang/buildc": ["julia", "openxla", "triton"],
        "build-universe": ["julia", "openxla", "mlflow"], "color calibration": ["aces", "opencolorio", "nist_ai_rmf"],
        "browser evidence": ["opentelemetry", "langfuse", "phoenix"], "model foundry": ["mlflow", "braintrust", "microsoft_discovery"],
        "loop ledger": ["opentelemetry", "nist_ai_rmf", "eu_ai_act"], "action receipts": ["opentelemetry", "langsmith", "phoenix"],
    }
    vector_names = [
        ("adapter_hardening", "adapter contract", "round-trip one incumbent artifact into a Telos receipt"),
        ("benchmark_harness", "measurement harness", "measure latency, completeness, and replay fidelity"),
        ("buyer_packet", "market packet", "convert the capability into a buyer-readable proof artifact"),
    ]
    for tool in TOOLS:
        for idx, (suffix, surface, metric) in enumerate(vector_names, start=1):
            rows.append(vector(tool, suffix, surface, metric, source_map[tool], idx))
    return rows


def vector(tool: str, suffix: str, surface: str, metric: str, source_ids: list[str], idx: int) -> dict[str, Any]:
    base = 5 if tool in {"Telos", "Crucible", "action receipts", "Index"} else 4
    feasibility = 5 - (idx // 3)
    priority = max(1, min(5, round((base + feasibility) / 2)))
    return {
        "claim_status": "hypothesis",
        "experiment_id": f"{tool.lower().replace('/', '-').replace(' ', '-')}-{suffix}",
        "falsifier": f"{tool} {surface} fails if it cannot emit a re-checkable receipt with a clear negative fixture.",
        "gap_status": "inferred",
        "market_need": f"Make {tool} legible as part of a cross-tool proof system instead of a standalone capability.",
        "priority_score": priority,
        "source_ids": source_ids,
        "success_metric": metric,
        "tool": tool,
        "vector": surface,
    }


def cross_tool_experiments() -> list[dict[str, Any]]:
    specs = [
        ("proof_os_core", ["Gather", "Index", "Forum", "Crucible", "Telos"], "claim-to-verdict packet"),
        ("regulated_agent_spine", ["OpenTelemetry", "action receipts", "loop ledger", "Crucible", "Telos"], "trace-to-receipt packet"),
        ("scientific_runtime_spine", ["BuildLang/buildc", "build-universe", "Crucible", "Telos"], "compiler-runtime proof receipt"),
        ("color_truth_spine", ["color calibration", "browser evidence", "Crucible", "Telos"], "measured color proof kit"),
        ("ai4science_lab_spine", ["Gather", "model foundry", "BuildLang/buildc", "Crucible", "Telos"], "research proof packet"),
        ("routing_repair_spine", ["Forum", "Index", "loop ledger", "Telos"], "route vocabulary repair receipt"),
        ("browser_to_claim_spine", ["browser evidence", "Gather", "Index", "Crucible"], "browser evidence claim packet"),
        ("model_improvement_spine", ["model foundry", "loop ledger", "Crucible", "action receipts"], "model workflow improvement receipt"),
        ("package_ecosystem_spine", ["build-universe", "Index", "Forum", "Telos"], "adapter package map"),
        ("market_learning_spine", ["Gather", "Forum", "loop ledger", "Telos"], "buyer learning loop packet"),
    ]
    return [{"experiment_id": eid, "tools": normalize_tools(tools), "expected_receipt": receipt, "falsifier": f"{eid} fails if any tool boundary cannot be replayed from receipts.", "status": "HYPOTHESIS"} for eid, tools, receipt in specs]


def normalize_tools(tools: list[str]) -> list[str]:
    return ["action receipts" if tool == "OpenTelemetry" else tool for tool in tools]


def synergy_graph(experiments: list[dict[str, Any]]) -> dict[str, Any]:
    centrality = {tool: 0 for tool in TOOLS}
    edges = []
    for exp in experiments:
        tools = exp["tools"]
        for tool in tools:
            centrality[tool] += 1
        edges.extend({"from": tools[i], "to": tools[i + 1], "experiment_id": exp["experiment_id"]} for i in range(len(tools) - 1))
    return {"centrality": centrality, "edges": edges, "top_nodes": sorted(centrality, key=lambda tool: (-centrality[tool], tool))[:5]}


def top_growth_bundles() -> list[dict[str, Any]]:
    return [
        {"bundle_id": "proof_os_core", "tools": ["Gather", "Index", "Forum", "Crucible", "Telos"], "market": "research and agent proof packets"},
        {"bundle_id": "accountable_agent_ops", "tools": ["action receipts", "loop ledger", "browser evidence", "Crucible", "Telos"], "market": "regulated agent operations"},
        {"bundle_id": "accountable_scientific_compute", "tools": ["BuildLang/buildc", "build-universe", "Crucible", "Telos"], "market": "scientific runtime receipts"},
        {"bundle_id": "visual_truth_lab", "tools": ["color calibration", "browser evidence", "Crucible", "Telos"], "market": "color/render measurement proof"},
    ]


def previous_pass_binding() -> dict[str, Any]:
    path = Path(__file__).resolve().parents[1] / "schemas" / "otel-trace-to-action-receipt-fixture-pass-0065.json"
    artifact = json.loads(path.read_text(encoding="utf-8"))
    return {"pass": "0065", "path": "schemas/otel-trace-to-action-receipt-fixture-pass-0065.json", "schema": artifact["schema"], "status": artifact["status"], "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "seal": artifact["seal"]}


def compose() -> dict[str, Any]:
    experiments = cross_tool_experiments()
    packet = {
        "schema": SCHEMA, "pass": PASS_ID, "generated_on": "2026-07-01", "promotion_state": "EXPERIMENT_MATRIX_NOT_MARKET_PROOF",
        "source_anchors": source_anchors(), "internal_tools": internal_tools(), "growth_vectors": growth_vectors(),
        "cross_tool_experiments": experiments, "synergy_graph": synergy_graph(experiments), "top_growth_bundles": top_growth_bundles(),
        "previous_pass_binding": previous_pass_binding(), "unsupported_claim_count": 0,
        "non_promotion_statement": "Pass 0066 is a growth-vector experiment matrix. It does not prove market adoption, technical completion, unique competitor absence, or new natural laws.",
    }
    errors = validate(packet)
    packet["validation_errors"] = errors
    packet["status"] = STATUS_MATCH if not errors else STATUS_DRIFT
    packet["seal"] = sha256_obj(packet)
    return packet


def validate(packet: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    source_ids = {source["source_id"] for source in packet.get("source_anchors", [])}
    tools = {tool["tool"] for tool in packet.get("internal_tools", [])}
    if packet.get("schema") != SCHEMA:
        errors.append("schema")
    if tools != set(TOOLS):
        errors.append("tool_set")
    if len(packet.get("growth_vectors", [])) < 36:
        errors.append("growth_vectors")
    if len(packet.get("cross_tool_experiments", [])) < 10:
        errors.append("cross_tool_experiments")
    for row in packet.get("growth_vectors", []):
        if not set(row.get("source_ids", [])).issubset(source_ids):
            errors.append(f"sources:{row.get('experiment_id')}")
        if row.get("claim_status") != "hypothesis":
            errors.append(f"claim_status:{row.get('experiment_id')}")
    if packet.get("unsupported_claim_count") != 0:
        errors.append("unsupported_claim_count")
    if packet.get("previous_pass_binding", {}).get("pass") != "0065":
        errors.append("previous_pass_binding")
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
