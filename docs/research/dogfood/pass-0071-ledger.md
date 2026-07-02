# Pass 0071 Ledger: Live Workspace-Context Replacement

Date: 2026-07-01

Status: `MATCH_LIVE_WORKSPACE_CONTEXT_REPLACEMENT`

## Purpose

Replace the synthetic pass 0070 workspace-context component with a live local
Index context-envelope surface while preserving the live Telos action component
from pass 0070.

This pass tests a growth-vector question: can the megatool proof spine bind
workspace context as an independently replayable surface, instead of a static
hash borrowed from an earlier fixture?

## Artifacts

| Artifact | Purpose |
| --- | --- |
| `tools/compose_live_workspace_context_replacement.py` | Deterministic live Index workspace-context replacement composer. |
| `tools/test_live_workspace_context_replacement.py` | Focused live-surface and replay-boundary test. |
| `tools/probe_live_workspace_context_replacement.py` | Packet, thesis, and measurement generator. |
| `tools/validate_pass_0071_live_workspace_context_replacement.py` | Validator for live Index surface, required classes, negative fixtures, and replay boundaries. |
| `schemas/live-workspace-context-replacement-pass-0071.json` | `LiveWorkspaceContextReplacement/v1` artifact. |
| `schemas/pass-0071-live-workspace-context-replacement-validator-result.json` | Validator receipt. |
| `schemas/tool-receipts-pass-0071.json` | Compact Index, Forum, Gather, Crucible, Telos, and shell receipts. |
| `packets/081-live-workspace-context-replacement.md` | Human-readable live workspace-context replacement packet. |
| `adversarial/pass-0071-live-workspace-context-replacement-steelman.md` | Local steelman. |
| `crucible/pass-0071-thesis.json` | Falsifiable claims. |
| `crucible/pass-0071-measurements.json` | Measurements/evidence. |
| `crucible/pass-0071-report.md` | Crucible report. |
| `crucible/pass-0071-run.json` | Crucible run record. |

## Measurements

| Check | Result |
| --- | --- |
| Live Index command | `index context-envelope --root C:\dev\public\telos --budget 700 --hops 0 --json` |
| Live surface schema | `project-telos.context-envelope/v1` |
| Verification verdict | `MATCH` |
| Index surface checks | 8 MATCH, 0 DRIFT |
| Retained context items | 1 |
| Receipt count | 1 |
| Product packet component count | 6 |
| Negative fixtures | 7 |
| Ablation cases | 7 |
| Unsupported claims | 0 |

## Replaced Component

| Receipt class | Component |
| --- | --- |
| workspace_context | `index.context-envelope.live.root.0071` |

The product packet still joins source intake, workspace context, routing,
verification, continuity, and action. The action component remains
`telos.action.receipt.live.happy_path.0070`.

## Negative Fixtures

- `missing_workspace_context` rejects with `missing_required_class:workspace_context`.
- `missing_action` rejects with `missing_required_class:action`.
- `missing_verification` rejects with `missing_required_class:verification`.
- `live_workspace_digest_drift` rejects with `component_digest_drift:workspace_context`.
- `focus_path_unknown_repo` records the current path-focus failure: `unknown focus repo: docs/research/dogfood`.
- `raw_payload_required` rejects with `raw_private_payload_required`.
- `unsupported_claim_promoted` rejects with `unsupported_claim_count_nonzero`.

## Steelman

This improves the proof spine but does not prove complete repo understanding.
The live Index envelope is budgeted and root-level; it retained one context item
and one receipt. That is enough to bind a replayable workspace-context surface,
not enough to claim semantic coverage over BuildLang/buildc, color calibration,
biology, physics, agent ops, and market research all at once.

The most important growth-vector finding is the path-focus failure. A research
megatool needs to bind domain slices like `docs/research/dogfood`, `buildc`,
`color`, `physics`, `ai-infra`, or `market-recon` without treating the focus as
an unknown repo. Index should gain a path/domain focus mode, and Forum should
route those focus labels into the right research lane.

## Tool Findings

- Index status and doctor returned `MATCH`; live context-envelope returned `project-telos.context-envelope/v1`.
- Forum status and doctor returned `MATCH`.
- Gather read packet 081 with SHA256 `e83a753d7ad2500de315afbdb5eeaba6d8998ebc8e7f937218ae845f9934a812` and digest seal `fcefcbdab7d5bad195d349316bfdd2b4b8a0dd289a2c7eda8deb3d80682c77da`.
- Crucible result: 8 claims, 8 MATCH, 0 DRIFT, 0 UNVERIFIABLE.
- Crucible thesis id: `5fab8471116232a4`.
- Crucible assessment seal: `f6e5d6bf6678930e1fb778a4e5470c34fa6b10fdb6a20af9c8b40077803fa1f3`.
- Crucible registry stats after this pass: 59 theses, 489 claims, 489 MATCH, 0 DRIFT, 0 UNVERIFIABLE.
- Telos MCP context-envelope and server-manifest surfaces returned expected schemas; the `telos` CLI is not on PATH in this shell.

## Verification

```powershell
python docs\research\dogfood\tools\test_live_workspace_context_replacement.py
python docs\research\dogfood\tools\probe_live_workspace_context_replacement.py
python docs\research\dogfood\tools\validate_pass_0071_live_workspace_context_replacement.py
crucible run docs\research\dogfood\crucible\pass-0071-thesis.json --measurements docs\research\dogfood\crucible\pass-0071-measurements.json --registry docs\research\dogfood\crucible\registry --report docs\research\dogfood\crucible\pass-0071-report.md --out docs\research\dogfood\crucible\pass-0071-run.json --json
```

## Next Pass

Run a targeted Index path-focus advancement pass: define a path/domain focus
adapter that turns monorepo-relative paths into valid Index selection requests,
then rerun this proof-packet replacement with a domain-specific context slice.
The market-facing wedge is clear: field-specific proof packets need precise
workspace slices, not root-only context.
