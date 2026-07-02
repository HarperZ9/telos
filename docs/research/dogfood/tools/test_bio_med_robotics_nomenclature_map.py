"""Focused tests for pass 0135 biology/medicine/robotics nomenclature map."""
from __future__ import annotations

from compose_bio_med_robotics_nomenclature_map import compose


def main() -> None:
    artifact = compose()
    assert artifact["schema"] == "BioMedRoboticsNomenclatureMapReceipt/v1"
    assert artifact["status"] == "BIO_MED_ROBOTICS_NOMENCLATURE_MAP_MATCH"
    assert artifact["gather_summary"]["source_count"] >= 30
    assert artifact["gather_summary"]["usable_source_count"] >= 25
    assert artifact["gather_summary"]["client_challenge_count"] >= 3
    assert artifact["gather_summary"]["empty_capture_count"] >= 1
    assert len(artifact["archive_substrate_catalog"]) >= 12
    assert len(artifact["domain_expansion_queue"]) >= 12
    assert len(artifact["domain_lanes"]) >= 8
    assert len(artifact["terminology_bridges"]) >= 8
    assert all(row["status"] == "HYPOTHESIS_SOURCE_MAP" for row in artifact["domain_lanes"])
    assert all(row["status"] == "REJECTED" for row in artifact["negative_fixtures"])
    assert artifact["current_promoted_natural_laws"] == []
    assert artifact["unsupported_claim_count"] == 0


if __name__ == "__main__":
    main()
