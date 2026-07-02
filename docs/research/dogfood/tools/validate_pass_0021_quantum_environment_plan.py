"""Validate pass 0021 quantum environment plan and OTel bridge receipts."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "quantum-environment-plan-otel-bridge-pass-0021.json"


def require(condition: bool, errors: list[str], message: str) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    data = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    errors: list[str] = []

    require(data.get("schema") == "QuantumFrameworkEnvironmentPlanSet/v1", errors, "wrong schema")
    require(data.get("pass") == "0021", errors, "wrong pass")
    require(data.get("status") == "ENVIRONMENT_PLAN_AND_OTEL_BRIDGE_MATCH", errors, "wrong status")
    require(bool(data.get("seal")), errors, "missing seal")
    require("does not install quantum SDKs" in data.get("non_promotion_statement", ""), errors, "missing non-promotion")

    env = data.get("local_environment", {})
    require(env.get("schema") == "LocalPythonEnvironmentReceipt/v1", errors, "wrong env schema")
    require(env.get("python_version"), errors, "missing python version")
    require(env.get("pip_version"), errors, "missing pip version")
    require(env.get("installer_boundary") == "PLAN_ONLY_NO_PACKAGE_INSTALL", errors, "installer boundary mismatch")

    plans = data.get("package_plans", [])
    required = {
        "qiskit",
        "qiskit-ibm-runtime",
        "amazon-braket-sdk",
        "cirq",
        "pennylane",
        "pyqir",
        "pytket",
        "pytket-qir",
        "cudaq",
        "opentelemetry-api",
        "opentelemetry-sdk",
    }
    require(data.get("package_plan_count") == len(plans), errors, "package plan count mismatch")
    require(required <= {p.get("distribution") for p in plans}, errors, "missing required package plan")
    for plan in plans:
        label = plan.get("distribution", "unknown")
        require(plan.get("schema") == "QuantumFrameworkPackagePlan/v1", errors, f"{label} wrong package plan schema")
        require(plan.get("install_now") is False, errors, f"{label} should not install now")
        require(str(plan.get("install_command", "")).startswith("python -m pip install "), errors, f"{label} invalid install command")
        require(plan.get("pin_policy") == "RESOLVE_IN_ISOLATED_ENV_THEN_FREEZE_WITH_HASHES", errors, f"{label} missing pin policy")
        require(plan.get("cloud_credentials_required_for_import_fixture") is False, errors, f"{label} import fixture should not require credentials")
        require(plan.get("plan_hash"), errors, f"{label} missing plan hash")
        require(plan.get("import_targets"), errors, f"{label} missing import targets")
        require(plan.get("first_framework_import_fixture"), errors, f"{label} missing fixture contract")
        require(all(str(url).startswith("https://") for url in plan.get("source_anchors", [])), errors, f"{label} source anchor not HTTPS")

    gates = set(data.get("promotion_gates", []))
    required_gates = {
        "ISOLATED_ENVIRONMENT_REQUIRED",
        "RESOLVE_AND_FREEZE_WITH_HASHES_REQUIRED",
        "NO_CLOUD_CREDENTIALS_FOR_FRAMEWORK_IMPORT_FIXTURES",
        "NO_CLOUD_PROVIDER_EXECUTION_WITHOUT_LIVE_PROVIDER_RECEIPT",
        "SDK_IMPORT_DOES_NOT_PROVE_PROVIDER_EXECUTION",
        "OTEL_API_NONRECORDING_SPAN_DOES_NOT_PROVE_EXPORTED_TRACE",
    }
    require(required_gates <= gates, errors, "missing promotion gate")

    otel = data.get("opentelemetry_action_bridge_fixture", {})
    require(otel.get("schema") == "OpenTelemetryActionBridgeFixture/v1", errors, "wrong otel schema")
    require(otel.get("distribution") == "opentelemetry-api", errors, "wrong otel distribution")
    require(otel.get("module_imported") is True, errors, "otel module not imported")
    require(otel.get("sdk_installed") is False, errors, "otel sdk should be false")
    require(otel.get("api_version") == "1.41.0", errors, "unexpected otel api version")
    require(otel.get("span_class") == "NonRecordingSpan", errors, "expected NonRecordingSpan")
    require(otel.get("is_recording") is False, errors, "otel span should be non-recording")
    require(otel.get("trace_id_hex") == "00000000000000000000000000000000", errors, "nonrecording trace id should be zero")
    require(otel.get("span_id_hex") == "0000000000000000", errors, "nonrecording span id should be zero")
    require(otel.get("status") == "API_IMPORT_MATCH_NONRECORDING", errors, "wrong otel status")
    require(otel.get("attribute_recording_status") == "NOT_RECORDED_WITH_API_ONLY_NONRECORDING_SPAN", errors, "wrong attribute recording boundary")
    require(otel.get("fixture_hash"), errors, "otel fixture missing hash")

    contract = data.get("quantum_proof_demo_contract", {})
    require(contract.get("schema") == "QuantumProofDemoContract/v1", errors, "wrong demo contract schema")
    layers = set(contract.get("packet_layers", []))
    for layer in [
        "source_anchor_receipts",
        "framework_import_receipt",
        "canonical_result_receipt",
        "negative_fixture_receipts",
        "otel_action_bridge_receipt",
        "crucible_verdict_receipt",
    ]:
        require(layer in layers, errors, f"missing packet layer {layer}")

    negatives = data.get("negative_fixtures", [])
    require(data.get("negative_fixture_count") == len(negatives), errors, "negative count mismatch")
    require(len(negatives) >= 8, errors, "expected at least eight negative fixtures")
    require(all(n.get("expected_validator_status") == "REJECT" for n in negatives), errors, "negative fixture not rejected")

    anchors = data.get("source_anchors", [])
    require(data.get("source_anchor_count") == len(anchors), errors, "source count mismatch")
    require(len(anchors) >= 12, errors, "expected at least 12 source anchors")
    require(all(str(anchor.get("url", "")).startswith("https://") for anchor in anchors), errors, "source anchor not HTTPS")

    result = {
        "schema": "Pass0021QuantumEnvironmentPlanValidatorRun/v1",
        "pass": "0021",
        "status": "MATCH" if not errors else "DRIFT",
        "match": 1 if not errors else 0,
        "drift": 0 if not errors else 1,
        "checks": [
            {
                "artifact": "QuantumFrameworkEnvironmentPlanSet",
                "path": str(SCHEMA_PATH.relative_to(ROOT)),
                "status": "MATCH" if not errors else "DRIFT",
                "package_plan_count": len(plans),
                "negative_fixture_count": len(negatives),
                "source_anchor_count": len(anchors),
                "otel_status": otel.get("status"),
                "errors": errors,
            }
        ],
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
