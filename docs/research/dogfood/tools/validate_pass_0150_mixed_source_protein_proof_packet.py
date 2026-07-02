"""Validate pass 0150 mixed-source protein proof packet artifact."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "schemas" / "mixed-source-protein-proof-packet-pass-0150.json"


def check(name: str, ok: bool) -> dict[str, str]:
    return {"name": name, "status": "MATCH" if ok else "DRIFT"}


def main() -> int:
    artifact = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    summary = artifact["summary"]
    computations = artifact["computations"]
    checks = [
        check("schema", artifact["schema"] == "MixedSourceProteinProofPacket/v1"),
        check("status", artifact["status"] == "MIXED_SOURCE_PROTEIN_PROOF_PACKET_MATCH_WITH_WARNINGS"),
        check("sources", summary["sources"] == 5),
        check("gather_verified_sources", summary["gather_verified_sources"] == 5),
        check("verification_checks", summary["checks_match"] == summary["checks"] == 7),
        check("warnings", summary["warnings"] == 3),
        check("negative_fixtures", summary["negative_fixtures"] == 12),
        check("accession", artifact["target"]["accession"] == computations["accession"] == "P69905"),
        check("sequence_length", computations["sequence_length"] == 142),
        check("rcsb_mature_chain_length", computations["rcsb_sequence_length"] == 141),
        check("literature_join", computations["pubmed_id_from_uniprot_refs"] is True),
        check("no_designs", artifact["current_promoted_designs"] == []),
        check("no_clinical_claims", artifact["current_promoted_clinical_claims"] == []),
        check("no_biological_discoveries", artifact["current_promoted_biological_discoveries"] == []),
        check("tool_receipts", len(artifact["tool_receipts"]) == 5 and all(row["status"] == "MATCH" for row in artifact["tool_receipts"].values())),
        check("seal_present", len(artifact.get("seal", "")) == 64),
    ]
    failures = [row for row in checks if row["status"] != "MATCH"]
    print(json.dumps({"schema": "Pass0150MixedSourceProteinProofPacketValidatorRun/v1", "pass": "0150", "status": "MATCH" if not failures else "DRIFT", "checks": checks, "failures": failures}, indent=2, sort_keys=True))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
