"""Focused tests for pass 0138 SAIR Stage 1 judge repository adapter."""
from __future__ import annotations

import importlib.util
from pathlib import Path

MODULE = Path(__file__).with_name("compose_sair_stage1_judge_repo_adapter.py")
spec = importlib.util.spec_from_file_location("compose_sair_stage1_judge_repo_adapter", MODULE)
mod = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(mod)


def test_checkout_and_model_config() -> None:
    mod.ensure_checkout()
    summary = mod.model_summary()
    assert summary["model_count"] == 3
    assert summary["allow_fallbacks"] is False
    assert summary["max_output_tokens_cap"] == 8192
    assert "gpt-oss-120b" in summary["model_aliases"]


def test_local_commands_respect_no_secret_boundary() -> None:
    receipts = mod.command_receipts()
    assert receipts["pytest"]["status"] == "MATCH"
    assert receipts["prompt_cli"]["status"] == "MATCH"
    assert receipts["judge_cli"]["status"] == "MATCH"
    assert receipts["missing_key_boundary"]["status"] == "MATCH"
    assert receipts["missing_key_boundary"]["external_model_call_performed"] is False


def test_composed_packet_gates() -> None:
    artifact = mod.compose()
    packet = artifact["competition_packet"]
    assert artifact["status"] == mod.STATUS_MATCH
    assert packet["execution_boundary"]["external_model_calls"] == 0
    assert packet["repository"]["head_commit"] == packet["repository"]["ls_remote_head"]
    assert len(packet["repository"]["source_hashes"]) == len(mod.OBSERVED_FILES)
    assert artifact["positive_validation"]["status"] == "MATCH"
    assert all(row["status"] == "MATCH" for row in artifact["negative_fixtures"])
    assert packet["current_promoted_results"] == []


if __name__ == "__main__":
    test_checkout_and_model_config()
    test_local_commands_respect_no_secret_boundary()
    test_composed_packet_gates()
