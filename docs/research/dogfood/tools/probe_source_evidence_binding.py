"""Generate pass 0028 source/browser evidence binding receipts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


PASS = "0028"
ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = ROOT / "schemas" / "redacted-ref-replay-pass-0027.json"
OUT_PATH = ROOT / "schemas" / "source-evidence-binding-pass-0028.json"
BROWSER_FIXTURE_PATH = ROOT / "fixtures" / "browser-evidence-redacted-pass-0028.json"
REPLAY_MANIFEST_PATH = ROOT / "fixtures" / "source-evidence-replay-manifest-pass-0028.json"


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


def read_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


source = read_json(SOURCE_PATH)

browser_evidence = {
    "schema": "project-telos.browser-evidence/v1",
    "tool": "telos.browser.evidence",
    "mode": "research-capture",
    "session_ref": "browser-session:fixture",
    "target_ref": "url:sha256:100680ad546ce6a577f42f52df33b4cfdca756859e664b8d7de329b150d09ce9",
    "action_receipt_ref": "receipt:fixture-browser-evidence",
    "action": {
        "kind": "browser.navigate",
        "selector": None,
        "args_hash": "args:sha256:abca4de9dd94d3ac2db9c470f8d4557f421b969fab4990c3c719629f7e7a8b69",
    },
    "before": {
        "url": "https://example.com",
        "url_digest": "url:sha256:100680ad546ce6a577f42f52df33b4cfdca756859e664b8d7de329b150d09ce9",
        "title": "Example Domain",
        "dom_snapshot_ref": "artifact:fixture/before-dom.html",
        "text_digest": "text:sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "screenshot_ref": "artifact:fixture/before.png",
    },
    "after": {
        "url": "https://example.com",
        "url_digest": "url:sha256:100680ad546ce6a577f42f52df33b4cfdca756859e664b8d7de329b150d09ce9",
        "title": "Example Domain",
        "dom_snapshot_ref": "artifact:fixture/after-dom.html",
        "text_digest": "text:sha256:f94d9486b327090cccbeb97d67953a1f234b83d67350b7b5f60196b0a30f24db",
        "screenshot_ref": "artifact:fixture/after.png",
    },
    "network_summary": {
        "kind": "network",
        "verdict": "UNVERIFIABLE",
        "failure_code": "network_capture_unavailable",
        "reason": "collector-not-attached",
    },
    "console_summary": {
        "kind": "console",
        "verdict": "UNVERIFIABLE",
        "failure_code": "console_capture_unavailable",
        "reason": "collector-not-attached",
    },
    "artifact_hashes": [
        {
            "ref": "artifact:fixture/after-dom.html",
            "hash": "sha256:3f3a3b3d4a6a7b8c9d00112233445566778899aabbccddeeff00112233445566",
        }
    ],
    "redaction_status": "redacted",
    "side_effect": {"class": "read", "external_write": False, "reversible": True},
    "verification": {"verdict": "MATCH", "ref": "crucible:fixture-browser-evidence-shape"},
    "created_at": "2026-07-01T00:00:00.000Z",
}
browser_evidence["fixture_hash"] = sha256_obj(browser_evidence)
write_json(BROWSER_FIXTURE_PATH, browser_evidence)

replay_manifest = {
    "schema": "SourceEvidenceReplayManifest/v1",
    "pass": PASS,
    "source_replay_schema": source["schema"],
    "source_replay_seal": source["seal"],
    "source_replay_sha256": sha256_file(SOURCE_PATH),
    "browser_evidence_ref": "fixtures/browser-evidence-redacted-pass-0028.json",
    "browser_evidence_sha256": sha256_file(BROWSER_FIXTURE_PATH),
    "target_ref": browser_evidence["target_ref"],
    "after_text_digest": browser_evidence["after"]["text_digest"],
    "network_capture_verdict": browser_evidence["network_summary"]["verdict"],
    "console_capture_verdict": browser_evidence["console_summary"]["verdict"],
    "raw_source_material_required": False,
    "raw_browser_payload_required": False,
    "verification_verdict": "MATCH",
    "non_promotion_statement": "This manifest proves only a local source-evidence binding from redacted browser evidence and digest refs. It does not prove live browsing, production browser capture, scientific discovery, buyer adoption, or any natural law.",
}
replay_manifest["seal"] = sha256_obj({key: value for key, value in replay_manifest.items() if key != "seal"})
write_json(REPLAY_MANIFEST_PATH, replay_manifest)

scan_targets = [
    "schemas/source-evidence-binding-pass-0028.json",
    "fixtures/browser-evidence-redacted-pass-0028.json",
    "fixtures/source-evidence-replay-manifest-pass-0028.json",
    "packets/038-source-evidence-binding.md",
    "adversarial/pass-0028-source-evidence-steelman.md",
    "schemas/tool-receipts-pass-0028.json",
    "crucible/pass-0028-thesis.json",
    "crucible/pass-0028-measurements.json",
]

record = {
    "schema": "SourceEvidenceBindingSet/v1",
    "pass": PASS,
    "generated_on": "2026-07-01",
    "status": "SOURCE_EVIDENCE_BINDING_MATCH",
    "source_receipt": {
        "path": "schemas/redacted-ref-replay-pass-0027.json",
        "sha256": sha256_file(SOURCE_PATH),
        "schema": source["schema"],
        "seal": source["seal"],
        "replay_contract_hash": source["replay_contract"]["contract_hash"],
    },
    "browser_evidence_receipt": {
        "path": "fixtures/browser-evidence-redacted-pass-0028.json",
        "sha256": sha256_file(BROWSER_FIXTURE_PATH),
        "schema": browser_evidence["schema"],
        "tool": browser_evidence["tool"],
        "target_ref": browser_evidence["target_ref"],
        "action_receipt_ref": browser_evidence["action_receipt_ref"],
        "before_url_digest": browser_evidence["before"]["url_digest"],
        "after_url_digest": browser_evidence["after"]["url_digest"],
        "after_text_digest": browser_evidence["after"]["text_digest"],
        "redaction_status": browser_evidence["redaction_status"],
        "network_summary_verdict": browser_evidence["network_summary"]["verdict"],
        "console_summary_verdict": browser_evidence["console_summary"]["verdict"],
        "verification_verdict": browser_evidence["verification"]["verdict"],
    },
    "action_receipt_evidence_binding": {
        "schema": "ActionReceiptSourceEvidenceBinding/v1",
        "action_id": "act_dogfood_0028_source_evidence",
        "event_id": "evt_dogfood_0028_source_evidence_bound",
        "event_type": "evidence_bound",
        "evidence_ref": "artifact:fixtures/browser-evidence-redacted-pass-0028.json",
        "evidence_digest": f"sha256:{sha256_file(BROWSER_FIXTURE_PATH)}",
        "source_replay_ref": "artifact:schemas/redacted-ref-replay-pass-0027.json",
        "source_replay_digest": f"sha256:{sha256_file(SOURCE_PATH)}",
        "redacted_before_ref": source["replay_contract"]["redacted_refs"][0]["source_path"],
        "redacted_after_ref": source["replay_contract"]["redacted_refs"][1]["source_path"],
        "raw_source_material_required": False,
        "raw_browser_payload_required": False,
        "verification": {
            "verdict": "MATCH",
            "ref": "validator:pass-0028-source-evidence-binding",
        },
    },
    "fresh_replay": {
        "schema": "SourceEvidenceDigestReplay/v1",
        "manifest_path": "fixtures/source-evidence-replay-manifest-pass-0028.json",
        "manifest_sha256": sha256_file(REPLAY_MANIFEST_PATH),
        "manifest_seal": replay_manifest["seal"],
        "input_ref_count": 3,
        "inputs": [
            "source replay digest",
            "browser evidence digest",
            "redacted before/after refs",
        ],
        "network_console_unverifiable_preserved": True,
        "raw_source_material_required": False,
        "raw_browser_payload_required": False,
        "replay_verdict": "MATCH",
    },
    "leak_scan": {
        "schema": "SourceEvidenceLeakScanPlan/v1",
        "raw_source_sentinel_hash": sha256_text("UNREDACTED_SOURCE_PAYLOAD_"),
        "raw_source_sentinel_absent_required": True,
        "scan_targets": scan_targets,
        "scan_target_count": len(scan_targets),
    },
    "negative_fixtures": [
        {
            "fixture_id": "negative-source-replay-sha-drift",
            "failure_mode": "Source replay digest differs from pass 0027.",
            "expected_validator_status": "REJECT",
        },
        {
            "fixture_id": "negative-browser-evidence-omitted",
            "failure_mode": "Action receipt binding omits browser evidence ref or digest.",
            "expected_validator_status": "REJECT",
        },
        {
            "fixture_id": "negative-browser-evidence-sha-drift",
            "failure_mode": "Browser evidence file SHA-256 differs from the receipt.",
            "expected_validator_status": "REJECT",
        },
        {
            "fixture_id": "negative-raw-source-required",
            "failure_mode": "Replay requires raw source material.",
            "expected_validator_status": "REJECT",
        },
        {
            "fixture_id": "negative-raw-browser-payload-required",
            "failure_mode": "Replay requires raw browser payload material.",
            "expected_validator_status": "REJECT",
        },
        {
            "fixture_id": "negative-network-unverifiable-promoted",
            "failure_mode": "Network capture UNVERIFIABLE is promoted to MATCH.",
            "expected_validator_status": "REJECT",
        },
        {
            "fixture_id": "negative-console-unverifiable-promoted",
            "failure_mode": "Console capture UNVERIFIABLE is promoted to MATCH.",
            "expected_validator_status": "REJECT",
        },
        {
            "fixture_id": "negative-redaction-status-unredacted",
            "failure_mode": "Browser evidence redaction_status is not redacted.",
            "expected_validator_status": "REJECT",
        },
        {
            "fixture_id": "negative-source-sentinel-present",
            "failure_mode": "A model-facing artifact contains the raw source sentinel token.",
            "expected_validator_status": "REJECT",
        },
    ],
    "source_anchors": [
        {"source": "Pass 0027 redacted-ref replay fixture", "url": "artifact:schemas/redacted-ref-replay-pass-0027.json"},
        {"source": "Telos browser evidence interface", "url": "mcp:telos.browser.evidence"},
        {"source": "Telos action receipt interface", "url": "mcp:telos.action.receipt"},
        {"source": "Telos loop ledger interface", "url": "mcp:telos.loop.ledger"},
    ],
    "non_promotion_statement": "Pass 0028 proves only a local source/browser evidence binding from redacted evidence refs, digest strings, and pass 0027 replay refs. It does not prove live browser collection, production DLP, external vault integration, theorem proof, scientific discovery, buyer adoption, or any natural law.",
}
record["negative_fixture_count"] = len(record["negative_fixtures"])
record["seal"] = sha256_obj({key: value for key, value in record.items() if key != "seal"})
write_json(OUT_PATH, record)

print(
    json.dumps(
        {
            "path": str(OUT_PATH),
            "schema": record["schema"],
            "status": record["status"],
            "source_sha256": record["source_receipt"]["sha256"],
            "browser_evidence_sha256": record["browser_evidence_receipt"]["sha256"],
            "manifest_sha256": record["fresh_replay"]["manifest_sha256"],
            "negative_fixture_count": record["negative_fixture_count"],
            "seal": record["seal"],
        },
        indent=2,
        sort_keys=True,
    )
)
