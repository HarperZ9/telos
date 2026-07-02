"""Focused tests for pass 0150 mixed-source protein proof packet."""
from __future__ import annotations

from compose_mixed_source_protein_proof_packet import build_receipt


def test_source_receipts_and_identity_checks() -> None:
    receipt = build_receipt(live_tools=False)
    assert receipt["schema"] == "MixedSourceProteinProofPacket/v1"
    assert receipt["summary"]["sources"] == 5
    assert receipt["summary"]["gather_verified_sources"] == 5
    assert receipt["target"]["accession"] == "P69905"
    assert receipt["computations"]["uniprot_id"] == "HBA_HUMAN"


def test_sequence_and_structure_boundaries() -> None:
    receipt = build_receipt(live_tools=False)
    assert receipt["computations"]["sequence_length"] == 142
    assert receipt["computations"]["sequence_alphabet_ok"] is True
    assert receipt["computations"]["rcsb_sequence_length"] == 141
    assert any(row["name"] == "rcsb_mature_chain_matches_uniprot_positions_2_142" and row["status"] == "MATCH" for row in receipt["verification_checks"])
    assert any("mature_chain" in row for row in receipt["warnings"])


def test_literature_join_and_no_promotion() -> None:
    receipt = build_receipt(live_tools=False)
    assert receipt["computations"]["pubmed_id_from_uniprot_refs"] is True
    assert receipt["summary"]["checks_match"] == receipt["summary"]["checks"]
    assert len(receipt["negative_fixtures"]) == 12
    assert receipt["current_promoted_biological_discoveries"] == []
    assert receipt["current_promoted_clinical_claims"] == []


if __name__ == "__main__":
    test_source_receipts_and_identity_checks()
    test_sequence_and_structure_boundaries()
    test_literature_join_and_no_promotion()
