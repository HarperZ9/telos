"""Validate pass 0137 SAIR-style CompetitionProofPacket artifact."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "sair-stage1-competition-proof-packet-pass-0137.json"


def main() -> None:
    artifact = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    packet = artifact["competition_packet"]
    checks = []
    checks.append(("schema", artifact["schema"] == "CompetitionProofPacketFixtureReceipt/v1"))
    checks.append(("status", artifact["status"] == "COMPETITION_PROOF_PACKET_FIXTURE_MATCH"))
    checks.append(("source_refs", len(packet["source_refs"]) >= 4))
    checks.append(("attempts", packet["verdict_summary"]["attempts"] == 4))
    checks.append(("correct", packet["verdict_summary"]["correct"] == 4))
    checks.append(("no_external_model_calls", packet["verdict_summary"]["external_model_calls"] == 0))
    checks.append(("negative_fixtures", len(packet["negative_fixtures"]) == 6 and all(row["status"] == "MATCH" for row in packet["negative_fixtures"])))
    checks.append(("parser_tests", len(artifact["parser_tests"]) == 5 and all(row["status"] == "MATCH" for row in artifact["parser_tests"])))
    checks.append(("non_promotion", packet["current_promoted_results"] == []))
    failures = [name for name, ok in checks if not ok]
    result = {
        "schema": "Pass0137CompetitionProofPacketValidatorRun/v1",
        "pass": "0137",
        "status": "MATCH" if not failures else "DRIFT",
        "checks": [{"name": name, "status": "MATCH" if ok else "DRIFT"} for name, ok in checks],
        "failures": failures,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
