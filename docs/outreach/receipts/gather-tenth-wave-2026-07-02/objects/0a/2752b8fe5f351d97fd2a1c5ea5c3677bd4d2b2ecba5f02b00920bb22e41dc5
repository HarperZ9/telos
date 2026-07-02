# Pass 0064 Ledger: Agent Observability Action-Receipt Adapter Matrix

Date: 2026-07-01

Status: `MATCH_AGENT_OBSERVABILITY_ADAPTER_MATRIX`

## Purpose

Deepen the top-ranked pass 0063 wedge: agent observability-to-action-receipt
proof packets. This pass maps incumbent observability/eval systems to the
Telos layer they do not automatically provide in the current product framing:
source refs, workspace state, authority scope, action admission,
side-effect class, stop reason, verification verdict, privacy boundary, and
compensation pointer.

This is not a replacement claim. Telos should preserve incumbent trace and eval
objects, then wrap them in accountable action receipts.

## Artifacts

| Artifact | Purpose |
| --- | --- |
| `tools/compose_agent_observability_action_receipt_adapter_matrix.py` | Deterministic adapter-matrix composer. |
| `tools/test_agent_observability_action_receipt_adapter_matrix.py` | Focused RED/GREEN adapter matrix test. |
| `tools/probe_agent_observability_action_receipt_adapter_matrix.py` | Packet, thesis, and measurement generator. |
| `tools/validate_pass_0064_agent_observability_action_receipt_adapter_matrix.py` | Validator for adapters, source anchors, receipt fields, and non-replacement controls. |
| `schemas/agent-observability-action-receipt-adapter-matrix-pass-0064.json` | `AgentObservabilityActionReceiptAdapterMatrix/v1` artifact. |
| `schemas/pass-0064-agent-observability-action-receipt-adapter-matrix-validator-result.json` | Validator receipt. |
| `schemas/tool-receipts-pass-0064.json` | Compact Index, Gather, Forum, Crucible, Telos, and shell receipts. |
| `packets/074-agent-observability-action-receipt-adapter-matrix.md` | Human-readable adapter packet. |
| `adversarial/pass-0064-agent-observability-action-receipt-adapter-matrix-steelman.md` | Local steelman. |
| `crucible/pass-0064-thesis.json` | Falsifiable claims. |
| `crucible/pass-0064-measurements.json` | Measurements/evidence. |
| `crucible/pass-0064-report.md` | Crucible report. |
| `crucible/pass-0064-run.json` | Crucible run record. |

## Adapter Rows

| Tool | Priority | Native refs to preserve |
| --- | ---: | --- |
| LangSmith | 5 | trace_ref, run_url, evaluation_ref |
| Langfuse | 5 | trace_id, prompt_version, score_ref |
| Arize Phoenix | 5 | span_id, trace_id, annotation_ref |
| Braintrust | 5 | experiment_id, trace_ref, eval_ref |
| OpenTelemetry | 5 | trace_id, span_id, metric_ref, log_ref |
| MLflow | 4 | run_id, model_version, artifact_uri |
| W&B Weave | 4 | call_ref, evaluation_ref, dataset_ref |
| DVC | 3 | dvc_stage, data_hash, pipeline_ref |
| promptfoo | 4 | eval_report, red_team_case, ci_result |
| Helicone | 4 | request_id, provider_route, cost_ref |

## Required Telos Receipt Fields

`receipt_id`, `schema`, `source_refs`, `workspace_state`, `authority_scope`,
`action_admission`, `tool_call`, `side_effect_class`, `materials_digest`,
`trace_refs`, `eval_refs`, `model_refs`, `runtime_refs`,
`verification_verdict`, `stop_reason`, `compensation_pointer`,
`privacy_boundary`, `receipt_status`.

## Measurements

| Check | Result |
| --- | --- |
| Source anchors | 10 |
| Adapter rows | 10 |
| Receipt fields | 18 |
| Demo slices | 3 |
| Unsupported uniqueness claims | 0 |
| Non-replacement claim | true |

## Source Anchors

The artifact records official-source anchors for LangSmith, Langfuse, Arize
Phoenix, Braintrust, OpenTelemetry, MLflow, W&B Weave, DVC, promptfoo, and
Helicone.

## Tool Findings

- Index status returned `MATCH`.
- Gather read packet 074 with SHA256 `2cfb44ab8f21615243cd5d9d77934198b3915b62ccd4a383cc6ece4f436a6de6` and digest seal `c2e230b423dc68db6149179222b0f306ea539f7ff288fbe277394bfc51287c09`.
- Forum ledger verified `chain=true`, `deep=true`.
- Crucible result: 8 claims, 8 MATCH, 0 DRIFT, 0 UNVERIFIABLE.
- Crucible thesis id: `34c751ce802ad08a`.
- Crucible assessment seal: `002dfed22d92866332b4e0d9f22f5f2b00707f048dda68be200e579928552be3`.
- Crucible registry stats after this pass: 52 theses, 434 claims, 434 MATCH, 0 DRIFT, 0 UNVERIFIABLE.
- Telos workflow returned `MATCH`.

## Verification

```powershell
python docs\research\dogfood\tools\test_agent_observability_action_receipt_adapter_matrix.py
python docs\research\dogfood\tools\probe_agent_observability_action_receipt_adapter_matrix.py
python docs\research\dogfood\tools\validate_pass_0064_agent_observability_action_receipt_adapter_matrix.py
crucible run docs\research\dogfood\crucible\pass-0064-thesis.json --measurements docs\research\dogfood\crucible\pass-0064-measurements.json --registry docs\research\dogfood\crucible\registry --report docs\research\dogfood\crucible\pass-0064-report.md --out docs\research\dogfood\crucible\pass-0064-run.json --json
```

## Next Pass

Build pass 0065 as one of:

1. an executable OpenTelemetry trace-to-Telos action-receipt fixture, or
2. a buyer-facing one-page spec for regulated agent action receipts.
