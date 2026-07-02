"""Validate pass 0108 detailed-balance Markov receipt."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "detailed-balance-markov-receipt-pass-0108.json"
RESULT = ROOT / "schemas" / "pass-0108-detailed-balance-markov-validator-result.json"


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
    positive = artifact.get("reversible_kernel", {})
    negatives = artifact.get("negative_fixtures", {})
    row_only = negatives.get("row_stochastic_not_stationary", {})
    circulation = negatives.get("stationary_not_reversible", {})
    errors: list[str] = []
    if artifact.get("schema") != "DetailedBalanceMarkovReceipt/v1":
        errors.append("schema")
    if artifact.get("status") != "DETAILED_BALANCE_MARKOV_RECEIPT_MATCH":
        errors.append("status")
    if seal != sha256_obj(unsealed):
        errors.append("seal")
    if artifact.get("source_bindings", {}).get("reaction_corpus_pass") != "0107":
        errors.append("reaction_corpus_binding")
    if artifact.get("proof", {}).get("symbolic_step") != "sum_i pi_i P_ij = sum_i pi_j P_ji = pi_j":
        errors.append("proof_step")
    if positive.get("pi") != ["1/2", "1/3", "1/6"]:
        errors.append("pi")
    if positive.get("stationary_residual") != ["0", "0", "0"] or positive.get("max_detailed_balance_residual") != "0":
        errors.append("positive_kernel")
    if positive.get("simulation_probe", {}).get("l1_distance_to_pi", 1) >= 1e-6:
        errors.append("simulation_probe")
    if row_only.get("row_sums") != ["1", "1", "1"] or row_only.get("stationary_residual") == ["0", "0", "0"]:
        errors.append("row_only_negative")
    if circulation.get("stationary_residual") != ["0", "0", "0"] or circulation.get("max_detailed_balance_residual") == "0":
        errors.append("nonnecessary_boundary")
    if artifact.get("market_surface", {}).get("tool_count", 0) < 8:
        errors.append("market_surface")
    if any(row.get("status") != "MATCH" for row in artifact.get("measurements", [])):
        errors.append("measurements")
    if any(row.get("status") != "MATCH" for row in artifact.get("flagship_receipts", {}).values()):
        errors.append("flagships")
    if artifact.get("unsupported_claim_count") != 0 or artifact.get("current_promoted_natural_laws") != []:
        errors.append("promotion_boundary")
    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0108DetailedBalanceMarkovValidatorRun/v1",
        "pass": "0108",
        "status": status,
        "match": 1 if status == "MATCH" else 0,
        "drift": 0 if status == "MATCH" else 1,
        "checks": [{
            "artifact": "DetailedBalanceMarkovReceipt",
            "errors": errors,
            "path": "schemas/detailed-balance-markov-receipt-pass-0108.json",
            "simulation_l1_distance_to_pi": positive.get("simulation_probe", {}).get("l1_distance_to_pi"),
            "tool_count": artifact.get("market_surface", {}).get("tool_count"),
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
