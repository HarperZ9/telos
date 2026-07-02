"""Validate pass 0143 registry adapter contract artifact."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "registry-adapter-contracts-pass-0143.json"


def check(name: str, ok: bool) -> dict[str, str]:
    return {"name": name, "status": "MATCH" if ok else "DRIFT"}


def main() -> int:
    artifact = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    observed = artifact["updated_tool_floor_observed"]
    checks = [
        check("schema", artifact.get("schema") == "RegistryAdapterContractsReceipt/v1"),
        check("status", artifact.get("status") == "REGISTRY_ADAPTER_CONTRACTS_MATCH"),
        check("source_registry", artifact["source_registry_ref"]["status"] == "SOURCE_REGISTRY_FEDERATION_MATCH"),
        check("contracts", len(artifact["contracts"]) == 2),
        check("repo_records", len(artifact["repository_directory_records"]) >= 6),
        check("graph_records", len(artifact["scholarly_graph_records"]) >= 8),
        check("join_keys", len(artifact["join_keys"]) >= 12),
        check("negative_fixtures", len(artifact["negative_fixtures"]) == 10),
        check("negative_rejections", all(row["expected_status"] == "REJECT" for row in artifact["negative_fixtures"])),
        check("tool_floor_count", len(observed) == 5),
        check("tool_floor_match", not artifact["tool_floor_mismatches"]),
        check("tool_receipts_match", all(row["status"] == "MATCH" for row in observed.values())),
        check("no_theorems", artifact["current_promoted_theorems"] == []),
        check("no_laws", artifact["current_promoted_natural_laws"] == []),
        check("seal_present", len(artifact.get("seal", "")) == 64),
    ]
    failures = [row for row in checks if row["status"] != "MATCH"]
    result = {"schema": "Pass0143RegistryAdapterContractsValidatorRun/v1", "pass": "0143", "status": "MATCH" if not failures else "DRIFT", "checks": checks, "failures": failures}
    print(json.dumps(result, indent=2, sort_keys=True))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
