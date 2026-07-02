"""Generate pass 0060 receipts for buyer outreach packets."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


PASS = "0060"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_buyer_outreach_packets.py"
TEST_SCRIPT = ROOT / "tools" / "test_buyer_outreach_packets.py"
SCORECARDS = ROOT / "schemas" / "buyer-discovery-evidence-scorecards-pass-0059.json"
OUT_PATH = ROOT / "schemas" / "buyer-outreach-packets-pass-0060.json"
PACKET_PATH = ROOT / "packets" / "070-buyer-outreach-packets.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0060-buyer-outreach-packets-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0060-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0060-measurements.json"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def write_json(path: Path, value: object) -> None:
    write_text(path, json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


def run_command(command: list[str]) -> dict:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True)
    return {
        "command": " ".join(command),
        "exit_code": result.returncode,
        "stderr_sha256": sha256_text(result.stderr),
        "stdout_sha256": sha256_text(result.stdout),
        "status": "MATCH" if result.returncode == 0 else "DRIFT",
    }


def render_summary(packet_set: dict, compose_receipt: dict, test_receipt: dict) -> str:
    rows = "\n".join(
        f"| `{row['buyer_id']}` | `{row['counterparty_seed']['status']}` | {len(row['evidence_intake_fields'])} | {len(row['follow_up_schedule'])} | `{row['verification_status']}` |"
        for row in packet_set["outreach_packets"]
    )
    return f"""# Packet 070: Buyer Outreach Packets

Date: 2026-07-01

Status: `{packet_set['status']}`

Pass 0060 turns pass 0059 scorecards into CRM-ready outreach packet drafts.
No outreach was sent and no CRM rows were written.

```text
crm_write_status = {packet_set['crm_write_status']}
send_status = {packet_set['send_status']}
counterparty_seed_count = {packet_set['crm_import']['counterparty_seed_count']}
outreach_event_count = {packet_set['crm_import']['outreach_event_count']}
next_touch_count = {packet_set['crm_import']['next_touch_count']}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
```

| Buyer | CRM Status | Evidence Fields | Follow-ups | Verification |
| --- | --- | ---: | ---: | --- |
{rows}

Current promoted natural laws: none.
"""


def render_payload(packet: dict) -> str:
    criteria = "\n".join(f"- {item}" for item in packet["acceptance_criteria"])
    disqualifiers = "\n".join(f"- {item}" for item in packet["negative_disqualifiers"])
    fields = "\n".join(f"- `{field['field_id']}`: {field['label']}" for field in packet["evidence_intake_fields"])
    followups = "\n".join(f"- day {item['offset_days']}: {item['reason']}" for item in packet["follow_up_schedule"])
    return f"""# {packet['subject']}

Buyer: `{packet['buyer_id']}`

Status: `{packet['verification_status']}`

## Draft

{packet['template_body']}

## Evidence Intake Fields

{fields}

## Acceptance Criteria

{criteria}

## Negative Disqualifiers

{disqualifiers}

## Follow-up Schedule

{followups}
"""


def render_steelman(packet_set: dict) -> str:
    return f"""# Pass 0060 Steelman: Buyer Outreach Packets

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

This pass can fail if draft packets remain too generic, if no real buyer names a
budget path, if CRM import shapes do not match later counterparty records, or if
operators accidentally treat draft outreach as sent outreach.

