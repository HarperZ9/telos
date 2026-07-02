"""Validate pass 0110 stochastic-runtime chain receipt."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "stochastic-runtime-chain-receipt-pass-0110.json"
RESULT = ROOT / "schemas" / "pass-0110-stochastic-runtime-chain-validator-result.json"


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)


def sha256_obj(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n", encoding="utf-8")


def validate() -> dict:
    artifact = read_json(ARTIFACT)
    unsealed = dict(artifact)
    seal = unsealed.pop("seal", None)
    runtime = artifact.get("runtime_receipt", {})
    adapter = artifact.get("adapter_contract", {})
    diagnostics = runtime.get("diagnostics_receipt", {})
    negative = runtime.get("negative_fixture_receipt", {})
    youtube = artifact.get("youtube_binding", {})
    errors: list[str] = []

    if artifact.get("schema") != "StochasticRuntimeChainReceipt/v1":
        errors.append("schema")
    if artifact.get("status") != "STOCHASTIC_RUNTIME_CHAIN_RECEIPT_MATCH":
        errors.append("status")
    if seal != sha256_obj(unsealed):
        errors.append("seal")
    if artifact.get("source_bindings", {}).get("stochastic_kernel_corpus_pass") != "0109":
        errors.append("corpus_binding")
    if artifact.get("source_bindings", {}).get("youtube_roadmap_pass") != "0102":
        errors.append("youtube_roadmap_binding")
    if adapter.get("missing_fields") != []:
        errors.append("adapter_missing_fields")
    if adapter.get("required_fields_satisfied") != adapter.get("required_field_count"):
        errors.append("adapter_count")
    if runtime.get("transition_kernel_digest") != artifact.get("selected_case", {}).get("transition_kernel_digest"):
        errors.append("transition_digest")
    if runtime.get("chain_seed_receipt", {}).get("seed") != 1109:
        errors.append("seed")
    if runtime.get("warmup_schedule_receipt", {}).get("warmup_steps") != 50:
        errors.append("warmup")
    if diagnostics.get("exact_distribution_l1_distance_to_pi", 1) >= 1e-9:
        errors.append("exact_distribution")
    if diagnostics.get("empirical_l1_distance_to_pi", 1) >= 0.08:
        errors.append("empirical_distribution")
    if diagnostics.get("stationary_residual_check", {}).get("status") != "MATCH":
        errors.append("stationary_check")
    if diagnostics.get("detailed_balance_or_invariance_check", {}).get("status") != "MATCH":
        errors.append("balance_check")
    if negative.get("row_stochastic_not_stationary", {}).get("status") != "DRIFT_EXPECTED":
        errors.append("negative_fixture")
    if negative.get("uncalibrated_random_walk_source_boundary", {}).get("status") != "REQUIRES_CALIBRATION":
        errors.append("source_boundary")
    if artifact.get("buildlang_target", {}).get("status") != "TARGET_INTERFACE_NOT_COMPILED":
        errors.append("buildlang_boundary")
    if youtube.get("valid_video_count") != 19 or youtube.get("raw_transcript_included") is not False:
        errors.append("youtube_binding")
    if any(row.get("status") != "MATCH" for row in artifact.get("measurements", [])):
        errors.append("measurements")
    if any(row.get("status") != "MATCH" for row in artifact.get("flagship_receipts", {}).values()):
        errors.append("flagships")
    if artifact.get("unsupported_claim_count") != 0 or artifact.get("current_promoted_natural_laws") != []:
        errors.append("promotion_boundary")

    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0110StochasticRuntimeChainValidatorRun/v1",
        "pass": "0110",
        "status": status,
        "match": 1 if status == "MATCH" else 0,
        "drift": 0 if status == "MATCH" else 1,
        "checks": [{
            "artifact": "StochasticRuntimeChainReceipt",
            "errors": errors,
            "path": "schemas/stochastic-runtime-chain-receipt-pass-0110.json",
            "empirical_l1_distance_to_pi": diagnostics.get("empirical_l1_distance_to_pi"),
            "exact_distribution_l1_distance_to_pi": diagnostics.get("exact_distribution_l1_distance_to_pi"),
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
