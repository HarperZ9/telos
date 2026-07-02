# Quantum Environment Plan And OTel Bridge Packet

Pass: `0021`

Date: 2026-07-01

Status: `ENVIRONMENT_PLAN_AND_OTEL_BRIDGE_MATCH`

This packet turns pass 0020's market and import audit into an execution plan for
the next proof-demo step: a pinned local quantum framework-import environment
and the first real OpenTelemetry action-bridge fixture.

No quantum SDKs were installed. No unavailable quantum framework was imported.
The only actual import fixture is `opentelemetry-api`, which was already present
locally.

## Generated Receipt

Artifact:

```text
schemas/quantum-environment-plan-otel-bridge-pass-0021.json
```

Seal:

```text
1ce3a1aaab7392d4a825564415a76e71a4f8b59c2a954dbb794d4ffe7e67cb1f
```

Validator:

```text
schema = Pass0021QuantumEnvironmentPlanValidatorRun/v1
status = MATCH
package_plan_count = 11
negative_fixture_count = 9
source_anchor_count = 15
otel_status = API_IMPORT_MATCH_NONRECORDING
```

## Local Environment

| Field | Value |
| --- | --- |
| Python | `3.12.10` |
| pip | `26.1.2` |
| Platform | `Windows-11-10.0.26220-SP0` |
| Boundary | `PLAN_ONLY_NO_PACKAGE_INSTALL` |

The generator records a hash of the Python executable path string. It does not
hash the interpreter binary itself.

## Package Plans

Each package plan sets:

```text
install_now = false
pin_policy = RESOLVE_IN_ISOLATED_ENV_THEN_FREEZE_WITH_HASHES
cloud_credentials_required_for_import_fixture = false
```

| Distribution | First Fixture Contract |
| --- | --- |
| `qiskit` | Create a two-qubit Bell circuit and emit source/circuit/canonical-count layout receipts without provider execution. |
| `qiskit-ibm-runtime` | Import runtime client classes and create metadata-only client-shape receipt; no token, account, session, or job execution. |
| `amazon-braket-sdk` | Create local Braket `Circuit` object and parse local/synthetic measurement count shape; no AWS task execution. |
| `cirq` | Create Bell circuit with `cirq.LineQubit` and local simulator/result canonicalization. |
| `pennylane` | Create `default.qubit` QNode with fixed shots and wire-order receipt. |
| `pyqir` | Create or parse minimal QIR module and emit result-record-map receipt. |
| `pytket` | Create a pytket `Circuit` and emit compiler/routing metadata receipt without backend execution. |
| `pytket-qir` | Convert local pytket circuit to QIR and bind QIR hash to framework-import fixture. |
| `cudaq` | Import CUDA-Q and run CPU/local simulator fixture if available; GPU acceleration separately detected. |
| `opentelemetry-api` | Map local action spans to `ActionReceipt/v1`; API-only spans remain non-recording without SDK/exporter. |
| `opentelemetry-sdk` | Create local in-memory recording span fixture with resource and attribute receipts. |

## Promotion Gates

The pass encodes eight gates:

- `ISOLATED_ENVIRONMENT_REQUIRED`;
- `RESOLVE_AND_FREEZE_WITH_HASHES_REQUIRED`;
- `NO_CLOUD_CREDENTIALS_FOR_FRAMEWORK_IMPORT_FIXTURES`;
- `NO_CLOUD_PROVIDER_EXECUTION_WITHOUT_LIVE_PROVIDER_RECEIPT`;
- `SDK_IMPORT_DOES_NOT_PROVE_PROVIDER_EXECUTION`;
- `OTEL_API_NONRECORDING_SPAN_DOES_NOT_PROVE_EXPORTED_TRACE`;
- `BUILD_RUNTIME_RECEIPTS_REQUIRED_FOR_BUILDLANG_PROMOTION`;
- `MEASURED_OUTPUT_RECEIPTS_REQUIRED_FOR_COLOR_RENDERING_PROMOTION`.

## OpenTelemetry Fixture

The fixture imports `opentelemetry-api` version `1.41.0` and creates a span from
the API-only tracer:

| Field | Value |
| --- | --- |
| Span class | `NonRecordingSpan` |
| Recording | `false` |
| Trace ID | `00000000000000000000000000000000` |
| Span ID | `0000000000000000` |
| Attribute status | `NOT_RECORDED_WITH_API_ONLY_NONRECORDING_SPAN` |
| Fixture hash | `a95002a2f3db465b1b460dc66fade557da46c1c70f8bac68dc149723167b6f90` |

This is a useful result because it prevents a common observability mistake:
`opentelemetry-api` alone can shape action-receipt semantics, but it does not
prove that a recording trace was exported. A future pass must add
`opentelemetry-sdk` and an in-memory exporter fixture if trace evidence is to be
promoted.

## QuantumProofDemo Contract

The next public demo packet should include these layers:

- source anchor receipts;
- workspace context receipt;
- framework import receipt;
- circuit or program receipt;
- canonical result receipt;
- negative fixture receipts;
- OTel action bridge receipt;
- Crucible verdict receipt.

The same contract should wrap BuildLang/buildc and Build Color as sibling
runtime demos:

```text
QuantumProofDemo/v1 -> ScientificRuntimeReceipt/v1 -> ColorMeasurementReceipt/v1
```

The common object is the proof packet, not a monolithic application.

## Negative Fixtures

| Fixture | Expected Result |
| --- | --- |
| `negative-installing-into-shared-base-env` | `REJECT` |
| `negative-unpinned-runtime-demo` | `REJECT` |
| `negative-cloud-credential-required-for-import-fixture` | `REJECT` |
| `negative-sdk-import-claimed-as-provider-execution` | `REJECT` |
| `negative-nonrecording-otel-span-claimed-as-exported-trace` | `REJECT` |
| `negative-cudaq-import-claimed-as-gpu-acceleration` | `REJECT` |
| `negative-qir-without-record-map` | `REJECT` |
| `negative-buildlang-runtime-without-compiler-receipt` | `REJECT` |
| `negative-color-runtime-without-measurement-receipt` | `REJECT` |

## Source Anchors

The schema stores 15 source anchors for Qiskit install, Qiskit Runtime install,
Braket SDK/getting started, Cirq install, PennyLane install/dependencies, PyQIR,
pytket, pytket-QIR, CUDA-Q, pip install semantics, and OpenTelemetry Python/API
trace documentation.

## Non-Promotion

Pass 0021 imports `opentelemetry-api` only because it is already present
locally. It does not install quantum SDKs, import unavailable quantum
frameworks, create cloud credentials, run provider jobs, run quantum hardware,
or promote scientific results.
