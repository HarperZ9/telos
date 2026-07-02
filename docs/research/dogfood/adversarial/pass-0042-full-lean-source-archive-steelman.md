# Pass 0042 Steelman: Full Lean Source Archive

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

## Thesis Under Pressure

Pass 0042 claims the local source/build input set needed before compiled replay
is captured into a content-addressed archive.

## Strongest Objections

1. A source archive is not a successful Lean build.

Correct. The pass is a precondition for compiled replay. It does not run
`lake build` or invoke the Lean kernel.

2. Dependency packages are not archived here.

Correct. The pass archives local project sources and build metadata. Mathlib
and Lake dependencies still need their own dependency-cache proof packet.

3. Archive paths prove byte identity, not theorem truth.

Correct. This is provenance and replay-preparation evidence, not mathematical
semantics.

4. One file has two roles.

Correct. `Prob4b.lean` is both a root import module and part of the build/replay
metadata surface. The archive records 22 role records over 21 unique files.

## Verdict

Useful source-completeness hardening before compiled replay. Still bounded to
source/build archive integrity, not semantic proof verification.
