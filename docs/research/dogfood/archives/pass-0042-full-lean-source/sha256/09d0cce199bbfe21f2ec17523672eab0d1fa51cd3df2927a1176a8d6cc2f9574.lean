/-
Copyright (c) 2026 Prob4b formalization. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Prob4b formalization
-/
import Prob4b.Proofs.Amplify.FiniteConductor
import Prob4b.Proofs.Amplify.NotQuasiCoherent

/-!
# Stage E (E4 + E5) — assembling the counterexample and the headline

This file closes Stage E by bundling the two halves of the amplification:

* `prob4b_counterexample_proof` (E4): `FiniteConductor R ∧ ¬ QuasiCoherent R`,
  the pair `⟨R_finite_conductor_proof, R_not_quasi_coherent_proof⟩`.

* `problem4b_false_proof` (E5, ★ HEADLINE): the existential refutation of
  Problem 4(b) — there is a commutative ring that is finite-conductor but not
  quasi-coherent, witnessed by `R` (with its inherited `CommRing` instance).

See `BLUEPRINT.md` "Stage E — Amplification" (E4, E5) and `PROGRESS.md`.
-/

namespace Prob4b

/-- **E4 — `prob4b_counterexample` (frozen type).** `R` is finite-conductor but
not quasi-coherent. -/
theorem prob4b_counterexample_proof : FiniteConductor R ∧ ¬ QuasiCoherent R :=
  ⟨R_finite_conductor_proof, R_not_quasi_coherent_proof⟩

/-- **E5 — `problem4b_false` (frozen type, ★ HEADLINE).** Refutation of Problem
4(b): there exists a commutative ring that is finite-conductor but not
quasi-coherent; hence finite-conductor does not imply quasi-coherent. The witness
is the amplified ring `R = Δ(B) + C^(ℕ)`. -/
theorem problem4b_false_proof :
    ∃ (S : Type) (_ : CommRing S), FiniteConductor S ∧ ¬ QuasiCoherent S :=
  ⟨R, inferInstance, prob4b_counterexample_proof⟩

end Prob4b
