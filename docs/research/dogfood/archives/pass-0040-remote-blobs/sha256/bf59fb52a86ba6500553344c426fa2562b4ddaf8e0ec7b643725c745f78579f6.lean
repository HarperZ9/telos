/-
Copyright (c) 2026 Prob4b formalization. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Prob4b formalization
-/
import Prob4b.Proofs.RingModel.Normal
import Prob4b.Proofs.Triple.Membership

/-!
# Stage C (assembly) — `u ≠ 0`, `M_triple_defect`, and `B_triple_zero`

This file closes Stage C of the Problem 4(b) project:

* `u_ne_zero : u ≠ 0` — the defect representative
  `uRep = (0, ab+b², 0, bc+bd)` is **not** in `B·v = span B {v}`. We build a
  `ZMod 2`-linear functional `Ψ : (Fin 4 → B) →ₗ[ZMod 2] ZMod 2`,
  `Ψ f = coordFun 5 (f 0) + coordFun 6 (f 1)` (read the `a²`-coordinate of the
  first entry plus the `ab`-coordinate of the second). It vanishes on every
  `r • v` (because `coeff (a²) (r·a) = coeff (ab) (r·b) = coeff a r`, summing to
  `2·… = 0` in characteristic `2`) yet `Ψ uRep = 1`. Descending `Ψ` through `Bv`
  with `Submodule.liftQ` gives `Ψ̄ : M →ₗ[ZMod 2] ZMod 2` with `Ψ̄ u = 1 ≠ 0`,
  hence `u ≠ 0`.

* `M_triple_defect_proof` — the frozen `M_triple_defect`, assembled as
  `⟨u_ne_zero, u_mem_a, u_mem_b, u_mem_ab⟩` from this file plus
  `Triple/Membership.lean`.

* `B_triple_zero_proof` — the frozen `B_triple_zero`:
  `aB ∩ bB ∩ (a+b)B = ⊥`. An element `x` of the intersection is
  `a·r = b·s = (a+b)·t`; reading the `14` `ZMod 2`-coordinates of these three
  equal degree-`≥1` elements forces every coordinate of `x` to be `0`, hence
  `x = 0` by injectivity of `Bcoord`.

See `BLUEPRINT.md` "Stage C" (C1, C3, C4) and `PROGRESS.md`.
-/

namespace Prob4b

open MvPolynomial

/-! ### `u ≠ 0` via a coordinate functional on `Fin 4 → B` -/

/-- The fixed representative `uRep = (0, ab+b², 0, bc+bd)` of `u`. -/
private noncomputable def uRep' : Fin 4 → B := ![0, a * b + b ^ 2, 0, b * c + b * d]

private theorem u_eq_mk' : u = Submodule.Quotient.mk uRep' := rfl

/-- The `ZMod 2`-linear functional `Ψ f = coordFun 5 (f 0) + coordFun 6 (f 1)`:
reads the `a²`-coordinate of the `0`-th entry and the `ab`-coordinate of the
`1`-st entry of a vector `f : Fin 4 → B`. -/
noncomputable def psiF : (Fin 4 → B) →ₗ[ZMod 2] ZMod 2 :=
  (coordFun 5).comp (LinearMap.proj 0) + (coordFun 6).comp (LinearMap.proj 1)

@[simp] theorem psiF_apply (f : Fin 4 → B) :
    psiF f = coordFun 5 (f 0) + coordFun 6 (f 1) := rfl

/-- `coordFun 5 (mk p * a) = coeff (a) p` (the `a²`-coordinate of `p·a` reads the
`a`-coordinate of `p`). -/
theorem coordFun5_mul_a (p : P4) :
    coordFun 5 (Ideal.Quotient.mk Brel p * a) = coeff (Finsupp.single 0 1) p := by
  have ha : (a : B) = Ideal.Quotient.mk Brel (X 0) := rfl
  rw [ha, ← map_mul, coordFun_apply (by decide)]
  have hbexp : bexp 5 = Finsupp.single 0 1 + Finsupp.single 0 1 := by
    rw [← Finsupp.single_add, bexp]; rfl
  rw [hbexp]
  exact coeff_mul_X (Finsupp.single 0 1) 0 p

