# Packet 082: Domain-Focus Adapter Experiment

Date: 2026-07-01

Status: `DOMAIN_FOCUS_ADAPTER_EXPERIMENT_MATCH`

Purpose: test whether domain-specific growth vectors can be routed and
packaged across Gather, Index, Forum, Crucible, and Telos as one adapter layer.

```text
domain_count = 6
adapted_project_telos = 6
adapted_escalations = 0
valid_index_focuses = ['telos']
rejected_index_focus_count = 7
compose_status = MATCH
test_status = MATCH
```

## Domain Rows

- `buildlang_buildc`: route `MATCH`, strategy `repo_root_context_plus_domain_path_filter_pending`
- `color_calibration`: route `MATCH`, strategy `repo_root_context_plus_domain_path_filter_pending`
- `ai4science`: route `MATCH`, strategy `repo_root_context_plus_domain_path_filter_pending`
- `agent_ops`: route `MATCH`, strategy `repo_root_context_plus_domain_path_filter_pending`
- `market_recon`: route `MATCH`, strategy `repo_root_context_plus_domain_path_filter_pending`
- `quantum_physics`: route `MATCH`, strategy `repo_root_context_plus_domain_path_filter_pending`

## Tool Improvement Queue

- `index`: path and domain labels are rejected as focus repos -> add path/domain focus adapter that resolves labels to repo root plus source-ref filters
- `forum`: domain prompts need operator-spine bridge vocabulary to route decisively -> teach router domain-focus vocabulary directly
- `gather`: domain packets need catalog-level grouping -> emit domain catalog receipts keyed by field and buyer
- `crucible`: domain focus needs reusable negative fixtures -> create standard route/focus gates for proof-packet promotion
- `telos`: domain focus is not yet a product-level envelope -> define TelosDomainFocusEnvelope/v1 as a megatool join layer

## Negative Fixtures

- `raw_domain_prompt_without_bridge` -> `forum_route_needs_escalation`
- `path_focus_direct_to_index` -> `unknown_focus_repo`
- `root_context_claims_domain_coverage` -> `root_context_not_domain_semantic_coverage`
- `missing_crucible_domain_gate` -> `unverified_domain_packet_promotion`
- `unsupported_claim_promoted` -> `unsupported_claim_count_nonzero`
- `raw_payload_required` -> `raw_private_payload_required`

Current promoted natural laws: none.
