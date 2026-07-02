/-
Copyright (c) 2026 Prob4b formalization. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Prob4b formalization
-/
import Prob4b.Proofs.RingModel.Normal

/-!
# Stage B — `M` preserves annihilators and pairwise principal intersections

This file develops the Stage-B reduction for the Problem 4(b) counterexample
(`BLUEPRINT.md` "Stage B", `SKETCH.md` Step 2). The two frozen targets are, over
the **entire** ring `B`:

* `M_annihilator : ∀ x, annihM x = (annih x) • (⊤ : Submodule B M)`
* `M_pairwise_intersection :
    ∀ x y, smulSub x ⊓ smulSub y = (Ideal.span {x} ⊓ Ideal.span {y}) • ⊤`

with `M = (Fin 4 → B) ⧸ Bv`, `Bv = span B {v}`, `v = (a,b,c,d)`.

## Status (complete)

Both frozen targets `M_annihilator_proof` / `M_pairwise_intersection_proof` are
**fully proved** here and axiom-clean (`[propext, Classical.choice, Quot.sound]`).
They reduce, in both directions and with the easy `⊇` inclusions fully formal, to
the **colon identity for `≤2`-generated ideals**

  `colon2 (x y r : B) (h : ∀ k, r * v k ∈ Ideal.span {x} ⊔ Ideal.span {y}) :
      r ∈ Ideal.span {x} ⊔ Ideal.span {y} ⊔ m ^ 2`.

Every piece is proved: the **unit case**, the `r ∈ 𝔪` reduction (`r_mem_m`), the
`𝔪²`-coordinate characterization (`mem_msq_of_coords`), the splitting bridge
(`colon2_mcase`), all supporting `𝔽₂`-coordinate machinery, and the former blocker
`colon2_core_d1`: for `x, y, r ∈ 𝔪`, the colon hypothesis forces the
linear-coordinate vector `d1 r ∈ 𝔽₂⁴` into `span(d1 x, d1 y)` — the degree-`2`
quadratic-`𝔽₂`-pairing rank step, dispatched by structured `𝔽₂` casework over a
computable `Fin`-bitmask model. Nothing here is open.

## Strategy of the reduction

Three reductions turn the submodule equalities into statements about the finite
ring `B`:

* `mem_smul_top_pi`: for a free module `B⁴`, `I • ⊤` is exactly the set of
  vectors with every coordinate in `I`.
* `mem_smul_top_M`: pushing through the surjection `mkQ : B⁴ → M`, an element of
  `I • (⊤ : Submodule B M)` is the class of some representative all of whose
  coordinates lie in `I`.
* `mem_annihM`: the class of `w` is annihilated by `x` iff `x • w ∈ Bv`.

The `⊇` inclusions are then formal (`I` kills the coordinates after scaling). The
`⊆` inclusions reduce to `colon2`, phrased concretely as: if `r • v` has every
coordinate in `(x) + (y)`, then `r ∈ (x) + (y) + 𝔪²`. (`v k` runs over the
generators `a,b,c,d` of `𝔪`, so "every coordinate of `r • v` is in `J`" is
exactly `r ∈ (J : 𝔪)`.) The annihilator case is the `y = 0` instance; the pairwise
case splits the resulting `r = p + q + e` (`p ∈ (x)`, `q ∈ (y)`, `e ∈ 𝔪²`) and uses
`𝔪² · 𝔪 = 𝔪³ = 0`.

Everything is structural / `𝔽₂`-coordinate based on the `14`-dimensional model of
`B` (`Normal.lean`); never a `decide` over the `2¹⁴` elements of `B` (whose
`Fintype` is noncomputable), only `decide` over the computable coordinate type
`Fin n → ZMod 2`.

See `BLUEPRINT.md` "Stage B" and `PROGRESS.md`.
-/

namespace Prob4b

open Submodule MvPolynomial

/-! ### Reduction lemmas: membership in `I • ⊤` and in `annihM` -/

/-- For the free module `B⁴`, `I • (⊤ : Submodule B (Fin 4 → B))` is exactly the
set of vectors all of whose coordinates lie in `I`. -/
theorem mem_smul_top_pi (I : Ideal B) (w : Fin 4 → B) :
    w ∈ I • (⊤ : Submodule B (Fin 4 → B)) ↔ ∀ k, w k ∈ I := by
  constructor
  · intro hw
    refine Submodule.smul_induction_on hw ?_ ?_
    · intro c hc t _ k; simpa using I.mul_mem_right (t k) hc
    · intro p q hp hq k; simpa using add_mem (hp k) (hq k)
  · intro hw
    have hrw : w = ∑ k, (w k) • (Pi.single k 1 : Fin 4 → B) := by
      funext j; simp [Pi.single_apply, Finset.sum_ite_eq]
    rw [hrw]
    exact sum_mem (fun k _ => Submodule.smul_mem_smul (hw k) Submodule.mem_top)

/-- `I • (⊤ : Submodule B M)` is the image of `I • ⊤_{B⁴}` under `mkQ`. -/
theorem smul_top_M_eq_map (I : Ideal B) :
    I • (⊤ : Submodule B M) = (I • (⊤ : Submodule B (Fin 4 → B))).map Bv.mkQ := by
  conv_lhs => rw [show (⊤ : Submodule B M) = (⊤ : Submodule B (Fin 4 → B)).map Bv.mkQ from by
    rw [Submodule.map_top, Submodule.range_mkQ]]
  rw [Submodule.map_smul'']

/-- Membership in `I • (⊤ : Submodule B M)`: `z` is the class of some
representative all of whose coordinates lie in `I`. -/
theorem mem_smul_top_M (I : Ideal B) (z : M) :
    z ∈ I • (⊤ : Submodule B M) ↔ ∃ w : Fin 4 → B, (∀ k, w k ∈ I) ∧ Bv.mkQ w = z := by
  rw [smul_top_M_eq_map, Submodule.mem_map]
  constructor
  · rintro ⟨w, hw, rfl⟩; exact ⟨w, (mem_smul_top_pi I w).mp hw, rfl⟩
  · rintro ⟨w, hw, rfl⟩; exact ⟨w, (mem_smul_top_pi I w).mpr hw, rfl⟩

/-- `mkQ w` is annihilated by `x` (in `M`) iff `x • w ∈ Bv`. -/
theorem mem_annihM (x : B) (w : Fin 4 → B) :
    (Bv.mkQ w) ∈ annihM x ↔ x • w ∈ Bv := by
  unfold annihM
  rw [LinearMap.mem_ker, show LinearMap.lsmul B M x (Bv.mkQ w) = x • Bv.mkQ w from rfl,
    ← LinearMap.map_smul, show Bv.mkQ (x • w) = Submodule.Quotient.mk (x • w) from rfl,
    Submodule.Quotient.mk_eq_zero]

/-- Membership in the elementwise annihilator ideal: `z ∈ annih x ↔ z * x = 0`. -/
theorem mem_annih_iff (x z : B) : z ∈ annih x ↔ z * x = 0 := by
  unfold annih
  rw [LinearMap.mem_ker, show LinearMap.lsmul B B x z = x * z from rfl, mul_comm]

/-- The classes of `w` and `w - s • v` agree in `M` (they differ by `s • v ∈ Bv`). -/
theorem mkQ_sub_smul_v (s : B) (w : Fin 4 → B) :
    Bv.mkQ (w - s • v) = Bv.mkQ w := by
  rw [show Bv.mkQ (w - s • v) = Submodule.Quotient.mk (w - s • v) from rfl,
      show Bv.mkQ w = Submodule.Quotient.mk w from rfl, Submodule.Quotient.eq]
  rw [show w - s • v - w = -(s • v) from by ring, Bv]
  exact Submodule.neg_mem _ (Submodule.smul_mem _ s (Submodule.mem_span_singleton_self v))

/-! ### Membership in `𝔪` via the constant coordinate, and the unit case -/

theorem a_mem_m : a ∈ m := Ideal.subset_span (by simp)
theorem b_mem_m : b ∈ m := Ideal.subset_span (by simp)
theorem c_mem_m : c ∈ m := Ideal.subset_span (by simp)
theorem d_mem_m : d ∈ m := Ideal.subset_span (by simp)

/-- Every basis monomial except `1` (index `0`) lies in `𝔪`. -/
theorem basisMon_mem_m (j : Fin 14) (hj : j ≠ 0) : basisMon j ∈ m := by
  rw [basisMon_eq]; fin_cases j
  · exact absurd rfl hj
  · exact a_mem_m
  · exact b_mem_m
  · exact c_mem_m
  · exact d_mem_m
  · exact Ideal.mul_mem_left _ _ a_mem_m
  · exact Ideal.mul_mem_left _ _ b_mem_m
  · exact Ideal.mul_mem_left _ _ c_mem_m
  · exact Ideal.mul_mem_left _ _ d_mem_m
  · exact Ideal.mul_mem_left _ _ b_mem_m
  · exact Ideal.mul_mem_left _ _ d_mem_m
  · exact Ideal.mul_mem_left _ _ c_mem_m
  · exact Ideal.mul_mem_left _ _ d_mem_m
  · exact Ideal.mul_mem_left _ _ d_mem_m

/-- `coordFun 0` reads the constant coefficient. -/
theorem coord0_mk (p : P4) : coordFun 0 (Ideal.Quotient.mk Brel p) = coeff 0 p := by
  rw [coordFun_apply (by decide), show bexp 0 = 0 from by rw [bexp]; rfl]

