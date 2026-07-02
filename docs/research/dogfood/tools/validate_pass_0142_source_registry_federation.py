"""Validate pass 0142 source registry federation artifact."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "source-registry-federation-pass-0142.json"


def check(name: str, ok: bool) -> dict[str, str]:
    return {"name": name, "status": "MATCH" if ok else "DRIFT"}


def main() -> int:
    artifact = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    checks = [
        check("schema", artifact.get("schema") == "SourceRegistryFederationReceipt/v1"),
        check("status", artifact.get("status") == "SOURCE_REGISTRY_FEDERATION_MATCH"),
        check("source_rows", artifact["gather_summary"]["total_source_rows"] >= 33),
        check("usable_captures", artifact["gather_summary"]["usable_captures"] >= 20),
        check("source_warnings", artifact["gather_summary"]["warning_count"] >= 3),
        check("families", artifact["gather_summary"]["families"] >= 8),
        check("registry_layers", len(artifact["registry_layers"]) == 10),
        check("underpinnings", len(artifact["cross_industry_underpinnings"]) == 5),
        check("workbenches", len(artifact["world_problem_workbenches"]) == 8),
        check("adapter_requirements", len(artifact["adapter_requirements"]) == 15),
        check("negative_fixtures", len(artifact["negative_fixtures"]) == 10),
        check("updated_tool_floor", len(artifact["updated_tool_floor"]) == 5),
        check("no_theorems", artifact["current_promoted_theorems"] == []),
        check("no_laws", artifact["current_promoted_natural_laws"] == []),
        check("seal_present", len(artifact.get("seal", "")) == 64),
    ]
    failures = [row for row in checks if row["status"] != "MATCH"]
    result = {"schema": "Pass0142SourceRegistryFederationValidatorRun/v1", "pass": "0142", "status": "MATCH" if not failures else "DRIFT", "checks": checks, "failures": failures}
    print(json.dumps(result, indent=2, sort_keys=True))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
