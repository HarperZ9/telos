"""Validate pass 0146 adapter retry policy artifact."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "adapter-retry-policy-pass-0146.json"


def check(name: str, ok: bool) -> dict[str, str]:
    return {"name": name, "status": "MATCH" if ok else "DRIFT"}


def main() -> int:
    artifact = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    rules = {row["id"]: row for row in artifact["policy_rules"]}
    scenarios = {row["id"]: row for row in artifact["scenario_fixtures"]}
    checks = [
        check("schema", artifact["schema"] == "AdapterRetryPolicyReceipt/v1"),
        check("status", artifact["status"] == "ADAPTER_RETRY_POLICY_MATCH"),
        check("sources", artifact["summary"]["policy_sources"] == 11),
        check("systems", artifact["summary"]["source_systems"] >= 5),
        check("rules", artifact["summary"]["policy_rules"] == 12),
        check("scenarios", artifact["summary"]["scenario_fixtures"] == 10),
        check("negative_fixtures", artifact["summary"]["negative_fixtures"] == 10),
        check("prior_warnings", artifact["summary"]["prior_warnings"] == 3),
        check("source_evidence", len(artifact["source_evidence"]) == 11 and all(row["sha256"] for row in artifact["source_evidence"])),
        check("crossref_429_rule", "RATE_LIMITED_429" in rules),
        check("openalex_auth_rule", rules["OPENALEX_API_KEY_CURRENT"]["status"] == "AUTH_POLICY"),
        check("oai_503_rule", rules["NO_AUTO_RETRY_ON_HEADERLESS_503"]["status"] == "HALT_OR_OPERATOR_POLICY"),
        check("scenario_gate", scenarios["openalex_mailto_only"]["promotion_allowed"] is False),
        check("tool_receipts", len(artifact["tool_receipts"]) == 5 and all(row["status"] == "MATCH" for row in artifact["tool_receipts"].values())),
        check("no_theorems", artifact["current_promoted_theorems"] == []),
        check("no_laws", artifact["current_promoted_natural_laws"] == []),
        check("seal_present", len(artifact.get("seal", "")) == 64),
    ]
    failures = [row for row in checks if row["status"] != "MATCH"]
    print(json.dumps({"schema": "Pass0146AdapterRetryPolicyValidatorRun/v1", "pass": "0146", "status": "MATCH" if not failures else "DRIFT", "checks": checks, "failures": failures}, indent=2, sort_keys=True))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
