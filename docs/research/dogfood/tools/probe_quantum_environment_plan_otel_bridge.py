"""Generate pass 0021 quantum environment plan and OTel bridge receipts."""

from __future__ import annotations

import hashlib
import importlib.metadata
import json
import platform
import sys
from pathlib import Path


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_obj(value: object) -> str:
    return sha256_text(canonical_json(value))


SOURCE_ANCHORS = [
    {"source": "IBM Quantum install Qiskit", "url": "https://quantum.cloud.ibm.com/docs/guides/install-qiskit"},
    {"source": "IBM Quantum install Qiskit Runtime", "url": "https://quantum.cloud.ibm.com/docs/guides/install-qiskit-runtime"},
    {"source": "Amazon Braket Python SDK docs", "url": "https://amazon-braket-sdk-python.readthedocs.io/"},
    {"source": "Amazon Braket getting started", "url": "https://aws.amazon.com/braket/getting-started/"},
    {"source": "Cirq install docs", "url": "https://quantumai.google/cirq/start/install"},
    {"source": "PennyLane install", "url": "https://pennylane.ai/install"},
    {"source": "PennyLane installation dependencies", "url": "https://docs.pennylane.ai/en/stable/development/guide/installation.html"},
    {"source": "PyQIR documentation", "url": "https://www.qir-alliance.org/pyqir/"},
    {"source": "pytket install docs", "url": "https://docs.quantinuum.com/tket/api-docs/install.html"},
    {"source": "pytket QIR extension docs", "url": "https://docs.quantinuum.com/tket/extensions/pytket-qir/"},
    {"source": "NVIDIA CUDA-Q quick start", "url": "https://nvidia.github.io/cuda-quantum/latest/using/quick_start.html"},
    {"source": "pip install docs", "url": "https://pip.pypa.io/en/stable/cli/pip_install/"},
    {"source": "OpenTelemetry Python docs", "url": "https://opentelemetry.io/docs/languages/python/"},
    {"source": "OpenTelemetry trace API docs", "url": "https://opentelemetry-python.readthedocs.io/en/latest/api/trace.html"},
    {"source": "OpenTelemetry trace API spec", "url": "https://opentelemetry.io/docs/specs/otel/trace/api/"},
]


def package_plan(
    distribution: str,
    import_targets: list[str],
    install_command: str,
    source_urls: list[str],
    fixture_contract: str,
    notes: list[str] | None = None,
) -> dict[str, object]:
    plan = {
        "schema": "QuantumFrameworkPackagePlan/v1",
        "distribution": distribution,
        "import_targets": import_targets,
        "install_command": install_command,
        "pin_policy": "RESOLVE_IN_ISOLATED_ENV_THEN_FREEZE_WITH_HASHES",
        "install_now": False,
        "cloud_credentials_required_for_import_fixture": False,
        "cloud_credentials_required_for_live_provider_fixture": distribution in {"qiskit-ibm-runtime", "amazon-braket-sdk"},
        "source_anchors": source_urls,
        "first_framework_import_fixture": fixture_contract,
        "notes": notes or [],
        "promotion_state_after_install": "FRAMEWORK_IMPORT_FIXTURE_ELIGIBLE",
    }
    plan["plan_hash"] = sha256_obj(plan)
    return plan


