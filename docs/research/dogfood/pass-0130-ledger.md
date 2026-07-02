# Pass 0130 Ledger: Brandom Work Lesson Graph

Date: 2026-07-01

## Objective

Deepen the pass 0129 Brandom functional-learning digest into a work-level
catalog and bounded lesson graph. This pass treats Brandom's texts and course
pages as source-backed learning substrate, then converts that substrate into
checkable learner actions: source intake, vocabulary identification,
inferential links, scorekeeping, challenge/repair, and AI-assistant action
receipts.

## Artifacts

| Artifact | Purpose |
| --- | --- |
| `tools/compose_brandom_work_lesson_graph.py` | Composer for Brandom source receipts, work catalog, lesson graph, learner action fixture, product hypotheses, and negative controls. |
| `tools/test_brandom_work_lesson_graph.py` | Focused TDD test for pass 0130. |
| `tools/validate_pass_0130_brandom_work_lesson_graph.py` | Validator for source receipts, graph invariants, learner fixture, negative controls, flagships, and artifact seal. |
| `tools/probe_brandom_work_lesson_graph.py` | Packet, brief, steelman, thesis, measurement, and tool-receipt generator. |
| `schemas/brandom-work-lesson-graph-pass-0130.json` | `BrandomWorkLessonGraphReceipt/v1` artifact. |
| `schemas/pass-0130-brandom-work-lesson-graph-validator-result.json` | Validator receipt. |
| `schemas/tool-receipts-pass-0130.json` | Compact source, work graph, Forum, Index, Telos, catalog, compose, test, and validator receipts. |
| `packets/140-brandom-work-lesson-graph.md` | Human-readable pass 0130 work lesson graph packet. |
| `briefs/140-brandom-work-lesson-graph-brief.md` | Buyer-facing pass 0130 learning-tool brief. |
| `adversarial/pass-0130-brandom-work-lesson-graph-steelman.md` | Local pass 0130 steelman. |
| `crucible/pass-0130-thesis.json` | Falsifiable claims. |
| `crucible/pass-0130-measurements.json` | Measurements/evidence. |
| `crucible/pass-0130-report.md` | Crucible report. |
| `crucible/pass-0130-run.json` | Crucible run record. |
| `gather/pass-0130-brandom-work-lesson-graph/` | Gather source store for five selected Brandom texts and course pages. |

## Result

| Measurement | Value |
| --- | --- |
| Artifact status | `BRANDOM_WORK_LESSON_GRAPH_MATCH` |
| Artifact sha256 | `1602d70d19c95bc0696b4063f56678deed74807643e0b618baa608c894ea46dd` |
| Artifact seal | `ff9b4fb1da095a4cee0ee2eda60f48347b00d2e901c1ef8365b7e8ca31e1fea4` |
| Gather source receipts | `5` |
| Cataloged works | `5` |
| Lesson nodes | `6` |
| Lesson edges | `5` |
| Product hypotheses | `3` |
| Learner action fixture | `MATCH` |
| Negative fixtures rejected | `5` |
| Unsupported claim count | `0` |
| Current promoted natural laws | `0` |

Boundary: this pass catalogs five gathered Brandom texts/course pages and
builds a bounded lesson graph. It does not export PDF bodies, prove learning
efficacy, complete Brandom's bibliography, or promote philosophical claims as
natural laws.

## Source Receipts

| Source | Kind | sha256 | status |
| --- | --- | --- | --- |
| `https://sites.pitt.edu/~rbrandom/Courses/2023%20Sellars/SM%202023%20Main%20n.html` | course page | `ebc0d410cb6a8a6ac16fadc5767b8a62ed8d7b1c225a886e2761850d7498fd6d` | `GATHER_VERIFIED` |
| `https://sites.pitt.edu/~rbrandom/Courses/2024%20Philosophy%20of%20Language/Language%20and%20Reasons%202024%20Main.html` | course page | `c938aaf054342470003135a9550f40e58e240435827052788542a932b4d5eb52` | `GATHER_VERIFIED` |
| `https://sites.pitt.edu/~rbrandom/Texts/Artificial_Intelligence_and_Analytic_Pra.pdf` | downloadable text | `997db0e31b2ef1995db788ea14352978d0ec44b29781053fb4d4cc638457155d` | `GATHER_VERIFIED` |
| `https://sites.pitt.edu/~rbrandom/Texts/Inferentialism_Normative_Pragmatism_and.pdf` | downloadable text | `263c5077f53fe41a5bdfdac70507bd56fc286f635d1cdbb8d4caa6e871deca7a` | `GATHER_VERIFIED` |
| `https://sites.pitt.edu/~rbrandom/Texts/Vocabularies%20of%20Reason%2025-5-23%20b.pdf` | downloadable text | `049f1b64f012089d082fec5101fb207323a17f76603d92945ea6809ed392fdca` | `GATHER_VERIFIED` |

