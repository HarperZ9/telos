# Senses And Sensibility Subregistry

Date: 2026-07-02
Status: first research/philosophy corpus consolidation pass

Machine-readable registry:
`docs/registry/senses-and-sensibility-subregistry-2026-07-02.json`

This subregistry classifies `C:/dev/public/senses-and-sensibility` as a
research and philosophy corpus. It is not a tooling repo, not a shipped Project
Telos capability, and not a publication-ready dissertation or journal package.
The corpus is valuable because it names the accountability thesis behind Telos,
but its own stated gates must control how Telos cites it.

## Evidence Read

| Evidence | What it supports | Boundary |
| --- | --- | --- |
| Live Gather, Index, Forum, and Crucible status | Flagship tools are reachable and current for this pass. | Status only; not content correctness. |
| Index map at `2026-07-02T13:27:18-07:00` | Public root still has 68 repos, 62 public-class, 6 local-class, now 10 dirty repos. | Workspace map only; not publication review. |
| Gather docs seal `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945` | Gather verified a digest over the Senses directory. | Payload was dropped from the model-facing catalog because the corpus is large. |
| `git status` in Senses | Repo is clean and one commit behind `origin/main`. | Local checkout may not include the latest remote change. |
| `README.md`, `INDEX.md`, `THESIS.md`, `DISSERTATION-PROSPECTUS.md`, `THE-STRAIGHT-LINE.md` | Corpus frames itself as live scholarship, pre-proof, AI-assisted substrate, and human-gated. | Does not prove the philosophy or publication readiness. |
| Missing-artifact check | Current index prose references curation artifacts that are absent from the checkout. | Treat referenced missing files as quarantine until restored or references are patched. |

## Corpus Counts

| Surface | Count |
| --- | ---: |
| Markdown/RST docs | 172 |
| Preserved `.txt` source files | 1 |
| Root Markdown docs | 12 |
| `_front` docs | 4 |
| `conferred-existence` docs | 5 |
| `dissertation` docs | 125 |
| `papers` docs | 3 |
| `references` docs | 1 |
| `submission` docs | 4 |
| `thesis` docs | 18 |

## Classification Rows

| Row | Role | Publication action |
| --- | --- | --- |
| Front door and map | Public research-corpus entry points: `README.md`, `INDEX.md`, `CATALOG.md`, `THESIS.md`, `THE-STRAIGHT-LINE.md`, and related overview docs. | Keep linkable as research corpus, but repair missing curation references before stronger claims. |
| Integrated thesis | Large thesis substrate in `THESIS.md`. | Treat as dissertation substrate, not direct submission. |
| Dissertation apparatus | Prospectus, contribution ledger, viva prep, mock viva, verdicts, verification docs. | Use for publication gates and human-ownership rules. |
| Paper track | Three paper drafts, one membrane paper, and four submission kits. | Queue as paper candidates; all are gated on human re-derivation and live policy checks. |
| Bibliography and citation policy | `references/BIBLIOGRAPHY.md`. | Import the rule: no exact locators unless independently verified. |
| Source substrate | `CONFERRED-EXISTENCE.txt` plus `conferred-existence/**`. | Keep separate from Telos tool docs; cite by path/digest/summary only. |
| Engineering/security bridge | Membrane, authorization, action, and security-accountability theory docs. | Use as rationale for receipts and gates, not as implementation proof. |
| Adversarial verdict corpus | Cross-examination, suture, aseity, verdict, attack, and defense docs. | Translate method into Crucible critique patterns, not philosophical truth claims. |
| Referenced missing artifacts | `CURATION.md`, `CONSOLIDATION.md`, `CROSS-MODEL-AUDIT.md`, `HUMAN-GATE-RUNBOOK.md`, `submission/SHIPPING-MANIFEST.md`, `SPRINT.md`. | Quarantine these references until restored or corrected. |

## Publication Gates

- **Human re-derivation gate:** the author must reconstruct and defend claims
  without relying on the substrate.
- **Provenance ledger gate:** claim origin, candidate repair, citation
  verification, and AI assistance must be recorded before submission.
- **Live policy gate:** journal requirements, APCs, AI-use policies, word
  limits, and blinding rules must be checked at submission time.
- **Citation locator gate:** no page, volume, verse, or exact locator should be
  asserted unless independently verified against the edition used.
- **AI-use disclosure gate:** material generative drafting must be disclosed in
  the venue-appropriate location.
- **Anonymization gate:** submission kits must strip author-identifying corpus
  references for double-blind review.
- **Telos separation gate:** philosophy/theory corpus can motivate tools, but
  tool capability requires separate receipts, tests, and verifier reports.

## Telos Integration

1. **Publication gate import.** Add the human-ownership, provenance-ledger,
   citation-locator, and AI-disclosure gates to the Telos publication queue
   rubric.
2. **Theory-to-receipt vocabulary map.** Map authentication/authorization, human
   gate, witness, conferral, and proof-before-trust terms to Telos receipt
   vocabulary without overclaiming the philosophy.
3. **Adversarial review pattern.** Translate attack/defense/verdict material
   into Crucible cleanroom-review patterns for papers and proof demos.
4. **Missing-artifact repair pass.** Restore or correct the absent curation
   artifacts before the Senses corpus becomes a public publication hub.

## Hard Non-Claims

- This subregistry does not validate the philosophical thesis.
- This subregistry does not verify journal requirements or APC/pricing.
- This subregistry does not satisfy human authorship or institutional AI policy.
- This subregistry does not prove any Telos product capability.
- This subregistry does not make absent files present evidence.
- This subregistry does not certify citations, page numbers, or exact locators.

## Next Passes

1. Import the Senses publication gates into the Telos publication queue.
2. Run a targeted Senses repair pass for referenced-missing curation artifacts.
3. Decide whether Senses front-door docs should be patched in its own repo after
   rebasing the one-behind branch.
4. Keep Senses theory references in Telos docs as rationale or substrate unless
   a separate Telos receipt proves an implementation claim.
5. Create the Telos subregistry next; it is the remaining dense mixed surface
   after Build, proof/witnessing, and Senses.
