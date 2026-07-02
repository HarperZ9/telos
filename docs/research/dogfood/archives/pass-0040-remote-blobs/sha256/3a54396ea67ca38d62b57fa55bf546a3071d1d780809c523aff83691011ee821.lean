/-
Copyright (c) 2026 Prob4b formalization. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Prob4b formalization
-/
import Prob4b.Proofs.EasyDirection.Basic
import Prob4b.Proofs.Module.Basic
import Prob4b.Proofs.Triple.Basic
import Prob4b.Proofs.Idealization.Basic
import Prob4b.Proofs.Amplify.Basic

/-!
# Solution: the frozen statements, proven

`Theorems.lean` holds the immutable *spec* (each theorem is `:= sorry`). This file
restates each of those statements **verbatim** in the `Prob4b.Solution` namespace
and proves it with the corresponding sorry-free declaration from `Proofs/`. Each
`:= …_proof` typechecks only if the proof has *exactly* the frozen proposition, so
this file is simultaneously the no-drift certificate and the clean, named result:
`#print axioms Prob4b.Solution.problem4b_false` is `[propext, Classical.choice,
Quot.sound]` — no `sorry`, no `sorryAx`, no `native_decide`.
-/

namespace Prob4b.Solution

open Prob4b

/-- **SKETCH Step 3 (in `B`).** `aB ∩ bB ∩ (a+b)B = 0` in the base ring `B`. -/
theorem B_triple_zero :
    Ideal.span {a} ⊓ Ideal.span {b} ⊓ Ideal.span {a + b} = (⊥ : Ideal B) :=
  B_triple_zero_proof

/-- **SKETCH Step 3 (in `M`).** The defect `u` is a nonzero member of all three
submodules `aM`, `bM`, `(a+b)M`. -/
theorem M_triple_defect :
    u ≠ 0 ∧ u ∈ smulSub a ∧ u ∈ smulSub b ∧ u ∈ smulSub (a + b) :=
  M_triple_defect_proof

/-- **SKETCH Step 2 (annihilators).** `M` preserves annihilators. -/
theorem M_annihilator :
    ∀ x : B, annihM x = (annih x) • (⊤ : Submodule B M) :=
  M_annihilator_proof

/-- **SKETCH Step 2 (pairwise intersections).** `M` preserves pairwise principal
intersections. -/
theorem M_pairwise_intersection :
    ∀ x y : B, smulSub x ⊓ smulSub y
      = (Ideal.span {x} ⊓ Ideal.span {y}) • (⊤ : Submodule B M) :=
  M_pairwise_intersection_proof

/-- **SKETCH Step 4.** The triple defect survives the idealization `C = B ⋉ M`. -/
theorem triple_defect_survives :
    Ideal.span {aC} ⊓ Ideal.span {bC} ⊓ Ideal.span {aC + bC}
      ≠ (Ideal.span {a} ⊓ Ideal.span {b} ⊓ Ideal.span {a + b}).map inlB :=
  triple_defect_survives_proof

/-- **SKETCH Step 5 (positive half).** `R = Δ(B) + C^(ℕ)` is finite-conductor. -/
theorem R_finite_conductor : FiniteConductor R := R_finite_conductor_proof

/-- **SKETCH Step 5 (negative half).** `R` is not quasi-coherent. -/
theorem R_not_quasi_coherent : ¬ QuasiCoherent R := R_not_quasi_coherent_proof

/-- **SKETCH Step 5 (witnesses).** `R` is finite-conductor but not quasi-coherent. -/
theorem prob4b_counterexample : FiniteConductor R ∧ ¬ QuasiCoherent R :=
  prob4b_counterexample_proof

/-- **Headline — refutation of Problem 4(b).** There exists a commutative ring
that is finite-conductor but not quasi-coherent. -/
theorem problem4b_false :
    ∃ (S : Type) (_ : CommRing S), FiniteConductor S ∧ ¬ QuasiCoherent S :=
  problem4b_false_proof

/-- **The easy direction.** Every quasi-coherent ring is finite-conductor. -/
theorem quasiCoherent_imp_finiteConductor {S : Type*} [CommRing S]
    (h : QuasiCoherent S) : FiniteConductor S :=
  quasiCoherent_imp_finiteConductor_proof h

end Prob4b.Solution
