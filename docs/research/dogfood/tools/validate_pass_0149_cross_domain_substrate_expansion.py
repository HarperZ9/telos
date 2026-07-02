"""Validate pass 0149 cross-domain substrate expansion artifact."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "cross-domain-substrate-expansion-pass-0149.json"


def check(name: str, ok: bool) -> dict[str, str]:
    return {"name": name, "status": "MATCH" if ok else "DRIFT"}


def main() -> int:
    artifact = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    summary = artifact["summary"]
    checks = [
        check("schema", artifact["schema"] == "CrossDomainSubstrateExpansionReceipt/v1"),
        check("status", artifact["status"] == "CROSS_DOMAIN_SUBSTRATE_EXPANSION_MATCH_WITH_WARNINGS"),
        check("candidate_substrates", summary["candidate_substrates"] >= 120),
        check("families", summary["families"] >= 14),
        check("domains", summary["domains"] >= 20),
        check("capture_jobs", summary["capture_jobs"] == 39),
        check("gather_verified", summary["gather_verified"] >= 20),
        check("capture_warnings", summary["capture_warnings"] >= 5),
        check("source_lead_only", summary["source_lead_only"] >= 80),
        check("workbenches", summary["workbenches"] == 12),
        check("adapter_policies", summary["adapter_policies"] == 7),
        check("negative_fixtures", summary["negative_fixtures"] == 12),
        check("empty_warning", any(row["status"] == "GATHER_EMPTY_WARNING" for row in artifact["capture_attempts"])),
        check("tool_receipts", len(artifact["tool_receipts"]) == 5 and all(row["status"] == "MATCH" for row in artifact["tool_receipts"].values())),
        check("no_theorems", artifact["current_promoted_theorems"] == []),
        check("no_laws", artifact["current_promoted_natural_laws"] == []),
        check("seal_present", len(artifact.get("seal", "")) == 64),
    ]
    failures = [row for row in checks if row["status"] != "MATCH"]
    print(json.dumps({"schema": "Pass0149CrossDomainSubstrateExpansionValidatorRun/v1", "pass": "0149", "status": "MATCH" if not failures else "DRIFT", "checks": checks, "failures": failures}, indent=2, sort_keys=True))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
