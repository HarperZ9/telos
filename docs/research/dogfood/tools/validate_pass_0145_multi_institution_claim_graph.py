"""Validate pass 0145 multi-institution claim graph artifact."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "multi-institution-claim-graph-pass-0145.json"


def check(name: str, ok: bool) -> dict[str, str]:
    return {"name": name, "status": "MATCH" if ok else "DRIFT"}


def main() -> int:
    artifact = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    institutions = {row["id"]: row for row in artifact["institutions"]}
    tool_receipts = artifact.get("tool_receipts", {})
    checks = [
        check("schema", artifact["schema"] == "MultiInstitutionClaimGraphReceipt/v1"),
        check("status", artifact["status"] == "MULTI_INSTITUTION_CLAIM_GRAPH_MATCH_WITH_WARNINGS"),
        check("institution_count", artifact["summary"]["institutions"] == 4),
        check("stored_captures", artifact["summary"]["stored_captures"] >= 18),
        check("distinct_bodies", artifact["summary"]["distinct_bodies"] >= 18),
        check("identity_matches", artifact["summary"]["identity_matches"] == 4),
        check("repository_matches", artifact["summary"]["repository_matches"] == 4),
        check("crossref_matches", artifact["summary"]["crossref_matches"] >= 3),
        check("cornell_rate_limit_fenced", institutions["cornell"]["crossref_status"] == "SOURCE_LEAD_ONLY"),
        check("caltech_endpoint_current", institutions["caltech"]["repository_status"] == "MATCH"),
        check("warnings", len(artifact["source_warnings"]) == 3),
        check("negative_fixtures", len(artifact["negative_fixtures"]) == 10),
        check("tool_receipts", len(tool_receipts) == 5 and all(row["status"] == "MATCH" for row in tool_receipts.values())),
        check("no_theorems", artifact["current_promoted_theorems"] == []),
        check("no_laws", artifact["current_promoted_natural_laws"] == []),
        check("seal_present", len(artifact.get("seal", "")) == 64),
    ]
    failures = [row for row in checks if row["status"] != "MATCH"]
    print(
        json.dumps(
            {
                "schema": "Pass0145MultiInstitutionClaimGraphValidatorRun/v1",
                "pass": "0145",
                "status": "MATCH" if not failures else "DRIFT",
                "checks": checks,
                "failures": failures,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
