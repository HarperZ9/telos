"""Compose pass 0084 Forum native lane-fixture proposal."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


SCHEMA = "ForumNativeLaneFixtureProposal/v1"
PASS_ID = "0084"
STATUS_MATCH = "FORUM_NATIVE_LANE_FIXTURE_PROPOSAL_MATCH"
STATUS_DRIFT = "FORUM_NATIVE_LANE_FIXTURE_PROPOSAL_DRIFT"
ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = ROOT / "schemas" / "forum-proof-lane-vocabulary-repair-pass-0083.json"


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)


def sha256_obj(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n", encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def lane_fixtures() -> list[dict[str, Any]]:
    return [
        fixture("project-telos-proof-os", "project-telos", None, "project-telos", ["proof OS", "proof packet", "receipt", "Crucible verdict", "loop ledger"], ["proof_os_core"]),
        fixture("buildlang-runtime-proof", "compiler-systems", "project-telos", "project-telos", ["BuildLang", "buildc", "compiler receipt", "runtime receipt", "numeric kernel"], ["buildlang_runtime_packets"]),
        fixture("visual-truth-proof", "render-pipeline", "project-telos", "project-telos", ["visual truth", "measured output", "color transform", "render proof", "calibration boundary"], ["visual_truth_packets"]),
        fixture("agent-action-proof", "project-telos", "deep-research", "project-telos", ["action receipt", "admission", "authority", "trace import", "redacted evidence"], ["agent_action_packets"]),
        fixture("ai4science-proof", "data-ml", "project-telos", "project-telos", ["AI4Science", "research proof packet", "experiment receipt", "formal check", "review verdict"], ["ai4science_packets"]),
        fixture("package-adapter-forge", "sdk-platform", "ci-cd", "project-telos", ["build-universe", "adapter package", "compatibility receipt", "plugin manifest", "release gate"], ["package_ecosystem_forge"]),
        fixture("world-scale-strategy", "deep-research", "project-telos", "project-telos", ["world-scale", "societal proof packet", "market map", "decompose into lanes"], ["world_scale_megatool"]),
        fixture("route-taxonomy-repair", "sdk-platform", "project-telos", "project-telos", ["Forum", "route taxonomy", "proof-lane", "over-routing", "handoff"], ["route_taxonomy_repair"]),
    ]


def fixture(lane_id: str, primary: str, handoff: str | None, proof_owner: str | None, terms: list[str], covered: list[str]) -> dict[str, Any]:
    return {
        "lane_id": lane_id,
        "primary_owner": primary,
        "domain_handoff": handoff,
        "proof_owner": proof_owner,
        "terms": terms,
        "covered_0082_lanes": covered,
        "required_output_fields": ["primary_owner", "proof_owner", "domain_handoff", "confidence", "needs_escalation", "rationale_terms"],
    }


def positive_tests() -> list[dict[str, str]]:
    return [
        test("proof_os_core", "Build a Project Telos proof OS core with source refs, context, routes, verdicts, and loop ledger.", "project-telos", "project-telos"),
        test("buildlang_runtime_packets", "Package BuildLang buildc compiler runtime receipts for a numeric kernel proof packet.", "compiler-systems", "project-telos"),
        test("visual_truth_packets", "Package visual truth measured-output receipts for color transforms and render proof boundaries.", "render-pipeline", "project-telos"),
        test("agent_action_packets", "Package agent action receipts with authority, admission, trace import, execution, and Crucible verdicts.", "project-telos", "project-telos"),
        test("ai4science_packets", "Package AI4Science experiment receipts, model runs, literature, formal checks, and review verdicts.", "data-ml", "project-telos"),
        test("package_ecosystem_forge", "Package build-universe adapter packages with compatibility receipts and release gates.", "sdk-platform", "project-telos"),
        test("route_taxonomy_repair", "Patch Forum route taxonomy with proof-lane fixtures and over-routing tests.", "sdk-platform", "project-telos"),
        test("world_scale_megatool", "Decompose world-scale societal proof-packet strategy into research, runtime, visual, and agent lanes.", "deep-research", "project-telos"),
    ]


def test(test_id: str, prompt: str, primary: str, proof_owner: str) -> dict[str, str]:
    return {"test_id": test_id, "prompt": prompt, "expected_primary_owner": primary, "expected_proof_owner": proof_owner}


def negative_tests() -> list[dict[str, str]]:
    return [
        negative("plain_compiler_task", "Implement a compiler optimization pass with no proof-packet receipt work.", "compiler-systems", "project-telos"),
        negative("plain_render_bug", "Fix a shader and render-pipeline bug with no measured-output proof packet.", "render-pipeline", "project-telos"),
        negative("plain_ci_release", "Fix a GitHub Actions release workflow with no proof-packet adapter package.", "ci-cd", "project-telos"),
        negative("plain_market_memo", "Write generic market research notes without Telos receipts or proof-packet claims.", "deep-research", "project-telos"),
        negative("plain_sdk_plugin", "Add an SDK plugin manifest without compatibility receipts or proof-packet release gates.", "sdk-platform", "project-telos"),
    ]


def negative(test_id: str, prompt: str, expected_primary: str, forbidden_proof_owner: str) -> dict[str, str]:
    return {"test_id": test_id, "prompt": prompt, "expected_primary_owner": expected_primary, "forbidden_proof_owner": forbidden_proof_owner}


def route_prompt(prompt: str, fixtures: list[dict[str, Any]]) -> dict[str, Any]:
    lower = prompt.lower()
    scored = []
    for row in fixtures:
        hits = [term for term in row["terms"] if term.lower() in lower]
        scored.append((len(hits), hits, row))
    scored.sort(key=lambda item: (-item[0], item[2]["lane_id"]))
    score, hits, row = scored[0]
    proof_terms = ["proof", "receipt", "verdict", "crucible", "telos"]
    proof_present = any(term in lower for term in proof_terms)
    proof_owner = row["proof_owner"] if proof_present else None
    return {
        "lane_id": row["lane_id"],
        "primary_owner": row["primary_owner"],
        "domain_handoff": row["domain_handoff"],
        "proof_owner": proof_owner,
        "confidence": min(1.0, round(score / max(1, len(row["terms"])), 2)),
        "needs_escalation": score == 0,
        "rationale_terms": hits,
    }


def run_tests(fixtures: list[dict[str, Any]]) -> dict[str, Any]:
    positives = []
    for row in positive_tests():
        actual = route_prompt(row["prompt"], fixtures)
        positives.append({**row, "actual": actual, "status": "MATCH" if actual["primary_owner"] == row["expected_primary_owner"] and actual["proof_owner"] == row["expected_proof_owner"] else "DRIFT"})
    negatives = []
    for row in negative_tests():
        actual = route_prompt(row["prompt"], fixtures)
        ok = actual["primary_owner"] == row["expected_primary_owner"] and actual["proof_owner"] != row["forbidden_proof_owner"]
        negatives.append({**row, "actual": actual, "status": "MATCH" if ok else "DRIFT"})
    return {
        "positive_count": len(positives),
        "positive_match": sum(1 for row in positives if row["status"] == "MATCH"),
        "negative_count": len(negatives),
        "negative_match": sum(1 for row in negatives if row["status"] == "MATCH"),
        "positives": positives,
        "negatives": negatives,
    }


def migration_plan() -> list[dict[str, str]]:
    return [
        {"step_id": "fixture-import", "work": "Import lane fixtures into Forum route metadata or route test fixtures."},
        {"step_id": "route-output-shape", "work": "Return primary_owner, proof_owner, domain_handoff, confidence, needs_escalation, and rationale_terms."},
        {"step_id": "overrouting-tests", "work": "Add negative tests so generic compiler/render/CI/market/SDK work does not route to project-telos."},
        {"step_id": "live-probe-regression", "work": "Rerun pass 0082 and 0083 route probes after the native patch."},
    ]


def compose() -> dict[str, Any]:
    upstream = read_json(UPSTREAM)
    fixtures = lane_fixtures()
    test_results = run_tests(fixtures)
    artifact: dict[str, Any] = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "generated_on": "2026-07-01",
        "promotion_state": "FIXTURE_PROPOSAL_NOT_FORUM_PATCH",
        "upstream": {"pass": "0083", "path": "schemas/forum-proof-lane-vocabulary-repair-pass-0083.json", "sha256": sha256_file(UPSTREAM), "seal": upstream["seal"], "status": upstream["status"]},
        "lane_fixtures": fixtures,
        "route_test_results": test_results,
        "migration_plan": migration_plan(),
        "acceptance_criteria": {
            "positive_match_required": test_results["positive_count"],
            "negative_match_required": test_results["negative_count"],
            "native_patch_required_before_production_claim": True,
        },
        "unsupported_claim_count": 0,
        "current_promoted_natural_laws": [],
        "non_promotion_statement": "Pass 0084 proposes native Forum lane fixtures. It does not patch Forum source, prove production routing, prove buyer demand, or promote a natural law.",
    }
    errors = validate_artifact(artifact)
    artifact["validation_errors"] = errors
    artifact["status"] = STATUS_MATCH if not errors else STATUS_DRIFT
    artifact["seal"] = sha256_obj(artifact)
    return artifact


def validate_artifact(artifact: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    results = artifact.get("route_test_results", {})
    if artifact.get("schema") != SCHEMA:
        errors.append("schema")
    if artifact.get("upstream", {}).get("pass") != "0083":
        errors.append("upstream")
    if len(artifact.get("lane_fixtures", [])) < 8:
        errors.append("lane_fixtures")
    if results.get("positive_match") != results.get("positive_count"):
        errors.append("positive_tests")
    if results.get("negative_match") != results.get("negative_count"):
        errors.append("negative_tests")
    if len(artifact.get("migration_plan", [])) < 4:
        errors.append("migration_plan")
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
