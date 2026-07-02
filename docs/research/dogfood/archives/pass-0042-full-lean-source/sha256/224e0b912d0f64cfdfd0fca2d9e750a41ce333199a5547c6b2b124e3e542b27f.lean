/-
Copyright (c) 2026 Prob4b formalization. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Prob4b formalization
-/
import Prob4b.Defs

/-!
# Stage A — structure of the base ring `B`

This file proves the Stage A support lemmas for the Problem 4(b) counterexample.
`B = 𝔽₂[a,b,c,d] / ((a,b,c,d)³, ad + bc)` is modeled (in `Defs.lean`) as the
`MvPolynomial` quotient `P4 ⧸ Brel`. Stage A recovers the computational handles
that Stages B and C build on:

* `m_pow_three : m ^ 3 = ⊥` — the maximal ideal `𝔪 = (a,b,c,d)` of `B` is
  nilpotent of order `3` (this is `mP ^ 3 ≤ Brel`, pushed through the quotient);
* `ad_eq_bc : a * d = b * c` — the sole degree-`2` relation (char-`2` form of
  `ad + bc = 0`);
* a `ZMod 2`-linear *coefficient functional* `phiP : P4 →ₗ[ZMod 2] ZMod 2` that
  reads `coeff (X₀X₃) + coeff (X₁X₂)`. It vanishes on `Brel` (degree reasons on
  `𝔪³`, the char-`2` cancellation on the generator `X₀X₃ + X₁X₂`), hence descends
  to a detector of nonvanishing in `B`. This yields `ad_ne_zero : a * d ≠ 0`: the
  degree-`2` relation identifies two *nonzero* elements, it does not kill them.

Everything here is structural; no `decide` over `B` itself is used (`B` is a
`noncomputable` quotient with no definitional `Fintype`). The functional `phiP`
is the reusable non-vanishing certificate that later stages can specialize to
other monomial coefficients.

See `BLUEPRINT.md` "Stage A" and `PROGRESS.md`.
-/

namespace Prob4b

open MvPolynomial Finsupp

/-! ### `𝔪 = (a,b,c,d)` is the image of `mP`, and `𝔪³ = 0` -/

/-- The maximal ideal `m = 𝔪` of `B` is the image of `mP = (X₀,X₁,X₂,X₃)` under
the quotient map. -/
theorem m_eq_map : m = mP.map (Ideal.Quotient.mk Brel) := by
  unfold m mP a b c d
  rw [Ideal.map_span]
  congr 1
  simp [Set.image_insert_eq]

/-- `𝔪³ = 0` in `B`: the maximal ideal is nilpotent of order `3`. This is the
structural statement that every degree-`≥ 3` product vanishes, obtained from
`mP ^ 3 ≤ Brel = ker (mk)`. -/
theorem m_pow_three : m ^ 3 = (⊥ : Ideal B) := by
  rw [m_eq_map, ← Ideal.map_pow, Ideal.map_eq_bot_iff_le_ker, Ideal.mk_ker]
  unfold Brel
  exact le_add_right le_rfl

/-! ### The degree-`2` relation `a*d = b*c` -/

/-- The sole degree-`2` relation of `B`: `a * d = b * c`. In characteristic `2`
this is the image of `X₀X₃ + X₁X₂ ∈ Brel`. -/
theorem ad_eq_bc : a * d = b * c := by
  unfold a b c d
  rw [← map_mul, ← map_mul, ← sub_eq_zero, ← map_sub, Ideal.Quotient.eq_zero_iff_mem]
  unfold Brel
  apply Ideal.mem_sup_right
  have h2 : (X 0 * X 3 - X 1 * X 2 : P4) = X 0 * X 3 + X 1 * X 2 := by
    rw [sub_eq_add_neg, CharTwo.neg_eq]
  rw [h2]
  exact Ideal.subset_span (by simp)

/-! ### A coefficient functional detecting nonvanishing in `B`

`phiP p = coeff (X₀X₃) p + coeff (X₁X₂) p`, a `ZMod 2`-linear functional on `P4`.
It vanishes on `Brel`, so any `p` with `phiP p ≠ 0` has nonzero image in `B`. -/

/-- The exponent vector of the monomial `X₀ * X₃`. -/
noncomputable def mon03 : Fin 4 →₀ ℕ := Finsupp.single 0 1 + Finsupp.single 3 1
/-- The exponent vector of the monomial `X₁ * X₂`. -/
noncomputable def mon12 : Fin 4 →₀ ℕ := Finsupp.single 1 1 + Finsupp.single 2 1

