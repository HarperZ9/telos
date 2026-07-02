# Packet 074: Agent Observability Action-Receipt Adapter Matrix

Date: 2026-07-01

Status: `AGENT_OBSERVABILITY_ACTION_RECEIPT_ADAPTER_MATRIX_MATCH`

Purpose: define how Telos should preserve incumbent observability and eval refs while adding authority, workspace, side-effect, admission, verification, and compensation receipt layers.

```text
source_anchor_count = 10
adapter_count = 10
receipt_field_count = 18
unsupported_uniqueness_claim_count = 0
non_replacement_claim = True
compose_status = MATCH
test_status = MATCH
```

## Adapter Rows

- `LangSmith` priority `5` preserves `trace_ref, run_url, evaluation_ref`.
- `Langfuse` priority `5` preserves `trace_id, prompt_version, score_ref`.
- `Arize Phoenix` priority `5` preserves `span_id, trace_id, annotation_ref`.
- `Braintrust` priority `5` preserves `experiment_id, trace_ref, eval_ref`.
- `OpenTelemetry` priority `5` preserves `trace_id, span_id, metric_ref, log_ref`.
- `MLflow` priority `4` preserves `run_id, model_version, artifact_uri`.
- `W&B Weave` priority `4` preserves `call_ref, evaluation_ref, dataset_ref`.
- `DVC` priority `3` preserves `dvc_stage, data_hash, pipeline_ref`.
- `promptfoo` priority `4` preserves `eval_report, red_team_case, ci_result`.
- `Helicone` priority `4` preserves `request_id, provider_route, cost_ref`.

## Action Receipt Fields

- `receipt_id`
- `schema`
- `source_refs`
- `workspace_state`
- `authority_scope`
- `action_admission`
- `tool_call`
- `side_effect_class`
- `materials_digest`
- `trace_refs`
- `eval_refs`
- `model_refs`
- `runtime_refs`
- `verification_verdict`
- `stop_reason`
- `compensation_pointer`
- `privacy_boundary`
- `receipt_status`

## Demo Slices

- `otel_trace_to_action_receipt`: convert one OpenTelemetry trace into a Telos action receipt with source refs, side-effect class, and Crucible verdict
- `langfuse_langsmith_eval_bridge`: preserve one Langfuse or LangSmith trace and add admission, workspace, stop reason, and replay fields
- `promptfoo_redteam_to_verdict_packet`: bind one promptfoo red-team report to a Telos verification packet and compensation pointer
