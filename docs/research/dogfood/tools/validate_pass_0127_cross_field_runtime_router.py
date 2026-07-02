"""Validate pass 0127 cross-field scientific runtime router."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "cross-field-scientific-runtime-router-pass-0127.json"
RESULT = ROOT / "schemas" / "pass-0127-cross-field-runtime-router-validator-result.json"


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
    negatives = artifact.get("negative_fixtures", [])
    errors: list[str] = []

    require(artifact.get("schema") == "CrossFieldScientificRuntimeRouterReceipt/v1", errors, "schema")
    require(artifact.get("status") == "CROSS_FIELD_SCIENTIFIC_RUNTIME_ROUTER_MATCH", errors, "status")
    require(seal == sha256_obj(unsealed), errors, "seal")
    require(artifact.get("source_bindings", {}).get("youtube_router_pass") == "0125", errors, "youtube_binding")
    require(artifact.get("source_bindings", {}).get("demotion_gate_pass") == "0126", errors, "gate_binding")
    require(artifact.get("source_bindings", {}).get("runtime_layer_pass") == "0122", errors, "runtime_layer_binding")
    require(artifact.get("demotion_gate_result", {}).get("gate_status") == "ACCEPTED", errors, "gate_status")
    require(artifact.get("exact_oracle", {}).get("status") == "MATCH", errors, "oracle_status")
    require(artifact.get("exact_oracle", {}).get("probability_sum") == "1", errors, "oracle_sum")
    require(artifact.get("runtime_branch", {}).get("status") == "MATCH", errors, "runtime_status")
    require(artifact.get("runtime_branch", {}).get("probability_sum_abs_drift", 1) <= artifact.get("runtime_branch", {}).get("tolerance", 0), errors, "runtime_drift")
    require(len(negatives) == 3 and all(row.get("status") == "REJECTED" for row in negatives), errors, "negative_fixtures")
    require(artifact.get("interpretation_claim_status") == "SOURCE_LEAD_ONLY", errors, "interpretation_boundary")
    require(artifact.get("market_claim_status") == "UNVERIFIED", errors, "market_boundary")
    require(all(row.get("status") == "MATCH" for row in artifact.get("flagship_receipts", {}).values()), errors, "flagships")
    require(artifact.get("unsupported_claim_count") == 0, errors, "unsupported_claim_count")
    require(artifact.get("current_promoted_natural_laws") == [], errors, "natural_laws")

    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0127CrossFieldRuntimeRouterValidatorRun/v1",
        "pass": "0127",
        "status": status,
        "checks": [{"artifact": "CrossFieldScientificRuntimeRouter", "errors": errors, "status": status, "negative_count": len(negatives)}],
    }


def main() -> None:
    result = validate()
    write_json(RESULT, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
