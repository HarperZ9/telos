"""Validate pass 0081 visual-truth proof-packet refresh."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "visual-truth-proof-packet-refresh-pass-0081.json"
RESULT = ROOT / "schemas" / "pass-0081-visual-truth-proof-packet-refresh-validator-result.json"


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def sha256_obj(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def validate() -> dict:
    artifact = read_json(ARTIFACT)
    errors: list[str] = []
    unsealed = dict(artifact)
    seal = unsealed.pop("seal", None)
    boundary = artifact.get("calibration_boundary", {})
    if artifact.get("schema") != "VisualTruthProofPacketRefresh/v1":
        errors.append("schema")
    if artifact.get("status") != "VISUAL_TRUTH_PROOF_PACKET_REFRESH_MATCH":
        errors.append("status")
    if seal != sha256_obj(unsealed):
        errors.append("seal")
    if artifact.get("targeted_regression", {}).get("status") != "MATCH":
        errors.append("targeted_regression")
    if artifact.get("market_map", {}).get("row_count") != 8:
        errors.append("market_map")
    if any(boundary.get(key) is not False for key in ["hardware_measurement_used", "display_state_mutated", "icc_profile_installed", "lut_written", "physical_calibration_claim"]):
        errors.append("calibration_boundary")
    if artifact.get("unsupported_claim_count") != 0 or artifact.get("current_promoted_natural_laws") != []:
        errors.append("promotion_boundary")
    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0081VisualTruthProofPacketRefreshValidatorRun/v1",
        "pass": "0081",
        "status": status,
        "match": 1 if status == "MATCH" else 0,
        "drift": 0 if status == "MATCH" else 1,
        "checks": [{
            "artifact": "VisualTruthProofPacketRefresh",
            "errors": errors,
            "path": "schemas/visual-truth-proof-packet-refresh-pass-0081.json",
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