theorem mem_m_of_coeff0 (p : P4) (hp : coeff 0 p = 0) :
    Ideal.Quotient.mk Brel p ∈ m := by
  rw [m_eq_map]; apply Ideal.mem_map_of_mem
  rw [mP_eq, ← pow_one (idealOfVars (Fin 4) (ZMod 2)), mem_pow_idealOfVars_iff']
  intro xx hxx
  rw [(by rw [Nat.lt_one_iff, Finsupp.degree_eq_zero_iff] at hxx; exact hxx : xx = 0)]; exact hp

/-- `z ∈ 𝔪` iff its constant coordinate vanishes (the augmentation kernel). -/
theorem mem_m_iff_coord0 (z : B) : z ∈ m ↔ coordFun 0 z = 0 := by
  obtain ⟨p, rfl⟩ := Ideal.Quotient.mk_surjective z
  rw [coord0_mk]
  constructor
  · intro hz
    rw [m_eq_map, Ideal.mem_map_iff_of_surjective _ Ideal.Quotient.mk_surjective] at hz
    obtain ⟨p', hp', hpp'⟩ := hz
    have hcc : coeff 0 p = coeff 0 p' := by rw [← coord0_mk, ← coord0_mk, hpp']
    rw [hcc, mP_eq, ← pow_one (idealOfVars (Fin 4) (ZMod 2)), mem_pow_idealOfVars_iff'] at *
    exact hp' 0 (by simp [Finsupp.degree])
  · intro hz; exact mem_m_of_coeff0 p hz

theorem isNilpotent_of_mem_m {n : B} (hn : n ∈ m) : IsNilpotent n := by
  refine ⟨3, ?_⟩
  have : n ^ 3 ∈ m ^ 3 := Ideal.pow_mem_pow hn 3
  rw [m_pow_three] at this; simpa using this

theorem coord0_one : coordFun 0 (1 : B) = 1 := by
  rw [show (1 : B) = Ideal.Quotient.mk Brel 1 from by simp, coord0_mk]; simp

/-- If `x` has constant coordinate `1`, it is a unit (`x = 1 - n`, `n ∈ 𝔪` nilpotent). -/
theorem isUnit_of_coord0_one {x : B} (hx : coordFun 0 x = 1) : IsUnit x := by
  have h1x : (1 - x) ∈ m := by rw [mem_m_iff_coord0, map_sub, hx, coord0_one]; ring
  simpa using (isNilpotent_of_mem_m h1x).isUnit_one_sub

/-- A unit (constant coordinate `1`) generates the whole ring. -/
theorem span_eq_top_of_coord0_one {x : B} (hx : coordFun 0 x = 1) :
    Ideal.span {x} = (⊤ : Ideal B) := by
  rw [Ideal.span_singleton_eq_top]; exact isUnit_of_coord0_one hx

/-! ### The colon identity for ≤2-generated ideals (the crux) -/

/-- The ideal `𝔪² ` annihilates `𝔪`: `e ∈ 𝔪² ⟹ e * (v k) = 0` (this is `𝔪³ = 0`). -/
theorem msq_smul_v (e : B) (he : e ∈ m ^ 2) (k : Fin 4) : e * v k = 0 := by
  have hvk : v k ∈ m := by
    have : v k ∈ ({a, b, c, d} : Set B) := by fin_cases k <;> simp [v]
    exact Ideal.subset_span this
  have : e * v k ∈ m ^ 3 := by
    rw [pow_succ]
    exact Ideal.mul_mem_mul he hvk
  rw [m_pow_three] at this
  simpa using this

/-! ### Coordinate machinery for multiplication in `B`

The remaining colon identity `colon2` (below) requires reading products `z * g`
in the `𝔽₂`-coordinate model. These lemmas express `coordFun ℓ (z * g)` through the
`14`-dimensional basis: the degree filtration `B = B₀ ⊕ B₁ ⊕ B₂` (constant /
linear / quadratic, coordinates `0` / `1..4` / `5..13`) makes multiplication
graded, with everything of degree `≥ 3` vanishing (`𝔪³ = 0`). -/

/-- Every coordinate of `z` equals the corresponding basis-representation coefficient. -/
theorem coord_repr (i : Fin 14) (z : B) : coordFun i z = B_basis.repr z i := by
  conv_lhs => rw [← B_basis.linearCombination_repr z]
  rw [Finsupp.linearCombination_apply, Finsupp.sum_fintype _ _ (by simp), map_sum]
  simp only [map_smul, B_basis_apply, coordFun_basisMon, smul_eq_mul]
  rw [Finset.sum_eq_single i]
  · simp
  · intro j _ hj; rw [if_neg (fun h => hj h.symm), mul_zero]
  · simp

/-- An element with all coordinates `0` is `0` (`coordFun` is injective jointly). -/
theorem eq_zero_of_coords (z : B) (h : ∀ i, coordFun i z = 0) : z = 0 := by
  have hr : B_basis.repr z = 0 := by ext i; rw [← coord_repr]; exact h i
  simpa using congrArg B_basis.repr.symm hr

/-- Expand a product `z * g` over the basis of the left factor. -/
theorem mul_gen_expand (z g : B) :
    z * g = ∑ j : Fin 14, (coordFun j z) • (basisMon j * g) := by
  conv_lhs => rw [← B_basis.linearCombination_repr z]
  rw [Finsupp.linearCombination_apply, Finsupp.sum_fintype _ _ (by simp), Finset.sum_mul]
  exact Finset.sum_congr rfl (fun j _ => by rw [B_basis_apply, smul_mul_assoc, coord_repr])

/-- The quadratic basis monomials (`j ≥ 5`) lie in `𝔪²`. -/
theorem basisMon_mem_msq (j : Fin 14) (hj : 5 ≤ j.val) : basisMon j ∈ m ^ 2 := by
  have hsq : ∀ p q : B, p ∈ m → q ∈ m → p * q ∈ m ^ 2 := fun p q hp hq => by
    rw [sq]; exact Ideal.mul_mem_mul hp hq
  rw [basisMon_eq]
  fin_cases j
  · exact absurd hj (by decide)
  · exact absurd hj (by decide)
  · exact absurd hj (by decide)
  · exact absurd hj (by decide)
  · exact absurd hj (by decide)
  · exact hsq _ _ a_mem_m a_mem_m
  · exact hsq _ _ a_mem_m b_mem_m
  · exact hsq _ _ a_mem_m c_mem_m
  · exact hsq _ _ a_mem_m d_mem_m
  · exact hsq _ _ b_mem_m b_mem_m
  · exact hsq _ _ b_mem_m d_mem_m
  · exact hsq _ _ c_mem_m c_mem_m
  · exact hsq _ _ c_mem_m d_mem_m
  · exact hsq _ _ d_mem_m d_mem_m

/-- A quadratic basis monomial times a generator is `0` (degree `3`, `𝔪³ = 0`). -/
theorem basisMon_mul_gen_eq_zero (j : Fin 14) (hj : 5 ≤ j.val) (g : B) (hg : g ∈ m) :
    basisMon j * g = 0 := by
  have : basisMon j * g ∈ m ^ 3 := by
    rw [show (3 : ℕ) = 2 + 1 from rfl, pow_add, pow_one]
    exact Ideal.mul_mem_mul (basisMon_mem_msq j hj) hg
  rw [m_pow_three] at this; simpa using this

/-- A linear basis monomial (`1 ≤ j ≤ 4`) times a generator lies in `𝔪²`. -/
theorem basisMon_mul_gen_mem_msq (j : Fin 14) (hj1 : 1 ≤ j.val) (hj2 : j.val ≤ 4)
    (g : B) (hg : g ∈ m) : basisMon j * g ∈ m ^ 2 := by
  rw [sq]; exact Ideal.mul_mem_mul (basisMon_mem_m j (by omega)) hg

theorem m_sq_eq_map : m ^ 2 = (mP ^ 2).map (Ideal.Quotient.mk Brel) := by
  rw [m_eq_map, ← Ideal.map_pow]

/-- The degree of a low basis exponent (`ℓ ≤ 4`) is `≤ 1`. -/
theorem bexp_degree_low (ℓ : Fin 14) (hℓ : ℓ.val ≤ 4) : Finsupp.degree (bexp ℓ) ≤ 1 := by
  rw [degree_eq_sum, bexp_apply, bexp_apply, bexp_apply, bexp_apply]
  fin_cases ℓ <;> simp_all

/-- A degree-`≤ 1` coordinate (`ℓ ≤ 4`) of an element of `𝔪²` is `0`. -/
theorem coord_low_msq (ℓ : Fin 14) (hℓ : ℓ.val ≤ 4) (z : B) (hz : z ∈ m ^ 2) :
    coordFun ℓ z = 0 := by
  rw [m_sq_eq_map, Ideal.mem_map_iff_of_surjective _ Ideal.Quotient.mk_surjective] at hz
  obtain ⟨p, hp, rfl⟩ := hz
  have hℓ8 : ℓ ≠ 8 := by intro h; rw [h] at hℓ; exact absurd hℓ (by decide)
  rw [coordFun_apply hℓ8, mP_eq, mem_pow_idealOfVars_iff' (R := ZMod 2)] at *
  exact hp (bexp ℓ) (by have := bexp_degree_low ℓ hℓ; omega)

/-- **The degree-`1` structure constant.** For a degree-`≤ 1` coordinate
(`1 ≤ ℓ ≤ 4`) and `g ∈ 𝔪`, `coordFun ℓ (z * g) = (const. coord of z) · coordFun ℓ g`:
only the constant part of `z` contributes to the linear part of `z * g`. -/
theorem coord_deg1_mul (ℓ : Fin 14) (hℓ2 : ℓ.val ≤ 4) (_hℓ1 : 1 ≤ ℓ.val)
    (z g : B) (hg : g ∈ m) : coordFun ℓ (z * g) = coordFun 0 z * coordFun ℓ g := by
  rw [mul_gen_expand z g, map_sum, Finset.sum_eq_single (0 : Fin 14)]
  · simp only [map_smul, smul_eq_mul]; congr 1
    rw [show basisMon 0 = 1 from by rw [basisMon_eq]; rfl, one_mul]
  · intro j _ hj
    rw [map_smul, smul_eq_mul]
    by_cases hj5 : 5 ≤ j.val
    · rw [basisMon_mul_gen_eq_zero j hj5 g hg, map_zero, mul_zero]
    · rw [coord_low_msq ℓ (by omega) _ (basisMon_mul_gen_mem_msq j (by omega) (by omega) g hg),
        mul_zero]
  · intro hc; exact absurd (Finset.mem_univ _) hc

/-- The linear coordinates of the generator `v k = g_{k}`: `coordFun ℓ (v k) = δ_{ℓ, k+1}`. -/
theorem coord_v (ℓ : Fin 14) (k : Fin 4) :
    coordFun ℓ (v k) = if ℓ.val = k.val + 1 then 1 else 0 := by
  have hbm : v k = basisMon ⟨k.val + 1, by omega⟩ := by
    fin_cases k <;> (rw [basisMon_eq]; rfl)
  rw [hbm, coordFun_basisMon]
  by_cases h : ℓ.val = k.val + 1
  · rw [if_pos (by apply Fin.ext; simpa using h), if_pos h]
  · rw [if_neg (by intro hh; exact h (by rw [hh])), if_neg h]

theorem v_mem_m (k : Fin 4) : v k ∈ m := by
  have : v k ∈ ({a, b, c, d} : Set B) := by fin_cases k <;> simp [v]
  exact Ideal.subset_span this

/-! ### The "`𝔪` is not `≤2`-generated" rank fact, and `r ∈ 𝔪`

`r ∈ (J : 𝔪)` with `J = (x) + (y)` and `x, y ∈ 𝔪` forces `r ∈ 𝔪`: otherwise `r`
is a unit, so the hypothesis `r · 𝔪 ⊆ J` gives `𝔪 ⊆ J`, making the four
generators' (linearly independent) images lie in the `≤ 2`-dimensional span of the
linear parts of `x, y` — impossible. The rank fact is a finite `𝔽₂`-computation
over coordinate vectors (`decide` on `Fin 4 → ZMod 2`, which **is** computable,
unlike `decide` over `B`). -/

/-- Four standard basis vectors of `𝔽₂⁴` cannot all lie in the span of two
vectors. A finite `decide` over the computable type `Fin 4 → ZMod 2`. -/
theorem four_std_not_in_two_span :
    ∀ X Y : Fin 4 → ZMod 2,
      ¬ (∀ k : Fin 4, ∃ s t : ZMod 2, (Pi.single k (1 : ZMod 2)) = s • X + t • Y) := by
  decide

/-- The linear-coordinate vector of `z : B` (coordinates `1..4`). -/
noncomputable def d1 (z : B) : Fin 4 → ZMod 2 := fun i => coordFun ⟨i.val + 1, by omega⟩ z

/-- **`r ∈ 𝔪` for the colon hypothesis** (`x, y ∈ 𝔪`). If `r` were a unit, the
hypothesis would force every generator's linear part into the `≤2`-dimensional
`span(x₁, y₁)`, contradicting `four_std_not_in_two_span`. -/
theorem r_mem_m (x y r : B) (hx : x ∈ m) (hy : y ∈ m)
    (h : ∀ k, r * v k ∈ (Ideal.span {x} ⊔ Ideal.span {y} : Ideal B)) : r ∈ m := by
  rw [mem_m_iff_coord0]
  by_contra hr0
  have hr1 : coordFun 0 r = 1 := by
    have := hr0; revert this; generalize coordFun 0 r = z; revert z; decide
  apply four_std_not_in_two_span (d1 x) (d1 y)
  intro k
  obtain ⟨wx, hwx, wy, hwy, hsum⟩ := Submodule.mem_sup.mp (h k)
  rw [Ideal.mem_span_singleton] at hwx hwy
  obtain ⟨ux, rfl⟩ := hwx
  obtain ⟨uy, rfl⟩ := hwy
  refine ⟨coordFun 0 ux, coordFun 0 uy, ?_⟩
  funext i
  simp only [Pi.add_apply, Pi.smul_apply, smul_eq_mul, d1]
  have hval : (⟨i.val + 1, by omega⟩ : Fin 14).val = i.val + 1 := rfl
  have hℓ : (⟨i.val + 1, by omega⟩ : Fin 14).val ≤ 4
      ∧ 1 ≤ (⟨i.val + 1, by omega⟩ : Fin 14).val := by rw [hval]; omega
  have key : coordFun ⟨i.val + 1, by omega⟩ (r * v k) = (if i = k then (1 : ZMod 2) else 0) := by
    rw [coord_deg1_mul _ hℓ.1 hℓ.2 r (v k) (v_mem_m k), hr1, one_mul, coord_v, hval]
    by_cases hik : i = k
    · rw [if_pos (by omega), if_pos hik]
    · rw [if_neg (by intro hh; exact hik (Fin.ext (by omega))), if_neg hik]
  rw [← hsum] at key
  rw [Pi.single_apply, ← key, map_add, mul_comm x ux, mul_comm y uy,
      coord_deg1_mul _ hℓ.1 hℓ.2 ux x hx, coord_deg1_mul _ hℓ.1 hℓ.2 uy y hy]

/-- `z ∈ 𝔪²` iff its degree-`≤1` coordinates (indices `0..4`) all vanish: `𝔪²` is
the span of the `9` degree-`2` basis monomials. -/
theorem mem_msq_of_coords (z : B) (h : ∀ ℓ : Fin 14, ℓ.val ≤ 4 → coordFun ℓ z = 0) :
    z ∈ m ^ 2 := by
  have hz : z = ∑ j : Fin 14, (coordFun j z) • basisMon j := by
    conv_lhs => rw [← B_basis.linearCombination_repr z]
    rw [Finsupp.linearCombination_apply, Finsupp.sum_fintype _ _ (by simp)]
    apply Finset.sum_congr rfl
    intro j _; rw [B_basis_apply, coord_repr]
  rw [hz]
  refine Submodule.sum_mem _ (fun j _ => ?_)
  by_cases hj : 5 ≤ j.val
  · exact (m ^ 2).restrictScalars (ZMod 2) |>.smul_mem _ (basisMon_mem_msq j hj)
  · rw [h j (by omega), zero_smul]; exact Submodule.zero_mem _

/-- A `ZMod 2`-scalar multiple of `x` lies in the principal ideal `(x)`. -/
theorem zmod2_smul_mem_span (α : ZMod 2) (x : B) : α • x ∈ Ideal.span {x} := by
  rw [Ideal.mem_span_singleton]
  refine ⟨algebraMap (ZMod 2) B α, ?_⟩
  rw [mul_comm]; exact Algebra.smul_def α x

/-! ### The remaining colon core (the degree-`2` quadratic rank step)

After the unit case and `r ∈ 𝔪`, the colon identity reduces to: the **linear**
part of `r` lies in the `𝔽₂`-span of the linear parts of `x` and `y`. This is the
one genuinely open step (`colon2_core_d1`); everything below (`colon2_mcase`,
`colon2`, and the two frozen theorems) is fully proved *modulo* it. -/

/-! #### The degree-`2` quadratic pairing `Φ`

For `z ∈ 𝔪` and a generator `v k`, the degree-`2` coordinates of `z · (v k)` are a
bilinear function of `d1 z` and the standard vector `e_k`. We package this as an
explicit `𝔽₂`-bilinear "pairing matrix": the products of generators
`(v i)·(v k)` are the degree-`2` basis monomials (with `b·c` collapsed to `a·d`),
recorded by the index table `prodIdx`. -/

/-- `v k` is the `(k+1)`-th basis monomial. -/
theorem v_eq_basisMon (k : Fin 4) : v k = basisMon ⟨k.val + 1, by omega⟩ := by
  fin_cases k <;> (rw [basisMon_eq]; rfl)

/-- The product index table for generators: `(v i)·(v k) = basisMon (prodIdx i k)`.
Row/column order `a,b,c,d`; `b·c` collapses to `a·d` (index `8`). -/
def prodIdx : Fin 4 → Fin 4 → Fin 14 :=
  ![![5, 6, 7, 8],
    ![6, 9, 8, 10],
    ![7, 8, 11, 12],
    ![8, 10, 12, 13]]

/-- `prodIdx` is symmetric (generator multiplication is commutative). -/
theorem prodIdx_symm (i k : Fin 4) : prodIdx i k = prodIdx k i := by
  fin_cases i <;> fin_cases k <;> rfl

/-- The generator product is the basis monomial named by `prodIdx`. -/
theorem gen_mul_eq_basisMon (i k : Fin 4) : v i * v k = basisMon (prodIdx i k) := by
  have e5 : basisMon 5 = a * a := by rw [basisMon_eq]; rfl
  have e6 : basisMon 6 = a * b := by rw [basisMon_eq]; rfl
  have e7 : basisMon 7 = a * c := by rw [basisMon_eq]; rfl
  have e8 : basisMon 8 = a * d := by rw [basisMon_eq]; rfl
  have e9 : basisMon 9 = b * b := by rw [basisMon_eq]; rfl
  have e10 : basisMon 10 = b * d := by rw [basisMon_eq]; rfl
  have e11 : basisMon 11 = c * c := by rw [basisMon_eq]; rfl
  have e12 : basisMon 12 = c * d := by rw [basisMon_eq]; rfl
  have e13 : basisMon 13 = d * d := by rw [basisMon_eq]; rfl
  have hbc : b * c = a * d := (ad_eq_bc).symm
  fin_cases i <;> fin_cases k <;>
    simp only [v, prodIdx, Fin.zero_eta, Fin.mk_one, Fin.isValue,
      Matrix.cons_val_zero, Matrix.cons_val_one,
      Matrix.cons_val, Matrix.cons_val_fin_one, Matrix.cons_val',
      Fin.reduceFinMk,
      e5, e6, e7, e8, e9, e10, e11, e12, e13] <;>
    first
      | rfl
      | exact hbc
      | exact mul_comm _ _
      | exact (mul_comm _ _).trans hbc

/-- The degree-`2` coordinate (`5 ≤ ℓ`) of a generator product, read off `prodIdx`. -/
theorem coord2_gen_mul (ℓ : Fin 14) (i k : Fin 4) :
    coordFun ℓ (v i * v k) = if ℓ = prodIdx i k then 1 else 0 := by
  rw [gen_mul_eq_basisMon, coordFun_basisMon]

/-- **The degree-`2` structure constant.** For `z ∈ 𝔪`, a generator `v k`, and a
degree-`2` coordinate (`5 ≤ ℓ`), `coordFun ℓ (z · v k)` is the bilinear pairing of
`d1 z` against `e_k`: only the linear part of `z` contributes (the constant part
gives a degree-`1` term, the degree-`≥2` part gives a degree-`≥3` term `= 0`). -/
theorem coord_deg2_mul (ℓ : Fin 14) (z : B) (hz : z ∈ m) (k : Fin 4) :
    coordFun ℓ (z * v k)
      = ∑ i : Fin 4, d1 z i * (if ℓ = prodIdx i k then 1 else 0) := by
  rw [mul_gen_expand z (v k), map_sum]
  -- Split the 14-term sum: j=0 (z∈𝔪 ⇒ coord0 z = 0), j∈{1..4} (the bilinear terms),
  -- j≥5 (basisMon j · v k = 0).
  have hsum : (∑ j : Fin 14, coordFun ℓ (coordFun j z • (basisMon j * v k)))
      = ∑ i : Fin 4, coordFun ℓ (coordFun ⟨i.val + 1, by omega⟩ z •
          (basisMon ⟨i.val + 1, by omega⟩ * v k)) := by
    rw [← Finset.sum_filter_add_sum_filter_not Finset.univ
        (fun j : Fin 14 => 1 ≤ j.val ∧ j.val ≤ 4)]
    have hnot : (∑ j ∈ Finset.univ.filter (fun j : Fin 14 => ¬ (1 ≤ j.val ∧ j.val ≤ 4)),
        coordFun ℓ (coordFun j z • (basisMon j * v k))) = 0 := by
      apply Finset.sum_eq_zero
      intro j hj
      rw [Finset.mem_filter] at hj
      rcases Nat.lt_or_ge j.val 1 with hj0 | hj1
      · have : j = 0 := Fin.ext (by omega)
        subst this
        rw [(mem_m_iff_coord0 z).mp hz, zero_smul, map_zero]
      · have hj5 : 5 ≤ j.val := by omega
        rw [basisMon_mul_gen_eq_zero j hj5 (v k) (v_mem_m k), smul_zero, map_zero]
    rw [hnot, add_zero]
    -- reindex the j∈{1..4} terms by i = j-1
    apply Finset.sum_nbij' (i := fun j => (⟨(j.val - 1) % 4, Nat.mod_lt _ (by omega)⟩ : Fin 4))
      (j := fun i => (⟨i.val + 1, by have := i.isLt; omega⟩ : Fin 14))
    · intro j hj; exact Finset.mem_univ _
    · intro i _; rw [Finset.mem_filter]
      have := i.isLt
      exact ⟨Finset.mem_univ _, by simp only; omega, by simp only; omega⟩
    · intro j hj; rw [Finset.mem_filter] at hj
      obtain ⟨_, h1, h2⟩ := hj
      apply Fin.ext; simp only; omega
    · intro i _; apply Fin.ext; simp only; have := i.isLt; omega
    · intro j hj; rw [Finset.mem_filter] at hj
      obtain ⟨_, h1, h2⟩ := hj
      have hidx : (⟨((j.val - 1) % 4) + 1, by have := j.isLt; omega⟩ : Fin 14) = j :=
        Fin.ext (by simp only; omega)
      rw [hidx]
  rw [hsum]
  apply Finset.sum_congr rfl
  intro i _
  rw [map_smul, smul_eq_mul]
  rw [show basisMon ⟨i.val + 1, by have := i.isLt; omega⟩ = v i from (v_eq_basisMon i).symm]
  rw [coord2_gen_mul]
  rfl

/-- The bilinear quadratic pairing on `𝔽₂⁴`: `Φ u w` is the degree-`2` coordinate
vector obtained from the products of generators, recorded by `prodIdx`. -/
def quadPair (u w : Fin 4 → ZMod 2) (ℓ : Fin 14) : ZMod 2 :=
  ∑ i : Fin 4, ∑ k : Fin 4, u i * w k * (if ℓ = prodIdx i k then 1 else 0)

/-- Degree-`2` coordinate of a degree-`2` basis monomial times `s`: only the
constant part of `s` survives (`𝔪² · 𝔪 = 0`). -/
theorem coord2_basisMon_high_mul (ℓ j : Fin 14) (hj : 5 ≤ j.val) (s : B) :
    coordFun ℓ (basisMon j * s) = coordFun 0 s * (if ℓ = j then 1 else 0) := by
  have hs'm : (s - coordFun 0 s • (1 : B)) ∈ m := by
    rw [mem_m_iff_coord0, map_sub, map_smul, smul_eq_mul, coord0_one, mul_one, sub_self]
  have hkey : basisMon j * s
      = coordFun 0 s • basisMon j + basisMon j * (s - coordFun 0 s • (1 : B)) := by
    rw [mul_sub, mul_smul_comm, mul_one]; ring
  rw [hkey, map_add, map_smul, smul_eq_mul, coordFun_basisMon,
      basisMon_mul_gen_eq_zero j hj _ hs'm, map_zero, add_zero]

/-- The constant part of `s` does not change the linear coordinates of `s`. -/
theorem d1_sub_const (s : B) : d1 (s - coordFun 0 s • (1 : B)) = d1 s := by
  funext i
  rw [d1, d1, map_sub, map_smul, smul_eq_mul,
      show (1 : B) = basisMon 0 from by rw [basisMon_eq]; rfl, coordFun_basisMon,
      if_neg (show (⟨i.val + 1, by omega⟩ : Fin 14) ≠ 0 from by
        intro h; have := congrArg Fin.val h; simp only at this; omega),
      mul_zero, sub_zero]

/-- **The degree-`2` coordinate of `v i · s`** (generator times general `s`):
the quadratic pairing of `e_i` with `d1 s`. -/
theorem coord2_deg1_mul_right (ℓ : Fin 14) (hℓ : 5 ≤ ℓ.val) (i : Fin 4) (s : B) :
    coordFun ℓ (v i * s) = ∑ k : Fin 4, d1 s k * (if ℓ = prodIdx i k then 1 else 0) := by
  have hs'm : (s - coordFun 0 s • (1 : B)) ∈ m := by
    rw [mem_m_iff_coord0, map_sub, map_smul, smul_eq_mul, coord0_one, mul_one, sub_self]
  have hkey : v i * s
      = coordFun 0 s • v i + (s - coordFun 0 s • (1 : B)) * v i := by
    rw [sub_mul, smul_mul_assoc, one_mul, add_sub_cancel, mul_comm]
  -- v i is degree 1, so coordFun ℓ (v i) = 0 for ℓ ≥ 5
  have hvi0 : coordFun ℓ (v i) = 0 := by
    rw [v_eq_basisMon, coordFun_basisMon, if_neg (by
      intro h; have := congrArg Fin.val h; simp only at this; omega)]
  rw [hkey, map_add, map_smul, smul_eq_mul, hvi0, mul_zero, zero_add,
      coord_deg2_mul ℓ _ hs'm i]
  apply Finset.sum_congr rfl
  intro k _
  rw [show d1 (s - coordFun 0 s • (1 : B)) k = d1 s k from congrArg (· k) (d1_sub_const s),
      prodIdx_symm k i]

theorem coord_deg2_mul_right (ℓ : Fin 14) (hℓ : 5 ≤ ℓ.val) (z : B) (hz : z ∈ m) (s : B) :
    coordFun ℓ (z * s)
      = coordFun 0 s * coordFun ℓ z + quadPair (d1 z) (d1 s) ℓ := by
  rw [mul_gen_expand z s, map_sum]
  -- Three-way split of Fin 14: {0} (coeff 0), {1..4} (pairing), {5..13} (junk).
  rw [← Finset.sum_filter_add_sum_filter_not Finset.univ
      (fun j : Fin 14 => 1 ≤ j.val ∧ j.val ≤ 4)]
  -- Part A: 1 ≤ j ≤ 4 gives the quadratic pairing.
  have hA : (∑ j ∈ Finset.univ.filter (fun j : Fin 14 => 1 ≤ j.val ∧ j.val ≤ 4),
      coordFun ℓ (coordFun j z • (basisMon j * s))) = quadPair (d1 z) (d1 s) ℓ := by
    rw [quadPair]
    apply Finset.sum_nbij' (i := fun j => (⟨(j.val - 1) % 4, Nat.mod_lt _ (by omega)⟩ : Fin 4))
      (j := fun i => (⟨i.val + 1, by have := i.isLt; omega⟩ : Fin 14))
    · intro j hj; exact Finset.mem_univ _
    · intro i _; rw [Finset.mem_filter]
      have := i.isLt
      exact ⟨Finset.mem_univ _, by simp only; omega, by simp only; omega⟩
    · intro j hj; rw [Finset.mem_filter] at hj
      obtain ⟨_, h1, h2⟩ := hj
      apply Fin.ext; simp only; omega
    · intro i _; apply Fin.ext; simp only; have := i.isLt; omega
    · intro j hj; rw [Finset.mem_filter] at hj
      obtain ⟨_, h1, h2⟩ := hj
      set mm : Fin 4 := ⟨(j.val - 1) % 4, Nat.mod_lt _ (by omega)⟩ with hmm
      have hjeq : j = (⟨mm.val + 1, by have := j.isLt; simp only [hmm]; omega⟩ : Fin 14) := by
        apply Fin.ext; simp only [hmm]; omega
      have hbm : basisMon j = v mm := by rw [v_eq_basisMon, hjeq]
      have hcz : coordFun j z = d1 z mm := by rw [d1, hjeq]
      rw [map_smul, smul_eq_mul, hbm, coord2_deg1_mul_right ℓ hℓ mm s, hcz, Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro k _
      ring
  -- Part B: not (1 ≤ j ≤ 4), i.e. j = 0 or j ≥ 5.
  have hB : (∑ j ∈ Finset.univ.filter (fun j : Fin 14 => ¬ (1 ≤ j.val ∧ j.val ≤ 4)),
      coordFun ℓ (coordFun j z • (basisMon j * s))) = coordFun 0 s * coordFun ℓ z := by
    have hsubset : (Finset.univ.filter (fun j : Fin 14 => ¬ (1 ≤ j.val ∧ j.val ≤ 4)))
        = insert (0 : Fin 14) (Finset.univ.filter (fun j : Fin 14 => 5 ≤ j.val)) := by
      ext j
      simp only [Finset.mem_filter, Finset.mem_univ, true_and, Finset.mem_insert]
      constructor
      · intro h; rcases Nat.eq_zero_or_pos j.val with h0 | h0
        · left; exact Fin.ext h0
        · right; omega
      · rintro (rfl | h); · decide
        · omega
    rw [hsubset, Finset.sum_insert (by
        simp only [Finset.mem_filter, Finset.mem_univ, true_and]; decide)]
    rw [(mem_m_iff_coord0 z).mp hz, zero_smul, map_zero, zero_add]
    -- the j ≥ 5 terms: coordFun ℓ (basisMon j * s) = coord0 s * [ℓ = j]
    have hstep : (∑ j ∈ Finset.univ.filter (fun j : Fin 14 => 5 ≤ j.val),
        coordFun ℓ (coordFun j z • (basisMon j * s)))
        = ∑ j ∈ Finset.univ.filter (fun j : Fin 14 => 5 ≤ j.val),
            coordFun j z * coordFun 0 s * (if ℓ = j then 1 else 0) := by
      apply Finset.sum_congr rfl
      intro j hj
      rw [Finset.mem_filter] at hj
      rw [map_smul, smul_eq_mul, coord2_basisMon_high_mul ℓ j hj.2 s]; ring
    rw [hstep]
    -- only j = ℓ survives, giving coordFun ℓ z * coord0 s
    rw [Finset.sum_eq_single ℓ]
    · rw [if_pos rfl, mul_one]; ring
    · intro j _ hjℓ; rw [if_neg (fun h => hjℓ h.symm), mul_zero]
    · intro hℓnotin
      exfalso; apply hℓnotin
      rw [Finset.mem_filter]; exact ⟨Finset.mem_univ _, hℓ⟩
  rw [hA, hB, add_comm]

/-- **The per-generator degree-`2` equation.** For `x, y, r ∈ 𝔪` with the colon
hypothesis, every degree-`2` coordinate (`5 ≤ ℓ`) of `r · v k` decomposes as the
`d1 x`- and `d1 y`-pairings plus the "junk" contributions
`(const. part of the multipliers) · (degree-2 parts of x, y)`. This is the algebraic
content the remaining rank argument runs on. -/
theorem colon2_deg2_eq (x y r : B) (hx : x ∈ m) (hy : y ∈ m)
    (h : ∀ k, r * v k ∈ (Ideal.span {x} ⊔ Ideal.span {y} : Ideal B)) (k : Fin 4) :
    ∃ sx sy : B, ∀ ℓ : Fin 14, 5 ≤ ℓ.val →
      quadPair (d1 r) (Pi.single k 1) ℓ
        = coordFun 0 sx * coordFun ℓ x + quadPair (d1 x) (d1 sx) ℓ
          + (coordFun 0 sy * coordFun ℓ y + quadPair (d1 y) (d1 sy) ℓ) := by
  obtain ⟨wx, hwx, wy, hwy, hsum⟩ := Submodule.mem_sup.mp (h k)
  rw [Ideal.mem_span_singleton] at hwx hwy
  obtain ⟨sx, rfl⟩ := hwx
  obtain ⟨sy, rfl⟩ := hwy
  refine ⟨sx, sy, fun ℓ hℓ => ?_⟩
  have hrm : r ∈ m := r_mem_m x y r hx hy h
  -- LHS = degree-2 coords of r * v k
  have hlhs : quadPair (d1 r) (Pi.single k 1) ℓ = coordFun ℓ (r * v k) := by
    rw [coord_deg2_mul ℓ r hrm k, quadPair]
    apply Finset.sum_congr rfl
    intro i _
    rw [Finset.sum_eq_single k]
    · rw [Pi.single_eq_same, mul_one]
    · intro j _ hjk; rw [Pi.single_eq_of_ne hjk, mul_zero, zero_mul]
    · intro hc; exact absurd (Finset.mem_univ _) hc
  rw [hlhs, ← hsum, map_add,
      coord_deg2_mul_right ℓ hℓ x hx sx, coord_deg2_mul_right ℓ hℓ y hy sy]

/-- **The combined per-generator equation.** Strengthens `colon2_deg2_eq` with the
degree-`1` constraint `(sx)₀ • d1 x + (sy)₀ • d1 y = 0`: since `r · v k ∈ 𝔪²` has
no linear part, the linear parts of `sx · x` and `sy · y` must cancel. This extra
constraint is what makes the rank step actually go through (the degree-`2` equation
alone is insufficient). -/
theorem colon2_full_eq (x y r : B) (hx : x ∈ m) (hy : y ∈ m)
    (h : ∀ k, r * v k ∈ (Ideal.span {x} ⊔ Ideal.span {y} : Ideal B)) (k : Fin 4) :
    ∃ sx sy : B,
      coordFun 0 sx • d1 x + coordFun 0 sy • d1 y = (0 : Fin 4 → ZMod 2) ∧
      ∀ ℓ : Fin 14, 5 ≤ ℓ.val →
        quadPair (d1 r) (Pi.single k 1) ℓ
          = coordFun 0 sx * coordFun ℓ x + quadPair (d1 x) (d1 sx) ℓ
            + (coordFun 0 sy * coordFun ℓ y + quadPair (d1 y) (d1 sy) ℓ) := by
  obtain ⟨wx, hwx, wy, hwy, hsum⟩ := Submodule.mem_sup.mp (h k)
  rw [Ideal.mem_span_singleton] at hwx hwy
  obtain ⟨sx, rfl⟩ := hwx
  obtain ⟨sy, rfl⟩ := hwy
  have hrm : r ∈ m := r_mem_m x y r hx hy h
  refine ⟨sx, sy, ?_, fun ℓ hℓ => ?_⟩
  · -- degree-1 constraint: d1 (x*sx) + d1 (y*sy) = d1 (r*v k) = 0
    funext i
    simp only [Pi.add_apply, Pi.smul_apply, smul_eq_mul, Pi.zero_apply]
    have hi1 : 1 ≤ (⟨i.val + 1, by omega⟩ : Fin 14).val := by simp
    have hi4 : (⟨i.val + 1, by omega⟩ : Fin 14).val ≤ 4 := by
      simp only; have := i.isLt; omega
    -- d1 (r * v k) i = 0 since r * v k ∈ 𝔪²
    have hrvk : r * v k ∈ m ^ 2 := by
      rw [pow_two]; exact Ideal.mul_mem_mul hrm (v_mem_m k)
    have hlin0 : coordFun ⟨i.val + 1, by omega⟩ (r * v k) = 0 :=
      coord_low_msq _ hi4 _ hrvk
    have hcong := congrArg (coordFun (⟨i.val + 1, by omega⟩ : Fin 14)) hsum
    rw [map_add, hlin0, mul_comm x sx, mul_comm y sy,
        coord_deg1_mul _ hi4 hi1 sx x hx, coord_deg1_mul _ hi4 hi1 sy y hy] at hcong
    -- hcong : 0 = coord0 sx * coordFun (i+1) x + coord0 sy * coordFun (i+1) y
    rw [d1, d1, ← hcong]
  · -- degree-2 equation, same as colon2_deg2_eq
    have hlhs : quadPair (d1 r) (Pi.single k 1) ℓ = coordFun ℓ (r * v k) := by
      rw [coord_deg2_mul ℓ r hrm k, quadPair]
      apply Finset.sum_congr rfl
      intro i _
      rw [Finset.sum_eq_single k]
      · rw [Pi.single_eq_same, mul_one]
      · intro j _ hjk; rw [Pi.single_eq_of_ne hjk, mul_zero, zero_mul]
      · intro hc; exact absurd (Finset.mem_univ _) hc
    rw [hlhs, ← hsum, map_add,
        coord_deg2_mul_right ℓ hℓ x hx sx, coord_deg2_mul_right ℓ hℓ y hy sy]

/-- **Abstract rank lower bound.** If `n` vectors `c i` are linearly independent
*modulo* `W` (no nontrivial combination lands in `W`), then adjoining their span to
`W` raises the dimension by at least `n`. Proven via the quotient `V ⧸ W`: the images
`W.mkQ (c i)` are linearly independent, so span an `n`-dimensional subspace of
`map W.mkQ (W ⊔ span (range c))`, and the quotient-dimension adds to `finrank W`. -/
theorem finrank_sup_span_ge {K V : Type*} [Field K] [AddCommGroup V] [Module K V]
    [FiniteDimensional K V] (W : Submodule K V) (n : ℕ) (c : Fin n → V)
    (hc : ∀ a : Fin n → K, (∑ i, a i • c i) ∈ W → a = 0) :
    Module.finrank K W + n ≤
      Module.finrank K (W ⊔ Submodule.span K (Set.range c) : Submodule K V) := by
  classical
  set U : Submodule K V := W ⊔ Submodule.span K (Set.range c) with hU
  have hWU : W ≤ U := le_sup_left
  -- images of c in the quotient U ⧸ (W viewed in U) are linearly independent
  -- Work with the quotient map of V by W, restricted in range to U.
  set q := W.mkQ
  have hqc : LinearIndependent K (fun i => q (c i)) := by
    rw [Fintype.linearIndependent_iff]
    intro a ha i
    have hmem : (∑ i, a i • c i) ∈ W := by
      have hz : q (∑ i, a i • c i) = 0 := by
        rw [map_sum]; simp only [map_smul]; exact ha
      rwa [← LinearMap.mem_ker, Submodule.ker_mkQ] at hz
    have := hc a hmem
    exact congrFun this i
  -- finrank of span of the images = n
  have hspan : Module.finrank K (Submodule.span K (Set.range (fun i => q (c i)))) = n := by
    rw [finrank_span_eq_card hqc, Fintype.card_fin]
  -- span (range (q ∘ c)) = map q (span (range c)) ≤ map q U
  have hle : Submodule.span K (Set.range (fun i => q (c i)))
      ≤ Submodule.map q U := by
    have hrw : Set.range (fun i => q (c i)) = q '' Set.range c :=
      (Set.range_comp q c).symm ▸ rfl
    rw [hrw, ← Submodule.map_span]
    apply Submodule.map_mono
    exact le_sup_right
  have hmono : Module.finrank K (Submodule.span K (Set.range (fun i => q (c i))))
      ≤ Module.finrank K (Submodule.map q U) := Submodule.finrank_mono hle
  rw [hspan] at hmono
  -- map q U = range of (q restricted to U); rank-nullity over U gives the bound.
  set f : U →ₗ[K] (V ⧸ W) := q.domRestrict U with hf
  have hrange : LinearMap.range f = Submodule.map q U := by
    rw [hf, LinearMap.range_domRestrict]
  have hker : Module.finrank K (LinearMap.ker f) = Module.finrank K (W ⊓ U : Submodule K V) := by
    -- ker f = (W ⊓ U) as a submodule of U; map by U.subtype to compare ranks
    have hkermap : (LinearMap.ker f).map U.subtype = (W ⊓ U : Submodule K V) := by
      rw [hf]
      ext z
      simp only [Submodule.mem_map, LinearMap.mem_ker, LinearMap.domRestrict_apply,
        Submodule.coe_subtype, Submodule.mem_inf]
      constructor
      · rintro ⟨w, hw, rfl⟩
        exact ⟨by rwa [← LinearMap.mem_ker, Submodule.ker_mkQ] at hw, w.2⟩
      · rintro ⟨hzW, hzU⟩
        refine ⟨⟨z, hzU⟩, ?_, rfl⟩
        rwa [← LinearMap.mem_ker, Submodule.ker_mkQ]
    rw [← Submodule.finrank_map_subtype_eq, hkermap]
  have hranknull := LinearMap.finrank_range_add_finrank_ker f
  rw [hrange, hker, inf_eq_left.mpr hWU] at hranknull
  -- hranknull : finrank (map q U) + finrank W = finrank U
  omega

/-- The degree-`2` "column" of the quadratic pairing: `Phi u k ℓ` reads the
degree-`2` coordinate `ℓ + 5` of `quadPair u e_k`, reindexing the `9` degree-`2`
coordinates `{5,…,13}` to `Fin 9`. -/
def Phi (u : Fin 4 → ZMod 2) (k : Fin 4) : Fin 9 → ZMod 2 :=
  fun ℓ => quadPair u (Pi.single k 1) ⟨ℓ.val + 5, by have := ℓ.isLt; omega⟩

/-- `quadPair` is symmetric (`prodIdx` is symmetric). -/
theorem quadPair_symm (u w : Fin 4 → ZMod 2) (ℓ : Fin 14) :
    quadPair u w ℓ = quadPair w u ℓ := by
  rw [quadPair, quadPair, Finset.sum_comm]
  apply Finset.sum_congr rfl; intro i _
  apply Finset.sum_congr rfl; intro k _
  rw [prodIdx_symm]; ring

/-- `quadPair` is additive in its second argument. -/
theorem quadPair_add_right (u w₁ w₂ : Fin 4 → ZMod 2) (ℓ : Fin 14) :
    quadPair u (w₁ + w₂) ℓ = quadPair u w₁ ℓ + quadPair u w₂ ℓ := by
  simp only [quadPair, ← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl; intro i _
  apply Finset.sum_congr rfl; intro k _
  simp only [Pi.add_apply]; ring

/-- `quadPair u e_k ℓ` picks out the `i`-sum at column `k`. -/
theorem quadPair_single (u : Fin 4 → ZMod 2) (k : Fin 4) (ℓ : Fin 14) :
    quadPair u (Pi.single k 1) ℓ = ∑ i : Fin 4, u i * (if ℓ = prodIdx i k then 1 else 0) := by
  rw [quadPair]
  apply Finset.sum_congr rfl; intro i _
  rw [Finset.sum_eq_single k]
  · rw [Pi.single_eq_same, mul_one]
  · intro j _ hjk; rw [Pi.single_eq_of_ne hjk, mul_zero, zero_mul]
  · intro hc; exact absurd (Finset.mem_univ _) hc

/-- **Column expansion.** `quadPair u w`, on the degree-`2` block, is the
`w`-combination of the columns `Phi u j`: `Phi`-as-a-function is `𝔽₂`-linear in `w`. -/
theorem quadPair_eq_sum_Phi (u w : Fin 4 → ZMod 2) (ℓ : Fin 9) :
    quadPair u w ⟨ℓ.val + 5, by have := ℓ.isLt; omega⟩ = ∑ j : Fin 4, w j • Phi u j ℓ := by
  set ℓ' : Fin 14 := ⟨ℓ.val + 5, by have := ℓ.isLt; omega⟩ with hℓ'
  have hcol : ∀ j, Phi u j ℓ = ∑ i : Fin 4, u i * (if ℓ' = prodIdx i j then 1 else 0) := by
    intro j; rw [Phi, quadPair_single]
  simp only [hcol, smul_eq_mul, Finset.mul_sum]
  rw [quadPair]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl; intro j _
  apply Finset.sum_congr rfl; intro i _
  ring

/-- The degree-`2` coordinate vector of `z : B`, reindexed `{5,…,13} → Fin 9`. -/
noncomputable def d2 (z : B) : Fin 9 → ZMod 2 :=
  fun ℓ => coordFun ⟨ℓ.val + 5, by have := ℓ.isLt; omega⟩ z

/-- **Bridge translation.** For each generator index `k`, the column `Phi (d1 r) k`
decomposes as: a junk part `cx • d2 x + cy • d2 y` (with `cx • d1 x + cy • d1 y = 0`
from the degree-`1` constraint) plus a `W`-part (a combination of the columns
`Phi (d1 x) j` and `Phi (d1 y) j`). -/
theorem Phi_R_decomp (x y r : B) (hx : x ∈ m) (hy : y ∈ m)
    (h : ∀ k, r * v k ∈ (Ideal.span {x} ⊔ Ideal.span {y} : Ideal B)) (k : Fin 4) :
    ∃ (cx cy : ZMod 2) (dx dy : Fin 4 → ZMod 2),
      cx • d1 x + cy • d1 y = (0 : Fin 4 → ZMod 2) ∧
      Phi (d1 r) k =
        (cx • d2 x + cy • d2 y)
          + ((∑ j, dx j • Phi (d1 x) j) + (∑ j, dy j • Phi (d1 y) j)) := by
  obtain ⟨sx, sy, hdeg1, hdeg2⟩ := colon2_full_eq x y r hx hy h k
  refine ⟨coordFun 0 sx, coordFun 0 sy, d1 sx, d1 sy, hdeg1, ?_⟩
  funext ℓ
  have hℓ5 : 5 ≤ (⟨ℓ.val + 5, by have := ℓ.isLt; omega⟩ : Fin 14).val := by simp
  have heq := hdeg2 ⟨ℓ.val + 5, by have := ℓ.isLt; omega⟩ hℓ5
  -- heq : Phi (d1 r) k ℓ = cx * coordFun ℓ+5 x + quadPair (d1 x)(d1 sx) (ℓ+5)
  --        + (cy * coordFun ℓ+5 y + quadPair (d1 y)(d1 sy)(ℓ+5))
  simp only [Pi.add_apply, Pi.smul_apply, smul_eq_mul, Finset.sum_apply]
  rw [Phi]
  rw [heq, d2, d2]
  rw [quadPair_eq_sum_Phi (d1 x) (d1 sx) ℓ, quadPair_eq_sum_Phi (d1 y) (d1 sy) ℓ]
  simp only [smul_eq_mul]
  ring

/-- The eight generators of `W = colSpace(d1 x) ⊔ colSpace(d1 y)`. -/
def colGens (X Y : Fin 4 → ZMod 2) : Fin 8 → (Fin 9 → ZMod 2) :=
  fun j => if hj : j.val < 4 then Phi X ⟨j.val, hj⟩ else Phi Y ⟨j.val - 4, by have := j.isLt; omega⟩

/-- The two raw junk directions `d2 x`, `d2 y`. -/
theorem Phi_R_mem_sup (x y r : B) (hx : x ∈ m) (hy : y ∈ m)
    (h : ∀ k, r * v k ∈ (Ideal.span {x} ⊔ Ideal.span {y} : Ideal B)) (k : Fin 4) :
    Phi (d1 r) k ∈
      (Submodule.span (ZMod 2) (Set.range (colGens (d1 x) (d1 y)))
        ⊔ Submodule.span (ZMod 2) {d2 x, d2 y} : Submodule (ZMod 2) (Fin 9 → ZMod 2)) := by
  obtain ⟨cx, cy, dx, dy, _hc, hdecomp⟩ := Phi_R_decomp x y r hx hy h k
  rw [hdecomp]
  apply Submodule.add_mem
  · apply Submodule.mem_sup_right
    apply Submodule.add_mem
    · exact Submodule.smul_mem _ _ (Submodule.subset_span (by left; rfl))
    · exact Submodule.smul_mem _ _ (Submodule.subset_span (by right; rfl))
  · apply Submodule.mem_sup_left
    apply Submodule.add_mem
    · apply Submodule.sum_mem; intro j _
      apply Submodule.smul_mem
      have hmem : Phi (d1 x) j
          = colGens (d1 x) (d1 y) ⟨j.val, by have := j.isLt; omega⟩ := by
        have hlt : ((⟨j.val, by have := j.isLt; omega⟩ : Fin 8).val < 4) := by
          simp only; exact j.isLt
        simp only [colGens, hlt, dif_pos]
      rw [hmem]
      exact Submodule.subset_span (Set.mem_range_self _)
    · apply Submodule.sum_mem; intro j _
      apply Submodule.smul_mem
      have hmem : Phi (d1 y) j
          = colGens (d1 x) (d1 y) ⟨j.val + 4, by have := j.isLt; omega⟩ := by
        have hlt : ¬ ((⟨j.val + 4, by have := j.isLt; omega⟩ : Fin 8).val < 4) := by
          simp only; omega
        simp only [colGens, hlt, dif_neg, not_false_iff, Nat.add_sub_cancel, Fin.eta]
      rw [hmem]
      exact Submodule.subset_span (Set.mem_range_self _)




/-! Nat bitmask model + bridge -/
def pidxN : Nat → Nat → Nat
| 0,0=>0|0,1=>1|0,2=>2|0,3=>3|1,0=>1|1,1=>4|1,2=>3|1,3=>5
| 2,0=>2|2,1=>3|2,2=>6|2,3=>7|3,0=>3|3,1=>5|3,2=>7|3,3=>8|_,_=>0
def bitN (n i : Nat) : Bool := (n / 2^i) % 2 == 1
def PhiCol (u k : Nat) : Nat :=
  (List.range 4).foldl (fun acc i => if bitN u i then acc ^^^ (2^(pidxN i k)) else acc) 0
def colGN (X Y : Nat) (j : Fin 8) : Nat := if j.val < 4 then PhiCol X j.val else PhiCol Y (j.val-4)
def fmaskN {n : Nat} (gN : Fin n → Nat) (mask : Nat) : Nat :=
  (List.finRange n).foldl (fun acc j => if bitN mask j.val then acc ^^^ gN j else acc) 0
def inSpanF (X Y col : Nat) : Bool :=
  (List.range 256).any (fun mask => fmaskN (colGN X Y) mask == col)
def colsIn (X Y R : Nat) : Bool := (List.range 4).all (fun k => inSpanF X Y (PhiCol R k))
def sp2N (X Y R : Nat) : Bool := R==0||R==X||R==Y||R==(X^^^Y)
def indepN (X Y : Nat) : Bool := X≠0&&Y≠0&&X≠Y

def toN4 (u : Fin 4 → ZMod 2) : Nat := ∑ i : Fin 4, (if u i = 1 then 2^i.val else 0)
def toN8 (c : Fin 8 → ZMod 2) : Nat := ∑ i : Fin 8, (if c i = 1 then 2^i.val else 0)
def toN9 (c : Fin 9 → ZMod 2) : Nat := ∑ i : Fin 9, (if c i = 1 then 2^i.val else 0)
def nxorN (a b : Nat) : Nat := a ^^^ b
instance : Std.Commutative nxorN := ⟨Nat.xor_comm⟩
instance : Std.Associative nxorN := ⟨Nat.xor_assoc⟩

set_option maxHeartbeats 4000000 in
-- Kernel `decide` over the finite `𝔽₂`-coordinate model (bitmask/quadratic-pairing
-- enumeration) needs a raised heartbeat and recursion budget.
set_option maxRecDepth 10000 in
theorem bitN_toN9 :
    ∀ (c : Fin 9 → ZMod 2) (ℓ : Fin 9), bitN (toN9 c) ℓ.val = decide (c ℓ = 1) := by
  decide
set_option maxHeartbeats 4000000 in
-- Kernel `decide` over the finite `𝔽₂`-coordinate model (bitmask/quadratic-pairing
-- enumeration) needs a raised heartbeat and recursion budget.
set_option maxRecDepth 10000 in
theorem bitN_toN8 :
    ∀ (c : Fin 8 → ZMod 2) (j : Fin 8), bitN (toN8 c) j.val = decide (c j = 1) := by decide
set_option maxHeartbeats 4000000 in
-- Kernel `decide` over the finite `𝔽₂`-coordinate model (bitmask/quadratic-pairing
-- enumeration) needs a raised heartbeat and recursion budget.
set_option maxRecDepth 10000 in
theorem bitN_toN4 :
    ∀ (u : Fin 4 → ZMod 2) (i : Fin 4), bitN (toN4 u) i.val = decide (u i = 1) := by decide
set_option maxHeartbeats 4000000 in
-- Kernel `decide` over the finite `𝔽₂`-coordinate model (bitmask/quadratic-pairing
-- enumeration) needs a raised heartbeat and recursion budget.
set_option maxRecDepth 10000 in
theorem toN9_lt (c : Fin 9 → ZMod 2) : toN9 c < 2^9 := by revert c; decide
set_option maxHeartbeats 4000000 in
-- Kernel `decide` over the finite `𝔽₂`-coordinate model (bitmask/quadratic-pairing
-- enumeration) needs a raised heartbeat and recursion budget.
set_option maxRecDepth 10000 in
theorem toN4_lt (u : Fin 4 → ZMod 2) : toN4 u < 16 := by revert u; decide
set_option maxHeartbeats 4000000 in
-- Kernel `decide` over the finite `𝔽₂`-coordinate model (bitmask/quadratic-pairing
-- enumeration) needs a raised heartbeat and recursion budget.
set_option maxRecDepth 10000 in
theorem toN9_inj : Function.Injective toN9 := by
  intro a b hab; funext i
  have ha := bitN_toN9 a i; have hb := bitN_toN9 b i
  rw [hab] at ha; rw [ha] at hb; revert hb; revert i; revert a b; decide
set_option maxHeartbeats 4000000 in
-- Kernel `decide` over the finite `𝔽₂`-coordinate model (bitmask/quadratic-pairing
-- enumeration) needs a raised heartbeat and recursion budget.
set_option maxRecDepth 10000 in
theorem toN4_inj : Function.Injective toN4 := by
  intro a b hab; funext i
  have ha := bitN_toN4 a i; have hb := bitN_toN4 b i
  rw [hab] at ha; rw [ha] at hb; revert hb; revert i; revert a b; decide
theorem bitN_toN9_high (c : Fin 9 → ZMod 2) (ℓ : Nat) (h : 9 ≤ ℓ) :
    bitN (toN9 c) ℓ = false := by
  have hb := toN9_lt c; unfold bitN
  have : toN9 c / 2^ℓ = 0 :=
    Nat.div_eq_of_lt (lt_of_lt_of_le hb (Nat.pow_le_pow_right (by norm_num) h))
  rw [this]; rfl
theorem bitN_eq_testBit (n i : Nat) : bitN n i = n.testBit i := by
  unfold bitN; rw [Nat.testBit, Nat.shiftRight_eq_div_pow]
  rcases Nat.even_or_odd (n / 2^i) with hh | hh
  · rw [Nat.even_iff] at hh; simp [hh]
  · rw [Nat.odd_iff] at hh; simp [hh]
set_option maxHeartbeats 4000000 in
-- Kernel `decide` over the finite `𝔽₂`-coordinate model (bitmask/quadratic-pairing
-- enumeration) needs a raised heartbeat and recursion budget.
set_option maxRecDepth 10000 in
theorem zmod2_add_one (x y : ZMod 2) : decide (x + y = 1) = (decide (x = 1) ^^ decide (y = 1)) := by
  revert x y; decide
set_option maxHeartbeats 4000000 in
-- Kernel `decide` over the finite `𝔽₂`-coordinate model (bitmask/quadratic-pairing
-- enumeration) needs a raised heartbeat and recursion budget.
set_option maxRecDepth 10000 in
theorem toN9_zero : toN9 (0 : Fin 9 → ZMod 2) = 0 := by decide
theorem toN9_add (a b : Fin 9 → ZMod 2) : toN9 (a + b) = toN9 a ^^^ toN9 b := by
  apply Nat.eq_of_testBit_eq; intro i
  rw [← bitN_eq_testBit, Nat.testBit_xor, ← bitN_eq_testBit, ← bitN_eq_testBit]
  rcases Nat.lt_or_ge i 9 with hi | hi
  · rw [bitN_toN9 _ ⟨i,hi⟩, bitN_toN9 _ ⟨i,hi⟩, bitN_toN9 _ ⟨i,hi⟩]
    simp only [Pi.add_apply]; rw [zmod2_add_one]
  · rw [bitN_toN9_high _ _ hi, bitN_toN9_high _ _ hi, bitN_toN9_high _ _ hi]; rfl
theorem ite_eq_smul (c : ZMod 2) (v : Fin 9 → ZMod 2) :
    (if c = 1 then v else 0) = c • v := by
  have : c = 0 ∨ c = 1 := by revert c; decide
  rcases this with h | h <;> subst h
  · rw [if_neg (by decide), zero_smul]
  · rw [if_pos rfl, one_smul]
theorem foldl_xor_acc {α : Type*} (l : List α) (p : α → Bool) (vv : α → Nat) (b : Nat) :
    l.foldl (fun acc j => if p j then acc ^^^ vv j else acc) b
    = b ^^^ l.foldl (fun acc j => if p j then acc ^^^ vv j else acc) 0 := by
  induction l generalizing b with
  | nil => simp
  | cons a t ih =>
    rw [List.foldl_cons, List.foldl_cons, ih, ih (if p a then 0 ^^^ vv a else 0)]
    split_ifs with h <;> simp [Nat.xor_assoc, Nat.zero_xor]
theorem fmask_toN9 (n : Nat) (g : Fin n → Fin 9 → ZMod 2) (p : Fin n → Bool) :
    (List.finRange n).foldl (fun acc j => if p j then acc ^^^ toN9 (g j) else acc) 0
    = toN9 (∑ j : Fin n, (if p j then g j else 0)) := by
  induction n with
  | zero => simp [toN9_zero]
  | succ m ih =>
    rw [List.finRange_succ, List.foldl_cons, foldl_xor_acc, List.foldl_map, Fin.sum_univ_succ,
      toN9_add]
    rw [ih (fun j => g j.succ) (fun j => p j.succ)]
    by_cases h : p 0
    · simp only [h, if_true]; rw [Nat.zero_xor, Nat.xor_comm]
    · simp only [h, Bool.false_eq_true, if_false, toN9_zero]

/-! PhiCol bridge + colGN bridge + membership bridge -/
set_option maxHeartbeats 4000000 in
-- Kernel `decide` over the finite `𝔽₂`-coordinate model (bitmask/quadratic-pairing
-- enumeration) needs a raised heartbeat and recursion budget.
set_option maxRecDepth 10000 in
theorem PhiCol_bridge : ∀ u : Fin 4 → ZMod 2, ∀ k : Fin 4, ∀ ℓ : Fin 9,
    bitN (PhiCol (toN4 u) k.val) ℓ.val = decide (Phi u k ℓ = 1) := by decide
set_option maxHeartbeats 4000000 in
-- Kernel `decide` over the finite `𝔽₂`-coordinate model (bitmask/quadratic-pairing
-- enumeration) needs a raised heartbeat and recursion budget.
set_option maxRecDepth 10000 in
theorem PhiCol_lt : ∀ (X : Fin 16) (k : Fin 4), PhiCol X.val k.val < 2^9 := by decide
set_option maxHeartbeats 4000000 in
-- The membership/`PhiCol` bridge unfolds the bitmask `toN9`/`fmaskN` model, which is
-- whnf-heavy and needs a raised heartbeat budget.
theorem PhiCol_toN9 (u : Fin 4 → ZMod 2) (k : Fin 4) :
    PhiCol (toN4 u) k.val = toN9 (Phi u k) := by
  apply Nat.eq_of_testBit_eq; intro i
  rw [← bitN_eq_testBit, ← bitN_eq_testBit]
  rcases Nat.lt_or_ge i 9 with hi | hi
  · rw [PhiCol_bridge u k ⟨i,hi⟩, bitN_toN9 _ ⟨i,hi⟩]
  · rw [bitN_toN9_high _ _ hi]
    have hlt : PhiCol (toN4 u) k.val < 2^9 := PhiCol_lt ⟨toN4 u, toN4_lt u⟩ k
    unfold bitN
    have : PhiCol (toN4 u) k.val / 2^i = 0 :=
      Nat.div_eq_of_lt (lt_of_lt_of_le hlt (Nat.pow_le_pow_right (by norm_num) hi))
    rw [this]; rfl
-- colGN (toN4 X)(toN4 Y) j = toN9 (colGens X Y j)
theorem colGN_toN9 (X Y : Fin 4 → ZMod 2) (j : Fin 8) :
    colGN (toN4 X) (toN4 Y) j = toN9 (colGens X Y j) := by
  unfold colGN colGens
  by_cases hj : j.val < 4
  · rw [dif_pos hj, if_pos hj]; exact PhiCol_toN9 X ⟨j.val, hj⟩
  · rw [dif_neg hj, if_neg hj]; exact PhiCol_toN9 Y ⟨j.val - 4, by have := j.isLt; omega⟩

/-! membership bridge -/
set_option maxHeartbeats 4000000 in
-- Kernel `decide` over the finite `𝔽₂`-coordinate model (bitmask/quadratic-pairing
-- enumeration) needs a raised heartbeat and recursion budget.
set_option maxRecDepth 10000 in
theorem toN8_lt (c : Fin 8 → ZMod 2) : toN8 c < 256 := by revert c; decide
set_option maxHeartbeats 4000000 in
-- The membership/`PhiCol` bridge unfolds the bitmask `toN9`/`fmaskN` model, which is
-- whnf-heavy and needs a raised heartbeat budget.
theorem inSpanF_of_mem (X Y : Fin 4 → ZMod 2) (col : Fin 9 → ZMod 2)
    (hmem : col ∈ Submodule.span (ZMod 2) (Set.range (colGens X Y))) :
    inSpanF (toN4 X) (toN4 Y) (toN9 col) = true := by
  rw [Submodule.mem_span_range_iff_exists_fun] at hmem
  obtain ⟨c, hc⟩ := hmem
  -- mask from c
  set mask := toN8 c with hmask
  unfold inSpanF
  rw [List.any_eq_true]
  refine ⟨mask, ?_, ?_⟩
  · simp only [List.mem_range]; exact toN8_lt c
  · rw [beq_iff_eq]
    -- fmaskN (colGN X Y) mask = toN9 col
    unfold fmaskN
    -- rewrite colGN to toN9 (colGens X Y j)
    have hgr : ∀ j : Fin 8, colGN (toN4 X) (toN4 Y) j = toN9 (colGens X Y j) := colGN_toN9 X Y
    rw [show (fun acc (j : Fin 8) =>
            if bitN mask j.val then acc ^^^ colGN (toN4 X) (toN4 Y) j else acc)
          = (fun acc (j : Fin 8) =>
            if bitN mask j.val then acc ^^^ toN9 (colGens X Y j) else acc) from by
      funext acc j; rw [hgr]]
    rw [fmask_toN9 8 (colGens X Y) (fun j => bitN mask j.val)]
    congr 1
    rw [← hc]
    apply Finset.sum_congr rfl
    intro j _
    simp only [hmask, bitN_toN8]
    have hcj : c j = 0 ∨ c j = 1 := by
      have : ∀ z : ZMod 2, z = 0 ∨ z = 1 := by decide
      exact this (c j)
    rcases hcj with h | h <;> rw [h]
    · rw [zero_smul]; rfl
    · rw [one_smul]; rfl

/-! the core decide (independent case) -/
set_option maxHeartbeats 4000000 in
-- Kernel `decide` over the finite `𝔽₂`-coordinate model (bitmask/quadratic-pairing
-- enumeration) needs a raised heartbeat and recursion budget.
set_option maxRecDepth 10000 in
theorem uniform : ∀ X : Fin 16, ∀ Y : Fin 16, ∀ R : Fin 16,
    indepN X.val Y.val = true → colsIn X.val Y.val R.val = true →
    sp2N X.val Y.val R.val = true := by
  decide

/-! back-bridges for hypotheses & conclusion -/
-- colsIn from per-column membership
set_option maxHeartbeats 4000000 in
-- The membership/`PhiCol` bridge unfolds the bitmask `toN9`/`fmaskN` model, which is
-- whnf-heavy and needs a raised heartbeat budget.
theorem colsIn_of_mem (X Y R : Fin 4 → ZMod 2)
    (h : ∀ k, Phi R k ∈ Submodule.span (ZMod 2) (Set.range (colGens X Y))) :
    colsIn (toN4 X) (toN4 Y) (toN4 R) = true := by
  unfold colsIn
  rw [List.all_eq_true]
  intro k hk
  simp only [List.mem_range] at hk
  rw [PhiCol_toN9 R ⟨k, hk⟩]
  exact inSpanF_of_mem X Y (Phi R ⟨k,hk⟩) (h ⟨k,hk⟩)

-- toN4 add bridge
theorem bitN_toN4_high (u : Fin 4 → ZMod 2) (i : Nat) (h : 4 ≤ i) :
    bitN (toN4 u) i = false := by
  have hb := toN4_lt u; unfold bitN
  have : toN4 u / 2^i = 0 := Nat.div_eq_of_lt (lt_of_lt_of_le hb (by
    calc (16:Nat) = 2^4 := by norm_num
    _ ≤ 2^i := Nat.pow_le_pow_right (by norm_num) h))
  rw [this]; rfl
theorem toN4_add (a b : Fin 4 → ZMod 2) : toN4 (a + b) = toN4 a ^^^ toN4 b := by
  apply Nat.eq_of_testBit_eq; intro i
  rw [← bitN_eq_testBit, Nat.testBit_xor, ← bitN_eq_testBit, ← bitN_eq_testBit]
  rcases Nat.lt_or_ge i 4 with hi | hi
  · rw [bitN_toN4 _ ⟨i,hi⟩, bitN_toN4 _ ⟨i,hi⟩, bitN_toN4 _ ⟨i,hi⟩]
    simp only [Pi.add_apply]; rw [zmod2_add_one]
  · rw [bitN_toN4_high _ _ hi, bitN_toN4_high _ _ hi, bitN_toN4_high _ _ hi]; rfl
set_option maxHeartbeats 4000000 in
-- Kernel `decide` over the finite `𝔽₂`-coordinate model (bitmask/quadratic-pairing
-- enumeration) needs a raised heartbeat and recursion budget.
set_option maxRecDepth 10000 in
theorem toN4_zero : toN4 (0 : Fin 4 → ZMod 2) = 0 := by decide

-- sp2N back-bridge: gives ∃ α β
theorem exists_of_sp2N (X Y R : Fin 4 → ZMod 2) (h : sp2N (toN4 X) (toN4 Y) (toN4 R) = true) :
    ∃ α β : ZMod 2, R = α • X + β • Y := by
  unfold sp2N at h
  simp only [Bool.or_eq_true, beq_iff_eq] at h
  rcases h with ((h | h) | h) | h
  · refine ⟨0, 0, ?_⟩
    have : toN4 R = toN4 (0 : Fin 4 → ZMod 2) := by rw [h, toN4_zero]
    have := toN4_inj this; rw [this]; simp
  · refine ⟨1, 0, ?_⟩
    have := toN4_inj h; rw [this]; simp
  · refine ⟨0, 1, ?_⟩
    have := toN4_inj h; rw [this]; simp
  · refine ⟨1, 1, ?_⟩
    have hxy : toN4 R = toN4 (X + Y) := by rw [h, toN4_add]
    have := toN4_inj hxy; rw [this]; simp

/-! independence bridges -/
-- linear independence of d1x,d1y → indepN
theorem indepN_of_indep (X Y : Fin 4 → ZMod 2)
    (h : ∀ a b : ZMod 2, a • X + b • Y = 0 → a = 0 ∧ b = 0) :
    indepN (toN4 X) (toN4 Y) = true := by
  unfold indepN
  have hX : X ≠ 0 := by intro hX0; have := (h 1 0 (by rw [hX0]; simp)).1; simp at this
  have hY : Y ≠ 0 := by intro hY0; have := (h 0 1 (by rw [hY0]; simp)).2; simp at this
  have hXY : X ≠ Y := by
    intro hXYeq
    have hz : (1:ZMod 2) • X + (1:ZMod 2) • Y = 0 := by
      rw [hXYeq, one_smul]; ext i
      simp only [Pi.add_apply, Pi.zero_apply]
      have h2 : ∀ z : ZMod 2, z + z = 0 := by decide
      exact h2 _
    have := (h 1 1 hz).1; simp at this
  have hnX : toN4 X ≠ 0 := fun hc => hX (toN4_inj (by rw [hc, toN4_zero]))
  have hnY : toN4 Y ≠ 0 := fun hc => hY (toN4_inj (by rw [hc, toN4_zero]))
  have hnXY : toN4 X ≠ toN4 Y := fun hc => hXY (toN4_inj hc)
  simp only [Bool.and_eq_true, ne_eq, decide_eq_true_eq]
  exact ⟨⟨hnX, hnY⟩, hnXY⟩

-- the independent case core
theorem core_indep (x y r : B) (hx : x ∈ m) (hy : y ∈ m)
    (h : ∀ k, r * v k ∈ (Ideal.span {x} ⊔ Ideal.span {y} : Ideal B))
    (hindep : ∀ a b : ZMod 2, a • d1 x + b • d1 y = 0 → a = 0 ∧ b = 0) :
    ∃ α β : ZMod 2, d1 r = α • d1 x + β • d1 y := by
  -- each column in span(colGens)
  have hcol : ∀ k,
      Phi (d1 r) k ∈ Submodule.span (ZMod 2) (Set.range (colGens (d1 x) (d1 y))) := by
    intro k
    obtain ⟨cx, cy, dx, dy, hcc, hdecomp⟩ := Phi_R_decomp x y r hx hy h k
    have hcx : cx = 0 := (hindep cx cy hcc).1
    have hcy : cy = 0 := (hindep cx cy hcc).2
    rw [hdecomp, hcx, hcy, zero_smul, zero_smul, add_zero, zero_add]
    apply Submodule.add_mem
    · apply Submodule.sum_mem; intro j _
      apply Submodule.smul_mem
      have hmem : Phi (d1 x) j = colGens (d1 x) (d1 y) ⟨j.val, by have := j.isLt; omega⟩ := by
        have hlt : ((⟨j.val, by have := j.isLt; omega⟩ : Fin 8).val < 4) := by
          simp only; exact j.isLt
        simp only [colGens, hlt, dif_pos]
      rw [hmem]; exact Submodule.subset_span (Set.mem_range_self _)
    · apply Submodule.sum_mem; intro j _
      apply Submodule.smul_mem
      have hmem : Phi (d1 y) j
          = colGens (d1 x) (d1 y) ⟨j.val + 4, by have := j.isLt; omega⟩ := by
        have hlt : ¬ ((⟨j.val + 4, by have := j.isLt; omega⟩ : Fin 8).val < 4) := by
          simp only; omega
        simp only [colGens]
        rw [dif_neg hlt]
        simp only [Nat.add_sub_cancel, Fin.eta]
      rw [hmem]; exact Submodule.subset_span (Set.mem_range_self _)
  have hcolsIn := colsIn_of_mem (d1 x) (d1 y) (d1 r) hcol
  have hindN := indepN_of_indep (d1 x) (d1 y) hindep
  have huni := uniform ⟨toN4 (d1 x), toN4_lt _⟩ ⟨toN4 (d1 y), toN4_lt _⟩
    ⟨toN4 (d1 r), toN4_lt _⟩ hindN hcolsIn
  exact exists_of_sp2N (d1 x) (d1 y) (d1 r) huni



set_option maxHeartbeats 4000000 in
-- Kernel `decide` over the finite `𝔽₂`-coordinate model (bitmask/quadratic-pairing
-- enumeration) needs a raised heartbeat and recursion budget.
set_option maxRecDepth 10000 in
theorem Phi_cols_indep (U : Fin 4 → ZMod 2) (hU : U ≠ 0) :
    LinearIndependent (ZMod 2) (Phi U) := by
  rw [Fintype.linearIndependent_iff]; revert hU; revert U; decide

def colSp (U : Fin 4 → ZMod 2) : Submodule (ZMod 2) (Fin 9 → ZMod 2) :=
  Submodule.span (ZMod 2) (Set.range (Phi U))

theorem finrank_colSp (U : Fin 4 → ZMod 2) (hU : U ≠ 0) :
    Module.finrank (ZMod 2) (colSp U) = 4 := by
  unfold colSp
  rw [finrank_span_eq_card (Phi_cols_indep U hU), Fintype.card_fin]

-- colSpaceMem decidable predicate (for factB)
def csMem (U : Fin 4 → ZMod 2) (c : Fin 9 → ZMod 2) : Prop :=
  ∃ a : Fin 4 → ZMod 2, c = ∑ j, a j • Phi U j
instance : ∀ U c, Decidable (csMem U c) := fun _ _ => Fintype.decidableExistsFintype

-- csMem ↔ ∈ colSp
theorem csMem_iff (U : Fin 4 → ZMod 2) (c : Fin 9 → ZMod 2) : csMem U c ↔ c ∈ colSp U := by
  unfold csMem colSp
  rw [Submodule.mem_span_range_iff_exists_fun]
  constructor
  · rintro ⟨a, rfl⟩; exact ⟨a, rfl⟩
  · rintro ⟨a, ha⟩; exact ⟨a, ha.symm⟩

def sp1P (U R : Fin 4 → ZMod 2) : Prop := ∃ a : ZMod 2, R = a • U
instance : ∀ U R, Decidable (sp1P U R) := fun _ _ => Fintype.decidableExistsFintype

set_option maxHeartbeats 4000000 in
-- Kernel `decide` over the finite `𝔽₂`-coordinate model (bitmask/quadratic-pairing
-- enumeration) needs a raised heartbeat and recursion budget.
set_option maxRecDepth 10000 in
theorem factB : ∀ U R : Fin 4 → ZMod 2, U ≠ 0 → ¬ sp1P U R →
    ∃ k1 k2 : Fin 4, k1 ≠ k2 ∧ ¬ csMem U (Phi R k1) ∧ ¬ csMem U (Phi R k2)
      ∧ ¬ csMem U (Phi R k1 + Phi R k2) := by
  decide
-- dependent core via finrank
theorem dep_core (U R : Fin 4 → ZMod 2) (w : Fin 9 → ZMod 2) (hU : U ≠ 0)
    (hcol : ∀ k, Phi R k ∈
      (colSp U ⊔ Submodule.span (ZMod 2) {w} : Submodule (ZMod 2) (Fin 9 → ZMod 2))) :
    sp1P U R := by
  by_contra hnot
  obtain ⟨k1, k2, hk12, hm1, hm2, hm12⟩ := factB U R hU hnot
  -- colSp R ⊆ colSp U ⊔ span{w}
  set W := colSp U with hW
  set Uw := (W ⊔ Submodule.span (ZMod 2) {w} : Submodule (ZMod 2) (Fin 9 → ZMod 2)) with hUw
  -- 2 columns independent mod W (from factB via csMem_iff)
  have hindep2 : ∀ a : Fin 2 → ZMod 2,
      (∑ i, a i • (![Phi R k1, Phi R k2] i)) ∈ W → a = 0 := by
    intro a ha
    rw [Fin.sum_univ_two] at ha
    simp only [Matrix.cons_val_zero, Matrix.cons_val_one] at ha
    -- a 0 • Phi R k1 + a 1 • Phi R k2 ∈ W. Show a = 0 by casing.
    by_contra hane
    -- find which is nonzero
    have key : ¬ (a 0 • Phi R k1 + a 1 • Phi R k2 ∈ W) := by
      have hz2 : ∀ z : ZMod 2, z = 0 ∨ z = 1 := by decide
      have h0 := hz2 (a 0)
      have h1 := hz2 (a 1)
      rcases h0 with e0|e0 <;> rcases h1 with e1|e1
      · exfalso; apply hane; funext i; fin_cases i <;> simp [e0,e1]
      · rw [e0,e1,zero_smul,one_smul,zero_add, ← csMem_iff]; exact hm2
      · rw [e0,e1,one_smul,zero_smul,add_zero, ← csMem_iff]; exact hm1
      · rw [e0,e1,one_smul,one_smul, ← csMem_iff]; exact hm12
    exact key ha
  -- finrank W + 2 ≤ finrank (W ⊔ span(range ![..]))
  have hge := finrank_sup_span_ge W 2 (![Phi R k1, Phi R k2]) hindep2
  -- span(range ![Phi R k1, Phi R k2]) ≤ span{w} ⊔ W actually ≤ Uw
  have hsub : Submodule.span (ZMod 2) (Set.range (![Phi R k1, Phi R k2])) ≤ Uw := by
    rw [Submodule.span_le]
    rintro x ⟨i, rfl⟩
    fin_cases i
    · exact hcol k1
    · exact hcol k2
  have hmono : (W ⊔ Submodule.span (ZMod 2) (Set.range (![Phi R k1, Phi R k2]))) ≤ Uw := by
    apply sup_le le_sup_left; exact hsub
  have hle : Module.finrank (ZMod 2)
      (W ⊔ Submodule.span (ZMod 2) (Set.range (![Phi R k1, Phi R k2])) :
        Submodule (ZMod 2) (Fin 9 → ZMod 2))
      ≤ Module.finrank (ZMod 2) Uw := Submodule.finrank_mono hmono
  -- finrank Uw ≤ finrank W + 1
  have hUwle : Module.finrank (ZMod 2) Uw ≤ Module.finrank (ZMod 2) W + 1 := by
    have hsspan1 : Module.finrank (ZMod 2) (Submodule.span (ZMod 2) {w}) ≤ 1 := by
      have h := finrank_span_le_card (R := ZMod 2) ({w} : Set (Fin 9 → ZMod 2))
      simpa using h
    have heq := Submodule.finrank_sup_add_finrank_inf_eq W (Submodule.span (ZMod 2) {w})
    rw [hUw]; omega
  have hWeq : Module.finrank (ZMod 2) W = 4 := finrank_colSp U hU
  omega


theorem Phi_smul (s : ZMod 2) (u : Fin 4 → ZMod 2) (k : Fin 4) :
    Phi (s • u) k = s • Phi u k := by
  funext ℓ; simp only [Phi, quadPair, Pi.smul_apply, smul_eq_mul]; rw [Finset.mul_sum]
  apply Finset.sum_congr rfl; intro i _; rw [Finset.mul_sum]
  apply Finset.sum_congr rfl; intro j _; ring

theorem Phi_mem_colSp (U : Fin 4 → ZMod 2) (j : Fin 4) : Phi U j ∈ colSp U :=
  Submodule.subset_span (Set.mem_range_self j)
theorem Phi_smul_mem_colSp (s : ZMod 2) (U : Fin 4 → ZMod 2) (j : Fin 4) :
    Phi (s • U) j ∈ colSp U := by
  rw [Phi_smul]; exact Submodule.smul_mem _ _ (Phi_mem_colSp U j)

-- KEY per-k membership for U = d1x ≠ 0, d1y = t • d1x.
theorem col_mem_dep (x y r : B) (hx : x ∈ m) (hy : y ∈ m)
    (h : ∀ k, r * v k ∈ (Ideal.span {x} ⊔ Ideal.span {y} : Ideal B))
    (hx0 : d1 x ≠ 0) (t : ZMod 2) (hyt : d1 y = t • d1 x) (k : Fin 4) :
    Phi (d1 r) k ∈ (colSp (d1 x) ⊔ Submodule.span (ZMod 2) {t • d2 x + d2 y} :
      Submodule (ZMod 2) (Fin 9 → ZMod 2)) := by
  obtain ⟨cx, cy, dx, dy, hcc, hdecomp⟩ := Phi_R_decomp x y r hx hy h k
  rw [hdecomp]
  apply Submodule.add_mem
  · -- junk: derive cx = cy * t
    have hcxt : cx = cy * t := by
      rw [hyt] at hcc
      -- cx•d1x + cy•(t•d1x) = 0  ->  (cx + cy*t)•d1x = 0
      have hcomb : (cx + cy * t) • d1 x = 0 := by
        rw [add_smul, mul_smul]; rw [smul_comm cy t (d1 x)] at hcc ⊢; exact hcc
      -- d1x ≠ 0 so scalar = 0
      have hsc : cx + cy * t = 0 := by
        by_contra hsne
        have hz2 : ∀ z : ZMod 2, z = 0 ∨ z = 1 := by decide
        rcases hz2 (cx + cy * t) with h0 | h1
        · exact hsne h0
        · rw [h1, one_smul] at hcomb; exact hx0 hcomb
      -- over ZMod 2: cx = cy*t
      have : ∀ p q : ZMod 2, p + q = 0 → p = q := by decide
      exact this _ _ hsc
    rw [hcxt]
    rw [show (cy * t) • d2 x + cy • d2 y = cy • (t • d2 x + d2 y) from by
      rw [smul_add, mul_smul]]
    exact Submodule.mem_sup_right
      (Submodule.smul_mem _ _ (Submodule.subset_span (Set.mem_singleton _)))
  · apply Submodule.mem_sup_left
    apply Submodule.add_mem
    · apply Submodule.sum_mem; intro j _; exact Submodule.smul_mem _ _ (Phi_mem_colSp (d1 x) j)
    · apply Submodule.sum_mem; intro j _
      rw [hyt]; exact Submodule.smul_mem _ _ (Phi_smul_mem_colSp t (d1 x) j)

-- dependence extraction: {X,Y} dependent (∃ nonzero combo = 0), X≠0 → ∃ t, Y = t•X
theorem dep_scalar (X Y : Fin 4 → ZMod 2) (hX : X ≠ 0)
    (hdep : ∃ a b : ZMod 2, (a • X + b • Y = 0) ∧ (a ≠ 0 ∨ b ≠ 0)) :
    ∃ t : ZMod 2, Y = t • X := by
  obtain ⟨a, b, hab, hne⟩ := hdep
  have hz2 : ∀ z : ZMod 2, z = 0 ∨ z = 1 := by decide
  rcases hz2 b with hb | hb
  · subst hb; simp only [zero_smul, add_zero] at hab
    rcases hz2 a with ha | ha
    · subst ha; simp at hne
    · subst ha; rw [one_smul] at hab; exact absurd hab hX
  · subst hb; rw [one_smul] at hab
    refine ⟨a, ?_⟩
    have h2 : Y = - (a • X) := by rw [eq_neg_iff_add_eq_zero, add_comm]; exact hab
    rw [h2]; ext i
    simp only [Pi.neg_apply, Pi.smul_apply, smul_eq_mul]
    rw [show -(a * X i) = a * X i from by
      have : (-(a * X i)) + (a * X i) = 0 := by ring
      have h3 : ∀ z : ZMod 2, -z = z := by decide
      exact h3 _]

/-! ### Final assembly -/
-- core for d1 x ≠ 0 (handles both independent and dependent-with-x)
theorem core_xne (x y r : B) (hx : x ∈ m) (hy : y ∈ m)
    (h : ∀ k, r * v k ∈ (Ideal.span {x} ⊔ Ideal.span {y} : Ideal B))
    (hx0 : d1 x ≠ 0) :
    ∃ α β : ZMod 2, d1 r = α • d1 x + β • d1 y := by
  by_cases hindep : ∀ a b : ZMod 2, a • d1 x + b • d1 y = 0 → a = 0 ∧ b = 0
  · exact core_indep x y r hx hy h hindep
  · -- dependent
    have hdep : ∃ a b : ZMod 2, (a • d1 x + b • d1 y = 0) ∧ (a ≠ 0 ∨ b ≠ 0) := by
      by_contra hcon
      apply hindep
      intro a b hab
      constructor
      · by_contra ha; exact hcon ⟨a, b, hab, Or.inl ha⟩
      · by_contra hb; exact hcon ⟨a, b, hab, Or.inr hb⟩
    obtain ⟨t, hyt⟩ := dep_scalar (d1 x) (d1 y) hx0 hdep
    have hcol : ∀ k, Phi (d1 r) k ∈
        (colSp (d1 x) ⊔ Submodule.span (ZMod 2) {t • d2 x + d2 y} :
          Submodule (ZMod 2) (Fin 9 → ZMod 2)) :=
      col_mem_dep x y r hx hy h hx0 t hyt
    obtain ⟨s, hs⟩ := dep_core (d1 x) (d1 r) (t • d2 x + d2 y) hx0 hcol
    exact ⟨s, 0, by rw [hs, zero_smul, add_zero]⟩

-- dim-0: d1 x = 0 and d1 y = 0 → d1 r = 0
theorem core_both_zero (x y r : B) (hx : x ∈ m) (hy : y ∈ m)
    (h : ∀ k, r * v k ∈ (Ideal.span {x} ⊔ Ideal.span {y} : Ideal B))
    (hx0 : d1 x = 0) (hy0 : d1 y = 0) :
    ∃ α β : ZMod 2, d1 r = α • d1 x + β • d1 y := by
  -- columns of Phi (d1 r) ∈ span{d2x, d2y} (≤2 dim) since colGens = 0
  have hcol : ∀ k, Phi (d1 r) k ∈ Submodule.span (ZMod 2) {d2 x, d2 y} := by
    intro k
    obtain ⟨cx, cy, dx, dy, hcc, hdecomp⟩ := Phi_R_decomp x y r hx hy h k
    rw [hdecomp]
    apply Submodule.add_mem
    · apply Submodule.add_mem
      · exact Submodule.smul_mem _ _ (Submodule.subset_span (by left; rfl))
      · exact Submodule.smul_mem _ _ (Submodule.subset_span (by right; rfl))
    · have hPhi0 : ∀ j : Fin 4, Phi (0 : Fin 4 → ZMod 2) j = 0 := by
        intro j; have := Phi_smul 0 (0 : Fin 4 → ZMod 2) j; rwa [zero_smul, zero_smul] at this
      have hz : (∑ j, dx j • Phi (d1 x) j) + (∑ j, dy j • Phi (d1 y) j) = 0 := by
        have h1 : (∑ j, dx j • Phi (d1 x) j) = 0 := by
          apply Finset.sum_eq_zero; intro j _; rw [hx0, hPhi0 j, smul_zero]
        have h2 : (∑ j, dy j • Phi (d1 y) j) = 0 := by
          apply Finset.sum_eq_zero; intro j _; rw [hy0, hPhi0 j, smul_zero]
        rw [h1, h2, add_zero]
      rw [hz]; exact Submodule.zero_mem _
  -- colSp(d1r) ⊆ span{d2x,d2y}; if d1r ≠ 0 then finrank colSp(d1r)=4 ≤ 2 contradiction
  have hd1r : d1 r = 0 := by
    by_contra hr0
    have hsub : colSp (d1 r) ≤ Submodule.span (ZMod 2) {d2 x, d2 y} := by
      unfold colSp; rw [Submodule.span_le]; rintro c ⟨k, rfl⟩; exact hcol k
    have h4 := finrank_colSp (d1 r) hr0
    have hmono := Submodule.finrank_mono hsub
    rw [h4] at hmono
    have h2 : Module.finrank (ZMod 2) (Submodule.span (ZMod 2) {d2 x, d2 y}) ≤ 2 := by
      have := finrank_span_le_card (R := ZMod 2) ({d2 x, d2 y} : Set (Fin 9 → ZMod 2))
      refine le_trans this ?_
      simp only [Set.toFinset_insert, Set.toFinset_singleton]
      exact le_trans (Finset.card_insert_le _ _) (by simp)
    omega
  exact ⟨0, 0, by rw [hd1r, hx0, hy0]; simp⟩

/-- **The degree-`1` span core.** For `x, y, r ∈ 𝔪` satisfying the colon hypothesis
`r · 𝔪 ⊆ (x) + (y)`, the linear-coordinate vector `d1 r ∈ 𝔽₂⁴` lies in the
`𝔽₂`-span of `d1 x` and `d1 y`. -/
theorem colon2_core_d1 (x y r : B) (hx : x ∈ m) (hy : y ∈ m)
    (h : ∀ k, r * v k ∈ (Ideal.span {x} ⊔ Ideal.span {y} : Ideal B)) :
    ∃ α β : ZMod 2, d1 r = α • d1 x + β • d1 y := by
  by_cases hx0 : d1 x = 0
  · by_cases hy0 : d1 y = 0
    · exact core_both_zero x y r hx hy h hx0 hy0
    · -- d1 y ≠ 0: swap roles. colon hyp symmetric.
      have hsw : ∀ k, r * v k ∈ (Ideal.span {y} ⊔ Ideal.span {x} : Ideal B) := by
        intro k; rw [sup_comm]; exact h k
      obtain ⟨α, β, hres⟩ := core_xne y x r hy hx hsw hy0
      exact ⟨β, α, by rw [hres]; abel⟩
  · exact core_xne x y r hx hy h hx0

/-- The `𝔪`-case of `colon2`: with `x, y ∈ 𝔪`, from `colon2_core_d1` the linear
part of `r` matches `α x + β y`, so `r - α x - β y ∈ 𝔪²` and `r ∈ (x)+(y)+𝔪²`. -/
theorem colon2_mcase (x y r : B) (hx : x ∈ m) (hy : y ∈ m)
    (h : ∀ k, r * v k ∈ (Ideal.span {x} ⊔ Ideal.span {y} : Ideal B)) :
    r ∈ (Ideal.span {x} ⊔ Ideal.span {y} ⊔ m ^ 2 : Ideal B) := by
  obtain ⟨α, β, hd1⟩ := colon2_core_d1 x y r hx hy h
  set z := r - α • x - β • y with hzdef
  have hzmsq : z ∈ m ^ 2 := by
    apply mem_msq_of_coords
    intro ℓ hℓ
    rcases Nat.lt_or_ge ℓ.val 1 with hℓ0 | hℓ1
    · have : ℓ = 0 := Fin.ext (by omega)
      subst this
      have hr0 : coordFun 0 r = 0 := (mem_m_iff_coord0 r).mp (r_mem_m x y r hx hy h)
      simp only [hzdef, map_sub, map_smul, smul_eq_mul]
      rw [hr0, (mem_m_iff_coord0 x).mp hx, (mem_m_iff_coord0 y).mp hy]; ring
    · set i : Fin 4 := ⟨ℓ.val - 1, by omega⟩ with hidef
      have hℓi : ℓ = ⟨i.val + 1, by omega⟩ := Fin.ext (by simp only [hidef]; omega)
      have hdi := congrArg (· i) hd1
      simp only [Pi.add_apply, Pi.smul_apply, smul_eq_mul, d1] at hdi
      rw [hℓi]
      have hzc : coordFun (⟨i.val + 1, by omega⟩ : Fin 14) z
          = coordFun (⟨i.val + 1, by omega⟩ : Fin 14) r
            - α * coordFun (⟨i.val + 1, by omega⟩ : Fin 14) x
            - β * coordFun (⟨i.val + 1, by omega⟩ : Fin 14) y := by
        rw [hzdef, map_sub, map_sub, map_smul, map_smul, smul_eq_mul, smul_eq_mul]
      rw [hzc,
          show coordFun (⟨i.val+1,by omega⟩:Fin 14) x = d1 x i from rfl,
          show coordFun (⟨i.val+1,by omega⟩:Fin 14) y = d1 y i from rfl,
          show coordFun (⟨i.val+1,by omega⟩:Fin 14) r = d1 r i from rfl]
      rw [show d1 r i = α * d1 x i + β * d1 y i from hdi]
      ring
  have hrsplit : r = α • x + β • y + z := by rw [hzdef]; ring
  rw [hrsplit]
  refine Submodule.add_mem _ (Submodule.add_mem _ ?_ ?_) ?_
  · exact Submodule.mem_sup_left (Submodule.mem_sup_left (zmod2_smul_mem_span α x))
  · exact Submodule.mem_sup_left (Submodule.mem_sup_right (zmod2_smul_mem_span β y))
  · exact Submodule.mem_sup_right hzmsq

/-- **The colon identity for `≤2`-generated ideals.** If every coordinate of
`r • v` lies in `J = (x) + (y)`, then `r ∈ J + 𝔪²`. Unit case: `(x)` or `(y)` is
`⊤`. `𝔪`-case: `colon2_mcase`. -/
theorem colon2 (x y r : B)
    (h : ∀ k, r * v k ∈ (Ideal.span {x} ⊔ Ideal.span {y} : Ideal B)) :
    r ∈ (Ideal.span {x} ⊔ Ideal.span {y} ⊔ m ^ 2 : Ideal B) := by
  by_cases hx : coordFun 0 x = 1
  · exact Submodule.mem_sup_left (Submodule.mem_sup_left
      (by rw [span_eq_top_of_coord0_one hx]; trivial))
  by_cases hy : coordFun 0 y = 1
  · exact Submodule.mem_sup_left (Submodule.mem_sup_right
      (by rw [span_eq_top_of_coord0_one hy]; trivial))
  have hxm : x ∈ m :=
    (mem_m_iff_coord0 x).mpr (by revert hx; generalize coordFun 0 x = z; revert z; decide)
  have hym : y ∈ m :=
    (mem_m_iff_coord0 y).mpr (by revert hy; generalize coordFun 0 y = z; revert z; decide)
  exact colon2_mcase x y r hxm hym h

/-! ### The two frozen Stage-B theorems -/

/-- **`M_annihilator` (frozen type).** `M` preserves annihilators: for every
`x : B`, `(0 :_M x) = (0 :_B x) · M`. -/
theorem M_annihilator_proof :
    ∀ x : B, annihM x = (annih x) • (⊤ : Submodule B M) := by
  intro x
  apply le_antisymm
  · rintro z hz
    obtain ⟨w, rfl⟩ := Bv.mkQ_surjective z
    rw [mem_annihM, Bv, Submodule.mem_span_singleton] at hz
    obtain ⟨r, hr⟩ := hz
    have hwk : ∀ k, x * w k = r * v k := fun k => by
      have := congrArg (· k) hr
      simpa [Pi.smul_apply, smul_eq_mul] using this.symm
    have hin : ∀ k, r * v k ∈ (Ideal.span {x} ⊔ Ideal.span {(0 : B)} : Ideal B) := fun k => by
      rw [← hwk k]
      exact Submodule.mem_sup_left (Ideal.mem_span_singleton.mpr ⟨w k, by ring⟩)
    have hr2 := colon2 x 0 r hin
    rw [show (Ideal.span {(0 : B)} : Ideal B) = ⊥ from by simp, sup_bot_eq] at hr2
    rw [Submodule.mem_sup] at hr2
    obtain ⟨p, hp, e, he, hpe⟩ := hr2
    rw [Ideal.mem_span_singleton] at hp
    obtain ⟨s, rfl⟩ := hp
    rw [mem_smul_top_M]
    refine ⟨w - s • v, fun k => ?_, mkQ_sub_smul_v s w⟩
    rw [mem_annih_iff]
    have hrx : r - s * x = e := by rw [← hpe]; ring
    have hcoord : (w - s • v) k * x = (r - s * x) * v k := by
      simp only [Pi.sub_apply, Pi.smul_apply, smul_eq_mul]
      rw [sub_mul, mul_comm (w k) x, hwk k]; ring
    rw [hcoord, hrx]; exact msq_smul_v e he k
  · rintro z hz
    rw [mem_smul_top_M] at hz
    obtain ⟨w, hw, rfl⟩ := hz
    rw [mem_annihM]
    have hxw : x • w = 0 := by
      funext k; simp only [Pi.smul_apply, smul_eq_mul, Pi.zero_apply]
      rw [mul_comm]; exact (mem_annih_iff x (w k)).mp (hw k)
    rw [hxw]; exact Submodule.zero_mem _

/-- **`M_pairwise_intersection` (frozen type).** `M` preserves every pairwise
principal intersection: for all `x y : B`, `xM ⊓ yM = (xB ⊓ yB) · M`. -/
theorem M_pairwise_intersection_proof :
    ∀ x y : B, smulSub x ⊓ smulSub y
      = (Ideal.span {x} ⊓ Ideal.span {y}) • (⊤ : Submodule B M) := by
  intro x y
  apply le_antisymm
  · rintro z ⟨hzx, hzy⟩
    rw [SetLike.mem_coe] at hzx hzy
    unfold smulSub at hzx hzy
    rw [mem_smul_top_M] at hzx hzy
    obtain ⟨w₁, hw₁, hmk₁⟩ := hzx
    obtain ⟨w₂, hw₂, hmk₂⟩ := hzy
    have hdiff : Bv.mkQ (w₁ - w₂) = 0 := by rw [map_sub, hmk₁, hmk₂, sub_self]
    rw [show Bv.mkQ (w₁ - w₂) = Submodule.Quotient.mk (w₁ - w₂) from rfl,
        Submodule.Quotient.mk_eq_zero, Bv, Submodule.mem_span_singleton] at hdiff
    obtain ⟨r, hr⟩ := hdiff
    have hrk : ∀ k, r * v k = w₁ k - w₂ k := fun k => by
      have := congrArg (· k) hr
      simpa [Pi.smul_apply, smul_eq_mul, Pi.sub_apply] using this
    have hin : ∀ k, r * v k ∈ (Ideal.span {x} ⊔ Ideal.span {y} : Ideal B) := fun k => by
      rw [hrk k]
      exact Submodule.sub_mem _ (Submodule.mem_sup_left (hw₁ k)) (Submodule.mem_sup_right (hw₂ k))
    have hr2 := colon2 x y r hin
    rw [Submodule.mem_sup] at hr2
    obtain ⟨pq, hpq, e, he, hpqe⟩ := hr2
    rw [Submodule.mem_sup] at hpq
    obtain ⟨p, hp, q, hq, hpq2⟩ := hpq
    set s := p + e with hs
    rw [mem_smul_top_M]
    refine ⟨w₁ - s • v, fun k => ?_, by rw [mkQ_sub_smul_v]; exact hmk₁⟩
    refine ⟨?_, ?_⟩
    · simp only [Pi.sub_apply, Pi.smul_apply, smul_eq_mul]
      refine Submodule.sub_mem _ (hw₁ k) ?_
      rw [hs, add_mul]
      refine Submodule.add_mem _ (Ideal.mul_mem_right _ _ hp) ?_
      rw [msq_smul_v e he k]; exact Submodule.zero_mem _
    · simp only [Pi.sub_apply, Pi.smul_apply, smul_eq_mul]
      have hw1k : w₁ k = r * v k + w₂ k := by rw [hrk k]; ring
      rw [hw1k]
      have hrs : r - s = q := by rw [hs, ← hpqe, ← hpq2]; ring
      have he2 : r * v k + w₂ k - s * v k = q * v k + w₂ k := by rw [← hrs]; ring
      rw [he2]
      exact Submodule.add_mem _ (Ideal.mul_mem_right _ _ hq) (hw₂ k)
  · refine le_inf ?_ ?_
    · unfold smulSub; exact Submodule.smul_mono inf_le_left le_rfl
    · unfold smulSub; exact Submodule.smul_mono inf_le_right le_rfl

end Prob4b

