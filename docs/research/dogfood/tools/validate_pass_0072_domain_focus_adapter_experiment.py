"""Validate pass 0072 domain-focus adapter experiment."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "domain-focus-adapter-experiment-pass-0072.json"
RESULT = ROOT / "schemas" / "pass-0072-domain-focus-adapter-experiment-validator-result.json"


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
    if artifact.get("schema") != "DomainFocusAdapterExperiment/v1":
        errors.append("schema")
    if artifact.get("status") != "DOMAIN_FOCUS_ADAPTER_EXPERIMENT_MATCH":
        errors.append("status")
    if seal != sha256_obj(unsealed):
        errors.append("seal")
    if artifact.get("domain_count") != len(artifact.get("adapter_rows", [])):
        errors.append("adapter_count")
    if artifact.get("route_summary", {}).get("adapted_project_telos") != artifact.get("domain_count"):
        errors.append("adapted_project_telos")
    if artifact.get("route_summary", {}).get("adapted_escalations") != 0:
        errors.append("adapted_escalations")
    if artifact.get("index_summary", {}).get("valid_focuses") != ["telos"]:
        errors.append("index_valid_focuses")
    if artifact.get("index_summary", {}).get("rejected_focus_count", 0) < 5:
        errors.append("index_rejected_focus_count")
    if len(artifact.get("tool_improvement_queue", [])) != 5:
        errors.append("tool_improvement_count")
    if artifact.get("unsupported_claim_count") != 0:
        errors.append("unsupported_claim_count")
    if len(artifact.get("negative_fixtures", [])) < 6:
        errors.append("negative_fixture_count")
    for item in artifact.get("negative_fixtures", []):
        if item.get("expected_status") != "REJECT" or not item.get("reject_reason"):
            errors.append(f"negative_fixture:{item.get('fixture_id')}")
    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0072DomainFocusAdapterExperimentValidatorRun/v1",
        "pass": "0072",
        "status": status,
        "match": 1 if status == "MATCH" else 0,
        "drift": 0 if status == "MATCH" else 1,
        "checks": [{
            "artifact": "DomainFocusAdapterExperiment",
            "domain_count": artifact.get("domain_count"),
            "errors": errors,
            "negative_fixture_count": len(artifact.get("negative_fixtures", [])),
            "path": "schemas/domain-focus-adapter-experiment-pass-0072.json",
            "status": status,
        }],
    }


def main() -> None:
    result = validate()
    write_json(RESULT, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
