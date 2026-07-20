# Hyphal Context Benchmark for Receipt Routing

Author: Zain Dana Harper
Status: working paper draft, not archive-submitted
Current evidence label: `HYPHAL_CONTEXT_FIXTURE_MATCH` for one deterministic fixture only
Updated: 2026-07-18 (reproducibility correction; original measurement preserved)

## Abstract

This working paper records the first benchmark pass for the Project Telos
hyphal context protocol. The previous biology/network-intelligence packet
proposed a receipt-first routing hypothesis: move low-dimensional gradient
signals through the tool graph, then retrieve high-dimensional evidence only
when needed. This paper turns that hypothesis into a deterministic fixture over
the twenty-first-wave biology corpus.

The fixture compares a full-context route against a hyphal-context route. The
full route estimates the cost of sending all ten source bodies plus the source
gate and architecture seed note. The hyphal route sends ten gradient envelopes
and rehydrates six evidence cards by receipt. In this fixture, both routes
recover the same six required evidence classes and the same three guardrails,
while the hyphal route has a lower estimated prompt footprint.

This is a benchmark fixture, not a general law. It does not measure model
answer quality, does not prove the route wins on all tasks, and does not replace
a BuildLang/buildc runtime receipt.

## Evidence Ledger

| Item | Verdict | Evidence |
| --- | --- | --- |
| Benchmark CLI | `MATCH` | `demo/hyphal-context-benchmark.mjs`, canonical-text SHA-256 `e9204b4692fc658077ab7c5ff64251308476438c65c40ed16ddfc75ae797a049` |
| Benchmark test | `MATCH` | `demo/hyphal-context-benchmark.test.mjs`, canonical-text SHA-256 `bdbdad49a35435d9ae8941c5df9dfc9c5fd3871175de5d7cb7127f609650d31e` |
| Benchmark receipt | `HYPHAL_CONTEXT_FIXTURE_MATCH` | `hyphal-context-benchmark-2026-07-02.json`, canonical-text SHA-256 `9df86246b406cd4c97b1d2952f9eeae6ff8cf7319bbea4514537ac7261953d03` |
| Reproducibility correction | `MATCH` | `docs/outreach/receipts/twenty-second-wave/hyphal-context-benchmark-correction-2026-07-18.json` |
| Source gate | `BIOLOGY_NETWORK_INTELLIGENCE_MATCH` | `biology-network-intelligence-source-gate-2026-07-02.json` |
| Historical Crucible bounded thesis | `MATCH` | `twenty-second-wave-hyphal-context-run-2026-07-02.json`, assessment seal `ccfb0ee4c6033b28d7d13fe4d9d73da41263606eead2c0fbb9ef6191a4ee282b` |
| Historical Learn prooflesson | `VERIFIED` | `twenty-second-wave-hyphal-context-benchmark.prooflesson.json`, witnessed hash `50d09a113d50471cc06b5a427fd9e32b632dc8509cee5dd07f1402a397368c90` |
| Model answer quality | `NOT_MEASURED` | No model answer run is part of this fixture |
| General route superiority | `UNVERIFIABLE` | One fixture cannot prove universal route superiority |
| BuildLang/buildc receipt | `NOT_REPLAYED` | No native buildc benchmark relation receipt yet |

## Fixture Design

The task requires six evidence classes:

- `fungal_signal`,
- `plant_signal`,
- `network_evidence`,
- `overclaim_boundary`,
- `source_availability`,
- `architecture_seed`.

The guardrails are:

- no biological nervous-system equivalence claim,
- no universal intentional common-mycorrhizal-network messaging claim,
- no claim that the hyphal context protocol is already benchmarked beyond this
  fixture.

The full-context route is intentionally expensive: it estimates prompt tokens
from LF-normalized source text, plus the source gate and seed note.

The hyphal route is intentionally receipt-first: it sends small gradient
envelopes for all ten source rows, then rehydrates six evidence cards carrying
refs, hashes, coverage, and retrieval reasons.

