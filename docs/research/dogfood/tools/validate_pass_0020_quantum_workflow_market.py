"""Validate pass 0020 quantum workflow market and import-audit receipts."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "quantum-workflow-market-import-audit-pass-0020.json"


def require(condition: bool, errors: list[str], message: str) -> None:
    if not condition:
        errors.append(message)


def in_range(value: object) -> bool:
    return isinstance(value, int) and 1 <= value <= 5


def main() -> int:
    data = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    errors: list[str] = []

    require(data.get("schema") == "QuantumWorkflowMarketImportSet/v1", errors, "wrong schema")
    require(data.get("pass") == "0020", errors, "wrong pass")
    require(data.get("status") == "MARKET_IMPORT_AUDIT_MATCH", errors, "wrong status")
    require(bool(data.get("seal")), errors, "missing seal")
    require("does not install packages" in data.get("non_promotion_statement", ""), errors, "missing non-promotion")

    rows = data.get("market_rows", [])
    require(len(rows) >= 12, errors, "expected at least 12 market rows")
    require(data.get("market_row_count") == len(rows), errors, "market row count mismatch")
    allowed_gap_status = {"verified", "inferred", "unverified"}
    for row in rows:
        label = row.get("company_tool", "unknown")
        require(row.get("schema") == "MarketRow/v1", errors, f"{label} wrong schema")
        require(row.get("category"), errors, f"{label} missing category")
        require(row.get("buyer"), errors, f"{label} missing buyer")
        require(row.get("official_claim"), errors, f"{label} missing official claim")
        require(row.get("market_gap_status") in allowed_gap_status, errors, f"{label} invalid gap status")
        require(row.get("uniqueness_claim_policy") == "HYPOTHESIS_ONLY_UNLESS_MATRIX_PROVES_EXCLUSION", errors, f"{label} uniqueness policy missing")
        sources = row.get("sources", [])
        require(bool(sources), errors, f"{label} missing sources")
        require(all(str(url).startswith("https://") for url in sources), errors, f"{label} source not HTTPS")
        combined = json.dumps(row, sort_keys=True).lower()
        require("no competitor does this" not in combined, errors, f"{label} contains unsupported uniqueness claim")

    scores = data.get("wedge_scorecard", [])
    require(len(scores) >= 3, errors, "expected at least three wedge scores")
    for score in scores:
        for field in ["urgency", "budget", "differentiation", "feasibility", "proof_demo_readiness", "risk"]:
            require(in_range(score.get(field)), errors, f"{score.get('market')} invalid score {field}")
        require("hypoth" in score.get("ranking_note", "").lower(), errors, f"{score.get('market')} score note must be hypothesis-labelled")

    audit = data.get("package_import_audit", [])
    require(len(audit) >= 10, errors, "expected at least 10 import audit rows")
    require(data.get("audit_row_count") == len(audit), errors, "audit row count mismatch")
    for receipt in audit:
        label = receipt.get("distribution", "unknown")
        require(receipt.get("schema") == "LocalPackageImportAuditReceipt/v1", errors, f"{label} wrong audit schema")
        require(receipt.get("import_attempted") is False, errors, f"{label} should not be imported in audit")
        require(receipt.get("version_status") in {"FOUND", "NOT_INSTALLED"}, errors, f"{label} invalid version status")
        require(receipt.get("receipt_hash"), errors, f"{label} missing receipt hash")

    nodes = data.get("megatool_integration_map", [])
    require(len(nodes) >= 10, errors, "expected at least ten megatool nodes")
    for node in nodes:
        label = node.get("internal_tool", "unknown")
        require(node.get("schema") == "MegatoolNode/v1", errors, f"{label} wrong node schema")
        require(node.get("inputs"), errors, f"{label} missing inputs")
        require(node.get("outputs"), errors, f"{label} missing outputs")
        require(node.get("receipts"), errors, f"{label} missing receipts")
        require(node.get("verification_layer"), errors, f"{label} missing verification layer")
        require(node.get("market_facing_product"), errors, f"{label} missing product")

    ladder = data.get("promotion_ladder", [])
    required_states = {"SYNTHETIC_ADAPTER_FIXTURE", "FRAMEWORK_IMPORT_FIXTURE", "LIVE_PROVIDER_FIXTURE", "PUBLIC_PROOF_DEMO"}
    require(required_states <= {item.get("state") for item in ladder}, errors, "promotion ladder missing required state")

    demos = data.get("demo_recommendations", [])
    require(len(demos) >= 3, errors, "expected at least three demos")
    require(data.get("primary_market_push", {}).get("rank") == 1, errors, "missing ranked primary push")
    require("hypothesis" in data.get("primary_market_push", {}).get("why_now", "").lower(), errors, "primary push must be hypothesis-labelled")

    anchors = data.get("source_anchors", [])
    require(len(anchors) >= 20, errors, "expected at least 20 source anchors")
    require(data.get("source_anchor_count") == len(anchors), errors, "source anchor count mismatch")
    require(all(str(anchor.get("url", "")).startswith("https://") for anchor in anchors), errors, "source anchor missing HTTPS")

    result = {
        "schema": "Pass0020QuantumWorkflowMarketValidatorRun/v1",
        "pass": "0020",
        "status": "MATCH" if not errors else "DRIFT",
        "match": 1 if not errors else 0,
        "drift": 0 if not errors else 1,
        "checks": [
            {
                "artifact": "QuantumWorkflowMarketImportSet",
                "path": str(SCHEMA_PATH.relative_to(ROOT)),
                "status": "MATCH" if not errors else "DRIFT",
                "market_row_count": len(rows),
                "wedge_score_count": len(scores),
                "audit_row_count": len(audit),
                "megatool_node_count": len(nodes),
                "source_anchor_count": len(anchors),
                "errors": errors,
            }
        ],
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
