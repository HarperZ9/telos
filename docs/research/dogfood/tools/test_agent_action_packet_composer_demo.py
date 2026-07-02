"""Focused tests for the pass 0053 agent action packet composer."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_agent_action_proof_packet_demo.py"
FIXTURE = ROOT / "fixtures" / "agent-action-proof-packet-negative-fixtures-pass-0051.json"
EXPECTED_OUTPUTS = [
    "packet.json",
    "packet.md",
    "receipts.json",
    "negative-fixture-report.json",
    "index.html",
    "replay-commands.md",
]


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="telos-agent-action-packet-") as tmp:
        out_dir = Path(tmp)
        command = [
            sys.executable,
            str(COMPOSER),
            "--fixture",
            str(FIXTURE),
            "--out",
            str(out_dir),
        ]
        result = subprocess.run(command, cwd=REPO, capture_output=True, text=True)
        assert_true(result.returncode == 0, result.stderr or result.stdout)
        for rel_path in EXPECTED_OUTPUTS:
            assert_true((out_dir / rel_path).exists(), f"missing output: {rel_path}")
        packet = json.loads((out_dir / "packet.json").read_text(encoding="utf-8"))
        negative = json.loads((out_dir / "negative-fixture-report.json").read_text(encoding="utf-8"))
        receipts = json.loads((out_dir / "receipts.json").read_text(encoding="utf-8"))
    assert_true(packet["schema"] == "project-telos.agent-action-proof-packet.bundle/v1", "bad packet schema")
    assert_true(packet["verification"]["verdict"] == "MATCH", "positive packet did not match")
    assert_true(packet["redaction_status"]["raw_private_payloads_included"] is False, "raw payload boundary failed")
    assert_true(negative["negative_fixture_count"] == 8, "negative fixture count mismatch")
    assert_true(negative["negative_match_count"] == 8, "negative fixtures did not fail as expected")
    assert_true(negative["negative_pass_observed_count"] == 0, "a negative fixture passed")
    assert_true(receipts["status"] == "MATCH", "receipt set did not match")
    print("PASS composer demo outputs verified")


if __name__ == "__main__":
    main()
