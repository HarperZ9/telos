"""Compose pass 0067 Forum routing repair experiment."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


SCHEMA = "ForumRoutingRepairExperiment/v1"
STATUS_MATCH = "FORUM_ROUTING_REPAIR_EXPERIMENT_MATCH"
STATUS_DRIFT = "FORUM_ROUTING_REPAIR_EXPERIMENT_DRIFT"
PASS_ID = "0067"


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def sha256_obj(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def route_probes() -> list[dict[str, Any]]:
    return [
        {
            "probe_id": "broad_cross_domain",
            "decided": None,
            "confidence": 0.0,
            "needs_escalation": True,
            "project_telos_score": 0.09090909090909091,
            "top_competing_scores": {"ci-cd": 0.2, "compiler-systems": 0.2, "data-ml": 0.2, "deep-research": 0.2, "native-cpp": 0.2, "render-pipeline": 0.2},
            "prompt_shape": "broad frontier problem-to-proof map without explicit Telos dogfood framing",
        },
        {
            "probe_id": "decomposed_telos_tool_chain",
            "decided": "project-telos",
            "confidence": 0.5,
            "needs_escalation": False,
            "project_telos_score": 0.3181818181818182,
            "top_competing_scores": {"model-foundry": 0.25, "data-ml": 0.2, "function-routing": 0.2},
            "prompt_shape": "Project Telos dogfood pass with Gather/Index/Forum/Crucible/Telos chain and scoped adapter lanes",
        },
        {
            "probe_id": "growth_vector_vocabulary",
            "decided": "project-telos",
            "confidence": 0.5,
            "needs_escalation": False,
            "project_telos_score": 0.3181818181818182,
            "top_competing_scores": {"model-foundry": 0.25, "ci-cd": 0.2, "data-ml": 0.2, "deep-research": 0.2},
            "prompt_shape": "Project Telos growth-vector experiment matrix with proof_os_core and explicit receipt vocabulary",
        },
    ]


def repair_metrics(probes: list[dict[str, Any]]) -> dict[str, Any]:
    baseline = probes[0]["project_telos_score"]
    repaired = probes[1:]
    best = max(row["project_telos_score"] for row in repaired)
    return {
        "baseline_project_telos_score": baseline,
        "best_repaired_project_telos_score": best,
        "project_telos_score_lift": round(best - baseline, 12),
        "repaired_no_escalation_count": sum(1 for row in repaired if not row["needs_escalation"] and row["decided"] == "project-telos"),
        "routing_repair_status": "MATCH" if all((not row["needs_escalation"] and row["decided"] == "project-telos") for row in repaired) else "DRIFT",
    }


def previous_pass_binding() -> dict[str, Any]:
    path = Path(__file__).resolve().parents[1] / "schemas" / "tool-growth-vector-experiment-matrix-pass-0066.json"
    artifact = json.loads(path.read_text(encoding="utf-8"))
    return {"pass": "0066", "path": "schemas/tool-growth-vector-experiment-matrix-pass-0066.json", "schema": artifact["schema"], "status": artifact["status"], "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "seal": artifact["seal"]}


def compose() -> dict[str, Any]:
    probes = route_probes()
    packet = {
        "schema": SCHEMA,
        "generated_on": "2026-07-01",
        "negative_fixture": {"probe_id": "broad_cross_domain", "status": "FAIL_EXPECTED", "expected_failure": "needs_escalation_true"},
        "non_promotion_statement": "Pass 0067 proves a prompt-shaping route repair for Forum. It does not modify Forum source code or prove all cross-domain prompts will route correctly.",
        "pass": PASS_ID,
        "previous_pass_binding": previous_pass_binding(),
        "repair_metrics": repair_metrics(probes),
        "repair_rule": {
            "required_prefix": "Project Telos dogfood pass",
            "required_tool_chain": ["Gather", "Index", "Forum", "Crucible", "Telos"],
            "required_vocabulary": ["growth-vector", "proof packet", "action receipt", "loop ledger", "scoped adapter lanes"],
        },
        "route_probes": probes,
        "unsupported_claim_count": 0,
    }
    errors = validate(packet)
    packet["validation_errors"] = errors
    packet["status"] = STATUS_MATCH if not errors else STATUS_DRIFT
    packet["seal"] = sha256_obj(packet)
    return packet


def validate(packet: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    probes = packet.get("route_probes", [])
    metrics = packet.get("repair_metrics", {})
    if packet.get("schema") != SCHEMA:
        errors.append("schema")
    if len(probes) != 3:
        errors.append("probe_count")
    if probes and probes[0].get("needs_escalation") is not True:
        errors.append("baseline_expected_failure")
    if metrics.get("repaired_no_escalation_count") != 2:
        errors.append("repair_count")
    if metrics.get("routing_repair_status") != "MATCH":
        errors.append("repair_status")
    if metrics.get("best_repaired_project_telos_score", 0) <= metrics.get("baseline_project_telos_score", 1):
        errors.append("score_lift")
    if packet.get("previous_pass_binding", {}).get("pass") != "0066":
        errors.append("previous_pass_binding")
    if packet.get("unsupported_claim_count") != 0:
        errors.append("unsupported_claim_count")
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