/-- The `ZMod 2`-linear functional `p ↦ coeff (X₀X₃) p + coeff (X₁X₂) p`. -/
noncomputable def phiP : P4 →ₗ[ZMod 2] ZMod 2 :=
  MvPolynomial.lcoeff (ZMod 2) mon03 + MvPolynomial.lcoeff (ZMod 2) mon12

theorem degree_mon03 : Finsupp.degree mon03 = 2 := by
  unfold mon03; rw [map_add]; simp [Finsupp.degree_single]

theorem degree_mon12 : Finsupp.degree mon12 = 2 := by
  unfold mon12; rw [map_add]; simp [Finsupp.degree_single]

/-- `mP` is exactly the ideal `idealOfVars` spanned by all variables. -/
theorem mP_eq : mP = idealOfVars (Fin 4) (ZMod 2) := by
  unfold mP idealOfVars
  congr 1
  ext p
  simp only [Set.mem_insert_iff, Set.mem_singleton_iff, Set.mem_range]
  constructor
  · rintro (h | h | h | h) <;> subst h
    exacts [⟨0, rfl⟩, ⟨1, rfl⟩, ⟨2, rfl⟩, ⟨3, rfl⟩]
  · rintro ⟨i, rfl⟩; fin_cases i <;> simp

theorem mon03_ne_mon12 : mon03 ≠ mon12 := by
  intro h
  apply_fun (fun f => f 0) at h
  simp only [mon03, mon12, Finsupp.add_apply, Finsupp.single_apply] at h
  revert h; decide

theorem X03_mon : (X 0 * X 3 : P4) = monomial mon03 1 := by
  rw [X, X, monomial_mul, mul_one]; rfl

theorem X12_mon : (X 1 * X 2 : P4) = monomial mon12 1 := by
  rw [X, X, monomial_mul, mul_one]; rfl

theorem mon12_not_le_mon03 : ¬ mon12 ≤ mon03 := by
  intro h
  have := h 1
  simp only [mon12, mon03, Finsupp.add_apply, Finsupp.single_apply] at this
  revert this; decide

theorem mon03_not_le_mon12 : ¬ mon03 ≤ mon12 := by
  intro h
  have := h 0
  simp only [mon12, mon03, Finsupp.add_apply, Finsupp.single_apply] at this
  revert this; decide

/-- `phiP` vanishes on every `P4`-multiple of the relation generator
`X₀X₃ + X₁X₂`. The degree-`2` part of `(X₀X₃ + X₁X₂) * w` is
`(X₀X₃ + X₁X₂) * w₀` (`w₀ = ` constant term of `w`); reading both monomials
gives `w₀ + w₀ = 2 w₀ = 0` in characteristic `2`. -/
theorem phiP_gen_mul (w : P4) : phiP ((X 0 * X 3 + X 1 * X 2) * w) = 0 := by
  rw [X03_mon, X12_mon, add_mul]
  unfold phiP
  rw [LinearMap.add_apply, map_add, map_add]
  simp only [lcoeff_apply]
  rw [coeff_monomial_mul' mon03 mon03 1 w, coeff_monomial_mul' mon03 mon12 1 w,
      coeff_monomial_mul' mon12 mon03 1 w, coeff_monomial_mul' mon12 mon12 1 w]
  rw [if_pos le_rfl, if_pos le_rfl, if_neg mon12_not_le_mon03, if_neg mon03_not_le_mon12]
  simp only [tsub_self, one_mul, add_zero, zero_add]
  have h2 : (2 : ZMod 2) = 0 := by decide
  rw [show coeff 0 w + coeff 0 w = (2 : ZMod 2) * coeff 0 w from by ring, h2, zero_mul]

