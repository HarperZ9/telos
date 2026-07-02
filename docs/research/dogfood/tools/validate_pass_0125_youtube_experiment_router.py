"""Validate pass 0125 YouTube experiment router."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "youtube-experiment-router-pass-0125.json"
RESULT = ROOT / "schemas" / "pass-0125-youtube-experiment-router-validator-result.json"


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
    leads = artifact.get("youtube_source_leads", [])
    experiments = artifact.get("routed_experiments", [])
    upstream = artifact.get("upstream_receipts", {})
    errors: list[str] = []

    require(artifact.get("schema") == "YoutubeExperimentRouterReceipt/v1", errors, "schema")
    require(artifact.get("status") == "YOUTUBE_EXPERIMENT_ROUTER_MATCH", errors, "status")
    require(seal == sha256_obj(unsealed), errors, "seal")
    require(len(leads) == 4, errors, "lead_count")
    require(all(row.get("claim_status") == "SOURCE_LEAD_ONLY" for row in leads), errors, "lead_status")
    require(all(row.get("raw_transcript_included") is False for row in leads), errors, "raw_transcript_boundary")
    require(all(row.get("transcript_object_present") for row in leads), errors, "transcript_objects")
    require(all(row.get("transcript_chars", 0) > 1000 for row in leads), errors, "transcript_chars")
    require(len(experiments) >= 6, errors, "experiment_count")
    require(all(row.get("claim_status") == "HYPOTHESIS" for row in experiments), errors, "experiment_status")
    require(all(row.get("success_receipt") and row.get("falsifiers") for row in experiments), errors, "receipt_falsifier_fields")
    require(upstream.get("youtube_growth", {}).get("pass") == "0121", errors, "youtube_upstream")
    require(upstream.get("field_factory", {}).get("pass") == "0123", errors, "field_factory_upstream")
    require(upstream.get("agent_action_adapter", {}).get("pass") == "0124", errors, "agent_action_upstream")
    require(all(row.get("status") == "MATCH" for row in artifact.get("flagship_receipts", {}).values()), errors, "flagships")
    require(artifact.get("unsupported_claim_count") == 0, errors, "unsupported_claim_count")
    require(artifact.get("current_promoted_natural_laws") == [], errors, "natural_laws")

    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0125YoutubeExperimentRouterValidatorRun/v1",
        "pass": "0125",
        "status": status,
        "checks": [{"artifact": "YoutubeExperimentRouter", "errors": errors, "status": status, "lead_count": len(leads), "experiment_count": len(experiments)}],
    }


def main() -> None:
    result = validate()
    write_json(RESULT, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
