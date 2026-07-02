"""Validate pass 0109 stochastic-kernel corpus harness receipt."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "stochastic-kernel-corpus-harness-receipt-pass-0109.json"
RESULT = ROOT / "schemas" / "pass-0109-stochastic-kernel-corpus-harness-validator-result.json"


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)


def sha256_obj(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n", encoding="utf-8")


def by_id(rows: list[dict]) -> dict[str, dict]:
    return {row["case_id"]: row for row in rows}


def validate() -> dict:
    artifact = read_json(ARTIFACT)
    unsealed = dict(artifact)
    seal = unsealed.pop("seal", None)
    cases = by_id(artifact.get("kernel_cases", []))
    summary = artifact.get("corpus_summary", {})
    adapter = artifact.get("adapter_spec", {})
    youtube = artifact.get("youtube_binding", {})
    errors: list[str] = []

    if artifact.get("schema") != "StochasticKernelCorpusHarnessReceipt/v1":
        errors.append("schema")
    if artifact.get("status") != "STOCHASTIC_KERNEL_CORPUS_HARNESS_RECEIPT_MATCH":
        errors.append("status")
    if seal != sha256_obj(unsealed):
        errors.append("seal")
    if artifact.get("source_bindings", {}).get("detailed_balance_pass") != "0108":
        errors.append("detailed_balance_pass")
    if artifact.get("source_bindings", {}).get("youtube_roadmap_pass") != "0102":
        errors.append("youtube_roadmap_pass")
    if summary.get("case_count") != 4 or summary.get("exact_kernel_count") != 3:
        errors.append("summary_counts")
    if summary.get("match_count") != 1 or summary.get("drift_expected_count") != 1 or summary.get("boundary_expected_count") != 2:
        errors.append("status_counts")
    reversible = cases.get("reversible_detailed_balance", {})
    if reversible.get("stationary_residual") != ["0", "0", "0"] or reversible.get("max_detailed_balance_residual") != "0":
        errors.append("reversible_case")
    cycle = cases.get("stationary_nonreversible_cycle", {})
    if cycle.get("stationary_residual") != ["0", "0", "0"] or cycle.get("max_detailed_balance_residual") == "0":
        errors.append("cycle_boundary")
    row_only = cases.get("row_stochastic_not_stationary", {})
    if row_only.get("row_sums") != ["1", "1", "1"] or row_only.get("stationary_residual") == ["0", "0", "0"]:
        errors.append("row_only_negative")
    source_boundary = cases.get("uncalibrated_random_walk_source_boundary", {})
    if source_boundary.get("status") != "REQUIRES_CALIBRATION" or source_boundary.get("calibration_required") is not True:
        errors.append("source_boundary")
    for field in ["target_log_prob_digest", "transition_kernel_digest", "diagnostics_receipt", "negative_fixture_receipt"]:
        if field not in adapter.get("required_fields", []):
            errors.append(f"adapter_{field}")
    if artifact.get("market_binding", {}).get("tool_count") != 8:
        errors.append("market_binding")
    if youtube.get("valid_video_count") != 19 or youtube.get("transcript_receipt_count") != 19:
        errors.append("youtube_counts")
    if youtube.get("raw_transcript_included") is not False:
        errors.append("youtube_raw_transcript_boundary")
    if any(row.get("status") != "MATCH" for row in artifact.get("measurements", [])):
        errors.append("measurements")
    if any(row.get("status") != "MATCH" for row in artifact.get("flagship_receipts", {}).values()):
        errors.append("flagships")
    if artifact.get("unsupported_claim_count") != 0 or artifact.get("current_promoted_natural_laws") != []:
        errors.append("promotion_boundary")

    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0109StochasticKernelCorpusHarnessValidatorRun/v1",
        "pass": "0109",
        "status": status,
        "match": 1 if status == "MATCH" else 0,
        "drift": 0 if status == "MATCH" else 1,
        "checks": [{
            "artifact": "StochasticKernelCorpusHarnessReceipt",
            "errors": errors,
            "path": "schemas/stochastic-kernel-corpus-harness-receipt-pass-0109.json",
            "case_count": summary.get("case_count"),
            "youtube_valid_video_count": youtube.get("valid_video_count"),
            "tool_count": artifact.get("market_binding", {}).get("tool_count"),
            "status": status,
        }],
    }


def main() -> None:
    result = validate()
    write_json(RESULT, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
