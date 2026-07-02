"""Validate pass 0028 source/browser evidence binding receipts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "source-evidence-binding-pass-0028.json"
SOURCE_PATH = ROOT / "schemas" / "redacted-ref-replay-pass-0027.json"
BROWSER_FIXTURE_PATH = ROOT / "fixtures" / "browser-evidence-redacted-pass-0028.json"
REPLAY_MANIFEST_PATH = ROOT / "fixtures" / "source-evidence-replay-manifest-pass-0028.json"
RAW_SOURCE_SENTINEL = "UNREDACTED_SOURCE_PAYLOAD_"


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_obj(value: object) -> str:
    return sha256_text(canonical_json(value))


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition: bool, errors: list[str], message: str) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    data = load_json(SCHEMA_PATH)
    source = load_json(SOURCE_PATH)
    browser = load_json(BROWSER_FIXTURE_PATH)
    manifest = load_json(REPLAY_MANIFEST_PATH)
    errors: list[str] = []

    require(data.get("schema") == "SourceEvidenceBindingSet/v1", errors, "wrong schema")
    require(data.get("pass") == "0028", errors, "wrong pass")
    require(data.get("status") == "SOURCE_EVIDENCE_BINDING_MATCH", errors, "wrong status")
    require(data.get("seal") == sha256_obj({key: value for key, value in data.items() if key != "seal"}), errors, "seal mismatch")

    source_receipt = data.get("source_receipt", {})
    require(source_receipt.get("path") == "schemas/redacted-ref-replay-pass-0027.json", errors, "wrong source path")
    require(source_receipt.get("sha256") == sha256_file(SOURCE_PATH), errors, "source sha mismatch")
    require(source_receipt.get("schema") == source.get("schema"), errors, "source schema mismatch")
    require(source_receipt.get("seal") == source.get("seal"), errors, "source seal mismatch")
    require(source_receipt.get("replay_contract_hash") == source.get("replay_contract", {}).get("contract_hash"), errors, "source replay contract hash mismatch")

    browser_receipt = data.get("browser_evidence_receipt", {})
    require(browser_receipt.get("path") == "fixtures/browser-evidence-redacted-pass-0028.json", errors, "wrong browser fixture path")
    require(browser_receipt.get("sha256") == sha256_file(BROWSER_FIXTURE_PATH), errors, "browser sha mismatch")
    require(browser_receipt.get("schema") == "project-telos.browser-evidence/v1", errors, "wrong browser schema")
    require(browser_receipt.get("tool") == "telos.browser.evidence", errors, "wrong browser tool")
    require(browser_receipt.get("target_ref") == browser.get("target_ref"), errors, "target ref mismatch")
    require(browser_receipt.get("action_receipt_ref") == browser.get("action_receipt_ref"), errors, "action receipt ref mismatch")
    require(browser_receipt.get("before_url_digest") == browser.get("before", {}).get("url_digest"), errors, "before digest mismatch")
    require(browser_receipt.get("after_url_digest") == browser.get("after", {}).get("url_digest"), errors, "after digest mismatch")
    require(browser_receipt.get("after_text_digest") == browser.get("after", {}).get("text_digest"), errors, "after text digest mismatch")
    require(browser_receipt.get("redaction_status") == "redacted", errors, "redaction status mismatch")
    require(browser_receipt.get("network_summary_verdict") == "UNVERIFIABLE", errors, "network verdict not preserved")
    require(browser_receipt.get("console_summary_verdict") == "UNVERIFIABLE", errors, "console verdict not preserved")
    require(browser_receipt.get("verification_verdict") == "MATCH", errors, "browser verification mismatch")
    require(browser.get("fixture_hash") == sha256_obj({key: value for key, value in browser.items() if key != "fixture_hash"}), errors, "browser fixture hash mismatch")

    binding = data.get("action_receipt_evidence_binding", {})
    require(binding.get("schema") == "ActionReceiptSourceEvidenceBinding/v1", errors, "wrong binding schema")
    require(binding.get("event_type") == "evidence_bound", errors, "wrong event type")
    require(binding.get("evidence_ref") == "artifact:fixtures/browser-evidence-redacted-pass-0028.json", errors, "wrong evidence ref")
    require(binding.get("evidence_digest") == f"sha256:{sha256_file(BROWSER_FIXTURE_PATH)}", errors, "evidence digest mismatch")
    require(binding.get("source_replay_digest") == f"sha256:{sha256_file(SOURCE_PATH)}", errors, "source replay digest mismatch")
    require(binding.get("raw_source_material_required") is False, errors, "raw source required")
    require(binding.get("raw_browser_payload_required") is False, errors, "raw browser payload required")
    require(binding.get("verification", {}).get("verdict") == "MATCH", errors, "binding verification mismatch")

    replay = data.get("fresh_replay", {})
    require(replay.get("schema") == "SourceEvidenceDigestReplay/v1", errors, "wrong replay schema")
    require(replay.get("manifest_path") == "fixtures/source-evidence-replay-manifest-pass-0028.json", errors, "wrong manifest path")
    require(replay.get("manifest_sha256") == sha256_file(REPLAY_MANIFEST_PATH), errors, "manifest sha mismatch")
    require(replay.get("manifest_seal") == manifest.get("seal"), errors, "manifest seal mismatch")
    require(replay.get("input_ref_count") == 3, errors, "wrong input ref count")
    require(replay.get("network_console_unverifiable_preserved") is True, errors, "unverifiable not preserved")
    require(replay.get("raw_source_material_required") is False, errors, "replay raw source required")
    require(replay.get("raw_browser_payload_required") is False, errors, "replay raw browser required")
    require(replay.get("replay_verdict") == "MATCH", errors, "replay verdict mismatch")

    require(manifest.get("seal") == sha256_obj({key: value for key, value in manifest.items() if key != "seal"}), errors, "manifest seal mismatch")
    require(manifest.get("source_replay_sha256") == sha256_file(SOURCE_PATH), errors, "manifest source sha mismatch")
    require(manifest.get("browser_evidence_sha256") == sha256_file(BROWSER_FIXTURE_PATH), errors, "manifest browser sha mismatch")
    require(manifest.get("network_capture_verdict") == "UNVERIFIABLE", errors, "manifest network promoted")
    require(manifest.get("console_capture_verdict") == "UNVERIFIABLE", errors, "manifest console promoted")
    require(manifest.get("raw_source_material_required") is False, errors, "manifest raw source required")
    require(manifest.get("raw_browser_payload_required") is False, errors, "manifest raw browser required")

    leak_scan = data.get("leak_scan", {})
    targets = leak_scan.get("scan_targets", [])
    required_targets = {
        "schemas/source-evidence-binding-pass-0028.json",
        "fixtures/browser-evidence-redacted-pass-0028.json",
        "fixtures/source-evidence-replay-manifest-pass-0028.json",
        "packets/038-source-evidence-binding.md",
        "adversarial/pass-0028-source-evidence-steelman.md",
        "schemas/tool-receipts-pass-0028.json",
        "crucible/pass-0028-thesis.json",
        "crucible/pass-0028-measurements.json",
    }
    require(leak_scan.get("raw_source_sentinel_hash") == sha256_text(RAW_SOURCE_SENTINEL), errors, "sentinel hash mismatch")
    require(leak_scan.get("raw_source_sentinel_absent_required") is True, errors, "sentinel absence not required")
    require(leak_scan.get("scan_target_count") == len(targets), errors, "scan target count mismatch")
    require(required_targets.issubset(set(targets)), errors, "missing scan target")
    sentinel_hits = []
    scanned = []
    for target in targets:
        path = ROOT / target
        require(path.exists(), errors, f"scan target missing {target}")
        if path.exists():
            text = path.read_text(encoding="utf-8")
            if RAW_SOURCE_SENTINEL in text:
                sentinel_hits.append(target)
            scanned.append(target)
    require(not sentinel_hits, errors, f"raw source sentinel leaks: {sentinel_hits}")

    negatives = data.get("negative_fixtures", [])
    require(data.get("negative_fixture_count") == len(negatives), errors, "negative count mismatch")
    require(len(negatives) >= 9, errors, "expected at least nine negatives")
    require(all(n.get("expected_validator_status") == "REJECT" for n in negatives), errors, "negative not rejected")

    result = {
        "schema": "Pass0028SourceEvidenceBindingValidatorRun/v1",
        "pass": "0028",
        "status": "MATCH" if not errors else "DRIFT",
        "match": 1 if not errors else 0,
        "drift": 0 if not errors else 1,
        "checks": [
            {
                "artifact": "SourceEvidenceBindingSet",
                "path": str(SCHEMA_PATH.relative_to(ROOT)),
                "status": "MATCH" if not errors else "DRIFT",
                "source_sha256": source_receipt.get("sha256"),
                "browser_evidence_sha256": browser_receipt.get("sha256"),
                "manifest_sha256": replay.get("manifest_sha256"),
                "negative_fixture_count": len(negatives),
                "scan_target_count": len(scanned),
                "raw_source_sentinel_leak_count": len(sentinel_hits),
                "network_summary_verdict": browser_receipt.get("network_summary_verdict"),
                "console_summary_verdict": browser_receipt.get("console_summary_verdict"),
                "errors": errors,
            }
        ],
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
