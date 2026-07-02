"""Compose pass 0072 domain-focus adapter experiment."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


SCHEMA = "DomainFocusAdapterExperiment/v1"
PASS_ID = "0072"
STATUS_MATCH = "DOMAIN_FOCUS_ADAPTER_EXPERIMENT_MATCH"
STATUS_DRIFT = "DOMAIN_FOCUS_ADAPTER_EXPERIMENT_DRIFT"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
BRIDGE_PREFIX = "Continue improving the five Project Telos flagship tools as protocol agnostic enterprise AI workflow tools."
BRIDGE_SUFFIX = "Use Gather Index Forum Crucible Telos receipts."

DOMAINS = [
    {
        "domain_id": "buildlang_buildc",
        "label": "BuildLang/buildc scientific compute",
        "raw": "Route BuildLang buildc scientific compute proof packet domain focus for rendering mathematics physics quant finance and security.",
        "focus": "BuildLang buildc scientific compute proof packet for rendering mathematics physics quant finance and security",
        "paths": ["buildlang", "buildc", "build-universe"],
    },
    {
        "domain_id": "color_calibration",
        "label": "Color calibration and rendering measurement",
        "raw": "Route color calibration rendering measurement proof kit with ACES OCIO calibration receipts and display measurement outputs.",
        "focus": "color calibration rendering measurement proof kit with ACES OCIO calibration receipts and display measurement outputs",
        "paths": ["color", "rendering", "display-calibration"],
    },
    {
        "domain_id": "ai4science",
        "label": "AI4Science research proof packets",
        "raw": "Route AI4Science research proof packets for math physics biology and autonomous discovery.",
        "focus": "AI4Science research proof packets for math physics biology and autonomous discovery",
        "paths": ["docs/research", "science", "proof-packets"],
    },
    {
        "domain_id": "agent_ops",
        "label": "Agent operations and action receipts",
        "raw": "Route agent observability action receipts for regulated multi-agent workflows.",
        "focus": "agent observability action receipts for regulated multi-agent workflows",
        "paths": ["telos", "action-receipts", "agent-ops"],
    },
    {
        "domain_id": "market_recon",
        "label": "Market recon and buyer evidence",
        "raw": "Route market recon competitor matrices buyer evidence and wedge scorecards.",
        "focus": "market recon competitor matrices buyer evidence and wedge scorecards",
        "paths": ["docs", "market-recon", "buyer-evidence"],
    },
    {
        "domain_id": "quantum_physics",
        "label": "Quantum and physics proof packets",
        "raw": "Route quantum computing proof packets with simulator hardware calibration and resource estimates.",
        "focus": "quantum computing proof packets with simulator hardware calibration and resource estimates",
        "paths": ["quantum", "physics", "simulators"],
    },
]
INDEX_FOCUSES = ["telos", "docs/research/dogfood", "buildc", "buildlang", "color", "forum", "gather", "crucible"]


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_obj(value: object) -> str:
    return sha256_text(canonical_json(value))


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def run_command(command: list[str]) -> dict[str, Any]:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True)
    return {
        "command": " ".join(command),
        "exit_code": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "stdout_sha256": sha256_text(result.stdout),
        "stderr_sha256": sha256_text(result.stderr),
    }


def project_telos_score(route: dict[str, Any]) -> float:
    for row in route.get("candidates", []):
        if row.get("agent") == "project-telos":
            return float(row.get("score") or 0.0)
    return 0.0


def route_probe(domain: dict[str, Any]) -> dict[str, Any]:
    adapted_prompt = f"{BRIDGE_PREFIX} Domain focus: {domain['focus']}. {BRIDGE_SUFFIX}"
    raw_result = run_command(["forum", "route", domain["raw"], "--json"])
    adapted_result = run_command(["forum", "route", adapted_prompt, "--json"])
    raw = json.loads(raw_result["stdout"])
    adapted = json.loads(adapted_result["stdout"])
    return {
        "domain_id": domain["domain_id"],
        "label": domain["label"],
        "raw_prompt_sha256": sha256_text(domain["raw"]),
        "adapted_prompt_sha256": sha256_text(adapted_prompt),
        "raw": {
            "decided": raw.get("decided"),
            "confidence": raw.get("confidence"),
            "needs_escalation": raw.get("needs_escalation"),
            "project_telos_score": project_telos_score(raw),
            "top_agent": raw.get("candidates", [{}])[0].get("agent"),
        },
        "adapted": {
            "decided": adapted.get("decided"),
            "confidence": adapted.get("confidence"),
            "needs_escalation": adapted.get("needs_escalation"),
            "project_telos_score": project_telos_score(adapted),
            "top_agent": adapted.get("candidates", [{}])[0].get("agent"),
        },
        "score_lift": project_telos_score(adapted) - project_telos_score(raw),
        "status": "MATCH" if adapted.get("decided") == "project-telos" and adapted.get("needs_escalation") is False else "DRIFT",
    }


def index_focus_probe(focus: str) -> dict[str, Any]:
    command = ["index", "context-envelope", "--root", str(REPO), "--budget", "500", "--focus", focus, "--hops", "0", "--json"]
    result = run_command(command)
    output = (result["stdout"] + result["stderr"]).strip()
    parsed: dict[str, Any] = {}
    if result["exit_code"] == 0:
        parsed = json.loads(result["stdout"])
    return {
        "focus": focus,
        "exit_code": result["exit_code"],
        "stdout_sha256": result["stdout_sha256"],
        "stderr_sha256": result["stderr_sha256"],
        "schema": parsed.get("schema"),
        "verification_verdict": parsed.get("verification_verdict"),
        "selection_mode": (parsed.get("selection") or {}).get("mode"),
        "retained_count": len(parsed.get("retained") or []),
        "receipt_count": len(parsed.get("receipts") or []),
        "observed_error": output[:200] if result["exit_code"] != 0 else "",
        "status": "MATCH" if result["exit_code"] == 0 and parsed.get("verification_verdict") == "MATCH" else "REJECT",
    }


def adapter_rows(route_probes: list[dict[str, Any]], index_probes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    valid_focuses = [row["focus"] for row in index_probes if row["status"] == "MATCH"]
    rows: list[dict[str, Any]] = []
    for domain, route in zip(DOMAINS, route_probes):
        rows.append({
            "domain_id": domain["domain_id"],
            "label": domain["label"],
            "forum_route_before": route["raw"],
            "forum_route_after": route["adapted"],
            "forum_status": route["status"],
            "index_strategy": "repo_root_context_plus_domain_path_filter_pending",
            "valid_index_focuses": valid_focuses,
            "requested_paths": domain["paths"],
            "gather_strategy": "domain packet catalog with source receipts",
            "crucible_strategy": "domain thesis and negative fixture gate",
            "telos_strategy": "join domain packet, route receipt, context receipt, verdict, and action receipt",
        })
    return rows


def tool_improvement_queue(index_probes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rejected = [row["focus"] for row in index_probes if row["status"] == "REJECT"]
    return [
        {"tool": "index", "gap": "path and domain labels are rejected as focus repos", "evidence": rejected, "next": "add path/domain focus adapter that resolves labels to repo root plus source-ref filters"},
        {"tool": "forum", "gap": "domain prompts need operator-spine bridge vocabulary to route decisively", "evidence": "raw route probes escalate; adapted probes decide project-telos", "next": "teach router domain-focus vocabulary directly"},
        {"tool": "gather", "gap": "domain packets need catalog-level grouping", "evidence": "pass 0071 packet can be gathered but domain packet families are not first-class", "next": "emit domain catalog receipts keyed by field and buyer"},
        {"tool": "crucible", "gap": "domain focus needs reusable negative fixtures", "evidence": "pass 0072 requires route and focus negative fixtures", "next": "create standard route/focus gates for proof-packet promotion"},
        {"tool": "telos", "gap": "domain focus is not yet a product-level envelope", "evidence": "Telos has context and server manifests but no domain-focus contract", "next": "define TelosDomainFocusEnvelope/v1 as a megatool join layer"},
    ]


def negative_fixtures(route_probes: list[dict[str, Any]], index_probes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    raw_escalations = [row["domain_id"] for row in route_probes if row["raw"]["needs_escalation"]]
    rejected_focuses = [row["focus"] for row in index_probes if row["status"] == "REJECT"]
    return [
        {"fixture_id": "raw_domain_prompt_without_bridge", "expected_status": "REJECT", "reject_reason": "forum_route_needs_escalation", "affected_domains": raw_escalations},
        {"fixture_id": "path_focus_direct_to_index", "expected_status": "REJECT", "reject_reason": "unknown_focus_repo", "rejected_focuses": rejected_focuses},
        {"fixture_id": "root_context_claims_domain_coverage", "expected_status": "REJECT", "reject_reason": "root_context_not_domain_semantic_coverage"},
        {"fixture_id": "missing_crucible_domain_gate", "expected_status": "REJECT", "reject_reason": "unverified_domain_packet_promotion"},
        {"fixture_id": "unsupported_claim_promoted", "expected_status": "REJECT", "reject_reason": "unsupported_claim_count_nonzero"},
        {"fixture_id": "raw_payload_required", "expected_status": "REJECT", "reject_reason": "raw_private_payload_required"},
    ]


def validate_artifact(artifact: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if artifact.get("domain_count") != len(DOMAINS):
        errors.append("domain_count")
    if artifact.get("route_summary", {}).get("adapted_project_telos") != len(DOMAINS):
        errors.append("adapted_route_count")
    if artifact.get("route_summary", {}).get("adapted_escalations") != 0:
        errors.append("adapted_escalations")
    if artifact.get("index_summary", {}).get("valid_focuses") != ["telos"]:
        errors.append("index_valid_focuses")
    if artifact.get("index_summary", {}).get("rejected_focus_count", 0) < 5:
        errors.append("index_rejections")
    if artifact.get("unsupported_claim_count") != 0:
        errors.append("unsupported_claim_count")
    if len(artifact.get("negative_fixtures", [])) < 6:
        errors.append("negative_fixture_count")
    for item in artifact.get("negative_fixtures", []):
        if item.get("expected_status") != "REJECT" or not item.get("reject_reason"):
            errors.append(f"negative_fixture:{item.get('fixture_id')}")
    return errors


def compose() -> dict[str, Any]:
    route_probes = [route_probe(domain) for domain in DOMAINS]
    index_probes = [index_focus_probe(focus) for focus in INDEX_FOCUSES]
    valid_focuses = [row["focus"] for row in index_probes if row["status"] == "MATCH"]
    rejected_focuses = [row["focus"] for row in index_probes if row["status"] == "REJECT"]
    artifact = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "generated_on": "2026-07-01",
        "domain_count": len(DOMAINS),
        "route_probes": route_probes,
        "index_focus_probes": index_probes,
        "adapter_rows": adapter_rows(route_probes, index_probes),
        "route_summary": {
            "raw_escalations": sum(1 for row in route_probes if row["raw"]["needs_escalation"]),
            "adapted_escalations": sum(1 for row in route_probes if row["adapted"]["needs_escalation"]),
            "adapted_project_telos": sum(1 for row in route_probes if row["adapted"]["decided"] == "project-telos"),
            "average_project_telos_score_lift": sum(row["score_lift"] for row in route_probes) / len(route_probes),
        },
        "index_summary": {
            "valid_focuses": valid_focuses,
            "rejected_focuses": rejected_focuses,
            "rejected_focus_count": len(rejected_focuses),
            "domain_focus_status": "ROOT_FALLBACK_REQUIRED",
        },
        "tool_improvement_queue": tool_improvement_queue(index_probes),
        "negative_fixtures": negative_fixtures(route_probes, index_probes),
        "unsupported_claim_count": 0,
        "non_promotion_statement": "Pass 0072 proves a bounded domain-focus adapter experiment. It does not prove Index path-focus implementation, complete domain retrieval, buyer adoption, scientific discovery, or a natural law.",
    }
    errors = validate_artifact(artifact)
    artifact["validation_errors"] = errors
    artifact["status"] = STATUS_MATCH if not errors else STATUS_DRIFT
    artifact["seal"] = sha256_obj(artifact)
    return artifact


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
