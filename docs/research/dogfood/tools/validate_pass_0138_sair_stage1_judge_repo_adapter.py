"""Validate pass 0138 SAIR Stage 1 judge repository adapter artifact."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "sair-stage1-judge-repo-adapter-pass-0138.json"


def main() -> None:
    artifact = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    packet = artifact["competition_packet"]
    receipts = packet["local_command_receipts"]
    checks = [
        ("schema", artifact["schema"] == "SAIRStage1JudgeRepoAdapterReceipt/v1"),
        ("status", artifact["status"] == "SAIR_STAGE1_JUDGE_REPO_ADAPTER_MATCH"),
        ("head_binding", packet["repository"]["head_commit"] == packet["repository"]["ls_remote_head"]),
        ("source_hashes", len(packet["repository"]["source_hashes"]) == len(packet["repository"]["observed_files"])),
        ("model_config", packet["model_config_summary"]["model_count"] == 3 and packet["model_config_summary"]["allow_fallbacks"] is False),
        ("pytest_receipt", receipts["pytest"]["status"] == "MATCH"),
        ("prompt_receipt", receipts["prompt_cli"]["status"] == "MATCH"),
        ("judge_receipt", receipts["judge_cli"]["status"] == "MATCH"),
        ("missing_key_boundary", receipts["missing_key_boundary"]["status"] == "MATCH" and receipts["missing_key_boundary"]["external_model_call_performed"] is False),
        ("no_external_calls", packet["execution_boundary"]["external_model_calls"] == 0),
        ("negative_fixtures", len(artifact["negative_fixtures"]) == 6 and all(row["status"] == "MATCH" for row in artifact["negative_fixtures"])),
        ("non_promotion", packet["current_promoted_results"] == []),
    ]
    failures = [name for name, ok in checks if not ok]
    result = {
        "schema": "Pass0138SAIRStage1JudgeRepoAdapterValidatorRun/v1",
        "pass": "0138",
        "status": "MATCH" if not failures else "DRIFT",
        "checks": [{"name": name, "status": "MATCH" if ok else "DRIFT"} for name, ok in checks],
        "failures": failures,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
