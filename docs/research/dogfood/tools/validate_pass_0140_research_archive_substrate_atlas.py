"""Validate pass 0140 research archive substrate atlas artifact."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "research-archive-substrate-atlas-pass-0140.json"


def main() -> None:
    artifact = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    checks = [
        ("schema", artifact["schema"] == "ResearchArchiveSubstrateAtlasReceipt/v1"),
        ("status", artifact["status"] == "RESEARCH_ARCHIVE_SUBSTRATE_ATLAS_MATCH"),
        ("captured_sources", artifact["gather_summary"]["captured_sources"] >= 28),
        ("usable_captures", artifact["gather_summary"]["usable_captures"] >= 26),
        ("source_systems", len(artifact["source_systems"]) >= 30),
        ("source_quality_warnings", len(artifact["source_quality_warnings"]) >= 4),
        ("substrate_families", len(artifact["substrate_families"]) >= 14),
        ("domain_queue", len(artifact["domain_expansion_queue"]) >= 18),
        ("megatool_routes", len(artifact["megatool_routes"]) >= 6),
        ("negative_fixtures", len(artifact["negative_fixtures"]) >= 10 and all(row["status"] == "REJECTED" for row in artifact["negative_fixtures"])),
        ("flagships", all(row["status"].startswith("MATCH") for row in artifact["flagship_receipts"].values())),
        ("non_promotion", artifact["current_promoted_natural_laws"] == []),
    ]
    failures = [name for name, ok in checks if not ok]
    result = {"schema": "Pass0140ResearchArchiveSubstrateAtlasValidatorRun/v1", "pass": "0140", "status": "MATCH" if not failures else "DRIFT", "checks": [{"name": name, "status": "MATCH" if ok else "DRIFT"} for name, ok in checks], "failures": failures}
    print(json.dumps(result, indent=2, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
