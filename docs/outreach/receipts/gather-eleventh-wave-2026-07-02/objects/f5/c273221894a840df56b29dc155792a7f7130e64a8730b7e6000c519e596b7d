# Pass 0080 Ledger: BuildLang Proof-Packet Demo Surface

Date: 2026-07-01

Status: `MATCH_BUILDLANG_PROOF_PACKET_DEMO_SURFACE`

## Purpose

Package a buyer-facing BuildLang proof-packet demo surface by binding source
intake, path-scoped workspace context, a fresh live `buildc` corpus receipt,
Forum routing evidence, negative fixtures, a packet, a brief, and Crucible
verdicts.

## Artifacts

| Artifact | Purpose |
| --- | --- |
| `tools/compose_buildlang_proof_packet_demo_surface.py` | Demo surface composer with live `buildc` and Forum route receipts. |
| `tools/test_buildlang_proof_packet_demo_surface.py` | Focused demo surface test. |
| `tools/probe_buildlang_proof_packet_demo_surface.py` | Packet, brief, thesis, and measurement generator. |
| `tools/validate_pass_0080_buildlang_proof_packet_demo_surface.py` | Validator for proof surface, live receipt, route, and promotion boundaries. |
| `schemas/buildlang-proof-packet-demo-surface-pass-0080.json` | `BuildLangProofPacketDemoSurface/v1` artifact. |
| `schemas/pass-0080-buildlang-proof-packet-demo-surface-validator-result.json` | Validator receipt. |
| `schemas/tool-receipts-pass-0080.json` | Compact Gather, Crucible, Telos, and shell receipts. |
| `packets/090-buildlang-proof-packet-demo-surface.md` | Human-readable proof-packet demo packet. |
| `briefs/090-buildlang-proof-packet-demo-brief.md` | Buyer-facing BuildLang proof-packet demo brief. |
| `adversarial/pass-0080-buildlang-proof-packet-demo-surface-steelman.md` | Local steelman. |
| `crucible/pass-0080-thesis.json` | Falsifiable claims. |
| `crucible/pass-0080-measurements.json` | Measurements/evidence. |
| `crucible/pass-0080-report.md` | Crucible report. |
| `crucible/pass-0080-run.json` | Crucible run record. |

## Measurements

| Check | Result |
| --- | --- |
| Source intake | pass 0074, 13 source refs |
| Workspace context | pass 0079, 128 path-scoped source refs |
| Path-scoped context | `true` |
| Root-context fallback | `false` |
| Live `buildc` corpus | `MATCH`, 10 expected lines matched |
| Forum route | `MATCH`, `needs_escalation=true` |
| Top Forum candidate | `sdk-platform` |
| Negative fixtures | 9 |
| Unsupported claims | 0 |
| Promoted natural laws | 0 |

## Buyer Brief

The brief positions BuildLang proof packets as portable evidence chains for
compiler and scientific-compute work. The differentiated wedge is not broad
language replacement; it is cross-layer proof: what was inspected, what was
executed, what was rejected, and what can be rechecked.

## Boundaries

This pass does not prove Julia replacement, all backend maturity, native Index
path selection, Build Universe coverage, market adoption, scientific discovery,
or a natural law.

## Tool Findings

- Gather read packet 090 with SHA256
  `36dfd6e3c8334d2db68ab7fe50b87d09dcd5af8f71cb9a87498a56d383c820f1` and digest
  seal `3d022600935ddc18e38cfe1967902d449445c1bd81316230b5a4159254ddc439`.
- Gather read the buyer brief with SHA256
  `8645d62e81f1b18a0a313d648da74beebcb572aff1fabcc78016ef46ae7d06ca` and digest
  seal `35ca436ad8a87ff9045effbb742cca4b206293ad124e6944642fc6d8870cb15a`.
- Crucible result: 8 claims, 8 MATCH, 0 DRIFT, 0 UNVERIFIABLE.
- Crucible thesis id: `d87ec0e84aeb2630`.
- Crucible assessment seal:
  `8e174504499e9279bf1b7a6d3c4257760c4b907b2b4ba892db3d43894ef77a5e`.
- Crucible registry stats after this pass: 68 theses, 561 claims, 561 MATCH,
  0 DRIFT, 0 UNVERIFIABLE.

## Verification

```powershell
python docs\research\dogfood\tools\test_buildlang_proof_packet_demo_surface.py
python -m py_compile docs\research\dogfood\tools\compose_buildlang_proof_packet_demo_surface.py docs\research\dogfood\tools\probe_buildlang_proof_packet_demo_surface.py docs\research\dogfood\tools\test_buildlang_proof_packet_demo_surface.py docs\research\dogfood\tools\validate_pass_0080_buildlang_proof_packet_demo_surface.py
python docs\research\dogfood\tools\probe_buildlang_proof_packet_demo_surface.py
python docs\research\dogfood\tools\validate_pass_0080_buildlang_proof_packet_demo_surface.py
crucible run docs\research\dogfood\crucible\pass-0080-thesis.json --measurements docs\research\dogfood\crucible\pass-0080-measurements.json --registry docs\research\dogfood\crucible\registry --report docs\research\dogfood\crucible\pass-0080-report.md --out docs\research\dogfood\crucible\pass-0080-run.json --json
gather docs docs\research\dogfood\packets\090-buildlang-proof-packet-demo-surface.md --json
gather docs docs\research\dogfood\briefs\090-buildlang-proof-packet-demo-brief.md --json
crucible registry stats docs\research\dogfood\crucible\registry --json
```

## Next Pass

Use this BuildLang demo surface as the template for a second domain packet:
either a visual-truth/color proof packet refresh or an AI4Science claim-ledger
packet with explicit unverified boundaries.
