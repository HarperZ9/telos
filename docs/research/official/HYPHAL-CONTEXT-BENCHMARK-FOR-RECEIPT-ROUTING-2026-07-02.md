# Hyphal Context Benchmark for Receipt Routing

Official local copy for publication packaging.
Author: Zain Dana Harper
Date: 2026-07-02
Status: working draft, not archive-submitted

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
- Benchmark CLI SHA-256:
  `11b5fcb0c79d5c3436bd7eba0474672a65f8c30f68f38906891203b35ce627a7`
- Benchmark test:
  `demo/hyphal-context-benchmark.test.mjs`
- Benchmark test SHA-256:
  `000f774e85f9c5d1885e0f3e8607f91af8d11a35f5bdbbe67abb62c4571ef1d3`
- Benchmark receipt:
  `docs/outreach/receipts/twenty-second-wave/hyphal-context-benchmark-2026-07-02.json`
- Benchmark receipt SHA-256:
  `7bf59b737ca49ea1230188f708b52e6d79b5730cec648b7949ba77ca48839e22`
- Learn packet:
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
- Learn prooflesson receipt:
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
full_context_tokens = 123413
hyphal_context_tokens = 1338
token_savings_ratio = 0.9892
evidence_recall_delta = 0
guardrail_delta = 0
```

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
