# Pass 0038 Steelman: Blob Statement Replay

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

## Thesis Under Pressure

Pass 0038 claims statement-signature checks can replay from Git object bytes
rather than worktree files.

## Strongest Objections

1. It still requires a local Git object database.

Correct. This pass removes dependence on mutable worktree files, not on local
Git availability. A later pass should fetch or archive blob bytes by commit.

2. Git object bytes are still source text, not Lean elaboration.

Correct. The pass checks source signatures and discharge gate shape. It does not
replace compiled Lean replay.

3. The replay inherits pass 0037 normalization.

Correct. The packet binds pass 0038 canonical signatures back to pass 0037 so
normalization drift is visible.

4. It does not inspect proof bodies.

Correct. Proof body and kernel-term inspection are separate future layers.

## Verdict

Useful hardening for proof-packet portability. Still bounded to source-signature
replay, not semantic proof verification.
