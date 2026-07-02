"""Validate pass 0107 reaction-network corpus harness receipt."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "reaction-network-corpus-harness-receipt-pass-0107.json"
RESULT = ROOT / "schemas" / "pass-0107-reaction-network-corpus-harness-validator-result.json"


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)


def sha256_obj(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n", encoding="utf-8")


def by_id(artifact: dict) -> dict:
    return {row["network_id"]: row for row in artifact.get("network_results", [])}


def validate() -> dict:
    artifact = read_json(ARTIFACT)
    unsealed = dict(artifact)
    seal = unsealed.pop("seal", None)
    summary = artifact.get("corpus_summary", {})
    bridge = artifact.get("buildlang_runtime_bridge", {})
    youtube = artifact.get("youtube_signal_binding", {})
    results = by_id(artifact)
    errors: list[str] = []
    if artifact.get("schema") != "ReactionNetworkCorpusHarnessReceipt/v1":
        errors.append("schema")
    if artifact.get("status") != "REACTION_NETWORK_CORPUS_HARNESS_RECEIPT_MATCH":
        errors.append("status")
    if seal != sha256_obj(unsealed):
        errors.append("seal")
    if artifact.get("source_bindings", {}).get("stoichiometric_pass") != "0106":
        errors.append("stoichiometric_binding")
    if artifact.get("source_bindings", {}).get("buildlang_native_pass") != "0095":
        errors.append("buildlang_binding")
    if summary.get("network_count") != 4 or summary.get("match_count") != 3:
        errors.append("summary")
    if summary.get("drift_expected_count") != 1 or summary.get("derived_invariant_count", 0) < 4:
        errors.append("corpus_counts")
    if results.get("closed_cycle_abc", {}).get("candidate_checks", [{}])[0].get("residual") != [0, 0, 0]:
        errors.append("cycle_residual")
    if results.get("reversible_dimerization", {}).get("candidate_checks", [{}])[0].get("residual") != [0, 0]:
        errors.append("dimer_residual")
    enzyme_checks = results.get("enzyme_product_skeleton", {}).get("candidate_checks", [])
    if len(enzyme_checks) != 2 or not all(row.get("residual_zero") for row in enzyme_checks):
        errors.append("enzyme_residuals")
    open_check = results.get("open_degradation", {}).get("candidate_checks", [{}])[0]
    if results.get("open_degradation", {}).get("status") != "DRIFT_EXPECTED" or open_check.get("residual_zero") is not False:
        errors.append("open_rejection")
    if bridge.get("status") != "TARGET_SPECIFIED_WITH_EXISTING_BUILDC_RECEIPT":
        errors.append("bridge_status")
    if bridge.get("compiler") != "buildc" or bridge.get("verify_check_count") != 18:
        errors.append("bridge_receipt")
    if "residual_zero_check" not in bridge.get("required_kernel_receipts", []):
        errors.append("bridge_requirements")
    if youtube.get("valid_video_count") != 19 or youtube.get("buildlang_scientific_runtime_video_count") != 14:
        errors.append("youtube_binding")
    if any(row.get("status") != "MATCH" for row in artifact.get("measurements", [])):
        errors.append("measurements")
    if any(row.get("status") != "MATCH" for row in artifact.get("flagship_receipts", {}).values()):
        errors.append("flagships")
    if artifact.get("unsupported_claim_count") != 0 or artifact.get("current_promoted_natural_laws") != []:
        errors.append("promotion_boundary")
    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0107ReactionNetworkCorpusHarnessValidatorRun/v1",
        "pass": "0107",
        "status": status,
        "match": 1 if status == "MATCH" else 0,
        "drift": 0 if status == "MATCH" else 1,
        "checks": [{
            "artifact": "ReactionNetworkCorpusHarnessReceipt",
            "errors": errors,
            "path": "schemas/reaction-network-corpus-harness-receipt-pass-0107.json",
            "network_count": summary.get("network_count"),
            "derived_invariant_count": summary.get("derived_invariant_count"),
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
