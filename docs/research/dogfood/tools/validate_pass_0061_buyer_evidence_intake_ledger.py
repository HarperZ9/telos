"""Validate pass 0061 buyer evidence intake ledger."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "buyer-evidence-intake-ledger-pass-0061.json"
OUTREACH = ROOT / "schemas" / "buyer-outreach-packets-pass-0060.json"
RESULT = ROOT / "schemas" / "pass-0061-buyer-evidence-intake-ledger-validator-result.json"
BUYERS = {"research_lab", "ai_infra", "regulated_agent"}


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
    upstream = read_json(OUTREACH)
    errors: list[str] = []
    unsealed = dict(artifact)
    seal = unsealed.pop("seal", None)
    records = artifact.get("intake_records", [])
    field_count = sum(len(row.get("evidence_capture_fields", [])) for row in records)
    private_field_count = sum(len(row.get("private_fields_forbidden_in_model_context", [])) for row in records)
    if artifact.get("schema") != "BuyerEvidenceIntakeLedger/v1":
        errors.append("schema")
    if artifact.get("status") != "BUYER_EVIDENCE_INTAKE_LEDGER_MATCH":
        errors.append("status")
    if seal != sha256_obj(unsealed):
        errors.append("seal")
    if artifact.get("upstream_outreach", {}).get("seal") != upstream.get("seal"):
        errors.append("upstream_outreach")
    if artifact.get("buyer_response_status") != "AWAITING_REAL_RESPONSES":
        errors.append("buyer_response_status")
    if artifact.get("crm_write_status") != "NOT_WRITTEN":
        errors.append("crm_write_status")
    if artifact.get("send_status") != "NOT_SENT":
        errors.append("send_status")
    if artifact.get("unsupported_claim_count") != 0:
        errors.append("unsupported_claim_count")
    if artifact.get("current_promoted_natural_laws") != []:
        errors.append("natural_law_promotion")
    if {row.get("buyer_id") for row in records} != BUYERS:
        errors.append("buyer_ids")
    if field_count < 24:
        errors.append("field_count")
    if private_field_count < 18:
        errors.append("private_field_count")
    for row in records:
        buyer_id = row.get("buyer_id")
        if row.get("privacy_boundary") != "NO_PRIVATE_CONTACT_DATA_IN_MODEL_CONTEXT":
            errors.append(f"{buyer_id}_privacy")
        if row.get("response_status") != "AWAITING_REAL_RESPONSE":
            errors.append(f"{buyer_id}_response")
        if row.get("score_status") != "UNSCORED_PENDING_BUYER_EVIDENCE":
            errors.append(f"{buyer_id}_score")
    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0061BuyerEvidenceIntakeLedgerValidatorRun/v1",
        "pass": "0061",
        "status": status,
        "match": 1 if status == "MATCH" else 0,
        "drift": 0 if status == "MATCH" else 1,
        "checks": [
            {
                "artifact": "BuyerEvidenceIntakeLedger",
                "errors": errors,
                "field_count": field_count,
                "private_field_count": private_field_count,
                "record_count": len(records),
                "path": "schemas/buyer-evidence-intake-ledger-pass-0061.json",
                "status": status,
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
