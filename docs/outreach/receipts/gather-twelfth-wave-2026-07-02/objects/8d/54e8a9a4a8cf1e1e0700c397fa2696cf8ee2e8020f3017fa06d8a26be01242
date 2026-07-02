# Packet 085: BuildLang Domain-Envelope Join

Date: 2026-07-01

Status: `BUILDLANG_DOMAIN_ENVELOPE_JOIN_MATCH`

Purpose: join the BuildLang source-ref receipt from pass 0074 into the
`buildlang_buildc` Telos domain-focus envelope from pass 0073.

```text
domain_id = buildlang_buildc
source_component = buildlang.source-ref.receipt.0074
source_ref_count = 13
corpus_verify_status = MATCH
joined_envelope = telos.domain-focus.buildlang_buildc.0075
root_context_fallback = True
path_scoped_context = False
compose_status = MATCH
test_status = MATCH
```

## Boundary

The source-intake layer is now domain-specific for BuildLang/buildc. The
workspace-context layer is still the live root Index envelope, not path-scoped
BuildLang context.

## Negative Fixtures

- `missing_buildlang_source_receipt` -> `missing_domain_source_receipt`
- `buildc_corpus_verify_drift` -> `corpus_verify_not_match`
- `source_digest_drift` -> `source_ref_digest_drift`
- `claims_path_scoped_context_without_index_refs` -> `path_scoped_context_unproven`
- `claims_all_backends_production` -> `experimental_backends_promoted`
- `self_hosted_compiler_promoted` -> `self_hosted_compiler_unverified`
- `raw_payload_required` -> `raw_private_payload_required`
- `unsupported_claim_promoted` -> `unsupported_claim_count_nonzero`

Current promoted natural laws: none.
