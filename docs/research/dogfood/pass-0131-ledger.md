# Pass 0131 Ledger: Tradition Derivation Atlas

Date: 2026-07-01

## Objective

Expand the Brandom work/lesson graph into a source-backed tradition atlas for
functional-learning tooling. This pass maps a sampled set of predecessor and
contrast anchors into bounded prerequisite/contrast edges, learner modules,
product hypotheses, and overclaim gates.

## Artifacts

| Artifact | Purpose |
| --- | --- |
| `tools/compose_tradition_derivation_atlas.py` | Composer for source receipts, tradition nodes, bounded hypothesis edges, learning modules, product hypotheses, flagships, and negative controls. |
| `tools/test_tradition_derivation_atlas.py` | Focused TDD test for pass 0131. |
| `tools/validate_pass_0131_tradition_derivation_atlas.py` | Validator for source receipts, edge boundaries, graph resolution, negative controls, flagships, and artifact seal. |
| `tools/probe_tradition_derivation_atlas.py` | Packet, brief, steelman, thesis, measurement, and tool-receipt generator. |
| `schemas/tradition-derivation-atlas-pass-0131.json` | `TraditionDerivationAtlasReceipt/v1` artifact. |
| `schemas/pass-0131-tradition-derivation-atlas-validator-result.json` | Validator receipt. |
| `schemas/tool-receipts-pass-0131.json` | Compact source, graph, Forum, Index, Telos, catalog, compose, test, and validator receipts. |
| `packets/141-tradition-derivation-atlas.md` | Human-readable pass 0131 tradition atlas packet. |
| `briefs/141-tradition-derivation-atlas-brief.md` | Buyer-facing pass 0131 learning-tool brief. |
| `adversarial/pass-0131-tradition-derivation-atlas-steelman.md` | Local pass 0131 steelman. |
| `crucible/pass-0131-thesis.json` | Falsifiable claims. |
| `crucible/pass-0131-measurements.json` | Measurements/evidence. |
| `crucible/pass-0131-report.md` | Crucible report. |
| `crucible/pass-0131-run.json` | Crucible run record. |
| `gather/pass-0131-tradition-derivation-atlas/` | Gather source store for 10 tradition anchors. |

## Result

| Measurement | Value |
| --- | --- |
| Artifact status | `TRADITION_DERIVATION_ATLAS_MATCH` |
| Artifact sha256 | `ea8cceda1433286f97914368ac0bc180e3b85e9b424ff7f026ae3110f54930e0` |
| Artifact seal | `69312c0f6f914696201cb9153b2893b222671a59c012697b4f569a9d49209d45` |
| Gather source receipts | `10` |
| Atlas nodes | `10` |
| Atlas edges | `13` |
| Learning modules | `5` |
| Product hypotheses | `4` |
| Negative fixtures rejected | `6` |
| Unsupported claim count | `0` |
| Current promoted natural laws | `0` |

Boundary: this pass builds a sampled, source-backed tradition atlas. Edges are
prerequisite or contrast hypotheses, not complete genealogy, causality proof,
learning-efficacy evidence, or natural-law promotion.

## Source Receipts

| Source | sha256 | status |
| --- | --- | --- |
| `https://plato.stanford.edu/entries/frege/` | `e0b3ca8f7c64a7d86433f2d27749f581ad9ffe31ef6ec8050bcd21538456ab4e` | `GATHER_VERIFIED` |
| `https://plato.stanford.edu/entries/hegel/` | `32015a02bfe4002c8d6cfc9191507a16be796361c08942213723700a38567dde` | `GATHER_VERIFIED` |
| `https://plato.stanford.edu/entries/kant/` | `dc9449021a3fa6e861f897e8906e58e0ab66b630acaf53eb2bee491401efcaf1` | `GATHER_VERIFIED` |
| `https://plato.stanford.edu/entries/logic-classical/` | `c86fa0e2cc0179aa36375c0b19c83b17e20211ad0265c27ee211e7ed760b1003` | `GATHER_VERIFIED` |
| `https://plato.stanford.edu/entries/logical-empiricism/` | `6de18ea3fc240aaf18f97fd5c55760441637492e0fc000f942f2444032fba3c9` | `GATHER_VERIFIED` |
| `https://plato.stanford.edu/entries/pragmatism/` | `03c203c3c29f082b7707dfd43df396d45165f6580c4e7a240f25afb46329eeb9` | `GATHER_VERIFIED` |
| `https://plato.stanford.edu/entries/rorty/` | `12246ceb76e025da9db5bdaa0e29bfed185e73aec94e5080476b7f1b59fc2fae` | `GATHER_VERIFIED` |
| `https://plato.stanford.edu/entries/sellars/` | `7aae2f1864f33e8784e08809c88ce4fffbbcb0b3b6c170e83cdf0959447d8fab` | `GATHER_VERIFIED` |
| `https://plato.stanford.edu/entries/wittgenstein/` | `54cf8480c1b87db5a4afca673d4b3496ba1afc276304caa02f1c6b32f4e8de5b` | `GATHER_VERIFIED` |
| `https://sites.pitt.edu/~rbrandom/Texts%20Mark%201%20p.html` | `bc801e10d78960b928caec6973ce5361a456f6b4a55f18112b6f2ae95fc2b3a1` | `GATHER_VERIFIED` |

