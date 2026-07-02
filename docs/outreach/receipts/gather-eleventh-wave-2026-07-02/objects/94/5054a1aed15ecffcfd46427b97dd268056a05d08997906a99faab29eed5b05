# Packet 033: Isolated OpenTelemetry Recording Span Fixture

Date: 2026-07-01

Status: `CRUCIBLE_MATCH`.

Pass 0023 advances the agent action proof-packet wedge by turning the pass
0021 OpenTelemetry API-only bridge and pass 0022 SDK dry-run lock into a real
recording span fixture inside a throwaway virtual environment. The shared base
interpreter remains unchanged.

This is still a bounded local proof. It proves a local SDK import, in-memory
exporter, nonzero trace identifiers, finished span count, exporter sink hash,
and Telos action-receipt bridge sketch. It does not prove Telos runtime
integration, cloud trace export, live agent safety, buyer demand, scientific
discovery, theorem proof, or any natural law.

## Receipt Summary

Primary schema:

```text
schemas/otel-recording-span-venv-pass-0023.json
```

Receipt seal:

```text
7d87821c3e35dbfe5493087092d7f5a1c3c0aea62a54e729e5ff7938b1d95796
```

Validator result:

```text
schema = Pass0023OTelRecordingSpanVenvValidatorRun/v1
status = MATCH
match = 1
drift = 0
resolved_install_count = 6
negative_fixture_count = 6
finished_span_count = 1
base_sdk_available_after = false
```

## Isolated Environment Boundary

The fixture uses a temporary virtual environment:

```text
C:\Users\Zain\AppData\Local\Temp\telos-dogfood-otel-sdk-0023
```

The venv is explicitly marked `TEMP_ISOLATED_ENV_DO_NOT_COMMIT`. The base
Python interpreter audit before and after the pass reports:

```text
opentelemetry_api_version = 1.41.0
opentelemetry_sdk_available = false
python_version = 3.12.10
```

That matters because pass 0023 is allowed to install packages only into the
throwaway interpreter. The base environment remains a separate witness that
`opentelemetry.sdk` was not silently added to the shared runtime.

## Pinned Install Receipt

Install command:

```text
python -m pip install --disable-pip-version-check --force-reinstall --report <temp-report> opentelemetry-api==1.41.0 opentelemetry-sdk==1.41.0 opentelemetry-semantic-conventions==0.62b0 typing-extensions==4.15.0
```

The command returned `0`.

Resolved wheels:

| Package | Version | Requested | SHA-256 |
| --- | --- | --- | --- |
| `opentelemetry-api` | `1.41.0` | `true` | `0e77c806e6a89c9e4f8d372034622f3e1418a11bdbe1c80a50b3d3397ad0fa4f` |
| `opentelemetry-sdk` | `1.41.0` | `true` | `a596f5687964a3e0d7f8edfdcf5b79cbca9c93c7025ebf5fb00f398a9443b0bd` |
| `opentelemetry-semantic-conventions` | `0.62b0` | `true` | `0ddac1ce59eaf1a827d9987ab60d9315fb27aea23304144242d1fcad9e16b489` |
| `typing_extensions` | `4.15.0` | `true` | `f0fa19c6845758ab08074a0cfa8b7aecb71c999ca73d62883bc25cc018c4e548` |
| `importlib_metadata` | `8.7.1` | `false` | `5a1f80bf1daa489495071efbb095d75a634cf28a8bc299581244063b53176151` |
| `zipp` | `4.1.0` | `false` | `25ad4e16390cd314347dd8f1de67a2ac538ae658ed4ab9db16029c07c188e97f` |

The pass intentionally records transitive packages instead of hiding them.
This keeps the future action-proof packet reproducible enough to challenge.

## Recording Span Fixture

Fixture schema:

```text
OpenTelemetryRecordingSpanFixture/v1
```

Fixture result:

```text
status = RECORDING_SPAN_EXPORTED_IN_MEMORY
sdk_imported = true
api_version = 1.41.0
sdk_version = 1.41.0
semantic_conventions_version = 0.62b0
exporter_class = InMemorySpanExporter
span_processor_class = SimpleSpanProcessor
span_was_recording_inside_context = true
finished_span_count = 1
no_network_export = true
```

Trace identifiers:

```text
trace_id_hex = aaa76491660d7a56086f69d1be94debe
span_id_hex = 1424d4ca9a6c5b58
```

