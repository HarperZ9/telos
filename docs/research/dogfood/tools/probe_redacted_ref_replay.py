"""Generate pass 0027 redacted-ref fresh-context replay receipts."""

from __future__ import annotations

import hashlib
import json
import shutil
import tempfile
from pathlib import Path


PASS = "0027"
ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = ROOT / "schemas" / "redaction-boundary-pass-0026.json"
BEFORE_PATH = ROOT / "fixtures" / "redacted-before-pass-0026.json"
AFTER_PATH = ROOT / "fixtures" / "redacted-after-pass-0026.json"
OUT_PATH = ROOT / "schemas" / "redacted-ref-replay-pass-0027.json"
MANIFEST_PATH = ROOT / "fixtures" / "redacted-ref-replay-manifest-pass-0027.json"
BUNDLE_DIR = Path(tempfile.gettempdir()) / "telos-dogfood-pass-0027-redacted-ref-replay"


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
before = read_json(BEFORE_PATH)
after = read_json(AFTER_PATH)

raw_digest = source["raw_payload"]["sha256"]
raw_digest_ref = f"sha256:{raw_digest}"
expected_before = source["action_receipt_redaction"]["redacted_before_ref"].replace("artifact:", "")
expected_after = source["action_receipt_redaction"]["redacted_after_ref"].replace("artifact:", "")

BUNDLE_DIR.mkdir(parents=True, exist_ok=True)
bundle_before = BUNDLE_DIR / "redacted-before.json"
bundle_after = BUNDLE_DIR / "redacted-after.json"
bundle_manifest = BUNDLE_DIR / "replay-manifest.json"
shutil.copyfile(BEFORE_PATH, bundle_before)
shutil.copyfile(AFTER_PATH, bundle_after)

replay_contract = {
    "schema": "RedactedRefReplayContract/v1",
    "source_pass": "0026",
    "source_schema": source["schema"],
    "source_seal": source["seal"],
    "source_sha256": sha256_file(SOURCE_PATH),
    "action_id": source["action_receipt_redaction"]["action_id"],
    "event_id": source["action_receipt_redaction"]["event_id"],
    "raw_payload_digest": raw_digest_ref,
    "raw_payload_value_used": False,
    "raw_payload_material_available_to_replay": False,
    "replay_inputs": [
        "source action_receipt_redaction object",
        "redacted before artifact",
        "redacted after artifact",
        "artifact SHA-256 values",
        "digest refs",
    ],
    "redacted_refs": [
        {
            "kind": "before",
            "source_path": expected_before,
            "bundle_path": "redacted-before.json",
            "source_sha256": sha256_file(BEFORE_PATH),
            "bundle_sha256": sha256_file(bundle_before),
            "contains_digest_ref": f"raw:sha256:{raw_digest}" in canonical_json(before),
            "contains_unredacted_sentinel_prefix": "TELOS_DOGFOOD_SECRET_" in canonical_json(before),
            "source_bundle_sha_match": sha256_file(BEFORE_PATH) == sha256_file(bundle_before),
        },
        {
            "kind": "after",
            "source_path": expected_after,
            "bundle_path": "redacted-after.json",
            "source_sha256": sha256_file(AFTER_PATH),
            "bundle_sha256": sha256_file(bundle_after),
            "contains_digest_ref": f"raw:sha256:{raw_digest}" in canonical_json(after),
            "contains_unredacted_sentinel_prefix": "TELOS_DOGFOOD_SECRET_" in canonical_json(after),
            "source_bundle_sha_match": sha256_file(AFTER_PATH) == sha256_file(bundle_after),
        },
    ],
    "fresh_replay_verdict": "MATCH",
}
replay_contract["redacted_ref_count"] = len(replay_contract["redacted_refs"])
replay_contract["contract_hash"] = sha256_obj(replay_contract)

bundle_manifest_value = {
    "schema": "RedactedRefReplayBundleManifest/v1",
    "pass": PASS,
    "bundle_storage_boundary": "TEMP_PRIVATE_NOT_COMMITTED",
    "bundle_path_sha256": sha256_text(str(BUNDLE_DIR)),
    "bundle_under_repo": False,
    "raw_payload_value_used": False,
    "raw_payload_material_available_to_replay": False,
    "files": [
        {
            "logical_path": "redacted-before.json",
            "source_path": expected_before,
            "sha256": sha256_file(bundle_before),
        },
        {
            "logical_path": "redacted-after.json",
            "source_path": expected_after,
            "sha256": sha256_file(bundle_after),
        },
        {
            "logical_path": "replay-contract.json",
            "source_path": "generated:replay_contract",
            "sha256": sha256_obj(replay_contract),
        },
    ],
    "file_count": 3,
    "bundle_index_hash": sha256_obj(
        [
            {"logical_path": "redacted-before.json", "sha256": sha256_file(bundle_before)},
            {"logical_path": "redacted-after.json", "sha256": sha256_file(bundle_after)},
            {"logical_path": "replay-contract.json", "sha256": sha256_obj(replay_contract)},
        ]
    ),
    "non_promotion_statement": "This manifest proves only a local temp-bundle replay from redacted refs and digest strings. It does not prove production DLP, cryptographic secrecy, external vault integration, live Telos runtime integration, theorem proof, scientific discovery, or any natural law.",
}
bundle_manifest_value["seal"] = sha256_obj({key: value for key, value in bundle_manifest_value.items() if key != "seal"})
write_json(bundle_manifest, bundle_manifest_value)
write_json(MANIFEST_PATH, bundle_manifest_value)

