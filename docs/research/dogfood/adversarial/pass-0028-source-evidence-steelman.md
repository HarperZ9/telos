# Pass 0028 Source Evidence Binding Steelman

Date: 2026-07-01

## Claim Under Test

Pass 0028 claims a local action receipt can bind pass 0027 redacted replay refs
to a redacted browser-evidence fixture using digest refs while preserving raw
source and raw browser payload boundaries.

## Strongest Objections

1. The browser evidence fixture is not live browsing.

   Correct. The pass uses the Telos browser-evidence fixture shape. It does not
   prove a live browser collector, network recorder, DOM recorder, screenshot
   capture, or authenticated browsing flow.

2. Network and console evidence are not captured.

   Correct. The fixture marks both as `UNVERIFIABLE`. The pass treats that as a
   preserved gap, not a success condition.

3. Digest refs do not prove semantic truth.

   Correct. They bind evidence identity and replayability. They do not prove
   that a source is true, complete, current, or sufficient for a scientific or
   market claim.

4. Redaction status is self-reported by the local fixture.

   Correct. The validator checks local fixture consistency and scanner-token
   absence. It does not prove production DLP, policy enforcement, or external
   auditor review.

5. The market implication is still a hypothesis.

   Correct. The pass supports a product wedge hypothesis: proof packets need
   source evidence binding. It does not prove buyer adoption, willingness to pay,
   or competitive uniqueness.

## What Would Falsify The Pass

- The source replay SHA-256 differs from pass 0027.
- The browser evidence SHA-256 differs from the receipt.
- The action receipt binding omits evidence refs or digests.
- Raw source material is required for replay.
- Raw browser payload material is required for replay.
- Network or console `UNVERIFIABLE` is promoted to `MATCH`.
- Browser evidence redaction status is not `redacted`.
- A model-facing artifact contains the raw source scanner token.

## Product Read

This pass is useful because it forces the proof packet to carry both evidence
and evidence gaps:

```text
source evidence identity
redacted evidence references
action receipt binding
explicit unverifiable capture surfaces
no raw-source dependency
```

That is a practical bridge from agent observability into accountable research
and regulated workflow evidence.

## Non-Promotion Boundary

This pass does not prove live browser collection, production browser capture,
production DLP, external vault integration, theorem proof, scientific discovery,
buyer adoption, or any natural law.

Current promoted natural laws: none.
