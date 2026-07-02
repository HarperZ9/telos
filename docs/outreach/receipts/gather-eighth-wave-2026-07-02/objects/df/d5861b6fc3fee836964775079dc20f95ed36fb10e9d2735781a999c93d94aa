# Spec: Action Receipt Failure Typing

## Objective

Use GitHub community feedback from Mastra, SmallHarness, AutoGen/scankii, Haystack, and OpenTelemetry GenAI to tighten the Project Telos action receipt convention. A failed MCP/tool call must remain failure-typed across every durable or replayable surface, while preserving the error payload as evidence.

Extend that same convention for Beater-style external writes: messages, refunds, bookings, account changes, PRs, file/database writes, deployments, and payment/commerce-adjacent actions need a receipt that is not merely a trace span. The receipt is the durable operational claim that joins proposed intent, authority/admission, execution, evidence, review, and append-only compensation without requiring raw prompts, raw tool args, private evidence, or full external payloads.

## Requirements

- [x] Add a conformance fixture for a failed MCP/tool call.
- [x] Preserve `result.state = failed` and a typed stop reason for the failed call.
- [x] Preserve the error payload by digest/ref, not raw secret-bearing content.
- [x] Assert the same failure bit across stream chunk, persisted message part, trace/span, and scorer/eval input surfaces.
- [x] Add negative cases for success-shaped persistence and missing failure payload evidence.
- [x] Keep action receipts separate from trace spans while preserving join fields back to trace/session execution.
- [x] Add external-write action kinds and refs for `intent_ref`, `authority_ref`, `execution_ref`, `evidence_ref`, `review_ref`, and `compensation_ref`.
- [x] Add durable execution fields for external request id, idempotency key, terminal status, redacted before/after refs, and result hash/ref.
- [x] Add negative cases for authority gaps, evidence gaps, missing approval refs, unjoinable execution spans, duplicate idempotency keys, trace-only receipts, collapsed proposed/completed reports, and missing before/after refs.
- [x] Mark the submitted `https://arxiv.org/abs/2605.22967` commerce/security source as `DRIFT`; use `https://arxiv.org/abs/2604.15367` for the SoK commerce/security source.

## Technical Approach

Extend `demo/integrations/action-receipt-conventions.json` and its existing Node test. No runtime behavior change is needed yet; this is a schema/fixture hardening pass that makes future adapters testable across CLI, MCP, IDE/TUI, app hosts, and external-write connectors.

## Files to Modify

- `demo/action-receipt.test.mjs` - add assertions for the failed tool-call fixture and negative cases.
- `demo/integrations/action-receipt-conventions.json` - add fixture fields and failure codes.

## Success Criteria

- [x] `node demo/action-receipt.test.mjs` fails before the convention change.
- [x] `node demo/action-receipt.test.mjs` passes after the convention change.
- [x] Existing action receipt assertions remain intact.
- [x] External-write receipts are testable without treating a trace span as the receipt.
- [x] Source corrections remain explicit when a supplied URL does not match the claimed source.

## Status

IMPLEMENTED
