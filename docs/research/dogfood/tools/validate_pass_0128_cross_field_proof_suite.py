"""Validate pass 0128 cross-field proof suite."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "cross-field-proof-suite-pass-0128.json"
RESULT = ROOT / "schemas" / "pass-0128-cross-field-proof-suite-validator-result.json"


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)


def sha256_obj(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n", encoding="utf-8")


def require(condition: bool, errors: list[str], label: str) -> None:
    if not condition:
        errors.append(label)


def validate() -> dict:
    artifact = read_json(ARTIFACT)
    unsealed = dict(artifact)
    seal = unsealed.pop("seal", None)
    fixtures = artifact.get("fixtures", [])
    fixture_ids = {row.get("fixture_id") for row in fixtures}
    negatives = artifact.get("negative_fixtures", [])
    errors: list[str] = []

    require(artifact.get("schema") == "CrossFieldProofSuiteReceipt/v1", errors, "schema")
    require(artifact.get("status") == "CROSS_FIELD_PROOF_SUITE_MATCH", errors, "status")
    require(seal == sha256_obj(unsealed), errors, "seal")
    require(artifact.get("source_bindings", {}).get("runtime_layer_pass") == "0122", errors, "runtime_layer_binding")
    require(artifact.get("source_bindings", {}).get("demotion_gate_pass") == "0126", errors, "demotion_gate_binding")
    require(artifact.get("source_bindings", {}).get("runtime_router_pass") == "0127", errors, "runtime_router_binding")
    require(len(artifact.get("source_receipts", [])) >= 4, errors, "source_count")
    require(all(row.get("status") == "GATHER_VERIFIED" for row in artifact.get("source_receipts", [])), errors, "source_status")
    require({"formal_odd_sum_identity", "quantum_born_normalization", "bounded_knapsack_exact_oracle", "euler_prime_counterexample_revision"} <= fixture_ids, errors, "fixture_ids")
    require(all(row.get("runtime_branch", {}).get("status") == "MATCH" for row in fixtures), errors, "runtime_status")
    require(all(row.get("verifier_status") == "PROBE_MATCH" for row in fixtures), errors, "verifier_status")
    require(len(negatives) == 4 and all(row.get("status") == "REJECTED" for row in negatives), errors, "negative_fixtures")
    require(artifact.get("unsupported_claim_count") == 0, errors, "unsupported_claim_count")
    require(artifact.get("current_promoted_natural_laws") == [], errors, "natural_laws")
    require(all(row.get("status") == "MATCH" for row in artifact.get("flagship_receipts", {}).values()), errors, "flagships")

    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0128CrossFieldProofSuiteValidatorRun/v1",
        "pass": "0128",
        "status": status,
        "checks": [{"artifact": "CrossFieldProofSuite", "errors": errors, "status": status, "fixture_count": len(fixtures), "negative_count": len(negatives)}],
    }


def main() -> None:
    result = validate()
    write_json(RESULT, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
