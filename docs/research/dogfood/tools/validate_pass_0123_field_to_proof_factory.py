"""Validate pass 0123 field-to-proof packet factory."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "field-to-proof-packet-factory-pass-0123.json"
RESULT = ROOT / "schemas" / "pass-0123-field-to-proof-factory-validator-result.json"


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
    factories = artifact.get("field_factories", [])
    experiment = artifact.get("coverage_experiment", {})
    errors: list[str] = []

    require(artifact.get("schema") == "FieldToProofPacketFactorySpec/v1", errors, "schema")
    require(artifact.get("status") == "FIELD_TO_PROOF_PACKET_FACTORY_MATCH", errors, "status")
    require(seal == sha256_obj(unsealed), errors, "seal")
    require(artifact.get("source_bindings", {}).get("youtube_growth_pass") == "0121", errors, "youtube_binding")
    require(artifact.get("source_bindings", {}).get("runtime_layer_pass") == "0122", errors, "runtime_binding")
    require(len(sources) >= 16, errors, "source_count")
    require(sum(row.get("chars", 0) >= 500 for row in sources) >= 14, errors, "substantial_sources")
    require(all(row.get("gap_status") == "inferred" for row in sources), errors, "source_gap_status")
    require(len(factories) >= 6, errors, "factory_count")
    require(all(row.get("claim_status") == "HYPOTHESIS" for row in factories), errors, "factory_claim_status")
    require(all(row.get("gap_status") == "inferred" for row in factories), errors, "factory_gap_status")
    require(experiment.get("status") == "MATCH", errors, "coverage_experiment")
    require(experiment.get("negative_fixture", {}).get("status") == "REJECTED", errors, "negative_fixture")
    require(artifact.get("uniqueness_claim_status") == "HYPOTHESIS_ONLY", errors, "uniqueness_boundary")
    require(artifact.get("unsupported_claim_count") == 0, errors, "unsupported_claim_count")
    require(artifact.get("current_promoted_natural_laws") == [], errors, "natural_laws")
    require(all(row.get("status") == "MATCH" for row in artifact.get("flagship_receipts", {}).values()), errors, "flagships")

    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0123FieldToProofFactoryValidatorRun/v1",
        "pass": "0123",
        "status": status,
        "checks": [{"artifact": "FieldToProofPacketFactorySpec", "errors": errors, "status": status, "source_count": len(sources), "factory_count": len(factories)}],
    }


def main() -> None:
    result = validate()
    write_json(RESULT, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