PACKAGE_PLANS = [
    package_plan(
        "qiskit",
        ["qiskit", "qiskit.circuit"],
        "python -m pip install qiskit",
        ["https://quantum.cloud.ibm.com/docs/guides/install-qiskit", "https://pypi.org/project/qiskit/"],
        "Create a two-qubit Bell circuit and emit source/circuit/canonical-count layout receipts without provider execution.",
    ),
    package_plan(
        "qiskit-ibm-runtime",
        ["qiskit_ibm_runtime"],
        "python -m pip install qiskit-ibm-runtime",
        ["https://quantum.cloud.ibm.com/docs/guides/install-qiskit-runtime", "https://quantum.cloud.ibm.com/docs/api/qiskit-ibm-runtime"],
        "Import runtime client classes and create a metadata-only client-shape receipt; no token, account, session, or job execution.",
        ["Live provider fixture requires credentials and a separate live-provider receipt gate."],
    ),
    package_plan(
        "amazon-braket-sdk",
        ["braket", "braket.circuits"],
        "python -m pip install amazon-braket-sdk",
        ["https://amazon-braket-sdk-python.readthedocs.io/", "https://aws.amazon.com/braket/getting-started/"],
        "Create a local Braket Circuit object and parse local/synthetic measurement count shape; no AWS task execution.",
        ["Live provider fixture requires AWS account configuration and separate task receipt."],
    ),
    package_plan(
        "cirq",
        ["cirq"],
        "python -m pip install cirq",
        ["https://quantumai.google/cirq/start/install", "https://quantumai.google/cirq"],
        "Create a Bell circuit with cirq.LineQubit objects and local simulator/result canonicalization.",
    ),
    package_plan(
        "pennylane",
        ["pennylane"],
        "python -m pip install pennylane",
        ["https://pennylane.ai/install", "https://docs.pennylane.ai/en/stable/development/guide/installation.html"],
        "Create default.qubit QNode with fixed shots and wire-order receipt.",
    ),
    package_plan(
        "pyqir",
        ["pyqir"],
        "python -m pip install pyqir",
        ["https://www.qir-alliance.org/pyqir/", "https://github.com/qir-alliance/pyqir"],
        "Create or parse a minimal QIR module and emit result-record-map receipt.",
    ),
    package_plan(
        "pytket",
        ["pytket"],
        "python -m pip install pytket",
        ["https://docs.quantinuum.com/tket/api-docs/install.html", "https://docs.quantinuum.com/tket/api-docs/getting_started.html"],
        "Create a pytket Circuit and emit compiler/routing metadata receipt without backend execution.",
    ),
    package_plan(
        "pytket-qir",
        ["pytket.extensions.qir"],
        "python -m pip install pytket-qir",
        ["https://docs.quantinuum.com/tket/extensions/pytket-qir/"],
        "Convert a local pytket circuit to QIR and bind QIR hash to the framework-import fixture.",
    ),
    package_plan(
        "cudaq",
        ["cudaq"],
        "python -m pip install cudaq",
        ["https://nvidia.github.io/cuda-quantum/latest/using/quick_start.html", "https://developer.nvidia.com/cuda-q"],
        "Import CUDA-Q and run a CPU/local simulator fixture if available; GPU acceleration must be separately detected.",
        ["Do not assume GPU acceleration from package import."],
    ),
    package_plan(
        "opentelemetry-api",
        ["opentelemetry", "opentelemetry.trace"],
        "python -m pip install opentelemetry-api",
        ["https://opentelemetry.io/docs/languages/python/", "https://opentelemetry-python.readthedocs.io/en/latest/api/trace.html"],
        "Map local tool/action spans to Telos ActionReceipt/v1; API-only spans remain non-recording without SDK/exporter.",
    ),
    package_plan(
        "opentelemetry-sdk",
        ["opentelemetry.sdk"],
        "python -m pip install opentelemetry-sdk",
        ["https://opentelemetry.io/docs/languages/python/", "https://opentelemetry.io/docs/languages/python/instrumentation/"],
        "Create a local in-memory recording span fixture with resource and attribute receipts.",
        ["Separate from opentelemetry-api; not present in pass 0020 audit."],
    ),
]


def opentelemetry_bridge_fixture() -> dict[str, object]:
    from opentelemetry import trace

    version = importlib.metadata.version("opentelemetry-api")
    tracer = trace.get_tracer("telos.pass0021", "0.1")
    span = tracer.start_span("telos.synthetic_action_bridge")
    span.set_attribute("telos.pass", "0021")
    span.set_attribute("telos.action.kind", "quantum_proof_demo_environment_plan")
    span.set_attribute("telos.promotion_state", "FRAMEWORK_IMPORT_FIXTURE_PLANNED")
    span_context = span.get_span_context()
    fixture = {
        "schema": "OpenTelemetryActionBridgeFixture/v1",
        "distribution": "opentelemetry-api",
        "module_imported": True,
        "sdk_installed": False,
        "api_version": version,
        "tracer_name": "telos.pass0021",
        "span_name": "telos.synthetic_action_bridge",
        "span_class": type(span).__name__,
        "is_recording": span.is_recording(),
        "trace_id_hex": format(span_context.trace_id, "032x"),
        "span_id_hex": format(span_context.span_id, "016x"),
        "trace_flags_int": int(span_context.trace_flags),
        "trace_state": str(span_context.trace_state),
        "attributes_attempted": [
            "telos.pass",
            "telos.action.kind",
            "telos.promotion_state",
        ],
        "attribute_recording_status": "NOT_RECORDED_WITH_API_ONLY_NONRECORDING_SPAN",
        "action_receipt_mapping": {
            "span.name": "action.name",
            "trace_id_hex": "action.trace_id",
            "span_id_hex": "action.span_id",
            "telos.action.kind": "action.kind",
            "telos.promotion_state": "action.promotion_state",
        },
        "source_anchors": [
            "https://opentelemetry.io/docs/languages/python/",
            "https://opentelemetry-python.readthedocs.io/en/latest/api/trace.html",
            "https://opentelemetry.io/docs/specs/otel/trace/api/",
        ],
        "status": "API_IMPORT_MATCH_NONRECORDING",
    }
    span.end()
    fixture["fixture_hash"] = sha256_obj(fixture)
    return fixture


