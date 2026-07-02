# Pass 0040 Steelman: Archived Blob Statement Replay

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

## Thesis Under Pressure

Pass 0040 claims theorem statement-signature checks can replay from a local
content-addressed archive after remote capture.

## Strongest Objections

1. Capture still depends on GitHub availability.

Correct. The archive removes remote dependence after capture, but the capture
step still needs source availability or a mirror.

2. The archive stores source text, not compiled proof evidence.

Correct. This is a source-provenance layer. It is not Lean kernel replay.

3. File names by SHA-256 are not a complete supply-chain proof.

Correct. They make byte identity portable. A stronger layer should add mirror
attestations, signatures, and toolchain receipts.

4. The pass inherits pass 0039 signature extraction.

Correct. Pass 0040 tests archive portability, not new theorem semantics.

## Verdict

Useful for portable proof packets and offline review. Still bounded to
source-signature replay, not semantic proof verification.
