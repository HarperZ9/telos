# Hyphal Context Benchmark for Receipt Routing

Official local copy for publication packaging.
Author: Zain Dana Harper
Date: 2026-07-02
Status: working draft, not archive-submitted
Reproducibility correction: 2026-07-18

## Official Status

`HYPHAL_CONTEXT_FIXTURE_MATCH` applies only to one deterministic fixture over
the twenty-first-wave biology/network-intelligence corpus.

`NOT_MEASURED` applies to model answer quality in this package.

`UNVERIFIABLE` applies to universal route-superiority claims.

`NOT_REPLAYED` applies to BuildLang/buildc runtime receipts for this relation.

## Abstract

Project Telos is building proof-centered research packets that can dogfood their
own context-routing claims. This official local copy records the first
hyphal-context benchmark fixture: a full-context route versus a
gradient-envelope-and-receipt route over a frozen biology source corpus. The
fixture reports equal required evidence-class recovery and equal guardrail
recovery with fewer estimated prompt tokens for the hyphal route.

## Verified Artifacts

- Benchmark CLI:
  `demo/hyphal-context-benchmark.mjs`
- Benchmark CLI canonical-text SHA-256:
  `e9204b4692fc658077ab7c5ff64251308476438c65c40ed16ddfc75ae797a049`
- Benchmark test:
  `demo/hyphal-context-benchmark.test.mjs`
- Benchmark test canonical-text SHA-256:
  `bdbdad49a35435d9ae8941c5df9dfc9c5fd3871175de5d7cb7127f609650d31e`
- Benchmark receipt:
  `docs/outreach/receipts/twenty-second-wave/hyphal-context-benchmark-2026-07-02.json`
- Benchmark receipt canonical-text SHA-256:
  `9df86246b406cd4c97b1d2952f9eeae6ff8cf7319bbea4514537ac7261953d03`
- Reproducibility correction:
  `docs/outreach/receipts/twenty-second-wave/hyphal-context-benchmark-correction-2026-07-18.json`
- Historical Learn packet:
  `docs/outreach/receipts/twenty-second-wave/hyphal-context-benchmark.learn-packet.json`
- Crucible thesis:
  `docs/outreach/receipts/twenty-second-wave-hyphal-context-thesis-2026-07-02.json`
- Crucible measurements:
  `docs/outreach/receipts/twenty-second-wave-hyphal-context-measurements-2026-07-02.json`
- Crucible run:
  `docs/outreach/receipts/twenty-second-wave-hyphal-context-run-2026-07-02.json`
- Crucible run SHA-256:
  `071a2d897945bbef16470d2eb41f59fcc3270d9703f2ef7bf7516764bda91400`
- Crucible report:
  `docs/outreach/receipts/twenty-second-wave-hyphal-context-report-2026-07-02.md`
- Crucible report SHA-256:
  `041e1b0d0e2295372c2f34d86c69628682e069eb92117cea08851d73f697368e`
- Historical Learn prooflesson receipt:
  `docs/outreach/receipts/twenty-second-wave/learn-hyphal-context/tutor/twenty-second-wave-hyphal-context-benchmark.prooflesson.json`
- Learn prooflesson SHA-256:
  `bc7749d420a22e2d0bd87d843be021bb9d64c516af366d56ba5c1c5db7ff6d2d`

## Claim Boundary

The benchmark relation is:

```text
hyphal.required_class_recall == full.required_class_recall
hyphal.guardrail_recall == full.guardrail_recall
hyphal.estimated_prompt_tokens < full.estimated_prompt_tokens
```

Current fixture values:

```text
full_context_tokens = 121805
hyphal_context_tokens = 1338
token_savings = 120467
token_savings_ratio = 0.989
evidence_recall_delta = 0
guardrail_delta = 0
```

## Reproducibility correction (2026-07-18)

The original July 2 artifact measured raw working-tree bytes. Its frozen
artifact records 123413 full-context tokens, 122075 tokens saved, and a 0.9892
savings ratio. Git history shows no source-gate, corpus-object, or
architecture-seed content change between the benchmark packet commit and the
correction merge. Clean LF and clean `core.autocrlf=true` materializations
produce different results from each other and from the frozen receipt, so the
original mixed-EOL working-tree state is unknown. The verified failure mechanism
is checkout-dependent raw-byte accounting, not a later source edit.

The active receipt normalizes CRLF and bare CR to LF, checks every corpus
object against its content-addressed hash, and estimates tokens from canonical
text. The original values and artifact digests remain preserved in
`docs/outreach/receipts/twenty-second-wave/hyphal-context-benchmark-correction-2026-07-18.json`.
The correction does not rewrite or reseal the July 2 Crucible and Learn
receipts. They remain immutable evidence for the original bounded claim;
current replayability is established by the benchmark test in CI, not by a new
Crucible or Learn verdict.

## Publication Checklist

- [x] The benchmark CLI exists.
- [x] The benchmark test exists.
- [x] The benchmark receipt reports `HYPHAL_CONTEXT_FIXTURE_MATCH`.
- [x] Required evidence-class recovery is equal in the fixture.
- [x] Guardrail recovery is equal in the fixture.
- [x] Hyphal estimated prompt tokens are lower in the fixture.
- [x] The receipt avoids raw source-body and raw-context payload fields.
- [x] Crucible has assessed the bounded benchmark claims as `MATCH`.
- [x] Learn has reverified the prooflesson receipt as `VERIFIED`.
- [ ] A model answer-quality phase exists.
- [ ] A native BuildLang/buildc benchmark receipt exists.
- [ ] An archive submission has been made.

## Next Submission Gate

Do not submit this as a general context-routing result. The correct submission
shape is a methods or systems working paper about benchmark discipline for
receipt-first routing. A stronger paper needs at least one model answer-quality
phase and a BuildLang/buildc receipt for the route relation.
