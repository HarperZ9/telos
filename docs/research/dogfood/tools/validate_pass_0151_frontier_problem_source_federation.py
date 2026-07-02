"""Validate pass 0151 frontier problem source federation artifact."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "frontier-problem-source-federation-pass-0151.json"


def check(name: str, ok: bool) -> dict[str, str]:
    return {"name": name, "status": "MATCH" if ok else "DRIFT"}


def main() -> int:
    artifact = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    summary = artifact["summary"]
    checks = [
        check("schema", artifact["schema"] == "FrontierProblemSourceFederationReceipt/v1"),
        check("status", artifact["status"] == "FRONTIER_PROBLEM_SOURCE_FEDERATION_MATCH_WITH_WARNINGS"),
        check("candidate_sources", summary["candidate_sources"] >= 80),
        check("families", summary["families"] >= 14),
        check("domains", summary["domains"] >= 25),
        check("capture_jobs", summary["capture_jobs"] == 28),
        check("gather_verified", summary["gather_verified"] >= 20),
        check("capture_warnings", summary["capture_warnings"] >= 4),
        check("college_database_sources", summary["college_database_sources"] >= 10),
        check("preprint_sources", summary["preprint_sources"] >= 8),
        check("scholarly_graph_sources", summary["scholarly_graph_sources"] >= 8),
        check("combined_context", summary["combined_nondeduplicated_substrate_context"] >= 200),
        check("problem_lanes", summary["problem_lanes"] == 12),
        check("admission_gates", summary["admission_gates"] == 8),
        check("negative_fixtures", summary["negative_fixtures"] == 12),
        check("warning_probe_present", any(row["status"].endswith("WARNING") for row in artifact["capture_attempts"])),
        check("tool_receipts", len(artifact["tool_receipts"]) == 5 and all(row["status"] == "MATCH" for row in artifact["tool_receipts"].values())),
        check("no_theorems", artifact["current_promoted_theorems"] == []),
        check("no_laws", artifact["current_promoted_natural_laws"] == []),
        check("no_world_solutions", artifact["current_promoted_world_solutions"] == []),
        check("seal_present", len(artifact.get("seal", "")) == 64),
    ]
    failures = [row for row in checks if row["status"] != "MATCH"]
    print(json.dumps({"schema": "Pass0151FrontierProblemSourceFederationValidatorRun/v1", "pass": "0151", "status": "MATCH" if not failures else "DRIFT", "checks": checks, "failures": failures}, indent=2, sort_keys=True))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
