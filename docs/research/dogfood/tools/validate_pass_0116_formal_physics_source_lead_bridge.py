"""Validate pass 0116 formal/physics source-lead bridge."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "formal-physics-source-lead-bridge-pass-0116.json"
RESULT = ROOT / "schemas" / "pass-0116-formal-physics-source-lead-bridge-validator-result.json"


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)


def sha256_obj(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n", encoding="utf-8")


def case(cases: list[dict], case_id: str) -> dict:
    return next((row for row in cases if row.get("case_id") == case_id), {})


def validate() -> dict:
    artifact = read_json(ARTIFACT)
    unsealed = dict(artifact)
    seal = unsealed.pop("seal", None)
    cases = artifact.get("bridge_cases", [])
    category = case(cases, "category_set_identity_associativity")
    born = case(cases, "born_rule_normalization_toy")
    counterexample = case(cases, "counterexample_revision_toy")
    loop = case(cases, "loop_replay_receipt_toy")
    errors: list[str] = []

    if artifact.get("schema") != "FormalPhysicsSourceLeadBridgeReceipt/v1":
        errors.append("schema")
    if artifact.get("status") != "FORMAL_PHYSICS_SOURCE_LEAD_BRIDGE_MATCH":
        errors.append("status")
    if seal != sha256_obj(unsealed):
        errors.append("seal")
    if artifact.get("source_bindings", {}).get("solver_replay_pass") != "0115":
        errors.append("solver_replay_pass")
    if artifact.get("source_bindings", {}).get("youtube_roadmap_pass") != "0102":
        errors.append("youtube_roadmap_pass")
    if artifact.get("source_bindings", {}).get("new_youtube_lead_count") != 4:
        errors.append("youtube_lead_count")
    if len(cases) != 4 or any(row.get("status") != "MATCH" for row in cases):
        errors.append("cases")
    if category.get("checks") != {"left_identity": True, "right_identity": True, "associativity": True}:
        errors.append("category")
    if category.get("negative_fixture", {}).get("classification") != "BAD_IDENTITY_DRIFT":
        errors.append("category_negative")
    if born.get("probability_sum") != "1" or born.get("negative_fixture", {}).get("classification") != "NON_NORMALIZED_STATE_REJECTED":
        errors.append("born")
    if counterexample.get("initial_claim_status") != "REFUTED_BY_COUNTEREXAMPLE" or counterexample.get("revised_claim_status") != "MATCH":
        errors.append("counterexample")
    if loop.get("final_status") != "MATCH" or loop.get("reasoning_trace_exposed") is not False:
        errors.append("loop")
    if artifact.get("source_surface", {}).get("anchor_count", 0) < 12:
        errors.append("source_surface")
    if len(artifact.get("roadmap_requirements", [])) != 4:
        errors.append("roadmap_requirements")
    if any(row.get("claim_status") != "HYPOTHESIS" for row in artifact.get("roadmap_requirements", [])):
        errors.append("roadmap_status")
    if any(row.get("status") != "MATCH" for row in artifact.get("flagship_receipts", {}).values()):
        errors.append("flagships")
    if artifact.get("unsupported_claim_count") != 0 or artifact.get("current_promoted_natural_laws") != []:
        errors.append("promotion_boundary")

    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0116FormalPhysicsSourceLeadBridgeValidatorRun/v1",
        "pass": "0116",
        "status": status,
        "match": 1 if status == "MATCH" else 0,
        "drift": 0 if status == "MATCH" else 1,
        "checks": [{
            "artifact": "FormalPhysicsSourceLeadBridgeReceipt",
            "case_count": len(cases),
            "errors": errors,
            "path": "schemas/formal-physics-source-lead-bridge-pass-0116.json",
            "source_anchor_count": artifact.get("source_surface", {}).get("anchor_count"),
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
