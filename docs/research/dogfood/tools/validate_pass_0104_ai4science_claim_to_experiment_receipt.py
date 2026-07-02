"""Validate pass 0104 AI4Science claim-to-experiment receipt."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "ai4science-claim-to-experiment-receipt-pass-0104.json"
RESULT = ROOT / "schemas" / "pass-0104-ai4science-claim-to-experiment-validator-result.json"


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
    source = artifact.get("source_summary", {})
    fields = artifact.get("minimum_packet_fields", [])
    gates = artifact.get("promotion_gates", {})
    unsealed = dict(artifact)
    seal = unsealed.pop("seal", None)
    errors: list[str] = []
    if artifact.get("schema") != "AI4ScienceClaimToExperimentReceipt/v1":
        errors.append("schema")
    if artifact.get("status") != "AI4SCIENCE_CLAIM_TO_EXPERIMENT_RECEIPT_MATCH":
        errors.append("status")
    if seal != sha256_obj(unsealed):
        errors.append("seal")
    if artifact.get("source_bindings", {}).get("roadmap_pass") != "0102":
        errors.append("roadmap_binding")
    if source.get("source_count", 0) < 8 or source.get("official_or_primary_count", 0) < 8:
        errors.append("source_counts")
    for field in ["source_claim", "experiment_or_simulation_protocol", "measurement_receipt", "negative_result_path"]:
        if field not in fields:
            errors.append(f"missing_{field}")
    if artifact.get("market_gap", {}).get("gap_status") != "inferred":
        errors.append("gap_status")
    if len(artifact.get("source_to_receipt_map", [])) != source.get("source_count"):
        errors.append("source_map")
    if len(artifact.get("next_experiments", [])) != 3:
        errors.append("experiments")
    if not all(gates.values()):
        errors.append("promotion_gates")
    if any(row.get("status") != "MATCH" for row in artifact.get("measurements", [])):
        errors.append("measurements")
    if any(row.get("status") != "MATCH" for row in artifact.get("flagship_receipts", {}).values()):
        errors.append("flagships")
    if artifact.get("unsupported_claim_count") != 0 or artifact.get("current_promoted_natural_laws") != []:
        errors.append("promotion_boundary")
    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0104AI4ScienceClaimToExperimentValidatorRun/v1",
        "pass": "0104",
        "status": status,
        "match": 1 if status == "MATCH" else 0,
        "drift": 0 if status == "MATCH" else 1,
        "checks": [{
            "artifact": "AI4ScienceClaimToExperimentReceipt",
            "errors": errors,
            "path": "schemas/ai4science-claim-to-experiment-receipt-pass-0104.json",
            "source_count": source.get("source_count"),
            "official_or_primary_count": source.get("official_or_primary_count"),
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
