# Dogfood Pass 0023 Ledger

Date: 2026-07-01

Status: `CRUCIBLE_MATCH`.

Crucible assessment:

- thesis id: `700246261ac3cbd6`;
- claims: `10`;
- match: `10`;
- drift: `0`;
- unverifiable: `0`;
- thesis seal: `700246261ac3cbd6ae47827262177aa646e148dc6b636a1906715536ef17eaa4`;
- verdict seal: `d45054703bbbe2a9ceea0da02358579804789cd0b81906a660d48e948ec9838f`;
- measurement seal: `21ece9e3167b4be8d1d17df857ee2afae3ad502bbde8e9fc452e896174c75db2`;
- assessment seal: `e5c55e68631fc65f0a1e51a7b073af7020eab4d33d29efb3be67c109b3eafd97`;
- integrity: `seals_ok=True`, `thesis_ok=True`, `verdicts_rederive=True`.

Pass theme: isolated OpenTelemetry SDK recording-span fixture and first bridge
toward Telos action proof packets. This pass advances the agent-infrastructure
market wedge by proving that trace evidence can be generated in an isolated
interpreter and then shaped into a future durable action receipt boundary.

No Telos runtime action receipt, cloud trace export, live agent safety guarantee,
buyer adoption signal, theorem proof, scientific discovery, biological result,
material result, medical result, finance result, safety result, or natural law is
promoted in this pass.

## Primary Receipt

Receipt schema:

```text
OTelRecordingSpanVenvReceiptSet/v1
```

Receipt seal:

```text
7d87821c3e35dbfe5493087092d7f5a1c3c0aea62a54e729e5ff7938b1d95796
```

Validator result:

```text
status = MATCH
match = 1
drift = 0
resolved_install_count = 6
negative_fixture_count = 6
finished_span_count = 1
base_sdk_available_after = false
```

## Isolated Install

The pass used this temporary venv:

```text
C:\Users\Zain\AppData\Local\Temp\telos-dogfood-otel-sdk-0023
```

Boundary:

```text
TEMP_ISOLATED_ENV_DO_NOT_COMMIT
```

The base interpreter remained unchanged:

```text
base_environment_before opentelemetry_sdk_available = false
base_environment_after opentelemetry_sdk_available = false
base Python = 3.12.10
base opentelemetry-api = 1.41.0
```

Resolved wheels:

| Package | Version | Requested | SHA-256 |
| --- | --- | --- | --- |
| `opentelemetry-api` | `1.41.0` | `true` | `0e77c806e6a89c9e4f8d372034622f3e1418a11bdbe1c80a50b3d3397ad0fa4f` |
| `opentelemetry-sdk` | `1.41.0` | `true` | `a596f5687964a3e0d7f8edfdcf5b79cbca9c93c7025ebf5fb00f398a9443b0bd` |
| `opentelemetry-semantic-conventions` | `0.62b0` | `true` | `0ddac1ce59eaf1a827d9987ab60d9315fb27aea23304144242d1fcad9e16b489` |
| `typing_extensions` | `4.15.0` | `true` | `f0fa19c6845758ab08074a0cfa8b7aecb71c999ca73d62883bc25cc018c4e548` |
| `importlib_metadata` | `8.7.1` | `false` | `5a1f80bf1daa489495071efbb095d75a634cf28a8bc299581244063b53176151` |
| `zipp` | `4.1.0` | `false` | `25ad4e16390cd314347dd8f1de67a2ac538ae658ed4ab9db16029c07c188e97f` |

## Span Fixture

Fixture schema:

```text
OpenTelemetryRecordingSpanFixture/v1
```

Fixture result:

```text
status = RECORDING_SPAN_EXPORTED_IN_MEMORY
sdk_imported = true
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

## Tool Substrate Receipt

Pass 0023 refreshed the tool surfaces:

| Tool | Status | Note |
| --- | --- | --- |
| Index | `MATCH` | Version 2.8.0; status and doctor available. |
| Gather | `MATCH` | Version 1.5.0; packet 033 read verified. |
| Telos | `MATCH` | Operator doctor 14/14; action receipt, loop ledger, native control, and catalog surfaced. |
| Forum | `MATCH_WITH_SUBMIT_GAP` | Status and ledger verification work; submit is `UNVERIFIABLE` because no model executor is configured. |
| Crucible | `MATCH` | Version 1.1.0; pass 0023 assessment matched. |

Gather docs receipt for packet 033:

```text
sha256=945054a1aed15ecffcfd46427b97dd268056a05d08997906a99faab29eed5b05
seal=68f9ce4e29ff0147006858732dfb26683ebbe24c2b5b62f5782a1e75334e7a91
```

Forum submit attempt:

```text
status=UNVERIFIABLE
error=submit needs a model executor
```

## Artifacts

| Artifact | Role |
| --- | --- |
| `tools/probe_otel_recording_span_venv.py` | Isolated venv, pinned OTel install, and in-memory span generator. |
| `tools/validate_pass_0023_otel_recording_span_venv.py` | Validator for base-boundary, install, span, bridge, source, and negative fixtures. |
| `packets/033-otel-recording-span-venv.md` | Human-readable isolated OTel recording-span packet. |
| `adversarial/pass-0023-otel-recording-span-steelman.md` | Forum failure receipt plus local pass 0023 steelman. |
| `schemas/otel-recording-span-venv-pass-0023.json` | `OTelRecordingSpanVenvReceiptSet/v1` artifact. |
| `schemas/pass-0023-otel-recording-span-venv-validator-result.json` | Validator receipt for pass 0023. |
| `schemas/tool-receipts-pass-0023.json` | Compact Index, Gather, Telos, Forum, and Crucible receipts. |
| `crucible/pass-0023-thesis.json` | Falsifiable claims for the twenty-third pass. |
| `crucible/pass-0023-measurements.json` | Measurements/evidence for the twenty-third pass. |
| `crucible/pass-0023-report.md` | Crucible assessment report. |
| `crucible/pass-0023-run.json` | Crucible run record. |

## Primary Next Push

Build `TelosActionReceiptFixture/v1` by binding the trace id and span id from
this pass to a durable action receipt object.

The next proof should include:

- action intent id;
- proposed action record;
- admitted action record;
- command receipt digest;
- source packet digest;
- trace id;
- span id;
- verification verdict;
- append-only event hash;
- rejection fixtures for trace-only receipts.

## Natural-Law Promotion

Current promoted natural laws: none.
