"""Validate pass 0122 scientific runtime receipt layer."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "scientific-runtime-receipt-layer-spec-pass-0122.json"
RESULT = ROOT / "schemas" / "pass-0122-scientific-runtime-layer-validator-result.json"


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
    sources = artifact.get("source_matrix", [])
    experiment = artifact.get("long_horizon_experiment", {})
    exact_cases = experiment.get("exact_cases", [])
    errors: list[str] = []

    require(artifact.get("schema") == "ScientificRuntimeReceiptLayerSpec/v1", errors, "schema")
    require(artifact.get("status") == "SCIENTIFIC_RUNTIME_RECEIPT_LAYER_MATCH", errors, "status")
    require(seal == sha256_obj(unsealed), errors, "seal")
    require(artifact.get("source_bindings", {}).get("growth_vector_pass") == "0121", errors, "growth_binding")
    require(artifact.get("source_bindings", {}).get("runtime_branch_pass") == "0120", errors, "runtime_binding")
    require(len(sources) >= 17, errors, "source_count")
    require(sum(row.get("local_gather_status", "").startswith("GATHER_VERIFIED") for row in sources) >= 14, errors, "gathered_sources")
    require(all(row.get("gap_status") == "inferred" for row in sources), errors, "gap_status")
    require(len(artifact.get("receipt_contract", [])) >= 8, errors, "receipt_contract")
    require(len(exact_cases) == 3, errors, "exact_case_count")
    require(all(row.get("exact_invariant_for_all_steps_by_induction") is True for row in exact_cases), errors, "exact_identity")
    require(all(h.get("status") == "MATCH" for row in exact_cases for h in row.get("float_horizons", [])), errors, "float_horizons")
    require(experiment.get("negative_fixture", {}).get("status") == "MATCH", errors, "negative_fixture")
    require(experiment.get("promoted_law_status") == "NOT_PROMOTED", errors, "not_promoted")
    require(artifact.get("unsupported_claim_count") == 0, errors, "unsupported_claim_count")
    require(artifact.get("current_promoted_natural_laws") == [], errors, "natural_laws")
    require(all(row.get("status") == "MATCH" for row in artifact.get("flagship_receipts", {}).values()), errors, "flagships")

    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0122ScientificRuntimeLayerValidatorRun/v1",
        "pass": "0122",
        "status": status,
        "checks": [{"artifact": "ScientificRuntimeReceiptLayerSpec", "errors": errors, "status": status, "source_count": len(sources), "exact_case_count": len(exact_cases)}],
    }


def main() -> None:
    result = validate()
    write_json(RESULT, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
