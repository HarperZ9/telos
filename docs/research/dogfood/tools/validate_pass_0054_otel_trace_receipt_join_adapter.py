"""Validate pass 0054 OTel trace receipt join adapter artifacts."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PASS_ARTIFACT = ROOT / "schemas" / "otel-trace-receipt-join-adapter-pass-0054.json"
JOIN_OUTPUT = ROOT / "schemas" / "otel-trace-receipt-join-pass-0054.json"
UPSTREAM_RECEIPT = ROOT / "schemas" / "telos-action-receipt-fixture-pass-0024.json"
RESULT_PATH = ROOT / "schemas" / "pass-0054-otel-trace-receipt-join-adapter-validator-result.json"


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_obj(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def validate() -> dict:
    artifact = read_json(PASS_ARTIFACT)
    join = read_json(JOIN_OUTPUT)
    upstream = read_json(UPSTREAM_RECEIPT)
    errors: list[str] = []
    unsealed = dict(artifact)
    seal = unsealed.pop("seal", None)
    if artifact.get("schema") != "OTelTraceReceiptJoinAdapterSet/v1":
        errors.append("schema")
    if artifact.get("status") != "OTEL_TRACE_RECEIPT_JOIN_ADAPTER_MATCH":
        errors.append("status")
    if seal != sha256_obj(unsealed):
        errors.append("seal")
    if artifact.get("join_output", {}).get("sha256") != sha256_file(JOIN_OUTPUT):
        errors.append("join_output_sha")
    if join.get("status") != "OTEL_TRACE_RECEIPT_JOIN_MATCH":
        errors.append("join_status")
    if join.get("join_summary", {}).get("joined_event_count") != 4:
        errors.append("joined_event_count")
    if join.get("join_summary", {}).get("trace_replaces_receipt_count") != 0:
        errors.append("trace_replaces_receipt_count")
    if join.get("negative_match_count") != 4 or join.get("negative_pass_observed_count") != 0:
        errors.append("negative_fixture_replay")
    if join.get("durable_receipt_identity", {}).get("receipt_ref") == join.get("imported_trace_ref"):
        errors.append("receipt_identity_replaced")
    binding = artifact.get("upstream_receipt_binding", {})
    if binding.get("sha256") != sha256_file(UPSTREAM_RECEIPT):
        errors.append("upstream_sha")
    if binding.get("seal") != upstream.get("seal"):
        errors.append("upstream_seal")
    if artifact.get("current_promoted_natural_laws") != []:
        errors.append("natural_law_promotion")
    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0054OTelTraceReceiptJoinAdapterValidatorRun/v1",
        "pass": "0054",
        "status": status,
        "match": 1 if status == "MATCH" else 0,
        "drift": 0 if status == "MATCH" else 1,
        "checks": [
            {
                "artifact": "OTelTraceReceiptJoinAdapterSet",
                "errors": errors,
                "joined_event_count": join.get("join_summary", {}).get("joined_event_count"),
                "path": "schemas/otel-trace-receipt-join-adapter-pass-0054.json",
                "status": status,
                "trace_replaces_receipt_count": join.get("join_summary", {}).get("trace_replaces_receipt_count"),
            }
        ],
    }


def main() -> None:
    result = validate()
    write_json(RESULT_PATH, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
