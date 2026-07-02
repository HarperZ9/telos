# Pass 0034 Steelman: Lean Replay Verification

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

## Thesis Under Pressure

Pass 0034 claims the local `pipeline-math` Problem 4(b) verifier completed with
exit code 0 after Mathlib cache hydration. It claims a bounded Lean replay
result, not a universal mathematical or market conclusion.

## Strongest Objections

1. The replay uses accepted axioms.

Correct. The pass records `[propext, Classical.choice, Quot.sound]` for all ten
checked theorems. The result must not be sold as axiom-free.

2. The verifier allows `sorry` in `Theorems.lean`.

Correct. The script defines `Theorems.lean` as frozen statement stubs. The
statement gates are what bind those frozen statements to proofs. The packet
should keep this distinction visible.

3. Cache hydration could hide dependency drift.

Partly correct. Cache hydration is still bound to the project and Lean
toolchain, but the next pass should record cache provenance more deeply and
hash representative cache artifacts.

4. A successful project verifier does not prove every public `pipeline-math`
claim.

Correct. It verifies the local Problem 4(b) artifact and its ten named theorem
checks. Public marketing claims, other problems, and broader "LLMs solved open
problems" claims remain separate evidence rows.

5. The result depends on a temp environment.

Correct. That is intentional for non-mutating dogfood. Production replay needs
a stable isolated runtime with cleanup policy and reproducible cache roots.

6. The transcript is summarized, not fully embedded.

Correct. The next pass should capture transcript digests, not huge terminal
logs, and bind them to each theorem-specific packet.

7. The statement gates compile, but that is still inside the project's verifier
design.

Correct. A stronger independent review should inspect `Discharge.lean`,
`Solution.lean`, and the frozen theorem stubs to confirm the intended gate
semantics.

8. The build took 1184 seconds even with cache hydration.

Correct. Demo readiness needs cache prewarming, better progress receipts, and
possibly smaller theorem-specific runs for interactive use.

9. The pass does not identify whether Problem 4(b) is a historically meaningful
open problem.

Correct. That is a separate market/research claim requiring literature review
and external expert comparison.

10. The proof packet is still too manual.

Correct. The megatool needs to automate source binding, cache hydration,
runner setup, transcript hashing, axiom extraction, statement-gate checks, and
Crucible scoring.

## Fatal Tests For The Next Pass

The next pass should fail if it:

- omits per-theorem command digests;
- hides the axiom set;
- treats project-local verifier success as external theorem novelty;
- skips independent inspection of statement-gate semantics;
- fails to separate public claims from verified Lean artifacts;
- leaves temp runtime processes running;
- mutates user-level toolchain state without a receipt.

## Product Implication

Pass 0034 is the clearest proof-packet demo so far. The next product move is to
make this a reusable "formal replay proof packet" flow that works for Lean,
BuildLang/buildc, scientific compute kernels, rendering/color verification, and
AI benchmark claims.

## Verdict

Strong replay evidence, bounded claim. Promote the receipt pattern, not an
unsupported world-scale conclusion.
