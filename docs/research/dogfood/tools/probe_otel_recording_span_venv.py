"""Generate pass 0023 isolated OTel SDK recording-span receipts."""

from __future__ import annotations

import hashlib
import importlib.metadata
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


PASS = "0023"
ROOT = Path(__file__).resolve().parents[1]
OUT_PATH = ROOT / "schemas" / "otel-recording-span-venv-pass-0023.json"
REPORT_PATH = Path(tempfile.gettempdir()) / "telos-dogfood-otel-sdk-0023-install-report.json"
VENV_DIR = Path(os.environ.get("TELOS_DOGFOOD_OTEL_VENV", Path(tempfile.gettempdir()) / "telos-dogfood-otel-sdk-0023"))


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_obj(value: object) -> str:
    return sha256_text(canonical_json(value))


def run(command: list[str]) -> dict[str, object]:
    completed = subprocess.run(command, capture_output=True, text=True, check=False)
    return {
        "command": command,
        "returncode": completed.returncode,
        "stdout_sha256": sha256_text(completed.stdout),
        "stderr_sha256": sha256_text(completed.stderr),
        "stdout_tail": completed.stdout.splitlines()[-8:],
        "stderr_tail": completed.stderr.splitlines()[-8:],
    }


def distribution_version(name: str) -> str | None:
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return None


def base_sdk_available() -> bool:
    return importlib.util.find_spec("opentelemetry.sdk") is not None


def venv_python_path() -> Path:
    if os.name == "nt":
        return VENV_DIR / "Scripts" / "python.exe"
    return VENV_DIR / "bin" / "python"


def load_report(path: Path) -> dict[str, object]:
    if not path.exists():
        return {"install": [], "missing": True}
    return json.loads(path.read_text(encoding="utf-8"))


