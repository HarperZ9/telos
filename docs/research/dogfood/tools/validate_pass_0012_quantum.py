#!/usr/bin/env python3
"""Validate pass 0012 quantum proof and market artifacts."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROBE_PATH = ROOT / "schemas" / "no-cloning-probe-pass-0012.json"
MARKET_PATH = ROOT / "schemas" / "quantum-computing-market-map-pass-0012.json"
PACKET_PATH = ROOT / "schemas" / "no-cloning-proof-packet-pass-0012.json"

REQUIRED_MARKET_FIELDS = [
    "category",
    "tool",
    "buyer",
    "source_url",
    "official_positioning",
    "capabilities",
    "proof_receipt_gap",
    "telos_wedge_hypothesis",
    "gap_status",
    "confidence",
]

REQUIRED_CATEGORIES = {
    "quantum-sdk",
    "cloud-platform",
    "hardware-platform",
    "quantum-ai",
    "quantum-compiler",
    "neutral-atom",
    "annealing",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def check_probe() -> dict[str, Any]:
    data = load_json(PROBE_PATH)
    errors: list[str] = []
    if data.get("schema") != "NoCloningProbe/v1":
        errors.append("schema must be NoCloningProbe/v1")
    if data.get("status") != "PROBE_MATCH":
        errors.append("probe status must be PROBE_MATCH")

    basis = data.get("basis_cloner_fixture", {})
    checks = basis.get("basis_checks", [])
    if len(checks) != 2:
        errors.append("basis fixture must include two basis checks")
    for check in checks:
        if check.get("status") != "PASS":
            errors.append(f"basis check {check.get('input')} must PASS")
        if abs(float(check.get("fidelity", 0.0)) - 1.0) > 1e-12:
            errors.append(f"basis check {check.get('input')} fidelity must be 1")

    negative = data.get("superposition_negative_fixture", {})
    if negative.get("status") != "FAILS_SUPERPOSITION":
        errors.append("superposition negative fixture must fail")
    if float(negative.get("fidelity_to_desired_clone", 1.0)) >= 0.999:
        errors.append("superposition fidelity should be below clone threshold")

    impossible = data.get("inner_product_impossibility", {})
    if impossible.get("status") != "IMPOSSIBLE_FOR_NONORTHOGONAL_DISTINCT_STATES":
        errors.append("inner-product impossibility status invalid")
    if float(impossible.get("defect", 0.0)) <= 0.0:
        errors.append("inner-product defect must be positive")
    if "seal" not in data:
        errors.append("probe missing seal")

    return {
        "artifact": "NoCloningProbe",
        "path": str(PROBE_PATH.relative_to(ROOT)),
        "status": "MATCH" if not errors else "DRIFT",
        "errors": errors,
    }


def check_market() -> dict[str, Any]:
    data = load_json(MARKET_PATH)
    errors: list[str] = []
    rows = data.get("rows", [])
    if data.get("schema") != "QuantumComputingMarketMap/v1":
        errors.append("schema must be QuantumComputingMarketMap/v1")
    if len(rows) < 12:
        errors.append("market map must include at least 12 rows")

    categories = {row.get("category") for row in rows}
    missing = REQUIRED_CATEGORIES - categories
    if missing:
        errors.append(f"missing categories: {sorted(missing)}")

    for idx, row in enumerate(rows):
        for field in REQUIRED_MARKET_FIELDS:
            if field not in row:
                errors.append(f"row {idx} missing {field}")
        if row.get("source_url") and not str(row["source_url"]).startswith("https://"):
            errors.append(f"row {idx} source_url must be https")
        if row.get("gap_status") not in {"verified", "inferred", "unverified"}:
            errors.append(f"row {idx} invalid gap_status")

    return {
        "artifact": "QuantumComputingMarketMap",
        "path": str(MARKET_PATH.relative_to(ROOT)),
        "status": "MATCH" if not errors else "DRIFT",
        "count": len(rows),
        "categories": sorted(category for category in categories if category),
        "errors": errors,
    }


def check_packet() -> dict[str, Any]:
    data = load_json(PACKET_PATH)
    errors: list[str] = []
    if data.get("schema") != "ProofPacket/v1":
        errors.append("packet schema must be ProofPacket/v1")
    if data.get("packet_id") != "proof-packet-pass-0012-no-cloning":
        errors.append("unexpected packet_id")
    claim_set = data.get("claim_set", [])
    if len(claim_set) < 3:
        errors.append("packet must include at least three claims")
    if any(claim.get("promotion_state") == "PROMOTED_LAW" for claim in claim_set):
        errors.append("packet must not promote a law")
    labels = {item.get("label") for item in data.get("failure_labels", []) if isinstance(item, dict)}
    if "NOT_A_NEW_THEOREM" not in labels:
        errors.append("packet must include NOT_A_NEW_THEOREM failure label")
    if "NO_QUANTUM_HARDWARE_RUN" not in labels:
        errors.append("packet must include NO_QUANTUM_HARDWARE_RUN failure label")

    return {
        "artifact": "NoCloningProofPacket",
        "path": str(PACKET_PATH.relative_to(ROOT)),
        "status": "MATCH" if not errors else "DRIFT",
        "claim_count": len(claim_set),
        "errors": errors,
    }


def main() -> int:
    checks = [check_probe(), check_market(), check_packet()]
    drift = sum(1 for check in checks if check["status"] != "MATCH")
    result = {
        "schema": "Pass0012QuantumValidatorRun/v1",
        "pass": "0012",
        "status": "MATCH" if drift == 0 else "DRIFT",
        "match": len(checks) - drift,
        "drift": drift,
        "checks": checks,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if drift == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
