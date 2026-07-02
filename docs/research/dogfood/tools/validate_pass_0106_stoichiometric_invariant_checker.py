"""Validate pass 0106 stoichiometric invariant checker receipt."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "stoichiometric-invariant-checker-receipt-pass-0106.json"
RESULT = ROOT / "schemas" / "pass-0106-stoichiometric-invariant-checker-validator-result.json"


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
    vector = artifact.get("derived_conservation_vectors", [{}])[0]
    probe = artifact.get("numerical_probe", {})
    negative = artifact.get("negative_network", {})
    youtube = artifact.get("youtube_signal_binding", {})
    errors: list[str] = []
    if artifact.get("schema") != "StoichiometricInvariantCheckerReceipt/v1":
        errors.append("schema")
    if artifact.get("status") != "STOICHIOMETRIC_INVARIANT_CHECKER_RECEIPT_MATCH":
        errors.append("status")
    if seal != sha256_obj(unsealed):
        errors.append("seal")
    if artifact.get("source_bindings", {}).get("reaction_pass") != "0105":
        errors.append("reaction_binding")
    if artifact.get("source_bindings", {}).get("ai4science_pass") != "0104":
        errors.append("ai4science_binding")
    if youtube.get("roadmap_pass") != "0102" or youtube.get("youtube_pass") != "0085":
        errors.append("youtube_binding")
    if youtube.get("valid_video_count") != 19 or youtube.get("transcript_receipt_count") != 19:
        errors.append("youtube_receipt_counts")
    if vector.get("vector") != [1, 1, 1] or vector.get("invariant") != "A+B+C":
        errors.append("conservation_vector")
    if vector.get("residual") != [0, 0, 0]:
        errors.append("conservation_residual")
    if probe.get("grid_points", 0) < 150 or probe.get("max_total_drift", 1) > 1e-10:
        errors.append("closed_probe")
    if negative.get("status") != "DRIFT_EXPECTED" or negative.get("candidate_residual") == [0, 0, 0, 0]:
        errors.append("negative_residual")
    if negative.get("breaks_invariant") is not True or negative.get("max_total_drift", 0) <= 0.01:
        errors.append("negative_probe")
    if any(row.get("status") != "MATCH" for row in artifact.get("measurements", [])):
        errors.append("measurements")
    if any(row.get("status") != "MATCH" for row in artifact.get("flagship_receipts", {}).values()):
        errors.append("flagships")
    if artifact.get("unsupported_claim_count") != 0 or artifact.get("current_promoted_natural_laws") != []:
        errors.append("promotion_boundary")
    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0106StoichiometricInvariantCheckerValidatorRun/v1",
        "pass": "0106",
        "status": status,
        "match": 1 if status == "MATCH" else 0,
        "drift": 0 if status == "MATCH" else 1,
        "checks": [{
            "artifact": "StoichiometricInvariantCheckerReceipt",
            "errors": errors,
            "path": "schemas/stoichiometric-invariant-checker-receipt-pass-0106.json",
            "closed_max_total_drift": probe.get("max_total_drift"),
            "negative_max_total_drift": negative.get("max_total_drift"),
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
