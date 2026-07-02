"""Validate pass 0067 Forum routing repair experiment."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "forum-routing-repair-experiment-pass-0067.json"
RESULT = ROOT / "schemas" / "pass-0067-forum-routing-repair-experiment-validator-result.json"


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
    probes = artifact.get("route_probes", [])
    metrics = artifact.get("repair_metrics", {})
    if artifact.get("schema") != "ForumRoutingRepairExperiment/v1":
        errors.append("schema")
    if artifact.get("status") != "FORUM_ROUTING_REPAIR_EXPERIMENT_MATCH":
        errors.append("status")
    if seal != sha256_obj(unsealed):
        errors.append("seal")
    if len(probes) != 3:
        errors.append("probe_count")
    if probes and probes[0].get("needs_escalation") is not True:
        errors.append("baseline_expected_failure")
    if metrics.get("repaired_no_escalation_count") != 2:
        errors.append("repair_count")
    if metrics.get("routing_repair_status") != "MATCH":
        errors.append("repair_status")
    if metrics.get("best_repaired_project_telos_score", 0) <= metrics.get("baseline_project_telos_score", 1):
        errors.append("score_lift")
    if artifact.get("previous_pass_binding", {}).get("pass") != "0066":
        errors.append("previous_pass_binding")
    if artifact.get("unsupported_claim_count") != 0:
        errors.append("unsupported_claim_count")
    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0067ForumRoutingRepairExperimentValidatorRun/v1",
        "pass": "0067",
        "status": status,
        "match": 1 if status == "MATCH" else 0,
        "drift": 0 if status == "MATCH" else 1,
        "checks": [
            {
                "artifact": "ForumRoutingRepairExperiment",
                "errors": errors,
                "path": "schemas/forum-routing-repair-experiment-pass-0067.json",
                "probe_count": len(probes),
                "repaired_no_escalation_count": metrics.get("repaired_no_escalation_count"),
                "score_lift": metrics.get("project_telos_score_lift"),
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