/-- `coordFun 6 (mk p * b) = coeff (a) p` (the `ab`-coordinate of `p·b` reads the
`a`-coordinate of `p`). -/
theorem coordFun6_mul_b (p : P4) :
    coordFun 6 (Ideal.Quotient.mk Brel p * b) = coeff (Finsupp.single 0 1) p := by
  have hb : (b : B) = Ideal.Quotient.mk Brel (X 1) := rfl
  rw [hb, ← map_mul, coordFun_apply (by decide)]
  have hbexp : bexp 6 = Finsupp.single 0 1 + Finsupp.single 1 1 := by
    rw [bexp]; simp
  rw [hbexp]
  exact coeff_mul_X (Finsupp.single 0 1) 1 p

/-- `Ψ` vanishes on every multiple `r • v` of `v`: the two coordinate reads both
return the `a`-coordinate of (a lift of) `r`, summing to `2·… = 0` in `ZMod 2`. -/
theorem psiF_smul_v (r : B) : psiF (r • v) = 0 := by
  obtain ⟨p, rfl⟩ := Ideal.Quotient.mk_surjective r
  rw [psiF_apply]
  rw [show (Ideal.Quotient.mk Brel p • v) 0 = Ideal.Quotient.mk Brel p * a from by
        change (Ideal.Quotient.mk Brel p) • v 0 = _; rw [smul_eq_mul]; rfl,
      show (Ideal.Quotient.mk Brel p • v) 1 = Ideal.Quotient.mk Brel p * b from by
        change (Ideal.Quotient.mk Brel p) • v 1 = _; rw [smul_eq_mul]; rfl,
      coordFun5_mul_a, coordFun6_mul_b]
  rw [← two_mul]
  have : (2 : ZMod 2) = 0 := by decide
  rw [this, zero_mul]

/-- `Ψ` vanishes on all of `Bv = span B {v}`. -/
theorem psiF_vanish_Bv : Bv.restrictScalars (ZMod 2) ≤ LinearMap.ker psiF := by
  intro x hx
  rw [Submodule.restrictScalars_mem, Bv, Submodule.mem_span_singleton] at hx
  obtain ⟨c, rfl⟩ := hx
  rw [LinearMap.mem_ker]
  exact psiF_smul_v c

/-- `Ψ uRep = 1`: the `a²`-coordinate of `0` is `0`, the `ab`-coordinate of
`ab + b²` is `1`. -/
theorem psiF_uRep : psiF uRep' = 1 := by
  rw [psiF_apply]
  have e0 : uRep' 0 = 0 := rfl
  have e1 : uRep' 1 = a * b + b ^ 2 := rfl
  rw [e0, e1, map_zero, zero_add]
  -- coordFun 6 (a*b + b^2) = 1
  have hab : (a * b + b ^ 2 : B)
      = Ideal.Quotient.mk Brel (X 0 * X 1 + X 1 ^ 2) := by
    rw [map_add, map_mul, map_pow]; rfl
  rw [hab, coordFun_apply (by decide)]
  have hbexp : bexp 6 = Finsupp.single 0 1 + Finsupp.single 1 1 := by
    rw [bexp]; simp
  rw [hbexp, coeff_add]
  rw [show (X 0 * X 1 : P4) = monomial (Finsupp.single 0 1 + Finsupp.single 1 1) 1 from by
        rw [X, X, monomial_mul, mul_one]]
  rw [coeff_monomial, if_pos rfl]
  rw [show (X 1 ^ 2 : P4) = monomial (Finsupp.single 1 2) 1 from by
        rw [X, monomial_pow]; simp]
  rw [coeff_monomial, if_neg, add_zero]
  intro h
  have := congrArg (· (0 : Fin 4)) h
  simp [Finsupp.add_apply] at this

