# Packet 081: Live Workspace-Context Replacement

Date: 2026-07-01

Status: `LIVE_WORKSPACE_CONTEXT_REPLACEMENT_MATCH`

Purpose: replace the pass 0070 synthetic workspace-context component with a
live local Index context envelope while retaining the live Telos action
component from pass 0070.

```text
live_surface_status = MATCH
context_schema = project-telos.context-envelope/v1
verification_verdict = MATCH
retained_count = 1
receipt_count = 1
workspace_component = index.context-envelope.live.root.0071
component_count = 6
negative_fixture_count = 7
compose_status = MATCH
test_status = MATCH
```

## Index Surface Checks

- `focus_failure_captured`: True
- `no_failure_codes`: True
- `raw_output_hash_bound`: True
- `receipt_present`: True
- `retained_context_present`: True
- `schema_match`: True
- `verification_match`: True
- `workspace_component_digest_bound`: True

## Negative Fixtures

- `missing_workspace_context` -> `missing_required_class:workspace_context`
- `missing_action` -> `missing_required_class:action`
- `missing_verification` -> `missing_required_class:verification`
- `live_workspace_digest_drift` -> `component_digest_drift:workspace_context`
- `focus_path_unknown_repo` -> `unknown_focus_repo`
- `raw_payload_required` -> `raw_private_payload_required`
- `unsupported_claim_promoted` -> `unsupported_claim_count_nonzero`

## Growth-Vector Finding

The root context envelope is usable as a live workspace-context receipt. The
path-focused probe currently rejects `docs/research/dogfood` as an unknown
focus repo, which marks a concrete ergonomic gap: Index needs a path-focus mode
or repo/path disambiguation layer before it can cleanly route field-specific
research packets inside a large monorepo.

Current promoted natural laws: none.
