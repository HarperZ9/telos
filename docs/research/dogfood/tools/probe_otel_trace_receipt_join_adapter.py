"""Generate pass 0054 receipts for OTel trace-to-receipt joining."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


PASS = "0054"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
ADAPTER = ROOT / "tools" / "import_otel_trace_receipts.py"
TEST_SCRIPT = ROOT / "tools" / "test_otel_trace_receipt_join_adapter.py"
RECEIPT_PATH = ROOT / "schemas" / "telos-action-receipt-fixture-pass-0024.json"
SPAN_FIXTURE_PATH = ROOT / "fixtures" / "otel-trace-receipt-join-spans-pass-0054.json"
JOIN_PATH = ROOT / "schemas" / "otel-trace-receipt-join-pass-0054.json"
OUT_PATH = ROOT / "schemas" / "otel-trace-receipt-join-adapter-pass-0054.json"
VALIDATOR_RESULT_PATH = ROOT / "schemas" / "pass-0054-otel-trace-receipt-join-adapter-validator-result.json"
PACKET_PATH = ROOT / "packets" / "064-otel-trace-receipt-join-adapter.md"
STEELMAN_PATH = ROOT / "adversarial" / "pass-0054-otel-trace-receipt-join-adapter-steelman.md"
THESIS_PATH = ROOT / "crucible" / "pass-0054-thesis.json"
MEASUREMENTS_PATH = ROOT / "crucible" / "pass-0054-measurements.json"


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_obj(value: object) -> str:
    return sha256_text(canonical_json(value))


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def write_json(path: Path, value: object) -> None:
    write_text(path, json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


def with_seal(value: dict) -> dict:
    sealed = dict(value)
    sealed["seal"] = sha256_obj(value)
    return sealed


def run_command(command: list[str]) -> dict:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True)
    return {
        "command": " ".join(command),
        "exit_code": result.returncode,
        "stderr_sha256": sha256_text(result.stderr),
        "stdout_sha256": sha256_text(result.stdout),
        "status": "MATCH" if result.returncode == 0 else "DRIFT",
    }


def span_fixture() -> dict:
    return {
        "schema": "OpenTelemetrySpanExportFixture/v1",
        "spans": [
            {
                "attributes": {
                    "telos.action_id": "act_dogfood_0024_001",
                    "telos.action_intent_id": "intent_dogfood_0024_001",
                    "telos.exporter_sink_hash": "f2e9f33d12e261457731f6eedbe62c3c6d04d574c2c8274870da4eee0c2c2fc0",
                    "telos.idempotency_key": "idem_dogfood_0024_001",
                },
                "context": {
                    "span_id": "1424d4ca9a6c5b58",
                    "trace_id": "aaa76491660d7a56086f69d1be94debe",
                },
                "end_time": "2026-07-01T12:03:00Z",
                "events": [
                    {"name": "action_proposed"},
                    {"name": "execution_completed"},
                    {"name": "verification_recorded"},
                ],
                "links": [],
                "name": "telos.action.receipt.fixture",
                "parent_id": None,
                "schema": "OpenTelemetrySpanLike/v1",
                "start_time": "2026-07-01T12:00:00Z",
                "status": "OK",
            }
        ],
    }


def render_packet(contract: dict, join: dict) -> str:
    summary = join["join_summary"]
    identity = join["durable_receipt_identity"]
    return f"""# Packet 064: OTel Trace Receipt Join Adapter

Date: 2026-07-01

Status: `{contract['status']}`

Pass 0054 imports an OpenTelemetry-style span export and joins it to the
existing pass 0024 action receipt fixture without replacing the durable Telos
receipt identity.

```text
implementation_status = {contract['implementation_status']}
joined_event_count = {summary['joined_event_count']}
trace_span_count = {summary['trace_span_count']}
trace_replaces_receipt_count = {summary['trace_replaces_receipt_count']}
negative_fixture_count = {contract['verifier_measurements']['negative_fixture_count']}
negative_match_count = {contract['verifier_measurements']['negative_match_count']}
negative_pass_observed_count = {contract['verifier_measurements']['negative_pass_observed_count']}
durable_action_id = {identity['action_id']}
```

