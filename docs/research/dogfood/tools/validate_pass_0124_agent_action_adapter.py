"""Validate pass 0124 agent action proof-packet adapter."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "agent-action-proof-packet-factory-adapter-pass-0124.json"
RESULT = ROOT / "schemas" / "pass-0124-agent-action-adapter-validator-result.json"


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
    receipts = artifact.get("action_receipts", [])
    negatives = artifact.get("negative_fixtures", [])
    required = set(artifact.get("adapter_contract_fields", []))
    errors: list[str] = []

    require(artifact.get("schema") == "AgentActionProofPacketFactoryAdapter/v1", errors, "schema")
    require(artifact.get("status") == "AGENT_ACTION_PROOF_PACKET_FACTORY_ADAPTER_MATCH", errors, "status")
    require(seal == sha256_obj(unsealed), errors, "seal")
    require(artifact.get("source_bindings", {}).get("factory_pass") == "0123", errors, "factory_binding")
    require(artifact.get("source_bindings", {}).get("adapter_matrix_pass") == "0064", errors, "matrix_binding")
    require(len(sources) >= 7, errors, "source_count")
    require(sum(row.get("chars", 0) >= 500 for row in sources) >= 7, errors, "source_chars")
    require(len(receipts) == 5, errors, "receipt_count")
    require(all(required.issubset(receipt) for receipt in receipts), errors, "required_fields")
    require(all(receipt.get("adapter_status") == "MATCH" for receipt in receipts), errors, "adapter_status")
    require(all(receipt.get("verification_verdict") == "MATCH" for receipt in receipts), errors, "verdicts")
    require(all(receipt.get("action_admission", {}).get("decision") == "admit" for receipt in receipts), errors, "admission")
    require(len(negatives) == 4, errors, "negative_count")
    require(all(row.get("status") == "REJECTED" and row.get("failures") for row in negatives), errors, "negative_status")
    require(artifact.get("unsupported_claim_count") == 0, errors, "unsupported_claim_count")
    require(artifact.get("current_promoted_natural_laws") == [], errors, "natural_laws")
    require(all(row.get("status") == "MATCH" for row in artifact.get("flagship_receipts", {}).values()), errors, "flagships")

    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0124AgentActionAdapterValidatorRun/v1",
        "pass": "0124",
        "status": status,
        "checks": [{"artifact": "AgentActionProofPacketFactoryAdapter", "errors": errors, "status": status, "source_count": len(sources), "receipt_count": len(receipts), "negative_count": len(negatives)}],
    }


def main() -> None:
    result = validate()
    write_json(RESULT, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
