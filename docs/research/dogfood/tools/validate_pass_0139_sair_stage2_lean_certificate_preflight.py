"""Validate pass 0139 SAIR Stage 2 Lean certificate preflight artifact."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "sair-stage2-lean-certificate-preflight-pass-0139.json"


def main() -> None:
    artifact = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    packet = artifact["certificate_packet"]
    receipts = packet["local_command_receipts"]
    checks = [
        ("schema", artifact["schema"] == "SAIRStage2LeanCertificatePreflightReceipt/v1"),
        ("status", artifact["status"] == "SAIR_STAGE2_LEAN_CERTIFICATE_PREFLIGHT_MATCH_WITH_TOOLCHAIN_GAP"),
        ("head_binding", packet["repository"]["head_commit"] == packet["repository"]["ls_remote_head"]),
        ("source_hashes", len(packet["repository"]["source_hashes"]) == len(packet["repository"]["observed_files"])),
        ("lean_toolchain", packet["toolchain"]["lean_toolchain"].startswith("leanprover/lean4:")),
        ("python_compileall", receipts["python_compileall"]["status"] == "MATCH"),
        ("lean_unavailable_boundary", packet["proof_replay"]["lean_replay_status"] == "UNVERIFIABLE_TOOL_UNAVAILABLE"),
        ("harness_boundary", receipts["run_harness"]["status"] == "UNVERIFIABLE_TOOL_UNAVAILABLE"),
        ("manifest_counts", packet["repository"]["manifest_counts"]["harness_manifest"] >= 10),
        ("negative_fixtures", len(artifact["negative_fixtures"]) == 6 and all(row["status"] == "MATCH" for row in artifact["negative_fixtures"])),
        ("non_promotion", packet["current_promoted_results"] == []),
    ]
    failures = [name for name, ok in checks if not ok]
    result = {
        "schema": "Pass0139SAIRStage2LeanCertificatePreflightValidatorRun/v1",
        "pass": "0139",
        "status": "MATCH" if not failures else "DRIFT",
        "checks": [{"name": name, "status": "MATCH" if ok else "DRIFT"} for name, ok in checks],
        "failures": failures,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
