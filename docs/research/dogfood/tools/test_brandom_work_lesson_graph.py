"""Focused tests for pass 0130 Brandom work lesson graph."""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "tools" / "compose_brandom_work_lesson_graph.py"


def load_module():
    spec = importlib.util.spec_from_file_location("compose_brandom_work_lesson_graph", MODULE)
    if spec is None or spec.loader is None:
        raise AssertionError("module spec unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_brandom_work_lesson_graph() -> None:
    module = load_module()
    artifact = module.compose()
    graph = artifact["lesson_graph"]

    assert artifact["schema"] == "BrandomWorkLessonGraphReceipt/v1"
    assert artifact["status"] == "BRANDOM_WORK_LESSON_GRAPH_MATCH"
    assert artifact["source_bindings"]["brandom_digest_pass"] == "0129"
    assert len(artifact["source_receipts"]) >= 5
    assert len(artifact["work_catalog"]) >= 5
    assert all(row["raw_body_exported"] is False for row in artifact["source_receipts"])
    assert graph["status"] == "MATCH"
    assert len(graph["nodes"]) >= 6
    assert all(node["source_refs"] and node["exercise"] for node in graph["nodes"])
    assert artifact["learner_action_fixture"]["status"] == "MATCH"
    assert all(row["status"] == "REJECTED" for row in artifact["negative_fixtures"])
    assert artifact["current_promoted_natural_laws"] == []


if __name__ == "__main__":
    test_brandom_work_lesson_graph()
