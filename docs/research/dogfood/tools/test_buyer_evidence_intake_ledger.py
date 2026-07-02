"""Behavior test for pass 0061 buyer evidence intake ledger."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_buyer_evidence_intake_ledger.py"
OUTREACH = ROOT / "schemas" / "buyer-outreach-packets-pass-0060.json"


def test_buyer_evidence_intake_ledger_preserves_privacy_and_open_status() -> None:
    with tempfile.TemporaryDirectory(prefix="telos-pass-0061-") as tmp:
        out_path = Path(tmp) / "intake-ledger.json"
        result = subprocess.run(
            [sys.executable, str(COMPOSER), "--outreach", str(OUTREACH), "--out", str(out_path)],
            cwd=REPO,
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0, result.stderr or result.stdout
        ledger = json.loads(out_path.read_text(encoding="utf-8"))

    buyer_ids = {row["buyer_id"] for row in ledger["intake_records"]}
    evidence_fields = sum(len(row["evidence_capture_fields"]) for row in ledger["intake_records"])
    private_field_count = sum(len(row["private_fields_forbidden_in_model_context"]) for row in ledger["intake_records"])

    assert ledger["schema"] == "BuyerEvidenceIntakeLedger/v1"
    assert ledger["pass"] == "0061"
    assert ledger["status"] == "BUYER_EVIDENCE_INTAKE_LEDGER_MATCH"
    assert ledger["buyer_response_status"] == "AWAITING_REAL_RESPONSES"
    assert ledger["crm_write_status"] == "NOT_WRITTEN"
    assert ledger["send_status"] == "NOT_SENT"
    assert ledger["market_claim_boundary"] == "HYPOTHESIS_ONLY"
    assert ledger["unsupported_claim_count"] == 0
    assert ledger["current_promoted_natural_laws"] == []
    assert ledger["upstream_outreach"]["status"] == "BUYER_OUTREACH_PACKETS_MATCH"
    assert buyer_ids == {"research_lab", "ai_infra", "regulated_agent"}
    assert evidence_fields >= 24
    assert private_field_count >= 18
    for record in ledger["intake_records"]:
        assert record["privacy_boundary"] == "NO_PRIVATE_CONTACT_DATA_IN_MODEL_CONTEXT"
        assert record["response_status"] == "AWAITING_REAL_RESPONSE"
        assert record["score_status"] == "UNSCORED_PENDING_BUYER_EVIDENCE"
        assert record["model_boundary_allowed_fields"]
        assert record["operator_local_only_fields"]
        assert "contact_email" in record["private_fields_forbidden_in_model_context"]
        assert "private_organization_name" in record["private_fields_forbidden_in_model_context"]
        assert all(field["capture_status"] == "pending_real_buyer_input" for field in record["evidence_capture_fields"])
        assert all(field["verification_status"] == "unverified" for field in record["evidence_capture_fields"])
        assert len(record["evidence_quality_gates"]) >= 5
        assert len(record["falsifiers"]) >= 3
    assert ledger["next_pass"] == "0062"


if __name__ == "__main__":
    test_buyer_evidence_intake_ledger_preserves_privacy_and_open_status()
    print("PASS buyer evidence intake ledger verified")
