"""Focused tests for pass 0139 SAIR Stage 2 Lean certificate preflight."""
from __future__ import annotations

import importlib.util
from pathlib import Path

MODULE = Path(__file__).with_name("compose_sair_stage2_lean_certificate_preflight.py")
spec = importlib.util.spec_from_file_location("compose_sair_stage2_lean_preflight", MODULE)
mod = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(mod)


def test_checkout_contract_and_counts() -> None:
    mod.ensure_checkout()
    assert (mod.CHECKOUT / "lean-toolchain").exists()
    counts = mod.repo_counts()
    assert counts["lean_files"] >= 4
    assert counts["python_files"] >= 10
    assert mod.manifest_counts()["harness_manifest"] >= 10


def test_toolchain_boundary_and_compileall() -> None:
    receipts = mod.toolchain_receipts()
    assert receipts["python_compileall"]["status"] == "MATCH"
    assert receipts["run_harness"]["status"] in {"MATCH", "UNVERIFIABLE_TOOL_UNAVAILABLE"}
    assert receipts["lean"]["status"] in {"MATCH", "UNVERIFIABLE_TOOL_UNAVAILABLE"}


def test_composed_packet_gates() -> None:
    artifact = mod.compose()
    packet = artifact["certificate_packet"]
    assert artifact["status"] == mod.STATUS_MATCH
    assert packet["repository"]["head_commit"] == packet["repository"]["ls_remote_head"]
    assert len(packet["repository"]["source_hashes"]) == len(mod.OBSERVED_FILES)
    assert packet["proof_replay"]["lean_replay_status"] == "UNVERIFIABLE_TOOL_UNAVAILABLE"
    assert all(row["status"] == "MATCH" for row in artifact["negative_fixtures"])
    assert packet["current_promoted_results"] == []


if __name__ == "__main__":
    test_checkout_contract_and_counts()
    test_toolchain_boundary_and_compileall()
    test_composed_packet_gates()
