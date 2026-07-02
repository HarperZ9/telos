"""Validate pass 0060 buyer outreach packets."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "buyer-outreach-packets-pass-0060.json"
SCORECARDS = ROOT / "schemas" / "buyer-discovery-evidence-scorecards-pass-0059.json"
RESULT = ROOT / "schemas" / "pass-0060-buyer-outreach-packets-validator-result.json"
LANES = ["project-telos", "deep-research", "technical-writing"]
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
    upstream = read_json(SCORECARDS)
    errors: list[str] = []
    unsealed = dict(artifact)
    seal = unsealed.pop("seal", None)
    packets = artifact.get("outreach_packets", [])
    field_count = sum(len(row.get("evidence_intake_fields", [])) for row in packets)
    followup_count = sum(len(row.get("follow_up_schedule", [])) for row in packets)
    if artifact.get("schema") != "BuyerOutreachPacketSet/v1":
        errors.append("schema")
    if artifact.get("status") != "BUYER_OUTREACH_PACKETS_MATCH":
        errors.append("status")
    if seal != sha256_obj(unsealed):
        errors.append("seal")
    if artifact.get("upstream_scorecards", {}).get("seal") != upstream.get("seal"):
        errors.append("upstream_scorecards")
    if artifact.get("crm_write_status") != "NOT_WRITTEN":
        errors.append("crm_write_status")
    if artifact.get("send_status") != "NOT_SENT":
        errors.append("send_status")
    if artifact.get("market_claim_boundary") != "HYPOTHESIS_ONLY":
        errors.append("market_boundary")
    if artifact.get("unsupported_claim_count") != 0:
        errors.append("unsupported_claim_count")
    if artifact.get("current_promoted_natural_laws") != []:
        errors.append("natural_law_promotion")
    if {row.get("buyer_id") for row in packets} != BUYERS:
        errors.append("buyer_ids")
    if field_count < 18:
        errors.append("field_count")
    if followup_count != 9:
        errors.append("followup_count")
    for row in packets:
        buyer_id = row.get("buyer_id")
        payload_path = ROOT.parents[2] / row.get("payload_ref", "")
        if row.get("route_lane_split") != LANES:
            errors.append(f"{buyer_id}_lanes")
        if row.get("counterparty_seed", {}).get("status") != "prospect_unverified":
            errors.append(f"{buyer_id}_seed_status")
        if not payload_path.exists():
            errors.append(f"{buyer_id}_payload_missing")
    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0060BuyerOutreachPacketsValidatorRun/v1",
        "pass": "0060",
        "status": status,
        "match": 1 if status == "MATCH" else 0,
        "drift": 0 if status == "MATCH" else 1,
        "checks": [
            {
                "artifact": "BuyerOutreachPacketSet",
                "errors": errors,
                "field_count": field_count,
                "followup_count": followup_count,
                "packet_count": len(packets),
                "path": "schemas/buyer-outreach-packets-pass-0060.json",
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