## Work Catalog

| Work | Source kind | Dominant terms | Status |
| --- | --- | --- | --- |
| `SM 2023 Main n` | `course_page` | `Sellars`, `expressivism`, `semantics`, `logic`, `modality` | `CATALOGED_FROM_GATHER_RECEIPT` |
| `Language and Reasons 2024 Main` | `course_page` | `reason`, `logic`, `language`, `expressivism`, `semantics` | `CATALOGED_FROM_GATHER_RECEIPT` |
| `Artificial Intelligence and Analytic Pra` | `downloadable_text` | `artificial intelligence` | `CATALOGED_FROM_GATHER_RECEIPT` |
| `Inferentialism Normative Pragmatism and` | `downloadable_text` | `inferentialism`, `pragmatism` | `CATALOGED_FROM_GATHER_RECEIPT` |
| `Vocabularies of Reason 25-5-23 b` | `downloadable_text` | `reason` | `CATALOGED_FROM_GATHER_RECEIPT` |

## Lesson Graph

| Node | Kind | Exercise |
| --- | --- | --- |
| `source_intake` | `source` | Identify which claims have receipts and which are missing. |
| `vocabulary` | `concept` | Mark terms that function as explicit vocabulary for a practice. |
| `inferential_link` | `concept` | Convert one reading claim into antecedent, rule, and consequence. |
| `scorekeeping` | `practice` | Given `p` and `p -> q`, record the commitment and entitlement ledger. |
| `challenge_repair` | `practice` | Reject an unsupported inference and add the missing source or rule. |
| `ai_application` | `tool` | Design a model action receipt that distinguishes assertion, inference, and repair. |

Graph invariant: all edges resolve, and every node has source references plus
an exercise. The edge chain is `source_intake -> vocabulary -> inferential_link
-> scorekeeping -> challenge_repair -> ai_application`.

## Learner Action Fixture

The bounded fixture requires a source, claim, exercise, and verifier before
accepting a learner answer. The accepted sequence is: cite source, state claim,
add inference, and submit answer. Status: `MATCH`.

## Product Hypotheses

| Tool | Status | Wedge |
| --- | --- | --- |
| `Lesson Graph Builder` | `HYPOTHESIS` | Source-backed course-to-exercise transformation. |
| `Reason Ledger Tutor` | `HYPOTHESIS` | Commitment, entitlement, challenge, and repair as checkable learner actions. |
| `AI Philosophy Lab` | `HYPOTHESIS` | AI assistance constrained by reason-action receipts. |

## Negative Controls

| Fixture | Status | Failure reason |
| --- | --- | --- |
| `filename_as_claim_rejected` | `REJECTED` | `filename_is_catalog_hint,requires_body_or_source_claim` |
| `pdf_body_export_rejected` | `REJECTED` | `copyright_boundary,receipt_digest_only` |
| `course_page_as_complete_syllabus_rejected` | `REJECTED` | `course_page_is_partial,requires_session_level_intake` |
| `lesson_graph_as_learning_efficacy_rejected` | `REJECTED` | `no_user_study,no_outcome_measure` |
| `philosophy_to_scientific_law_rejected` | `REJECTED` | `humanities_corpus,not_natural_law` |

## Gather

| Document | sha256 | seal |
| --- | --- | --- |
| `packets/140-brandom-work-lesson-graph.md` | `59e8598a0464cb9797a42863bfdb50c6df7ecbaad89f98efcb1516d1dd9dbd94` | `c2c7e2d5281031583bbd4037e40966455ccce083ef43027e4662ef5c0d10a373` |
| `briefs/140-brandom-work-lesson-graph-brief.md` | `156b4e0334927b05ccaffdca10a07366b6a6a0d5c234be5373cf1eca98b297f3` | `b82a5f05b604c75897fb35e8ac1ddd2ecede13d636df644676f8651bbf3b09c3` |

## Crucible

| Measurement | Value |
| --- | --- |
| Thesis id | `7a27b8da4fb83edd` |
| Thesis seal | `7a27b8da4fb83edd3d4e6bfff1782f94635f8bcb6dc7808d0eef774cf92782a0` |
| Claims | `12` |
| MATCH | `12` |
| DRIFT | `0` |
| UNVERIFIABLE | `0` |
| Verdict seal | `50c921898e3d7930512349192f50366a37c7b397322b859e78999c17be59e1ff` |
| Measurement seal | `5e25996087abb2425a2d33becdb5ee744de002f391e06aa546cb26c3f27d76fd` |
| Assessment seal | `50a259bd32a790449347f7c587141714e21febb44dc2509f97993d383d477ec9` |

