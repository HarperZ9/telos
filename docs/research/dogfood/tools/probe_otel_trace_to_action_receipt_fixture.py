"""Generate pass 0065 receipts for the OTel trace to action receipt fixture."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
COMPOSER = ROOT / "tools" / "compose_otel_trace_to_action_receipt_fixture.py"
TEST_SCRIPT = ROOT / "tools" / "test_otel_trace_to_action_receipt_fixture.py"
OUT_PATH = ROOT / "schemas" / "otel-trace-to-action-receipt-fixture-pass-0065.json"
PACKET_PATH = ROOT / "packets" / "075-otel-trace-to-action-receipt-fixture.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0065-otel-trace-to-action-receipt-fixture-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0065-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0065-measurements.json"


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


def render_packet(packet: dict, compose_receipt: dict, test_receipt: dict) -> str:
    trace = packet["trace_fixture"]
    receipt = packet["action_receipt"]
    span_lines = "\n".join(f"- `{span['span_id']}` `{span['name']}` kind `{span['kind']}`" for span in trace["spans"])
    return f"""# Packet 075: OTel Trace to Telos Action Receipt Fixture

Date: 2026-07-01

Status: `{packet['status']}`

Purpose: prove a bounded adapter path from a synthetic OpenTelemetry-style trace into a Telos action receipt.

```text
trace_id = {trace['trace_id']}
span_count = {len(trace['spans'])}
receipt_id = {receipt['receipt_id']}
side_effect_class = {receipt['side_effect_class']}
verification_verdict = {receipt['verification_verdict']}
negative_fixture_status = {packet['negative_fixture']['status']}
compose_status = {compose_receipt['status']}
test_status = {test_receipt['status']}
```

## Spans

{span_lines}

Current promoted natural laws: none.
"""


def render_steelman(packet: dict) -> str:
    return f"""# Pass 0065 Steelman: OTel Trace to Action Receipt Fixture

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

This is a synthetic fixture, not live OpenTelemetry ingestion. It proves the
minimum shape of the adapter, not SDK compatibility, production performance,
vendor integration, or buyer value. The next pass should either ingest a real
OTLP export file or package this receipt for a buyer-facing regulated-agent demo.

Non-promotion statement: {packet['non_promotion_statement']}
"""


def build_thesis_measurements(packet: dict, compose_receipt: dict, test_receipt: dict) -> tuple[dict, dict]:
    shas = {
        "artifact": sha256_file(OUT_PATH),
        "composer": sha256_file(COMPOSER),
        "packet": sha256_file(PACKET_PATH),
        "steelman": sha256_file(STEELMAN_PATH),
        "test": sha256_file(TEST_SCRIPT),
    }
    trace = packet["trace_fixture"]
    receipt = packet["action_receipt"]
    claims = [
        f"Pass 0065 created an OtelTraceToTelosActionReceiptFixture/v1 artifact with status {packet['status']}, sha256 {shas['artifact']}, and seal {packet['seal']}.",
        f"Pass 0065 trace fixture has trace_id {trace['trace_id']} and {len(trace['spans'])} spans.",
        f"Pass 0065 action receipt uses schema {receipt['schema']}, receipt_status {receipt['receipt_status']}, verification_verdict {receipt['verification_verdict']}, and side_effect_class {receipt['side_effect_class']}.",
        f"Pass 0065 action receipt trace_refs preserve trace_id {receipt['trace_refs']['trace_id']} and {len(receipt['trace_refs']['span_ids'])} span ids.",
        f"Pass 0065 negative fixture status is {packet['negative_fixture']['status']} with expected failures {','.join(packet['negative_fixture']['expected_failures'])}.",
        f"Pass 0065 composer sha256 is {shas['composer']} and compose_receipt status is {compose_receipt['status']}.",
        f"Pass 0065 packet sha256 is {shas['packet']}, steelman sha256 is {shas['steelman']}, and test sha256 is {shas['test']} with test_receipt status {test_receipt['status']}.",
    ]
    evidence = [
        [f"schema={packet['schema']}", f"status={packet['status']}", f"sha256={shas['artifact']}", f"seal={packet['seal']}"],
        [f"trace_id={trace['trace_id']}", f"span_count={len(trace['spans'])}"],
        [f"receipt_schema={receipt['schema']}", f"receipt_status={receipt['receipt_status']}", f"verification_verdict={receipt['verification_verdict']}", f"side_effect_class={receipt['side_effect_class']}"],
        [f"trace_ref={receipt['trace_refs']['trace_id']}", f"span_ref_count={len(receipt['trace_refs']['span_ids'])}"],
        [f"negative_status={packet['negative_fixture']['status']}", ",".join(packet["negative_fixture"]["expected_failures"])],
        [f"composer_sha256={shas['composer']}", f"compose_status={compose_receipt['status']}"],
        [f"packet_sha256={shas['packet']}", f"steelman_sha256={shas['steelman']}", f"test_sha256={shas['test']}", f"test_status={test_receipt['status']}"],
    ]
    thesis = {"claims": [{"falsification": f"Claim {i + 1} differs from pass 0065 artifact values or required files are missing", "text": claim} for i, claim in enumerate(claims)], "disposition": "fenced", "title": "Dogfood Pass 0065 OTel Trace to Action Receipt Fixture"}
    measurements = {"measurements": [{"claim": claim, "deviation": 0.0, "evidence": evidence[i], "method": "artifact-review", "tolerance": 0.5} for i, claim in enumerate(claims)]}
    return thesis, measurements


def main() -> None:
    compose_receipt = run_command([sys.executable, str(COMPOSER), "--out", str(OUT_PATH)])
    test_receipt = run_command([sys.executable, str(TEST_SCRIPT)])
    packet = read_json(OUT_PATH)
    write_text(PACKET_PATH, render_packet(packet, compose_receipt, test_receipt))
    write_text(STEELMAN_PATH, render_steelman(packet))
    thesis, measurements = build_thesis_measurements(packet, compose_receipt, test_receipt)
    write_json(THESIS_PATH, thesis)
    write_json(MEASUREMENTS_PATH, measurements)
    status = "MATCH" if compose_receipt["status"] == "MATCH" and test_receipt["status"] == "MATCH" and packet["status"].endswith("_MATCH") else "DRIFT"
    print(json.dumps({"path": str(OUT_PATH), "seal": packet["seal"], "status": status}, indent=2, sort_keys=True))
    if status != "MATCH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