def resolved_rows(report: dict[str, object]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for row in report.get("install", []):
        metadata = row.get("metadata", {})
        archive_info = row.get("download_info", {}).get("archive_info", {})
        rows.append(
            {
                "schema": "ResolvedWheelReceipt/v1",
                "name": metadata.get("name"),
                "version": metadata.get("version"),
                "requested": row.get("requested"),
                "url": row.get("download_info", {}).get("url"),
                "sha256": archive_info.get("hashes", {}).get("sha256"),
                "hash": archive_info.get("hash"),
                "requires_python": metadata.get("requires_python"),
                "requires_dist": metadata.get("requires_dist", []),
            }
        )
    return rows


def generate_span_fixture(python_exe: Path) -> dict[str, object]:
    snippet = r'''
import hashlib
import importlib.metadata as metadata
import json
import platform
import sys

from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter


def canonical_json(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


exporter = InMemorySpanExporter()
provider = TracerProvider(
    resource=Resource.create(
        {
            "service.name": "telos-dogfood-pass-0023",
            "telos.pass": "0023",
            "telos.export.boundary": "in-memory-only",
        }
    )
)
provider.add_span_processor(SimpleSpanProcessor(exporter))
tracer = provider.get_tracer("telos.dogfood.pass0023", "0.1.0")

span_was_recording = None
with tracer.start_as_current_span("telos.action.receipt.fixture") as span:
    span_was_recording = span.is_recording()
    span.set_attribute("telos.pass", "0023")
    span.set_attribute("telos.action", "recording-span-fixture")
    span.set_attribute("telos.receipt.kind", "OpenTelemetryRecordingSpanFixture/v1")
    span.set_attribute("telos.no_cloud_export", True)

finished = exporter.get_finished_spans()
first = finished[0]
ctx = first.get_span_context()
sink = {
    "span_count": len(finished),
    "span_name": first.name,
    "trace_id_hex": f"{ctx.trace_id:032x}",
    "span_id_hex": f"{ctx.span_id:016x}",
    "trace_flags": int(ctx.trace_flags),
    "attributes": dict(first.attributes),
    "resource_attributes": dict(first.resource.attributes),
    "status_code": first.status.status_code.name,
}
payload = {
    "python_executable": sys.executable,
    "python_version": sys.version.split()[0],
    "platform": platform.platform(),
    "api_version": metadata.version("opentelemetry-api"),
    "sdk_version": metadata.version("opentelemetry-sdk"),
    "semantic_conventions_version": metadata.version("opentelemetry-semantic-conventions"),
    "exporter_class": exporter.__class__.__name__,
    "span_processor_class": "SimpleSpanProcessor",
    "span_was_recording_inside_context": span_was_recording,
    "finished_span_count": len(finished),
    "trace_id_hex": sink["trace_id_hex"],
    "span_id_hex": sink["span_id_hex"],
    "span_name": first.name,
    "attributes": sink["attributes"],
    "resource_attributes": sink["resource_attributes"],
    "exporter_sink_hash": hashlib.sha256(canonical_json(sink).encode("utf-8")).hexdigest(),
}
payload["fixture_hash"] = hashlib.sha256(canonical_json(payload).encode("utf-8")).hexdigest()
print(json.dumps(payload, sort_keys=True))
'''
    completed = subprocess.run([str(python_exe), "-c", snippet], capture_output=True, text=True, check=False)
    fixture: dict[str, object] = {
        "command": [str(python_exe), "-c", "<otel-recording-span-fixture>"],
        "returncode": completed.returncode,
        "stdout_sha256": sha256_text(completed.stdout),
        "stderr_sha256": sha256_text(completed.stderr),
        "stderr_tail": completed.stderr.splitlines()[-8:],
    }
    if completed.returncode == 0:
        fixture.update(json.loads(completed.stdout))
    return fixture


base_before = {
    "schema": "BaseInterpreterImportAudit/v1",
    "python_executable": sys.executable,
    "python_version": sys.version.split()[0],
    "opentelemetry_api_version": distribution_version("opentelemetry-api"),
    "opentelemetry_sdk_available": base_sdk_available(),
}

VENV_DIR.parent.mkdir(parents=True, exist_ok=True)
python_exe = venv_python_path()
venv_create = {
    "command": [sys.executable, "-m", "venv", str(VENV_DIR)],
    "returncode": 0,
    "stdout_sha256": sha256_text(""),
    "stderr_sha256": sha256_text(""),
    "stdout_tail": [],
    "stderr_tail": [],
    "skipped": python_exe.exists(),
}
if not python_exe.exists():
    venv_create = run([sys.executable, "-m", "venv", str(VENV_DIR)])

install_command = [
    str(python_exe),
    "-m",
    "pip",
    "install",
    "--disable-pip-version-check",
    "--force-reinstall",
    "--report",
    str(REPORT_PATH),
    "opentelemetry-api==1.41.0",
    "opentelemetry-sdk==1.41.0",
    "opentelemetry-semantic-conventions==0.62b0",
    "typing-extensions==4.15.0",
]
install = run(install_command) if python_exe.exists() else {"command": install_command, "returncode": 127}
report = load_report(REPORT_PATH)
span_fixture = generate_span_fixture(python_exe) if install.get("returncode") == 0 else {"returncode": 127}

base_after = {
    "schema": "BaseInterpreterImportAudit/v1",
    "python_executable": sys.executable,
    "python_version": sys.version.split()[0],
    "opentelemetry_api_version": distribution_version("opentelemetry-api"),
    "opentelemetry_sdk_available": base_sdk_available(),
}

receipt = {
    "schema": "OTelRecordingSpanVenvReceiptSet/v1",
    "pass": PASS,
    "generated_on": "2026-07-01",
    "status": "OTEL_RECORDING_SPAN_VENV_MATCH" if span_fixture.get("returncode") == 0 else "OTEL_RECORDING_SPAN_VENV_FAILED",
    "base_environment_before": base_before,
    "venv": {
        "schema": "IsolatedVenvReceipt/v1",
        "path": str(VENV_DIR),
        "path_sha256": sha256_text(str(VENV_DIR)),
        "python_executable": str(python_exe),
        "python_executable_sha256": sha256_text(str(python_exe)),
        "create": venv_create,
        "boundary": "TEMP_ISOLATED_ENV_DO_NOT_COMMIT",
    },
    "install": {
        "schema": "PipInstallReportReceipt/v1",
        "command": install_command,
        "returncode": install.get("returncode"),
        "stdout_sha256": install.get("stdout_sha256"),
        "stderr_sha256": install.get("stderr_sha256"),
        "stdout_tail": install.get("stdout_tail", []),
        "stderr_tail": install.get("stderr_tail", []),
        "report_path_sha256": sha256_text(str(REPORT_PATH)),
        "report_sha256": sha256_obj(report),
        "resolved": resolved_rows(report),
    },
    "recording_span_fixture": {
        "schema": "OpenTelemetryRecordingSpanFixture/v1",
        "status": "RECORDING_SPAN_EXPORTED_IN_MEMORY" if span_fixture.get("returncode") == 0 else "FAILED",
        "sdk_imported": span_fixture.get("returncode") == 0,
        "no_network_export": True,
        **span_fixture,
    },
    "base_environment_after": base_after,
    "action_receipt_bridge": {
        "schema": "TelosActionReceiptBridgeSketch/v1",
        "status": "BRIDGE_FIXTURE_READY_NOT_TELOS_RUNTIME",
        "internal_tool": "telos.action.receipt",
        "inputs": [
            "source packet digest",
            "operator action label",
            "tool command receipt",
            "OpenTelemetryRecordingSpanFixture/v1",
        ],
        "outputs": [
            "action receipt id",
            "trace id",
            "span id",
            "exporter sink hash",
            "validator verdict",
        ],
        "verification_layer": [
            "nonzero trace id",
            "nonzero span id",
            "finished span count",
            "receipt hash binding",
            "base interpreter non-mutation audit",
        ],
        "market_facing_product": "agent action proof packet with portable OTel bridge",
    },
    "source_anchors": [
        {"source": "OpenTelemetry Python getting started", "url": "https://opentelemetry.io/docs/languages/python/getting-started/"},
        {"source": "OpenTelemetry Python instrumentation", "url": "https://opentelemetry.io/docs/languages/python/instrumentation/"},
        {"source": "OpenTelemetry Python trace API", "url": "https://opentelemetry-python.readthedocs.io/en/latest/api/trace.html"},
        {"source": "pip install report option", "url": "https://pip.pypa.io/en/stable/cli/pip_install/"},
    ],
    "negative_fixtures": [
        {
            "fixture_id": "negative-base-env-sdk-mutation",
            "failure_mode": "The shared base interpreter gains opentelemetry.sdk availability.",
            "expected_validator_status": "REJECT",
        },
        {
            "fixture_id": "negative-zero-trace-or-span-id",
            "failure_mode": "A recording span fixture reports an all-zero trace id or span id.",
            "expected_validator_status": "REJECT",
        },
        {
            "fixture_id": "negative-nonrecording-span-promoted",
            "failure_mode": "A NonRecordingSpan is promoted as exported trace evidence.",
            "expected_validator_status": "REJECT",
        },
        {
            "fixture_id": "negative-cloud-exporter-claim",
            "failure_mode": "The pass claims cloud/provider export without a live exporter receipt.",
            "expected_validator_status": "REJECT",
        },
        {
            "fixture_id": "negative-missing-exporter-sink-hash",
            "failure_mode": "The span fixture lacks a hash of the exporter sink payload.",
            "expected_validator_status": "REJECT",
        },
        {
            "fixture_id": "negative-otel-version-drift",
            "failure_mode": "The installed OTel API, SDK, or semantic-conventions version drifts from the pinned plan.",
            "expected_validator_status": "REJECT",
        },
    ],
    "non_promotion_statement": "Pass 0023 proves only an isolated local OpenTelemetry SDK recording-span fixture and a bridge sketch. It does not prove Telos runtime integration, cloud trace export, live agent safety, scientific discovery, theorem proof, or any natural law.",
}
receipt["resolved_install_count"] = len(receipt["install"]["resolved"])
receipt["negative_fixture_count"] = len(receipt["negative_fixtures"])
receipt["source_anchor_count"] = len(receipt["source_anchors"])
receipt["seal"] = sha256_obj(receipt)

OUT_PATH.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(
    json.dumps(
        {
            "path": str(OUT_PATH),
            "schema": receipt["schema"],
            "status": receipt["status"],
            "seal": receipt["seal"],
            "resolved_install_count": receipt["resolved_install_count"],
            "finished_span_count": receipt["recording_span_fixture"].get("finished_span_count"),
            "base_sdk_available_after": receipt["base_environment_after"]["opentelemetry_sdk_available"],
        },
        indent=2,
        sort_keys=True,
    )
)