Registry after pass 0130:

- theses: `122`;
- claims: `1105`;
- verdicts: `1105 MATCH`, `0 DRIFT`, `0 UNVERIFIABLE`;
- invalid latest assessments: `0`.

## File Hashes

| File | sha256 |
| --- | --- |
| `schemas/brandom-work-lesson-graph-pass-0130.json` | `1602d70d19c95bc0696b4063f56678deed74807643e0b618baa608c894ea46dd` |
| `schemas/pass-0130-brandom-work-lesson-graph-validator-result.json` | `d281ea2a11bfd5ce14f47a4d1156faae3c626e9484a081bb646097854b0890e4` |
| `schemas/tool-receipts-pass-0130.json` | `6668185973fa5df5d261f80ffc927ed48c37b3cad07f26e8522eca25d733ebc9` |
| `packets/140-brandom-work-lesson-graph.md` | `59e8598a0464cb9797a42863bfdb50c6df7ecbaad89f98efcb1516d1dd9dbd94` |
| `briefs/140-brandom-work-lesson-graph-brief.md` | `156b4e0334927b05ccaffdca10a07366b6a6a0d5c234be5373cf1eca98b297f3` |
| `adversarial/pass-0130-brandom-work-lesson-graph-steelman.md` | `ec362b83b852eec8cbda1288a3307aa11f946128108ef636989abfe60fc3ad5d` |
| `crucible/pass-0130-thesis.json` | `133ad5ab24d4cc7a680f6e8914ffc17b0770b3398dac7f245ad9dcd124ddd5c2` |
| `crucible/pass-0130-measurements.json` | `f199c21cfae77b5b5183b718e4acff10596a0d6e068fa6ee102a049e610bbaa1` |
| `crucible/pass-0130-report.md` | `2a92b40c34690c3f0507c8616241c6941fc7d3bfe7c023d4cf9d1dbb7cc98d71` |
| `crucible/pass-0130-run.json` | `eea926a300227732ca46605bf70e3db23155295334ea65445d76e318867f9233` |
| `tools/compose_brandom_work_lesson_graph.py` | `29f54668abf8d24b602a30beac9ae1565ca44881f26dcb6cc159fdc31c9c5b3a` |
| `tools/test_brandom_work_lesson_graph.py` | `69fa6bea6b360e18826957b8f383c723f491ccbfe18fe5988a6b46f30a20c5ca` |
| `tools/validate_pass_0130_brandom_work_lesson_graph.py` | `80c9d6b110015c484dc67f57e814de5b14e2b2d25d5376431f79ce1a8c5128e2` |
| `tools/probe_brandom_work_lesson_graph.py` | `fc17e90d6aa68c989a93e328889f1ca0c08494f3c9f375b6ba6cb28b1ac09699` |

## Verification Commands

```powershell
python -m py_compile docs\research\dogfood\tools\compose_brandom_work_lesson_graph.py docs\research\dogfood\tools\test_brandom_work_lesson_graph.py docs\research\dogfood\tools\validate_pass_0130_brandom_work_lesson_graph.py docs\research\dogfood\tools\probe_brandom_work_lesson_graph.py
python docs\research\dogfood\tools\test_brandom_work_lesson_graph.py
python docs\research\dogfood\tools\probe_brandom_work_lesson_graph.py
python docs\research\dogfood\tools\validate_pass_0130_brandom_work_lesson_graph.py
gather docs docs\research\dogfood\packets\140-brandom-work-lesson-graph.md --json
gather docs docs\research\dogfood\briefs\140-brandom-work-lesson-graph-brief.md --json
crucible run docs\research\dogfood\crucible\pass-0130-thesis.json --measurements docs\research\dogfood\crucible\pass-0130-measurements.json --registry docs\research\dogfood\crucible\registry --report docs\research\dogfood\crucible\pass-0130-report.md --out docs\research\dogfood\crucible\pass-0130-run.json --json
crucible registry stats docs\research\dogfood\crucible\registry --json
```

## Next Pass

The next pass should expand from five works into a Brandom-derived tradition
atlas. Candidate inputs: Sellars, Kant, Hegel, Rorty, Frege, Wittgenstein,
inferentialism, pragmatism, expressivism, semantic holism, and AI-as-reasoning
source leads. The practical target is a `TraditionDerivationAtlasReceipt` that
turns intellectual dependencies into prerequisite graphs, learner exercises,
market gaps for functional-learning tools, and Crucible-checked overclaim
rejections.
