"""Validate pass 0065 OpenTelemetry trace to Telos action receipt fixture."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "otel-trace-to-action-receipt-fixture-pass-0065.json"
RESULT = ROOT / "schemas" / "pass-0065-otel-trace-to-action-receipt-fixture-validator-result.json"


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def sha256_obj(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def validate() -> dict:
    artifact = read_json(ARTIFACT)
    errors: list[str] = []
    unsealed = dict(artifact)
    seal = unsealed.pop("seal", None)
    trace = artifact.get("trace_fixture", {})
    receipt = artifact.get("action_receipt", {})
    required = {"receipt_id", "source_refs", "workspace_state", "authority_scope", "action_admission", "tool_call", "side_effect_class", "trace_refs", "eval_refs", "verification_verdict", "stop_reason", "compensation_pointer", "privacy_boundary", "receipt_status"}
    if artifact.get("schema") != "OtelTraceToTelosActionReceiptFixture/v1":
        errors.append("schema")
    if artifact.get("status") != "OTEL_TRACE_TO_ACTION_RECEIPT_FIXTURE_MATCH":
        errors.append("status")
    if seal != sha256_obj(unsealed):
        errors.append("seal")
    if trace.get("schema") != "OpenTelemetryTraceFixture/v1":
        errors.append("trace_schema")
    if len(trace.get("spans", [])) != 4:
        errors.append("span_count")
    if not required.issubset(receipt.keys()):
        errors.append("required_receipt_fields")
    if receipt.get("trace_refs", {}).get("trace_id") != trace.get("trace_id"):
        errors.append("trace_link")
    if len(receipt.get("trace_refs", {}).get("span_ids", [])) != len(trace.get("spans", [])):
        errors.append("span_link")
    if receipt.get("verification_verdict") != "MATCH" or receipt.get("receipt_status") != "MATCH":
        errors.append("receipt_status")
    if artifact.get("negative_fixture", {}).get("status") != "FAIL_EXPECTED":
        errors.append("negative_fixture")
    if artifact.get("unsupported_claim_count") != 0:
        errors.append("unsupported_claim_count")
    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0065OtelTraceToActionReceiptFixtureValidatorRun/v1",
        "pass": "0065",
        "status": status,
        "match": 1 if status == "MATCH" else 0,
        "drift": 0 if status == "MATCH" else 1,
        "checks": [
            {
                "artifact": "OtelTraceToTelosActionReceiptFixture",
                "errors": errors,
                "path": "schemas/otel-trace-to-action-receipt-fixture-pass-0065.json",
                "receipt_field_count": len(receipt.keys()),
                "span_count": len(trace.get("spans", [])),
                "status": status,
                "trace_id": trace.get("trace_id"),
            }
        ],
    }


def main() -> None:
    result = validate()
    write_json(RESULT, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
