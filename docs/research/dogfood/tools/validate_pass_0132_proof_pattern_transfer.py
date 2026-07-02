"""Validate pass 0132 proof pattern transfer."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "proof-pattern-transfer-pass-0132.json"
RESULT = ROOT / "schemas" / "pass-0132-proof-pattern-transfer-validator-result.json"


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
    sources = artifact.get("source_receipts", [])
    positives = artifact.get("positive_fixtures", [])
    counter = artifact.get("counterexample_fixtures", [])
    negatives = artifact.get("negative_fixtures", [])
    law = artifact.get("law_candidate", {})
    errors: list[str] = []

    require(artifact.get("schema") == "ProofPatternTransferReceipt/v1", errors, "schema")
    require(artifact.get("status") == "PROOF_PATTERN_TRANSFER_MATCH", errors, "status")
    require(seal == sha256_obj(unsealed), errors, "seal")
    require(artifact.get("source_bindings", {}).get("tradition_atlas_pass") == "0131", errors, "upstream_binding")
    require(len(sources) >= 6 and all(row.get("status") == "GATHER_VERIFIED" for row in sources), errors, "sources")
    require(all(row.get("raw_body_exported") is False for row in sources), errors, "raw_body_boundary")
    require(len(positives) >= 2 and all(row.get("status") == "MATCH" for row in positives), errors, "positive_fixtures")
    require(abs(positives[0].get("derivative_residual", 1.0)) < 1e-12, errors, "derivative_residual")
    require(positives[0].get("norm_delta", 1.0) < 1e-12, errors, "norm_delta")
    require(len(counter) >= 2 and all(row.get("status") == "REJECTED" for row in counter), errors, "counterexamples")
    require(law.get("status") == "LAW_CANDIDATE" and law.get("promotion_status") == "NOT_PROMOTED", errors, "law_boundary")
    require(len(negatives) >= 6 and all(row.get("status") == "REJECTED" for row in negatives), errors, "negative_fixtures")
    require(artifact.get("current_promoted_natural_laws") == [], errors, "natural_laws")
    require(all(row.get("status") == "MATCH" for row in artifact.get("flagship_receipts", {}).values()), errors, "flagships")

    status = "MATCH" if not errors else "DRIFT"
    return {"schema": "Pass0132ProofPatternTransferValidatorRun/v1", "pass": "0132", "status": status, "checks": [{"artifact": "ProofPatternTransfer", "errors": errors, "status": status, "source_count": len(sources), "positive_count": len(positives), "counterexample_count": len(counter)}]}


def main() -> None:
    result = validate()
    write_json(RESULT, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