## Measured Result

| Measurement | Full context | Hyphal context |
| --- | ---: | ---: |
| Estimated prompt tokens | 121,805 | 1,338 |
| Required evidence classes recovered | 6 | 6 |
| Guardrails blocked | 3 | 3 |

The fixture reports:

```text
token_savings = 120467
token_savings_ratio = 0.989
evidence_recall_delta = 0
guardrail_delta = 0
result = HYPHAL_CONTEXT_FIXTURE_MATCH
```

## Reproducibility correction (2026-07-18)

The original July 2 result was generated from raw working-tree byte sizes and a
raw-byte architecture-seed hash. The frozen artifact records the historical
123,413 full-context token estimate, 122075 saved-token estimate, and 0.9892
savings ratio. Git shows no source-content change between the benchmark and
correction commits. Clean LF and clean `core.autocrlf=true` materializations
produce different results from each other and from the frozen receipt, so the
exact original mixed-EOL working-tree state is unknown. The verified failure
mechanism is checkout-dependent raw-byte accounting, not a later source edit.

The active replay normalizes CRLF and bare CR to LF, verifies corpus-object
hashes, and estimates tokens from canonical text. The original result and
digests remain recoverable through Git and are recorded in
`docs/outreach/receipts/twenty-second-wave/hyphal-context-benchmark-correction-2026-07-18.json`.
The July 2 Crucible and Learn receipts were not rewritten or resealed. They
remain historical evidence for the original bounded claim; the active replay
is now enforced by the CI benchmark test rather than a new Crucible or Learn
assessment.

The important result is not the absolute token estimate. The important result is
the measurement shape: evidence-class recovery, guardrail recovery, and route
cost are separate fields, so a later benchmark can fail honestly.

## Tooling Thesis

This pass uses the Telos flagships as a research loop:

1. Gather owns the source corpus and source-body hashes.
2. Index-style context envelopes define the lossless-by-reference contract.
3. Forum's routing model motivates gradient envelopes and evidence pressure.
4. Crucible receives the benchmark thesis and measurements.
5. Learn converts the benchmark boundary into a prooflesson.
6. BuildLang/buildc is the next runtime target for a native relation-invariant
   receipt.

The fixture intentionally does not embed raw source bodies. It measures body
sizes and carries refs, hashes, coverage strings, and retrieval reasons.

The July 2 Crucible run assessed three bounded claims as `MATCH`: the benchmark
CLI emitted the fixture result with equal required evidence-class and guardrail
recovery, the publication copy kept the deterministic-fixture boundary, and
the benchmark receipt avoided raw source-body and raw-context payload fields.
Learn reverified the historical prooflesson receipt from its recorded hash
chain. The reproducibility correction did not rerun either assessment.

## Publication Claim

The publishable claim is:

> Project Telos now has a deterministic hyphal-context benchmark fixture showing
> equal required evidence-class and guardrail recovery with fewer estimated
> prompt tokens for one frozen biology corpus.

The publishable non-claim is:

> Project Telos has not proved that hyphal routing wins generally, has not
> measured model answer quality in this fixture, and has not produced a native
> BuildLang/buildc benchmark receipt.

## Next Experiment

The next benchmark should add a model answer phase:

1. Run both routes through the same synthesis prompt.
2. Ask Crucible to classify output claims against the source receipts.
3. Measure unsupported claims, missed evidence, and required retrieval count.
4. Re-run the relation in BuildLang/buildc with deterministic receipt output.

## Do Not Infer

- Do not infer that this fixture is a general context-routing theorem.
- Do not infer that estimated prompt tokens equal provider billing tokens.
- Do not infer that the hyphal route has measured model answer quality yet.
- Do not infer that this benchmark changes the biology source boundaries.
- Do not infer that this relation already has a native BuildLang/buildc receipt.
