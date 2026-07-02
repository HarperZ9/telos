# Fourth-Wave Visibility Content Queue

Date: 2026-07-02

Use these after the third-wave closed-loop posts. This queue is about fail-closed behavior and measurement-gate boundaries.

## Post 26: Measurement Gate

Short post:

> Telos now has a concrete Crucible measurement-gate demo: five supported measurement rows go in, Crucible returns `MATCH` and `allow`. Same packet with a wrong histogram criterion returns `UNVERIFIABLE` and `block`.

Evidence:

- `docs/outreach/FOURTH-WAVE-MEASUREMENT-GATE-DEMO-2026-07-02.md`
- `docs/outreach/receipts/fourth-wave-measurement-gate-result.json`
- `docs/outreach/receipts/fourth-wave-measurement-gate-negative-result.json`

## Post 27: Gate Boundary

Short post:

> The honest boundary matters: Telos has a 10-layer measurement bus, while current Crucible `measurement-gate` validates five layer types. That is a good public line: show what gates now, then expand the gate rather than pretending coverage is broader.

Evidence:

- `node demo\measurement-layers.mjs --summary`
- `crucible measurement-gate docs\outreach\receipts\fourth-wave-measurement-gate-packet.json --criteria docs\outreach\receipts\fourth-wave-measurement-gate-criteria.json --json`

## Post 28: Negative Prooflesson

Short post:

> Learn refuses forged proof-packet verdicts. A packet claiming `VERIFIED_SUPREME` exits 1 and writes no prooflesson receipt. That is the shape we want: lessons derive from bounded proof packets, not arbitrary confidence words.

Evidence:

- `docs/outreach/receipts/fourth-wave-forged-proof-packet.json`
- `docs/outreach/receipts/fourth-wave-negative-prooflesson-result.json`
- `tests\tutor-prooflesson.test.mjs`

## Post 29: Fail Closed

Short post:

> The point of proof packets is not a prettier success story. It is a system that can say `MATCH`, `DRIFT`, or `UNVERIFIABLE`, then block or require review when the evidence does not satisfy the criteria.

Evidence:

- `docs/outreach/receipts/fourth-wave-measurement-gate-negative-result.json`
- `docs/outreach/receipts/second-wave-tooling-report-2026-07-02.md`
- `docs/outreach/receipts/third-wave-tooling-report-2026-07-02.md`

## Operating Rule

When posting the fourth-wave results, always pair the positive result with the negative fixture. The product claim is fail-closed evidence, not just a green check.
