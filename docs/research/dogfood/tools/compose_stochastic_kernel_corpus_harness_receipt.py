"""Compose pass 0109 stochastic-kernel corpus harness receipt."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import subprocess
from fractions import Fraction
from pathlib import Path
from typing import Any

SCHEMA = "StochasticKernelCorpusHarnessReceipt/v1"
PASS_ID = "0109"
STATUS_MATCH = "STOCHASTIC_KERNEL_CORPUS_HARNESS_RECEIPT_MATCH"
STATUS_DRIFT = "STOCHASTIC_KERNEL_CORPUS_HARNESS_RECEIPT_DRIFT"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
DETAILED = ROOT / "schemas" / "detailed-balance-markov-receipt-pass-0108.json"
DETAILED_COMPOSER = ROOT / "tools" / "compose_detailed_balance_markov_receipt.py"
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


def load_markov_module():
    spec = importlib.util.spec_from_file_location("pass0108_markov", DETAILED_COMPOSER)
    if not spec or not spec.loader:
        raise RuntimeError("could not load pass 0108 composer")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


MARKOV = load_markov_module()


def run_json(command: list[str], timeout: int = 45) -> tuple[int, str, str, dict[str, Any]]:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    parsed = json.loads(result.stdout) if result.returncode == 0 and result.stdout.strip().startswith("{") else {}
    return result.returncode, result.stdout, result.stderr, parsed


def fstr(value: Fraction) -> str:
    return MARKOV.fstr(value)


def frow(row: list[Fraction]) -> list[str]:
    return MARKOV.frow(row)


def finite_kernel_case(case_id: str, title: str, pi: list[Fraction], p: list[list[Fraction]], expected: str) -> dict[str, Any]:
    stationary = MARKOV.stationary_residual(pi, p)
    balance = MARKOV.detailed_balance_residuals(pi, p)
    return {
        "case_id": case_id,
        "title": title,
        "case_type": "finite_exact_kernel",
        "status": expected,
        "pi": frow(pi),
        "transition_matrix": [frow(row) for row in p],
        "row_sums": frow(MARKOV.row_sums(p)),
        "stationary_residual": frow(stationary),
        "max_stationary_residual": fstr(MARKOV.max_abs(stationary)),
        "max_detailed_balance_residual": fstr(MARKOV.max_abs(balance)),
        "transition_kernel_digest": sha256_obj({"pi": frow(pi), "p": [frow(row) for row in p]}),
    }


def kernel_cases() -> list[dict[str, Any]]:
    pi, p = MARKOV.reversible_kernel()
    cycle_pi, cycle_p = MARKOV.cycle_kernel()
    row_case = finite_kernel_case(
        "row_stochastic_not_stationary",
        "row-stochastic kernel that is not stationary for the declared pi",
        pi,
        MARKOV.row_only_kernel(),
        "DRIFT_EXPECTED",
    )
    source_boundary = {
        "case_id": "uncalibrated_random_walk_source_boundary",
        "title": "uncalibrated source boundary for production MCMC kernels",
        "case_type": "source_boundary",
        "status": "REQUIRES_CALIBRATION",
        "source_url": "https://www.tensorflow.org/probability/api_docs/python/tfp/mcmc/UncalibratedRandomWalk",
        "source_digest": sha256_text("https://www.tensorflow.org/probability/api_docs/python/tfp/mcmc/UncalibratedRandomWalk"),
        "calibration_required": True,
        "required_receipt": "acceptance_correction_or_calibration_layer",
        "reason": "A source-level uncalibrated kernel is not a claim of target-stationary production sampling.",
    }
    return [
        finite_kernel_case("reversible_detailed_balance", "pass 0108 reversible detailed-balance kernel", pi, p, "MATCH"),
        finite_kernel_case("stationary_nonreversible_cycle", "stationary cyclic kernel that violates detailed balance", cycle_pi, cycle_p, "BOUNDARY_EXPECTED"),
        row_case,
        source_boundary,
    ]


def corpus_summary(cases: list[dict[str, Any]]) -> dict[str, Any]:
    exact_cases = [case for case in cases if case.get("case_type") == "finite_exact_kernel"]
    return {
        "case_count": len(cases),
        "exact_kernel_count": len(exact_cases),
        "match_count": sum(1 for case in cases if case["status"] == "MATCH"),
        "drift_expected_count": sum(1 for case in cases if case["status"] == "DRIFT_EXPECTED"),
        "boundary_expected_count": sum(1 for case in cases if case["status"] in {"BOUNDARY_EXPECTED", "REQUIRES_CALIBRATION"}),
        "zero_stationary_exact_count": sum(1 for case in exact_cases if case["stationary_residual"] == ["0", "0", "0"]),
    }


def adapter_spec() -> dict[str, Any]:
    fields = [
        "target_log_prob_digest",
        "transition_kernel_digest",
        "kernel_family",
        "calibration_layer",
        "acceptance_correction",
        "stationary_residual_check",
        "detailed_balance_or_invariance_check",
        "chain_seed_receipt",
        "warmup_schedule_receipt",
        "diagnostics_receipt",
        "negative_fixture_receipt",
        "source_provenance_receipt",
    ]
    return {
        "schema": "StochasticKernelAdapterSpec/v1",
        "required_fields": fields,
        "required_field_count": len(fields),
        "target_tools": ["Stan", "NumPyro", "TensorFlow Probability", "PyMC", "BlackJAX", "Turing.jl"],
        "acceptance_rule": "A sampler adapter cannot claim target-stationary behavior without kernel provenance, calibration or acceptance correction, diagnostics, and a negative fixture.",
    }


def youtube_binding(roadmap: dict[str, Any]) -> dict[str, Any]:
    summary = roadmap["source_summary"]
    architecture_claims = [
        {
            "cluster_id": row["cluster_id"],
            "video_count": row["video_count"],
            "evidence_status": row["evidence_status"],
            "architecture_pull": row["architecture_pull"],
        }
        for row in roadmap["source_to_architecture_claims"]
    ]
    return {
        "roadmap_pass": roadmap["pass"],
        "source_policy": summary["source_policy"],
        "valid_video_count": summary["valid_video_count"],
        "transcript_receipt_count": summary["transcript_receipt_count"],
        "metadata_match_count": summary["metadata_match_count"],
        "dominant_cluster": summary["dominant_cluster"],
        "dominant_cluster_video_count": summary["dominant_cluster_video_count"],
        "raw_transcript_included": summary["raw_transcript_stored"],
        "top_priority": roadmap["top_priority"],
        "architecture_pull_count": len(architecture_claims),
        "architecture_pulls": architecture_claims,
    }


def forum_route() -> dict[str, Any]:
    prompt = "Pass 0109: stochastic-kernel corpus harness, MCMC adapter receipts, YouTube source-lead architecture signals, probabilistic runtime proof packets."
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
    cases = {case["case_id"]: case for case in artifact.get("kernel_cases", [])}
    if artifact.get("schema") != SCHEMA:
        errors.append("schema")
    if artifact.get("source_bindings", {}).get("detailed_balance_pass") != "0108":
        errors.append("detailed_balance_binding")
    if artifact.get("source_bindings", {}).get("youtube_roadmap_pass") != "0102":
        errors.append("youtube_binding")
    if artifact.get("corpus_summary", {}).get("case_count") != 4:
        errors.append("case_count")
    if cases.get("reversible_detailed_balance", {}).get("max_detailed_balance_residual") != "0":
        errors.append("reversible_case")
    if cases.get("stationary_nonreversible_cycle", {}).get("max_detailed_balance_residual") == "0":
        errors.append("nonreversible_boundary")
    if cases.get("row_stochastic_not_stationary", {}).get("stationary_residual") == ["0", "0", "0"]:
        errors.append("row_only_negative")
    if cases.get("uncalibrated_random_walk_source_boundary", {}).get("calibration_required") is not True:
        errors.append("uncalibrated_boundary")
    if artifact.get("adapter_spec", {}).get("required_field_count", 0) < 10:
        errors.append("adapter_spec")
    if artifact.get("market_binding", {}).get("tool_count") != 8:
        errors.append("market_binding")
    if artifact.get("youtube_binding", {}).get("valid_video_count") != 19:
        errors.append("youtube_video_count")
    if any(row.get("status") != "MATCH" for row in artifact.get("flagship_receipts", {}).values()):
        errors.append("flagships")
    if artifact.get("unsupported_claim_count") != 0 or artifact.get("current_promoted_natural_laws") != []:
        errors.append("promotion_boundary")
    return errors


def compose() -> dict[str, Any]:
    detailed = read_json(DETAILED)
    roadmap = read_json(YOUTUBE)
    cases = kernel_cases()
    artifact: dict[str, Any] = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "generated_on": "2026-07-01",
        "status": STATUS_DRIFT,
        "source_bindings": {
            "detailed_balance_pass": detailed["pass"],
            "reaction_corpus_pass": detailed["source_bindings"]["reaction_corpus_pass"],
            "youtube_roadmap_pass": roadmap["pass"],
            "youtube_source_pass": roadmap["source_bindings"]["youtube_pass"],
            "source_packet": "DetailedBalanceMarkovReceipt/v1",
        },
        "source_anchors": detailed["source_anchors"],
        "market_binding": detailed["market_surface"],
        "youtube_binding": youtube_binding(roadmap),
        "kernel_cases": cases,
        "corpus_summary": corpus_summary(cases),
        "adapter_spec": adapter_spec(),
        "law_candidate": {"name": "stochastic_kernel_invariance_receipt_corpus", "status": "LAW_CANDIDATE", "scope": "finite exact kernels plus explicit source-boundary cases for sampler adapters"},
        "promotion_requirements": ["independent kernel corpus", "sampler runtime adapter", "traceable chain diagnostics", "domain reviewer signoff"],
        "unsupported_claim_count": 0,
        "current_promoted_natural_laws": [],
        "non_promotion_statement": "This pass validates a bounded stochastic-kernel corpus and source-boundary adapter contract. It does not prove production sampler correctness, quantum advantage, scientific discovery, or any YouTube video claim.",
        "flagship_receipts": {"forum": forum_route(), "index": index_receipt(), "telos": telos_status()},
    }
    artifact["validation_errors"] = validate_artifact(artifact)
    artifact["status"] = STATUS_MATCH if not artifact["validation_errors"] else STATUS_DRIFT
    artifact["measurements"] = [
        {"id": "corpus_counts", "status": "MATCH" if artifact["corpus_summary"]["case_count"] == 4 else "DRIFT"},
        {"id": "reversible_case", "status": "MATCH" if cases[0]["max_detailed_balance_residual"] == "0" else "DRIFT"},
        {"id": "boundary_cases", "status": "MATCH" if artifact["corpus_summary"]["boundary_expected_count"] == 2 else "DRIFT"},
        {"id": "adapter_spec", "status": "MATCH" if artifact["adapter_spec"]["required_field_count"] >= 10 else "DRIFT"},
        {"id": "youtube_binding", "status": "MATCH" if artifact["youtube_binding"]["valid_video_count"] == 19 else "DRIFT"},
        {"id": "flagships", "status": "MATCH" if all(row["status"] == "MATCH" for row in artifact["flagship_receipts"].values()) else "DRIFT"},
        {"id": "promotion_boundary", "status": "MATCH" if artifact["current_promoted_natural_laws"] == [] else "DRIFT"},
    ]
    unsealed = dict(artifact)
    artifact["seal"] = sha256_obj(unsealed)
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(ROOT / "schemas" / "stochastic-kernel-corpus-harness-receipt-pass-0109.json"))
    args = parser.parse_args()
    artifact = compose()
    write_json(Path(args.out), artifact)
    print(json.dumps({"path": args.out, "seal": artifact["seal"], "status": artifact["status"]}, indent=2, sort_keys=True))
    if artifact["status"] != STATUS_MATCH:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