## Atlas Nodes

| Node | Dominant terms |
| --- | --- |
| `classical_logic` | `logic`, `language`, `reason`, `semantics`, `inference`, `meaning` |
| `frege` | `Frege`, `logic`, `concept`, `language`, `Kant`, `inference` |
| `wittgenstein` | `Wittgenstein`, `logic`, `language`, `meaning`, `concept`, `representation` |
| `kant` | `Kant`, `reason`, `experience`, `representation`, `concept`, `logic` |
| `hegel` | `Hegel`, `logic`, `concept`, `Kant`, `reason`, `analytic` |
| `logical_empiricism` | `logic`, `language`, `concept`, `empiricism`, `analytic`, `meaning` |
| `pragmatism` | `pragmatism`, `experience`, `concept`, `logic`, `reason`, `norm` |
| `sellars` | `Sellars`, `concept`, `language`, `logic`, `norm`, `reason` |
| `rorty` | `Rorty`, `pragmatism`, `analytic`, `concept`, `logic`, `representation` |
| `brandom` | `Hegel`, `concept`, `norm`, `reason`, `logic`, `pragmatism` |

## Atlas Edges

All edges are `HYPOTHESIS_SOURCE_BACKED` and require at least two source
references. They are not treated as proven causal influence claims.

| From | To | Relation |
| --- | --- | --- |
| `classical_logic` | `frege` | formal logic and semantics prerequisite |
| `frege` | `wittgenstein` | logic-language analytic tradition |
| `kant` | `hegel` | post-Kantian idealism line |
| `hegel` | `brandom` | Hegelian recognitive/normative source lead |
| `classical_logic` | `logical_empiricism` | logic-centered analytic context |
| `logical_empiricism` | `sellars` | empiricism as contrast and inheritance |
| `kant` | `sellars` | Kantian categories and experience source lead |
| `pragmatism` | `rorty` | pragmatist anti-foundational context |
| `sellars` | `rorty` | Sellarsian analytic-pragmatist bridge |
| `sellars` | `brandom` | norms, reasons, and scorekeeping dependency |
| `rorty` | `brandom` | pragmatist conversation source lead |
| `pragmatism` | `brandom` | pragmatist inferentialist source lead |
| `frege` | `brandom` | inferential semantics source lead |

## Learning Modules

| Module | Verifier |
| --- | --- |
| `source_trace` | every concept edge names source refs |
| `contrast_class` | learner names inherited and rejected commitments |
| `prerequisite_path` | all path nodes exist in atlas |
| `inferential_rewrite` | answer contains claim, rule, consequence, and objection |
| `overclaim_audit` | unsupported causality and completeness claims are rejected |

## Product Hypotheses

| Tool | Status | Wedge |
| --- | --- | --- |
| `Tradition Derivation Atlas` | `HYPOTHESIS` | Source-backed intellectual dependency maps with explicit overclaim gates. |
| `Concept Prerequisite Tutor` | `HYPOTHESIS` | Turns dense theory into prerequisite paths and checkable exercises. |
| `Citation-to-Exercise Studio` | `HYPOTHESIS` | Converts citation clusters into learner tasks, objections, and repair receipts. |
| `Research Lineage Packet` | `HYPOTHESIS` | Packages tradition edges with provenance, confidence, and falsifiers. |

## Negative Controls

| Fixture | Status | Failure reason |
| --- | --- | --- |
| `complete_genealogy_rejected` | `REJECTED` | `sampled_sources_only,requires_bibliographic_exhaustiveness` |
| `causal_influence_from_edge_rejected` | `REJECTED` | `edge_is_prerequisite_hypothesis,requires_primary_historical_evidence` |
| `learning_efficacy_rejected` | `REJECTED` | `no_user_study,no_outcome_measure` |
| `sourceless_edge_rejected` | `REJECTED` | `missing_source_refs,no_receipt` |
| `raw_article_export_rejected` | `REJECTED` | `copyright_boundary,receipt_digest_only` |
| `humanities_to_natural_law_rejected` | `REJECTED` | `not_a_physics_law,requires_independent_reproduction` |

## Gather

| Document | sha256 | seal |
| --- | --- | --- |
| `packets/141-tradition-derivation-atlas.md` | `90ce43619ccd00c2f8529fb20661f4a68a2eaf33aaea5d3d46c7a83e4199d339` | `4b57a921c415a0965b34b78d3a6fa14ab8ada60a8e0847e94181237ca6ea0e5c` |
| `briefs/141-tradition-derivation-atlas-brief.md` | `8516fe0dd6b76bc5f6faf62d7747659467c4d7b42a9585c4e6ff600d2ae694a5` | `dda3d771a0dc3924bb3d97df1740052ce64bea05a4962ad873e639381989d72d` |

## Crucible

