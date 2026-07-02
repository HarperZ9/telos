"""Compose pass 0113 constrained-MPC feasibility receipt."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from fractions import Fraction
from pathlib import Path
from typing import Any

SCHEMA = "ConstrainedMPCFeasibilityReceipt/v1"
PASS_ID = "0113"
STATUS_MATCH = "CONSTRAINED_MPC_FEASIBILITY_RECEIPT_MATCH"
STATUS_DRIFT = "CONSTRAINED_MPC_FEASIBILITY_RECEIPT_DRIFT"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
LYAPUNOV = ROOT / "schemas" / "lyapunov-stability-certificate-receipt-pass-0112.json"
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


def fseq(values: list[Fraction]) -> list[str]:
    return [fstr(value) for value in values]


def rollout(x0: Fraction, controls: list[Fraction]) -> list[Fraction]:
    states = [x0]
    x = x0
    for u in controls:
        x += u
        states.append(x)
    return states


def max_abs(values: list[Fraction]) -> Fraction:
    return max(abs(value) for value in values)


def objective(states: list[Fraction], controls: list[Fraction]) -> Fraction:
    return sum(x * x for x in states[:-1]) + sum(u * u for u in controls)


def run_json(command: list[str], timeout: int = 45) -> tuple[int, str, str, dict[str, Any]]:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    parsed = json.loads(result.stdout) if result.returncode == 0 and result.stdout.strip().startswith("{") else {}
    return result.returncode, result.stdout, result.stderr, parsed


def source_anchors() -> list[dict[str, str]]:
    return [
        {"tool": "OSQP", "url": "https://osqp.org/docs/examples/mpc.html", "claim": "documents constrained linear-quadratic MPC for LTI systems", "kind": "official_docs"},
        {"tool": "do-mpc", "url": "https://www.do-mpc.com/en/latest/theory_mpc.html", "claim": "describes MPC over a finite prediction horizon with constraints", "kind": "official_docs"},
        {"tool": "CasADi", "url": "https://web.casadi.org/docs/", "claim": "supports numerical optimization and optimal control", "kind": "official_docs"},
        {"tool": "CVXPY", "url": "https://www.cvxpy.org/examples/", "claim": "provides application examples for convex optimization modeling", "kind": "official_docs"},
        {"tool": "MathWorks MPC", "url": "https://www.mathworks.com/help/mpc/gs/what-is-mpc.html", "claim": "defines MPC as constrained finite-horizon optimal control", "kind": "official_docs"},
        {"tool": "SCS", "url": "https://www.cvxgrp.org/scs/examples/python/mpc.html", "claim": "documents an MPC example using box cones and warm starts", "kind": "official_docs"},
        {"tool": "Drake", "url": "https://drake.mit.edu/", "claim": "supports model-based design and verification for robotics", "kind": "official_docs"},
        {"tool": "MATLAB Control System Toolbox", "url": "https://www.mathworks.com/products/control.html", "claim": "models, analyzes, and designs control systems", "kind": "official_product"},
        {"tool": "python-control", "url": "https://python-control.readthedocs.io/en/0.10.2/", "claim": "provides control-system analysis and design tooling", "kind": "official_docs"},
    ]


def youtube_binding(roadmap: dict[str, Any]) -> dict[str, Any]:
    summary = roadmap["source_summary"]
    return {
        "roadmap_pass": roadmap["pass"],
        "valid_video_count": summary["valid_video_count"],
        "transcript_receipt_count": summary["transcript_receipt_count"],
        "dominant_cluster": summary["dominant_cluster"],
        "dominant_cluster_video_count": summary["dominant_cluster_video_count"],
        "raw_transcript_included": summary["raw_transcript_stored"],
        "source_policy": summary["source_policy"],
    }


def youtube_requirements(roadmap: dict[str, Any]) -> dict[str, Any]:
    node = next(row for row in roadmap["roadmap_nodes"] if row["node_id"] == "optimization_proof_workbench")
    requirement = next(row for row in node["requirements"] if isinstance(row, dict) and row["requirement_id"] == "constraint_encoding_receipt")
    return {
        "top_priority": roadmap["top_priority"],
        "dominant_cluster": roadmap["source_summary"]["dominant_cluster"],
        "dominant_cluster_video_count": roadmap["source_summary"]["dominant_cluster_video_count"],
        "source_video_ids": node["source_video_ids"],
        "source_titles": node["youtube_titles"],
        "required_receipt_fields": requirement["required_fields"],
        "requirement_id": requirement["requirement_id"],
        "source_policy": roadmap["source_summary"]["source_policy"],
    }


def feasible_case() -> dict[str, Any]:
    x0 = Fraction(2)
    controls = [Fraction(-1), Fraction(-1), Fraction(0)]
    states = rollout(x0, controls)
    x_bound = Fraction(2)
    u_bound = Fraction(1)
    terminal_target = Fraction(0)
    checks = {
        "state_bound_max_abs": fstr(max_abs(states)),
        "input_bound_max_abs": fstr(max_abs(controls)),
        "state_bound": fstr(x_bound),
        "input_bound": fstr(u_bound),
        "terminal_target": fstr(terminal_target),
        "terminal_residual": fstr(states[-1] - terminal_target),
    }
    return {
        "system": "x[k+1] = x[k] + u[k]",
        "x0": fstr(x0),
        "horizon": len(controls),
        "controls": fseq(controls),
        "states": fseq(states),
        "objective": fstr(objective(states, controls)),
        "constraints": checks,
        "terminal_residual": checks["terminal_residual"],
        "constraint_status": "MATCH" if max_abs(states) <= x_bound and max_abs(controls) <= u_bound and states[-1] == terminal_target else "DRIFT",
    }


def negative_fixtures() -> dict[str, Any]:
    infeasible_x0 = Fraction(3)
    horizon = 2
    u_bound = Fraction(1)
    target = Fraction(0)
    best_terminal = infeasible_x0 - horizon * u_bound
    bad_controls = [Fraction(-1), Fraction(0), Fraction(0)]
    bad_states = rollout(Fraction(2), bad_controls)
    return {
        "infeasible_terminal_fixture": {
            "x0": fstr(infeasible_x0),
            "horizon": horizon,
            "input_bound": fstr(u_bound),
            "terminal_target": fstr(target),
            "minimum_terminal_abs_residual": fstr(abs(best_terminal - target)),
            "classification": "INFEASIBLE_EXPECTED",
        },
        "bad_plan_fixture": {
            "x0": "2",
            "controls": fseq(bad_controls),
            "states": fseq(bad_states),
            "terminal_target": "0",
            "terminal_residual": fstr(bad_states[-1]),
            "classification": "TERMINAL_VIOLATION_EXPECTED",
        },
    }


def market_surface() -> dict[str, Any]:
    tools = [{"tool": row["tool"], "source": row["url"], "gap_status": "inferred"} for row in source_anchors()]
    return {
        "tool_count": len(tools),
        "tools": tools,
        "gap_status": "hypothesis",
        "gap_hypothesis": "MPC and control stacks expose solvers and modeling APIs, while a proof packet can bind the finite-horizon problem, constraints, candidate plan, rollout, infeasibility witness, source provenance, and verification verdicts.",
    }


def forum_route() -> dict[str, Any]:
    prompt = "Pass 0113: constrained MPC feasibility receipt from YouTube optimization signals, control source anchors, and exact rollout witnesses."
    code, stdout, stderr, parsed = run_json(["forum", "route", "--json", prompt], timeout=30)
    return {"status": "MATCH" if code == 0 else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "decided": parsed.get("decided"), "confidence": parsed.get("confidence"), "needs_escalation": parsed.get("needs_escalation"), "top_candidates": parsed.get("candidates", [])[:5]}


def index_receipt() -> dict[str, Any]:
    code, stdout, stderr, parsed = run_json(["index", "context-envelope", "--root", ".", "--budget", "1200", "--json"], timeout=45)
    return {"status": "MATCH" if code == 0 and parsed.get("verification_verdict") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "schema": parsed.get("schema"), "verification_verdict": parsed.get("verification_verdict"), "graph_pack_sha256": parsed.get("recheck", {}).get("graph_pack_sha256"), "source_refs_only": parsed.get("privacy", {}).get("source_refs_only")}


def telos_status() -> dict[str, Any]:
    code, stdout, stderr, parsed = run_json(["node", "demo/status.mjs", "--summary"], timeout=30)
    return {"status": "MATCH" if code == 0 and parsed.get("status") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "tool_version": parsed.get("tool_version"), "tool": parsed.get("tool")}


def validate_artifact(artifact: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    feasible = artifact.get("feasible_case", {})
    neg = artifact.get("negative_fixtures", {})
    youtube = artifact.get("youtube_binding", {})
    requirements = artifact.get("youtube_requirements", {})
    if artifact.get("schema") != SCHEMA:
        errors.append("schema")
    if feasible.get("states") != ["2", "1", "0", "0"] or feasible.get("terminal_residual") != "0":
        errors.append("feasible_rollout")
    if feasible.get("objective") != "7" or feasible.get("constraint_status") != "MATCH":
        errors.append("feasible_objective")
    if neg.get("infeasible_terminal_fixture", {}).get("minimum_terminal_abs_residual") != "1":
        errors.append("infeasible_fixture")
    if neg.get("bad_plan_fixture", {}).get("terminal_residual") != "1":
        errors.append("bad_plan_fixture")
    if artifact.get("market_surface", {}).get("tool_count", 0) < 8:
        errors.append("market")
    if youtube.get("valid_video_count") != 19 or youtube.get("transcript_receipt_count") != 19:
        errors.append("youtube_counts")
    if requirements.get("top_priority") != "optimization_proof_workbench" or requirements.get("dominant_cluster_video_count") != 13:
        errors.append("youtube_requirements")
    if requirements.get("required_receipt_fields", [None])[0] != "constraint_type":
        errors.append("required_receipt_fields")
    if any(row.get("status") != "MATCH" for row in artifact.get("flagship_receipts", {}).values()):
        errors.append("flagships")
    if artifact.get("unsupported_claim_count") != 0 or artifact.get("current_promoted_natural_laws") != []:
        errors.append("promotion_boundary")
    return errors


def compose() -> dict[str, Any]:
    lyapunov = read_json(LYAPUNOV)
    roadmap = read_json(YOUTUBE)
    artifact: dict[str, Any] = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "generated_on": "2026-07-01",
        "status": STATUS_DRIFT,
        "source_bindings": {"lyapunov_pass": lyapunov["pass"], "youtube_roadmap_pass": roadmap["pass"], "youtube_source_pass": roadmap["source_bindings"]["youtube_pass"]},
        "source_anchors": source_anchors(),
        "youtube_binding": youtube_binding(roadmap),
        "youtube_requirements": youtube_requirements(roadmap),
        "market_surface": market_surface(),
        "feasible_case": feasible_case(),
        "negative_fixtures": negative_fixtures(),
        "buildlang_target": {"target_kernel": "constrained_mpc_feasibility_kernel.bld", "status": "TARGET_INTERFACE_NOT_COMPILED"},
        "law_candidate": {"name": "finite_horizon_mpc_rollout_feasibility_certificate", "status": "LAW_CANDIDATE", "scope": "scalar integrator with exact finite-horizon constraints and candidate plan"},
        "unsupported_claim_count": 0,
        "current_promoted_natural_laws": [],
        "non_promotion_statement": "This pass proves one bounded scalar MPC feasibility certificate and two negative fixtures. It does not validate quantum advantage, hardware control, nonlinear MPC, BuildLang compilation, or a promoted natural law.",
        "flagship_receipts": {"forum": forum_route(), "index": index_receipt(), "telos": telos_status()},
    }
    artifact["validation_errors"] = validate_artifact(artifact)
    artifact["status"] = STATUS_MATCH if not artifact["validation_errors"] else STATUS_DRIFT
    artifact["measurements"] = [
        {"id": "feasible_rollout", "status": "MATCH" if artifact["feasible_case"]["constraint_status"] == "MATCH" else "DRIFT"},
        {"id": "infeasible_fixture", "status": "MATCH" if artifact["negative_fixtures"]["infeasible_terminal_fixture"]["minimum_terminal_abs_residual"] == "1" else "DRIFT"},
        {"id": "bad_plan_fixture", "status": "MATCH" if artifact["negative_fixtures"]["bad_plan_fixture"]["terminal_residual"] == "1" else "DRIFT"},
        {"id": "youtube_requirements", "status": "MATCH" if artifact["youtube_requirements"]["dominant_cluster_video_count"] == 13 else "DRIFT"},
        {"id": "market_surface", "status": "MATCH" if artifact["market_surface"]["tool_count"] >= 8 else "DRIFT"},
        {"id": "flagships", "status": "MATCH" if all(row["status"] == "MATCH" for row in artifact["flagship_receipts"].values()) else "DRIFT"},
        {"id": "promotion_boundary", "status": "MATCH" if artifact["current_promoted_natural_laws"] == [] else "DRIFT"},
    ]
    unsealed = dict(artifact)
    artifact["seal"] = sha256_obj(unsealed)
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(ROOT / "schemas" / "constrained-mpc-feasibility-receipt-pass-0113.json"))
    args = parser.parse_args()
    artifact = compose()
    write_json(Path(args.out), artifact)
    print(json.dumps({"path": args.out, "seal": artifact["seal"], "status": artifact["status"]}, indent=2, sort_keys=True))
    if artifact["status"] != STATUS_MATCH:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
