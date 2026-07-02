"""Focused tests for pass 0134 all-video author/theory index."""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "tools" / "compose_all_video_author_theory_index.py"


def load_module():
    spec = importlib.util.spec_from_file_location("compose_all_video_author_theory_index", MODULE)
    if spec is None or spec.loader is None:
        raise AssertionError("module spec unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_all_video_author_theory_index() -> None:
    module = load_module()
    artifact = module.compose()
    lanes = {row["lane_id"] for row in artifact["theory_lanes"]}
    authors = {row["name"] for row in artifact["author_nodes"]}
    videos = {row["video_id"] for row in artifact["video_sources"]}

    assert artifact["schema"] == "AllVideoAuthorTheoryIndexReceipt/v1"
    assert artifact["status"] == "ALL_VIDEO_AUTHOR_THEORY_INDEX_MATCH"
    assert len(videos) >= 50
    assert len(authors) >= 20
    assert "brandom_functional_learning" in lanes
    assert "quantum_optimization" in lanes
    assert "rendering_compute_kernels" in lanes
    assert "Robert Brandom" in authors
    assert "Inigo Quilez" in authors
    assert "EdVG5qNm2rY" in videos
    assert all(row["claim_status"] == "SOURCE_LEAD_ONLY" for row in artifact["video_sources"])
    assert all(row["status"] == "REJECTED" for row in artifact["negative_fixtures"])
    assert artifact["current_promoted_natural_laws"] == []


if __name__ == "__main__":
    test_all_video_author_theory_index()
