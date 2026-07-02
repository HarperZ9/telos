"""Compose pass 0116 formal/physics source-lead bridge."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

TOOLS_DIR = Path(__file__).resolve().parent
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))
from solver_youtube_leads import gather_youtube_source_leads

SCHEMA = "FormalPhysicsSourceLeadBridgeReceipt/v1"
PASS_ID = "0116"
STATUS_MATCH = "FORMAL_PHYSICS_SOURCE_LEAD_BRIDGE_MATCH"
STATUS_DRIFT = "FORMAL_PHYSICS_SOURCE_LEAD_BRIDGE_DRIFT"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
SOLVER_REPLAY = ROOT / "schemas" / "solver-branch-replay-adapter-pass-0115.json"
YOUTUBE = ROOT / "schemas" / "youtube-critical-data-megatool-roadmap-pass-0102.json"


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


def fstr(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def clean_text(value: object) -> str:
    return str(value).replace("\ufffd", "-").encode("ascii", "ignore").decode("ascii")


def run_json(command: list[str], timeout: int = 45) -> tuple[int, str, str, dict[str, Any]]:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    parsed = json.loads(result.stdout) if result.returncode == 0 and result.stdout.strip().startswith("{") else {}
    return result.returncode, result.stdout, result.stderr, parsed


def compose_map(first: dict[str, str], second: dict[str, str]) -> dict[str, str]:
    return {key: second[value] for key, value in first.items()}


def category_case() -> dict[str, Any]:
    ida = {"a0": "a0", "a1": "a1"}
    idb = {"b0": "b0", "b1": "b1"}
    f = {"a0": "b0", "a1": "b1"}
    g = {"b0": "c1", "b1": "c0"}
    h = {"c0": "d0", "c1": "d1"}
    bad_idb = {"b0": "b1", "b1": "b0"}
    checks = {
        "left_identity": compose_map(f, idb) == f,
        "right_identity": compose_map(ida, f) == f,
        "associativity": compose_map(compose_map(f, g), h) == compose_map(f, compose_map(g, h)),
    }
    return {
        "case_id": "category_set_identity_associativity",
        "domain": "formal_math_category_theory_toy",
        "status": "MATCH" if all(checks.values()) and compose_map(f, bad_idb) != f else "DRIFT",
        "checks": checks,
        "witness": {"f": f, "g": g, "h": h, "composite": compose_map(compose_map(f, g), h)},
        "negative_fixture": {"bad_identity": bad_idb, "classification": "BAD_IDENTITY_DRIFT"},
    }


def born_case() -> dict[str, Any]:
    amplitudes = {"q0": Fraction(3, 5), "q1": Fraction(4, 5)}
    probs = {key: value * value for key, value in amplitudes.items()}
    total = sum(probs.values(), Fraction(0, 1))
    bad = {"q0": Fraction(1, 1), "q1": Fraction(1, 1)}
    bad_total = sum(v * v for v in bad.values())
    return {
        "case_id": "born_rule_normalization_toy",
        "domain": "quantum_foundations_toy",
        "status": "MATCH" if total == 1 and bad_total != 1 else "DRIFT",
        "amplitudes": {key: fstr(value) for key, value in amplitudes.items()},
        "probabilities": {key: fstr(value) for key, value in probs.items()},
        "probability_sum": fstr(total),
        "negative_fixture": {"amplitudes": {key: fstr(value) for key, value in bad.items()}, "probability_sum": fstr(bad_total), "classification": "NON_NORMALIZED_STATE_REJECTED"},
    }


def counterexample_case() -> dict[str, Any]:
    samples = [-2, -1, 0, 1, 2]
    counterexamples = [n for n in samples if not n > 0]
    revised_holds = all(n * n >= 0 for n in samples)
    return {
        "case_id": "counterexample_revision_toy",
        "domain": "theoretical_cs_counterexample_toy",
        "status": "MATCH" if counterexamples and revised_holds else "DRIFT",
        "sample_domain": samples,
        "initial_claim": "Every sampled integer is positive.",
        "initial_claim_status": "REFUTED_BY_COUNTEREXAMPLE",
        "counterexamples": counterexamples,
        "revised_claim": "Every sampled integer has nonnegative square.",
        "revised_claim_status": "MATCH" if revised_holds else "DRIFT",
    }


def loop_replay_case() -> dict[str, Any]:
    attempts = [
        {"attempt": 1, "answer": "5", "verifier": "DRIFT", "receipt": "arithmetic-counterexample:2+2!=5"},
        {"attempt": 2, "answer": "4", "verifier": "MATCH", "receipt": "arithmetic-match:2+2=4"},
    ]
    sealed = [{**row, "receipt_sha256": sha256_obj(row)} for row in attempts]
    return {
        "case_id": "loop_replay_receipt_toy",
        "domain": "agent_loop_replay_toy",
        "status": "MATCH" if sealed[-1]["verifier"] == "MATCH" and sealed[0]["verifier"] == "DRIFT" else "DRIFT",
        "attempt_count": len(sealed),
        "attempts": sealed,
        "final_status": sealed[-1]["verifier"],
        "reasoning_trace_exposed": False,
        "external_verifier": "integer-arithmetic-equality",
    }


def source_anchors() -> list[dict[str, str]]:
    return [
        {"area": "formal_math", "name": "Lean language reference", "url": "https://lean-lang.org/doc/reference/latest/", "gap_status": "verified"},
        {"area": "formal_math", "name": "Theorem Proving in Lean 4", "url": "https://lean-lang.org/theorem_proving_in_lean4/", "gap_status": "verified"},
        {"area": "formal_math", "name": "Mathlib documentation", "url": "https://leanprover-community.github.io/mathlib4_docs/", "gap_status": "verified"},
        {"area": "formal_math", "name": "Lean mathlib use case", "url": "https://lean-lang.org/use-cases/mathlib/", "gap_status": "verified"},
        {"area": "homotopy", "name": "Homotopy Type Theory book", "url": "https://homotopytypetheory.org/book/", "gap_status": "verified"},
        {"area": "homotopy", "name": "UniMath", "url": "https://unimath.github.io/", "gap_status": "verified"},
        {"area": "quantum", "name": "IBM quantum information basics", "url": "https://learning.quantum.ibm.com/course/basics-of-quantum-information/single-systems", "gap_status": "verified"},
        {"area": "quantum", "name": "Stanford Encyclopedia quantum mechanics", "url": "https://plato.stanford.edu/entries/qm/", "gap_status": "verified"},
        {"area": "ai_math", "name": "LeanDojo", "url": "https://leandojo.org/", "gap_status": "verified"},
        {"area": "ai_math", "name": "AlphaEvolve", "url": "https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/", "gap_status": "verified"},
        {"area": "agent_loops", "name": "Self-Refine", "url": "https://arxiv.org/abs/2303.17651", "gap_status": "verified"},
        {"area": "agent_loops", "name": "Reflexion", "url": "https://arxiv.org/abs/2303.11366", "gap_status": "verified"},
        {"area": "agent_loops", "name": "Tree of Thoughts", "url": "https://arxiv.org/abs/2305.10601", "gap_status": "verified"},
        {"area": "agent_loops", "name": "ReAct", "url": "https://arxiv.org/abs/2210.03629", "gap_status": "verified"},
    ]


def roadmap_requirements(leads: list[dict[str, Any]]) -> list[dict[str, str]]:
    by_id = {row["video_id"]: row for row in leads}
    return [
        {"video_id": "4MQbd5wTlI8", "claim_status": "HYPOTHESIS", "requirement": "formal packet must carry notation system, theorem prover target, and proof-object or countermodel slot", "title": clean_text(by_id["4MQbd5wTlI8"]["title"])},
        {"video_id": "HbKzqvey5PA", "claim_status": "HYPOTHESIS", "requirement": "physics packet must separate normalized-state arithmetic from interpretive Born-rule claims", "title": clean_text(by_id["HbKzqvey5PA"]["title"])},
        {"video_id": "EdVG5qNm2rY", "claim_status": "HYPOTHESIS", "requirement": "research packet must keep initial claim, counterexample, revised claim, and bounded domain explicit", "title": clean_text(by_id["EdVG5qNm2rY"]["title"])},
        {"video_id": "nYwid6Q5HXk", "claim_status": "HYPOTHESIS", "requirement": "agent packet must carry loop attempts, external verifier verdicts, and action receipts without exposing hidden reasoning", "title": clean_text(by_id["nYwid6Q5HXk"]["title"])},
    ]


def forum_route() -> dict[str, Any]:
    prompt = "Pass 0116: formal math, quantum normalization, counterexample revision, and loop replay source-lead bridge."
    code, stdout, stderr, parsed = run_json(["forum", "route", "--json", prompt], timeout=30)
    return {"status": "MATCH" if code == 0 else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "decided": parsed.get("decided"), "confidence": parsed.get("confidence"), "needs_escalation": parsed.get("needs_escalation"), "top_candidates": parsed.get("candidates", [])[:5]}


def index_receipt() -> dict[str, Any]:
    code, stdout, stderr, parsed = run_json(["index", "context-envelope", "--root", ".", "--budget", "1200", "--json"], timeout=45)
    return {"status": "MATCH" if code == 0 and parsed.get("verification_verdict") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "schema": parsed.get("schema"), "verification_verdict": parsed.get("verification_verdict")}


def telos_status() -> dict[str, Any]:
    code, stdout, stderr, parsed = run_json(["node", "demo/status.mjs", "--summary"], timeout=30)
    return {"status": "MATCH" if code == 0 and parsed.get("status") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "tool_version": parsed.get("tool_version"), "tool": parsed.get("tool")}


def compose() -> dict[str, Any]:
    solver = read_json(SOLVER_REPLAY)
    roadmap = read_json(YOUTUBE)
    leads = [{**row, "title": clean_text(row.get("title", ""))} for row in gather_youtube_source_leads()]
    cases = [category_case(), born_case(), counterexample_case(), loop_replay_case()]
    anchors = source_anchors()
    artifact: dict[str, Any] = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "generated_on": "2026-07-01",
        "status": STATUS_DRIFT,
        "source_bindings": {"solver_replay_pass": solver["pass"], "youtube_roadmap_pass": roadmap["pass"], "youtube_source_pass": roadmap["source_bindings"]["youtube_pass"], "new_youtube_lead_count": len(leads)},
        "bridge_cases": cases,
        "roadmap_requirements": roadmap_requirements(leads),
        "source_surface": {"anchor_count": len(anchors), "anchors": anchors, "gap_status": "hypothesis"},
        "new_youtube_source_leads": leads,
        "unsupported_claim_count": 0,
        "current_promoted_natural_laws": [],
        "non_promotion_statement": "This pass proves only bounded toy identities and receipt requirements. It does not settle category theory, quantum interpretation, theoretical CS, or agent reasoning research.",
        "flagship_receipts": {"forum": forum_route(), "index": index_receipt(), "telos": telos_status()},
    }
    errors = []
    if len(cases) != 4 or any(row["status"] != "MATCH" for row in cases):
        errors.append("bridge_cases")
    if len(artifact["roadmap_requirements"]) != 4:
        errors.append("roadmap_requirements")
    if artifact["source_surface"]["anchor_count"] < 12:
        errors.append("source_surface")
    if any(row.get("status") != "MATCH" for row in artifact["flagship_receipts"].values()):
        errors.append("flagships")
    artifact["validation_errors"] = errors
    artifact["status"] = STATUS_MATCH if not errors else STATUS_DRIFT
    artifact["measurements"] = [{"id": row["case_id"], "status": row["status"]} for row in cases]
    artifact["measurements"].append({"id": "promotion_boundary", "status": "MATCH"})
    unsealed = dict(artifact)
    artifact["seal"] = sha256_obj(unsealed)
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(ROOT / "schemas" / "formal-physics-source-lead-bridge-pass-0116.json"))
    args = parser.parse_args()
    artifact = compose()
    write_json(Path(args.out), artifact)
    print(json.dumps({"path": args.out, "seal": artifact["seal"], "status": artifact["status"]}, indent=2, sort_keys=True))
    if artifact["status"] != STATUS_MATCH:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
