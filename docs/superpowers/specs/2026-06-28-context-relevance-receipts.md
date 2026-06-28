# Spec: Context Relevance Receipts

## Objective

Convert OpenTelemetry GenAI community feedback into a Telos context-envelope fixture that keeps context delivery separate from later evidence relevance. A context item being loaded into a session must not imply it was decisive or supporting evidence.

## Requirements

- [x] Add a conformance fixture for context selection, loading, suppression, and post-hoc relevance evaluation.
- [x] Preserve selected, delivered, suppressed, decisive, supporting, unused, and unknown counts.
- [x] Assert `selected_count == decisive_count + supporting_count + unused_count + unknown_count`.
- [x] Keep relevance labels out of selection/load events.
- [x] Use hashed source and delivered identities; do not store raw prompt, memory, ticket, source body, or tool output.
- [x] Add negative cases for missing relevance accounting and raw context leakage.

## Technical Approach

Extend `demo/integrations/context-envelope-conventions.json` and its existing Node test. This is a conformance fixture and schema hardening pass; runtime adapters can follow after the fixture proves the boundary.

## Files to Modify

- `demo/context-envelope.test.mjs` - add assertions for the context relevance fixture and negative cases.
- `demo/integrations/context-envelope-conventions.json` - add fixture fields and failure codes.

## Success Criteria

- [x] `node demo/context-envelope.test.mjs` fails before the convention change.
- [x] `node demo/context-envelope.test.mjs` passes after the convention change.
- [x] Existing context-envelope assertions remain intact.

## Status

IMPLEMENTED
