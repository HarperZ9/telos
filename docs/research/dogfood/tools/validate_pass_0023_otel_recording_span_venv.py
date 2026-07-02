"""Validate pass 0023 isolated OTel SDK recording-span receipts."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "otel-recording-span-venv-pass-0023.json"


def require(condition: bool, errors: list[str], message: str) -> None:
    if not condition:
        errors.append(message)


def nonzero_hex(value: object, width: int) -> bool:
    text = str(value or "")
    return len(text) == width and set(text) != {"0"} and all(char in "0123456789abcdef" for char in text)


def main() -> int:
    data = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    errors: list[str] = []

    require(data.get("schema") == "OTelRecordingSpanVenvReceiptSet/v1", errors, "wrong schema")
    require(data.get("pass") == "0023", errors, "wrong pass")
    require(data.get("status") == "OTEL_RECORDING_SPAN_VENV_MATCH", errors, "wrong status")
    require(bool(data.get("seal")), errors, "missing seal")
    require("isolated local OpenTelemetry SDK recording-span fixture" in data.get("non_promotion_statement", ""), errors, "missing non-promotion")

    base_before = data.get("base_environment_before", {})
    base_after = data.get("base_environment_after", {})
    require(base_before.get("schema") == "BaseInterpreterImportAudit/v1", errors, "wrong base-before schema")
    require(base_after.get("schema") == "BaseInterpreterImportAudit/v1", errors, "wrong base-after schema")
    require(base_before.get("opentelemetry_sdk_available") is False, errors, "base SDK available before pass")
    require(base_after.get("opentelemetry_sdk_available") is False, errors, "base SDK mutated by pass")

    venv = data.get("venv", {})
    require(venv.get("schema") == "IsolatedVenvReceipt/v1", errors, "wrong venv schema")
    require(venv.get("boundary") == "TEMP_ISOLATED_ENV_DO_NOT_COMMIT", errors, "wrong venv boundary")
    require(bool(venv.get("path_sha256")), errors, "missing venv path hash")
    create = venv.get("create", {})
    require(create.get("returncode") == 0, errors, "venv creation failed")

    install = data.get("install", {})
    require(install.get("schema") == "PipInstallReportReceipt/v1", errors, "wrong install schema")
    require(install.get("returncode") == 0, errors, "pip install failed")
    command = install.get("command", [])
    for requirement in [
        "opentelemetry-api==1.41.0",
        "opentelemetry-sdk==1.41.0",
        "opentelemetry-semantic-conventions==0.62b0",
        "typing-extensions==4.15.0",
    ]:
        require(requirement in command, errors, f"missing requirement {requirement}")
    require("--report" in command and "--force-reinstall" in command, errors, "install command missing report/force reinstall")
    require(bool(install.get("report_sha256")), errors, "missing install report hash")

    resolved = install.get("resolved", [])
    by_name = {row.get("name"): row for row in resolved}
    require(data.get("resolved_install_count") == len(resolved), errors, "resolved count mismatch")
    for name in [
        "opentelemetry-api",
        "opentelemetry-sdk",
        "opentelemetry-semantic-conventions",
        "typing_extensions",
        "typing-extensions",
    ]:
        if name in {"typing_extensions", "typing-extensions"}:
            continue
        require(name in by_name, errors, f"missing resolved package {name}")
    typing_row = by_name.get("typing_extensions") or by_name.get("typing-extensions")
    require(typing_row is not None, errors, "missing typing extensions")

    expected_versions = {
        "opentelemetry-api": "1.41.0",
        "opentelemetry-sdk": "1.41.0",
        "opentelemetry-semantic-conventions": "0.62b0",
    }
    for name, version in expected_versions.items():
        row = by_name.get(name, {})
        require(row.get("version") == version, errors, f"{name} version drift")
        require(isinstance(row.get("sha256"), str) and len(row.get("sha256")) == 64, errors, f"{name} missing sha256")
    if typing_row:
        require(typing_row.get("version") == "4.15.0", errors, "typing extensions version drift")
        require(isinstance(typing_row.get("sha256"), str) and len(typing_row.get("sha256")) == 64, errors, "typing extensions missing sha256")

    fixture = data.get("recording_span_fixture", {})
    require(fixture.get("schema") == "OpenTelemetryRecordingSpanFixture/v1", errors, "wrong fixture schema")
    require(fixture.get("status") == "RECORDING_SPAN_EXPORTED_IN_MEMORY", errors, "wrong fixture status")
    require(fixture.get("returncode") == 0, errors, "fixture command failed")
    require(fixture.get("sdk_imported") is True, errors, "SDK was not imported in venv")
    require(fixture.get("api_version") == "1.41.0", errors, "fixture API version drift")
    require(fixture.get("sdk_version") == "1.41.0", errors, "fixture SDK version drift")
    require(fixture.get("semantic_conventions_version") == "0.62b0", errors, "fixture semconv version drift")
    require(fixture.get("exporter_class") == "InMemorySpanExporter", errors, "wrong exporter class")
    require(fixture.get("span_processor_class") == "SimpleSpanProcessor", errors, "wrong span processor")
    require(fixture.get("span_was_recording_inside_context") is True, errors, "span did not record inside context")
    require(fixture.get("finished_span_count") == 1, errors, "expected one finished span")
    require(nonzero_hex(fixture.get("trace_id_hex"), 32), errors, "trace id is zero or malformed")
    require(nonzero_hex(fixture.get("span_id_hex"), 16), errors, "span id is zero or malformed")
    attrs = fixture.get("attributes", {})
    require(attrs.get("telos.pass") == "0023", errors, "missing telos pass attr")
    require(attrs.get("telos.action") == "recording-span-fixture", errors, "missing telos action attr")
    require(attrs.get("telos.receipt.kind") == "OpenTelemetryRecordingSpanFixture/v1", errors, "missing receipt kind attr")
    require(attrs.get("telos.no_cloud_export") is True, errors, "missing no-cloud attr")
    require(bool(fixture.get("fixture_hash")), errors, "missing fixture hash")
    require(bool(fixture.get("exporter_sink_hash")), errors, "missing exporter sink hash")

    bridge = data.get("action_receipt_bridge", {})
    require(bridge.get("schema") == "TelosActionReceiptBridgeSketch/v1", errors, "wrong bridge schema")
    require(bridge.get("status") == "BRIDGE_FIXTURE_READY_NOT_TELOS_RUNTIME", errors, "wrong bridge status")
    require("telos.action.receipt" == bridge.get("internal_tool"), errors, "wrong bridge internal tool")
    layer = set(bridge.get("verification_layer", []))
    for expected in ["nonzero trace id", "nonzero span id", "finished span count", "receipt hash binding", "base interpreter non-mutation audit"]:
        require(expected in layer, errors, f"missing bridge verification {expected}")

    negatives = data.get("negative_fixtures", [])
    require(data.get("negative_fixture_count") == len(negatives), errors, "negative count mismatch")
    require(len(negatives) >= 6, errors, "expected at least six negatives")
    require(all(n.get("expected_validator_status") == "REJECT" for n in negatives), errors, "negative fixture not rejected")

    anchors = data.get("source_anchors", [])
    require(data.get("source_anchor_count") == len(anchors), errors, "source count mismatch")
    require(len(anchors) >= 4, errors, "expected at least four anchors")
    require(all(str(anchor.get("url", "")).startswith("https://") for anchor in anchors), errors, "source anchor not HTTPS")

    result = {
        "schema": "Pass0023OTelRecordingSpanVenvValidatorRun/v1",
        "pass": "0023",
        "status": "MATCH" if not errors else "DRIFT",
        "match": 1 if not errors else 0,
        "drift": 0 if not errors else 1,
        "checks": [
            {
                "artifact": "OTelRecordingSpanVenvReceiptSet",
                "path": str(SCHEMA_PATH.relative_to(ROOT)),
                "status": "MATCH" if not errors else "DRIFT",
                "resolved_install_count": len(resolved),
                "negative_fixture_count": len(negatives),
                "finished_span_count": fixture.get("finished_span_count"),
                "trace_id_hex": fixture.get("trace_id_hex"),
                "span_id_hex": fixture.get("span_id_hex"),
                "base_sdk_available_after": base_after.get("opentelemetry_sdk_available"),
                "errors": errors,
            }
        ],
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
