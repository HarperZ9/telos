"""Compose pass 0137 SAIR-style CompetitionProofPacket fixture."""
from __future__ import annotations

import hashlib
import json
import re
from copy import deepcopy
from pathlib import Path
from typing import Any

SCHEMA = "CompetitionProofPacketFixtureReceipt/v1"
PASS_ID = "0137"
STATUS_MATCH = "COMPETITION_PROOF_PACKET_FIXTURE_MATCH"
STATUS_DRIFT = "COMPETITION_PROOF_PACKET_FIXTURE_DRIFT"
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "schemas" / "sair-stage1-competition-proof-packet-pass-0137.json"


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_obj(value: object) -> str:
    return sha256_text(canonical_json(value))


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n", encoding="utf-8")


PROMPT_TEMPLATE = """You are judging whether Equation 1 implies Equation 2 over all magmas.

Equation 1:
{{equation1}}

Equation 2:
{{equation2}}

Return exactly one final line in this format:
VERDICT: TRUE
or
VERDICT: FALSE
"""


def render_prompt(template: str, equation1: str, equation2: str) -> str:
    return (
        template.replace("{{equation1}}", equation1)
        .replace("{{ equation1 }}", equation1)
        .replace("{{equation2}}", equation2)
        .replace("{{ equation2 }}", equation2)
    )


def _normalize_answer(value: str) -> str | None:
    upper = value.strip().upper()
    if upper in {"TRUE", "FALSE"}:
        return upper
    return None


def extract_verdict(text: str) -> dict[str, str | None]:
    boxed = re.findall(r"\\boxed\s*\{\s*(TRUE|FALSE)\s*\}", text, flags=re.IGNORECASE)
    if boxed:
        return {"verdict": boxed[-1].upper(), "method": "boxed_answer"}

    labeled: list[str] = []
    for match in re.finditer(r"\bVERDICT\s*:\s*([A-Za-z ]+)", text, flags=re.IGNORECASE):
        raw = match.group(1).strip()
        if " OR " in raw.upper():
            continue
        first = raw.split()[0] if raw.split() else ""
        norm = _normalize_answer(first)
        if norm:
            labeled.append(norm)
    if labeled:
        return {"verdict": labeled[-1], "method": "labeled_answer"}

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    bare = [_normalize_answer(line) for line in [*(lines[:1]), *(lines[-1:] if lines else [])]]
    bare = [value for value in bare if value]
    if bare:
        return {"verdict": bare[-1], "method": "bare_edge_line"}
    return {"verdict": None, "method": "unparseable"}


def problem_fixtures() -> list[dict[str, Any]]:
    return [
        {
            "problem_id": "singleton_implies_commutative",
            "equation1": "x = y",
            "equation2": "x * y = y * x",
            "expected_answer": "TRUE",
            "oracle_kind": "human_curated_fixture",
            "witness": "The singleton law collapses all variables, so both sides of every binary equation denote the same element.",
        },
        {
            "problem_id": "commutative_not_associative",
            "equation1": "x * y = y * x",
            "equation2": "(x * y) * z = x * (y * z)",
            "expected_answer": "FALSE",
            "oracle_kind": "finite_counterexample_fixture",
            "witness": "Boolean NAND is commutative but not associative: (1 NAND 1) NAND 0 = 1, while 1 NAND (1 NAND 0) = 0.",
        },
        {
            "problem_id": "associative_not_commutative",
            "equation1": "(x * y) * z = x * (y * z)",
            "equation2": "x * y = y * x",
            "expected_answer": "FALSE",
            "oracle_kind": "finite_counterexample_fixture",
            "witness": "Left projection x*y=x is associative but not commutative when x != y.",
        },
        {
            "problem_id": "left_projection_implies_associative",
            "equation1": "x * y = x",
            "equation2": "(x * y) * z = x * (y * z)",
            "expected_answer": "TRUE",
            "oracle_kind": "human_curated_fixture",
            "witness": "Under left projection, both sides reduce to x.",
        },
    ]


def model_fixture_response(problem: dict[str, Any]) -> str:
    return f"Reasoning omitted from receipt. Witness: {problem['witness']}\nVERDICT: {problem['expected_answer']}"