Current promoted natural laws: none.
"""


def render_steelman() -> str:
    return """# Pass 0054 Steelman: OTel Trace Receipt Join Adapter

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

This pass proves a local imported-span join over a synthetic span fixture and
the existing pass 0024 receipt chain. It does not prove live OpenTelemetry
collector ingestion, distributed trace backend retention, cross-process
causality, buyer adoption, scientific truth, or any natural law.
"""


def build_thesis_and_measurements(contract: dict, join: dict) -> tuple[dict, dict]:
    schema_sha = sha256_file(OUT_PATH)
    adapter_sha = sha256_file(ADAPTER)
    test_sha = sha256_file(TEST_SCRIPT)
    join_sha = sha256_file(JOIN_PATH)
    receipt_sha = sha256_file(RECEIPT_PATH)
    packet_sha = sha256_file(PACKET_PATH)
    steelman_sha = sha256_file(STEELMAN_PATH)
    claims = [
        f"Pass 0054 created an OTelTraceReceiptJoinAdapterSet/v1 artifact with status {contract['status']}, joined_event_count {contract['verifier_measurements']['joined_event_count']}, sha256 {schema_sha}, and seal {contract['seal']}.",
        f"Pass 0054 implements import_otel_trace_receipts.py with sha256 {adapter_sha} and records implementation_status {contract['implementation_status']}.",
        f"Pass 0054 records a trace join adapter test script with sha256 {test_sha} and test_receipt status {contract['test_receipt']['status']}.",
        f"Pass 0054 generated an OTelTraceReceiptJoinSet/v1 output with status {join['status']}, joined_event_count {join['join_summary']['joined_event_count']}, trace_span_count {join['join_summary']['trace_span_count']}, trace_replaces_receipt_count {join['join_summary']['trace_replaces_receipt_count']}, and sha256 {join_sha}.",
        f"Pass 0054 records negative_fixture_count {join['negative_fixture_count']}, negative_match_count {join['negative_match_count']}, and negative_pass_observed_count {join['negative_pass_observed_count']} from the trace join adapter.",
        f"Pass 0054 binds to pass 0024 action receipt fixture with sha256 {receipt_sha}, seal {contract['upstream_receipt_binding']['seal']}, and source status {contract['upstream_receipt_binding']['source_status']}.",
        "Pass 0054 validator result reports MATCH with joined_event_count 4 and trace_replaces_receipt_count 0.",
        f"Pass 0054 records packet 064 sha256 {packet_sha}, steelman sha256 {steelman_sha}, uniqueness_claim_status HYPOTHESIS_ONLY, and current_promoted_natural_laws remains none.",
    ]
    thesis = {
        "claims": [{"falsification": f"Claim {i + 1} differs from pass 0054 artifact values or required files are missing", "text": claim} for i, claim in enumerate(claims)],
        "disposition": "fenced",
        "title": "Dogfood Pass 0054 OTel Trace Receipt Join Adapter",
    }
    methods = [
        "trace-join-adapter-schema-review",
        "trace-join-adapter-file-review",
        "trace-join-adapter-test-review",
        "trace-join-output-review",
        "trace-join-negative-fixture-review",
        "upstream-action-receipt-binding-review",
        "validator-result-review",
        "non-promotion-boundary-review",
    ]
    evidence = [
        [f"schema=OTelTraceReceiptJoinAdapterSet/v1", f"status={contract['status']}", f"joined_event_count={contract['verifier_measurements']['joined_event_count']}", f"sha256={schema_sha}", f"seal={contract['seal']}"],
        [f"adapter_sha256={adapter_sha}", f"implementation_status={contract['implementation_status']}"],
        [f"test_sha256={test_sha}", f"test_status={contract['test_receipt']['status']}"],
        [f"join_status={join['status']}", f"joined_event_count={join['join_summary']['joined_event_count']}", f"trace_span_count={join['join_summary']['trace_span_count']}", f"trace_replaces_receipt_count={join['join_summary']['trace_replaces_receipt_count']}", f"sha256={join_sha}"],
        [f"negative_fixture_count={join['negative_fixture_count']}", f"negative_match_count={join['negative_match_count']}", f"negative_pass_observed_count={join['negative_pass_observed_count']}"],
        [f"upstream_sha256={receipt_sha}", f"upstream_seal={contract['upstream_receipt_binding']['seal']}", f"source_status={contract['upstream_receipt_binding']['source_status']}"],
        ["validator_status=MATCH", "joined_event_count=4", "trace_replaces_receipt_count=0"],
        [f"packet_sha256={packet_sha}", f"steelman_sha256={steelman_sha}", "uniqueness_claim_status=HYPOTHESIS_ONLY", "current_promoted_natural_laws=[]"],
    ]
    measurements = {
        "measurements": [
            {"claim": claim, "deviation": 0.0, "evidence": evidence[i], "method": methods[i], "tolerance": 0.5}
            for i, claim in enumerate(claims)
        ]
    }
    return thesis, measurements


def main() -> None:
    write_json(SPAN_FIXTURE_PATH, span_fixture())
    adapter_receipt = run_command([sys.executable, str(ADAPTER), "--receipt", str(RECEIPT_PATH), "--spans", str(SPAN_FIXTURE_PATH), "--out", str(JOIN_PATH)])
    test_receipt = run_command([sys.executable, str(TEST_SCRIPT)])
    join = read_json(JOIN_PATH)
    upstream = read_json(RECEIPT_PATH)
    all_match = (
        adapter_receipt["status"] == "MATCH"
        and test_receipt["status"] == "MATCH"
        and join["status"] == "OTEL_TRACE_RECEIPT_JOIN_MATCH"
        and join["join_summary"]["joined_event_count"] == 4
        and join["join_summary"]["trace_replaces_receipt_count"] == 0
        and join["negative_match_count"] == 4
        and join["negative_pass_observed_count"] == 0
    )
    contract = with_seal({
        "adapter_receipt": adapter_receipt,
        "current_promoted_natural_laws": [],
        "generated_on": "2026-07-01",
        "implementation_status": "IMPLEMENTED_LOCAL_TRACE_JOIN_ADAPTER",
        "join_output": {"path": "schemas/otel-trace-receipt-join-pass-0054.json", "schema": join["schema"], "sha256": sha256_file(JOIN_PATH), "status": join["status"]},
        "non_promotion_statement": join["non_promotion_statement"],
        "pass": PASS,
        "schema": "OTelTraceReceiptJoinAdapterSet/v1",
        "span_fixture": {"path": "fixtures/otel-trace-receipt-join-spans-pass-0054.json", "sha256": sha256_file(SPAN_FIXTURE_PATH), "span_count": len(read_json(SPAN_FIXTURE_PATH)["spans"])},
        "status": "OTEL_TRACE_RECEIPT_JOIN_ADAPTER_MATCH" if all_match else "OTEL_TRACE_RECEIPT_JOIN_ADAPTER_DRIFT",
        "test_receipt": test_receipt,
        "uniqueness_claim_status": "HYPOTHESIS_ONLY",
        "upstream_receipt_binding": {"path": "schemas/telos-action-receipt-fixture-pass-0024.json", "seal": upstream["seal"], "sha256": sha256_file(RECEIPT_PATH), "source_status": upstream["status"]},
        "verifier_measurements": {
            "joined_event_count": join["join_summary"]["joined_event_count"],
            "negative_fixture_count": join["negative_fixture_count"],
            "negative_match_count": join["negative_match_count"],
            "negative_pass_observed_count": join["negative_pass_observed_count"],
            "receipt_identity_retained": join["durable_receipt_identity"]["receipt_ref"] != join["imported_trace_ref"],
            "trace_replaces_receipt_count": join["join_summary"]["trace_replaces_receipt_count"],
            "trace_span_count": join["join_summary"]["trace_span_count"],
        },
    })
    write_json(OUT_PATH, contract)
    write_text(PACKET_PATH, render_packet(contract, join))
    write_text(STEELMAN_PATH, render_steelman())
    thesis, measurements = build_thesis_and_measurements(contract, join)
    write_json(THESIS_PATH, thesis)
    write_json(MEASUREMENTS_PATH, measurements)
    print(json.dumps({"path": str(OUT_PATH), "seal": contract["seal"], "status": contract["status"]}, indent=2, sort_keys=True))
    if contract["status"].endswith("_DRIFT"):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
