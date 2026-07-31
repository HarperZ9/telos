# Twenty-Second Wave: Hyphal Context Benchmark

Date: 2026-07-02
Verdict: `HYPHAL_CONTEXT_FIXTURE_MATCH` for one deterministic fixture only

## What Changed

The biology/network-intelligence hypothesis now has a runnable fixture. The
new benchmark compares two ways to carry the same research task over the
twenty-first-wave biology corpus:

- full-context route: send all ten source bodies plus the source gate and seed
  note;
- hyphal route: send ten gradient envelopes and rehydrate six evidence cards by
  receipt.

The fixture reports the same required evidence classes, the same guardrails,
and a smaller estimated prompt footprint for the hyphal route.

## Receipts

- Benchmark CLI:
  `demo/hyphal-context-benchmark.mjs`
- Benchmark test:
  `demo/hyphal-context-benchmark.test.mjs`
- Benchmark receipt:
  `docs/outreach/receipts/twenty-second-wave/hyphal-context-benchmark-2026-07-02.json`
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
- Crucible report:
  `docs/outreach/receipts/twenty-second-wave-hyphal-context-report-2026-07-02.md`
- Historical Learn prooflesson:
  `docs/outreach/receipts/twenty-second-wave/learn-hyphal-context/tutor/twenty-second-wave-hyphal-context-benchmark.prooflesson.json`

## Measured Fixture Result

| Route | Estimated prompt tokens | Required evidence classes | Guardrails |
| --- | ---: | ---: | ---: |
| Full context | 121,805 | 6 / 6 | 3 / 3 |
| Hyphal context | 1,338 | 6 / 6 | 3 / 3 |

Token savings in this fixture: 120,467 estimated prompt tokens, or 0.989 of
the full-context estimate.

## Reproducibility correction (2026-07-18)

The original July 2 replay used working-tree byte sizes and hashed the
architecture seed as raw working-tree bytes. That made its result depend on the
checkout's exact EOL mixture even though Git shows no source-content change
between the benchmark and correction commits. Its frozen historical values
were 123,413 full-context tokens, 122,075 tokens saved, and a 0.9892 savings
ratio. The original working-tree EOL distribution is unknown: neither a clean
LF materialization nor a clean `core.autocrlf=true` materialization reproduces
those exact values.

The active replay normalizes CRLF and bare CR to LF, verifies each
content-addressed corpus object, and estimates tokens from canonical text. The
historical result remains recoverable in Git and is recorded alongside the
canonical result in
`docs/outreach/receipts/twenty-second-wave/hyphal-context-benchmark-correction-2026-07-18.json`.
The July 2 Crucible and Learn receipts were not regenerated; they remain
immutable evidence for the original bounded claim and retain their original
artifact digests. Current replayability is enforced by the CI benchmark test.

## Public Copy Boundary

Allowed:

- "Project Telos has a deterministic hyphal-context benchmark fixture."
- "The fixture reports equal required evidence-class and guardrail recovery with
  fewer estimated prompt tokens."
- "The benchmark is a next-step measurement target for BuildLang/buildc runtime
  receipts."

Blocked:

- "Hyphal routing wins on all research tasks."
- "The fixture measures model answer quality."
- "The fixture proves biological cognition or universal network-message claims."
- "The fixture replaces full BuildLang/buildc receipts."

## Next Tooling Target

BuildLang/buildc should own the next receipt: the same frozen input corpus, the
same route definitions, deterministic token/cost accounting, and a native
relation invariant:

```text
hyphal.required_class_recall == full.required_class_recall
hyphal.guardrail_recall == full.guardrail_recall
hyphal.estimated_prompt_tokens < full.estimated_prompt_tokens
```

That relation still needs a buildc-native receipt. This wave only creates the
JavaScript fixture and publication packet.

## Tool Results

The historical July 2 Crucible run returned
`MATCH 3 / DRIFT 0 / UNVERIFIABLE 0` for the bounded thesis, and Learn generated
and reverified its prooflesson receipt as `VERIFIED`. The reproducibility
correction did not rerun either system. These results verify the original local
fixture discipline only; they do not promote this fixture into a general
route-selection law.
