#!/usr/bin/env python3
"""Validate pass 0010 BuildLang scientific runtime receipt fixtures."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

SCHEMA_PATH = ROOT / "schemas" / "buildlang-scientific-runtime-receipt-schema-pass-0010.json"
RECEIPTS_PATH = ROOT / "schemas" / "buildlang-scientific-runtime-receipts-pass-0010.json"

REQUIRED_RECEIPT_FIELDS = [
    "receipt_id",
    "schema",
    "role",
    "claim_id",
    "domain",
    "source_state",
    "build_state",
    "runtime_state",
    "problem_state",
    "measurement_state",
    "invariant_checks",
    "negative_fixture",
    "verification_verdicts",
    "failure_labels",
    "promotion_state",
    "receipt_status",
]

REQUIRED_SUBFIELDS = {
    "source_state": ["workspace", "head", "source_files", "source_refs", "source_hash"],
    "build_state": ["compiler", "compiler_status", "target", "flags", "dependencies", "build_hash"],
    "runtime_state": ["runtime", "os", "hardware", "seed", "environment_hash"],
    "problem_state": ["equation", "domain", "boundary_conditions", "discretization"],
    "measurement_state": ["metric", "observed", "threshold", "units"],
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def check_schema() -> dict[str, Any]:
    errors: list[str] = []
    data = load_json(SCHEMA_PATH)
    if data.get("schema") != "BuildScientificRuntimeReceiptSchema/v1":
        errors.append("schema identifier must be BuildScientificRuntimeReceiptSchema/v1")

    required = data.get("required_receipt_fields", [])
    for field in REQUIRED_RECEIPT_FIELDS:
        if field not in required:
            errors.append(f"schema missing required receipt field {field}")

    status_values = set(data.get("status_values", []))
    for status in ["PASS", "FAIL_EXPECTED", "FAIL_UNEXPECTED", "UNVERIFIABLE"]:
        if status not in status_values:
            errors.append(f"schema missing status value {status}")

    layers = {layer.get("layer") for layer in data.get("verification_layers", [])}
    for layer in ["source", "build", "runtime", "problem", "measurement", "invariant", "external_verdict"]:
        if layer not in layers:
            errors.append(f"schema missing verification layer {layer}")

    return {
        "artifact": "BuildScientificRuntimeReceiptSchema",
        "path": str(SCHEMA_PATH.relative_to(ROOT)),
        "status": "MATCH" if not errors else "DRIFT",
        "required_count": len(required),
        "errors": errors,
    }


def check_receipt(receipt: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    rid = receipt.get("receipt_id", "<missing>")
    for field in REQUIRED_RECEIPT_FIELDS:
        if field not in receipt:
            errors.append(f"{rid} missing {field}")

    for field, subfields in REQUIRED_SUBFIELDS.items():
        value = receipt.get(field)
        if not isinstance(value, dict):
            errors.append(f"{rid} {field} must be object")
            continue
        for subfield in subfields:
            if subfield not in value:
                errors.append(f"{rid} {field} missing {subfield}")

    if receipt.get("schema") != "BuildScientificRuntimeReceipt/v1":
        errors.append(f"{rid} schema must be BuildScientificRuntimeReceipt/v1")
    if receipt.get("promotion_state") == "PROMOTED_LAW":
        errors.append(f"{rid} must not promote a natural law")
    if not receipt.get("invariant_checks"):
        errors.append(f"{rid} must include at least one invariant check")
    if not receipt.get("verification_verdicts"):
        errors.append(f"{rid} must include at least one verification verdict")
    if not receipt.get("failure_labels"):
        errors.append(f"{rid} must include failure labels")

    return errors


def check_receipts() -> dict[str, Any]:
    data = load_json(RECEIPTS_PATH)
    errors: list[str] = []
    if data.get("schema") != "BuildScientificRuntimeReceiptSet/v1":
        errors.append("receipt set schema must be BuildScientificRuntimeReceiptSet/v1")

    receipts = data.get("receipts", [])
    if len(receipts) < 2:
        errors.append("receipt set must contain at least two receipts")

    roles = {receipt.get("role") for receipt in receipts}
    if "primary_positive" not in roles:
        errors.append("receipt set missing primary_positive role")
    if "negative_fixture" not in roles:
        errors.append("receipt set missing negative_fixture role")

    statuses = {receipt.get("receipt_status") for receipt in receipts}
    if "PASS" not in statuses:
        errors.append("receipt set missing PASS receipt")
    if "FAIL_EXPECTED" not in statuses:
        errors.append("receipt set missing FAIL_EXPECTED receipt")

    for receipt in receipts:
        errors.extend(check_receipt(receipt))
        if receipt.get("negative_fixture") and receipt.get("receipt_status") != "FAIL_EXPECTED":
            errors.append(f"{receipt.get('receipt_id')} negative fixture must be FAIL_EXPECTED")
        if receipt.get("role") == "primary_positive" and receipt.get("receipt_status") != "PASS":
            errors.append(f"{receipt.get('receipt_id')} primary positive receipt must be PASS")

    return {
        "artifact": "BuildScientificRuntimeReceiptSet",
        "path": str(RECEIPTS_PATH.relative_to(ROOT)),
        "status": "MATCH" if not errors else "DRIFT",
        "receipt_count": len(receipts),
        "roles": sorted(role for role in roles if role),
        "statuses": sorted(status for status in statuses if status),
        "errors": errors,
    }


def main() -> int:
    checks = [check_schema(), check_receipts()]
    drift = sum(1 for check in checks if check["status"] != "MATCH")
    result = {
        "schema": "Pass0010ScientificRuntimeReceiptValidatorRun/v1",
        "pass": "0010",
        "status": "MATCH" if drift == 0 else "DRIFT",
        "match": len(checks) - drift,
        "drift": drift,
        "checks": checks,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if drift == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
