"""Validate pass 0131 tradition derivation atlas."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "tradition-derivation-atlas-pass-0131.json"
RESULT = ROOT / "schemas" / "pass-0131-tradition-derivation-atlas-validator-result.json"


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
    nodes = artifact.get("atlas_nodes", [])
    edges = artifact.get("atlas_edges", [])
    negatives = artifact.get("negative_fixtures", [])
    node_ids = {node.get("id") for node in nodes}
    errors: list[str] = []

    require(artifact.get("schema") == "TraditionDerivationAtlasReceipt/v1", errors, "schema")
    require(artifact.get("status") == "TRADITION_DERIVATION_ATLAS_MATCH", errors, "status")
    require(seal == sha256_obj(unsealed), errors, "seal")
    require(artifact.get("source_bindings", {}).get("brandom_work_graph_pass") == "0130", errors, "upstream_binding")
    require(len(sources) >= 10 and all(row.get("status") == "GATHER_VERIFIED" for row in sources), errors, "sources")
    require(all(row.get("raw_body_exported") is False for row in sources), errors, "raw_body_boundary")
    require(len(nodes) >= 10 and all(node.get("dominant_terms") for node in nodes), errors, "nodes")
    require(len(edges) >= 12 and all(edge.get("from") in node_ids and edge.get("to") in node_ids for edge in edges), errors, "edges_resolve")
    require(all(edge.get("status") == "HYPOTHESIS_SOURCE_BACKED" and len(edge.get("source_refs", [])) >= 2 for edge in edges), errors, "edge_boundaries")
    require(len(artifact.get("learning_modules", [])) >= 5, errors, "learning_modules")
    require(len(negatives) >= 6 and all(row.get("status") == "REJECTED" for row in negatives), errors, "negative_fixtures")
    require(artifact.get("current_promoted_natural_laws") == [], errors, "natural_laws")
    require(all(row.get("status") == "MATCH" for row in artifact.get("flagship_receipts", {}).values()), errors, "flagships")

    status = "MATCH" if not errors else "DRIFT"
    return {"schema": "Pass0131TraditionDerivationAtlasValidatorRun/v1", "pass": "0131", "status": status, "checks": [{"artifact": "TraditionDerivationAtlas", "errors": errors, "status": status, "source_count": len(sources), "node_count": len(nodes), "edge_count": len(edges)}]}


def main() -> None:
    result = validate()
    write_json(RESULT, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
