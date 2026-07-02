"""Validate pass 0009 scientific-compute proof and market artifacts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_probe(path: Path) -> dict[str, Any]:
    data = load_json(path)
    errors: list[str] = []
    if data.get("status") != "PROBE_MATCH":
        errors.append("probe status is not PROBE_MATCH")
    stable = data.get("stable_probe", {})
    unstable = data.get("unstable_probe", {})
    if stable.get("status") != "ENERGY_MONOTONE":
        errors.append("stable probe is not ENERGY_MONOTONE")
    if stable.get("increase_count") != 0:
        errors.append("stable probe has energy increases")
    if unstable.get("status") != "ENERGY_INCREASE_DETECTED":
        errors.append("unstable probe did not detect energy increase")
    if not data.get("seal"):
        errors.append("missing seal")
    return {
        "artifact": "HeatEquationEnergyProbe",
        "path": str(path.relative_to(ROOT)),
        "errors": errors,
        "status": "MATCH" if not errors else "DRIFT",
    }


def validate_market(path: Path) -> dict[str, Any]:
    data = load_json(path)
    rows = data.get("rows", [])
    errors: list[str] = []
    required = [
        "category",
        "tool",
        "buyer",
        "source_url",
        "official_positioning",
        "capabilities",
        "proof_receipt_gap",
        "buildlang_wedge_hypothesis",
        "gap_status",
        "confidence",
    ]
    categories = set()
    if not isinstance(rows, list):
        errors.append("rows is not a list")
        rows = []
    if len(rows) < 10:
        errors.append(f"rows count {len(rows)} below minimum 10")
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            errors.append(f"rows[{index}] is not an object")
            continue
        for field in required:
            if field not in row:
                errors.append(f"rows[{index}] missing {field}")
            elif row[field] in (None, "", []):
                errors.append(f"rows[{index}] empty {field}")
        if row.get("gap_status") not in {"verified", "inferred", "unverified"}:
            errors.append(f"rows[{index}] invalid gap_status")
        if row.get("source_url") and not str(row["source_url"]).startswith("https://"):
            errors.append(f"rows[{index}] source_url is not https")
        if row.get("category"):
            categories.add(row["category"])
    for category in ["language-ecosystem", "pde-framework", "hpc-solver", "physics-ai", "commercial-simulation"]:
        if category not in categories:
            errors.append(f"missing category {category}")
    return {
        "artifact": "ScientificComputeMarketMap",
        "path": str(path.relative_to(ROOT)),
        "count": len(rows),
        "categories": sorted(categories),
        "errors": errors,
        "status": "MATCH" if not errors else "DRIFT",
    }


def main() -> int:
    checks = [
        validate_probe(SCHEMAS / "heat-equation-energy-probe-pass-0009.json"),
        validate_market(SCHEMAS / "scientific-compute-market-map-pass-0009.json"),
    ]
    result = {
        "schema": "Pass0009ScientificComputeValidatorRun/v1",
        "pass": "0009",
        "status": "MATCH" if all(check["status"] == "MATCH" for check in checks) else "DRIFT",
        "checks": checks,
        "match": sum(1 for check in checks if check["status"] == "MATCH"),
        "drift": sum(1 for check in checks if check["status"] == "DRIFT"),
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "MATCH" else 1


if __name__ == "__main__":
    raise SystemExit(main())
