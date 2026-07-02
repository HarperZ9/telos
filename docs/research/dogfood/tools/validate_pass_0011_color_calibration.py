#!/usr/bin/env python3
"""Validate pass 0011 color calibration proof-kit artifacts."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MARKET_PATH = ROOT / "schemas" / "color-calibration-market-map-pass-0011.json"
KIT_PATH = ROOT / "schemas" / "build-color-calibration-proof-kit-pass-0011.json"

REQUIRED_MARKET_FIELDS = [
    "category",
    "tool",
    "buyer",
    "source_url",
    "official_positioning",
    "capabilities",
    "proof_receipt_gap",
    "build_color_wedge_hypothesis",
    "gap_status",
    "confidence",
]

REQUIRED_CATEGORIES = {
    "color-standard",
    "color-management",
    "calibration-software",
    "grading-tool",
    "open-source-calibration",
    "profile-standard",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def check_market() -> dict[str, Any]:
    data = load_json(MARKET_PATH)
    errors: list[str] = []
    rows = data.get("rows", [])
    if data.get("schema") != "ColorCalibrationMarketMap/v1":
        errors.append("schema must be ColorCalibrationMarketMap/v1")
    if len(rows) < 8:
        errors.append("market map must contain at least 8 rows")

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
        "artifact": "ColorCalibrationMarketMap",
        "path": str(MARKET_PATH.relative_to(ROOT)),
        "status": "MATCH" if not errors else "DRIFT",
        "count": len(rows),
        "categories": sorted(category for category in categories if category),
        "errors": errors,
    }


def check_kit() -> dict[str, Any]:
    data = load_json(KIT_PATH)
    errors: list[str] = []
    if data.get("schema") != "BuildColorCalibrationProofKit/v1":
        errors.append("schema must be BuildColorCalibrationProofKit/v1")
    if data.get("status") != "PROOF_KIT_MATCH":
        errors.append("proof kit status must be PROOF_KIT_MATCH")

    metrics = data.get("metrics", [])
    if len(metrics) < 4:
        errors.append("proof kit must include at least 4 metrics")
    for metric in metrics:
        observed = metric.get("observed")
        threshold = metric.get("threshold")
        if metric.get("status") != "PASS":
            errors.append(f"{metric.get('metric')} metric must pass")
        if isinstance(observed, (int, float)) and isinstance(threshold, (int, float)):
            if observed > threshold:
                errors.append(f"{metric.get('metric')} observed value exceeds threshold")
        else:
            errors.append(f"{metric.get('metric')} observed and threshold must be numeric")

    boundary = data.get("calibration_boundary", {})
    for field in [
        "hardware_measurement_used",
        "display_state_mutated",
        "icc_profile_installed",
        "lut_written",
        "physical_calibration_claim",
    ]:
        if boundary.get(field) is not False:
            errors.append(f"boundary {field} must be false")
    if data.get("negative_fixture", {}).get("status") != "REJECTED_BY_BOUNDARY":
        errors.append("negative fixture must be rejected by boundary")
    if data.get("promotion_state") == "PROMOTED_LAW":
        errors.append("proof kit must not promote a natural law")

    return {
        "artifact": "BuildColorCalibrationProofKit",
        "path": str(KIT_PATH.relative_to(ROOT)),
        "status": "MATCH" if not errors else "DRIFT",
        "metric_count": len(metrics),
        "errors": errors,
    }


def main() -> int:
    checks = [check_market(), check_kit()]
    drift = sum(1 for check in checks if check["status"] != "MATCH")
    result = {
        "schema": "Pass0011ColorCalibrationValidatorRun/v1",
        "pass": "0011",
        "status": "MATCH" if drift == 0 else "DRIFT",
        "match": len(checks) - drift,
        "drift": drift,
        "checks": checks,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if drift == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
