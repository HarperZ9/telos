#!/usr/bin/env python3
"""Validate pass 0013 quantum experiment receipt artifacts."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RECEIPTS_PATH = ROOT / "schemas" / "quantum-experiment-receipts-pass-0013.json"
SCHEMA_PATH = ROOT / "schemas" / "quantum-experiment-receipt-schema-pass-0013.json"

REQUIRED_RECEIPT_FIELDS = [
    "receipt_id",
    "schema",
    "branch",
    "hardware_claim_allowed",
    "theorem_claim_ref",
    "circuit",
    "backend",
    "resource_estimate",
    "result",
    "verdict",
]

REQUIRED_BRANCHES = {"EXACT_SIMULATOR", "NOISY_SIMULATOR"}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def check_schema() -> dict[str, Any]:
    data = load_json(SCHEMA_PATH)
    errors: list[str] = []
    if data.get("schema") != "QuantumExperimentReceiptSchema/v1":
        errors.append("schema must be QuantumExperimentReceiptSchema/v1")
    required = data.get("required_receipt_fields", [])
    for field in REQUIRED_RECEIPT_FIELDS:
        if field not in required:
            errors.append(f"schema missing {field}")
    branches = set(data.get("branch_values", []))
    for branch in ["EXACT_SIMULATOR", "NOISY_SIMULATOR", "HARDWARE_MOCK", "CLOUD_HARDWARE"]:
        if branch not in branches:
            errors.append(f"schema missing branch {branch}")
    if not data.get("branch_promotion_forbidden", False):
        errors.append("schema must forbid branch promotion")
    return {
        "artifact": "QuantumExperimentReceiptSchema",
        "path": str(SCHEMA_PATH.relative_to(ROOT)),
        "status": "MATCH" if not errors else "DRIFT",
        "errors": errors,
    }


def check_receipts() -> dict[str, Any]:
    data = load_json(RECEIPTS_PATH)
    errors: list[str] = []
    if data.get("schema") != "QuantumExperimentReceiptSet/v1":
        errors.append("receipt set schema must be QuantumExperimentReceiptSet/v1")
    if data.get("status") != "RECEIPT_SET_MATCH":
        errors.append("receipt set status must be RECEIPT_SET_MATCH")
    receipts = data.get("receipts", [])
    if len(receipts) < 2:
        errors.append("receipt set must contain at least two receipts")
    branches = {receipt.get("branch") for receipt in receipts}
    missing = REQUIRED_BRANCHES - branches
    if missing:
        errors.append(f"missing branches: {sorted(missing)}")
    for receipt in receipts:
        rid = receipt.get("receipt_id", "<missing>")
        for field in REQUIRED_RECEIPT_FIELDS:
            if field not in receipt:
                errors.append(f"{rid} missing {field}")
        if receipt.get("schema") != "QuantumExperimentReceipt/v1":
            errors.append(f"{rid} schema must be QuantumExperimentReceipt/v1")
        if receipt.get("hardware_claim_allowed") is not False:
            errors.append(f"{rid} hardware_claim_allowed must be false")
        for nested in ["circuit", "backend", "resource_estimate", "result"]:
            if not isinstance(receipt.get(nested), dict):
                errors.append(f"{rid} {nested} must be object")
    exact = next((receipt for receipt in receipts if receipt.get("branch") == "EXACT_SIMULATOR"), {})
    noisy = next((receipt for receipt in receipts if receipt.get("branch") == "NOISY_SIMULATOR"), {})
    if exact:
        fidelity = float(exact.get("result", {}).get("fidelity_to_desired_clone", 1.0))
        if abs(fidelity - 0.5) > 1e-12:
            errors.append("exact simulator fidelity must be 0.5 for |+> no-cloning fixture")
    if noisy:
        result = noisy.get("result", {})
        if result.get("status") != "NOISY_BRANCH_NOT_THEOREM_PROOF":
            errors.append("noisy branch must be labeled not theorem proof")
        if float(result.get("histogram_l1_drift_from_exact", 1.0)) != 0.0:
            errors.append("histogram drift should be zero for phase-flip warning fixture")
        if float(result.get("fidelity_to_desired_clone", 1.0)) >= 0.5:
            errors.append("noisy branch fidelity should be below exact fixture fidelity")
    branch_state = data.get("branch_separation", {})
    if branch_state.get("status") != "BRANCH_SEPARATION_MATCH":
        errors.append("branch separation status must match")
    if "seal" not in data:
        errors.append("receipt set missing seal")
    return {
        "artifact": "QuantumExperimentReceiptSet",
        "path": str(RECEIPTS_PATH.relative_to(ROOT)),
        "status": "MATCH" if not errors else "DRIFT",
        "receipt_count": len(receipts),
        "branches": sorted(branch for branch in branches if branch),
        "errors": errors,
    }


def main() -> int:
    checks = [check_schema(), check_receipts()]
    drift = sum(1 for check in checks if check["status"] != "MATCH")
    result = {
        "schema": "Pass0013QuantumExperimentValidatorRun/v1",
        "pass": "0013",
        "status": "MATCH" if drift == 0 else "DRIFT",
        "match": len(checks) - drift,
        "drift": drift,
        "checks": checks,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if drift == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
