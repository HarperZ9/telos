"""Validate Project Telos dogfood research artifacts.

This is intentionally small and local to the dogfood research program. It
checks the schema shapes that prior passes already produced; it does not define
product APIs.
"""

from __future__ import annotations

import json
import sys
import argparse
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def artifact_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def check_rows(
    *,
    artifact: str,
    path: Path,
    key: str,
    minimum: int,
    required_fields: list[str],
) -> dict[str, Any]:
    data = load_json(path)
    rows = data.get(key, [])
    errors: list[str] = []

    if not isinstance(rows, list):
        errors.append(f"{key} is not a list")
        rows = []

    if len(rows) < minimum:
        errors.append(f"{key} count {len(rows)} below minimum {minimum}")

    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            errors.append(f"{key}[{index}] is not an object")
            continue
        for field in required_fields:
            if field not in row:
                errors.append(f"{key}[{index}] missing {field}")
            elif row[field] in (None, "", []):
                errors.append(f"{key}[{index}] empty {field}")

    return {
        "artifact": artifact,
        "path": display_path(path),
        "key": key,
        "count": len(rows),
        "minimum": minimum,
        "required_fields": required_fields,
        "errors": errors,
        "status": "MATCH" if not errors else "DRIFT",
    }


def validate_proof_packet(path: Path) -> dict[str, Any]:
    data = load_json(path)
    required = [
        "packet_id",
        "schema",
        "domain",
        "claim_set",
        "source_receipts",
        "action_receipts",
        "authority_receipts",
        "workspace_state",
        "verification_verdicts",
        "failure_labels",
        "decision_summary",
    ]
    errors: list[str] = []

    for field in required:
        if field not in data:
            errors.append(f"missing {field}")
        elif data[field] in (None, "", []):
            errors.append(f"empty {field}")

    decision = data.get("decision_summary", {})
    if not isinstance(decision, dict):
        errors.append("decision_summary is not an object")
    else:
        for field in ["decision", "reason", "confidence", "next_action"]:
            if not decision.get(field):
                errors.append(f"decision_summary missing {field}")

    promoted = [
        claim
        for claim in data.get("claim_set", [])
        if isinstance(claim, dict) and claim.get("promotion_state") == "PROMOTED_LAW"
    ]
    if promoted:
        errors.append("proof packet promotes a law")

    return {
        "artifact": "ProofPacketMinimumValidator",
        "path": display_path(path),
        "required_fields": required,
        "claim_count": len(data.get("claim_set", [])),
        "errors": errors,
        "status": "MATCH" if not errors else "DRIFT",
    }


def validate_all() -> dict[str, Any]:
    checks = [
        check_rows(
            artifact="MarketRowValidator",
            path=SCHEMAS / "market-rows-pass-0003.json",
            key="rows",
            minimum=42,
            required_fields=[
                "category",
                "company_tool",
                "buyer",
                "official_claim",
                "capabilities",
                "gaps",
                "gap_status",
                "sources",
                "confidence",
            ],
        ),
        check_rows(
            artifact="WedgeScoreValidator",
            path=SCHEMAS / "wedge-scores-pass-0003.json",
            key="scores",
            minimum=8,
            required_fields=[
                "market",
                "urgency",
                "budget",
                "differentiation",
                "feasibility",
                "proof_demo_readiness",
                "risk",
                "rank",
            ],
        ),
        check_rows(
            artifact="MegatoolNodeValidator",
            path=SCHEMAS / "megatool-nodes-pass-0003.json",
            key="nodes",
            minimum=8,
            required_fields=[
                "internal_tool",
                "external_analogs",
                "inputs",
                "outputs",
                "receipts",
                "verification_layer",
                "market_facing_product",
            ],
        ),
        check_rows(
            artifact="ResearchClaimValidator",
            path=SCHEMAS / "research-claims-pass-0004.json",
            key="claims",
            minimum=12,
            required_fields=[
                "claim",
                "evidence_url",
                "confidence",
                "verification_status",
                "notes",
            ],
        ),
        check_rows(
            artifact="ProofPacketAdapterValidator",
            path=SCHEMAS / "proof-packet-adapters-pass-0005.json",
            key="adapters",
            minimum=10,
            required_fields=[
                "priority",
                "adapter",
                "external_analogs",
                "buyer_workflow",
                "evidence_inputs",
                "telos_outputs",
                "missing_binding",
                "build_first",
                "source_urls",
                "confidence",
            ],
        ),
        check_rows(
            artifact="BuyerObjectionValidator",
            path=SCHEMAS / "buyer-objections-pass-0005.json",
            key="objections",
            minimum=7,
            required_fields=[
                "objection",
                "buyer_question",
                "required_demo_evidence",
                "product_response",
                "status",
                "confidence",
            ],
        ),
        check_rows(
            artifact="ValidatorContractValidator",
            path=SCHEMAS / "validator-contracts-pass-0005.json",
            key="contracts",
            minimum=8,
            required_fields=[
                "validator",
                "target_schema",
                "required_fields",
                "minimum_rows",
                "failure_modes",
                "first_target",
            ],
        ),
        check_rows(
            artifact="OpenTelemetryActionNormalizationValidator",
            path=SCHEMAS / "otel-action-normalization-pass-0006.json",
            key="mappings",
            minimum=8,
            required_fields=[
                "otel_field",
                "telos_field",
                "normalization_rule",
                "lossiness",
                "required",
            ],
        ),
        validate_proof_packet(SCHEMAS / "proof-packet-pass-0006.json"),
    ]

    status = "MATCH" if all(check["status"] == "MATCH" for check in checks) else "DRIFT"
    result = {
        "schema": "DogfoodValidatorRun/v1",
        "pass": "0006",
        "status": status,
        "checks": checks,
        "match": sum(1 for check in checks if check["status"] == "MATCH"),
        "drift": sum(1 for check in checks if check["status"] == "DRIFT"),
    }
    return result


def validate_one_proof_packet(path: Path) -> dict[str, Any]:
    check = validate_proof_packet(path)
    return {
        "schema": "ProofPacketValidatorRun/v1",
        "status": check["status"],
        "check": check,
        "match": 1 if check["status"] == "MATCH" else 0,
        "drift": 1 if check["status"] == "DRIFT" else 0,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate Telos dogfood artifacts.")
    parser.add_argument(
        "--proof-packet",
        help="Validate one ProofPacket/v1 JSON artifact instead of the full dogfood set.",
    )
    args = parser.parse_args(argv)

    if args.proof_packet:
        result = validate_one_proof_packet(artifact_path(args.proof_packet))
    else:
        result = validate_all()

    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "MATCH" else 1


if __name__ == "__main__":
    raise SystemExit(main())
