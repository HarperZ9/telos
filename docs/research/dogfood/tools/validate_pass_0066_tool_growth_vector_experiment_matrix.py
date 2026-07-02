"""Validate pass 0066 tool growth-vector experiment matrix."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "tool-growth-vector-experiment-matrix-pass-0066.json"
RESULT = ROOT / "schemas" / "pass-0066-tool-growth-vector-experiment-matrix-validator-result.json"
REQUIRED_TOOLS = {"Gather", "Index", "Forum", "Crucible", "Telos", "BuildLang/buildc", "build-universe", "color calibration", "browser evidence", "model foundry", "loop ledger", "action receipts"}


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
    tools = {tool.get("tool") for tool in artifact.get("internal_tools", [])}
    centrality = artifact.get("synergy_graph", {}).get("centrality", {})
    if artifact.get("schema") != "ToolGrowthVectorExperimentMatrix/v1":
        errors.append("schema")
    if artifact.get("status") != "TOOL_GROWTH_VECTOR_EXPERIMENT_MATRIX_MATCH":
        errors.append("status")
    if seal != sha256_obj(unsealed):
        errors.append("seal")
    if tools != REQUIRED_TOOLS:
        errors.append("tool_set")
    if len(artifact.get("source_anchors", [])) < 12:
        errors.append("source_anchor_count")
    if len(artifact.get("growth_vectors", [])) < 36:
        errors.append("growth_vector_count")
    if len(artifact.get("cross_tool_experiments", [])) < 10:
        errors.append("cross_tool_experiment_count")
    if centrality.get("Telos", 0) < 6 or centrality.get("Crucible", 0) < 6:
        errors.append("centrality")
    if artifact.get("top_growth_bundles", [{}])[0].get("bundle_id") != "proof_os_core":
        errors.append("top_bundle")
    if artifact.get("previous_pass_binding", {}).get("pass") != "0065":
        errors.append("previous_pass_binding")
    if artifact.get("unsupported_claim_count") != 0:
        errors.append("unsupported_claim_count")
    for row in artifact.get("growth_vectors", []):
        if row.get("tool") not in REQUIRED_TOOLS:
            errors.append(f"tool:{row.get('experiment_id')}")
        if not set(row.get("source_ids", [])).issubset(source_ids):
            errors.append(f"sources:{row.get('experiment_id')}")
        if row.get("claim_status") != "hypothesis":
            errors.append(f"claim_status:{row.get('experiment_id')}")
    status = "MATCH" if not errors else "DRIFT"
    return {
        "schema": "Pass0066ToolGrowthVectorExperimentMatrixValidatorRun/v1",
        "pass": "0066",
        "status": status,
        "match": 1 if status == "MATCH" else 0,
        "drift": 0 if status == "MATCH" else 1,
        "checks": [
            {
                "artifact": "ToolGrowthVectorExperimentMatrix",
                "cross_tool_experiment_count": len(artifact.get("cross_tool_experiments", [])),
                "errors": errors,
                "growth_vector_count": len(artifact.get("growth_vectors", [])),
                "path": "schemas/tool-growth-vector-experiment-matrix-pass-0066.json",
                "source_anchor_count": len(artifact.get("source_anchors", [])),
                "status": status,
                "top_bundle": artifact.get("top_growth_bundles", [{}])[0].get("bundle_id"),
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
