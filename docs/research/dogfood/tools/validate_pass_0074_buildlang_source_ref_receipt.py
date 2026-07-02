"""Validate pass 0074 BuildLang source-ref receipt."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "buildlang-source-ref-receipt-pass-0074.json"
RESULT = ROOT / "schemas" / "pass-0074-buildlang-source-ref-receipt-validator-result.json"


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
    if artifact.get("schema") != "BuildLangSourceRefReceipt/v1":
        errors.append("schema")
    if artifact.get("status") != "BUILDLANG_SOURCE_REF_RECEIPT_MATCH":
        errors.append("status")
    if seal != sha256_obj(unsealed):
        errors.append("seal")
    if artifact.get("source_ref_count") != len(artifact.get("source_refs", [])):
        errors.append("source_ref_count")
    if not all(ref.get("exists") and ref.get("sha256") for ref in artifact.get("source_refs", [])):
        errors.append("source_refs")
    if artifact.get("corpus_verify", {}).get("status") != "MATCH":
        errors.append("corpus_verify")
    if artifact.get("program_count") != 8:
        errors.append("program_count")
    if artifact.get("production_backend_claim") != "C backend only":
        errors.append("backend_scope")
    if artifact.get("unsupported_claim_count") != 0:
        errors.append("unsupported_claim_count")
    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0074BuildLangSourceRefReceiptValidatorRun/v1",
        "pass": "0074",
        "status": status,
        "match": 1 if status == "MATCH" else 0,
        "drift": 0 if status == "MATCH" else 1,
        "checks": [{
            "artifact": "BuildLangSourceRefReceipt",
            "errors": errors,
            "path": "schemas/buildlang-source-ref-receipt-pass-0074.json",
            "source_ref_count": artifact.get("source_ref_count"),
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
