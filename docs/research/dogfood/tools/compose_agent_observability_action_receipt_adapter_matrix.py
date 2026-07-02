"""Compose pass 0064 agent observability action-receipt adapter matrix."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


SCHEMA = "AgentObservabilityActionReceiptAdapterMatrix/v1"
STATUS_MATCH = "AGENT_OBSERVABILITY_ACTION_RECEIPT_ADAPTER_MATRIX_MATCH"
STATUS_DRIFT = "AGENT_OBSERVABILITY_ACTION_RECEIPT_ADAPTER_MATRIX_DRIFT"
PASS_ID = "0064"


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def sha256_obj(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def source_anchors() -> list[dict[str, str]]:
    return [
        src("langsmith", "https://docs.langchain.com/langsmith/observability", "LangSmith", "Observability for LLM applications from individual traces to production metrics."),
        src("langfuse", "https://langfuse.com/docs", "Langfuse", "Open-source AI engineering platform for tracing, prompt management, evaluations, and analytics."),
        src("phoenix", "https://arize.com/docs/phoenix", "Arize Phoenix", "AI observability with tracing for model calls, retrieval, tool use, and custom logic."),
        src("braintrust", "https://www.braintrust.dev/docs", "Braintrust", "AI observability platform for measuring, evaluating, and improving AI in production."),
        src("opentelemetry", "https://opentelemetry.io/docs/", "OpenTelemetry", "Vendor-neutral framework for traces, metrics, and logs."),
        src("mlflow", "https://mlflow.org/docs/latest/ml/model-registry/", "MLflow", "Model registry with lineage, versioning, aliases, metadata, and annotation support."),
        src("weave", "https://docs.wandb.ai/weave", "W&B Weave", "Observability and evaluation platform for tracking, evaluating, and improving agents and LLM apps."),
        src("dvc", "https://doc.dvc.org/start/data-pipelines/data-pipelines", "DVC", "Versioned data pipelines for organizing and reproducing data science and ML workflows."),
        src("promptfoo", "https://www.promptfoo.dev/docs/intro/", "promptfoo", "Open-source CLI and library for evaluating and red-teaming LLM apps."),
        src("helicone", "https://docs.helicone.ai/gateway/overview", "Helicone", "AI gateway with unified provider API, routing, fallbacks, and observability."),
    ]


def src(source_id: str, url: str, label: str, summary: str) -> dict[str, str]:
    return {"confidence": "high", "label": label, "retrieved_on": "2026-07-01", "source_id": source_id, "summary": summary, "url": url, "verification_status": "source_anchor"}


def adapter_rows() -> list[dict[str, Any]]:
    return [
        adapter("LangSmith", "langsmith", "LLM app and agent observability", ["traces", "production metrics", "integrations"], ["trace_ref", "run_url", "evaluation_ref"], 5),
        adapter("Langfuse", "langfuse", "open-source AI engineering and LLM observability", ["traces", "prompt management", "evaluations", "datasets"], ["trace_id", "prompt_version", "score_ref"], 5),
        adapter("Arize Phoenix", "phoenix", "AI observability and evaluation", ["OpenTelemetry ingest", "tracing", "annotations", "sessions"], ["span_id", "trace_id", "annotation_ref"], 5),
        adapter("Braintrust", "braintrust", "AI observability and evals", ["traces", "experiments", "evals", "regression detection"], ["experiment_id", "trace_ref", "eval_ref"], 5),
        adapter("OpenTelemetry", "opentelemetry", "vendor-neutral telemetry substrate", ["traces", "metrics", "logs", "collector"], ["trace_id", "span_id", "metric_ref", "log_ref"], 5),
        adapter("MLflow", "mlflow", "model lifecycle and lineage", ["model registry", "lineage", "versioning", "metadata"], ["run_id", "model_version", "artifact_uri"], 4),
        adapter("W&B Weave", "weave", "agent and LLM app evaluation", ["tracing", "evaluations", "experiments"], ["call_ref", "evaluation_ref", "dataset_ref"], 4),
        adapter("DVC", "dvc", "data pipeline reproducibility", ["versioned pipelines", "Git-backed workflow", "reproducible DAGs"], ["dvc_stage", "data_hash", "pipeline_ref"], 3),
        adapter("promptfoo", "promptfoo", "LLM evals and red teaming", ["evals", "red teaming", "CI checks"], ["eval_report", "red_team_case", "ci_result"], 4),
        adapter("Helicone", "helicone", "LLM gateway and observability", ["provider routing", "fallbacks", "request logging", "observability"], ["request_id", "provider_route", "cost_ref"], 4),
    ]


def adapter(tool: str, source_id: str, category: str, official_capabilities: list[str], native_refs: list[str], priority: int) -> dict[str, Any]:
    return {
        "adapter_priority": priority,
        "buyer": "AI platform teams and regulated agent workflow owners",
        "category": category,
        "gap_status": "inferred",
        "native_refs_to_preserve": native_refs,
        "official_capabilities": official_capabilities,
        "proof_layer_gap_status": "inferred",
        "source_id": source_id,
        "telos_adapter_inputs": native_refs + ["source_refs", "workspace_state", "tool_call", "policy_decision"],
        "telos_adapter_outputs": ["action_receipt", "verification_packet", "loop_ledger_entry", "compensation_pointer"],
        "tool": tool,
        "wedge_hypothesis": "Hypothesis: preserve the incumbent trace/eval object and bind it to authority, workspace state, side-effect class, admission, verification, and replay receipts.",
    }


def action_receipt_fields() -> list[str]:
    return [
        "receipt_id", "schema", "source_refs", "workspace_state", "authority_scope", "action_admission",
        "tool_call", "side_effect_class", "materials_digest", "trace_refs", "eval_refs", "model_refs",
        "runtime_refs", "verification_verdict", "stop_reason", "compensation_pointer", "privacy_boundary",
        "receipt_status",
    ]


def demo_slices() -> list[dict[str, str]]:
    return [
        {"demo_id": "otel_trace_to_action_receipt", "promotion_state": "DEMO_NOT_PRODUCT_MARKET_FIT", "success_metric": "convert one OpenTelemetry trace into a Telos action receipt with source refs, side-effect class, and Crucible verdict"},
        {"demo_id": "langfuse_langsmith_eval_bridge", "promotion_state": "DEMO_NOT_PRODUCT_MARKET_FIT", "success_metric": "preserve one Langfuse or LangSmith trace and add admission, workspace, stop reason, and replay fields"},
        {"demo_id": "promptfoo_redteam_to_verdict_packet", "promotion_state": "DEMO_NOT_PRODUCT_MARKET_FIT", "success_metric": "bind one promptfoo red-team report to a Telos verification packet and compensation pointer"},
    ]


def compose() -> dict[str, Any]:
    packet = {
        "schema": SCHEMA,
        "action_receipt_fields": action_receipt_fields(),
        "adapter_rows": adapter_rows(),
        "current_promoted_natural_laws": [],
        "demo_slices": demo_slices(),
        "generated_on": "2026-07-01",
        "market_wedge": "agent_observability_to_action_receipt",
        "non_promotion_statement": "Pass 0064 is an adapter requirements matrix. It does not claim replacement of observability platforms, product-market fit, or unique absence of competitor features.",
        "non_replacement_claim": True,
        "pass": PASS_ID,
        "source_anchors": source_anchors(),
        "unsupported_uniqueness_claim_count": 0,
    }
    errors = validate(packet)
    packet["validation_errors"] = errors
    packet["status"] = STATUS_MATCH if not errors else STATUS_DRIFT
    packet["seal"] = sha256_obj(packet)
    return packet


def validate(packet: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    source_ids = {item.get("source_id") for item in packet.get("source_anchors", [])}
    tools = {row.get("tool") for row in packet.get("adapter_rows", [])}
    required_tools = {"LangSmith", "Langfuse", "Arize Phoenix", "Braintrust", "OpenTelemetry", "MLflow", "W&B Weave", "DVC", "promptfoo", "Helicone"}
    required_fields = {"receipt_id", "source_refs", "workspace_state", "authority_scope", "action_admission", "tool_call", "side_effect_class", "trace_refs", "eval_refs", "verification_verdict", "stop_reason", "compensation_pointer", "privacy_boundary", "receipt_status"}
    if packet.get("schema") != SCHEMA:
        errors.append("schema")
    if not required_tools.issubset(tools):
        errors.append("required_tools")
    if not required_fields.issubset(set(packet.get("action_receipt_fields", []))):
        errors.append("action_receipt_fields")
    if len(source_ids) < 10:
        errors.append("source_anchor_count")
    if len(packet.get("demo_slices", [])) != 3:
        errors.append("demo_slices")
    if packet.get("unsupported_uniqueness_claim_count") != 0:
        errors.append("unsupported_uniqueness_claim_count")
    if packet.get("non_replacement_claim") is not True:
        errors.append("non_replacement_claim")
    for row in packet.get("adapter_rows", []):
        if row.get("source_id") not in source_ids:
            errors.append(f"source:{row.get('tool')}")
        if row.get("proof_layer_gap_status") != "inferred":
            errors.append(f"proof_gap:{row.get('tool')}")
        if not 1 <= row.get("adapter_priority", 0) <= 5:
            errors.append(f"priority:{row.get('tool')}")
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