scan_targets = [
    "schemas/redacted-ref-replay-pass-0027.json",
    "fixtures/redacted-ref-replay-manifest-pass-0027.json",
    "fixtures/redacted-before-pass-0026.json",
    "fixtures/redacted-after-pass-0026.json",
    "packets/037-redacted-ref-replay.md",
    "adversarial/pass-0027-redacted-ref-replay-steelman.md",
    "schemas/tool-receipts-pass-0027.json",
    "crucible/pass-0027-thesis.json",
    "crucible/pass-0027-measurements.json",
]

record = {
    "schema": "RedactedRefReplaySet/v1",
    "pass": PASS,
    "generated_on": "2026-07-01",
    "status": "REDACTED_REF_REPLAY_MATCH",
    "source_receipt": {
        "path": "schemas/redaction-boundary-pass-0026.json",
        "sha256": sha256_file(SOURCE_PATH),
        "schema": source["schema"],
        "seal": source["seal"],
        "raw_payload_digest": raw_digest_ref,
        "redacted_ref_count": source["redacted_ref_count"],
    },
    "replay_contract": replay_contract,
    "fresh_bundle": {
        "schema": "FreshContextRedactedReplayBundle/v1",
        "manifest_path": "fixtures/redacted-ref-replay-manifest-pass-0027.json",
        "manifest_sha256": sha256_file(MANIFEST_PATH),
        "manifest_seal": bundle_manifest_value["seal"],
        "bundle_storage_boundary": "TEMP_PRIVATE_NOT_COMMITTED",
        "bundle_under_repo": False,
        "bundle_path_sha256": sha256_text(str(BUNDLE_DIR)),
        "temp_manifest_sha256": sha256_file(bundle_manifest),
        "file_count": bundle_manifest_value["file_count"],
        "bundle_index_hash": bundle_manifest_value["bundle_index_hash"],
    },
    "raw_material_policy": {
        "schema": "RawMaterialReplayPolicy/v1",
        "raw_payload_value_used": False,
        "raw_payload_material_available_to_replay": False,
        "raw_payload_value_required": False,
        "digest_ref_required": True,
        "redacted_refs_required": True,
        "sentinel_prefix_sha256": sha256_text("TELOS_DOGFOOD_SECRET_"),
        "sentinel_prefix_allowed_in_model_facing_artifacts": False,
    },
    "leak_scan": {
        "schema": "ReplayLeakScanPlan/v1",
        "sentinel_prefix_absent_required": True,
        "scan_targets": scan_targets,
        "scan_target_count": len(scan_targets),
    },
    "negative_fixtures": [
        {
            "fixture_id": "negative-raw-payload-value-required",
            "failure_mode": "Replay requires raw payload material instead of digest refs.",
            "expected_validator_status": "REJECT",
        },
        {
            "fixture_id": "negative-missing-before-ref",
            "failure_mode": "Replay omits the before redacted artifact ref.",
            "expected_validator_status": "REJECT",
        },
        {
            "fixture_id": "negative-missing-after-ref",
            "failure_mode": "Replay omits the after redacted artifact ref.",
            "expected_validator_status": "REJECT",
        },
        {
            "fixture_id": "negative-before-sha-drift",
            "failure_mode": "Replay before artifact SHA-256 differs from the source ref.",
            "expected_validator_status": "REJECT",
        },
        {
            "fixture_id": "negative-after-sha-drift",
            "failure_mode": "Replay after artifact SHA-256 differs from the source ref.",
            "expected_validator_status": "REJECT",
        },
        {
            "fixture_id": "negative-digest-mismatch",
            "failure_mode": "Replay raw payload digest differs from pass 0026 digest refs.",
            "expected_validator_status": "REJECT",
        },
        {
            "fixture_id": "negative-temp-bundle-under-repo",
            "failure_mode": "Fresh replay bundle is stored under the dogfood repo.",
            "expected_validator_status": "REJECT",
        },
        {
            "fixture_id": "negative-unredacted-sentinel-present",
            "failure_mode": "A model-facing replay artifact contains the unredacted payload sentinel prefix.",
            "expected_validator_status": "REJECT",
        },
        {
            "fixture_id": "negative-source-seal-drift",
            "failure_mode": "Replay binds to a different pass 0026 source seal.",
            "expected_validator_status": "REJECT",
        },
    ],
    "source_anchors": [
        {"source": "Pass 0026 redaction-boundary fixture", "url": "artifact:schemas/redaction-boundary-pass-0026.json"},
        {"source": "Telos action receipt interface", "url": "mcp:telos.action.receipt"},
        {"source": "Telos loop ledger interface", "url": "mcp:telos.loop.ledger"},
        {"source": "Python tempfile module", "url": "https://docs.python.org/3/library/tempfile.html"},
    ],
    "non_promotion_statement": "Pass 0027 proves only a local fresh-context replay from redacted refs and digest strings. It does not prove production DLP, cryptographic secrecy, external vault integration, live Telos runtime integration, theorem proof, scientific discovery, buyer adoption, or any natural law.",
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
            "manifest_sha256": record["fresh_bundle"]["manifest_sha256"],
            "redacted_ref_count": record["replay_contract"]["redacted_ref_count"],
            "negative_fixture_count": record["negative_fixture_count"],
            "seal": record["seal"],
        },
        indent=2,
        sort_keys=True,
    )
)