Fixture hashes:

```text
exporter_sink_hash = f2e9f33d12e261457731f6eedbe62c3c6d04d574c2c8274870da4eee0c2c2fc0
fixture_hash = b1f3b6cd1c5b81d1784b29f5f9e11dd9ab1c2849f7510de94926dca07d5e2a25
```

Recorded attributes:

```text
telos.pass = 0023
telos.action = recording-span-fixture
telos.receipt.kind = OpenTelemetryRecordingSpanFixture/v1
telos.no_cloud_export = true
```

Resource attributes include:

```text
service.name = telos-dogfood-pass-0023
telos.export.boundary = in-memory-only
telos.pass = 0023
telemetry.sdk.name = opentelemetry
telemetry.sdk.language = python
telemetry.sdk.version = 1.41.0
```

## Action Receipt Bridge

The bridge is deliberately labeled:

```text
TelosActionReceiptBridgeSketch/v1
BRIDGE_FIXTURE_READY_NOT_TELOS_RUNTIME
```

Bridge inputs:

| Input | Purpose |
| --- | --- |
| source packet digest | Binds trace evidence to gathered source state. |
| operator action label | Separates proposed/action intent from runtime observation. |
| tool command receipt | Gives the action an executable or command witness. |
| `OpenTelemetryRecordingSpanFixture/v1` | Supplies trace and span identifiers plus exporter sink hash. |

Bridge outputs:

| Output | Purpose |
| --- | --- |
| action receipt id | Durable join key outside trace retention windows. |
| trace id | Runtime observation join key. |
| span id | Runtime operation join key. |
| exporter sink hash | Local evidence that the span was exported to the in-memory sink. |
| validator verdict | MATCH/DRIFT/UNVERIFIABLE pressure before promotion. |

Verification layer:

```text
nonzero trace id
nonzero span id
finished span count
receipt hash binding
base interpreter non-mutation audit
```

This is the first narrow step from generic observability toward a portable
agent action proof packet. The market gap remains a hypothesis: observability
tools can expose traces, but high-stakes agent workflows need durable receipts
that survive trace retention, redact raw payloads, join authority/evidence, and
carry explicit verification verdicts.

## Negative Fixtures

| Fixture | Expected Result |
| --- | --- |
| `negative-base-env-sdk-mutation` | `REJECT` |
| `negative-zero-trace-or-span-id` | `REJECT` |
| `negative-nonrecording-span-promoted` | `REJECT` |
| `negative-cloud-exporter-claim` | `REJECT` |
| `negative-missing-exporter-sink-hash` | `REJECT` |
| `negative-otel-version-drift` | `REJECT` |

## Market Implication

This pass strengthens the AI infrastructure and agent-ops wedge:

1. Existing tracing stacks are useful runtime observability systems.
2. Telos should not compete by making another trace viewer first.
3. The sharper wedge is a durable action-proof packet that can ingest traces,
   source digests, command receipts, authority references, policy decisions,
   verification verdicts, and compensation records.
4. OTel becomes a bridge substrate, not the final proof object.

The near-term product move is a public demo where a tool action produces:

- source packet digest;
- command receipt;
- OTel trace id and span id;
- exporter sink hash;
- Telos action receipt sketch;
- Crucible verdict;
- negative fixtures showing what must not be promoted.

## Source Anchors

| Source | URL |
| --- | --- |
| OpenTelemetry Python getting started | https://opentelemetry.io/docs/languages/python/getting-started/ |
| OpenTelemetry Python instrumentation | https://opentelemetry.io/docs/languages/python/instrumentation/ |
| OpenTelemetry Python trace API | https://opentelemetry-python.readthedocs.io/en/latest/api/trace.html |
| pip install report option | https://pip.pypa.io/en/stable/cli/pip_install/ |

## Next Push

Pass 0024 should use this fixture to build a real `TelosActionReceiptFixture/v1`
that binds:

- action intent id;
- trace id;
- span id;
- command receipt digest;
- source packet digest;
- policy/admission placeholder;
- Crucible validator result;
- append-only event hash.

After that, the loop can choose between a Cirq-only quantum import fixture or
a Telos action-receipt persistence fixture. The stricter move is the receipt
persistence fixture because it turns the OTel bridge into the product wedge.

## Natural-Law Promotion

Current promoted natural laws: none.