| Measurement | Value |
| --- | --- |
| Thesis id | `7cec7c065269396b` |
| Thesis seal | `7cec7c065269396b3f528ea2edaa1d2bfc6930d8553d25efced6b02292c579b1` |
| Claims | `12` |
| MATCH | `12` |
| DRIFT | `0` |
| UNVERIFIABLE | `0` |
| Verdict seal | `a73aaa5f552415b8620f2ecc792762833892387f753e46333801026d942bff04` |
| Measurement seal | `8cbc0dd7d5e7837191ab68ced3825cbefc4b86854d80cf2f79c5d2df97fb5d10` |
| Assessment seal | `ce16a074c6795fa3223cdb8213c53bbfb9c9713e206105e04f40eaaeb0bfb85c` |

Registry after pass 0131:

- theses: `123`;
- claims: `1117`;
- verdicts: `1117 MATCH`, `0 DRIFT`, `0 UNVERIFIABLE`;
- invalid latest assessments: `0`.

## File Hashes

| File | sha256 |
| --- | --- |
| `schemas/tradition-derivation-atlas-pass-0131.json` | `ea8cceda1433286f97914368ac0bc180e3b85e9b424ff7f026ae3110f54930e0` |
| `schemas/pass-0131-tradition-derivation-atlas-validator-result.json` | `d23d7c7826a6ac2b880c4f5e728a30a11f7fddcfd0daaa970623d395a9a907d8` |
| `schemas/tool-receipts-pass-0131.json` | `720260adc1a84acb62a845ec7311783304ba725b41b2579b4ee5e2315af83268` |
| `packets/141-tradition-derivation-atlas.md` | `90ce43619ccd00c2f8529fb20661f4a68a2eaf33aaea5d3d46c7a83e4199d339` |
| `briefs/141-tradition-derivation-atlas-brief.md` | `8516fe0dd6b76bc5f6faf62d7747659467c4d7b42a9585c4e6ff600d2ae694a5` |
| `adversarial/pass-0131-tradition-derivation-atlas-steelman.md` | `ff9de35f7b80b6e622fee279dd231e96977017a2224197831fa0d5030f068d68` |
| `crucible/pass-0131-thesis.json` | `704efd0f8aa4f0aa8e7fdc5d02515b48980481945966a009bb70231510031aa8` |
| `crucible/pass-0131-measurements.json` | `d05adc62f276ac9ef844faa5bb0722ec043a437390e48e215f9808851b2fe63c` |
| `crucible/pass-0131-report.md` | `7096f4a66b8529d3cad4b433096fa002c4ea362ad72ca0e9c290794e60733c52` |
| `crucible/pass-0131-run.json` | `f35fd0cfac6380d97295961418ce4cd79e5f3401c187c45bf46dda2c96fa6b75` |
| `tools/compose_tradition_derivation_atlas.py` | `653eddd2d04e05c252d356ca05570ea7ea071f52ca2da24b46e66701d4a27153` |
| `tools/test_tradition_derivation_atlas.py` | `1ff12433e3fd50497294d0abb76c2219c78974f9aa71750e596c96b800ae49a1` |
| `tools/validate_pass_0131_tradition_derivation_atlas.py` | `85e8ca959aaccfe446c3c515553c0045f440a3951c665301b244284bb5234854` |
| `tools/probe_tradition_derivation_atlas.py` | `e240c046403758c24d1c722312497d95882ecb93d56762321528dd2e58f9756c` |

## Verification Commands

```powershell
python -m py_compile docs\research\dogfood\tools\compose_tradition_derivation_atlas.py docs\research\dogfood\tools\test_tradition_derivation_atlas.py docs\research\dogfood\tools\validate_pass_0131_tradition_derivation_atlas.py docs\research\dogfood\tools\probe_tradition_derivation_atlas.py
python docs\research\dogfood\tools\test_tradition_derivation_atlas.py
python docs\research\dogfood\tools\probe_tradition_derivation_atlas.py
python docs\research\dogfood\tools\validate_pass_0131_tradition_derivation_atlas.py
gather corpus verify docs\research\dogfood\gather\pass-0131-tradition-derivation-atlas --json
gather docs docs\research\dogfood\packets\141-tradition-derivation-atlas.md --json
gather docs docs\research\dogfood\briefs\141-tradition-derivation-atlas-brief.md --json
crucible run docs\research\dogfood\crucible\pass-0131-thesis.json --measurements docs\research\dogfood\crucible\pass-0131-measurements.json --registry docs\research\dogfood\crucible\registry --report docs\research\dogfood\crucible\pass-0131-report.md --out docs\research\dogfood\crucible\pass-0131-run.json --json
crucible registry stats docs\research\dogfood\crucible\registry --json
```

## Next Pass

The next pass should leave the humanities atlas and return to computational
problem solving: build a `ProofPatternTransferReceipt` that transfers the same
source-trace, prerequisite, contrast, and overclaim-audit pattern into one
bounded mathematics or physics identity, with at least one executable positive
fixture and one explicit counterexample fixture.
