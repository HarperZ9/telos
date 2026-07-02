"""Validate pass 0148 live source router probe artifact."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "live-source-router-probes-pass-0148.json"


def check(name: str, ok: bool) -> dict[str, str]:
    return {"name": name, "status": "MATCH" if ok else "DRIFT"}


def main() -> int:
    artifact = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    rows = {row["id"]: row for row in artifact["routes"]}
    checks = [
        check("schema", artifact["schema"] == "LiveSourceRouterProbeReceipt/v1"),
        check("status", artifact["status"] == "LIVE_SOURCE_ROUTER_PROBES_MATCH_WITH_WARNINGS"),
        check("routes", artifact["summary"]["routes"] == 25),
        check("families", artifact["summary"]["families"] >= 7),
        check("live_matches", artifact["summary"]["live_query_matches"] >= 17),
        check("fallback_matches", artifact["summary"]["fallback_matches"] >= 4),
        check("source_lead_only", artifact["summary"]["source_lead_only"] == 2),
        check("negative_fixtures", artifact["summary"]["negative_fixtures"] == 10),
        check("base_policy", rows["base_oai"]["warning"] == "HTTP_403_RESTRICTED_INTERFACE"),
        check("openalex_policy", rows["openalex_works"]["warning"] == "HTTP_503_RETRYABLE"),
        check("semantic_policy", rows["semantic_scholar_search"]["warning"] == "HTTP_429_RETRYABLE"),
        check("cambridge_policy", rows["cambridge_apollo_oai"]["warning"] == "HTTP_404_ENDPOINT_ALIAS_REQUIRED"),
        check("tool_receipts", len(artifact["tool_receipts"]) == 5 and all(row["status"] == "MATCH" for row in artifact["tool_receipts"].values())),
        check("no_theorems", artifact["current_promoted_theorems"] == []),
        check("no_laws", artifact["current_promoted_natural_laws"] == []),
        check("seal_present", len(artifact.get("seal", "")) == 64),
    ]
    failures = [row for row in checks if row["status"] != "MATCH"]
    print(json.dumps({"schema": "Pass0148LiveSourceRouterProbeValidatorRun/v1", "pass": "0148", "status": "MATCH" if not failures else "DRIFT", "checks": checks, "failures": failures}, indent=2, sort_keys=True))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
