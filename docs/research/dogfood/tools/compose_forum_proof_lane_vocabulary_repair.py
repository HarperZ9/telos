"""Compose pass 0083 Forum proof-lane vocabulary repair experiment."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


SCHEMA = "ForumProofLaneVocabularyRepair/v1"
PASS_ID = "0083"
STATUS_MATCH = "FORUM_PROOF_LANE_VOCABULARY_REPAIR_MATCH"
STATUS_DRIFT = "FORUM_PROOF_LANE_VOCABULARY_REPAIR_DRIFT"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
BASELINE = ROOT / "schemas" / "cross-tool-growth-vector-experiment-matrix-pass-0082.json"
LANE_DESCRIPTIONS = {
    "proof_os_core": "proof OS core joining source intake, workspace context, routes, verdicts, and loop ledger receipts",
    "buildlang_runtime_packets": "BuildLang buildc compiler and scientific runtime proof packets",
    "visual_truth_packets": "visual truth and measured-output proof packets for color, rendering, and scientific visualization",
    "agent_action_packets": "agent action accountability packets with traces, authority, admission, execution, and verdicts",
    "ai4science_packets": "AI4Science research proof packets for literature, model runs, experiments, formal checks, and review",
    "package_ecosystem_forge": "build-universe package and adapter ecosystem for proof-packet plugins and compatibility receipts",
    "route_taxonomy_repair": "Forum route taxonomy repair for explicit proof-packet product lanes",
    "world_scale_megatool": "world-scale megatool strategy across research, compiler/runtime, visual truth, agent ops, and societal proof packets",
}


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_obj(value: object) -> str:
    return sha256_text(canonical_json(value))


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n", encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def bridge_prompt(lane: str) -> str:
    return (
        "Project Telos dogfood pass route repair. Primary owner: project-telos. "
        "Use proof-packet lane vocabulary with Gather, Index, Forum, Crucible, "
        "Telos, action receipts, loop ledger, source refs, verifier verdicts, "
        "negative fixtures, and scoped adapter lanes. "
        f"Product lane: {lane}. Task: {LANE_DESCRIPTIONS[lane]}."
    )


def run_forum_route(lane: str) -> dict[str, Any]:
    prompt = bridge_prompt(lane)
    result = subprocess.run(["forum", "route", "--json", prompt], cwd=REPO, capture_output=True, text=True)
    parsed: dict[str, Any] = {}
    if result.returncode == 0 and result.stdout.strip():
        parsed = json.loads(result.stdout)
    candidates = parsed.get("candidates", [])[:5]
    return {
        "lane": lane,
        "bridge_prompt_sha256": sha256_text(prompt),
        "exit_code": result.returncode,
        "stdout_sha256": sha256_text(result.stdout),
        "stderr_sha256": sha256_text(result.stderr),
        "decided": parsed.get("decided"),
        "confidence": parsed.get("confidence"),
        "needs_escalation": parsed.get("needs_escalation"),
        "top_agent": candidates[0].get("agent") if candidates else None,
        "top_candidates": candidates,
        "status": "MATCH" if result.returncode == 0 else "DRIFT",
    }


def baseline_summary(baseline: dict[str, Any]) -> dict[str, Any]:
    routes = baseline["live_forum_routes"]
    return {
        "source_pass": "0082",
        "source_path": "schemas/cross-tool-growth-vector-experiment-matrix-pass-0082.json",
        "source_sha256": sha256_file(BASELINE),
        "source_seal": baseline["seal"],
        "route_probe_count": len(routes),
        "non_escalated_count": sum(1 for row in routes if row.get("needs_escalation") is False),
        "escalation_count": sum(1 for row in routes if row.get("needs_escalation") is True),
        "decided_count": sum(1 for row in routes if row.get("decided")),
    }


def repair_summary(routes: list[dict[str, Any]], baseline: dict[str, Any]) -> dict[str, Any]:
    non_escalated = [row for row in routes if row.get("needs_escalation") is False]
    persistent = [row["lane"] for row in routes if row.get("needs_escalation") is True]
    return {
        "route_probe_count": len(routes),
        "route_match_count": sum(1 for row in routes if row["status"] == "MATCH"),
        "non_escalated_count": len(non_escalated),
        "escalation_count": len(persistent),
        "improvement_over_baseline": len(non_escalated) - baseline["non_escalated_count"],
        "persistent_escalation_lanes": persistent,
        "repair_threshold": 5,
        "repair_status": "MATCH" if len(non_escalated) >= 5 and len(non_escalated) > baseline["non_escalated_count"] else "DRIFT",
    }


def taxonomy_patch() -> list[dict[str, Any]]:
    return [
        {"lane_id": "project-telos-proof-os", "owner": "project-telos", "terms": ["proof OS", "proof packet", "receipt", "Crucible verdict", "loop ledger"]},
        {"lane_id": "buildlang-runtime-proof", "owner": "project-telos", "handoff": "compiler-systems", "terms": ["BuildLang", "buildc", "compiler receipt", "runtime receipt", "numeric kernel"]},
        {"lane_id": "visual-truth-proof", "owner": "project-telos", "handoff": "render-pipeline", "terms": ["visual truth", "measured output", "color transform", "render proof", "calibration boundary"]},
        {"lane_id": "agent-action-proof", "owner": "project-telos", "handoff": "deep-research", "terms": ["action receipt", "admission", "authority", "trace import", "redacted evidence"]},
        {"lane_id": "ai4science-proof", "owner": "project-telos", "handoff": "data-ml", "terms": ["AI4Science", "research proof packet", "experiment receipt", "formal check", "review verdict"]},
        {"lane_id": "package-adapter-forge", "owner": "sdk-platform", "handoff": "ci-cd", "terms": ["build-universe", "adapter package", "compatibility receipt", "plugin manifest", "release gate"]},
        {"lane_id": "world-scale-strategy", "owner": "deep-research", "handoff": "project-telos", "terms": ["world-scale", "societal proof packet", "market map", "decompose into lanes"]},
    ]


def remaining_gaps(summary: dict[str, Any]) -> list[dict[str, str]]:
    gaps = []
    for lane in summary["persistent_escalation_lanes"]:
        if lane == "package_ecosystem_forge":
            gaps.append({"lane": lane, "gap": "Package ecosystem language still competes with ci-cd and sdk-platform.", "next_action": "Add a package-adapter forge lane with sdk-platform primary and project-telos proof-packet handoff."})
        elif lane == "world_scale_megatool":
            gaps.append({"lane": lane, "gap": "World-scale strategy is too broad for one owner.", "next_action": "Force decomposition into research, runtime, visual, agent-action, and societal packet sublanes."})
        else:
            gaps.append({"lane": lane, "gap": "Unclassified persistent route escalation.", "next_action": "Add lane-specific vocabulary and rerun route probe."})
    return gaps


def repair_caveats(summary: dict[str, Any]) -> list[dict[str, str]]:
    caveats = [
        {
            "caveat_id": "prompt_bridge_not_source_patch",
            "caveat": "The repair is prompt-level vocabulary, not a Forum source or catalog patch.",
            "next_action": "Convert bridge terms into native route fixtures or catalog lane metadata.",
        },
        {
            "caveat_id": "project_telos_overrouting_risk",
            "caveat": "A strong Project Telos prefix can over-route domain work to project-telos.",
            "next_action": "Add handoff fields so project-telos owns proof packets while compiler, render, data, SDK, and CI lanes own domain implementation.",
        },
    ]
    if summary["persistent_escalation_lanes"]:
        caveats.append({
            "caveat_id": "persistent_escalations_remain",
            "caveat": "Some lanes still escalate after bridge vocabulary.",
            "next_action": "Add lane-specific owner terms and rerun the same probes.",
        })
    return caveats


def negative_fixtures() -> list[dict[str, str]]:
    return [
        {"fixture_id": "claims_forum_source_patched", "expected_status": "REJECT", "reject_reason": "prompt_bridge_only"},
        {"fixture_id": "claims_all_routes_fixed", "expected_status": "REJECT", "reject_reason": "persistent_escalations_remain"},
        {"fixture_id": "claims_market_demand", "expected_status": "REJECT", "reject_reason": "no_buyer_evidence"},
        {"fixture_id": "claims_world_scale_solution", "expected_status": "REJECT", "reject_reason": "strategy_requires_decomposition"},
        {"fixture_id": "missing_baseline_comparison", "expected_status": "REJECT", "reject_reason": "baseline_0082_required"},
        {"fixture_id": "missing_live_routes", "expected_status": "REJECT", "reject_reason": "fresh_forum_routes_required"},
    ]


def compose() -> dict[str, Any]:
    baseline = read_json(BASELINE)
    base = baseline_summary(baseline)
    lanes = [route["lane"] for route in baseline["live_forum_routes"]]
    repaired_routes = [run_forum_route(lane) for lane in lanes]
    repair = repair_summary(repaired_routes, base)
    artifact: dict[str, Any] = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "generated_on": "2026-07-01",
        "promotion_state": "PROMPT_BRIDGE_NOT_FORUM_PATCH",
        "baseline": base,
        "repair_rule": {
            "required_prefix": "Project Telos dogfood pass route repair",
            "primary_owner": "project-telos",
            "required_terms": ["proof-packet", "Gather", "Index", "Forum", "Crucible", "Telos", "action receipts", "loop ledger", "negative fixtures"],
        },
        "repaired_routes": repaired_routes,
        "repair_summary": repair,
        "taxonomy_patch_candidates": taxonomy_patch(),
        "remaining_gaps": remaining_gaps(repair),
        "repair_caveats": repair_caveats(repair),
        "negative_fixtures": negative_fixtures(),
        "unsupported_claim_count": 0,
        "current_promoted_natural_laws": [],
        "non_promotion_statement": "Pass 0083 tests a prompt-level Forum proof-lane bridge. It does not patch Forum source, prove all routes fixed, prove buyer demand, or promote a natural law.",
    }
    errors = validate_artifact(artifact)
    artifact["validation_errors"] = errors
    artifact["status"] = STATUS_MATCH if not errors else STATUS_DRIFT
    artifact["seal"] = sha256_obj(artifact)
    return artifact


def validate_artifact(artifact: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if artifact.get("schema") != SCHEMA:
        errors.append("schema")
    if artifact.get("baseline", {}).get("source_pass") != "0082":
        errors.append("baseline")
    if artifact.get("repair_summary", {}).get("route_probe_count") != 8:
        errors.append("route_probe_count")
    if artifact.get("repair_summary", {}).get("route_match_count") != 8:
        errors.append("route_match_count")
    if artifact.get("repair_summary", {}).get("repair_status") != "MATCH":
        errors.append("repair_status")
    if artifact.get("repair_summary", {}).get("improvement_over_baseline", 0) < 4:
        errors.append("improvement")
    if len(artifact.get("taxonomy_patch_candidates", [])) < 7:
        errors.append("taxonomy_patch_candidates")
    if artifact.get("unsupported_claim_count") != 0 or artifact.get("current_promoted_natural_laws") != []:
        errors.append("promotion_boundary")
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
