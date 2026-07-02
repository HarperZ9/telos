"""Focused tests for pass 0137 SAIR-style proof-packet fixture."""
from __future__ import annotations

import importlib.util
from pathlib import Path

MODULE = Path(__file__).with_name("compose_sair_stage1_competition_proof_packet.py")
spec = importlib.util.spec_from_file_location("compose_sair_stage1", MODULE)
mod = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(mod)


def test_prompt_rendering() -> None:
    rendered = mod.render_prompt("A {{equation1}} B {{ equation2 }}", "x=y", "x*x=x")
    assert rendered == "A x=y B x*x=x"


def test_verdict_precedence() -> None:
    assert mod.extract_verdict("VERDICT: TRUE\n\\boxed{FALSE}")["verdict"] == "FALSE"
    assert mod.extract_verdict("VERDICT: FALSE\nVERDICT: TRUE")["verdict"] == "TRUE"
    assert mod.extract_verdict("Use VERDICT: TRUE or FALSE.\nVERDICT: FALSE")["verdict"] == "FALSE"
    assert mod.extract_verdict("reason\nTRUE")["method"] == "bare_edge_line"
    assert mod.extract_verdict("probably yes")["verdict"] is None


def test_composed_packet_gates() -> None:
    artifact = mod.compose()
    packet = artifact["competition_packet"]
    assert artifact["status"] == mod.STATUS_MATCH
    assert packet["positive_validation"]["status"] == "MATCH"
    assert packet["verdict_summary"]["attempts"] == 4
    assert packet["verdict_summary"]["correct"] == 4
    assert packet["verdict_summary"]["external_model_calls"] == 0
    assert all(row["status"] == "MATCH" for row in packet["negative_fixtures"])
    assert artifact["competition_packet"]["current_promoted_results"] == []


if __name__ == "__main__":
    test_prompt_rendering()
    test_verdict_precedence()
    test_composed_packet_gates()
