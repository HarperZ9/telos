"""Validate pass 0141 SAIR Foundation source-refresh artifact."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "sair-foundation-refresh-pass-0141.json"


def check(name: str, ok: bool) -> dict[str, str]:
    return {"name": name, "status": "MATCH" if ok else "DRIFT"}


def main() -> int:
    artifact = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    checks = [
        check("schema", artifact.get("schema") == "SAIRFoundationRefreshReceipt/v1"),
        check("status", artifact.get("status") == "SAIR_FOUNDATION_REFRESH_MATCH"),
        check("gather_items", artifact["gather_summary"]["items"] >= 11),
        check("verified_items", artifact["gather_summary"]["verified_items"] >= 6),
        check("empty_captures_fenced", artifact["gather_summary"]["empty_captures"] >= 1),
        check("channel_leads", len(artifact["channel_leads"]) == 12),
        check("updated_tool_floor", len(artifact["updated_tool_floor"]) == 6),
        check("updated_tool_experiments", len(artifact["updated_tool_experiments"]) == 6),
        check("megatool_routes", len(artifact["megatool_routes"]) == 6),
        check("experiments", len(artifact["experiments"]) == 8),
        check("negative_fixtures", len(artifact["negative_fixtures"]) == 8),
        check("no_promoted_theorems", artifact["current_promoted_theorems"] == []),
        check("no_promoted_laws", artifact["current_promoted_natural_laws"] == []),
        check("seal_present", len(artifact.get("seal", "")) == 64),
    ]
    failures = [row for row in checks if row["status"] != "MATCH"]
    result = {
        "schema": "Pass0141SAIRFoundationRefreshValidatorRun/v1",
        "pass": "0141",
        "status": "MATCH" if not failures else "DRIFT",
        "checks": checks,
        "failures": failures,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
