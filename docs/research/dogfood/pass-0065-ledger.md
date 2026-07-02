# Pass 0065 Ledger: OTel Trace to Telos Action Receipt Fixture

Date: 2026-07-01

Status: `MATCH_OTEL_TRACE_TO_ACTION_RECEIPT_FIXTURE`

## Purpose

Turn the pass 0064 adapter matrix into an executable local fixture: a synthetic
OpenTelemetry-style trace becomes a `project-telos.action-receipt/v1` packet
with source refs, workspace state, authority scope, action admission,
side-effect class, trace refs, eval refs, verification verdict, stop reason,
privacy boundary, and compensation pointer.

This pass does not claim live OpenTelemetry ingestion, production SDK
compatibility, product-market fit, or buyer value. It proves the minimum local
adapter shape.

## Artifacts

| Artifact | Purpose |
| --- | --- |
| `tools/compose_otel_trace_to_action_receipt_fixture.py` | Deterministic OTel trace to action receipt composer. |
| `tools/test_otel_trace_to_action_receipt_fixture.py` | Focused RED/GREEN fixture test. |
| `tools/probe_otel_trace_to_action_receipt_fixture.py` | Packet, thesis, and measurement generator. |
| `tools/validate_pass_0065_otel_trace_to_action_receipt_fixture.py` | Validator for trace, receipt fields, span linkage, and negative fixture controls. |
| `schemas/otel-trace-to-action-receipt-fixture-pass-0065.json` | `OtelTraceToTelosActionReceiptFixture/v1` artifact. |
| `schemas/pass-0065-otel-trace-to-action-receipt-fixture-validator-result.json` | Validator receipt. |
| `schemas/tool-receipts-pass-0065.json` | Compact Index, Gather, Forum, Crucible, Telos, and shell receipts. |
| `packets/075-otel-trace-to-action-receipt-fixture.md` | Human-readable fixture packet. |
| `adversarial/pass-0065-otel-trace-to-action-receipt-fixture-steelman.md` | Local steelman. |
| `crucible/pass-0065-thesis.json` | Falsifiable claims. |
| `crucible/pass-0065-measurements.json` | Measurements/evidence. |
| `crucible/pass-0065-report.md` | Crucible report. |
| `crucible/pass-0065-run.json` | Crucible run record. |

## Measurements

| Check | Result |
| --- | --- |
| Trace fixture schema | `OpenTelemetryTraceFixture/v1` |
| Trace id | `4f7e65b0c6c34c2aa1d6f64e08b03a65` |
| Span count | 4 |
| Receipt schema | `project-telos.action-receipt/v1` |
| Side-effect class | `local_read_only_fixture` |
| Verification verdict | `MATCH` |
| Negative fixture status | `FAIL_EXPECTED` |
| Unsupported claims | 0 |

## Trace Shape

| Span id | Name | Kind |
| --- | --- | --- |
| `0f1a` | `agent.run` | `root` |
| `0f1b` | `gather.docs` | `tool` |
| `0f1c` | `validator.run` | `tool` |
| `0f1d` | `crucible.run` | `verifier` |

## Tool Findings

- Index status returned `MATCH`.
- Gather read packet 075 with SHA256 `99f2ff824ab1b7825084e3764d4d85ff97e94a0b0687a3030654c58892ca83b1` and digest seal `96fb1dd7a200af80e0b5dba8fab88e422d50975163ba20c601859e5b64b055df`.
- Forum ledger verified `chain=true`, `deep=true`.
- Crucible result: 7 claims, 7 MATCH, 0 DRIFT, 0 UNVERIFIABLE.
- Crucible thesis id: `41af816e4556a37c`.
- Crucible assessment seal: `cd383c2757ad996649a083b4ba516cf6cfb2aebabaef34bac87ecd612e1929e7`.
- Crucible registry stats after this pass: 53 theses, 441 claims, 441 MATCH, 0 DRIFT, 0 UNVERIFIABLE.
- Telos workflow returned `MATCH`.

## Verification

```powershell
python docs\research\dogfood\tools\test_otel_trace_to_action_receipt_fixture.py
python docs\research\dogfood\tools\probe_otel_trace_to_action_receipt_fixture.py
python docs\research\dogfood\tools\validate_pass_0065_otel_trace_to_action_receipt_fixture.py
crucible run docs\research\dogfood\crucible\pass-0065-thesis.json --measurements docs\research\dogfood\crucible\pass-0065-measurements.json --registry docs\research\dogfood\crucible\registry --report docs\research\dogfood\crucible\pass-0065-report.md --out docs\research\dogfood\crucible\pass-0065-run.json --json
```

## Next Pass

Build pass 0066 as either:

1. a real OTLP JSON export importer that maps external trace files into this fixture, or
2. a buyer-facing regulated-agent proof packet that uses pass 0065 as the execution spine.