/-- `phiP` vanishes on all of `Brel`: on `mP³` by degree (`phiP` reads only the
two degree-`2` monomials `X₀X₃, X₁X₂`, both absent from degree-`≥ 3` elements),
and on `span {X₀X₃ + X₁X₂}` by `phiP_gen_mul`. -/
theorem phiP_vanish_Brel : ∀ p ∈ Brel, phiP p = 0 := by
  intro p hp
  unfold Brel at hp
  rw [Submodule.add_eq_sup, Submodule.mem_sup] at hp
  obtain ⟨y, hy, z, hz, rfl⟩ := hp
  rw [map_add]
  have hyz : phiP y = 0 := by
    rw [mP_eq, mem_pow_idealOfVars_iff'] at hy
    unfold phiP
    rw [LinearMap.add_apply]
    simp only [lcoeff_apply]
    rw [hy mon03 (by rw [degree_mon03]; norm_num),
        hy mon12 (by rw [degree_mon12]; norm_num)]
    simp
  have hzz : phiP z = 0 := by
    rw [Ideal.mem_span_singleton] at hz
    obtain ⟨w, rfl⟩ := hz
    exact phiP_gen_mul w
  rw [hyz, hzz, add_zero]

/-- The detection principle: if `phiP p ≠ 0` then the image of `p` in `B` is
nonzero. -/
theorem ne_zero_of_phiP {p : P4} (h : phiP p ≠ 0) :
    Ideal.Quotient.mk Brel p ≠ 0 := by
  intro hp
  rw [Ideal.Quotient.eq_zero_iff_mem] at hp
  exact h (phiP_vanish_Brel p hp)

/-- `phiP (X₀ * X₃) = 1`. -/
theorem phiP_X03 : phiP (X 0 * X 3 : P4) = 1 := by
  unfold phiP
  rw [LinearMap.add_apply]
  simp only [lcoeff_apply]
  rw [X03_mon, coeff_monomial, coeff_monomial, if_pos rfl, if_neg mon03_ne_mon12]
  ring

/-- `a * d ≠ 0` in `B`: the degree-`2` relation `a*d = b*c` identifies two
*nonzero* elements. Certified by the coefficient functional `phiP`. -/
theorem ad_ne_zero : a * d ≠ (0 : B) := by
  unfold a d
  rw [← map_mul]
  exact ne_zero_of_phiP (by rw [phiP_X03]; exact one_ne_zero)

/-- `b * c ≠ 0` in `B` (equal to `a * d` by `ad_eq_bc`). -/
theorem bc_ne_zero : b * c ≠ (0 : B) := by
  rw [← ad_eq_bc]; exact ad_ne_zero

/-! ### The 14-element `𝔽₂`-spanning set of `B`

The monomial images of degree `≤ 2`, with `b*c` collapsed to `a*d` by `ad_eq_bc`,
span `B` over `𝔽₂ = ZMod 2`. This gives `Module.Finite (ZMod 2) B` — the
finiteness handle the upper-bound results of later stages need. -/

/-- The explicit 14-element `𝔽₂`-spanning set of `B`:
`{1, a, b, c, d, a², ab, ac, ad, b², bd, c², cd, d²}` (with `bc = ad`). -/
noncomputable def Sset : Set B :=
  {1, a, b, c, d, a * a, a * b, a * c, a * d, b * b, b * d, c * c, c * d, d * d}

/-- The generator tuple `(a, b, c, d) : Fin 4 → B`, used to express the quotient
map as an evaluation. -/
noncomputable def gen : Fin 4 → B := ![a, b, c, d]

/-- The quotient map `mk : P4 → B` is the `ZMod 2`-algebra evaluation at the
generators. -/
theorem mk_eq_aeval (p : P4) : Ideal.Quotient.mk Brel p = aeval gen p := by
  have h : (Ideal.Quotient.mkₐ (ZMod 2) Brel) = aeval gen := by
    apply MvPolynomial.algHom_ext
    intro i
    rw [Ideal.Quotient.mkₐ_eq_mk, aeval_X]
    fin_cases i <;> rfl
  simpa [Ideal.Quotient.mkₐ_eq_mk] using congrArg (fun f => f p) h

/-- The image of `monomial e 1` is the product of generator powers. -/
theorem mk_mono_prod (e : Fin 4 →₀ ℕ) :
    Ideal.Quotient.mk Brel (monomial e 1) = a ^ e 0 * b ^ e 1 * c ^ e 2 * d ^ e 3 := by
  rw [mk_eq_aeval, aeval_monomial, map_one, one_mul, Finsupp.prod]
  rw [Finset.prod_subset (Finset.subset_univ e.support)
      (fun i _ hi => by rw [Finsupp.notMem_support_iff.mp hi, pow_zero])]
  rw [Fin.prod_univ_four]; rfl

/-- `degree e` on `Fin 4` is the sum of the four exponents. -/
theorem degree_eq_sum (e : Fin 4 →₀ ℕ) : Finsupp.degree e = e 0 + e 1 + e 2 + e 3 := by
  have hz : ∀ i ∈ (Finset.univ : Finset (Fin 4)), i ∉ e.support → e i = 0 :=
    fun i _ hi => Finsupp.notMem_support_iff.mp hi
  rw [Finsupp.degree_apply, Finset.sum_subset (Finset.subset_univ e.support) hz,
    Fin.sum_univ_four]

theorem bc_mem_Sset : b * c ∈ Submodule.span (ZMod 2) Sset := by
  rw [← ad_eq_bc]; apply Submodule.subset_span; unfold Sset; simp

theorem cb_mem_Sset : c * b ∈ Submodule.span (ZMod 2) Sset := by
  rw [mul_comm, ← ad_eq_bc]; apply Submodule.subset_span; unfold Sset; simp

set_option maxHeartbeats 2000000 in
-- The `interval_cases` quadruple split over the four exponents (each `≤ 2`)
-- produces enough kernel work to exceed the default heartbeat budget.
/-- Any product of generator powers of total degree `< 3` lies in `span Sset`.
This is the finite enumeration of the `≤ 2`-degree monomials (the degree-`≥ 3`
products vanish by `𝔪³ = 0`). -/
theorem prod_low_mem (n0 n1 n2 n3 : ℕ) (hd : n0 + n1 + n2 + n3 < 3) :
    a ^ n0 * b ^ n1 * c ^ n2 * d ^ n3 ∈ Submodule.span (ZMod 2) Sset := by
  have h0 : n0 ≤ 2 := by omega
  have h1 : n1 ≤ 2 := by omega
  have h2 : n2 ≤ 2 := by omega
  have h3 : n3 ≤ 2 := by omega
  interval_cases n0 <;> interval_cases n1 <;> interval_cases n2 <;> interval_cases n3 <;>
    (try omega) <;>
    simp only [pow_zero, pow_one, pow_two, one_mul, mul_one] <;>
    first
    | exact bc_mem_Sset
    | exact cb_mem_Sset
    | (apply Submodule.subset_span; unfold Sset; simp)

/-- Every monomial image lies in `span Sset`: degree `≥ 3` maps to `0`
(`𝔪³ = 0`), degree `≤ 2` is enumerated by `prod_low_mem`. -/
theorem mk_mono_mem (e : Fin 4 →₀ ℕ) :
    Ideal.Quotient.mk Brel (monomial e 1) ∈ Submodule.span (ZMod 2) Sset := by
  rcases le_or_gt 3 (Finsupp.degree e) with hd | hd
  · rw [Ideal.Quotient.eq_zero_iff_mem.mpr]
    · exact Submodule.zero_mem _
    · unfold Brel
      exact Ideal.mem_sup_left
        ((mP_eq ▸ monomial_mem_pow_idealOfVars_iff 3 e one_ne_zero).mpr hd)
  · rw [mk_mono_prod]
    rw [degree_eq_sum] at hd
    exact prod_low_mem _ _ _ _ hd

/-- **The 14-element set spans `B` over `𝔽₂`.** `Submodule.span (ZMod 2) Sset = ⊤`.
This is the upper-bound handle (`dim_{𝔽₂} B ≤ 14`) for later stages. -/
theorem span_Sset_eq_top : Submodule.span (ZMod 2) Sset = ⊤ := by
  rw [eq_top_iff]
  rintro x -
  obtain ⟨p, rfl⟩ := Ideal.Quotient.mk_surjective x
  have hp : p ∈ Submodule.span (ZMod 2)
      (Set.range (fun e : Fin 4 →₀ ℕ => (monomial e 1 : P4))) := by
    rw [show (Set.range (fun e : Fin 4 →₀ ℕ => (monomial e 1 : P4)))
        = Set.range (basisMonomials (Fin 4) (ZMod 2)) from by rw [coe_basisMonomials]]
    rw [Module.Basis.span_eq]; trivial
  refine Submodule.span_induction ?_ ?_ ?_ ?_ hp
  · rintro y ⟨e, rfl⟩; exact mk_mono_mem e
  · rw [map_zero]; exact Submodule.zero_mem _
  · intro y z _ _ hy hz; rw [map_add]; exact Submodule.add_mem _ hy hz
  · intro r y _ hy
    rw [ZMod.map_smul (Ideal.Quotient.mk Brel) r y]
    exact Submodule.smul_mem _ r hy

/-- `Sset` is a finite set (`14` explicit elements). -/
theorem Sset_finite : Sset.Finite := by
  unfold Sset
  apply Set.Finite.insert
  repeat apply Set.Finite.insert
  exact Set.finite_singleton _

/-- `B` is module-finite over `𝔽₂` (a finite-dimensional algebra). -/
theorem B_module_finite : Module.Finite (ZMod 2) B := by
  refine ⟨⟨Sset_finite.toFinset, ?_⟩⟩
  rw [Set.Finite.coe_toFinset]
  exact span_Sset_eq_top

end Prob4b
