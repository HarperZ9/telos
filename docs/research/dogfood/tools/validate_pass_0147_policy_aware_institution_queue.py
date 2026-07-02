"""Validate pass 0147 policy-aware institution queue artifact."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "policy-aware-institution-queue-pass-0147.json"


def check(name: str, ok: bool) -> dict[str, str]:
    return {"name": name, "status": "MATCH" if ok else "DRIFT"}


def main() -> int:
    artifact = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    rows = {row["id"]: row for row in artifact["institutions"]}
    checks = [
        check("schema", artifact["schema"] == "PolicyAwareInstitutionQueueReceipt/v1"),
        check("status", artifact["status"] == "POLICY_AWARE_INSTITUTION_QUEUE_MATCH_WITH_WARNINGS"),
        check("institutions", artifact["summary"]["institutions"] == 4),
        check("source_captures", artifact["summary"]["source_captures"] == 16),
        check("identity_warning", artifact["summary"]["identity_warnings"] == 1),
        check("repository_warning", artifact["summary"]["repository_warnings"] == 1),
        check("crossref_samples", artifact["summary"]["crossref_samples"] == 4),
        check("negative_fixtures", artifact["summary"]["negative_fixtures"] == 10),
        check("tokyo_identity_rank", rows["university-of-tokyo"]["identity"]["ror_rank_for_openalex"] == 2),
        check("usp_repository_drift", rows["universidade-de-sao-paulo"]["repository"]["status"] == "SOURCE_LEAD_ONLY_ENDPOINT_DRIFT"),
        check("source_refs", all(len(row["source_refs"]) == 4 for row in artifact["institutions"])),
        check("prior_policy", len(artifact["prior_policy_rules"]) == 12),
        check("tool_receipts", len(artifact["tool_receipts"]) == 5 and all(row["status"] == "MATCH" for row in artifact["tool_receipts"].values())),
        check("no_theorems", artifact["current_promoted_theorems"] == []),
        check("no_laws", artifact["current_promoted_natural_laws"] == []),
        check("seal_present", len(artifact.get("seal", "")) == 64),
    ]
    failures = [row for row in checks if row["status"] != "MATCH"]
    print(json.dumps({"schema": "Pass0147PolicyAwareInstitutionQueueValidatorRun/v1", "pass": "0147", "status": "MATCH" if not failures else "DRIFT", "checks": checks, "failures": failures}, indent=2, sort_keys=True))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
