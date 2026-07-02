"""Validate pass 0129 Brandom functional-learning digest."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "brandom-functional-learning-digest-pass-0129.json"
RESULT = ROOT / "schemas" / "pass-0129-brandom-functional-learning-validator-result.json"


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
    terms = {row.get("term"): row for row in artifact.get("term_signals", [])}
    negatives = artifact.get("negative_fixtures", [])
    errors: list[str] = []

    require(artifact.get("schema") == "BrandomFunctionalLearningDigestReceipt/v1", errors, "schema")
    require(artifact.get("status") == "BRANDOM_FUNCTIONAL_LEARNING_DIGEST_MATCH", errors, "status")
    require(seal == sha256_obj(unsealed), errors, "seal")
    require(artifact.get("source_bindings", {}).get("proof_suite_pass") == "0128", errors, "proof_suite_binding")
    require(len(sources) >= 7 and all(row.get("status") == "GATHER_VERIFIED" for row in sources), errors, "sources")
    require(any(row.get("kind") == "transcript" for row in sources), errors, "transcript_receipt")
    require(all(row.get("raw_body_exported") is False for row in sources), errors, "raw_body_boundary")
    require(terms.get("Sellars", {}).get("hits", 0) > 0, errors, "sellars_signal")
    require(terms.get("Kant", {}).get("hits", 0) > 0, errors, "kant_signal")
    require(terms.get("Hegel", {}).get("hits", 0) > 0, errors, "hegel_signal")
    require(artifact.get("scorekeeping_fixture", {}).get("status") == "MATCH", errors, "scorekeeping")
    require(len(artifact.get("tool_hypotheses", [])) >= 5, errors, "tool_hypotheses")
    require(len(negatives) >= 5 and all(row.get("status") == "REJECTED" for row in negatives), errors, "negative_fixtures")
    require(artifact.get("current_promoted_natural_laws") == [], errors, "natural_laws")
    require(all(row.get("status") == "MATCH" for row in artifact.get("flagship_receipts", {}).values()), errors, "flagships")

    status = "MATCH" if not errors else "DRIFT"
    return {"schema": "Pass0129BrandomFunctionalLearningValidatorRun/v1", "pass": "0129", "status": status, "checks": [{"artifact": "BrandomFunctionalLearningDigest", "errors": errors, "status": status, "source_count": len(sources), "negative_count": len(negatives)}]}


def main() -> None:
    result = validate()
    write_json(RESULT, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
