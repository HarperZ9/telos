/-
Copyright (c) 2026 Prob4b formalization. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Prob4b formalization
-/
import Prob4b.Defs

/-!
# The frozen theorems for the Problem 4(b) counterexample

This file is **frozen** after the SETUP stage. Each statement is the minimal
faithful rendering of Problem 4(b) ("Is every finite-conductor ring
quasi-coherent?") and `SKETCH.md`.

The headline `problem4b_false` refutes Problem 4(b): there is a commutative ring
that is finite-conductor (`FiniteConductor`) but not quasi-coherent
(`QuasiCoherent`), with both predicates the literal textbook definitions
(`Defs.lean`). The finite engine — the module `M = B⁴/Bv` preserves all
annihilators (`M_annihilator`) and pairwise principal intersections
(`M_pairwise_intersection`) yet acquires a nonzero triple-intersection defect
`u` (`M_triple_defect`) absent in `B` (`B_triple_zero`) — is the mathematical
heart; the idealization (`triple_defect_survives`) and amplification
(`R_finite_conductor`, `R_not_quasi_coherent`) lift it to the ring `R`. The
companion `quasiCoherent_imp_finiteConductor` supplies the easy direction, so
that "the two classes are distinct" means *finite-conductor is strictly weaker*.
-/

namespace Prob4b

/-- **SKETCH Step 3 (in `B`).** The triple principal intersection
`aB ∩ bB ∩ (a+b)B` vanishes in the base ring `B`. -/
theorem B_triple_zero :
    Ideal.span {a} ⊓ Ideal.span {b} ⊓ Ideal.span {a + b} = (⊥ : Ideal B) := sorry

/-- **SKETCH Step 3 (in `M`).** The element `u = [(0, ab+b², 0, bc+bd)]` is a
*nonzero* member of all three submodules `aM`, `bM`, `(a+b)M`, so the triple
intersection `aM ∩ bM ∩ (a+b)M` does not vanish — the defect absent in `B`. -/
theorem M_triple_defect :
    u ≠ 0 ∧ u ∈ smulSub a ∧ u ∈ smulSub b ∧ u ∈ smulSub (a + b) := sorry

/-- **SKETCH Step 2 (annihilators).** `M` preserves annihilators: for every
`x : B`, `(0 :_M x) = (0 :_B x) · M`. -/
theorem M_annihilator :
    ∀ x : B, annihM x = (annih x) • (⊤ : Submodule B M) := sorry

/-- **SKETCH Step 2 (pairwise intersections).** `M` preserves every pairwise
principal intersection: for all `x y : B`, `xM ∩ yM = (xB ∩ yB) · M`. -/
theorem M_pairwise_intersection :
    ∀ x y : B, smulSub x ⊓ smulSub y
      = (Ideal.span {x} ⊓ Ideal.span {y}) • (⊤ : Submodule B M) := sorry

/-- **SKETCH Step 4.** The triple-intersection defect survives the idealization
`C = B ⋉ M`: `aC ∩ bC ∩ (a+b)C` strictly exceeds the image of the (vanishing)
triple intersection in `B`. -/
theorem triple_defect_survives :
    Ideal.span {aC} ⊓ Ideal.span {bC} ⊓ Ideal.span {aC + bC}
      ≠ (Ideal.span {a} ⊓ Ideal.span {b} ⊓ Ideal.span {a + b}).map inlB := sorry

/-- **SKETCH Step 5 (positive half).** The amplified ring `R = Δ(B) + C^(ℕ)` is
finite-conductor. -/
theorem R_finite_conductor : FiniteConductor R := sorry

/-- **SKETCH Step 5 (negative half).** The amplified ring `R` is *not*
quasi-coherent: the triple intersection `aR ∩ bR ∩ (a+b)R` is not finitely
generated. -/
theorem R_not_quasi_coherent : ¬ QuasiCoherent R := sorry

/-- **SKETCH Step 5 (witnesses).** `R` is finite-conductor but not
quasi-coherent. -/
theorem prob4b_counterexample : FiniteConductor R ∧ ¬ QuasiCoherent R := sorry

/-- **Headline — refutation of Problem 4(b).** There exists a commutative ring
that is finite-conductor but not quasi-coherent; hence finite-conductor does not
imply quasi-coherent. -/
theorem problem4b_false :
    ∃ (S : Type) (_ : CommRing S), FiniteConductor S ∧ ¬ QuasiCoherent S := sorry

/-- **The easy direction (for airtight "distinct").** Every quasi-coherent ring
is finite-conductor: the pairwise principal-intersection condition is the `n = 2`
instance of the arbitrary-finite one, and the annihilator condition is shared.
Together with `problem4b_false` this certifies that the two classes are
genuinely distinct, with finite-conductor *strictly weaker* than quasi-coherent
(not merely incomparable). -/
theorem quasiCoherent_imp_finiteConductor {S : Type*} [CommRing S]
    (h : QuasiCoherent S) : FiniteConductor S := sorry

end Prob4b