def attempt_receipts(problems: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for problem in problems:
        prompt = render_prompt(PROMPT_TEMPLATE, problem["equation1"], problem["equation2"])
        response = model_fixture_response(problem)
        parsed = extract_verdict(response)
        rows.append(
            {
                "attempt_id": f"local_fixture::{problem['problem_id']}",
                "problem_id": problem["problem_id"],
                "runner": "deterministic_local_fixture_no_model_call",
                "external_model_call": False,
                "prompt_sha256": sha256_text(prompt),
                "response_sha256": sha256_text(response),
                "parsed_verdict": parsed["verdict"],
                "parse_method": parsed["method"],
                "expected_answer": problem["expected_answer"],
                "correct": parsed["verdict"] == problem["expected_answer"],
            }
        )
    return rows


def parser_tests() -> list[dict[str, Any]]:
    cases = [
        ("boxed_beats_labeled", "VERDICT: TRUE\nLater: \\boxed{FALSE}", "FALSE", "boxed_answer"),
        ("last_labeled_wins", "VERDICT: FALSE\nrevision\nVERDICT: TRUE", "TRUE", "labeled_answer"),
        ("instruction_pattern_ignored", "Use VERDICT: TRUE or FALSE.\nVERDICT: FALSE", "FALSE", "labeled_answer"),
        ("bare_last_line", "Reasoning text\nTRUE", "TRUE", "bare_edge_line"),
        ("malformed_unparseable", "The answer is probably yes.", None, "unparseable"),
    ]
    rows = []
    for case_id, text, expected, method in cases:
        parsed = extract_verdict(text)
        rows.append(
            {
                "case_id": case_id,
                "expected_verdict": expected,
                "expected_method": method,
                "observed_verdict": parsed["verdict"],
                "observed_method": parsed["method"],
                "status": "MATCH" if parsed["verdict"] == expected and parsed["method"] == method else "DRIFT",
            }
        )
    return rows


REQUIRED_PACKET_FIELDS = {
    "packet_id",
    "competition_ref",
    "source_refs",
    "prompt_template_sha256",
    "problem_set_sha256",
    "attempt_receipts",
    "parser_policy",
    "verdict_summary",
    "negative_fixtures",
    "promotion_boundary",
}


def validate_packet(packet: dict[str, Any]) -> dict[str, Any]:
    failures = []
    missing = sorted(REQUIRED_PACKET_FIELDS - set(packet))
    if missing:
        failures.extend(f"missing_{field}" for field in missing)
    if not packet.get("source_refs"):
        failures.append("missing_source_refs")
    if "{{" in packet.get("rendered_prompt_sample", ""):
        failures.append("unrendered_prompt_placeholder")
    if any(row.get("external_model_call") for row in packet.get("attempt_receipts", [])):
        failures.append("external_model_call_present")
    if not all(row.get("correct") for row in packet.get("attempt_receipts", [])):
        failures.append("incorrect_attempt_verdict")
    if packet.get("current_promoted_results"):
        failures.append("promoted_result_present")
    return {"status": "MATCH" if not failures else "REJECTED", "failures": failures}


def negative_fixtures(packet: dict[str, Any]) -> list[dict[str, Any]]:
    fixtures = []
    for fixture_id, mutate in [
        ("missing_source_refs", lambda p: p.update({"source_refs": []})),
        ("unrendered_prompt_placeholder", lambda p: p.update({"rendered_prompt_sample": "{{equation1}}"})),
        ("malformed_verdict", lambda p: p["attempt_receipts"][0].update({"parsed_verdict": None, "correct": False})),
        ("wrong_answer", lambda p: p["attempt_receipts"][1].update({"parsed_verdict": "TRUE", "correct": False})),
        ("external_model_claim_without_receipt", lambda p: p["attempt_receipts"][0].update({"external_model_call": True})),
        ("promoted_theorem_result", lambda p: p.update({"current_promoted_results": ["fixture_overclaim"]})),
    ]:
        candidate = deepcopy(packet)
        mutate(candidate)
        observed = validate_packet(candidate)
        fixtures.append(
            {
                "fixture_id": fixture_id,
                "expected_status": "REJECTED",
                "observed_status": observed["status"],
                "failures": observed["failures"],
                "status": "MATCH" if observed["status"] == "REJECTED" else "DRIFT",
            }
        )
    return fixtures


def compose() -> dict[str, Any]:
    problems = problem_fixtures()
    attempts = attempt_receipts(problems)
    packet = {
        "packet_id": "sair_stage1_local_fixture_packet",
        "competition_ref": "https://competition.sair.foundation/competitions/mathematics-distillation-challenge-equational-theories-stage1/overview",
        "source_refs": [
            "https://github.com/SAIRcompetition/equational-theories-stage1-judge",
            "https://competition.sair.foundation/competitions/mathematics-distillation-challenge-equational-theories-stage1/overview",
            "https://github.com/teorth/equational_theories",
            "docs/research/dogfood/schemas/sair-math-research-infrastructure-source-leads-pass-0136.json",
        ],
        "prompt_template_sha256": sha256_text(PROMPT_TEMPLATE),
        "problem_set_sha256": sha256_obj(problems),
        "rendered_prompt_sample": render_prompt(PROMPT_TEMPLATE, problems[0]["equation1"], problems[0]["equation2"]),
        "attempt_receipts": attempts,
        "parser_policy": {
            "boxed_answers_beat_labeled": True,
            "labeled_answers_beat_bare_edge_lines": True,
            "last_marker_wins_within_same_marker_type": True,
            "ignore_instruction_pattern_true_or_false": True,
            "unparseable_verdict": "UNVERIFIABLE",
        },
        "verdict_summary": {
            "attempts": len(attempts),
            "correct": sum(1 for row in attempts if row["correct"]),
            "incorrect": sum(1 for row in attempts if not row["correct"]),
            "external_model_calls": sum(1 for row in attempts if row["external_model_call"]),
        },
        "negative_fixtures": [],
        "promotion_boundary": "This packet verifies local fixture mechanics only. It does not submit to SAIR, call official models, claim leaderboard performance, or prove new mathematics.",
        "current_promoted_results": [],
    }
    packet["positive_validation"] = validate_packet(packet)
    packet["negative_fixtures"] = negative_fixtures(packet)
    artifact: dict[str, Any] = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "generated_on": "2026-07-02",
        "status": STATUS_MATCH,
        "competition_packet": packet,
        "problem_fixtures": problems,
        "parser_tests": parser_tests(),
        "source_basis": {
            "stage1_repo_observation": "Official local toolkit exposes prompt rendering, model calls, verdict extraction, and smoke tests.",
            "stage1_competition_observation": "Official competition page frames Stage 1 as in-context mathematical distillation.",
            "equational_theories_observation": "Upstream project frames equation implication graph and Lean verification boundaries.",
            "source_status": "SOURCE_LEAD_PLUS_LOCAL_FIXTURE",
        },
        "tooling_gap": {
            "forum_route_status": "needs_escalation",
            "needed_router_lane": "formal_math_competition_proof_packet",
        },
    }
    validation_errors = []
    if packet["positive_validation"]["status"] != "MATCH":
        validation_errors.append("positive_packet_validation")
    if any(row["status"] != "MATCH" for row in packet["negative_fixtures"]):
        validation_errors.append("negative_fixture_validation")
    if any(row["status"] != "MATCH" for row in artifact["parser_tests"]):
        validation_errors.append("parser_tests")
    if packet["verdict_summary"]["external_model_calls"] != 0:
        validation_errors.append("external_model_calls")
    if packet["current_promoted_results"]:
        validation_errors.append("promoted_results")
    artifact["validation_errors"] = validation_errors
    artifact["status"] = STATUS_MATCH if not validation_errors else STATUS_DRIFT
    artifact["seal"] = sha256_obj(artifact)
    return artifact


def main() -> None:
    artifact = compose()
    write_json(OUT, artifact)
    print(json.dumps({"status": artifact["status"], "artifact": str(OUT), "seal": artifact["seal"]}, indent=2))
    if artifact["status"] != STATUS_MATCH:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
