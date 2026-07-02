/-
Copyright (c) 2026 Prob4b formalization. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Prob4b formalization
-/
import Prob4b.Proofs.RingModel.Basic

/-!
# Stage C — the triple-intersection defect `u` is a genuine triple member

This file proves the three membership facts (Blueprint Stage C2 / SKETCH Step 3)
that the defect element

`u = [(0, ab+b², 0, bc+bd)] ∈ M = (Fin 4 → B) ⧸ B·v`

lies in each of the three principal submodules `aM`, `bM`, `(a+b)M`:

* `u_mem_a  : u ∈ smulSub a`
* `u_mem_b  : u ∈ smulSub b`
* `u_mem_ab : u ∈ smulSub (a + b)`

The strategy is uniform. Recall `smulSub x = (Ideal.span {x}) • (⊤ : Submodule B M)`,
which contains `x • m` for every `m : M` (lemma `smul_mem_smulSub`). For each
scalar `x ∈ {a, b, a+b}` we exhibit an explicit witness vector `w : Fin 4 → B` and
show `x • (mk w) = u`, i.e. that `x • w` and the representative
`p = ![0, a*b+b^2, 0, b*c+b*d]` of `u` agree modulo `B·v`. The difference is the
explicit multiple `r • v` for an explicit `r : B`, checked coordinatewise using the
two structural facts of `B`: `ad_eq_bc` (`a*d = b*c`) and characteristic `2`.

The explicit witnesses (used by the later C4 assembly of `M_triple_defect`):

| `x`     | `w`              | `r`     |
| ------- | ---------------- | ------- |
| `a`     | `![b, b, d, d]`  | `b`     |
| `b`     | `![a, a, c, c]`  | `b`     |
| `a + b` | `![a, 0, c, 0]`  | `a + b` |

This file does **not** prove `u ≠ 0` (a non-membership in `B·v` needing the
coordinate normal form / `Basis`, built separately).

See `BLUEPRINT.md` "Stage C — the triple intersection defect" (C2) and
`PROGRESS.md`.
-/

namespace Prob4b

open scoped BigOperators

/-- `(2 : B) = 0`: `B` is a `ZMod 2`-algebra, hence of characteristic `2`. -/
private theorem two_eq_zero : (2 : B) = 0 := by
  have h : ((2 : ℕ) : B) = 0 := by
    have h2 : ((2 : ℕ) : ZMod 2) = 0 := by decide
    calc ((2 : ℕ) : B) = (algebraMap (ZMod 2) B) ((2 : ℕ) : ZMod 2) := by rw [map_natCast]
      _ = (algebraMap (ZMod 2) B) 0 := by rw [h2]
      _ = 0 := map_zero _
  exact_mod_cast h

/-- `x • m ∈ smulSub x` for every `m : M`: `smulSub x = (span {x}) • ⊤` contains
the scalar multiple `x • m` since `x ∈ span {x}` and `m ∈ ⊤`. -/
theorem smul_mem_smulSub (x : B) (p : M) : x • p ∈ smulSub x := by
  unfold smulSub
  exact Submodule.smul_mem_smul (Ideal.mem_span_singleton_self x) Submodule.mem_top

/-- The fixed representative `p = (0, ab+b², 0, bc+bd)` of `u`, so that
`u = Submodule.Quotient.mk uRep`. -/
private noncomputable def uRep : Fin 4 → B := ![0, a * b + b ^ 2, 0, b * c + b * d]

/-- `u` is the class of `uRep`. -/
private theorem u_eq_mk : u = Submodule.Quotient.mk uRep := rfl

/-- Membership criterion via an explicit preimage: if `x • w` and `uRep` agree
modulo `B·v` (witnessed by `x • w = uRep + r • v`), then `u ∈ smulSub x`. -/
private theorem u_mem_of_witness (x r : B) (w : Fin 4 → B)
    (hw : x • w = uRep + r • v) : u ∈ smulSub x := by
  have hmk : x • (Submodule.Quotient.mk w : M) = u := by
    rw [u_eq_mk, ← Submodule.Quotient.mk_smul, Submodule.Quotient.eq]
    -- goal: x • w - uRep ∈ Bv
    rw [hw, add_sub_cancel_left]
    -- goal: r • v ∈ Bv
    unfold Bv
    exact Submodule.smul_mem _ r (Submodule.mem_span_singleton_self v)
  rw [← hmk]
  exact smul_mem_smulSub x _

/-- Reduce a `Fin 4 → B` equation `x • ![w0,w1,w2,w3] = uRep + r • v` to its four
scalar coordinate equations. `v = ![a,b,c,d]`, `uRep = ![0, ab+b², 0, bc+bd]`. -/
private theorem witness_coords (x r w0 w1 w2 w3 : B)
    (h0 : x * w0 = 0 + r * a)
    (h1 : x * w1 = (a * b + b ^ 2) + r * b)
    (h2 : x * w2 = 0 + r * c)
    (h3 : x * w3 = (b * c + b * d) + r * d) :
    x • ![w0, w1, w2, w3] = uRep + r • v := by
  funext i
  fin_cases i <;>
    simp only [uRep, v, Pi.smul_apply, smul_eq_mul, Pi.add_apply]
  exacts [h0, h1, h2, h3]

/-- `u ∈ aM`. Witness `w = ![b, b, d, d]`, `r = b`. -/
theorem u_mem_a : u ∈ smulSub a := by
  refine u_mem_of_witness a b ![b, b, d, d] (witness_coords a b _ _ _ _ ?_ ?_ ?_ ?_)
  · ring
  · linear_combination (-b ^ 2 : B) * two_eq_zero
  · linear_combination ad_eq_bc
  · linear_combination ad_eq_bc - (b * d : B) * two_eq_zero

/-- `u ∈ bM`. Witness `w = ![a, a, c, c]`, `r = b`. -/
theorem u_mem_b : u ∈ smulSub b := by
  refine u_mem_of_witness b b ![a, a, c, c] (witness_coords b b _ _ _ _ ?_ ?_ ?_ ?_)
  · ring
  · linear_combination (-b ^ 2 : B) * two_eq_zero
  · ring
  · linear_combination (-(b * d) : B) * two_eq_zero

/-- `u ∈ (a+b)M`. Witness `w = ![a, 0, c, 0]`, `r = a + b`. -/
theorem u_mem_ab : u ∈ smulSub (a + b) := by
  refine u_mem_of_witness (a + b) (a + b) ![a, 0, c, 0]
    (witness_coords (a + b) (a + b) _ _ _ _ ?_ ?_ ?_ ?_)
  · ring
  · linear_combination (-(a * b) - b ^ 2 : B) * two_eq_zero
  · ring
  · linear_combination -ad_eq_bc - (b * c + b * d : B) * two_eq_zero

end Prob4b
