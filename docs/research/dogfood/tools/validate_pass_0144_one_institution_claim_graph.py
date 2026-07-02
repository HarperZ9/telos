"""Validate pass 0144 one-institution claim graph artifact."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "one-institution-claim-graph-pass-0144.json"


def check(name: str, ok: bool) -> dict[str, str]:
    return {"name": name, "status": "MATCH" if ok else "DRIFT"}


def main() -> int:
    a = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    statuses = {row["join"]: row["status"] for row in a["join_verdicts"]}
    checks = [
        check("schema", a["schema"] == "OneInstitutionClaimGraphReceipt/v1"),
        check("status", a["status"] == "ONE_INSTITUTION_CLAIM_GRAPH_MATCH_WITH_WARNINGS"),
        check("captures", a["gather_summary"]["live_captures"] >= 6),
        check("docs", a["gather_summary"]["protocol_docs"] >= 5),
        check("ror_openalex_join", statuses.get("ror_openalex_identity") == "MATCH"),
        check("dspace_identify", statuses.get("dspace_oai_identify") == "MATCH"),
        check("dspace_records", statuses.get("dspace_recent_record_sample") == "MATCH"),
        check("crossref_affiliation", statuses.get("crossref_affiliation_sample") == "MATCH"),
        check("datacite_fenced", statuses.get("datacite_dataset_relation") == "SOURCE_LEAD_ONLY"),
        check("warnings", len(a["source_warnings"]) == 3),
        check("negative_fixtures", len(a["negative_fixtures"]) == 10),
        check("tool_receipts", len(a["tool_receipts"]) == 5 and all(row["status"] == "MATCH" for row in a["tool_receipts"].values())),
        check("no_theorems", a["current_promoted_theorems"] == []),
        check("no_laws", a["current_promoted_natural_laws"] == []),
        check("seal_present", len(a.get("seal", "")) == 64),
    ]
    failures = [row for row in checks if row["status"] != "MATCH"]
    print(json.dumps({"schema": "Pass0144OneInstitutionClaimGraphValidatorRun/v1", "pass": "0144", "status": "MATCH" if not failures else "DRIFT", "checks": checks, "failures": failures}, indent=2, sort_keys=True))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
