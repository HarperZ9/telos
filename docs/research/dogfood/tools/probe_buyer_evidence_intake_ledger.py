"""Generate pass 0061 receipts for buyer evidence intake ledger."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_buyer_evidence_intake_ledger.py"
TEST_SCRIPT = ROOT / "tools" / "test_buyer_evidence_intake_ledger.py"
OUTREACH = ROOT / "schemas" / "buyer-outreach-packets-pass-0060.json"
OUT_PATH = ROOT / "schemas" / "buyer-evidence-intake-ledger-pass-0061.json"
PACKET_PATH = ROOT / "packets" / "071-buyer-evidence-intake-ledger.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0061-buyer-evidence-intake-ledger-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0061-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0061-measurements.json"


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


def render_packet(ledger: dict, compose_receipt: dict, test_receipt: dict) -> str:
    rows = "\n".join(
        f"| `{row['buyer_id']}` | {len(row['evidence_capture_fields'])} | {len(row['evidence_quality_gates'])} | {len(row['falsifiers'])} | `{row['response_status']}` |"
        for row in ledger["intake_records"]
    )
    return f"""# Packet 071: Buyer Evidence Intake Ledger

Date: 2026-07-01

Status: `{ledger['status']}`

Pass 0061 defines model-safe intake records for real buyer evidence. It does
not collect real buyer responses, write CRM records, or prove demand.

```text
buyer_response_status = {ledger['buyer_response_status']}
crm_write_status = {ledger['crm_write_status']}
send_status = {ledger['send_status']}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
```

| Buyer | Fields | Gates | Falsifiers | Status |
| --- | ---: | ---: | ---: | --- |
{rows}

Current promoted natural laws: none.
"""


def render_steelman(ledger: dict) -> str:
    return f"""# Pass 0061 Steelman: Buyer Evidence Intake Ledger

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

The ledger can fail if it captures too little evidence to score a market wedge,
if redaction strips away the facts needed for decision-making, or if private
buyer data crosses the model boundary.

Current response state: `{ledger['buyer_response_status']}`.
"""


def build_thesis_measurements(ledger: dict, compose_receipt: dict, test_receipt: dict) -> tuple[dict, dict]:
    shas = {
        "artifact": sha256_file(OUT_PATH),
        "composer": sha256_file(COMPOSER),
        "packet": sha256_file(PACKET_PATH),
        "steelman": sha256_file(STEELMAN_PATH),
        "test": sha256_file(TEST_SCRIPT),
    }
    field_count = sum(len(row["evidence_capture_fields"]) for row in ledger["intake_records"])
    private_field_count = sum(len(row["private_fields_forbidden_in_model_context"]) for row in ledger["intake_records"])
    gate_count = sum(len(row["evidence_quality_gates"]) for row in ledger["intake_records"])
    claims = [
        f"Pass 0061 created a BuyerEvidenceIntakeLedger/v1 artifact with status {ledger['status']}, record_count {len(ledger['intake_records'])}, evidence_field_count {field_count}, private_field_count {private_field_count}, gate_count {gate_count}, sha256 {shas['artifact']}, and seal {ledger['seal']}.",
        f"Pass 0061 implements compose_buyer_evidence_intake_ledger.py with sha256 {shas['composer']} and compose_receipt status {compose_receipt['status']}.",
        f"Pass 0061 records a buyer evidence intake test with sha256 {shas['test']} and test_receipt status {test_receipt['status']}.",
        f"Pass 0061 binds upstream pass 0060 seal {ledger['upstream_outreach']['seal']} and status {ledger['upstream_outreach']['status']}.",
        f"Pass 0061 buyer_response_status is {ledger['buyer_response_status']}, crm_write_status is {ledger['crm_write_status']}, and send_status is {ledger['send_status']}.",
        f"Pass 0061 forbids private contact data in model context and records private_field_count {private_field_count}.",
        f"Pass 0061 unsupported_claim_count is {ledger['unsupported_claim_count']}, market_claim_boundary is {ledger['market_claim_boundary']}, and current_promoted_natural_laws remains none.",
        f"Pass 0061 records packet 071 sha256 {shas['packet']} and steelman sha256 {shas['steelman']}.",
    ]
    evidence = [
        [f"schema={ledger['schema']}", f"status={ledger['status']}", f"record_count={len(ledger['intake_records'])}", f"evidence_field_count={field_count}", f"private_field_count={private_field_count}", f"gate_count={gate_count}", f"sha256={shas['artifact']}", f"seal={ledger['seal']}"],
        [f"composer_sha256={shas['composer']}", f"compose_status={compose_receipt['status']}"],
        [f"test_sha256={shas['test']}", f"test_status={test_receipt['status']}"],
        [f"upstream_seal={ledger['upstream_outreach']['seal']}", f"upstream_status={ledger['upstream_outreach']['status']}"],
        [f"buyer_response_status={ledger['buyer_response_status']}", f"crm_write_status={ledger['crm_write_status']}", f"send_status={ledger['send_status']}"],
        [f"private_field_count={private_field_count}", "privacy_boundary=NO_PRIVATE_CONTACT_DATA_IN_MODEL_CONTEXT"],
        [f"unsupported_claim_count={ledger['unsupported_claim_count']}", f"market_claim_boundary={ledger['market_claim_boundary']}", "current_promoted_natural_laws=[]"],
        [f"packet_sha256={shas['packet']}", f"steelman_sha256={shas['steelman']}"],
    ]
    methods = ["artifact-schema-review", "composer-file-review", "composer-test-review", "upstream-binding-review", "open-status-review", "privacy-boundary-review", "non-promotion-boundary-review", "packet-steelman-review"]
    thesis = {"claims": [{"falsification": f"Claim {i + 1} differs from pass 0061 artifact values or required files are missing", "text": claim} for i, claim in enumerate(claims)], "disposition": "fenced", "title": "Dogfood Pass 0061 Buyer Evidence Intake Ledger"}
    measurements = {"measurements": [{"claim": claim, "deviation": 0.0, "evidence": evidence[i], "method": methods[i], "tolerance": 0.5} for i, claim in enumerate(claims)]}
    return thesis, measurements


def main() -> None:
    compose_receipt = run_command([sys.executable, str(COMPOSER), "--outreach", str(OUTREACH), "--out", str(OUT_PATH)])
    test_receipt = run_command([sys.executable, str(TEST_SCRIPT)])
    ledger = read_json(OUT_PATH)
    write_text(PACKET_PATH, render_packet(ledger, compose_receipt, test_receipt))
    write_text(STEELMAN_PATH, render_steelman(ledger))
    thesis, measurements = build_thesis_measurements(ledger, compose_receipt, test_receipt)
    write_json(THESIS_PATH, thesis)
    write_json(MEASUREMENTS_PATH, measurements)
    status = "MATCH" if compose_receipt["status"] == "MATCH" and test_receipt["status"] == "MATCH" and ledger["status"].endswith("_MATCH") else "DRIFT"
    print(json.dumps({"path": str(OUT_PATH), "seal": ledger["seal"], "status": status}, indent=2, sort_keys=True))
    if status != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
