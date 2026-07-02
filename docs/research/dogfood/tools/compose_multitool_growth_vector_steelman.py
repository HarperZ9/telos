"""Compose pass 0068 multi-tool growth-vector steelman artifact."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


SCHEMA = "MultiToolGrowthVectorSteelman/v1"
PASS_ID = "0068"
STATUS_MATCH = "MULTITOOL_GROWTH_VECTOR_STEELMAN_MATCH"
STATUS_DRIFT = "MULTITOOL_GROWTH_VECTOR_STEELMAN_DRIFT"
TOOLS = [
    "Gather", "Index", "Forum", "Crucible", "Telos", "BuildLang/buildc",
    "build-universe", "color calibration", "browser evidence", "model foundry",
    "loop ledger", "action receipts",
]


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def sha256_obj(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def source_anchors() -> list[dict[str, str]]:
    rows = [
        ("opentelemetry", "https://opentelemetry.io/docs/what-is-opentelemetry/", "OpenTelemetry", "Vendor-neutral telemetry standard with traces, metrics, logs, and baggage."),
        ("openlineage", "https://openlineage.io/", "OpenLineage", "Open standard for data lineage collection and analysis."),
        ("ro_crate", "https://www.researchobject.org/ro-crate/", "RO-Crate", "Research object packaging model for data, software, workflows, and provenance."),
        ("software_heritage", "https://www.softwareheritage.org/", "Software Heritage", "Archive and reference infrastructure for source code."),
        ("mlflow", "https://mlflow.org/docs/latest/index.html", "MLflow", "ML lifecycle platform for experiment tracking and model management."),
        ("wandb", "https://docs.wandb.ai/", "Weights & Biases", "AI developer platform with experiments, models, and agent/application tooling."),
        ("langfuse", "https://langfuse.com/docs", "Langfuse", "LLM engineering platform for tracing, evals, prompt management, and metrics."),
        ("langsmith", "https://docs.langchain.com/langsmith/observability", "LangSmith", "LLM application observability and evaluation tooling."),
        ("nextflow", "https://www.nextflow.io/", "Nextflow", "Scalable and reproducible scientific workflow engine."),
        ("snakemake", "https://snakemake.readthedocs.io/", "Snakemake", "Reproducible and scalable workflow management system."),
        ("mlir", "https://mlir.llvm.org/", "MLIR", "Compiler infrastructure for reusable and extensible compiler construction."),
        ("triton", "https://triton-lang.org/main/index.html", "Triton", "GPU programming and compiler stack for custom kernels."),
        ("opencolorio", "https://opencolorio.org/", "OpenColorIO", "Color management solution for motion picture production."),
        ("aces", "https://acescentral.com/knowledge-base-2/", "ACES", "Industry color-management knowledge base and ecosystem."),
        ("spack", "https://spack.readthedocs.io/en/latest/", "Spack", "Package manager for reproducible HPC software stacks."),
        ("nist_ai_rmf", "https://www.nist.gov/itl/ai-risk-management-framework", "NIST AI RMF", "AI risk-management framework anchor for governance-facing receipts."),
    ]
    return [
        {"confidence": "high", "label": label, "retrieved_on": "2026-07-01", "source_id": sid, "summary": summary, "url": url}
        for sid, url, label, summary in rows
    ]


def previous_binding(pass_id: str, name: str) -> dict[str, Any]:
    path = Path(__file__).resolve().parents[1] / "schemas" / name
    artifact = read_json(path)
    return {"pass": pass_id, "path": f"schemas/{name}", "schema": artifact["schema"], "status": artifact["status"], "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "seal": artifact["seal"]}


def prior_centrality() -> dict[str, int]:
    artifact = read_json(Path(__file__).resolve().parents[1] / "schemas" / "tool-growth-vector-experiment-matrix-pass-0066.json")
    return artifact["synergy_graph"]["centrality"]


def tool_specs() -> dict[str, dict[str, Any]]:
    return {
        "Gather": spec("perception-intake", "source packet recall", "source-to-claim ingestion adapters", "research labs", ["ro_crate", "software_heritage", "nextflow", "snakemake"]),
        "Index": spec("structure-context", "context selection freshness", "proof-aware workspace atlas slices", "AI infra teams", ["software_heritage", "openlineage", "opentelemetry"]),
        "Forum": spec("orchestration-routing", "broad cross-domain prompt ambiguity", "route repair vocabulary and lane adapters", "agent operators", ["langfuse", "langsmith", "opentelemetry"]),
        "Crucible": spec("verification-pressure", "measurement quality and negative fixtures", "claim-to-verdict regression harness", "regulated AI teams", ["nist_ai_rmf", "mlflow", "wandb"]),
        "Telos": spec("receipt-room", "cross-tool receipt joins", "proof packet operating system spine", "platform buyers", ["opentelemetry", "openlineage", "ro_crate", "nist_ai_rmf"]),
        "BuildLang/buildc": spec("scientific-runtime", "compiler/runtime proof receipts", "equation-to-kernel accountable runtime", "scientific compute teams", ["mlir", "triton", "spack"]),
        "build-universe": spec("package-ecosystem", "adapter distribution and reproducible environments", "proof package registry", "HPC and research platform teams", ["spack", "software_heritage", "openlineage"]),
        "color calibration": spec("visual-truth", "measurement binding to rendered output", "color proof kit with calibrated receipts", "post-production and rendering teams", ["aces", "opencolorio", "nist_ai_rmf"]),
        "browser evidence": spec("web-evidence", "inspectable source capture boundaries", "redacted browser evidence packets", "research and compliance teams", ["opentelemetry", "langfuse", "software_heritage"]),
        "model foundry": spec("model-improvement", "model loop provenance", "model workflow receipt ledger", "AI research teams", ["mlflow", "wandb", "langsmith"]),
        "loop ledger": spec("continuity-ledger", "cross-pass continuity and replay", "append-only dogfood memory receipts", "agent ops teams", ["opentelemetry", "openlineage", "nist_ai_rmf"]),
        "action receipts": spec("execution-accountability", "authority/action/result binding", "agent action proof packets", "regulated agent teams", ["opentelemetry", "langfuse", "langsmith"]),
    }


def spec(role: str, bottleneck: str, lever: str, buyer: str, sources: list[str]) -> dict[str, Any]:
    return {"role": role, "bottleneck": bottleneck, "upgrade_lever": lever, "buyer": buyer, "source_ids": sources}


def tool_rows() -> list[dict[str, Any]]:
    centrality = prior_centrality()
    specs = tool_specs()
    rows = []
    for tool in TOOLS:
        row = specs[tool]
        readiness = 3 if tool in {"BuildLang/buildc", "build-universe"} else 4
        proof_advantage = 5 if tool in {"Telos", "Crucible", "action receipts", "BuildLang/buildc"} else 4
        market_pull = 5 if tool in {"action receipts", "Telos", "BuildLang/buildc", "Gather"} else 4
        friction = 4 if tool in {"BuildLang/buildc", "build-universe", "color calibration"} else 2
        priority = round((proof_advantage + market_pull + min(5, centrality.get(tool, 0) + 1) + (6 - readiness) + (6 - friction)) / 5, 2)
        rows.append({
            "tool": tool,
            "role": row["role"],
            "buyer": row["buyer"],
            "bottleneck_hypothesis": row["bottleneck"],
            "upgrade_lever": row["upgrade_lever"],
            "market_wedge_hypothesis": f"{row['buyer']} need {row['upgrade_lever']} when local proof is not enough for audit, replay, or collaboration.",
            "primary_experiment": f"p0068-{slug(tool)}-upgrade-ablation",
            "success_metric": f"{tool} improves a cross-tool proof packet without increasing unsupported_claim_count above 0.",
            "falsifier": f"{tool} row fails if a receipt cannot be replayed, a negative fixture is absent, or the market wedge remains untestable.",
            "integration_target": integration_target(tool),
            "source_ids": row["source_ids"],
            "gap_status": "inferred",
            "claim_status": "hypothesis",
            "scores": {
                "readiness": readiness,
                "proof_advantage": proof_advantage,
                "market_pull": market_pull,
                "integration_centrality": centrality.get(tool, 0),
                "implementation_friction": friction,
                "priority": priority,
            },
        })
    return sorted(rows, key=lambda item: (-item["scores"]["priority"], item["tool"]))


def slug(value: str) -> str:
    return value.lower().replace("/", "-").replace(" ", "-")


def integration_target(tool: str) -> str:
    targets = {
        "Gather": "source receipt to ResearchClaim adapter",
        "Index": "workspace context envelope to proof packet adapter",
        "Forum": "route decision receipt to action ledger adapter",
        "Crucible": "negative fixture verdict registry",
        "Telos": "multi-receipt join and product packet exporter",
        "BuildLang/buildc": "equation-to-kernel runtime receipt",
        "build-universe": "adapter package manifest and reproducible environment lock",
        "color calibration": "display/render measurement receipt",
        "browser evidence": "redacted browser state to claim evidence packet",
        "model foundry": "model loop run card to Crucible verdict",
        "loop ledger": "cross-pass replay ledger with hash checkpoints",
        "action receipts": "tool authority/action/result receipt envelope",
    }
    return targets[tool]


def synergy_edges(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    pairs = [
        ("Gather", "Index"), ("Index", "Forum"), ("Forum", "Crucible"), ("Crucible", "Telos"),
        ("Telos", "loop ledger"), ("loop ledger", "action receipts"), ("action receipts", "browser evidence"),
        ("BuildLang/buildc", "build-universe"), ("build-universe", "Telos"), ("color calibration", "browser evidence"),
        ("model foundry", "Crucible"), ("Gather", "model foundry"), ("BuildLang/buildc", "color calibration"),
        ("browser evidence", "Crucible"), ("action receipts", "Telos"),
    ]
    priority = {row["tool"]: row["scores"]["priority"] for row in rows}
    return [
        {
            "from": left,
            "to": right,
            "experiment_id": f"p0068-{slug(left)}-{slug(right)}-join",
            "receipt_target": f"{integration_target(left)} joins {integration_target(right)}",
            "synergy_score": round((priority[left] + priority[right]) / 2, 2),
            "falsifier": "Join fails if either side cannot emit a hashable receipt with a negative fixture.",
        }
        for left, right in pairs
    ]


def steelman_objections() -> list[dict[str, str]]:
    rows = [
        ("market_pull", "Buyers may prefer incumbent dashboards over proof packets.", "Run buyer-review demos with incumbent export adapters.", "No buyer can name a must-have audit gap."),
        ("integration_cost", "A megatool can become integration debt.", "Limit each pass to one replayable adapter and one negative fixture.", "Adapters require raw private payloads to replay."),
        ("compiler_scope", "BuildLang/buildc could overfit to language ambition before proof demand is validated.", "Tie compiler work to measured physics/color/finance receipts.", "No runtime receipt beats incumbent reproducibility workflows."),
        ("research_claim_quality", "Research proof packets can become polished summaries, not discovery tools.", "Require source, proof, experiment, and verifier layers.", "A packet cannot reject false or overstated claims."),
        ("routing_fragility", "Forum routing may depend on prompt phrasing.", "Promote pass 0067 repair into roster/scoring tests.", "Broad Telos prompts still escalate after route fixtures are added."),
        ("receipt_fatigue", "Too many receipts can slow operators.", "Measure minimal sufficient receipt sets per buyer.", "Replay confidence does not increase after adding receipts."),
        ("standards_overlap", "OpenTelemetry, RO-Crate, OpenLineage, MLflow, and W&B already cover pieces.", "Treat them as ingestion surfaces, not enemies.", "A Telos packet cannot add claim verification or action authority beyond imports."),
        ("proof_overclaim", "World-scale claims can outrun evidence.", "Keep unsupported_claim_count at zero and publish falsifiers first.", "Any artifact promotes market uniqueness or scientific discovery without evidence."),
    ]
    return [{"risk_id": rid, "objection": obj, "counter_experiment": exp, "kill_criterion": kill} for rid, obj, exp, kill in rows]


def experiment_queue(rows: list[dict[str, Any]], edges: list[dict[str, Any]]) -> list[dict[str, Any]]:
    top_tools = rows[:8]
    top_edges = sorted(edges, key=lambda item: (-item["synergy_score"], item["experiment_id"]))[:6]
    queue = [{"kind": "tool_upgrade", "id": row["primary_experiment"], "tool": row["tool"], "priority": row["scores"]["priority"]} for row in top_tools]
    queue.extend({"kind": "tool_join", "id": edge["experiment_id"], "tool": f"{edge['from']}->{edge['to']}", "priority": edge["synergy_score"]} for edge in top_edges)
    return sorted(queue, key=lambda item: (-item["priority"], item["id"]))


def compose() -> dict[str, Any]:
    rows = tool_rows()
    edges = synergy_edges(rows)
    artifact = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "generated_on": "2026-07-01",
        "source_anchors": source_anchors(),
        "tool_rows": rows,
        "synergy_edges": edges,
        "experiment_queue": experiment_queue(rows, edges),
        "steelman_objections": steelman_objections(),
        "previous_pass_bindings": [
            previous_binding("0066", "tool-growth-vector-experiment-matrix-pass-0066.json"),
            previous_binding("0067", "forum-routing-repair-experiment-pass-0067.json"),
        ],
        "unsupported_claim_count": 0,
        "non_promotion_statement": "Pass 0068 ranks hypotheses and executable experiment designs. It does not prove market adoption, product completion, unique competitor absence, scientific discovery, or new natural laws.",
    }
    errors = validate_artifact(artifact)
    artifact["validation_errors"] = errors
    artifact["status"] = STATUS_MATCH if not errors else STATUS_DRIFT
    artifact["seal"] = sha256_obj(artifact)
    return artifact


def validate_artifact(artifact: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    source_ids = {source["source_id"] for source in artifact.get("source_anchors", [])}
    tools = {row["tool"] for row in artifact.get("tool_rows", [])}
    if artifact.get("schema") != SCHEMA:
        errors.append("schema")
    if tools != set(TOOLS):
        errors.append("tool_set")
    if len(artifact.get("source_anchors", [])) < 16:
        errors.append("source_anchors")
    if len(artifact.get("synergy_edges", [])) < 15:
        errors.append("synergy_edges")
    if len(artifact.get("steelman_objections", [])) < 8:
        errors.append("steelman_objections")
    if len(artifact.get("experiment_queue", [])) < 12:
        errors.append("experiment_queue")
    for row in artifact.get("tool_rows", []):
        if row.get("claim_status") != "hypothesis" or row.get("gap_status") != "inferred":
            errors.append(f"claim_boundary:{row.get('tool')}")
        if not set(row.get("source_ids", [])).issubset(source_ids):
            errors.append(f"sources:{row.get('tool')}")
        if not row.get("falsifier") or not row.get("success_metric"):
            errors.append(f"metric_or_falsifier:{row.get('tool')}")
    if artifact.get("unsupported_claim_count") != 0:
        errors.append("unsupported_claim_count")
    if {row.get("pass") for row in artifact.get("previous_pass_bindings", [])} != {"0066", "0067"}:
        errors.append("previous_pass_bindings")
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
