# Proof And Witnessing Subregistry

Date: 2026-07-02
Status: first proof/witnessing consolidation pass

Machine-readable registry:
`docs/registry/proof-witnessing-subregistry-2026-07-02.json`

This subregistry turns the proof and witnessing repos into a coherent Telos
verification substrate. The key discipline is separation: a witness is not a
validator, a validator is not an index, an index is not a release decision, a
report is not approval, and a theory corpus is not shipped product capability.

## Evidence Read

| Evidence | What it supports | Boundary |
| --- | --- | --- |
| `C:/dev/public/emet/README.md` and `SPEC.md` | EMET as an external witness with a closed `MATCH` / `DRIFT` / `UNVERIFIABLE` lattice. | No trust, approval, safety, authorization, or compliance verdict. |
| `C:/dev/public/proof-surface/README.md` and wedge docs | Proof Surface as validator contracts and eleven domain proof-packet wedges. | Validates records; does not execute actions or grant authority. |
| `C:/dev/public/repo-proof-index/README.md` and interop docs | Repo Proof Index as reviewer-ready proof artifact index. | Indexes evidence; does not decide sufficiency. |
| `C:/dev/public/proof-surface-report/README.md` | Reviewer-facing Markdown handoff renderer. | Evidence handoff only, not certification or release approval. |
| `C:/dev/public/witnessing-spine/README.md` | Citable publication corpus for the witnessing thesis. | Theory and market context, not product validation. |

## Layer Stack

| Layer | Tool | Job | Telos use |
| --- | --- | --- | --- |
| Witness | EMET | Re-derive raw bytes and source/view consistency into closed verdicts. | Source/view and report integrity witness. |
| Contract | Proof Surface | Validate evidence packets, receipts, gates, ledgers, and domain wedges. | Portable proof-packet contract layer. |
| Index | Repo Proof Index | Make proof artifacts discoverable and summarize evidence gaps. | Cross-repo proof inventory before release or publication. |
| Report | Proof Surface Report | Render proof packets and witness receipts into Markdown. | Reviewer handoff for demos, papers, and release bundles. |
| Theory | Witnessing Spine | Explain why external witnessing matters across sectors. | Publication and market-context reference. |

## Rows

| Row | Role | Maturity | Publication boundary |
| --- | --- | --- | --- |
| EMET | External witness and integrity layer. | Stable v1.0 witness spec with multi-language conformance docs. | Integrity/provenance only; no trust or approval language. |
| Proof Surface | Contract validators and proof-packet wedges. | Stdlib-only validator library with eleven domain wedges. | Validates records and honesty gates; does not grant authority. |
| Repo Proof Index | Reviewer-ready proof artifact index. | Python package and CLI for proof artifact indexing. | Evidence discovery only; no sufficiency decision. |
| Proof Surface Report | Markdown report renderer. | Small Python adapter with CLI and examples. | Evidence handoff only. |
| Witnessing Spine | Publication corpus. | Published/citable research corpus with DOI/ORCID metadata in README. | Theory corpus, not shipped product proof. |

## First Telos Bridges

1. **Agent action proof packet bridge.**
   Convert one Telos action receipt into a Proof Surface `agent-action` packet,
   re-derive verdicts with Crucible, and index the artifact with Repo Proof
   Index.

2. **Research claim packet bridge.**
   Convert one existing Telos causal or QEC research packet into a Proof Surface
   `research-claim` packet plus Proof Surface Report handoff.

3. **Visual measurement bridge.**
   Join Build Color, Calibrate Pro, and Proof Surface `visual-measurement` for
   a read-only color measurement packet with artifact digest, metrics, and
   display caveats.

4. **AI4Science bridge.**
   Join Gather, BuildLang/buildc, Proof Surface `ai4science`, Crucible, and
   Learning Forge for one claim-to-experiment packet with measurement,
   reproduction status, reviewer objections, and negative-result handling.

## Hard Non-Claims

- EMET does not emit `TRUSTED`, `APPROVED`, or `SAFE`.
- Proof Surface validates records; it does not grant authority, execute
  actions, or store private payloads.
- Repo Proof Index indexes proof artifacts; it does not decide if the evidence
  is enough.
- Proof Surface Report renders evidence; it does not certify, approve, or
  declare compliance.
- Witnessing Spine supports the theory and market context; it does not prove a
  Telos product capability shipped.

## Next Passes

1. Create one Telos proof-surface bridge fixture from an existing research
   packet.
2. Run Repo Proof Index over selected Telos proof artifacts after deciding which
   working-tree proof files are in scope.
3. Add Witnessing Spine to the publication queue as theory context.
4. Render one proof-demo report with Proof Surface Report.
5. Keep the public copy separated by layer: witness, contract, index, report,
   theory.
