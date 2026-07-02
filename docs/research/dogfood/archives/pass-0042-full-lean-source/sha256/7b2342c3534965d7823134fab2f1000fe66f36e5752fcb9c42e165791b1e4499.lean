/-
Copyright (c) 2026 Prob4b formalization. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Prob4b formalization
-/
import Prob4b.Theorems
import Prob4b.Proofs.EasyDirection.Basic
import Prob4b.Proofs.Module.Basic
import Prob4b.Proofs.Triple.Basic
import Prob4b.Proofs.Idealization.Basic
import Prob4b.Proofs.Amplify.Basic

/-!
# Discharge: each frozen theorem is proven by its `Proofs/` counterpart

The frozen `Theorems.lean` holds the immutable *statements* (as `sorry`). The
real proofs live in `Proofs/` as `*_proof` declarations. Each
`example : @Frozen = @Proof := rfl` below compiles **iff** the proven version has
*exactly* the frozen proposition: by proof irrelevance the `rfl` typechecks when
the two share a type, and is a type error otherwise — a machine-checked guarantee
that no statement drifted and nothing was weakened.
-/

namespace Prob4b

-- Stage C (the decidable engine + milestone):
example : @B_triple_zero = @B_triple_zero_proof := rfl
example : @M_triple_defect = @M_triple_defect_proof := rfl

-- Stage B (pairwise preservation):
example : @M_annihilator = @M_annihilator_proof := rfl
example : @M_pairwise_intersection = @M_pairwise_intersection_proof := rfl

-- Stage D (the idealization keeps the defect):
example : @triple_defect_survives = @triple_defect_survives_proof := rfl

-- Stage E (the two halves over the amplified ring R):
example : @R_finite_conductor = @R_finite_conductor_proof := rfl
example : @R_not_quasi_coherent = @R_not_quasi_coherent_proof := rfl

-- Stage E (the witnesses + headline):
example : @prob4b_counterexample = @prob4b_counterexample_proof := rfl
example : @problem4b_false = @problem4b_false_proof := rfl

-- The easy direction:
example : @quasiCoherent_imp_finiteConductor = @quasiCoherent_imp_finiteConductor_proof := rfl

end Prob4b
