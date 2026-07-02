"""Behavior test for pass 0060 buyer outreach packets."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_buyer_outreach_packets.py"
SCORECARDS = ROOT / "schemas" / "buyer-discovery-evidence-scorecards-pass-0059.json"


def test_buyer_outreach_packets_are_crm_ready_without_sending() -> None:
    with tempfile.TemporaryDirectory(prefix="telos-pass-0060-") as tmp:
        out_path = Path(tmp) / "outreach.json"
        result = subprocess.run(
            [sys.executable, str(COMPOSER), "--scorecards", str(SCORECARDS), "--out", str(out_path)],
            cwd=REPO,
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0, result.stderr or result.stdout
        packet_set = json.loads(out_path.read_text(encoding="utf-8"))

    buyer_ids = {row["buyer_id"] for row in packet_set["outreach_packets"]}
    template_ids = {row["template_id"] for row in packet_set["outreach_packets"]}
    evidence_fields = sum(len(row["evidence_intake_fields"]) for row in packet_set["outreach_packets"])
    followups = sum(len(row["follow_up_schedule"]) for row in packet_set["outreach_packets"])

    assert packet_set["schema"] == "BuyerOutreachPacketSet/v1"
    assert packet_set["pass"] == "0060"
    assert packet_set["status"] == "BUYER_OUTREACH_PACKETS_MATCH"
    assert packet_set["crm_write_status"] == "NOT_WRITTEN"
    assert packet_set["send_status"] == "NOT_SENT"
    assert packet_set["market_claim_boundary"] == "HYPOTHESIS_ONLY"
    assert packet_set["unsupported_claim_count"] == 0
    assert packet_set["current_promoted_natural_laws"] == []
    assert packet_set["upstream_scorecards"]["status"] == "BUYER_DISCOVERY_EVIDENCE_SCORECARDS_MATCH"
    assert buyer_ids == {"research_lab", "ai_infra", "regulated_agent"}
    assert len(template_ids) == 3
    assert evidence_fields >= 18
    assert followups == 9
    assert packet_set["crm_import"]["counterparty_seed_count"] == 3
    assert packet_set["crm_import"]["outreach_event_count"] == 3
    assert packet_set["crm_import"]["next_touch_count"] == 3
    for packet in packet_set["outreach_packets"]:
        assert packet["route_lane_split"] == ["project-telos", "deep-research", "technical-writing"]
        assert packet["payload_ref"].startswith("docs/research/dogfood/packets/")
        assert packet["counterparty_seed"]["status"] == "prospect_unverified"
        assert packet["outreach_event"]["direction"] == "outbound"
        assert packet["outreach_event"]["event_type"] == "proposal_draft"
        assert packet["negative_disqualifiers"]
        assert packet["acceptance_criteria"]
        assert all(field["required"] is True for field in packet["evidence_intake_fields"])
        assert all(item["verification_status"] in {"verified", "inferred", "unverified"} for item in packet["market_data_targets"])


if __name__ == "__main__":
    test_buyer_outreach_packets_are_crm_ready_without_sending()
    print("PASS buyer outreach packets verified")
