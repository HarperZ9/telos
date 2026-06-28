# Spec: Action Receipt Failure Typing

## Objective

Use GitHub community feedback from Mastra, SmallHarness, AutoGen/scankii, Haystack, and OpenTelemetry GenAI to tighten the Project Telos action receipt convention. A failed MCP/tool call must remain failure-typed across every durable or replayable surface, while preserving the error payload as evidence.

## Requirements

- [x] Add a conformance fixture for a failed MCP/tool call.
- [x] Preserve `result.state = failed` and a typed stop reason for the failed call.
- [x] Preserve the error payload by digest/ref, not raw secret-bearing content.
- [x] Assert the same failure bit across stream chunk, persisted message part, trace/span, and scorer/eval input surfaces.
- [x] Add negative cases for success-shaped persistence and missing failure payload evidence.

## Technical Approach

Extend `demo/integrations/action-receipt-conventions.json` and its existing Node test. No runtime behavior change is needed yet; this is a schema/fixture hardening pass that makes future adapters testable.

## Files to Modify

- `demo/action-receipt.test.mjs` - add assertions for the failed tool-call fixture and negative cases.
- `demo/integrations/action-receipt-conventions.json` - add fixture fields and failure codes.

## Success Criteria

- [x] `node demo/action-receipt.test.mjs` fails before the convention change.
- [x] `node demo/action-receipt.test.mjs` passes after the convention change.
- [x] Existing action receipt assertions remain intact.

## Status

IMPLEMENTED
