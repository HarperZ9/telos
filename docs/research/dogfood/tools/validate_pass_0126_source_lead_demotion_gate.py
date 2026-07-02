"""Validate pass 0126 source-lead demotion gate."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "source-lead-demotion-gate-pass-0126.json"
RESULT = ROOT / "schemas" / "pass-0126-source-lead-demotion-gate-validator-result.json"


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)


def sha256_obj(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n", encoding="utf-8")


def require(condition: bool, errors: list[str], label: str) -> None:
    if not condition:
        errors.append(label)


def validate() -> dict:
    artifact = read_json(ARTIFACT)
    unsealed = dict(artifact)
    seal = unsealed.pop("seal", None)
    fixtures = artifact.get("gate_fixtures", [])
    errors: list[str] = []

    require(artifact.get("schema") == "SourceLeadDemotionGateReceipt/v1", errors, "schema")
    require(artifact.get("status") == "SOURCE_LEAD_DEMOTION_GATE_MATCH", errors, "status")
    require(seal == sha256_obj(unsealed), errors, "seal")
    require(artifact.get("source_bindings", {}).get("youtube_router_pass") == "0125", errors, "youtube_router_binding")
    require(artifact.get("source_bindings", {}).get("agent_action_adapter_pass") == "0124", errors, "adapter_binding")
    require(len(fixtures) == 7, errors, "fixture_count")
    require(all(row.get("matches_expected") for row in fixtures), errors, "fixture_expectations")
    require(artifact.get("accepted_count") == 3, errors, "accepted_count")
    require(artifact.get("rejected_count") == 4, errors, "rejected_count")
    require(any("video_only_promotion" in row.get("failures", []) for row in fixtures), errors, "video_rejection")
    require(any("law_promotion_forbidden" in row.get("failures", []) for row in fixtures), errors, "law_rejection")
    require(any("raw_transcript_included" in row.get("failures", []) for row in fixtures), errors, "raw_transcript_rejection")
    require(any("keyword_count_not_proof" in row.get("failures", []) for row in fixtures), errors, "keyword_rejection")
    require(all(row.get("raw_transcript_included") is False for row in artifact.get("source_lead_summary", [])), errors, "source_summary_boundary")
    require(all(row.get("status") == "MATCH" for row in artifact.get("flagship_receipts", {}).values()), errors, "flagships")
    require(artifact.get("unsupported_claim_count") == 0, errors, "unsupported_claim_count")
    require(artifact.get("current_promoted_natural_laws") == [], errors, "natural_laws")

    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0126SourceLeadDemotionGateValidatorRun/v1",
        "pass": "0126",
        "status": status,
        "checks": [{"artifact": "SourceLeadDemotionGate", "errors": errors, "status": status, "fixture_count": len(fixtures), "accepted_count": artifact.get("accepted_count"), "rejected_count": artifact.get("rejected_count")}],
    }


def main() -> None:
    result = validate()
    write_json(RESULT, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
