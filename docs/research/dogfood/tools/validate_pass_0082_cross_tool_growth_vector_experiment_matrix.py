"""Validate pass 0082 cross-tool growth-vector experiment matrix."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "cross-tool-growth-vector-experiment-matrix-pass-0082.json"
RESULT = ROOT / "schemas" / "pass-0082-cross-tool-growth-vector-experiment-matrix-validator-result.json"
TOOLS = {
    "Gather",
    "Index",
    "Forum",
    "Crucible",
    "Telos",
    "BuildLang/buildc",
    "build-universe",
    "color calibration",
    "browser evidence",
    "model foundry",
    "loop ledger",
    "action receipts",
}


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)


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
    tool_set = {row.get("tool") for row in artifact.get("tool_improvements", [])}
    if artifact.get("schema") != "CrossToolGrowthVectorExperimentMatrix/v1":
        errors.append("schema")
    if artifact.get("status") != "CROSS_TOOL_GROWTH_VECTOR_EXPERIMENT_MATRIX_MATCH":
        errors.append("status")
    if seal != sha256_obj(unsealed):
        errors.append("seal")
    if len(artifact.get("live_forum_routes", [])) < 8:
        errors.append("forum_route_count")
    if any(route.get("status") != "MATCH" for route in artifact.get("live_forum_routes", [])):
        errors.append("forum_route_status")
    if len(artifact.get("ranked_product_lanes", [])) < 8:
        errors.append("ranked_product_lanes")
    if tool_set != TOOLS:
        errors.append("tool_set")
    if artifact.get("unsupported_claim_count") != 0 or artifact.get("current_promoted_natural_laws") != []:
        errors.append("promotion_boundary")
    if len(artifact.get("negative_fixtures", [])) < 8:
        errors.append("negative_fixtures")
    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0082CrossToolGrowthVectorExperimentMatrixValidatorRun/v1",
        "pass": "0082",
        "status": status,
        "match": 1 if status == "MATCH" else 0,
        "drift": 0 if status == "MATCH" else 1,
        "checks": [{
            "artifact": "CrossToolGrowthVectorExperimentMatrix",
            "errors": errors,
            "path": "schemas/cross-tool-growth-vector-experiment-matrix-pass-0082.json",
            "route_probe_count": len(artifact.get("live_forum_routes", [])),
            "product_lane_count": len(artifact.get("ranked_product_lanes", [])),
            "tool_improvement_count": len(artifact.get("tool_improvements", [])),
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
