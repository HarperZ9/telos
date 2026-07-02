"""Validate pass 0027 redacted-ref fresh-context replay receipts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "redacted-ref-replay-pass-0027.json"
SOURCE_PATH = ROOT / "schemas" / "redaction-boundary-pass-0026.json"
BEFORE_PATH = ROOT / "fixtures" / "redacted-before-pass-0026.json"
AFTER_PATH = ROOT / "fixtures" / "redacted-after-pass-0026.json"
MANIFEST_PATH = ROOT / "fixtures" / "redacted-ref-replay-manifest-pass-0027.json"
SENTINEL_PREFIX = "TELOS_DOGFOOD_SECRET_"


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_obj(value: object) -> str:
    return sha256_text(canonical_json(value))


def require(condition: bool, errors: list[str], message: str) -> None:
    if not condition:
        errors.append(message)


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    data = load_json(SCHEMA_PATH)
    source = load_json(SOURCE_PATH)
    before = load_json(BEFORE_PATH)
    after = load_json(AFTER_PATH)
    manifest = load_json(MANIFEST_PATH)
    errors: list[str] = []

    require(data.get("schema") == "RedactedRefReplaySet/v1", errors, "wrong schema")
    require(data.get("pass") == "0027", errors, "wrong pass")
    require(data.get("status") == "REDACTED_REF_REPLAY_MATCH", errors, "wrong status")
    expected_seal = sha256_obj({key: value for key, value in data.items() if key != "seal"})
    require(data.get("seal") == expected_seal, errors, "seal mismatch")

    source_receipt = data.get("source_receipt", {})
    require(source_receipt.get("path") == "schemas/redaction-boundary-pass-0026.json", errors, "wrong source path")
    require(source_receipt.get("sha256") == sha256_file(SOURCE_PATH), errors, "source sha mismatch")
    require(source_receipt.get("schema") == source.get("schema"), errors, "source schema mismatch")
    require(source_receipt.get("seal") == source.get("seal"), errors, "source seal mismatch")
    require(source_receipt.get("raw_payload_digest") == source.get("action_receipt_redaction", {}).get("raw_payload_digest"), errors, "source digest mismatch")
    require(source_receipt.get("redacted_ref_count") == source.get("redacted_ref_count"), errors, "source ref count mismatch")

    raw_digest = source.get("raw_payload", {}).get("sha256")
    raw_digest_ref = f"sha256:{raw_digest}"
    require(source_receipt.get("raw_payload_digest") == raw_digest_ref, errors, "raw digest ref mismatch")

    contract = data.get("replay_contract", {})
    require(contract.get("schema") == "RedactedRefReplayContract/v1", errors, "wrong replay contract schema")
    require(contract.get("source_pass") == "0026", errors, "wrong replay source pass")
    require(contract.get("source_seal") == source.get("seal"), errors, "replay source seal mismatch")
    require(contract.get("source_sha256") == sha256_file(SOURCE_PATH), errors, "replay source sha mismatch")
    require(contract.get("raw_payload_digest") == raw_digest_ref, errors, "replay digest mismatch")
    require(contract.get("raw_payload_value_used") is False, errors, "raw payload value used")
    require(contract.get("raw_payload_material_available_to_replay") is False, errors, "raw payload material available")
    require(contract.get("fresh_replay_verdict") == "MATCH", errors, "fresh replay verdict mismatch")
    require(contract.get("redacted_ref_count") == 2, errors, "wrong replay ref count")
    require(contract.get("contract_hash") == sha256_obj({key: value for key, value in contract.items() if key != "contract_hash"}), errors, "contract hash mismatch")

    refs = contract.get("redacted_refs", [])
    ref_by_kind = {ref.get("kind"): ref for ref in refs}
    expected_paths = {
        "before": source.get("action_receipt_redaction", {}).get("redacted_before_ref", "").replace("artifact:", ""),
        "after": source.get("action_receipt_redaction", {}).get("redacted_after_ref", "").replace("artifact:", ""),
    }
    expected_files = {"before": BEFORE_PATH, "after": AFTER_PATH}
    expected_values = {"before": before, "after": after}
    for kind in ("before", "after"):
        ref = ref_by_kind.get(kind, {})
        path = expected_files[kind]
        value = expected_values[kind]
        require(ref.get("source_path") == expected_paths[kind], errors, f"{kind} source path mismatch")
        require(ref.get("source_sha256") == sha256_file(path), errors, f"{kind} source sha mismatch")
        require(ref.get("bundle_sha256") == sha256_file(path), errors, f"{kind} bundle sha mismatch")
        require(ref.get("contains_digest_ref") is True, errors, f"{kind} digest ref missing")
        require(f"raw:sha256:{raw_digest}" in canonical_json(value), errors, f"{kind} file lacks digest ref")
        require(ref.get("contains_unredacted_sentinel_prefix") is False, errors, f"{kind} sentinel prefix flagged")
        require(SENTINEL_PREFIX not in canonical_json(value), errors, f"{kind} sentinel prefix present")
        require(ref.get("source_bundle_sha_match") is True, errors, f"{kind} source bundle mismatch")

    bundle = data.get("fresh_bundle", {})
    require(bundle.get("schema") == "FreshContextRedactedReplayBundle/v1", errors, "wrong bundle schema")
    require(bundle.get("manifest_path") == "fixtures/redacted-ref-replay-manifest-pass-0027.json", errors, "wrong manifest path")
    require(bundle.get("manifest_sha256") == sha256_file(MANIFEST_PATH), errors, "manifest sha mismatch")
    require(bundle.get("manifest_seal") == manifest.get("seal"), errors, "manifest seal mismatch")
    require(bundle.get("bundle_storage_boundary") == "TEMP_PRIVATE_NOT_COMMITTED", errors, "wrong bundle storage boundary")
    require(bundle.get("bundle_under_repo") is False, errors, "bundle under repo")
    require(bundle.get("temp_manifest_sha256") == sha256_file(MANIFEST_PATH), errors, "temp manifest sha mismatch")
    require(bundle.get("file_count") == 3, errors, "wrong bundle file count")
    require(bundle.get("bundle_index_hash") == manifest.get("bundle_index_hash"), errors, "bundle index mismatch")

    expected_manifest_seal = sha256_obj({key: value for key, value in manifest.items() if key != "seal"})
    require(manifest.get("seal") == expected_manifest_seal, errors, "manifest seal mismatch")
    require(manifest.get("bundle_under_repo") is False, errors, "manifest bundle under repo")
    require(manifest.get("raw_payload_value_used") is False, errors, "manifest raw value used")
    require(manifest.get("raw_payload_material_available_to_replay") is False, errors, "manifest raw material available")

    policy = data.get("raw_material_policy", {})
    require(policy.get("schema") == "RawMaterialReplayPolicy/v1", errors, "wrong raw material policy schema")
    require(policy.get("raw_payload_value_used") is False, errors, "policy raw value used")
    require(policy.get("raw_payload_material_available_to_replay") is False, errors, "policy raw material available")
    require(policy.get("raw_payload_value_required") is False, errors, "policy raw value required")
    require(policy.get("digest_ref_required") is True, errors, "digest ref not required")
    require(policy.get("redacted_refs_required") is True, errors, "redacted refs not required")
    require(policy.get("sentinel_prefix_sha256") == sha256_text(SENTINEL_PREFIX), errors, "sentinel prefix hash mismatch")
    require(policy.get("sentinel_prefix_allowed_in_model_facing_artifacts") is False, errors, "sentinel prefix allowed")

    leak_scan = data.get("leak_scan", {})
    targets = leak_scan.get("scan_targets", [])
    required_targets = {
        "schemas/redacted-ref-replay-pass-0027.json",
        "fixtures/redacted-ref-replay-manifest-pass-0027.json",
        "fixtures/redacted-before-pass-0026.json",
        "fixtures/redacted-after-pass-0026.json",
        "packets/037-redacted-ref-replay.md",
        "adversarial/pass-0027-redacted-ref-replay-steelman.md",
        "schemas/tool-receipts-pass-0027.json",
        "crucible/pass-0027-thesis.json",
        "crucible/pass-0027-measurements.json",
    }
    require(leak_scan.get("sentinel_prefix_absent_required") is True, errors, "sentinel prefix scan not required")
    require(leak_scan.get("scan_target_count") == len(targets), errors, "scan target count mismatch")
    require(required_targets.issubset(set(targets)), errors, "missing required scan target")
    scanned = []
    sentinel_hits = []
    for target in targets:
        path = ROOT / target
        require(path.exists(), errors, f"scan target missing {target}")
        if path.exists():
            text = path.read_text(encoding="utf-8")
            if SENTINEL_PREFIX in text:
                sentinel_hits.append(target)
            scanned.append(target)
    require(not sentinel_hits, errors, f"sentinel prefix leaks: {sentinel_hits}")

    negatives = data.get("negative_fixtures", [])
    require(data.get("negative_fixture_count") == len(negatives), errors, "negative count mismatch")
    require(len(negatives) >= 9, errors, "expected at least nine negatives")
    require(all(n.get("expected_validator_status") == "REJECT" for n in negatives), errors, "negative not rejected")

    result = {
        "schema": "Pass0027RedactedRefReplayValidatorRun/v1",
        "pass": "0027",
        "status": "MATCH" if not errors else "DRIFT",
        "match": 1 if not errors else 0,
        "drift": 0 if not errors else 1,
        "checks": [
            {
                "artifact": "RedactedRefReplaySet",
                "path": str(SCHEMA_PATH.relative_to(ROOT)),
                "status": "MATCH" if not errors else "DRIFT",
                "source_sha256": source_receipt.get("sha256"),
                "manifest_sha256": bundle.get("manifest_sha256"),
                "redacted_ref_count": contract.get("redacted_ref_count"),
                "negative_fixture_count": len(negatives),
                "scan_target_count": len(scanned),
                "sentinel_prefix_leak_count": len(sentinel_hits),
                "raw_payload_value_used": contract.get("raw_payload_value_used"),
                "errors": errors,
            }
        ],
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
