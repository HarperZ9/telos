"""Validate pass 0062 heat-equation energy identity."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "heat-equation-energy-identity-pass-0062.json"
RESULT = ROOT / "schemas" / "pass-0062-heat-equation-energy-identity-validator-result.json"


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
    probe = artifact.get("numeric_probe", {})
    if artifact.get("schema") != "HeatEquationEnergyIdentity/v1":
        errors.append("schema")
    if artifact.get("status") != "HEAT_EQUATION_ENERGY_IDENTITY_MATCH":
        errors.append("status")
    if seal != sha256_obj(unsealed):
        errors.append("seal")
    if artifact.get("promotion_state") != "IDENTITY_NOT_PROMOTED_LAW":
        errors.append("promotion_state")
    if artifact.get("current_promoted_natural_laws") != []:
        errors.append("natural_law_promotion")
    if artifact.get("unsupported_claim_count") != 0:
        errors.append("unsupported_claim_count")
    if probe.get("max_symbolic_residual", 1.0) > 1e-12:
        errors.append("symbolic_residual")
    if probe.get("max_finite_difference_residual", 1.0) > 1e-5:
        errors.append("finite_difference_residual")
    if probe.get("energy_monotone_nonincreasing") is not True:
        errors.append("energy_monotonicity")
    if len(artifact.get("source_anchors", [])) < 3:
        errors.append("source_anchors")
    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0062HeatEquationEnergyIdentityValidatorRun/v1",
        "pass": "0062",
        "status": status,
        "match": 1 if status == "MATCH" else 0,
        "drift": 0 if status == "MATCH" else 1,
        "checks": [
            {
                "artifact": "HeatEquationEnergyIdentity",
                "errors": errors,
                "max_finite_difference_residual": probe.get("max_finite_difference_residual"),
                "max_symbolic_residual": probe.get("max_symbolic_residual"),
                "mode_count": probe.get("mode_count"),
                "path": "schemas/heat-equation-energy-identity-pass-0062.json",
                "promotion_state": artifact.get("promotion_state"),
                "status": status,
            }
        ],
    }


def main() -> None:
    result = validate()
    write_json(RESULT, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
