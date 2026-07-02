"""Validate pass 0092 BuildLang check receipt adapter."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "buildlang-check-receipt-adapter-pass-0092.json"
RESULT = ROOT / "schemas" / "pass-0092-buildlang-check-receipt-adapter-validator-result.json"


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)


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
    receipt = artifact.get("check_receipt", {})
    verify = artifact.get("verify_report", {})
    adapter = artifact.get("crucible_adapter", {})
    boundary = artifact.get("promotion_boundary", {})
    if artifact.get("schema") != "BuildLangCheckReceiptAdapter/v1":
        errors.append("schema")
    if artifact.get("status") != "BUILDLANG_CHECK_RECEIPT_ADAPTER_MATCH":
        errors.append("status")
    if seal != sha256_obj(unsealed):
        errors.append("seal")
    if artifact.get("prior_binding", {}).get("source_pass") != "0091":
        errors.append("prior_binding")
    if artifact.get("check_command", {}).get("exit_code") != 0 or artifact.get("verify_command", {}).get("exit_code") != 0:
        errors.append("commands")
    if receipt.get("schema") != "buildlang-check-receipt/v1" or receipt.get("status") != "passed":
        errors.append("receipt")
    if len(receipt.get("source_digest", {}).get("hex", "")) != 64:
        errors.append("source_digest")
    if receipt.get("policy", {}).get("profile") != "console-only" or receipt.get("policy", {}).get("status") != "passed":
        errors.append("policy")
    if receipt.get("declared_effects", {}).get("main") != ["Console"]:
        errors.append("declared_effects")
    if receipt.get("observed_capabilities", {}).get("main", {}).get("Console") != ["println!"]:
        errors.append("observed_capabilities")
    if verify.get("status") != "passed" or artifact.get("verify_summary", {}).get("all_required_passed") is not True:
        errors.append("verify")
    if adapter.get("measurement_count") != 10 or adapter.get("match") != 10 or adapter.get("drift") != 0:
        errors.append("adapter")
    if any(row.get("status") != "MATCH" for row in adapter.get("measurements", [])):
        errors.append("measurements")
    if any(tool.get("status") != "MATCH" for tool in artifact.get("flagship_receipts", {}).values()):
        errors.append("flagship_receipts")
    if any(boundary.get(key) for key in ["language_replacement_claim", "scientific_discovery_claim", "new_natural_law_claim"]):
        errors.append("promotion_boundary")
    if artifact.get("unsupported_claim_count") != 0 or artifact.get("current_promoted_natural_laws") != []:
        errors.append("unsupported_claims")
    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0092BuildLangCheckReceiptAdapterValidatorRun/v1",
        "pass": "0092",
        "status": status,
        "match": 1 if status == "MATCH" else 0,
        "drift": 0 if status == "MATCH" else 1,
        "checks": [{
            "artifact": "BuildLangCheckReceiptAdapter",
            "errors": errors,
            "path": "schemas/buildlang-check-receipt-adapter-pass-0092.json",
            "receipt_status": receipt.get("status"),
            "verify_status": verify.get("status"),
            "measurement_count": adapter.get("measurement_count"),
            "adapter_match": adapter.get("match"),
            "adapter_drift": adapter.get("drift"),
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
