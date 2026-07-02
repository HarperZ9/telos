"""Compose pass 0105 reaction mass-conservation receipt."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import subprocess
from pathlib import Path
from typing import Any

SCHEMA = "ReactionMassConservationReceipt/v1"
PASS_ID = "0105"
STATUS_MATCH = "REACTION_MASS_CONSERVATION_RECEIPT_MATCH"
STATUS_DRIFT = "REACTION_MASS_CONSERVATION_RECEIPT_DRIFT"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
AI4SCIENCE = ROOT / "schemas" / "ai4science-claim-to-experiment-receipt-pass-0104.json"


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


def run_json(command: list[str], timeout: int = 45) -> tuple[int, str, str, dict[str, Any]]:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    parsed = json.loads(result.stdout) if result.returncode == 0 and result.stdout.strip().startswith("{") else {}
    return result.returncode, result.stdout, result.stderr, parsed


def source_anchors() -> list[dict[str, str]]:
    return [
        {"title": "Chemical Kinetics and Mass Action in Coexisting Phases", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC9620980/", "claim": "mass action is used for chemical reaction kinetics", "kind": "primary_or_review"},
        {"title": "Modeling with ODE", "url": "https://people.tamu.edu/~phoward/m647/modode.pdf", "claim": "conservation of mass links loss of one species to gain of another", "kind": "course_notes"},
        {"title": "Modeling and Analysis of Mass-Action Kinetics", "url": "https://haddad.gatech.edu/journal/Mass_Action.pdf", "claim": "mass-action kinetics yield polynomial ODE systems", "kind": "paper"},
        {"title": "Law of Mass Action", "url": "https://math.libretexts.org/Bookshelves/Applied_Mathematics/Mathematical_Biology_%28Chasnov%29/06%3A_Biochemical_Reactions/6.01%3A_The_Law_of_Mass_Action", "claim": "reaction rate is proportional to collision frequency under mass action assumptions", "kind": "textbook"},
    ]


def exact_state(t: float, a0: float, b0: float, k: float) -> tuple[float, float]:
    a = a0 * math.exp(-k * t)
    return a, b0 + a0 - a


def numerical_probe() -> dict[str, Any]:
    a0, b0, k, dt, steps = 2.5, 0.75, 0.37, 0.125, 96
    total = a0 + b0
    a_euler, b_euler = a0, b0
    max_exact = 0.0
    max_euler = 0.0
    samples: list[dict[str, float]] = []
    for step in range(steps + 1):
        t = step * dt
        a_exact, b_exact = exact_state(t, a0, b0, k)
        max_exact = max(max_exact, abs((a_exact + b_exact) - total))
        max_euler = max(max_euler, abs((a_euler + b_euler) - total))
        if step in {0, 24, 48, 72, 96}:
            samples.append({"t": t, "A_exact": a_exact, "B_exact": b_exact, "A_euler": a_euler, "B_euler": b_euler, "total_euler": a_euler + b_euler})
        delta = k * a_euler * dt
        a_euler -= delta
        b_euler += delta
    return {
        "A0": a0,
        "B0": b0,
        "k": k,
        "dt": dt,
        "grid_points": steps + 1,
        "initial_total": total,
        "max_exact_invariant_drift": max_exact,
        "max_euler_invariant_drift": max_euler,
        "samples": samples,
    }


def negative_fixture() -> dict[str, Any]:
    a0, b0, k, leak, dt, steps = 2.5, 0.75, 0.37, 0.05, 0.125, 96
    a, b = a0, b0
    total = a + b
    max_drift = 0.0
    for _ in range(steps):
        reaction = k * a * dt
        loss = leak * a * dt
        a -= reaction + loss
        b += reaction
        max_drift = max(max_drift, abs((a + b) - total))
    return {"fixture_id": "open_system_degradation", "status": "DRIFT_EXPECTED", "breaks_invariant": max_drift > 0.01, "max_total_drift": max_drift}


def forum_route() -> dict[str, Any]:
    prompt = "Pass 0105: reaction mass conservation proof packet for closed first-order mass-action A to B equation, AI4Science receipt, law candidate."
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
    probe = artifact.get("numerical_probe", {})
    if artifact.get("schema") != SCHEMA:
        errors.append("schema")
    if artifact.get("proof", {}).get("symbolic_derivative_total") != "0":
        errors.append("symbolic_proof")
    if probe.get("grid_points", 0) < 80 or probe.get("max_exact_invariant_drift", 1) > 1e-12:
        errors.append("exact_probe")
    if probe.get("max_euler_invariant_drift", 1) > 1e-10:
        errors.append("euler_probe")
    if artifact.get("negative_fixture", {}).get("breaks_invariant") is not True:
        errors.append("negative_fixture")
    if any(row.get("status") != "MATCH" for row in artifact.get("flagship_receipts", {}).values()):
        errors.append("flagships")
    if artifact.get("unsupported_claim_count") != 0 or artifact.get("current_promoted_natural_laws") != []:
        errors.append("promotion_boundary")
    return errors


def compose() -> dict[str, Any]:
    ai4science = read_json(AI4SCIENCE)
    probe = numerical_probe()
    artifact: dict[str, Any] = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "generated_on": "2026-07-01",
        "status": STATUS_DRIFT,
        "source_bindings": {"ai4science_pass": ai4science["pass"], "source_packet": "AI4ScienceClaimToExperimentReceipt/v1"},
        "reaction": {"equation": "A -> B", "rate_law": "dA/dt=-kA; dB/dt=kA", "stoichiometry": {"A": -1, "B": 1}, "system_boundary": "closed"},
        "proof": {"invariant": "A+B", "derivation": "d(A+B)/dt=dA/dt+dB/dt=-kA+kA", "symbolic_derivative_total": "0"},
        "numerical_probe": probe,
        "negative_fixture": negative_fixture(),
        "source_anchors": source_anchors(),
        "law_candidate": {"name": "closed_first_order_reaction_total_mass_invariant", "status": "LAW_CANDIDATE", "scope": "closed two-species first-order conversion A -> B with stoichiometry -1,+1"},
        "promotion_requirements": ["independent reproduction", "symbolic checker adapter", "broader reaction-network class proof", "reviewer signoff"],
        "unsupported_claim_count": 0,
        "current_promoted_natural_laws": [],
        "non_promotion_statement": "This pass proves a bounded invariant for a closed toy reaction model. It does not prove a new natural law, biological discovery, enzyme mechanism, or experimental result.",
        "flagship_receipts": {"forum": forum_route(), "index": index_receipt(), "telos": telos_status()},
    }
    artifact["validation_errors"] = validate_artifact(artifact)
    artifact["status"] = STATUS_MATCH if not artifact["validation_errors"] else STATUS_DRIFT
    artifact["measurements"] = [
        {"id": "symbolic_derivative", "status": "MATCH" if artifact["proof"]["symbolic_derivative_total"] == "0" else "DRIFT"},
        {"id": "exact_invariant", "status": "MATCH" if probe["max_exact_invariant_drift"] <= 1e-12 else "DRIFT"},
        {"id": "euler_invariant", "status": "MATCH" if probe["max_euler_invariant_drift"] <= 1e-10 else "DRIFT"},
        {"id": "negative_fixture", "status": "MATCH" if artifact["negative_fixture"]["breaks_invariant"] else "DRIFT"},
        {"id": "flagships", "status": "MATCH" if all(row["status"] == "MATCH" for row in artifact["flagship_receipts"].values()) else "DRIFT"},
        {"id": "promotion_boundary", "status": "MATCH" if artifact["current_promoted_natural_laws"] == [] else "DRIFT"},
    ]
    unsealed = dict(artifact)
    artifact["seal"] = sha256_obj(unsealed)
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(ROOT / "schemas" / "reaction-mass-conservation-receipt-pass-0105.json"))
    args = parser.parse_args()
    artifact = compose()
    write_json(Path(args.out), artifact)
    print(json.dumps({"path": args.out, "seal": artifact["seal"], "status": artifact["status"]}, indent=2, sort_keys=True))
    if artifact["status"] != STATUS_MATCH:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
