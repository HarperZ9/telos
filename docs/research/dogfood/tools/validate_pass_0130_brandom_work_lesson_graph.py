"""Validate pass 0130 Brandom work lesson graph."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "brandom-work-lesson-graph-pass-0130.json"
RESULT = ROOT / "schemas" / "pass-0130-brandom-work-lesson-graph-validator-result.json"


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
    sources = artifact.get("source_receipts", [])
    catalog = artifact.get("work_catalog", [])
    graph = artifact.get("lesson_graph", {})
    negatives = artifact.get("negative_fixtures", [])
    errors: list[str] = []

    require(artifact.get("schema") == "BrandomWorkLessonGraphReceipt/v1", errors, "schema")
    require(artifact.get("status") == "BRANDOM_WORK_LESSON_GRAPH_MATCH", errors, "status")
    require(seal == sha256_obj(unsealed), errors, "seal")
    require(artifact.get("source_bindings", {}).get("brandom_digest_pass") == "0129", errors, "brandom_digest_binding")
    require(len(sources) >= 5 and all(row.get("status") == "GATHER_VERIFIED" for row in sources), errors, "sources")
    require(all(row.get("raw_body_exported") is False for row in sources), errors, "raw_body_boundary")
    require(len(catalog) >= 5 and all(row.get("dominant_terms") for row in catalog), errors, "work_catalog")
    require(graph.get("status") == "MATCH", errors, "lesson_graph")
    require(all(node.get("source_refs") and node.get("exercise") for node in graph.get("nodes", [])), errors, "lesson_node_fields")
    require(artifact.get("learner_action_fixture", {}).get("status") == "MATCH", errors, "learner_action_fixture")
    require(len(negatives) >= 5 and all(row.get("status") == "REJECTED" for row in negatives), errors, "negative_fixtures")
    require(artifact.get("current_promoted_natural_laws") == [], errors, "natural_laws")
    require(all(row.get("status") == "MATCH" for row in artifact.get("flagship_receipts", {}).values()), errors, "flagships")

    status = "MATCH" if not errors else "DRIFT"
    return {"schema": "Pass0130BrandomWorkLessonGraphValidatorRun/v1", "pass": "0130", "status": status, "checks": [{"artifact": "BrandomWorkLessonGraph", "errors": errors, "status": status, "source_count": len(sources), "work_count": len(catalog)}]}


def main() -> None:
    result = validate()
    write_json(RESULT, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