negative_fixtures = [
    ("negative-installing-into-shared-base-env", "Installs quantum SDKs into the shared base environment without an environment receipt."),
    ("negative-unpinned-runtime-demo", "Runs a framework demo without resolving and freezing dependency versions and hashes."),
    ("negative-cloud-credential-required-for-import-fixture", "Requires IBM/AWS/cloud credentials for a framework-import fixture."),
    ("negative-sdk-import-claimed-as-provider-execution", "Treats SDK import success as a cloud/provider execution receipt."),
    ("negative-nonrecording-otel-span-claimed-as-exported-trace", "Treats an API-only NonRecordingSpan as exported trace evidence."),
    ("negative-cudaq-import-claimed-as-gpu-acceleration", "Treats CUDA-Q import success as GPU acceleration evidence."),
    ("negative-qir-without-record-map", "Creates QIR fixture without result record map or IR hash."),
    ("negative-buildlang-runtime-without-compiler-receipt", "Claims BuildLang/buildc runtime proof without compiler/runtime receipt."),
    ("negative-color-runtime-without-measurement-receipt", "Claims color/rendering proof without measured-output receipt."),
]


record = {
    "schema": "QuantumFrameworkEnvironmentPlanSet/v1",
    "pass": "0021",
    "generated_on": "2026-07-01",
    "status": "ENVIRONMENT_PLAN_AND_OTEL_BRIDGE_MATCH",
    "local_environment": {
        "schema": "LocalPythonEnvironmentReceipt/v1",
        "python_version": platform.python_version(),
        "python_executable_hash": sha256_text(sys.executable),
        "platform": platform.platform(),
        "pip_version": importlib.metadata.version("pip"),
        "installer_boundary": "PLAN_ONLY_NO_PACKAGE_INSTALL",
    },
    "package_plans": PACKAGE_PLANS,
    "promotion_gates": [
        "ISOLATED_ENVIRONMENT_REQUIRED",
        "RESOLVE_AND_FREEZE_WITH_HASHES_REQUIRED",
        "NO_CLOUD_CREDENTIALS_FOR_FRAMEWORK_IMPORT_FIXTURES",
        "NO_CLOUD_PROVIDER_EXECUTION_WITHOUT_LIVE_PROVIDER_RECEIPT",
        "SDK_IMPORT_DOES_NOT_PROVE_PROVIDER_EXECUTION",
        "OTEL_API_NONRECORDING_SPAN_DOES_NOT_PROVE_EXPORTED_TRACE",
        "BUILD_RUNTIME_RECEIPTS_REQUIRED_FOR_BUILDLANG_PROMOTION",
        "MEASURED_OUTPUT_RECEIPTS_REQUIRED_FOR_COLOR_RENDERING_PROMOTION",
    ],
    "opentelemetry_action_bridge_fixture": opentelemetry_bridge_fixture(),
    "quantum_proof_demo_contract": {
        "schema": "QuantumProofDemoContract/v1",
        "packet_layers": [
            "source_anchor_receipts",
            "workspace_context_receipt",
            "framework_import_receipt",
            "circuit_or_program_receipt",
            "canonical_result_receipt",
            "negative_fixture_receipts",
            "otel_action_bridge_receipt",
            "crucible_verdict_receipt",
        ],
        "public_demo_scope": "local framework import and simulator/result canonicalization only until live-provider receipts exist",
        "shared_runtime_extension": "same packet layers can wrap BuildLang/buildc numeric kernels and Build Color measurement kernels",
    },
    "negative_fixtures": [
        {"fixture_id": fixture_id, "failure_mode": failure_mode, "expected_validator_status": "REJECT"}
        for fixture_id, failure_mode in negative_fixtures
    ],
    "source_anchors": SOURCE_ANCHORS,
    "non_promotion_statement": "Pass 0021 imports opentelemetry-api only because it is already present locally. It does not install quantum SDKs, import unavailable quantum frameworks, create cloud credentials, run provider jobs, run quantum hardware, or promote scientific results.",
}
record["package_plan_count"] = len(PACKAGE_PLANS)
record["negative_fixture_count"] = len(record["negative_fixtures"])
record["source_anchor_count"] = len(SOURCE_ANCHORS)
record["seal"] = sha256_obj(record)

ROOT = Path(__file__).resolve().parents[1]
OUT_PATH = ROOT / "schemas" / "quantum-environment-plan-otel-bridge-pass-0021.json"
OUT_PATH.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(
    json.dumps(
        {
            "path": str(OUT_PATH),
            "schema": record["schema"],
            "seal": record["seal"],
            "package_plan_count": record["package_plan_count"],
            "negative_fixture_count": record["negative_fixture_count"],
            "source_anchor_count": record["source_anchor_count"],
            "otel_status": record["opentelemetry_action_bridge_fixture"]["status"],
        },
        indent=2,
        sort_keys=True,
    )
)
