"""Compose pass 0110 stochastic-runtime chain receipt."""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import subprocess
from fractions import Fraction
from pathlib import Path
from typing import Any

SCHEMA = "StochasticRuntimeChainReceipt/v1"
PASS_ID = "0110"
STATUS_MATCH = "STOCHASTIC_RUNTIME_CHAIN_RECEIPT_MATCH"
STATUS_DRIFT = "STOCHASTIC_RUNTIME_CHAIN_RECEIPT_DRIFT"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
CORPUS = ROOT / "schemas" / "stochastic-kernel-corpus-harness-receipt-pass-0109.json"


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


def parse_fraction(value: str) -> Fraction:
    return Fraction(value)


def parse_vector(values: list[str]) -> list[Fraction]:
    return [parse_fraction(value) for value in values]


def parse_matrix(rows: list[list[str]]) -> list[list[Fraction]]:
    return [parse_vector(row) for row in rows]


def fstr(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def frow(row: list[Fraction]) -> list[str]:
    return [fstr(value) for value in row]


def stationary_residual(pi: list[Fraction], p: list[list[Fraction]]) -> list[Fraction]:
    return [sum(pi[i] * p[i][j] for i in range(len(pi))) - pi[j] for j in range(len(pi))]


def detailed_balance_residuals(pi: list[Fraction], p: list[list[Fraction]]) -> list[list[Fraction]]:
    return [[pi[i] * p[i][j] - pi[j] * p[j][i] for j in range(len(pi))] for i in range(len(pi))]


def max_abs(values: list[Fraction] | list[list[Fraction]]) -> Fraction:
    flat: list[Fraction] = []
    for value in values:
        flat.extend(value if isinstance(value, list) else [value])
    return max((abs(value) for value in flat), default=Fraction(0))


def exact_distribution(p: list[list[Fraction]], steps: int) -> list[float]:
    dist = [1.0, 0.0, 0.0]
    pf = [[float(value) for value in row] for row in p]
    for _ in range(steps):
        dist = [sum(dist[i] * pf[i][j] for i in range(len(dist))) for j in range(len(dist))]
    return dist


def seeded_chain(p: list[list[Fraction]], seed: int, warmup: int, samples: int) -> dict[str, Any]:
    rng = random.Random(seed)
    state = 0
    counts = [0, 0, 0]
    pf = [[float(value) for value in row] for row in p]
    for step in range(warmup + samples):
        draw = rng.random()
        total = 0.0
        for candidate, probability in enumerate(pf[state]):
            total += probability
            if draw <= total:
                state = candidate
                break
        if step >= warmup:
            counts[state] += 1
    return {
        "seed": seed,
        "warmup_steps": warmup,
        "sample_steps": samples,
        "counts": counts,
        "empirical_distribution": [count / samples for count in counts],
    }


def l1_distance(a: list[float], b: list[float]) -> float:
    return sum(abs(a[idx] - b[idx]) for idx in range(len(a)))


def run_json(command: list[str], timeout: int = 45) -> tuple[int, str, str, dict[str, Any]]:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    parsed = json.loads(result.stdout) if result.returncode == 0 and result.stdout.strip().startswith("{") else {}
    return result.returncode, result.stdout, result.stderr, parsed


def forum_route() -> dict[str, Any]:
    prompt = "Pass 0110: stochastic runtime chain receipt, sampler adapter contract, seeded diagnostics, YouTube source-lead architecture binding."
    code, stdout, stderr, parsed = run_json(["forum", "route", "--json", prompt], timeout=30)
    return {"status": "MATCH" if code == 0 else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "decided": parsed.get("decided"), "confidence": parsed.get("confidence"), "needs_escalation": parsed.get("needs_escalation"), "top_candidates": parsed.get("candidates", [])[:5]}


def index_receipt() -> dict[str, Any]:
    code, stdout, stderr, parsed = run_json(["index", "context-envelope", "--root", ".", "--budget", "1200", "--json"], timeout=45)
    return {"status": "MATCH" if code == 0 and parsed.get("verification_verdict") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "schema": parsed.get("schema"), "verification_verdict": parsed.get("verification_verdict"), "graph_pack_sha256": parsed.get("recheck", {}).get("graph_pack_sha256"), "source_refs_only": parsed.get("privacy", {}).get("source_refs_only")}


def telos_status() -> dict[str, Any]:
    code, stdout, stderr, parsed = run_json(["node", "demo/status.mjs", "--summary"], timeout=30)
    return {"status": "MATCH" if code == 0 and parsed.get("status") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "tool_version": parsed.get("tool_version"), "tool": parsed.get("tool")}


def selected_case(corpus: dict[str, Any]) -> dict[str, Any]:
    for case in corpus["kernel_cases"]:
        if case["case_id"] == "reversible_detailed_balance":
            return case
    raise KeyError("reversible_detailed_balance")


def runtime_receipt(corpus: dict[str, Any], case: dict[str, Any]) -> dict[str, Any]:
    pi = parse_vector(case["pi"])
    p = parse_matrix(case["transition_matrix"])
    seed = 1109
    warmup = 50
    samples = 5000
    exact = exact_distribution(p, warmup + samples)
    empirical = seeded_chain(p, seed, warmup, samples)
    target = [float(value) for value in pi]
    stationary = stationary_residual(pi, p)
    balance = detailed_balance_residuals(pi, p)
    diagnostics = {
        "exact_distribution": exact,
        "target_distribution": target,
        "exact_distribution_l1_distance_to_pi": l1_distance(exact, target),
        "empirical_distribution": empirical["empirical_distribution"],
        "empirical_counts": empirical["counts"],
        "empirical_l1_distance_to_pi": l1_distance(empirical["empirical_distribution"], target),
        "empirical_threshold_l1": 0.08,
        "stationary_residual_check": {"status": "MATCH" if max_abs(stationary) == 0 else "DRIFT", "residual": frow(stationary), "max_residual": fstr(max_abs(stationary))},
        "detailed_balance_or_invariance_check": {"status": "MATCH" if max_abs(balance) == 0 else "DRIFT", "max_residual": fstr(max_abs(balance))},
    }
    negatives = {row["case_id"]: row for row in corpus["kernel_cases"] if row["case_id"] != case["case_id"]}
    return {
        "target_log_prob_digest": sha256_obj({"target_distribution": case["pi"], "representation": "finite_discrete_log_target"}),
        "transition_kernel_digest": case["transition_kernel_digest"],
        "kernel_family": "finite_markov_kernel",
        "calibration_layer": "exact_reversible_fixture",
        "acceptance_correction": "identity",
        "stationary_residual_check": diagnostics["stationary_residual_check"],
        "detailed_balance_or_invariance_check": diagnostics["detailed_balance_or_invariance_check"],
        "chain_seed_receipt": {"seed": seed, "prng": "python.random.Random", "reproducible": True},
        "warmup_schedule_receipt": {"warmup_steps": warmup, "sample_steps": samples, "start_state": 0},
        "diagnostics_receipt": diagnostics,
        "negative_fixture_receipt": negatives,
        "source_provenance_receipt": {
            "stochastic_kernel_corpus_pass": corpus["pass"],
            "corpus_artifact_sha256": sha256_text(CORPUS.read_text(encoding="utf-8")),
            "youtube_roadmap_pass": corpus["source_bindings"]["youtube_roadmap_pass"],
            "market_tool_count": corpus["market_binding"]["tool_count"],
        },
    }


def adapter_contract(corpus: dict[str, Any], receipt: dict[str, Any]) -> dict[str, Any]:
    required = corpus["adapter_spec"]["required_fields"]
    missing = [field for field in required if field not in receipt]
    return {
        "required_fields": required,
        "required_field_count": len(required),
        "required_fields_satisfied": len(required) - len(missing),
        "missing_fields": missing,
        "source_adapter_spec": corpus["adapter_spec"]["schema"],
    }


def validate_artifact(artifact: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    diag = artifact.get("runtime_receipt", {}).get("diagnostics_receipt", {})
    negative = artifact.get("runtime_receipt", {}).get("negative_fixture_receipt", {})
    if artifact.get("schema") != SCHEMA:
        errors.append("schema")
    if artifact.get("source_bindings", {}).get("stochastic_kernel_corpus_pass") != "0109":
        errors.append("corpus_binding")
    if artifact.get("adapter_contract", {}).get("missing_fields") != []:
        errors.append("adapter_missing_fields")
    if diag.get("exact_distribution_l1_distance_to_pi", 1) >= 1e-9:
        errors.append("exact_distribution")
    if diag.get("empirical_l1_distance_to_pi", 1) >= diag.get("empirical_threshold_l1", 0):
        errors.append("empirical_distribution")
    if negative.get("row_stochastic_not_stationary", {}).get("status") != "DRIFT_EXPECTED":
        errors.append("negative_fixture")
    if artifact.get("youtube_binding", {}).get("valid_video_count") != 19:
        errors.append("youtube_binding")
    if any(row.get("status") != "MATCH" for row in artifact.get("flagship_receipts", {}).values()):
        errors.append("flagships")
    if artifact.get("unsupported_claim_count") != 0 or artifact.get("current_promoted_natural_laws") != []:
        errors.append("promotion_boundary")
    return errors


def compose() -> dict[str, Any]:
    corpus = read_json(CORPUS)
    case = selected_case(corpus)
    receipt = runtime_receipt(corpus, case)
    artifact: dict[str, Any] = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "generated_on": "2026-07-01",
        "status": STATUS_DRIFT,
        "source_bindings": {
            "stochastic_kernel_corpus_pass": corpus["pass"],
            "detailed_balance_pass": corpus["source_bindings"]["detailed_balance_pass"],
            "youtube_roadmap_pass": corpus["source_bindings"]["youtube_roadmap_pass"],
            "youtube_source_pass": corpus["source_bindings"]["youtube_source_pass"],
        },
        "selected_case": case,
        "runtime_receipt": receipt,
        "adapter_contract": adapter_contract(corpus, receipt),
        "youtube_binding": corpus["youtube_binding"],
        "market_binding": corpus["market_binding"],
        "buildlang_target": {"target_kernel": "stochastic_runtime_chain_kernel.bld", "status": "TARGET_INTERFACE_NOT_COMPILED", "required_next_receipts": ["buildc_compile_receipt", "runtime_measurement_receipt"]},
        "law_candidate": {"name": "stochastic_runtime_adapter_receipt_minimum", "status": "LAW_CANDIDATE", "scope": "receipt schema for finite-kernel stochastic runtime checks"},
        "unsupported_claim_count": 0,
        "current_promoted_natural_laws": [],
        "non_promotion_statement": "This pass creates a finite-kernel runtime receipt skeleton. It does not prove production sampler correctness, compile a BuildLang kernel, validate YouTube video claims, or promote a natural law.",
        "flagship_receipts": {"forum": forum_route(), "index": index_receipt(), "telos": telos_status()},
    }
    artifact["validation_errors"] = validate_artifact(artifact)
    artifact["status"] = STATUS_MATCH if not artifact["validation_errors"] else STATUS_DRIFT
    artifact["measurements"] = [
        {"id": "adapter_contract", "status": "MATCH" if artifact["adapter_contract"]["missing_fields"] == [] else "DRIFT"},
        {"id": "exact_distribution", "status": "MATCH" if receipt["diagnostics_receipt"]["exact_distribution_l1_distance_to_pi"] < 1e-9 else "DRIFT"},
        {"id": "empirical_distribution", "status": "MATCH" if receipt["diagnostics_receipt"]["empirical_l1_distance_to_pi"] < 0.08 else "DRIFT"},
        {"id": "negative_fixture", "status": "MATCH" if receipt["negative_fixture_receipt"]["row_stochastic_not_stationary"]["status"] == "DRIFT_EXPECTED" else "DRIFT"},
        {"id": "youtube_binding", "status": "MATCH" if artifact["youtube_binding"]["valid_video_count"] == 19 else "DRIFT"},
        {"id": "flagships", "status": "MATCH" if all(row["status"] == "MATCH" for row in artifact["flagship_receipts"].values()) else "DRIFT"},
        {"id": "promotion_boundary", "status": "MATCH" if artifact["current_promoted_natural_laws"] == [] else "DRIFT"},
    ]
    unsealed = dict(artifact)
    artifact["seal"] = sha256_obj(unsealed)
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(ROOT / "schemas" / "stochastic-runtime-chain-receipt-pass-0110.json"))
    args = parser.parse_args()
    artifact = compose()
    write_json(Path(args.out), artifact)
    print(json.dumps({"path": args.out, "seal": artifact["seal"], "status": artifact["status"]}, indent=2, sort_keys=True))
    if artifact["status"] != STATUS_MATCH:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
