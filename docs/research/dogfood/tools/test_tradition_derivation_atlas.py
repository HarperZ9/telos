"""Focused tests for pass 0131 tradition derivation atlas."""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "tools" / "compose_tradition_derivation_atlas.py"


def load_module():
    spec = importlib.util.spec_from_file_location("compose_tradition_derivation_atlas", MODULE)
    if spec is None or spec.loader is None:
        raise AssertionError("module spec unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_tradition_derivation_atlas() -> None:
    module = load_module()
    artifact = module.compose()
    node_ids = {node["id"] for node in artifact["atlas_nodes"]}

    assert artifact["schema"] == "TraditionDerivationAtlasReceipt/v1"
    assert artifact["status"] == "TRADITION_DERIVATION_ATLAS_MATCH"
    assert artifact["source_bindings"]["brandom_work_graph_pass"] == "0130"
    assert len(artifact["source_receipts"]) >= 10
    assert all(row["raw_body_exported"] is False for row in artifact["source_receipts"])
    assert len(artifact["atlas_nodes"]) >= 10
    assert {"sellars", "kant", "hegel", "brandom"}.issubset(node_ids)
    assert len(artifact["atlas_edges"]) >= 12
    assert all(edge["from"] in node_ids and edge["to"] in node_ids for edge in artifact["atlas_edges"])
    assert all(edge["status"] == "HYPOTHESIS_SOURCE_BACKED" for edge in artifact["atlas_edges"])
    assert len(artifact["learning_modules"]) >= 5
    assert all(row["status"] == "REJECTED" for row in artifact["negative_fixtures"])
    assert artifact["current_promoted_natural_laws"] == []


if __name__ == "__main__":
    test_tradition_derivation_atlas()
