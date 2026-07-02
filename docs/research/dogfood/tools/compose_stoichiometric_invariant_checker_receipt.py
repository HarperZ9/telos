"""Compose pass 0106 stoichiometric invariant checker receipt."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from fractions import Fraction
from math import gcd, lcm
from pathlib import Path
from typing import Any

SCHEMA = "StoichiometricInvariantCheckerReceipt/v1"
PASS_ID = "0106"
STATUS_MATCH = "STOICHIOMETRIC_INVARIANT_CHECKER_RECEIPT_MATCH"
STATUS_DRIFT = "STOICHIOMETRIC_INVARIANT_CHECKER_RECEIPT_DRIFT"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
REACTION = ROOT / "schemas" / "reaction-mass-conservation-receipt-pass-0105.json"
AI4SCIENCE = ROOT / "schemas" / "ai4science-claim-to-experiment-receipt-pass-0104.json"
ROADMAP = ROOT / "schemas" / "youtube-critical-data-megatool-roadmap-pass-0102.json"
YOUTUBE = ROOT / "schemas" / "youtube-research-compounding-packet-pass-0085.json"


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


def transpose(matrix: list[list[int]]) -> list[list[Fraction]]:
    return [[Fraction(matrix[row][col]) for row in range(len(matrix))] for col in range(len(matrix[0]))]


def rref(matrix: list[list[Fraction]]) -> tuple[list[list[Fraction]], list[int]]:
    rows = [row[:] for row in matrix]
    pivots: list[int] = []
    row = 0
    width = len(rows[0]) if rows else 0
    for col in range(width):
        pivot = next((idx for idx in range(row, len(rows)) if rows[idx][col]), None)
        if pivot is None:
            continue
        rows[row], rows[pivot] = rows[pivot], rows[row]
        lead = rows[row][col]
        rows[row] = [value / lead for value in rows[row]]
        for idx in range(len(rows)):
            if idx == row or not rows[idx][col]:
                continue
            factor = rows[idx][col]
            rows[idx] = [rows[idx][j] - factor * rows[row][j] for j in range(width)]
        pivots.append(col)
        row += 1
        if row == len(rows):
            break
    return rows, pivots


def primitive_integer_vector(values: list[Fraction]) -> list[int]:
    denominator = 1
    for value in values:
        denominator = lcm(denominator, value.denominator)
    ints = [value.numerator * (denominator // value.denominator) for value in values]
    divisor = 0
    for value in ints:
        divisor = gcd(divisor, abs(value))
    if divisor:
        ints = [value // divisor for value in ints]
    first = next((value for value in ints if value), 0)
    return [-value for value in ints] if first < 0 else ints


def nullspace(matrix: list[list[Fraction]]) -> list[list[int]]:
    reduced, pivots = rref(matrix)
    width = len(matrix[0]) if matrix else 0
    free_cols = [col for col in range(width) if col not in pivots]
    basis: list[list[int]] = []
    for free in free_cols:
        vector = [Fraction(0) for _ in range(width)]
        vector[free] = Fraction(1)
        for row_index, pivot_col in enumerate(pivots):
            vector[pivot_col] = -reduced[row_index][free]
        basis.append(primitive_integer_vector(vector))
    return basis


def residual(vector: list[int], matrix: list[list[int]]) -> list[int]:
    return [sum(vector[row] * matrix[row][col] for row in range(len(vector))) for col in range(len(matrix[0]))]


def invariant_label(species: list[str], vector: list[int]) -> str:
    terms = [f"{coef}*{name}" if coef != 1 else name for coef, name in zip(vector, species) if coef]
    return "+".join(terms)


def source_anchors() -> list[dict[str, str]]:
    return [
        {"title": "The Convex Basis of the Left Null Space of the Stoichiometric Matrix", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC1303061/", "claim": "stoichiometric left-nullspace vectors encode conserved moieties", "kind": "paper"},
        {"title": "What makes a reaction network chemical?", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC9484159/", "claim": "reaction-network stoichiometry is constrained by conservation structure", "kind": "paper"},
        {"title": "Catalyst.jl CRN Theory", "url": "https://docs.sciml.ai/Catalyst/stable/network_analysis/crn_theory/", "claim": "chemical reaction network analysis includes conservation laws", "kind": "official_docs"},
        {"title": "Catalyst.jl Network Analysis API", "url": "https://docs.sciml.ai/Catalyst/stable/api/network_analysis_api/", "claim": "conservation-law rows are computed from net stoichiometry", "kind": "official_docs"},
        {"title": "EQTK Core Concepts", "url": "https://eqtk.github.io/user_guide/core_concepts.html", "claim": "conservation matrices span the nullspace associated with stoichiometry", "kind": "official_docs"},
    ]


def cycle_network() -> dict[str, Any]:
    matrix = [[-1, 0, 1], [1, -1, 0], [0, 1, -1]]
    return {"species": ["A", "B", "C"], "reactions": ["A_to_B", "B_to_C", "C_to_A"], "stoichiometric_matrix": matrix, "system_boundary": "closed"}


def leak_network() -> dict[str, Any]:
    matrix = [[-1, 0, 1, 0], [1, -1, 0, 0], [0, 1, -1, -1]]
    return {"species": ["A", "B", "C"], "reactions": ["A_to_B", "B_to_C", "C_to_A", "C_to_sink"], "stoichiometric_matrix": matrix, "system_boundary": "open_leaky"}


def numerical_probe(network: dict[str, Any]) -> dict[str, Any]:
    matrix = network["stoichiometric_matrix"]
    state = [2.0, 0.5, 1.25]
    initial_total = sum(state)
    rates = [0.23, 0.31, 0.17]
    dt, steps = 0.025, 200
    max_drift = 0.0
    samples: list[dict[str, float]] = []
    for step in range(steps + 1):
        max_drift = max(max_drift, abs(sum(state) - initial_total))
        if step in {0, 50, 100, 150, 200}:
            samples.append({"t": step * dt, "A": state[0], "B": state[1], "C": state[2], "total": sum(state)})
        reaction_rates = [rates[0] * state[0], rates[1] * state[1], rates[2] * state[2]]
        deltas = [sum(matrix[row][col] * reaction_rates[col] for col in range(3)) * dt for row in range(3)]
        state = [state[idx] + deltas[idx] for idx in range(3)]
    return {"initial_state": {"A": 2.0, "B": 0.5, "C": 1.25}, "rate_constants": rates, "dt": dt, "grid_points": steps + 1, "initial_total": initial_total, "max_total_drift": max_drift, "samples": samples}


def negative_probe(network: dict[str, Any], candidate: list[int]) -> dict[str, Any]:
    matrix = network["stoichiometric_matrix"]
    state = [2.0, 0.5, 1.25]
    initial_total = sum(state)
    rates = [0.23, 0.31, 0.17, 0.08]
    dt, steps = 0.025, 200
    max_drift = 0.0
    for _ in range(steps + 1):
        max_drift = max(max_drift, abs(sum(state) - initial_total))
        reaction_rates = [rates[0] * state[0], rates[1] * state[1], rates[2] * state[2], rates[3] * state[2]]
        deltas = [sum(matrix[row][col] * reaction_rates[col] for col in range(4)) * dt for row in range(3)]
        state = [state[idx] + deltas[idx] for idx in range(3)]
    return {"network_id": "cycle_with_C_sink", "status": "DRIFT_EXPECTED", "candidate_vector": candidate, "candidate_residual": residual(candidate, matrix), "breaks_invariant": max_drift > 0.01, "max_total_drift": max_drift}


def youtube_binding() -> dict[str, Any]:
    roadmap = read_json(ROADMAP)
    youtube = read_json(YOUTUBE)
    by_node = {row["node_id"]: row for row in roadmap["roadmap_nodes"]}
    return {
        "youtube_pass": youtube["pass"],
        "roadmap_pass": roadmap["pass"],
        "valid_video_count": roadmap["source_summary"]["valid_video_count"],
        "transcript_receipt_count": roadmap["source_summary"]["transcript_receipt_count"],
        "ai4science_video_count": by_node["ai4science_claim_to_experiment"]["source_video_count"],
        "buildlang_scientific_runtime_video_count": by_node["buildlang_scientific_runtime"]["source_video_count"],
        "relevant_clusters": ["molecular_ai_drug_discovery", "enterprise_quantum_optimization", "quantitative_finance_laws"],
        "architecture_pull": "turn source leads into executable invariant, simulation, runtime, and proof receipts",
        "raw_transcript_included": False,
    }


def forum_route() -> dict[str, Any]:
    prompt = "Pass 0106: stoichiometric matrix invariant checker for AI4Science, BuildLang scientific runtime, and YouTube-driven proof packet roadmap."
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
    vector = artifact.get("derived_conservation_vectors", [{}])[0]
    probe = artifact.get("numerical_probe", {})
    negative = artifact.get("negative_network", {})
    if artifact.get("schema") != SCHEMA:
        errors.append("schema")
    if vector.get("vector") != [1, 1, 1] or vector.get("residual") != [0, 0, 0]:
        errors.append("conservation_vector")
    if probe.get("grid_points", 0) < 150 or probe.get("max_total_drift", 1) > 1e-10:
        errors.append("closed_probe")
    if negative.get("candidate_residual") == [0, 0, 0, 0] or negative.get("breaks_invariant") is not True:
        errors.append("negative_fixture")
    if artifact.get("youtube_signal_binding", {}).get("valid_video_count") != 19:
        errors.append("youtube_binding")
    if any(row.get("status") != "MATCH" for row in artifact.get("flagship_receipts", {}).values()):
        errors.append("flagships")
    if artifact.get("unsupported_claim_count") != 0 or artifact.get("current_promoted_natural_laws") != []:
        errors.append("promotion_boundary")
    return errors


def compose() -> dict[str, Any]:
    reaction = read_json(REACTION)
    ai4science = read_json(AI4SCIENCE)
    network = cycle_network()
    basis = nullspace(transpose(network["stoichiometric_matrix"]))
    derived = [{"vector": vector, "invariant": invariant_label(network["species"], vector), "residual": residual(vector, network["stoichiometric_matrix"])} for vector in basis]
    artifact: dict[str, Any] = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "generated_on": "2026-07-01",
        "status": STATUS_DRIFT,
        "source_bindings": {"reaction_pass": reaction["pass"], "ai4science_pass": ai4science["pass"], "source_packet": "AI4ScienceClaimToExperimentReceipt/v1"},
        "youtube_signal_binding": youtube_binding(),
        "source_anchors": source_anchors(),
        "closed_network": network,
        "derived_conservation_vectors": derived,
        "numerical_probe": numerical_probe(network),
        "negative_network": negative_probe(leak_network(), [1, 1, 1]),
        "law_candidate": {"name": "stoichiometric_left_nullspace_conservation_invariant", "status": "LAW_CANDIDATE", "scope": "closed reaction networks where l^T S = 0 for a candidate conservation vector l"},
        "promotion_requirements": ["independent reproduction", "formal symbolic checker adapter", "larger reaction-network corpus", "reviewer signoff"],
        "unsupported_claim_count": 0,
        "current_promoted_natural_laws": [],
        "non_promotion_statement": "This pass implements a bounded stoichiometric invariant checker. It does not prove a new natural law, biological discovery, wet-lab result, or production scientific runtime.",
        "flagship_receipts": {"forum": forum_route(), "index": index_receipt(), "telos": telos_status()},
    }
    artifact["validation_errors"] = validate_artifact(artifact)
    artifact["status"] = STATUS_MATCH if not artifact["validation_errors"] else STATUS_DRIFT
    artifact["measurements"] = [
        {"id": "left_nullspace_vector", "status": "MATCH" if derived and derived[0]["residual"] == [0, 0, 0] else "DRIFT"},
        {"id": "closed_cycle_probe", "status": "MATCH" if artifact["numerical_probe"]["max_total_drift"] <= 1e-10 else "DRIFT"},
        {"id": "leaky_negative_fixture", "status": "MATCH" if artifact["negative_network"]["breaks_invariant"] else "DRIFT"},
        {"id": "youtube_signal_binding", "status": "MATCH" if artifact["youtube_signal_binding"]["valid_video_count"] == 19 else "DRIFT"},
        {"id": "flagships", "status": "MATCH" if all(row["status"] == "MATCH" for row in artifact["flagship_receipts"].values()) else "DRIFT"},
        {"id": "promotion_boundary", "status": "MATCH" if artifact["current_promoted_natural_laws"] == [] else "DRIFT"},
    ]
    unsealed = dict(artifact)
    artifact["seal"] = sha256_obj(unsealed)
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(ROOT / "schemas" / "stoichiometric-invariant-checker-receipt-pass-0106.json"))
    args = parser.parse_args()
    artifact = compose()
    write_json(Path(args.out), artifact)
    print(json.dumps({"path": args.out, "seal": artifact["seal"], "status": artifact["status"]}, indent=2, sort_keys=True))
    if artifact["status"] != STATUS_MATCH:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
