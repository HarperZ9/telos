"""Compose pass 0111 multi-kernel runtime suite receipt."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import subprocess
from pathlib import Path
from typing import Any

SCHEMA = "MultiKernelRuntimeSuiteReceipt/v1"
PASS_ID = "0111"
STATUS_MATCH = "MULTI_KERNEL_RUNTIME_SUITE_RECEIPT_MATCH"
STATUS_DRIFT = "MULTI_KERNEL_RUNTIME_SUITE_RECEIPT_DRIFT"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
CORPUS = ROOT / "schemas" / "stochastic-kernel-corpus-harness-receipt-pass-0109.json"
RUNTIME = ROOT / "schemas" / "stochastic-runtime-chain-receipt-pass-0110.json"
RUNTIME_COMPOSER = ROOT / "tools" / "compose_stochastic_runtime_chain_receipt.py"


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


def load_runtime_module():
    spec = importlib.util.spec_from_file_location("pass0110_runtime", RUNTIME_COMPOSER)
    if not spec or not spec.loader:
        raise RuntimeError("could not load pass 0110 composer")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


RT = load_runtime_module()


def run_json(command: list[str], timeout: int = 45) -> tuple[int, str, str, dict[str, Any]]:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    parsed = json.loads(result.stdout) if result.returncode == 0 and result.stdout.strip().startswith("{") else {}
    return result.returncode, result.stdout, result.stderr, parsed


def forum_route() -> dict[str, Any]:
    prompt = "Pass 0111: multi-kernel stochastic runtime suite classifying MATCH, DRIFT_EXPECTED, and BOUNDARY_EXPECTED cases with YouTube source-lead binding."
    code, stdout, stderr, parsed = run_json(["forum", "route", "--json", prompt], timeout=30)
    return {"status": "MATCH" if code == 0 else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "decided": parsed.get("decided"), "confidence": parsed.get("confidence"), "needs_escalation": parsed.get("needs_escalation"), "top_candidates": parsed.get("candidates", [])[:5]}


def index_receipt() -> dict[str, Any]:
    code, stdout, stderr, parsed = run_json(["index", "context-envelope", "--root", ".", "--budget", "1200", "--json"], timeout=45)
    return {"status": "MATCH" if code == 0 and parsed.get("verification_verdict") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "schema": parsed.get("schema"), "verification_verdict": parsed.get("verification_verdict"), "graph_pack_sha256": parsed.get("recheck", {}).get("graph_pack_sha256"), "source_refs_only": parsed.get("privacy", {}).get("source_refs_only")}


def telos_status() -> dict[str, Any]:
    code, stdout, stderr, parsed = run_json(["node", "demo/status.mjs", "--summary"], timeout=30)
    return {"status": "MATCH" if code == 0 and parsed.get("status") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "tool_version": parsed.get("tool_version"), "tool": parsed.get("tool")}


def row_sums(p: list[list[Any]]) -> list[Any]:
    return [sum(row) for row in p]


def adapter_contract(adapter_spec: dict[str, Any], receipt: dict[str, Any]) -> dict[str, Any]:
    required = adapter_spec["required_fields"]
    missing = [field for field in required if field not in receipt]
    return {"required_fields": required, "required_field_count": len(required), "required_fields_satisfied": len(required) - len(missing), "missing_fields": missing}


def classify(case_id: str, stat_max: str, db_max: str) -> str:
    if case_id == "reversible_detailed_balance" and stat_max == "0" and db_max == "0":
        return "MATCH"
    if case_id == "row_stochastic_not_stationary" and stat_max != "0":
        return "DRIFT_EXPECTED"
    if case_id == "stationary_nonreversible_cycle" and stat_max == "0" and db_max != "0":
        return "BOUNDARY_EXPECTED"
    return "DRIFT"


def case_receipt(corpus: dict[str, Any], case: dict[str, Any], idx: int) -> dict[str, Any]:
    pi = RT.parse_vector(case["pi"])
    p = RT.parse_matrix(case["transition_matrix"])
    stationary = RT.stationary_residual(pi, p)
    balance = RT.detailed_balance_residuals(pi, p)
    stat_max = RT.fstr(RT.max_abs(stationary))
    db_max = RT.fstr(RT.max_abs(balance))
    exact = RT.exact_distribution(p, 5050)
    target = [float(value) for value in pi]
    empirical = RT.seeded_chain(p, 1111 + idx, 50, 5000)
    receipt = {
        "target_log_prob_digest": sha256_obj({"target_distribution": case["pi"], "case_id": case["case_id"]}),
        "transition_kernel_digest": case["transition_kernel_digest"],
        "kernel_family": "finite_markov_kernel",
        "calibration_layer": "suite_case_exact_matrix",
        "acceptance_correction": "identity_or_boundary",
        "stationary_residual_check": {"status": "MATCH" if stat_max == "0" else "DRIFT", "residual": RT.frow(stationary), "max_residual": stat_max},
        "detailed_balance_or_invariance_check": {"status": "MATCH" if db_max == "0" else "BOUNDARY_EXPECTED", "max_residual": db_max},
        "chain_seed_receipt": {"seed": 1111 + idx, "prng": "python.random.Random", "reproducible": True},
        "warmup_schedule_receipt": {"warmup_steps": 50, "sample_steps": 5000, "start_state": 0},
        "diagnostics_receipt": {"exact_distribution": exact, "empirical_distribution": empirical["empirical_distribution"], "empirical_counts": empirical["counts"]},
        "negative_fixture_receipt": {"source_case_status": case["status"]},
        "source_provenance_receipt": {"stochastic_kernel_corpus_pass": corpus["pass"], "case_id": case["case_id"]},
    }
    adapter = adapter_contract(corpus["adapter_spec"], receipt)
    classification = classify(case["case_id"], stat_max, db_max)
    return {
        "case_id": case["case_id"],
        "expected_status": case["status"],
        "classification": classification,
        "row_sums": RT.frow(row_sums(p)),
        "stationary_residual_check": receipt["stationary_residual_check"],
        "detailed_balance_or_invariance_check": receipt["detailed_balance_or_invariance_check"],
        "max_detailed_balance_residual": db_max,
        "exact_distribution_l1_distance_to_declared_pi": RT.l1_distance(exact, target),
        "empirical_l1_distance_to_declared_pi": RT.l1_distance(empirical["empirical_distribution"], target),
        "adapter_contract": adapter,
        "runtime_receipt": receipt,
    }


def suite_summary(results: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "case_count": len(results),
        "match_count": sum(1 for row in results if row["classification"] == "MATCH"),
        "drift_expected_count": sum(1 for row in results if row["classification"] == "DRIFT_EXPECTED"),
        "boundary_expected_count": sum(1 for row in results if row["classification"] == "BOUNDARY_EXPECTED"),
        "adapter_missing_field_total": sum(len(row["adapter_contract"]["missing_fields"]) for row in results),
    }


def validate_artifact(artifact: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    results = {row["case_id"]: row for row in artifact.get("case_results", [])}
    summary = artifact.get("suite_summary", {})
    if artifact.get("schema") != SCHEMA:
        errors.append("schema")
    if artifact.get("source_bindings", {}).get("runtime_chain_pass") != "0110":
        errors.append("runtime_binding")
    if summary.get("case_count") != 3 or summary.get("adapter_missing_field_total") != 0:
        errors.append("summary")
    if results.get("reversible_detailed_balance", {}).get("classification") != "MATCH":
        errors.append("reversible")
    if results.get("row_stochastic_not_stationary", {}).get("classification") != "DRIFT_EXPECTED":
        errors.append("row_only")
    if results.get("stationary_nonreversible_cycle", {}).get("classification") != "BOUNDARY_EXPECTED":
        errors.append("cycle")
    if artifact.get("source_boundary_receipts", {}).get("uncalibrated_random_walk_source_boundary", {}).get("status") != "REQUIRES_CALIBRATION":
        errors.append("source_boundary")
    if artifact.get("youtube_binding", {}).get("valid_video_count") != 19:
        errors.append("youtube")
    if any(row.get("status") != "MATCH" for row in artifact.get("flagship_receipts", {}).values()):
        errors.append("flagships")
    if artifact.get("unsupported_claim_count") != 0 or artifact.get("current_promoted_natural_laws") != []:
        errors.append("promotion_boundary")
    return errors


def compose() -> dict[str, Any]:
    corpus = read_json(CORPUS)
    runtime = read_json(RUNTIME)
    case_ids = ["reversible_detailed_balance", "row_stochastic_not_stationary", "stationary_nonreversible_cycle"]
    cases = {row["case_id"]: row for row in corpus["kernel_cases"]}
    results = [case_receipt(corpus, cases[case_id], idx) for idx, case_id in enumerate(case_ids)]
    source_boundaries = {row["case_id"]: row for row in corpus["kernel_cases"] if row["case_type"] == "source_boundary"}
    artifact: dict[str, Any] = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "generated_on": "2026-07-01",
        "status": STATUS_DRIFT,
        "source_bindings": {
            "runtime_chain_pass": runtime["pass"],
            "stochastic_kernel_corpus_pass": corpus["pass"],
            "detailed_balance_pass": corpus["source_bindings"]["detailed_balance_pass"],
            "youtube_roadmap_pass": corpus["source_bindings"]["youtube_roadmap_pass"],
            "youtube_source_pass": corpus["source_bindings"]["youtube_source_pass"],
        },
        "suite_summary": suite_summary(results),
        "case_results": results,
        "source_boundary_receipts": source_boundaries,
        "youtube_binding": corpus["youtube_binding"],
        "market_binding": corpus["market_binding"],
        "buildlang_target": {"target_kernel": "multi_kernel_stochastic_runtime_suite.bld", "status": "TARGET_INTERFACE_NOT_COMPILED"},
        "law_candidate": {"name": "multi_kernel_runtime_receipts_classify_match_drift_boundary", "status": "LAW_CANDIDATE", "scope": "finite kernels under one adapter interface"},
        "unsupported_claim_count": 0,
        "current_promoted_natural_laws": [],
        "non_promotion_statement": "This pass classifies finite stochastic kernels under one receipt interface. It does not prove production sampler correctness, compile BuildLang, validate YouTube video claims, or promote a natural law.",
        "flagship_receipts": {"forum": forum_route(), "index": index_receipt(), "telos": telos_status()},
    }
    artifact["validation_errors"] = validate_artifact(artifact)
    artifact["status"] = STATUS_MATCH if not artifact["validation_errors"] else STATUS_DRIFT
    artifact["measurements"] = [
        {"id": "suite_summary", "status": "MATCH" if artifact["suite_summary"]["adapter_missing_field_total"] == 0 else "DRIFT"},
        {"id": "reversible", "status": "MATCH" if results[0]["classification"] == "MATCH" else "DRIFT"},
        {"id": "row_only", "status": "MATCH" if results[1]["classification"] == "DRIFT_EXPECTED" else "DRIFT"},
        {"id": "cycle_boundary", "status": "MATCH" if results[2]["classification"] == "BOUNDARY_EXPECTED" else "DRIFT"},
        {"id": "youtube_binding", "status": "MATCH" if artifact["youtube_binding"]["valid_video_count"] == 19 else "DRIFT"},
        {"id": "flagships", "status": "MATCH" if all(row["status"] == "MATCH" for row in artifact["flagship_receipts"].values()) else "DRIFT"},
        {"id": "promotion_boundary", "status": "MATCH" if artifact["current_promoted_natural_laws"] == [] else "DRIFT"},
    ]
    unsealed = dict(artifact)
    artifact["seal"] = sha256_obj(unsealed)
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(ROOT / "schemas" / "multi-kernel-runtime-suite-receipt-pass-0111.json"))
    args = parser.parse_args()
    artifact = compose()
    write_json(Path(args.out), artifact)
    print(json.dumps({"path": args.out, "seal": artifact["seal"], "status": artifact["status"]}, indent=2, sort_keys=True))
    if artifact["status"] != STATUS_MATCH:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
