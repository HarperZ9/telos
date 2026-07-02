"""Validate pass 0026 redaction-boundary receipts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "redaction-boundary-pass-0026.json"
SOURCE_PATH = ROOT / "schemas" / "action-receipt-persistence-replay-pass-0025.json"


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_obj(value: object) -> str:
    return sha256_text(canonical_json(value))


def require(condition: bool, errors: list[str], message: str) -> None:
    if not condition:
        errors.append(message)


def raw_payload_fixture() -> str:
    return "TELOS_DOGFOOD_SECRET_" + sha256_text("pass-0026-redaction-boundary-raw-payload")


def main() -> int:
    data = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    source = json.loads(SOURCE_PATH.read_text(encoding="utf-8"))
    raw_payload = raw_payload_fixture()
    raw_digest = sha256_text(raw_payload)
    errors: list[str] = []

    require(data.get("schema") == "RedactionBoundaryFixtureSet/v1", errors, "wrong schema")
    require(data.get("pass") == "0026", errors, "wrong pass")
    require(data.get("status") == "REDACTION_BOUNDARY_MATCH", errors, "wrong status")
    expected_seal = sha256_obj({key: value for key, value in data.items() if key != "seal"})
    require(data.get("seal") == expected_seal, errors, "seal mismatch")
    require("temp-private raw payload" in data.get("non_promotion_statement", ""), errors, "missing non-promotion")

    source_receipt = data.get("source_receipt", {})
    require(source_receipt.get("path") == "schemas/action-receipt-persistence-replay-pass-0025.json", errors, "wrong source path")
    require(source_receipt.get("sha256") == sha256_file(SOURCE_PATH), errors, "source sha mismatch")
    require(source_receipt.get("seal") == source.get("seal"), errors, "source seal mismatch")
    require(source_receipt.get("ledger_head_hash") == source.get("ledger", {}).get("ledger_head_hash"), errors, "source ledger head mismatch")

    raw = data.get("raw_payload", {})
    require(raw.get("storage_boundary") == "TEMP_PRIVATE_NOT_COMMITTED", errors, "wrong raw storage boundary")
    require(raw.get("sha256") == raw_digest, errors, "raw digest mismatch")
    require(raw.get("length") == len(raw_payload), errors, "raw length mismatch")
    require(raw.get("value_in_receipts") is False, errors, "raw value allowed in receipts")
    require(raw.get("value_in_model_facing_artifacts") is False, errors, "raw value allowed in model artifacts")

    redacted_refs = data.get("redacted_refs", [])
    require(data.get("redacted_ref_count") == len(redacted_refs), errors, "redacted ref count mismatch")
    require(len(redacted_refs) == 2, errors, "expected two redacted refs")
    for ref in redacted_refs:
        path = ROOT / ref.get("path", "")
        require(path.exists(), errors, f"missing redacted ref {ref.get('path')}")
        if path.exists():
            text = path.read_text(encoding="utf-8")
            require(ref.get("sha256") == sha256_file(path), errors, f"redacted ref sha mismatch {ref.get('path')}")
            require(raw_payload not in text, errors, f"raw payload leaked into {ref.get('path')}")
            require(raw_digest[:16] in text or raw_digest in text, errors, f"digest ref missing in {ref.get('path')}")
            require(ref.get("contains_raw_payload") is False, errors, f"ref marks raw payload present {ref.get('path')}")
            require(ref.get("contains_digest_ref") is True, errors, f"ref marks digest absent {ref.get('path')}")

    action = data.get("action_receipt_redaction", {})
    require(action.get("schema") == "ActionReceiptRedactionRef/v1", errors, "wrong action redaction schema")
    require(action.get("redacted_before_ref") == "artifact:fixtures/redacted-before-pass-0026.json", errors, "wrong before ref")
    require(action.get("redacted_after_ref") == "artifact:fixtures/redacted-after-pass-0026.json", errors, "wrong after ref")
    require(action.get("raw_payload_digest") == f"sha256:{raw_digest}", errors, "action raw digest mismatch")
    require(action.get("raw_payload_required_for_model") is False, errors, "raw payload required for model")
    require(action.get("verification", {}).get("verdict") == "MATCH", errors, "redaction verdict mismatch")

    leak_scan = data.get("leak_scan", {})
    targets = leak_scan.get("scan_targets", [])
    require(leak_scan.get("raw_payload_absent_required") is True, errors, "leak scan not required")
    require(leak_scan.get("scan_target_count") == len(targets), errors, "scan target count mismatch")
    required_targets = {
        "schemas/redaction-boundary-pass-0026.json",
        "fixtures/redacted-before-pass-0026.json",
        "fixtures/redacted-after-pass-0026.json",
        "packets/036-redaction-boundary.md",
        "adversarial/pass-0026-redaction-boundary-steelman.md",
        "schemas/tool-receipts-pass-0026.json",
        "crucible/pass-0026-thesis.json",
        "crucible/pass-0026-measurements.json",
    }
    require(required_targets.issubset(set(targets)), errors, "missing leak scan target")

    scanned = []
    for target in targets:
        path = ROOT / target
        require(path.exists(), errors, f"scan target missing {target}")
        if path.exists():
            text = path.read_text(encoding="utf-8")
            require(raw_payload not in text, errors, f"raw payload leaked into {target}")
            scanned.append(target)

    negatives = data.get("negative_fixtures", [])
    require(data.get("negative_fixture_count") == len(negatives), errors, "negative count mismatch")
    require(len(negatives) >= 8, errors, "expected at least eight negatives")
    require(all(n.get("expected_validator_status") == "REJECT" for n in negatives), errors, "negative not rejected")

    result = {
        "schema": "Pass0026RedactionBoundaryValidatorRun/v1",
        "pass": "0026",
        "status": "MATCH" if not errors else "DRIFT",
        "match": 1 if not errors else 0,
        "drift": 0 if not errors else 1,
        "checks": [
            {
                "artifact": "RedactionBoundaryFixtureSet",
                "path": str(SCHEMA_PATH.relative_to(ROOT)),
                "status": "MATCH" if not errors else "DRIFT",
                "raw_payload_sha256": raw_digest,
                "redacted_ref_count": len(redacted_refs),
                "negative_fixture_count": len(negatives),
                "scan_target_count": len(scanned),
                "raw_payload_leak_count": 0 if not errors else None,
                "errors": errors,
            }
        ],
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
