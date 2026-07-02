"""Validate pass 0019 strict receipt runtime fixtures."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "strict-receipt-runtime-fixtures-pass-0019.json"


def require(condition: bool, errors: list[str], message: str) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    data = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    errors: list[str] = []

    require(data.get("schema") == "StrictReceiptRuntimeFixtureSet/v1", errors, "wrong schema")
    require(data.get("pass") == "0019", errors, "wrong pass")
    require(data.get("status") == "STRICT_RUNTIME_MATCH", errors, "wrong status")
    require(bool(data.get("seal")), errors, "missing seal")
    require("does not import quantum frameworks" in data.get("non_promotion_statement", ""), errors, "missing non-promotion")

    loader = data.get("strict_json_loader_receipt", {})
    require(loader.get("schema") == "StrictJsonLoaderReceipt/v1", errors, "missing strict loader")
    require(loader.get("object_pairs_hook_required") is True, errors, "object_pairs_hook not required")
    require(loader.get("parse_constant_rejects_nonfinite") is True, errors, "parse_constant rejection missing")
    require(loader.get("allow_nan_on_serialization") is False, errors, "allow_nan should be false")
    require(loader.get("positive_fixture", {}).get("expected_validator_status") == "MATCH", errors, "positive fixture not match")
    require(loader.get("duplicate_key_fixture", {}).get("expected_validator_status") == "REJECT", errors, "duplicate fixture not reject")
    require(loader.get("duplicate_key_fixture", {}).get("duplicate_keys") == ["00"], errors, "duplicate key 00 not detected")
    require(all(f.get("expected_validator_status") == "REJECT" for f in loader.get("nonfinite_fixtures", [])), errors, "nonfinite fixture not rejected")

    numeric = data.get("numeric_precision_receipts", [])
    expected_numeric = {
        "decimal-string-exact-0p1",
        "binary-float-expanded-0p1",
        "decimal-quantized-one-seventh",
    }
    require(expected_numeric <= {r.get("receipt_id") for r in numeric}, errors, "missing numeric receipt")
    require(all(r.get("schema") == "NumericPrecisionReceipt/v1" for r in numeric), errors, "numeric schema mismatch")
    require(all(r.get("receipt_hash") for r in numeric), errors, "numeric receipt missing hash")
    require(any(r.get("lossiness") == "ROUNDED_WITH_POLICY" for r in numeric), errors, "missing rounded numeric policy")

    storage = data.get("object_storage_evidence_receipt", {})
    require(storage.get("schema") == "ObjectStorageEvidenceReceipt/v1", errors, "missing storage receipt")
    require(storage.get("uri", "").startswith("s3://"), errors, "storage URI missing")
    require(storage.get("content_sha256"), errors, "storage content hash missing")
    require(storage.get("content_sha256_base64"), errors, "storage base64 hash missing")
    require(storage.get("version_id"), errors, "storage version missing")
    require(storage.get("etag_or_generation"), errors, "storage etag/generation missing")
    require(storage.get("retrieval_timestamp"), errors, "storage retrieval timestamp missing")
    require(storage.get("locator_only_allowed") is False, errors, "locator-only evidence should be false")

    fixtures = data.get("executable_framework_output_fixtures", [])
    expected_fixtures = {
        "executable-fixture-qiskit-counts",
        "executable-fixture-braket-measurement-counts",
        "executable-fixture-cirq-histogram",
        "executable-fixture-pennylane-counts",
        "executable-fixture-qir-result-record-map",
    }
    require(expected_fixtures <= {f.get("fixture_id") for f in fixtures}, errors, "missing executable fixture")
    for fixture in fixtures:
        require(fixture.get("schema") == "ExecutableFrameworkOutputFixture/v1", errors, f"{fixture.get('fixture_id')} wrong schema")
        require(fixture.get("status") == "ADAPTER_EXECUTION_MATCH", errors, f"{fixture.get('fixture_id')} wrong status")
        require(fixture.get("execution_mode") == "LOCAL_ADAPTER_FUNCTION_OVER_SYNTHETIC_OUTPUT", errors, f"{fixture.get('fixture_id')} wrong mode")
        require(fixture.get("framework_imported") is False, errors, f"{fixture.get('fixture_id')} should not import framework")
        require(fixture.get("raw_output_hash"), errors, f"{fixture.get('fixture_id')} missing raw hash")
        require(fixture.get("normalized_output_hash"), errors, f"{fixture.get('fixture_id')} missing normalized hash")
        require(fixture.get("normalized_output", {}).get("normalized_counts"), errors, f"{fixture.get('fixture_id')} missing normalized counts")
        require(str(fixture.get("source_anchor", "")).startswith("https://"), errors, f"{fixture.get('fixture_id')} missing HTTPS source")

    negatives = data.get("negative_fixtures", [])
    expected_negatives = {
        "negative-strict-json-loader-not-used",
        "negative-nan-accepted-as-json-number",
        "negative-decimal-serialized-as-float",
        "negative-object-storage-uri-only",
        "negative-qiskit-fixture-without-layout",
        "negative-braket-fixture-without-measured-qubit-order",
        "negative-cirq-fixture-without-fold-func",
        "negative-pennylane-fixture-without-wire-order",
        "negative-qir-fixture-without-record-map",
    }
    require(expected_negatives <= {n.get("fixture_id") for n in negatives}, errors, "missing negative fixture")
    require(all(n.get("expected_validator_status") == "REJECT" for n in negatives), errors, "negative fixture not rejected")

    anchors = data.get("source_anchors", [])
    require(len(anchors) >= 11, errors, "expected at least eleven source anchors")
    require(all(a.get("url", "").startswith("https://") for a in anchors), errors, "source anchor missing HTTPS")

    result = {
        "schema": "Pass0019StrictReceiptRuntimeValidatorRun/v1",
        "pass": "0019",
        "status": "MATCH" if not errors else "DRIFT",
        "match": 1 if not errors else 0,
        "drift": 0 if not errors else 1,
        "checks": [
            {
                "artifact": "StrictReceiptRuntimeFixtureSet",
                "path": str(SCHEMA_PATH.relative_to(ROOT)),
                "status": "MATCH" if not errors else "DRIFT",
                "numeric_receipt_count": len(numeric),
                "executable_fixture_count": len(fixtures),
                "negative_fixture_count": len(negatives),
                "source_anchor_count": len(anchors),
                "errors": errors,
            }
        ],
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