/-- **C3 — `u ≠ 0`.** The descended functional `Ψ̄ : M →ₗ[ZMod 2] ZMod 2`
satisfies `Ψ̄ u = Ψ uRep = 1 ≠ 0`, so `u ≠ 0`. -/
theorem u_ne_zero : u ≠ 0 := by
  intro hu
  -- Descend Ψ through Bv to a ZMod 2-linear map on M.
  set Ψbar : M →ₗ[ZMod 2] ZMod 2 :=
    (Bv.restrictScalars (ZMod 2)).liftQ psiF psiF_vanish_Bv with hΨbar
  have hval : Ψbar u = 1 := by
    rw [hΨbar, u_eq_mk']
    exact (Submodule.liftQ_apply _ _ _).trans psiF_uRep
  rw [hu, map_zero] at hval
  exact one_ne_zero hval.symm

/-! ### C1 — `B_triple_zero` : `aB ∩ bB ∩ (a+b)B = ⊥` -/

/-- The coordinate functionals `coordFun i` are the dual basis of `B_basis`. -/
theorem coordFun_eq_coord (i : Fin 14) : coordFun i = B_basis.coord i := by
  apply B_basis.ext
  intro j
  rw [B_basis.coord_apply, B_basis.repr_self, Finsupp.single_apply, B_basis_apply,
    coordFun_basisMon]
  by_cases h : i = j <;> simp [h, eq_comm]

/-- **Coordinate-zero criterion.** An element of `B` is `0` iff all `14`
coordinate functionals vanish on it. -/
theorem eq_zero_of_coordFun (x : B) (h : ∀ i, coordFun i x = 0) : x = 0 := by
  rw [← B_basis.forall_coord_eq_zero_iff]
  intro i
  rw [← coordFun_eq_coord]; exact h i

/-- `coordFun i (a * mk p) = coeff (bexp i) (X₀ * p)` for `i ≠ 8`. -/
theorem coordFun_a_mul {i : Fin 14} (hi : i ≠ 8) (p : P4) :
    coordFun i (a * Ideal.Quotient.mk Brel p) = coeff (bexp i) (X 0 * p) := by
  have : (a : B) * Ideal.Quotient.mk Brel p = Ideal.Quotient.mk Brel (X 0 * p) := by
    rw [show (a : B) = Ideal.Quotient.mk Brel (X 0) from rfl, ← map_mul]
  rw [this, coordFun_apply hi]

/-- `coordFun i (b * mk p) = coeff (bexp i) (X₁ * p)` for `i ≠ 8`. -/
theorem coordFun_b_mul {i : Fin 14} (hi : i ≠ 8) (p : P4) :
    coordFun i (b * Ideal.Quotient.mk Brel p) = coeff (bexp i) (X 1 * p) := by
  have : (b : B) * Ideal.Quotient.mk Brel p = Ideal.Quotient.mk Brel (X 1 * p) := by
    rw [show (b : B) = Ideal.Quotient.mk Brel (X 1) from rfl, ← map_mul]
  rw [this, coordFun_apply hi]

/-- `coordFun i ((a+b) * mk p) = coeff (bexp i) ((X₀+X₁) * p)` for `i ≠ 8`. -/
theorem coordFun_ab_mul {i : Fin 14} (hi : i ≠ 8) (p : P4) :
    coordFun i ((a + b) * Ideal.Quotient.mk Brel p)
      = coeff (bexp i) ((X 0 + X 1) * p) := by
  have : (a + b : B) * Ideal.Quotient.mk Brel p
      = Ideal.Quotient.mk Brel ((X 0 + X 1) * p) := by
    rw [show (a : B) = Ideal.Quotient.mk Brel (X 0) from rfl,
        show (b : B) = Ideal.Quotient.mk Brel (X 1) from rfl, ← map_add, ← map_mul]
  rw [this, coordFun_apply hi]

/-- `coordFun 8 ((a+b) * mk p) = phiP ((X₀+X₁) * p)`. -/
theorem coordFun8_ab_mul (p : P4) :
    coordFun 8 ((a + b) * Ideal.Quotient.mk Brel p)
      = phiP ((X 0 + X 1) * p) := by
  have : (a + b : B) * Ideal.Quotient.mk Brel p
      = Ideal.Quotient.mk Brel ((X 0 + X 1) * p) := by
    rw [show (a : B) = Ideal.Quotient.mk Brel (X 0) from rfl,
        show (b : B) = Ideal.Quotient.mk Brel (X 1) from rfl, ← map_add, ← map_mul]
  rw [this, coordFun_eight_apply]

/-- `coeff (X₀ * p) μ = 0` when `μ 0 = 0` (the monomial `μ` is not divisible by
`X₀`, so it cannot occur in `X₀ * p`). -/
theorem coeff_X0_mul_eq_zero (μ : Fin 4 →₀ ℕ) (h : μ 0 = 0) (p : P4) :
    coeff μ (X 0 * p) = 0 := by
  rw [coeff_X_mul', if_neg]
  rw [Finsupp.mem_support_iff]; simp [h]

/-- `coeff (X₁ * p) μ = 0` when `μ 1 = 0`. -/
theorem coeff_X1_mul_eq_zero (μ : Fin 4 →₀ ℕ) (h : μ 1 = 0) (p : P4) :
    coeff μ (X 1 * p) = 0 := by
  rw [coeff_X_mul', if_neg]
  rw [Finsupp.mem_support_iff]; simp [h]

/-! Concrete `bexp` exponents needed below. -/
theorem bexp_one : bexp 1 = Finsupp.single 0 1 := by rw [bexp]; rfl
theorem bexp_two : bexp 2 = Finsupp.single 1 1 := by rw [bexp]; rfl

/-- **C1 — `B_triple_zero` (frozen type).** The triple principal intersection
`aB ∩ bB ∩ (a+b)B` vanishes in `B`. An element `x` of the intersection is
`a·r = b·s = (a+b)·t`; reading the `14` coordinate functionals on these three
equal elements forces every coordinate of `x` to be `0`. -/
theorem B_triple_zero_proof :
    Ideal.span {a} ⊓ Ideal.span {b} ⊓ Ideal.span {a + b} = (⊥ : Ideal B) := by
  rw [eq_bot_iff]
  intro x hx
  rw [Ideal.mem_inf, Ideal.mem_inf] at hx
  obtain ⟨⟨hxa, hxb⟩, hxab⟩ := hx
  rw [Ideal.mem_span_singleton'] at hxa hxb hxab
  obtain ⟨r, hr⟩ := hxa
  obtain ⟨s, hs⟩ := hxb
  obtain ⟨t, ht⟩ := hxab
  -- Lift the multipliers to polynomials.
  obtain ⟨pr, rfl⟩ := Ideal.Quotient.mk_surjective r
  obtain ⟨ps, rfl⟩ := Ideal.Quotient.mk_surjective s
  obtain ⟨pt, rfl⟩ := Ideal.Quotient.mk_surjective t
  -- `x` is each of the three products.
  rw [mul_comm] at hr hs ht
  rw [Submodule.mem_bot]
  apply eq_zero_of_coordFun
  -- We establish all 14 coordinates of x are 0.
  -- First, the four "extraction" coordinates (5,9,7,10) of x are 0 via a·r / b·s.
  have hx5 : coordFun 5 x = 0 := by
    rw [← hs, coordFun_b_mul (by decide)]
    exact coeff_X1_mul_eq_zero _ (by rw [bexp_apply]; decide) ps
  have hx7 : coordFun 7 x = 0 := by
    rw [← hs, coordFun_b_mul (by decide)]
    exact coeff_X1_mul_eq_zero _ (by rw [bexp_apply]; decide) ps
  have hx9 : coordFun 9 x = 0 := by
    rw [← hr, coordFun_a_mul (by decide)]
    exact coeff_X0_mul_eq_zero _ (by rw [bexp_apply]; decide) pr
  have hx10 : coordFun 10 x = 0 := by
    rw [← hr, coordFun_a_mul (by decide)]
    exact coeff_X0_mul_eq_zero _ (by rw [bexp_apply]; decide) pr
  -- The (a+b)·t readings of coords 5,9,7,10 give t_a,t_b,t_c,t_d = 0.
  have ht_a : coeff (Finsupp.single 0 1) pt = 0 := by
    have := hx5; rw [← ht, coordFun_ab_mul (by decide)] at this
    rw [add_mul, coeff_add] at this
    rw [show bexp 5 = Finsupp.single 0 1 + Finsupp.single 0 1 from by
          rw [← Finsupp.single_add, bexp]; rfl] at this
    rw [coeff_X_mul, coeff_X1_mul_eq_zero _ (by simp [Finsupp.add_apply])
        pt, add_zero] at this
    exact this
  have ht_b : coeff (Finsupp.single 1 1) pt = 0 := by
    have := hx9; rw [← ht, coordFun_ab_mul (by decide)] at this
    rw [add_mul, coeff_add] at this
    rw [show bexp 9 = Finsupp.single 1 1 + Finsupp.single 1 1 from by
          rw [← Finsupp.single_add, bexp]; rfl] at this
    rw [coeff_X0_mul_eq_zero _ (by simp [Finsupp.add_apply]) pt,
        zero_add, coeff_X_mul] at this
    exact this
  have ht_c : coeff (Finsupp.single 2 1) pt = 0 := by
    have := hx7; rw [← ht, coordFun_ab_mul (by decide)] at this
    rw [add_mul, coeff_add] at this
    rw [show bexp 7 = Finsupp.single 0 1 + Finsupp.single 2 1 from by
          rw [bexp]; rfl] at this
    rw [coeff_X_mul (Finsupp.single 2 1) 0 pt,
        coeff_X1_mul_eq_zero (Finsupp.single 0 1 + Finsupp.single 2 1)
          (by simp [Finsupp.add_apply]) pt, add_zero] at this
    exact this
  have ht_d : coeff (Finsupp.single 3 1) pt = 0 := by
    have := hx10; rw [← ht, coordFun_ab_mul (by decide)] at this
    rw [add_mul, coeff_add] at this
    rw [show bexp 10 = Finsupp.single 1 1 + Finsupp.single 3 1 from by
          rw [bexp]; rfl] at this
    rw [coeff_X0_mul_eq_zero (Finsupp.single 1 1 + Finsupp.single 3 1)
          (by simp [Finsupp.add_apply]) pt,
        coeff_X_mul (Finsupp.single 3 1) 1 pt, zero_add] at this
    exact this
  -- Now coord 6 (ab) and coord 8 (ad) of x via (a+b)·t.
  have hx6 : coordFun 6 x = 0 := by
    rw [← ht, coordFun_ab_mul (by decide), add_mul, coeff_add]
    rw [show bexp 6 = Finsupp.single 0 1 + Finsupp.single 1 1 from by rw [bexp]; rfl]
    -- coeff (ab) (X0·pt) = t_b ; coeff (ab) (X1·pt) = t_a
    rw [coeff_X_mul]
    rw [show (Finsupp.single 0 1 + Finsupp.single 1 1 : Fin 4 →₀ ℕ)
          = Finsupp.single 1 1 + Finsupp.single 0 1 from by abel]
    rw [coeff_X_mul, ht_a, ht_b, add_zero]
  have hx8 : coordFun 8 x = 0 := by
    rw [← ht, coordFun8_ab_mul, add_mul]
    unfold phiP
    rw [LinearMap.add_apply, map_add, map_add]
    simp only [lcoeff_apply]
    -- mon03 = ad, mon12 = bc
    rw [show (mon03 : Fin 4 →₀ ℕ) = Finsupp.single 0 1 + Finsupp.single 3 1 from rfl,
        show (mon12 : Fin 4 →₀ ℕ) = Finsupp.single 1 1 + Finsupp.single 2 1 from rfl]
    rw [coeff_X_mul]  -- coeff mon03 (X0 pt) = coeff (single 3 1) pt = t_d
    rw [coeff_X1_mul_eq_zero (Finsupp.single 0 1 + Finsupp.single 3 1)
        (by simp [Finsupp.add_apply]) pt]  -- coeff mon03 (X1 pt) = 0
    rw [coeff_X0_mul_eq_zero (Finsupp.single 1 1 + Finsupp.single 2 1)
        (by simp [Finsupp.add_apply]) pt]  -- coeff mon12 (X0 pt) = 0
    rw [coeff_X_mul]  -- coeff mon12 (X1 pt) = coeff (single 2 1) pt = t_c
    rw [ht_d, ht_c]; ring
  -- All remaining coordinates are 0 directly via a·r or b·s.
  intro i
  fin_cases i
  · -- coord 0 (the `1` coordinate): via a·r, X0*pr has no constant term
    change coordFun 0 x = 0
    rw [← hr, coordFun_a_mul (by decide)]
    exact coeff_X0_mul_eq_zero _ (by rw [bexp_apply]; decide) pr
  · change coordFun 1 x = 0
    rw [← hs, coordFun_b_mul (by decide)]
    exact coeff_X1_mul_eq_zero _ (by rw [bexp_apply]; decide) ps
  · change coordFun 2 x = 0
    rw [← hr, coordFun_a_mul (by decide)]
    exact coeff_X0_mul_eq_zero _ (by rw [bexp_apply]; decide) pr
  · change coordFun 3 x = 0
    rw [← hr, coordFun_a_mul (by decide)]
    exact coeff_X0_mul_eq_zero _ (by rw [bexp_apply]; decide) pr
  · change coordFun 4 x = 0
    rw [← hr, coordFun_a_mul (by decide)]
    exact coeff_X0_mul_eq_zero _ (by rw [bexp_apply]; decide) pr
  · change coordFun 5 x = 0; exact hx5
  · change coordFun 6 x = 0; exact hx6
  · change coordFun 7 x = 0; exact hx7
  · change coordFun 8 x = 0; exact hx8
  · change coordFun 9 x = 0; exact hx9
  · change coordFun 10 x = 0; exact hx10
  · change coordFun 11 x = 0
    rw [← hr, coordFun_a_mul (by decide)]
    exact coeff_X0_mul_eq_zero _ (by rw [bexp_apply]; decide) pr
  · change coordFun 12 x = 0
    rw [← hr, coordFun_a_mul (by decide)]
    exact coeff_X0_mul_eq_zero _ (by rw [bexp_apply]; decide) pr
  · change coordFun 13 x = 0
    rw [← hr, coordFun_a_mul (by decide)]
    exact coeff_X0_mul_eq_zero _ (by rw [bexp_apply]; decide) pr

/-! ### C4 — the frozen `M_triple_defect` -/

/-- **C4 milestone — `M_triple_defect` (frozen type).** The module `M = B⁴/Bv`
acquires a nonzero triple-intersection defect `u`, lying in each of `aM`, `bM`,
`(a+b)M`. Assembled from `u_ne_zero` and the three memberships. -/
theorem M_triple_defect_proof :
    u ≠ 0 ∧ u ∈ smulSub a ∧ u ∈ smulSub b ∧ u ∈ smulSub (a + b) :=
  ⟨u_ne_zero, u_mem_a, u_mem_b, u_mem_ab⟩

end Prob4b
