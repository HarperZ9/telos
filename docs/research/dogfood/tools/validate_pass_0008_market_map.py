"""Validate pass 0008 AI4Science market-map artifacts."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_market_rows(path: Path) -> dict[str, Any]:
    data = load_json(path)
    rows = data.get("rows", [])
    errors: list[str] = []
    required_fields = [
        "category",
        "tool",
        "buyer",
        "source_url",
        "official_positioning",
        "capabilities",
        "proof_layer_gap",
        "gap_status",
        "telos_wedge_hypothesis",
        "uniqueness_claim_status",
        "confidence",
    ]
    allowed_gap_status = {"verified", "inferred", "unverified"}
    required_categories = {
        "automated-discovery",
        "formal-math",
        "literature-search",
        "lab-platform",
        "workflow-notebook",
    }

    if not isinstance(rows, list):
        errors.append("rows is not a list")
        rows = []

    if len(rows) < 16:
        errors.append(f"rows count {len(rows)} below minimum 16")

    categories = set()
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            errors.append(f"rows[{index}] is not an object")
            continue
        for field in required_fields:
            if field not in row:
                errors.append(f"rows[{index}] missing {field}")
            elif row[field] in (None, "", []):
                errors.append(f"rows[{index}] empty {field}")
        if row.get("gap_status") not in allowed_gap_status:
            errors.append(f"rows[{index}] invalid gap_status")
        if row.get("source_url") and not str(row["source_url"]).startswith("https://"):
            errors.append(f"rows[{index}] source_url is not https")
        if row.get("uniqueness_claim_status") == "fact":
            errors.append(f"rows[{index}] treats uniqueness as fact")
        if row.get("category"):
            categories.add(row["category"])

    missing_categories = sorted(required_categories - categories)
    for category in missing_categories:
        errors.append(f"missing category {category}")

    return {
        "artifact": "Pass0008MarketRows",
        "path": str(path.relative_to(ROOT)),
        "count": len(rows),
        "categories": sorted(categories),
        "required_categories": sorted(required_categories),
        "errors": errors,
        "status": "MATCH" if not errors else "DRIFT",
    }


def validate_wedges(path: Path) -> dict[str, Any]:
    data = load_json(path)
    wedges = data.get("wedges", [])
    errors: list[str] = []
    required_fields = [
        "wedge",
        "buyer",
        "problem",
        "existing_tool_fragments",
        "telos_integration",
        "thirty_day_push",
        "hypothesis_status",
        "score",
    ]

    if not isinstance(wedges, list):
        errors.append("wedges is not a list")
        wedges = []

    if len(wedges) < 5:
        errors.append(f"wedges count {len(wedges)} below minimum 5")

    primary = [wedge for wedge in wedges if isinstance(wedge, dict) and wedge.get("rank") == 1]
    if len(primary) != 1:
        errors.append("expected exactly one rank=1 wedge")

    for index, wedge in enumerate(wedges):
        if not isinstance(wedge, dict):
            errors.append(f"wedges[{index}] is not an object")
            continue
        for field in required_fields:
            if field not in wedge:
                errors.append(f"wedges[{index}] missing {field}")
            elif wedge[field] in (None, "", []):
                errors.append(f"wedges[{index}] empty {field}")
        if wedge.get("hypothesis_status") not in {"hypothesis", "source-backed", "unverified"}:
            errors.append(f"wedges[{index}] invalid hypothesis_status")
        score = wedge.get("score", {})
        if isinstance(score, dict):
            for metric in ["urgency", "budget", "differentiation", "demo_readiness", "strategic_upside"]:
                value = score.get(metric)
                if not isinstance(value, int) or value < 1 or value > 5:
                    errors.append(f"wedges[{index}] invalid score.{metric}")
        else:
            errors.append(f"wedges[{index}] score is not an object")

    return {
        "artifact": "Pass0008Wedges",
        "path": str(path.relative_to(ROOT)),
        "count": len(wedges),
        "errors": errors,
        "status": "MATCH" if not errors else "DRIFT",
    }


def main() -> int:
    checks = [
        validate_market_rows(SCHEMAS / "ai4science-frontier-map-pass-0008.json"),
        validate_wedges(SCHEMAS / "proof-packet-market-wedges-pass-0008.json"),
    ]
    result = {
        "schema": "Pass0008MarketValidatorRun/v1",
        "pass": "0008",
        "status": "MATCH" if all(check["status"] == "MATCH" for check in checks) else "DRIFT",
        "checks": checks,
        "match": sum(1 for check in checks if check["status"] == "MATCH"),
        "drift": sum(1 for check in checks if check["status"] == "DRIFT"),
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "MATCH" else 1


if __name__ == "__main__":
    raise SystemExit(main())