The packet set remains `{packet_set['market_claim_boundary']}`, with
`{packet_set['crm_write_status']}` and `{packet_set['send_status']}` boundaries.
"""


def write_payloads(packet_set: dict) -> list[Path]:
    paths = []
    for packet in packet_set["outreach_packets"]:
        path = REPO / packet["payload_ref"]
        write_text(path, render_payload(packet))
        paths.append(path)
    return paths


def build_thesis_measurements(packet_set: dict, compose_receipt: dict, test_receipt: dict, payload_paths: list[Path]) -> tuple[dict, dict]:
    shas = {
        "artifact": sha256_file(OUT_PATH),
        "composer": sha256_file(COMPOSER),
        "packet": sha256_file(PACKET_PATH),
        "steelman": sha256_file(STEELMAN_PATH),
        "test": sha256_file(TEST_SCRIPT),
    }
    payload_shas = [sha256_file(path) for path in payload_paths]
    field_count = sum(len(row["evidence_intake_fields"]) for row in packet_set["outreach_packets"])
    followup_count = sum(len(row["follow_up_schedule"]) for row in packet_set["outreach_packets"])
    claims = [
        f"Pass 0060 created a BuyerOutreachPacketSet/v1 artifact with status {packet_set['status']}, packet_count {len(packet_set['outreach_packets'])}, evidence_field_count {field_count}, followup_count {followup_count}, sha256 {shas['artifact']}, and seal {packet_set['seal']}.",
        f"Pass 0060 implements compose_buyer_outreach_packets.py with sha256 {shas['composer']} and compose_receipt status {compose_receipt['status']}.",
        f"Pass 0060 records a buyer outreach packet test with sha256 {shas['test']} and test_receipt status {test_receipt['status']}.",
        f"Pass 0060 binds upstream pass 0059 seal {packet_set['upstream_scorecards']['seal']} and status {packet_set['upstream_scorecards']['status']}.",
        f"Pass 0060 wrote three draft payload files with sha256 values {','.join(payload_shas)}.",
        f"Pass 0060 crm_write_status is {packet_set['crm_write_status']}, send_status is {packet_set['send_status']}, and CRM import counts are {packet_set['crm_import']['counterparty_seed_count']}, {packet_set['crm_import']['outreach_event_count']}, {packet_set['crm_import']['next_touch_count']}.",
        f"Pass 0060 unsupported_claim_count is {packet_set['unsupported_claim_count']}, market_claim_boundary is {packet_set['market_claim_boundary']}, and current_promoted_natural_laws remains none.",
        f"Pass 0060 records packet 070 sha256 {shas['packet']} and steelman sha256 {shas['steelman']}.",
    ]
    evidence = [
        [f"schema={packet_set['schema']}", f"status={packet_set['status']}", f"packet_count={len(packet_set['outreach_packets'])}", f"evidence_field_count={field_count}", f"followup_count={followup_count}", f"sha256={shas['artifact']}", f"seal={packet_set['seal']}"],
        [f"composer_sha256={shas['composer']}", f"compose_status={compose_receipt['status']}"],
        [f"test_sha256={shas['test']}", f"test_status={test_receipt['status']}"],
        [f"upstream_seal={packet_set['upstream_scorecards']['seal']}", f"upstream_status={packet_set['upstream_scorecards']['status']}"],
        [f"payload_count={len(payload_paths)}", f"payload_shas={','.join(payload_shas)}"],
        [f"crm_write_status={packet_set['crm_write_status']}", f"send_status={packet_set['send_status']}", f"crm_import_counts={packet_set['crm_import']['counterparty_seed_count']},{packet_set['crm_import']['outreach_event_count']},{packet_set['crm_import']['next_touch_count']}"],
        [f"unsupported_claim_count={packet_set['unsupported_claim_count']}", f"market_claim_boundary={packet_set['market_claim_boundary']}", "current_promoted_natural_laws=[]"],
        [f"packet_sha256={shas['packet']}", f"steelman_sha256={shas['steelman']}"],
    ]
    methods = ["artifact-schema-review", "composer-file-review", "composer-test-review", "upstream-binding-review", "payload-file-review", "crm-boundary-review", "non-promotion-boundary-review", "packet-steelman-review"]
    thesis = {"claims": [{"falsification": f"Claim {i + 1} differs from pass 0060 artifact values or required files are missing", "text": claim} for i, claim in enumerate(claims)], "disposition": "fenced", "title": "Dogfood Pass 0060 Buyer Outreach Packets"}
    measurements = {"measurements": [{"claim": claim, "deviation": 0.0, "evidence": evidence[i], "method": methods[i], "tolerance": 0.5} for i, claim in enumerate(claims)]}
    return thesis, measurements


def main() -> None:
    compose_receipt = run_command([sys.executable, str(COMPOSER), "--scorecards", str(SCORECARDS), "--out", str(OUT_PATH)])
    test_receipt = run_command([sys.executable, str(TEST_SCRIPT)])
    packet_set = read_json(OUT_PATH)
    payload_paths = write_payloads(packet_set)
    write_text(PACKET_PATH, render_summary(packet_set, compose_receipt, test_receipt))
    write_text(STEELMAN_PATH, render_steelman(packet_set))
    thesis, measurements = build_thesis_measurements(packet_set, compose_receipt, test_receipt, payload_paths)
    write_json(THESIS_PATH, thesis)
    write_json(MEASUREMENTS_PATH, measurements)
    status = "MATCH" if compose_receipt["status"] == "MATCH" and test_receipt["status"] == "MATCH" and packet_set["status"].endswith("_MATCH") else "DRIFT"
    print(json.dumps({"path": str(OUT_PATH), "seal": packet_set["seal"], "status": status}, indent=2, sort_keys=True))
    if status != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
