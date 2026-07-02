"""Compose pass 0082 cross-tool growth-vector experiment matrix."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


SCHEMA = "CrossToolGrowthVectorExperimentMatrix/v1"
PASS_ID = "0082"
STATUS_MATCH = "CROSS_TOOL_GROWTH_VECTOR_EXPERIMENT_MATRIX_MATCH"
STATUS_DRIFT = "CROSS_TOOL_GROWTH_VECTOR_EXPERIMENT_MATRIX_DRIFT"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
TOOLS = [
    "Gather",
    "Index",
    "Forum",
    "Crucible",
    "Telos",
    "BuildLang/buildc",
    "build-universe",
    "color calibration",
    "browser evidence",
    "model foundry",
    "loop ledger",
    "action receipts",
]


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_obj(value: object) -> str:
    return sha256_text(canonical_json(value))


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(rel: str) -> dict[str, Any]:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n", encoding="utf-8")


def route_prompts() -> list[dict[str, str]]:
    return [
        {"lane": "proof_os_core", "text": "Route a Project Telos proof OS core lane that joins Gather source intake, Index workspace context, Forum handoff, Crucible verdicts, and Telos loop ledger receipts."},
        {"lane": "buildlang_runtime_packets", "text": "Route a BuildLang buildc scientific-runtime proof packet that binds source refs, path-scoped context, compiler corpus receipts, negative fixtures, and verifier verdicts."},
        {"lane": "visual_truth_packets", "text": "Route a visual-truth measured-output proof packet for color, rendering, scientific visualization, software metrics, and hardware-calibration boundaries."},
        {"lane": "agent_action_packets", "text": "Route an agent action accountability proof packet that converts traces, tool calls, authority, admission, execution, redacted evidence, and Crucible verdicts into one receipt."},
        {"lane": "ai4science_packets", "text": "Route an AI4Science research proof packet for literature, model runs, experiment receipts, formal checks, reproducibility, and reviewer verdicts."},
        {"lane": "package_ecosystem_forge", "text": "Route a build-universe package and adapter ecosystem lane for proof-packet plugins, source refs, package metadata, compatibility receipts, and release gates."},
        {"lane": "route_taxonomy_repair", "text": "Route a Forum taxonomy repair experiment that adds proof-packet product lanes for BuildLang, visual truth, agent action, AI4Science, and package ecosystem work."},
        {"lane": "world_scale_megatool", "text": "Route a world-scale Project Telos megatool strategy spanning research, compiler/runtime, visual truth, agent ops, model foundry, browser evidence, and societal proof packets."},
    ]


def run_forum_route(prompt: dict[str, str]) -> dict[str, Any]:
    result = subprocess.run(["forum", "route", "--json", prompt["text"]], cwd=REPO, capture_output=True, text=True)
    parsed: dict[str, Any] = {}
    if result.returncode == 0 and result.stdout.strip():
        parsed = json.loads(result.stdout)
    candidates = parsed.get("candidates", [])[:5]
    top = candidates[0].get("agent") if candidates else None
    return {
        "lane": prompt["lane"],
        "command": f"forum route --json {prompt['text']!r}",
        "exit_code": result.returncode,
        "stdout_sha256": sha256_text(result.stdout),
        "stderr_sha256": sha256_text(result.stderr),
        "decided": parsed.get("decided"),
        "confidence": parsed.get("confidence"),
        "needs_escalation": parsed.get("needs_escalation"),
        "top_agent": top,
        "top_candidates": candidates,
        "status": "MATCH" if result.returncode == 0 else "DRIFT",
    }


def prior_bindings() -> dict[str, Any]:
    paths = {
        "growth_matrix_0066": "schemas/tool-growth-vector-experiment-matrix-pass-0066.json",
        "path_selector_scorecard_0077": "schemas/path-selector-contract-scorecard-pass-0077.json",
        "buildlang_demo_0080": "schemas/buildlang-proof-packet-demo-surface-pass-0080.json",
        "visual_truth_0081": "schemas/visual-truth-proof-packet-refresh-pass-0081.json",
        "tool_receipts_0080": "schemas/tool-receipts-pass-0080.json",
        "tool_receipts_0081": "schemas/tool-receipts-pass-0081.json",
    }
    bindings: dict[str, Any] = {}
    for key, rel in paths.items():
        path = ROOT / rel
        artifact = json.loads(path.read_text(encoding="utf-8"))
        bindings[key] = {
            "path": rel,
            "schema": artifact.get("schema"),
            "status": artifact.get("status"),
            "sha256": sha256_file(path),
            "seal": artifact.get("seal"),
        }
    return bindings


def product_lanes(routes: list[dict[str, Any]], bindings: dict[str, Any]) -> list[dict[str, Any]]:
    route_by_lane = {route["lane"]: route for route in routes}
    specs = [
        ("proof_os_core", ["Gather", "Index", "Forum", "Crucible", "Telos"], "Unified claim-to-verdict product shell", 5, 5),
        ("buildlang_runtime_packets", ["BuildLang/buildc", "build-universe", "Index", "Crucible", "Telos"], "Accountable scientific runtime receipts", 5, 5),
        ("visual_truth_packets", ["color calibration", "browser evidence", "Crucible", "Telos"], "Measured-output proof packets", 5, 4),
        ("agent_action_packets", ["action receipts", "loop ledger", "browser evidence", "Forum", "Crucible", "Telos"], "Regulated agent execution packets", 4, 5),
        ("ai4science_packets", ["Gather", "model foundry", "BuildLang/buildc", "Crucible", "Telos"], "Research proof packets for science teams", 3, 5),
        ("package_ecosystem_forge", ["build-universe", "Index", "Forum", "Telos"], "Proof-packet adapter package forge", 2, 4),
        ("route_taxonomy_repair", ["Forum", "Index", "loop ledger", "Telos"], "Proof-lane routing and ownership repair", 4, 4),
        ("world_scale_megatool", TOOLS, "Portfolio map across world-scale proof products", 2, 5),
    ]
    lanes = []
    for lane_id, tools, offer, demo_readiness, leverage in specs:
        route = route_by_lane[lane_id]
        clarity = route_clarity_score(route)
        score = round((demo_readiness + leverage + clarity + route_pressure_score(route)) / 4, 2)
        lanes.append({
            "lane_id": lane_id,
            "claim_status": "hypothesis",
            "gap_status": "inferred",
            "offer": offer,
            "tools": tools,
            "route": {"needs_escalation": route["needs_escalation"], "confidence": route["confidence"], "top_agent": route["top_agent"]},
            "scores": {
                "demo_readiness": demo_readiness,
                "integration_leverage": leverage,
                "route_clarity": clarity,
                "route_pressure": route_pressure_score(route),
                "composite": score,
            },
            "next_experiment": next_experiment(lane_id, bindings),
            "falsifier": f"{lane_id} fails if a fresh packet cannot name source, context, action/runtime, verifier, negative fixtures, and missing receipt boundaries.",
        })
    return sorted(lanes, key=lambda row: (-row["scores"]["composite"], row["lane_id"]))


def route_clarity_score(route: dict[str, Any]) -> int:
    confidence = float(route.get("confidence") or 0.0)
    if route.get("needs_escalation") is False and confidence >= 0.1:
        return 5
    if route.get("needs_escalation") is False:
        return 4
    if route.get("top_agent"):
        return 2
    return 1


def route_pressure_score(route: dict[str, Any]) -> int:
    return 5 if route.get("needs_escalation") is True else 2


def next_experiment(lane_id: str, bindings: dict[str, Any]) -> str:
    if lane_id == "buildlang_runtime_packets":
        return f"Promote {bindings['buildlang_demo_0080']['path']} into a rerunnable public demo with one numerical kernel receipt."
    if lane_id == "visual_truth_packets":
        return f"Promote {bindings['visual_truth_0081']['path']} into a measured-output packet with image/hash and optional sensor branches."
    if lane_id == "route_taxonomy_repair":
        return "Patch Forum lanes or vocabulary bridge, then rerun the eight route probes until at least five route without escalation."
    if lane_id == "package_ecosystem_forge":
        return "Create a build-universe package-adapter manifest and validate it against two proof-packet schemas."
    return "Package one public-safe demo packet and one negative fixture that a buyer or reviewer can re-run."


def tool_improvements(lanes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    lane_ids = [lane["lane_id"] for lane in lanes[:4]]
    rows = {
        "Gather": ("source delta packs", "source URL/file freshness, duplicate detection, and citation receipts"),
        "Index": ("native path selector", "selected-path context envelopes with rejection receipts"),
        "Forum": ("proof-lane taxonomy", "route lanes for BuildLang, visual truth, AI4Science, agent action, and packages"),
        "Crucible": ("bundle verdicts", "multi-artifact claim bundles plus rejected-claim viewer"),
        "Telos": ("proof-packet orchestrator", "one command that joins source, context, route, receipt, and verdict layers"),
        "BuildLang/buildc": ("runtime receipt ABI", "compiler/runtime/numeric kernel receipt schema and verifier hooks"),
        "build-universe": ("adapter registry", "package metadata, compatibility, and proof-packet plugin receipts"),
        "color calibration": ("sensor branch", "separate software metrics from meter-backed hardware calibration receipts"),
        "browser evidence": ("visual evidence packet", "screenshot, DOM digest, action class, and side-effect receipts"),
        "model foundry": ("promotion lab", "model/eval/checkpoint/reward receipts gated by Crucible"),
        "loop ledger": ("market-learning ledger", "append buyer hypotheses, route probes, and demo outcomes across continuations"),
        "action receipts": ("trace importer", "OpenTelemetry and agent trace import into durable action proof packets"),
    }
    return [{
        "tool": tool,
        "improvement": rows[tool][0],
        "receipt_needed": rows[tool][1],
        "claim_status": "hypothesis",
        "linked_priority_lanes": lane_ids,
    } for tool in TOOLS]


def live_experiment_summary(routes: list[dict[str, Any]]) -> dict[str, Any]:
    escalations = [route for route in routes if route.get("needs_escalation") is True]
    decided = [route for route in routes if route.get("decided")]
    top_agents = sorted({route.get("top_agent") for route in routes if route.get("top_agent")})
    return {
        "route_probe_count": len(routes),
        "route_match_count": sum(1 for route in routes if route["status"] == "MATCH"),
        "needs_escalation_count": len(escalations),
        "decided_count": len(decided),
        "top_agents": top_agents,
        "finding": "Repeated proof-packet prompts route as cross-domain work; that is evidence for explicit product lanes and owner taxonomy, not evidence of market adoption.",
    }


def negative_fixtures() -> list[dict[str, str]]:
    return [
        {"fixture_id": "claims_market_adoption", "expected_status": "REJECT", "reject_reason": "no_buyer_interview_or_sales_evidence"},
        {"fixture_id": "claims_no_competitor_exists", "expected_status": "REJECT", "reject_reason": "comparison_matrix_supports_hypotheses_only"},
        {"fixture_id": "claims_julia_replacement", "expected_status": "REJECT", "reject_reason": "buildlang_demo_is_bounded"},
        {"fixture_id": "claims_physical_calibration", "expected_status": "REJECT", "reject_reason": "visual_truth_packet_has_no_hardware_probe"},
        {"fixture_id": "claims_scientific_discovery", "expected_status": "REJECT", "reject_reason": "no_new_theorem_law_or_bio_result"},
        {"fixture_id": "missing_forum_route_probe", "expected_status": "REJECT", "reject_reason": "live_route_experiments_required"},
        {"fixture_id": "missing_tool_improvements", "expected_status": "REJECT", "reject_reason": "all_12_tools_need_improvement_rows"},
        {"fixture_id": "raw_payload_required", "expected_status": "REJECT", "reject_reason": "receipt_refs_only"},
    ]


def compose() -> dict[str, Any]:
    bindings = prior_bindings()
    routes = [run_forum_route(prompt) for prompt in route_prompts()]
    lanes = product_lanes(routes, bindings)
    artifact: dict[str, Any] = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "generated_on": "2026-07-01",
        "promotion_state": "EXPERIMENT_MATRIX_NOT_MARKET_PROOF",
        "prior_bindings": bindings,
        "live_forum_routes": routes,
        "live_experiment_summary": live_experiment_summary(routes),
        "ranked_product_lanes": lanes,
        "tool_improvements": tool_improvements(lanes),
        "negative_fixtures": negative_fixtures(),
        "unsupported_claim_count": 0,
        "current_promoted_natural_laws": [],
        "non_promotion_statement": "Pass 0082 ranks growth-vector hypotheses from live route probes and prior packets. It does not prove buyer demand, competitor absence, scientific discovery, Julia replacement, or physical calibration.",
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
    if len(artifact.get("live_forum_routes", [])) < 8:
        errors.append("forum_routes")
    if any(route.get("status") != "MATCH" for route in artifact.get("live_forum_routes", [])):
        errors.append("forum_route_status")
    if len(artifact.get("ranked_product_lanes", [])) < 8:
        errors.append("ranked_product_lanes")
    if len(artifact.get("tool_improvements", [])) != len(TOOLS):
        errors.append("tool_improvements")
    if {row.get("tool") for row in artifact.get("tool_improvements", [])} != set(TOOLS):
        errors.append("tool_set")
    if artifact.get("unsupported_claim_count") != 0 or artifact.get("current_promoted_natural_laws") != []:
        errors.append("promotion_boundary")
    if len(artifact.get("negative_fixtures", [])) < 8:
        errors.append("negative_fixtures")
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
