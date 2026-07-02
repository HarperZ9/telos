"""Validate pass 0111 multi-kernel runtime suite receipt."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "multi-kernel-runtime-suite-receipt-pass-0111.json"
RESULT = ROOT / "schemas" / "pass-0111-multi-kernel-runtime-suite-validator-result.json"


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
    summary = artifact.get("suite_summary", {})
    results = by_id(artifact.get("case_results", []))
    youtube = artifact.get("youtube_binding", {})
    errors: list[str] = []

    if artifact.get("schema") != "MultiKernelRuntimeSuiteReceipt/v1":
        errors.append("schema")
    if artifact.get("status") != "MULTI_KERNEL_RUNTIME_SUITE_RECEIPT_MATCH":
        errors.append("status")
    if seal != sha256_obj(unsealed):
        errors.append("seal")
    if artifact.get("source_bindings", {}).get("runtime_chain_pass") != "0110":
        errors.append("runtime_chain_pass")
    if artifact.get("source_bindings", {}).get("stochastic_kernel_corpus_pass") != "0109":
        errors.append("corpus_pass")
    if summary.get("case_count") != 3 or summary.get("adapter_missing_field_total") != 0:
        errors.append("summary")
    if summary.get("match_count") != 1 or summary.get("drift_expected_count") != 1 or summary.get("boundary_expected_count") != 1:
        errors.append("classification_counts")
    reversible = results.get("reversible_detailed_balance", {})
    if reversible.get("classification") != "MATCH" or reversible.get("exact_distribution_l1_distance_to_declared_pi", 1) >= 1e-9:
        errors.append("reversible")
    row_only = results.get("row_stochastic_not_stationary", {})
    if row_only.get("classification") != "DRIFT_EXPECTED" or row_only.get("stationary_residual_check", {}).get("status") != "DRIFT":
        errors.append("row_only")
    if row_only.get("exact_distribution_l1_distance_to_declared_pi", 0) <= 0.1:
        errors.append("row_only_l1")
    cycle = results.get("stationary_nonreversible_cycle", {})
    if cycle.get("classification") != "BOUNDARY_EXPECTED" or cycle.get("max_detailed_balance_residual") != "1/3":
        errors.append("cycle")
    if artifact.get("source_boundary_receipts", {}).get("uncalibrated_random_walk_source_boundary", {}).get("status") != "REQUIRES_CALIBRATION":
        errors.append("source_boundary")
    if artifact.get("market_binding", {}).get("tool_count") != 8:
        errors.append("market")
    if youtube.get("valid_video_count") != 19 or youtube.get("raw_transcript_included") is not False:
        errors.append("youtube")
    if any(row.get("status") != "MATCH" for row in artifact.get("measurements", [])):
        errors.append("measurements")
    if any(row.get("status") != "MATCH" for row in artifact.get("flagship_receipts", {}).values()):
        errors.append("flagships")
    if artifact.get("unsupported_claim_count") != 0 or artifact.get("current_promoted_natural_laws") != []:
        errors.append("promotion_boundary")

    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0111MultiKernelRuntimeSuiteValidatorRun/v1",
        "pass": "0111",
        "status": status,
        "match": 1 if status == "MATCH" else 0,
        "drift": 0 if status == "MATCH" else 1,
        "checks": [{
            "artifact": "MultiKernelRuntimeSuiteReceipt",
            "errors": errors,
            "path": "schemas/multi-kernel-runtime-suite-receipt-pass-0111.json",
            "case_count": summary.get("case_count"),
            "classification_counts": {
                "match": summary.get("match_count"),
                "drift_expected": summary.get("drift_expected_count"),
                "boundary_expected": summary.get("boundary_expected_count"),
            },
            "youtube_valid_video_count": youtube.get("valid_video_count"),
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
