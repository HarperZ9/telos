"""Validate pass 0105 reaction mass-conservation receipt."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "reaction-mass-conservation-receipt-pass-0105.json"
RESULT = ROOT / "schemas" / "pass-0105-reaction-mass-conservation-validator-result.json"


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
    probe = artifact.get("numerical_probe", {})
    unsealed = dict(artifact)
    seal = unsealed.pop("seal", None)
    errors: list[str] = []
    if artifact.get("schema") != "ReactionMassConservationReceipt/v1":
        errors.append("schema")
    if artifact.get("status") != "REACTION_MASS_CONSERVATION_RECEIPT_MATCH":
        errors.append("status")
    if seal != sha256_obj(unsealed):
        errors.append("seal")
    if artifact.get("source_bindings", {}).get("ai4science_pass") != "0104":
        errors.append("ai4science_binding")
    if artifact.get("reaction", {}).get("stoichiometry") != {"A": -1, "B": 1}:
        errors.append("stoichiometry")
    if artifact.get("proof", {}).get("symbolic_derivative_total") != "0":
        errors.append("symbolic_proof")
    if probe.get("grid_points", 0) < 80 or probe.get("max_exact_invariant_drift", 1) > 1e-12:
        errors.append("exact_probe")
    if probe.get("max_euler_invariant_drift", 1) > 1e-10:
        errors.append("euler_probe")
    if artifact.get("negative_fixture", {}).get("breaks_invariant") is not True:
        errors.append("negative_fixture")
    if artifact.get("law_candidate", {}).get("status") != "LAW_CANDIDATE":
        errors.append("law_candidate")
    if any(row.get("status") != "MATCH" for row in artifact.get("measurements", [])):
        errors.append("measurements")
    if any(row.get("status") != "MATCH" for row in artifact.get("flagship_receipts", {}).values()):
        errors.append("flagships")
    if artifact.get("unsupported_claim_count") != 0 or artifact.get("current_promoted_natural_laws") != []:
        errors.append("promotion_boundary")
    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0105ReactionMassConservationValidatorRun/v1",
        "pass": "0105",
        "status": status,
        "match": 1 if status == "MATCH" else 0,
        "drift": 0 if status == "MATCH" else 1,
        "checks": [{
            "artifact": "ReactionMassConservationReceipt",
            "errors": errors,
            "path": "schemas/reaction-mass-conservation-receipt-pass-0105.json",
            "max_exact_invariant_drift": probe.get("max_exact_invariant_drift"),
            "max_euler_invariant_drift": probe.get("max_euler_invariant_drift"),
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
