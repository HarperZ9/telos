# Packet 086: BuildLang Index Focus Bridge

Date: 2026-07-01

Status: `BUILDLANG_INDEX_FOCUS_BRIDGE_REQUIRED`

Purpose: test whether Index can produce path-scoped context for BuildLang
today, then specify the bridge required when it cannot.

```text
root_context_status = MATCH
root_context_source_refs = 1
path_scoped_context = False
bridge_required = True
buildlang_present = True
compiler_present = True
build_universe_present = False
compose_status = MATCH
test_status = MATCH
```

## Focus Probes

- `index context --root C:\dev\public\pubscan\quantalang --json --focus buildlang` -> `EXPECTED_REJECT`
- `index context --root C:\dev\public\pubscan\quantalang --json --focus compiler` -> `EXPECTED_REJECT`
- `index context --root C:\dev\public\pubscan\quantalang --json --focus build-universe` -> `EXPECTED_REJECT`
- `index context-envelope --root C:\dev\public\pubscan\quantalang --json --focus buildlang --budget 3000` -> `EXPECTED_REJECT`

## Bridge

`index_path_selector_source_ref_bridge` should convert explicit path selectors
into source-ref manifests, preserve source-ref-only privacy, and reject missing
paths until a concrete source root exists.

## Negative Fixtures

- `claims_path_scoped_context_match` -> `focus_probes_rejected`
- `missing_root_context_envelope` -> `root_context_required`
- `missing_focus_probe_rejections` -> `negative_evidence_required`
- `claims_build_universe_top_level_present` -> `build_universe_absent_in_index_map`
- `missing_buildlang_source_receipt` -> `source_ref_receipt_required`
- `raw_private_payload_required` -> `source_refs_only_boundary`
- `claims_bridge_implemented_in_index` -> `bridge_plan_not_index_feature`
- `unsupported_claim_promoted` -> `unsupported_claim_count_nonzero`

Current promoted natural laws: none.
