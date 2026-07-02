"""Validate pass 0068 multi-tool growth-vector steelman."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "multitool-growth-vector-steelman-pass-0068.json"
RESULT = ROOT / "schemas" / "pass-0068-multitool-growth-vector-steelman-validator-result.json"
REQUIRED_TOOLS = {
    "Gather", "Index", "Forum", "Crucible", "Telos", "BuildLang/buildc",
    "build-universe", "color calibration", "browser evidence", "model foundry",
    "loop ledger", "action receipts",
}


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
    source_ids = {source.get("source_id") for source in artifact.get("source_anchors", [])}
    tools = {row.get("tool") for row in artifact.get("tool_rows", [])}
    if artifact.get("schema") != "MultiToolGrowthVectorSteelman/v1":
        errors.append("schema")
    if artifact.get("status") != "MULTITOOL_GROWTH_VECTOR_STEELMAN_MATCH":
        errors.append("status")
    if seal != sha256_obj(unsealed):
        errors.append("seal")
    if tools != REQUIRED_TOOLS:
        errors.append("tool_set")
    if len(artifact.get("source_anchors", [])) < 16:
        errors.append("source_anchor_count")
    if len(artifact.get("synergy_edges", [])) < 15:
        errors.append("synergy_edge_count")
    if len(artifact.get("steelman_objections", [])) < 8:
        errors.append("steelman_objection_count")
    if len(artifact.get("experiment_queue", [])) < 12:
        errors.append("experiment_queue_count")
    if {row.get("pass") for row in artifact.get("previous_pass_bindings", [])} != {"0066", "0067"}:
        errors.append("previous_pass_bindings")
    if artifact.get("unsupported_claim_count") != 0:
        errors.append("unsupported_claim_count")
    for row in artifact.get("tool_rows", []):
        if row.get("claim_status") != "hypothesis" or row.get("gap_status") != "inferred":
            errors.append(f"claim_boundary:{row.get('tool')}")
        if not set(row.get("source_ids", [])).issubset(source_ids):
            errors.append(f"sources:{row.get('tool')}")
        if not row.get("falsifier") or not row.get("success_metric") or not row.get("integration_target"):
            errors.append(f"experiment_contract:{row.get('tool')}")
        if not 1 <= row.get("scores", {}).get("priority", 0) <= 5:
            errors.append(f"priority:{row.get('tool')}")
    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0068MultiToolGrowthVectorSteelmanValidatorRun/v1",
        "pass": "0068",
        "status": status,
        "match": 1 if status == "MATCH" else 0,
        "drift": 0 if status == "MATCH" else 1,
        "checks": [{
            "artifact": "MultiToolGrowthVectorSteelman",
            "errors": errors,
            "experiment_queue_count": len(artifact.get("experiment_queue", [])),
            "path": "schemas/multitool-growth-vector-steelman-pass-0068.json",
            "source_anchor_count": len(artifact.get("source_anchors", [])),
            "status": status,
            "synergy_edge_count": len(artifact.get("synergy_edges", [])),
            "tool_count": len(artifact.get("tool_rows", [])),
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
