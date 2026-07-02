"""Validate pass 0117 theorem-prover adapter receipt."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "theorem-prover-adapter-receipt-pass-0117.json"
RESULT = ROOT / "schemas" / "pass-0117-theorem-prover-adapter-validator-result.json"


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)


def sha256_obj(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n", encoding="utf-8")


def branch(branches: list[dict], branch_id: str) -> dict:
    return next((row for row in branches if row.get("branch_id") == branch_id), {})


def validate() -> dict:
    artifact = read_json(ARTIFACT)
    unsealed = dict(artifact)
    seal = unsealed.pop("seal", None)
    targets = artifact.get("theorem_targets", [])
    branches = artifact.get("prover_branches", [])
    errors: list[str] = []

    if artifact.get("schema") != "TheoremProverAdapterReceipt/v1":
        errors.append("schema")
    if artifact.get("status") != "THEOREM_PROVER_ADAPTER_MATCH":
        errors.append("status")
    if seal != sha256_obj(unsealed):
        errors.append("seal")
    if artifact.get("source_bindings", {}).get("formal_physics_bridge_pass") != "0116":
        errors.append("bridge_pass")
    if any(artifact.get("availability", {}).get(exe, {}).get("status") != "MISSING" for exe in ["lean", "lake", "coqc", "isabelle", "agda"]):
        errors.append("availability")
    if {row.get("target_id") for row in targets} != {"left_identity", "right_identity", "associativity"}:
        errors.append("target_ids")
    if any(row.get("claim_status") != "FINITE_MODEL_VERIFIED" for row in targets):
        errors.append("target_status")
    if branch(branches, "python_finite_model_replay").get("status") != "MATCH":
        errors.append("python_replay")
    if branch(branches, "lean4_target").get("status") != "UNAVAILABLE_FENCED":
        errors.append("lean_fence")
    if any(row.get("status") not in {"MATCH", "UNAVAILABLE_FENCED"} for row in branches):
        errors.append("branch_status")
    if artifact.get("countermodel", {}).get("classification") != "BAD_IDENTITY_DRIFT" or artifact.get("countermodel", {}).get("status") != "MATCH":
        errors.append("countermodel")
    if artifact.get("source_surface", {}).get("anchor_count", 0) < 6:
        errors.append("source_surface")
    if any(row.get("status") != "MATCH" for row in artifact.get("flagship_receipts", {}).values()):
        errors.append("flagships")
    if artifact.get("unsupported_claim_count") != 0 or artifact.get("current_promoted_natural_laws") != []:
        errors.append("promotion_boundary")

    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0117TheoremProverAdapterValidatorRun/v1",
        "pass": "0117",
        "status": status,
        "match": 1 if status == "MATCH" else 0,
        "drift": 0 if status == "MATCH" else 1,
        "checks": [{
            "artifact": "TheoremProverAdapterReceipt",
            "branch_count": len(branches),
            "errors": errors,
            "path": "schemas/theorem-prover-adapter-receipt-pass-0117.json",
            "target_count": len(targets),
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
