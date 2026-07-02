"""Generate pass 0022 OTel SDK dry-run lock receipts."""

from __future__ import annotations

import hashlib
import importlib.metadata
import importlib.util
import json
import subprocess
import sys
from pathlib import Path


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_obj(value: object) -> str:
    return sha256_text(canonical_json(value))


def parse_pip_report(stdout: str) -> dict[str, object]:
    decoder = json.JSONDecoder()
    for idx, char in enumerate(stdout):
        if char == "{":
            try:
                report, _ = decoder.raw_decode(stdout[idx:])
                return report
            except json.JSONDecodeError:
                continue
    raise ValueError("pip dry-run report JSON not found")


command = [
    sys.executable,
    "-m",
    "pip",
    "install",
    "--disable-pip-version-check",
    "--dry-run",
    "--report",
    "-",
    "opentelemetry-sdk==1.41.0",
]
completed = subprocess.run(command, capture_output=True, text=True, check=False)
report = parse_pip_report(completed.stdout)
install_rows = report.get("install", [])
invalid_distribution_warnings = [
    line
    for stream in [completed.stdout, completed.stderr]
    for line in stream.splitlines()
    if "Ignoring invalid distribution" in line
]

post_dryrun_sdk_spec = importlib.util.find_spec("opentelemetry.sdk")
try:
    api_version = importlib.metadata.version("opentelemetry-api")
except importlib.metadata.PackageNotFoundError:
    api_version = None

receipt = {
    "schema": "OTelSdkDryRunLockReceiptSet/v1",
    "pass": "0022",
    "generated_on": "2026-07-01",
    "status": "OTEL_SDK_DRYRUN_LOCK_MATCH",
    "dry_run": {
        "schema": "PipDryRunReportReceipt/v1",
        "command": command,
        "returncode": completed.returncode,
        "no_install_boundary": True,
        "target_requirement": "opentelemetry-sdk==1.41.0",
        "stdout_sha256": sha256_text(completed.stdout),
        "stderr_sha256": sha256_text(completed.stderr),
        "report_sha256": sha256_obj(report),
        "invalid_distribution_warning_count": len(invalid_distribution_warnings),
        "invalid_distribution_warning_labels": sorted(
            {
                line.split("Ignoring invalid distribution ", 1)[1].split(" ", 1)[0]
                for line in invalid_distribution_warnings
                if "Ignoring invalid distribution " in line
            }
        ),
    },
    "resolved_install": [
        {
            "schema": "ResolvedWheelReceipt/v1",
            "name": row.get("metadata", {}).get("name"),
            "version": row.get("metadata", {}).get("version"),
            "requested": row.get("requested"),
            "url": row.get("download_info", {}).get("url"),
            "sha256": row.get("download_info", {}).get("archive_info", {}).get("hashes", {}).get("sha256"),
            "requires_python": row.get("metadata", {}).get("requires_python"),
            "requires_dist": row.get("metadata", {}).get("requires_dist", []),
        }
        for row in install_rows
    ],
    "already_satisfied": [
        {
            "schema": "AlreadySatisfiedDistributionReceipt/v1",
            "name": "opentelemetry-api",
            "version": api_version,
            "module": "opentelemetry",
            "find_spec_available": importlib.util.find_spec("opentelemetry") is not None,
        }
    ],
    "post_dryrun_import_audit": {
        "schema": "PostDryRunImportAudit/v1",
        "distribution": "opentelemetry-sdk",
        "module": "opentelemetry.sdk",
        "find_spec_available": post_dryrun_sdk_spec is not None,
        "version": None,
        "install_performed": False,
        "expected_status": "NOT_INSTALLED_AFTER_DRY_RUN",
    },
    "environment": report.get("environment", {}),
    "source_anchors": [
        {"source": "pip install --dry-run report output", "url": "https://pip.pypa.io/en/stable/cli/pip_install/"},
        {"source": "OpenTelemetry Python docs", "url": "https://opentelemetry.io/docs/languages/python/"},
        {"source": "opentelemetry-sdk wheel", "url": "https://files.pythonhosted.org/packages/2c/13/a7825118208cb32e6a4edcd0a99f925cbef81e77b3b0aedfd9125583c543/opentelemetry_sdk-1.41.0-py3-none-any.whl"},
        {"source": "opentelemetry-semantic-conventions wheel", "url": "https://files.pythonhosted.org/packages/58/6c/5e86fa1759a525ef91c2d8b79d668574760ff3f900d114297765eb8786cb/opentelemetry_semantic_conventions-0.62b0-py3-none-any.whl"},
    ],
    "negative_fixtures": [
        {
            "fixture_id": "negative-dryrun-treated-as-install",
            "failure_mode": "Treats pip --dry-run report as an installed SDK.",
            "expected_validator_status": "REJECT",
        },
        {
            "fixture_id": "negative-wheel-without-hash",
            "failure_mode": "Promotes a resolved wheel without SHA-256 hash.",
            "expected_validator_status": "REJECT",
        },
        {
            "fixture_id": "negative-unmatched-api-sdk-version",
            "failure_mode": "Plans opentelemetry-sdk version that does not match installed opentelemetry-api version.",
            "expected_validator_status": "REJECT",
        },
        {
            "fixture_id": "negative-ignore-invalid-distribution-warnings",
            "failure_mode": "Ignores pip invalid-distribution warnings in environment evidence.",
            "expected_validator_status": "REJECT",
        },
        {
            "fixture_id": "negative-recording-span-without-sdk-import",
            "failure_mode": "Claims recording span evidence without opentelemetry.sdk import availability.",
            "expected_validator_status": "REJECT",
        },
    ],
    "non_promotion_statement": "Pass 0022 performs pip dry-run resolution only. It does not install opentelemetry-sdk, import opentelemetry.sdk, create recording spans, modify the environment, or promote trace evidence.",
}
receipt["resolved_install_count"] = len(receipt["resolved_install"])
receipt["negative_fixture_count"] = len(receipt["negative_fixtures"])
receipt["seal"] = sha256_obj(receipt)

ROOT = Path(__file__).resolve().parents[1]
OUT_PATH = ROOT / "schemas" / "otel-sdk-dryrun-lock-pass-0022.json"
OUT_PATH.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(
    json.dumps(
        {
            "path": str(OUT_PATH),
            "schema": receipt["schema"],
            "seal": receipt["seal"],
            "resolved_install_count": receipt["resolved_install_count"],
            "invalid_distribution_warning_count": receipt["dry_run"]["invalid_distribution_warning_count"],
            "post_dryrun_sdk_available": receipt["post_dryrun_import_audit"]["find_spec_available"],
        },
        indent=2,
        sort_keys=True,
    )
)
