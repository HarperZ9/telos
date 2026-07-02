"""Validate pass 0119 Hamiltonian/symplectic receipt."""
from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "hamiltonian-symplectic-receipt-pass-0119.json"
RESULT = ROOT / "schemas" / "pass-0119-hamiltonian-symplectic-validator-result.json"


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)


def sha256_obj(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def parse_fraction(value: str) -> Fraction:
    return Fraction(value)


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n", encoding="utf-8")


def require(condition: bool, errors: list[str], label: str) -> None:
    if not condition:
        errors.append(label)


def det2(matrix: list[list[str]]) -> Fraction:
    m = [[parse_fraction(value) for value in row] for row in matrix]
    return m[0][0] * m[1][1] - m[0][1] * m[1][0]


def validate_cases(artifact: dict, errors: list[str]) -> None:
    cases = artifact.get("symplectic_cases", [])
    require(len(cases) == 3, errors, "case_count")
    require({row.get("h") for row in cases} == {"1/3", "1/2", "2/3"}, errors, "case_h_values")
    for row in cases:
        label = f"case_{row.get('h')}"
        require(row.get("status") == "MATCH", errors, f"{label}:status")
        require(det2(row.get("matrix", [["0", "0"], ["0", "0"]])) == 1, errors, f"{label}:det_recompute")
        require(row.get("determinant") == "1", errors, f"{label}:det_value")
        require(row.get("phase_space_area_preserved") is True, errors, f"{label}:area")
        require(row.get("symplectic_form_preserved") is True, errors, f"{label}:form")
        require(row.get("modified_quadratic_invariant_preserved") is True, errors, f"{label}:modified")
        require(row.get("modified_initial") == row.get("modified_final"), errors, f"{label}:modified_final")


def validate_negative(artifact: dict, errors: list[str]) -> None:
    negative = artifact.get("negative_fixtures", [{}])[0]
    require(negative.get("fixture_id") == "explicit_euler_area_energy_growth", errors, "negative_id")
    require(negative.get("status") == "MATCH", errors, "negative_status")
    require(det2(negative.get("matrix", [["0", "0"], ["0", "0"]])) == Fraction(10, 9), errors, "negative_det_recompute")
    require(negative.get("determinant") == "10/9", errors, "negative_det_value")
    require(negative.get("phase_space_area_preserved") is False, errors, "negative_area")
    require(negative.get("standard_energy_growth") is True, errors, "negative_energy")


def validate() -> dict:
    artifact = read_json(ARTIFACT)
    unsealed = dict(artifact)
    seal = unsealed.pop("seal", None)
    errors: list[str] = []

    require(artifact.get("schema") == "HamiltonianSymplecticReceipt/v1", errors, "schema")
    require(artifact.get("status") == "HAMILTONIAN_SYMPLECTIC_MATCH", errors, "status")
    require(seal == sha256_obj(unsealed), errors, "seal")
    require(artifact.get("source_bindings", {}).get("formal_target_packaging_pass") == "0118", errors, "source_binding")
    require(artifact.get("law_candidate", {}).get("status") == "LAW_CANDIDATE", errors, "law_candidate")
    validate_cases(artifact, errors)
    validate_negative(artifact, errors)
    require(artifact.get("source_surface", {}).get("anchor_count", 0) >= 12, errors, "source_anchor_count")
    require(len(artifact.get("source_surface", {}).get("market_rows", [])) == artifact.get("source_surface", {}).get("anchor_count"), errors, "market_rows")
    require(artifact.get("unsupported_claim_count") == 0, errors, "unsupported_claim_count")
    require(artifact.get("current_promoted_natural_laws") == [], errors, "natural_laws")
    require("does not claim new natural law" in artifact.get("non_promotion_statement", ""), errors, "non_promotion")
    require(all(row.get("status") == "MATCH" for row in artifact.get("flagship_receipts", {}).values()), errors, "flagships")

    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0119HamiltonianSymplecticValidatorRun/v1",
        "pass": "0119",
        "status": status,
        "match": 1 if status == "MATCH" else 0,
        "drift": 0 if status == "MATCH" else 1,
        "checks": [{"artifact": "HamiltonianSymplecticReceipt", "errors": errors, "case_count": len(artifact.get("symplectic_cases", [])), "status": status}],
    }


def main() -> None:
    result = validate()
    write_json(RESULT, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
