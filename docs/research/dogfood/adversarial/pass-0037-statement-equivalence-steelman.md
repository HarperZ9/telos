# Pass 0037 Steelman: Statement Equivalence

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

## Thesis Under Pressure

Pass 0037 claims that frozen theorem declarations, solution declarations, proof
declaration headers, and discharge equality gates match at the normalized
source-signature level.

## Strongest Objections

1. This is still text normalization, not Lean elaboration.

Correct. It catches obvious drift between declarations but does not replace the
Lean kernel, theorem replay, or an AST/elaboration equivalence checker.

2. Whitespace normalization can hide formatting differences.

Correct. That is intentional for signature comparison, but the packet keeps raw
signature text hashes and spans for stricter review.

3. It only checks theorem declaration signatures, not proof bodies.

Correct. Proof-body review belongs to a later AST or elaboration pass.

4. The discharge gate is checked as source text.

Correct. It must still be compiled by the replay harness to become a theorem
kernel fact. This pass only verifies the gate source has the expected equality
shape.

## Verdict

Useful protection against statement drift. Not a substitute for compiled Lean
replay or semantic proof review.
