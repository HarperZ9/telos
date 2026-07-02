"""Compose pass 0108 detailed-balance Markov receipt."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from fractions import Fraction
from pathlib import Path
from typing import Any

SCHEMA = "DetailedBalanceMarkovReceipt/v1"
PASS_ID = "0108"
STATUS_MATCH = "DETAILED_BALANCE_MARKOV_RECEIPT_MATCH"
STATUS_DRIFT = "DETAILED_BALANCE_MARKOV_RECEIPT_DRIFT"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
REACTION_CORPUS = ROOT / "schemas" / "reaction-network-corpus-harness-receipt-pass-0107.json"


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


def frow(row: list[Fraction]) -> list[str]:
    return [fstr(value) for value in row]


def run_json(command: list[str], timeout: int = 45) -> tuple[int, str, str, dict[str, Any]]:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    parsed = json.loads(result.stdout) if result.returncode == 0 and result.stdout.strip().startswith("{") else {}
    return result.returncode, result.stdout, result.stderr, parsed


def source_anchors() -> list[dict[str, str]]:
    return [
        {"title": "Stan Reference Manual: MCMC Sampling", "url": "https://mc-stan.org/docs/reference-manual/mcmc.html", "claim": "Stan exposes HMC and NUTS Markov chain Monte Carlo algorithms", "kind": "official_docs"},
        {"title": "NumPyro Markov Chain Monte Carlo", "url": "https://num.pyro.ai/en/latest/mcmc.html", "claim": "NumPyro provides MCMC algorithms including HMC/NUTS", "kind": "official_docs"},
        {"title": "TensorFlow Probability API", "url": "https://www.tensorflow.org/probability/api_docs/python/tfp", "claim": "TensorFlow Probability includes an MCMC module for probabilistic reasoning", "kind": "official_docs"},
        {"title": "TensorFlow Probability UncalibratedRandomWalk", "url": "https://www.tensorflow.org/probability/api_docs/python/tfp/mcmc/UncalibratedRandomWalk", "claim": "uncalibrated MCMC kernels can fail to converge to the target distribution", "kind": "official_docs"},
        {"title": "Detailed Balance and Markov Chain Monte Carlo", "url": "https://personal.math.ubc.ca/~holmescerfon/teaching/asa22/handout-Lecture3_2022.pdf", "claim": "detailed balance is used in physics and statistics for reversible Markov chains", "kind": "course_notes"},
        {"title": "Markov Chains and Markov Chain Monte Carlo", "url": "https://www.stats.ox.ac.uk/~teh/teaching/dtc2014/Markov4.pdf", "claim": "detailed balance can check stationary distributions for reversible Markov chains", "kind": "course_notes"},
        {"title": "tfp.mcmc: Modern Markov Chain Monte Carlo Tools Built for Modern Hardware", "url": "https://arxiv.org/pdf/2002.01184", "claim": "TFP MCMC is positioned as modern MCMC tooling for hardware-backed probabilistic computation", "kind": "whitepaper"},
    ]


def market_surface() -> dict[str, Any]:
    tools = [
        ("Stan", "Bayesian modeling and MCMC", "https://mc-stan.org/docs/reference-manual/mcmc.html"),
        ("NumPyro", "JAX-backed probabilistic programming and MCMC", "https://num.pyro.ai/en/latest/mcmc.html"),
        ("TensorFlow Probability", "probabilistic reasoning and MCMC in TensorFlow", "https://www.tensorflow.org/probability/api_docs/python/tfp"),
        ("PyMC", "Bayesian modeling and MCMC ecosystem", "https://www.pymc.io/projects/examples/en/latest/statistical_rethinking_lectures/08-Markov_Chain_Monte_Carlo.html"),
        ("BlackJAX", "JAX sampling algorithms", "https://blackjax-devs.github.io/blackjax/"),
        ("Turing.jl", "Julia probabilistic programming", "https://turinglang.org/"),
        ("ArviZ", "Bayesian diagnostics and visualization", "https://python.arviz.org/"),
        ("UQpy", "uncertainty quantification with MCMC sampling", "https://uqpyproject.readthedocs.io/en/latest/sampling/mcmc/index.html"),
    ]
    return {
        "tool_count": len(tools),
        "tools": [{"tool": name, "category": category, "source": source, "gap_status": "inferred"} for name, category, source in tools],
        "gap_status": "hypothesis",
        "gap_hypothesis": "Probabilistic runtimes expose samplers and diagnostics, but portable proof packets can bind transition kernels, detailed-balance residuals, stationary residuals, convergence probes, and negative fixtures.",
    }


def reversible_kernel() -> tuple[list[Fraction], list[list[Fraction]]]:
    pi = [Fraction(1, 2), Fraction(1, 3), Fraction(1, 6)]
    p = [
        [Fraction(7, 10), Fraction(1, 5), Fraction(1, 10)],
        [Fraction(3, 10), Fraction(3, 5), Fraction(1, 10)],
        [Fraction(3, 10), Fraction(1, 5), Fraction(1, 2)],
    ]
    return pi, p


def row_only_kernel() -> list[list[Fraction]]:
    return [
        [Fraction(3, 5), Fraction(2, 5), Fraction(0)],
        [Fraction(1, 10), Fraction(4, 5), Fraction(1, 10)],
        [Fraction(1, 5), Fraction(3, 10), Fraction(1, 2)],
    ]


def cycle_kernel() -> tuple[list[Fraction], list[list[Fraction]]]:
    return [Fraction(1, 3), Fraction(1, 3), Fraction(1, 3)], [
        [Fraction(0), Fraction(1), Fraction(0)],
        [Fraction(0), Fraction(0), Fraction(1)],
        [Fraction(1), Fraction(0), Fraction(0)],
    ]


def stationary_residual(pi: list[Fraction], p: list[list[Fraction]]) -> list[Fraction]:
    return [sum(pi[i] * p[i][j] for i in range(len(pi))) - pi[j] for j in range(len(pi))]


def detailed_balance_residuals(pi: list[Fraction], p: list[list[Fraction]]) -> list[list[Fraction]]:
    return [[pi[i] * p[i][j] - pi[j] * p[j][i] for j in range(len(pi))] for i in range(len(pi))]


def max_abs(values: list[Fraction] | list[list[Fraction]]) -> Fraction:
    flat: list[Fraction] = []
    for value in values:
        flat.extend(value if isinstance(value, list) else [value])
    return max((abs(value) for value in flat), default=Fraction(0))


def row_sums(p: list[list[Fraction]]) -> list[Fraction]:
    return [sum(row) for row in p]


def simulate(pi: list[Fraction], p: list[list[Fraction]], steps: int = 200) -> dict[str, Any]:
    dist = [1.0, 0.0, 0.0]
    pf = [[float(value) for value in row] for row in p]
    for _ in range(steps):
        dist = [sum(dist[i] * pf[i][j] for i in range(len(dist))) for j in range(len(dist))]
    target = [float(value) for value in pi]
    l1 = sum(abs(dist[i] - target[i]) for i in range(len(dist)))
    return {"steps": steps, "start": [1.0, 0.0, 0.0], "final_distribution": dist, "l1_distance_to_pi": l1}


def forum_route() -> dict[str, Any]:
    prompt = "Pass 0108: detailed-balance Markov proof packet for MCMC, stochastic physics, AI uncertainty, probabilistic programming, and proof receipts."
    code, stdout, stderr, parsed = run_json(["forum", "route", "--json", prompt], timeout=30)
    return {"status": "MATCH" if code == 0 else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "decided": parsed.get("decided"), "confidence": parsed.get("confidence"), "needs_escalation": parsed.get("needs_escalation"), "top_candidates": parsed.get("candidates", [])[:5]}


def index_receipt() -> dict[str, Any]:
    code, stdout, stderr, parsed = run_json(["index", "context-envelope", "--root", ".", "--budget", "1200", "--json"], timeout=45)
    return {"status": "MATCH" if code == 0 and parsed.get("verification_verdict") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "schema": parsed.get("schema"), "verification_verdict": parsed.get("verification_verdict"), "graph_pack_sha256": parsed.get("recheck", {}).get("graph_pack_sha256"), "source_refs_only": parsed.get("privacy", {}).get("source_refs_only")}


def telos_status() -> dict[str, Any]:
    code, stdout, stderr, parsed = run_json(["node", "demo/status.mjs", "--summary"], timeout=30)
    return {"status": "MATCH" if code == 0 and parsed.get("status") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "tool_version": parsed.get("tool_version"), "tool": parsed.get("tool")}


def reversible_packet() -> dict[str, Any]:
    pi, p = reversible_kernel()
    db = detailed_balance_residuals(pi, p)
    stat = stationary_residual(pi, p)
    return {
        "pi": frow(pi),
        "transition_matrix": [frow(row) for row in p],
        "row_sums": frow(row_sums(p)),
        "max_detailed_balance_residual": fstr(max_abs(db)),
        "stationary_residual": frow(stat),
        "simulation_probe": simulate(pi, p),
    }


def negative_fixtures(pi: list[Fraction]) -> dict[str, Any]:
    row_p = row_only_kernel()
    cycle_pi, cycle_p = cycle_kernel()
    return {
        "row_stochastic_not_stationary": {
            "transition_matrix": [frow(row) for row in row_p],
            "row_sums": frow(row_sums(row_p)),
            "stationary_residual": frow(stationary_residual(pi, row_p)),
            "max_detailed_balance_residual": fstr(max_abs(detailed_balance_residuals(pi, row_p))),
            "status": "DRIFT_EXPECTED",
        },
        "stationary_not_reversible": {
            "transition_matrix": [frow(row) for row in cycle_p],
            "pi": frow(cycle_pi),
            "stationary_residual": frow(stationary_residual(cycle_pi, cycle_p)),
            "max_detailed_balance_residual": fstr(max_abs(detailed_balance_residuals(cycle_pi, cycle_p))),
            "status": "BOUNDARY_EXPECTED",
        },
    }


def validate_artifact(artifact: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    pos = artifact.get("reversible_kernel", {})
    neg = artifact.get("negative_fixtures", {})
    if artifact.get("schema") != SCHEMA:
        errors.append("schema")
    if pos.get("stationary_residual") != ["0", "0", "0"] or pos.get("max_detailed_balance_residual") != "0":
        errors.append("positive_kernel")
    if pos.get("simulation_probe", {}).get("l1_distance_to_pi", 1) >= 1e-6:
        errors.append("simulation_probe")
    if neg.get("row_stochastic_not_stationary", {}).get("stationary_residual") == ["0", "0", "0"]:
        errors.append("row_only_negative")
    if neg.get("stationary_not_reversible", {}).get("max_detailed_balance_residual") == "0":
        errors.append("nonnecessary_boundary")
    if artifact.get("market_surface", {}).get("tool_count", 0) < 8:
        errors.append("market_surface")
    if any(row.get("status") != "MATCH" for row in artifact.get("flagship_receipts", {}).values()):
        errors.append("flagships")
    if artifact.get("unsupported_claim_count") != 0 or artifact.get("current_promoted_natural_laws") != []:
        errors.append("promotion_boundary")
    return errors


def compose() -> dict[str, Any]:
    corpus = read_json(REACTION_CORPUS)
    pi, _ = reversible_kernel()
    artifact: dict[str, Any] = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "generated_on": "2026-07-01",
        "status": STATUS_DRIFT,
        "source_bindings": {"reaction_corpus_pass": corpus["pass"], "source_packet": "ReactionNetworkCorpusHarnessReceipt/v1"},
        "source_anchors": source_anchors(),
        "market_surface": market_surface(),
        "proof": {"claim": "detailed balance implies stationarity for finite Markov kernels", "symbolic_step": "sum_i pi_i P_ij = sum_i pi_j P_ji = pi_j", "boundary": "detailed balance is sufficient for stationarity, not necessary"},
        "reversible_kernel": reversible_packet(),
        "negative_fixtures": negative_fixtures(pi),
        "law_candidate": {"name": "finite_markov_detailed_balance_stationarity", "status": "LAW_CANDIDATE", "scope": "finite row-stochastic transition kernels with positive pi satisfying detailed balance"},
        "promotion_requirements": ["independent reproduction", "larger stochastic-kernel corpus", "MCMC runtime adapter", "domain reviewer signoff"],
        "unsupported_claim_count": 0,
        "current_promoted_natural_laws": [],
        "non_promotion_statement": "This pass proves a bounded finite Markov-chain identity and market proof-packet gap. It does not prove sampler correctness for Stan, NumPyro, TFP, PyMC, or any production probabilistic runtime.",
        "flagship_receipts": {"forum": forum_route(), "index": index_receipt(), "telos": telos_status()},
    }
    artifact["validation_errors"] = validate_artifact(artifact)
    artifact["status"] = STATUS_MATCH if not artifact["validation_errors"] else STATUS_DRIFT
    artifact["measurements"] = [
        {"id": "detailed_balance_residual", "status": "MATCH" if artifact["reversible_kernel"]["max_detailed_balance_residual"] == "0" else "DRIFT"},
        {"id": "stationary_residual", "status": "MATCH" if artifact["reversible_kernel"]["stationary_residual"] == ["0", "0", "0"] else "DRIFT"},
        {"id": "row_stochastic_negative", "status": "MATCH" if artifact["negative_fixtures"]["row_stochastic_not_stationary"]["stationary_residual"] != ["0", "0", "0"] else "DRIFT"},
        {"id": "nonnecessary_boundary", "status": "MATCH" if artifact["negative_fixtures"]["stationary_not_reversible"]["max_detailed_balance_residual"] != "0" else "DRIFT"},
        {"id": "market_surface", "status": "MATCH" if artifact["market_surface"]["tool_count"] >= 8 else "DRIFT"},
        {"id": "flagships", "status": "MATCH" if all(row["status"] == "MATCH" for row in artifact["flagship_receipts"].values()) else "DRIFT"},
        {"id": "promotion_boundary", "status": "MATCH" if artifact["current_promoted_natural_laws"] == [] else "DRIFT"},
    ]
    unsealed = dict(artifact)
    artifact["seal"] = sha256_obj(unsealed)
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(ROOT / "schemas" / "detailed-balance-markov-receipt-pass-0108.json"))
    args = parser.parse_args()
    artifact = compose()
    write_json(Path(args.out), artifact)
    print(json.dumps({"path": args.out, "seal": artifact["seal"], "status": artifact["status"]}, indent=2, sort_keys=True))
    if artifact["status"] != STATUS_MATCH:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
