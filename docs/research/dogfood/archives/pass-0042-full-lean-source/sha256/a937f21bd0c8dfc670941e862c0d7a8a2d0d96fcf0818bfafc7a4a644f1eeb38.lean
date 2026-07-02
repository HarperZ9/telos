/-
Copyright (c) 2026 Prob4b formalization. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Prob4b formalization
-/
import Prob4b.Proofs.Triple.Basic

/-!
# Stage D — the triple defect survives the idealization `C = B ⋉ M`

This file closes Stage D (D2) of the Problem 4(b) project: the frozen theorem
`triple_defect_survives`.

The idealization is `C = TrivSqZeroExt B M`, with `inlB : B →+* C` the diagonal
embedding `x ↦ (x, 0)` (`= TrivSqZeroExt.inlHom B M`) and `aC = inlB a`,
`bC = inlB b`. Multiplication is `(x, m)(y, n) = (xy, xn + ym)`, in particular
`M·M = 0` (square-zero): `inl r * inr m = inr (r • m)`.

**Strategy (BLUEPRINT D2).**

* *RHS = ⊥.* By `B_triple_zero_proof`, the base-ring triple intersection
  `aB ∩ bB ∩ (a+b)B = ⊥`, so its image
  `(Ideal.span {a} ⊓ Ideal.span {b} ⊓ Ideal.span {a+b}).map inlB
   = (⊥ : Ideal B).map inlB = ⊥` by `Ideal.map_bot`.

* *LHS ≠ ⊥.* Lift the module defect `u : M` (nonzero, by `u_ne_zero`) into `C`
  along the right `B`-linear inclusion `inr : M → C` (`= TrivSqZeroExt.inrHom`),
  giving `uC := inr u`. Because `u ∈ aM` (`u_mem_a`), there is `m : M` with
  `a • m = u`, whence `aC * inr m = inl a * inr m = inr (a • m) = inr u = uC`,
  so `uC ∈ Ideal.span {aC}`; symmetrically for `bC` and `aC + bC`. Hence
  `uC ∈ Ideal.span {aC} ⊓ Ideal.span {bC} ⊓ Ideal.span {aC + bC}`. And
  `uC = inr u ≠ inr 0 = 0` since `inr` is injective and `u ≠ 0`.

Since `uC ≠ 0` lies in the LHS but the RHS is `⊥`, the two sides differ.

See `BLUEPRINT.md` "Stage D — Idealization `C = B ⋉ M`" (D2) and `PROGRESS.md`.
-/

namespace Prob4b

open TrivSqZeroExt

/-- The lifted defect `uC = inr u = (0, u) ∈ C`. -/
noncomputable def uC : C := TrivSqZeroExt.inr u

/-- From `u ∈ smulSub x = (span {x}) • ⊤`, extract a single preimage:
`∃ m : M, x • m = u`. The set `{x • m | m : M}` is a submodule containing every
generator of `(span {x}) • ⊤`, so it contains the whole submodule. -/
theorem exists_smul_eq_of_mem_smulSub {x : B} {p : M} (hp : p ∈ smulSub x) :
    ∃ m : M, x • m = p := by
  refine Submodule.smul_induction_on hp ?_ ?_
  · intro r hr n _
    rw [Ideal.mem_span_singleton'] at hr
    obtain ⟨z, rfl⟩ := hr
    exact ⟨z • n, by rw [smul_comm, smul_smul]⟩
  · rintro p q ⟨mp, hmp⟩ ⟨mq, hmq⟩
    exact ⟨mp + mq, by rw [smul_add, hmp, hmq]⟩

/-- `inlB x * inr m = inr (x • m)` in `C` (the structural square-zero product). -/
theorem inlB_mul_inr (x : B) (m : M) :
    inlB x * (TrivSqZeroExt.inr m : C) = TrivSqZeroExt.inr (x • m) := by
  rw [show inlB x = TrivSqZeroExt.inl x from rfl, TrivSqZeroExt.inl_mul_inr]

/-- `uC ∈ Ideal.span {inlB x}` whenever `u ∈ smulSub x`. -/
theorem uC_mem_span_inlB {x : B} (hx : u ∈ smulSub x) :
    uC ∈ Ideal.span {inlB x} := by
  obtain ⟨m, hm⟩ := exists_smul_eq_of_mem_smulSub hx
  rw [Ideal.mem_span_singleton']
  refine ⟨(TrivSqZeroExt.inr m : C), ?_⟩
  rw [mul_comm, inlB_mul_inr, hm, uC]

/-- `aC + bC = inlB (a + b)`. -/
theorem aC_add_bC : aC + bC = inlB (a + b) := by
  rw [aC, bC, map_add]

/-- `uC ≠ 0`: `inr` is injective and `u ≠ 0`. -/
theorem uC_ne_zero : uC ≠ 0 := by
  rw [uC]
  intro h
  rw [show (0 : C) = TrivSqZeroExt.inr (0 : M) from (map_zero (TrivSqZeroExt.inrHom B M)).symm] at h
  exact u_ne_zero (TrivSqZeroExt.inr_injective h)

/-- **D2 — `triple_defect_survives` (frozen type).** The triple-intersection
defect survives the idealization `C = B ⋉ M`: the principal triple intersection
in `C` strictly exceeds the image of the (vanishing) base-ring triple
intersection. The lifted defect `uC = inr u ≠ 0` lies in the left-hand side,
while the right-hand side is `⊥` (`B_triple_zero_proof` + `Ideal.map_bot`). -/
theorem triple_defect_survives_proof :
    Ideal.span {aC} ⊓ Ideal.span {bC} ⊓ Ideal.span {aC + bC}
      ≠ (Ideal.span {a} ⊓ Ideal.span {b} ⊓ Ideal.span {a + b}).map inlB := by
  -- The RHS is `⊥`.
  have hRHS : (Ideal.span {a} ⊓ Ideal.span {b} ⊓ Ideal.span {a + b}).map inlB
      = (⊥ : Ideal C) := by
    rw [B_triple_zero_proof, Ideal.map_bot]
  -- `uC` lies in the LHS.
  have huC : uC ∈ Ideal.span {aC} ⊓ Ideal.span {bC} ⊓ Ideal.span {aC + bC} := by
    refine ⟨⟨?_, ?_⟩, ?_⟩
    · exact uC_mem_span_inlB u_mem_a
    · exact uC_mem_span_inlB u_mem_b
    · rw [aC_add_bC]; exact uC_mem_span_inlB u_mem_ab
  -- If the two sides were equal, `uC` would be in `⊥`, contradicting `uC ≠ 0`.
  intro heq
  rw [heq, hRHS, Submodule.mem_bot] at huC
  exact uC_ne_zero huC

end Prob4b
