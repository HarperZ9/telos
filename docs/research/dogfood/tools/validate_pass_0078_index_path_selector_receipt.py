"""Validate pass 0078 Index path-selector receipt fixture."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "index-path-selector-receipt-pass-0078.json"
RESULT = ROOT / "schemas" / "pass-0078-index-path-selector-receipt-validator-result.json"


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
    results = {row["selector"]: row for row in artifact.get("selector_results", [])}
    if artifact.get("schema") != "IndexPathSelectorReceipt/v1":
        errors.append("schema")
    if artifact.get("status") != "INDEX_PATH_SELECTOR_RECEIPT_FIXTURE_MATCH":
        errors.append("status")
    if seal != sha256_obj(unsealed):
        errors.append("seal")
    if results.get("buildlang", {}).get("status") != "MATCH":
        errors.append("buildlang")
    if results.get("compiler", {}).get("status") != "MATCH":
        errors.append("compiler")
    if results.get("build-universe", {}).get("status") != "REJECT":
        errors.append("build_universe")
    if artifact.get("source_ref_count", 0) < 2:
        errors.append("source_ref_count")
    if artifact.get("raw_source_included") is not False or artifact.get("source_refs_only") is not True:
        errors.append("privacy")
    if "target" not in artifact.get("excluded_dirs", []):
        errors.append("target_exclusion")
    if artifact.get("unsupported_claim_count") != 0:
        errors.append("unsupported_claim_count")
    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0078IndexPathSelectorReceiptValidatorRun/v1",
        "pass": "0078",
        "status": status,
        "match": 1 if status == "MATCH" else 0,
        "drift": 0 if status == "MATCH" else 1,
        "checks": [{
            "artifact": "IndexPathSelectorReceipt",
            "errors": errors,
            "path": "schemas/index-path-selector-receipt-pass-0078.json",
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
