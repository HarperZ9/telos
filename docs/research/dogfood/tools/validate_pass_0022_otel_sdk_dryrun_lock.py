"""Validate pass 0022 OTel SDK dry-run lock receipts."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "otel-sdk-dryrun-lock-pass-0022.json"


def require(condition: bool, errors: list[str], message: str) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    data = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    errors: list[str] = []

    require(data.get("schema") == "OTelSdkDryRunLockReceiptSet/v1", errors, "wrong schema")
    require(data.get("pass") == "0022", errors, "wrong pass")
    require(data.get("status") == "OTEL_SDK_DRYRUN_LOCK_MATCH", errors, "wrong status")
    require(bool(data.get("seal")), errors, "missing seal")
    require("does not install opentelemetry-sdk" in data.get("non_promotion_statement", ""), errors, "missing non-promotion")

    dry = data.get("dry_run", {})
    require(dry.get("schema") == "PipDryRunReportReceipt/v1", errors, "wrong dry-run schema")
    require(dry.get("returncode") == 0, errors, "dry-run failed")
    require(dry.get("no_install_boundary") is True, errors, "no-install boundary missing")
    require(dry.get("target_requirement") == "opentelemetry-sdk==1.41.0", errors, "wrong target requirement")
    command = dry.get("command", [])
    require("--dry-run" in command and "--report" in command and "-" in command, errors, "dry-run/report command missing")
    require(dry.get("report_sha256"), errors, "missing report hash")

    resolved = data.get("resolved_install", [])
    by_name = {row.get("name"): row for row in resolved}
    require(data.get("resolved_install_count") == len(resolved), errors, "resolved count mismatch")
    require("opentelemetry-sdk" in by_name, errors, "missing opentelemetry-sdk")
    require("opentelemetry-semantic-conventions" in by_name, errors, "missing semantic conventions")
    sdk = by_name.get("opentelemetry-sdk", {})
    semconv = by_name.get("opentelemetry-semantic-conventions", {})
    require(sdk.get("version") == "1.41.0", errors, "wrong SDK version")
    require(sdk.get("requested") is True, errors, "SDK should be requested")
    require(sdk.get("sha256") == "a596f5687964a3e0d7f8edfdcf5b79cbca9c93c7025ebf5fb00f398a9443b0bd", errors, "SDK hash mismatch")
    require("opentelemetry-api==1.41.0" in sdk.get("requires_dist", []), errors, "SDK should require matching API")
    require(semconv.get("version") == "0.62b0", errors, "wrong semconv version")
    require(semconv.get("requested") is False, errors, "semconv should be transitive")
    require(semconv.get("sha256") == "0ddac1ce59eaf1a827d9987ab60d9315fb27aea23304144242d1fcad9e16b489", errors, "semconv hash mismatch")

    already = data.get("already_satisfied", [])
    require(any(row.get("name") == "opentelemetry-api" and row.get("version") == "1.41.0" for row in already), errors, "missing already satisfied API")

    post = data.get("post_dryrun_import_audit", {})
    require(post.get("schema") == "PostDryRunImportAudit/v1", errors, "wrong post audit schema")
    require(post.get("find_spec_available") is False, errors, "SDK should remain unavailable after dry run")
    require(post.get("install_performed") is False, errors, "dry run must not install")
    require(post.get("expected_status") == "NOT_INSTALLED_AFTER_DRY_RUN", errors, "wrong post dry-run status")

    env = data.get("environment", {})
    require(env.get("python_full_version") == "3.12.10", errors, "unexpected Python full version")
    require(env.get("sys_platform") == "win32", errors, "unexpected sys platform")

    negatives = data.get("negative_fixtures", [])
    require(data.get("negative_fixture_count") == len(negatives), errors, "negative count mismatch")
    require(len(negatives) >= 5, errors, "expected at least five negatives")
    require(all(n.get("expected_validator_status") == "REJECT" for n in negatives), errors, "negative fixture not rejected")

    anchors = data.get("source_anchors", [])
    require(len(anchors) >= 4, errors, "expected at least four source anchors")
    require(all(str(anchor.get("url", "")).startswith("https://") for anchor in anchors), errors, "source anchor not HTTPS")

    result = {
        "schema": "Pass0022OTelSdkDryRunLockValidatorRun/v1",
        "pass": "0022",
        "status": "MATCH" if not errors else "DRIFT",
        "match": 1 if not errors else 0,
        "drift": 0 if not errors else 1,
        "checks": [
            {
                "artifact": "OTelSdkDryRunLockReceiptSet",
                "path": str(SCHEMA_PATH.relative_to(ROOT)),
                "status": "MATCH" if not errors else "DRIFT",
                "resolved_install_count": len(resolved),
                "negative_fixture_count": len(negatives),
                "invalid_distribution_warning_count": dry.get("invalid_distribution_warning_count"),
                "post_dryrun_sdk_available": post.get("find_spec_available"),
                "errors": errors,
            }
        ],
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
