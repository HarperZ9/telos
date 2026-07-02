# Twenty-First Wave: Biology Network Intelligence

Date: 2026-07-02
Verdict: `BIOLOGY_NETWORK_INTELLIGENCE_MATCH` for one bounded source packet

## What Changed

The biology/network-intelligence lane now has a fresh Gather corpus and a
source gate for fungal, mycorrhizal, and plant signaling literature. The packet
is useful because it upgrades the mycology seed into a stricter publication
boundary:

- ten stored source-bound items,
- ten distinct bodies,
- all object hashes verified as `MATCH`,
- one verified run digest,
- two publisher DOI routes demoted to `HTTP_403_SOURCE_LEAD_ONLY`,
- and an explicit non-claim boundary for biological overreach.

## Receipts

- Gather config:
  `docs/outreach/receipts/twenty-first-wave/biology-network-intelligence-gather-config-2026-07-02.json`
- Gather corpus:
  `docs/outreach/receipts/twenty-first-wave/biology-network-intelligence-corpus`
- Source gate:
  `docs/outreach/receipts/twenty-first-wave/biology-network-intelligence-source-gate-2026-07-02.json`
- Learn packet:
  `docs/outreach/receipts/twenty-first-wave/biology-network-intelligence.learn-packet.json`
- Crucible thesis:
  `docs/outreach/receipts/twenty-first-wave-biology-thesis-2026-07-02.json`
- Crucible measurements:
  `docs/outreach/receipts/twenty-first-wave-biology-measurements-2026-07-02.json`
- Crucible run:
  `docs/outreach/receipts/twenty-first-wave-biology-run-2026-07-02.json`
- Crucible report:
  `docs/outreach/receipts/twenty-first-wave-biology-report-2026-07-02.md`
- Learn prooflesson:
  `docs/outreach/receipts/twenty-first-wave/learn-biology-network/tutor/twenty-first-wave-biology-network-intelligence.prooflesson.json`

## Source Intake

The retained corpus covers four evidence clusters:

- fungal electrical signaling and spike-like activity,
- plant glutamate, calcium, and bioelectric signaling,
- specific common fungal or mycorrhizal network studies,
- and critique/response material around overinterpreted network narratives.

Science and Wiley publisher DOI routes were not locally accessible through
Gather and are held as `SOURCE_LEAD_ONLY`. The packet uses accessible source
pages and PubMed/PMC/arXiv records instead of pretending full-text coverage.

## Public Copy Boundary

Allowed:

- "Project Telos has a verified biology/network-intelligence source packet."
- "The packet supports a hyphal context protocol hypothesis."
- "The protocol should be benchmarked against full-context routing."
- "Biological systems suggest sparse signal, substrate memory, route
  reinforcement, and receipt-triggered evidence retrieval primitives."

Blocked:

- "This packet establishes biological cognition claims."
- "This packet establishes universal intentional messaging through common
  mycorrhizal networks."
- "The hyphal context protocol is proven."
- "The corpus is exhaustive across biology, medicine, robotics, and AI."

## Tooling Direction

The next experiment is a two-route benchmark:

1. Full prompt route: send all candidate context into a model.
2. Hyphal route: send gradient pulses plus receipt IDs, then retrieve evidence
   only when a downstream step needs it.

Measurements should include token cost, relevant evidence recovered, false
claims emitted, `MATCH` / `DRIFT` / `UNVERIFIABLE` verdicts, resume quality
after context loss, and whether later agents can join each claim to a receipt.

## Tool Results

Crucible returned `MATCH 3 / DRIFT 0 / UNVERIFIABLE 0` for the bounded thesis.
Learn generated and reverified the prooflesson receipt as `VERIFIED`. These
results verify the local packet discipline only; they do not convert the
hyphal context protocol into a benchmarked system.
