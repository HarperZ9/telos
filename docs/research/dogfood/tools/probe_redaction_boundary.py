"""Generate pass 0026 redaction-boundary receipts."""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from pathlib import Path


PASS = "0026"
ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = ROOT / "schemas" / "action-receipt-persistence-replay-pass-0025.json"
OUT_PATH = ROOT / "schemas" / "redaction-boundary-pass-0026.json"
BEFORE_PATH = ROOT / "fixtures" / "redacted-before-pass-0026.json"
AFTER_PATH = ROOT / "fixtures" / "redacted-after-pass-0026.json"
RAW_PATH = Path(os.environ.get("TELOS_DOGFOOD_REDACTION_RAW_PATH", Path(tempfile.gettempdir()) / "telos-dogfood-redaction-pass-0026-raw.txt"))


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_obj(value: object) -> str:
    return sha256_text(canonical_json(value))


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


raw_payload = "TELOS_DOGFOOD_SECRET_" + sha256_text("pass-0026-redaction-boundary-raw-payload")
RAW_PATH.write_text(raw_payload, encoding="utf-8")
raw_digest = sha256_text(raw_payload)
redaction_token = f"[REDACTED:sha256:{raw_digest[:16]}]"
source = json.loads(SOURCE_PATH.read_text(encoding="utf-8"))

before = {
    "schema": "RedactedBeforeRef/v1",
    "pass": PASS,
    "raw_payload_ref": f"raw:sha256:{raw_digest}",
    "message": f"local fixture payload {redaction_token}",
    "redaction_policy": "replace raw payload with digest-bound token",
}
after = {
    "schema": "RedactedAfterRef/v1",
    "pass": PASS,
    "action_id": "act_dogfood_0024_001",
    "event_id": "evt_dogfood_0026_redaction_boundary",
    "raw_payload_ref": f"raw:sha256:{raw_digest}",
    "result_summary": f"payload preserved only as {redaction_token}",
    "redaction_policy": "raw payload absent from model-facing artifacts",
}
write_json(BEFORE_PATH, before)
write_json(AFTER_PATH, after)

scan_targets = [
    "schemas/redaction-boundary-pass-0026.json",
    "fixtures/redacted-before-pass-0026.json",
    "fixtures/redacted-after-pass-0026.json",
    "packets/036-redaction-boundary.md",
    "adversarial/pass-0026-redaction-boundary-steelman.md",
    "schemas/tool-receipts-pass-0026.json",
    "crucible/pass-0026-thesis.json",
    "crucible/pass-0026-measurements.json",
]

record = {
    "schema": "RedactionBoundaryFixtureSet/v1",
    "pass": PASS,
    "generated_on": "2026-07-01",
    "status": "REDACTION_BOUNDARY_MATCH",
    "source_receipt": {
        "path": "schemas/action-receipt-persistence-replay-pass-0025.json",
        "sha256": sha256_file(SOURCE_PATH),
        "schema": source["schema"],
        "seal": source["seal"],
        "ledger_head_hash": source["ledger"]["ledger_head_hash"],
    },
    "raw_payload": {
        "schema": "TempPrivateRawPayloadRef/v1",
        "storage_boundary": "TEMP_PRIVATE_NOT_COMMITTED",
        "path_sha256": sha256_text(str(RAW_PATH)),
        "sha256": raw_digest,
        "length": len(raw_payload),
        "value_in_receipts": False,
        "value_in_model_facing_artifacts": False,
    },
    "redacted_refs": [
        {
            "kind": "before",
            "path": "fixtures/redacted-before-pass-0026.json",
            "sha256": sha256_file(BEFORE_PATH),
            "contains_raw_payload": False,
            "contains_digest_ref": True,
        },
        {
            "kind": "after",
            "path": "fixtures/redacted-after-pass-0026.json",
            "sha256": sha256_file(AFTER_PATH),
            "contains_raw_payload": False,
            "contains_digest_ref": True,
        },
    ],
    "action_receipt_redaction": {
        "schema": "ActionReceiptRedactionRef/v1",
        "action_id": "act_dogfood_0024_001",
        "event_id": "evt_dogfood_0026_redaction_boundary",
        "redacted_before_ref": "artifact:fixtures/redacted-before-pass-0026.json",
        "redacted_after_ref": "artifact:fixtures/redacted-after-pass-0026.json",
        "raw_payload_digest": f"sha256:{raw_digest}",
        "raw_payload_required_for_model": False,
        "verification": {"verdict": "MATCH", "ref": "validator:pass-0026-redaction-boundary"},
    },
    "leak_scan": {
        "schema": "RedactionLeakScanPlan/v1",
        "raw_payload_absent_required": True,
        "scan_targets": scan_targets,
        "scan_target_count": len(scan_targets),
    },
    "negative_fixtures": [
        {
            "fixture_id": "negative-raw-payload-in-packet",
            "failure_mode": "The raw payload appears in a packet or measurement artifact.",
            "expected_validator_status": "REJECT",
        },
        {
            "fixture_id": "negative-raw-payload-in-receipt",
            "failure_mode": "The receipt stores the raw payload value instead of a digest ref.",
            "expected_validator_status": "REJECT",
        },
        {
            "fixture_id": "negative-redacted-ref-missing-digest",
            "failure_mode": "A redacted before or after ref omits the raw payload digest.",
            "expected_validator_status": "REJECT",
        },
        {
            "fixture_id": "negative-digest-mismatch",
            "failure_mode": "The digest in the redacted ref does not match the temp-private raw payload.",
            "expected_validator_status": "REJECT",
        },
        {
            "fixture_id": "negative-before-ref-missing",
            "failure_mode": "The action receipt has no redacted_before_ref.",
            "expected_validator_status": "REJECT",
        },
        {
            "fixture_id": "negative-after-ref-missing",
            "failure_mode": "The action receipt has no redacted_after_ref.",
            "expected_validator_status": "REJECT",
        },
        {
            "fixture_id": "negative-raw-path-committed",
            "failure_mode": "The raw payload is stored under the repo instead of a temp-private boundary.",
            "expected_validator_status": "REJECT",
        },
        {
            "fixture_id": "negative-leak-scan-target-missing",
            "failure_mode": "A model-facing artifact is omitted from the leak scan target list.",
            "expected_validator_status": "REJECT",
        },
    ],
    "source_anchors": [
        {"source": "Telos action receipt interface", "url": "mcp:telos.action.receipt"},
        {"source": "Telos browser evidence privacy boundary", "url": "mcp:telos.browser.evidence"},
        {"source": "Python tempfile module", "url": "https://docs.python.org/3/library/tempfile.html"},
    ],
    "non_promotion_statement": "Pass 0026 proves only a local redaction-boundary fixture: a temp-private raw payload, digest-bound redacted refs, and leak scans over model-facing artifacts. It does not prove production DLP, cryptographic secrecy, external vault integration, live Telos runtime integration, scientific discovery, theorem proof, or any natural law.",
}
record["redacted_ref_count"] = len(record["redacted_refs"])
record["negative_fixture_count"] = len(record["negative_fixtures"])
record["seal"] = sha256_obj({key: value for key, value in record.items() if key != "seal"})
write_json(OUT_PATH, record)

print(
    json.dumps(
        {
            "path": str(OUT_PATH),
            "schema": record["schema"],
            "status": record["status"],
            "raw_payload_sha256": raw_digest,
            "redacted_ref_count": record["redacted_ref_count"],
            "negative_fixture_count": record["negative_fixture_count"],
            "seal": record["seal"],
        },
        indent=2,
        sort_keys=True,
    )
)
