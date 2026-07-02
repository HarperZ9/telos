/-
Copyright (c) 2026 Prob4b formalization. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Prob4b formalization
-/
import Prob4b.Proofs.RingModel.Basic

/-!
# Stage A2 — the `𝔽₂`-normal form of the base ring `B`

This file upgrades the Stage A spanning result (`span_Sset_eq_top`) to a genuine
`14`-dimensional `ZMod 2`-basis of `B = 𝔽₂[a,b,c,d] / ((a,b,c,d)³, ad + bc)`,
giving later stages a usable coordinate system.

The construction:

* `bexp : Fin 14 → (Fin 4 →₀ ℕ)` lists the `14` basis monomial exponents in the
  same order as `Sset`: `1, a, b, c, d, a², ab, ac, ad, b², bd, c², cd, d²`
  (note `bc = ad` is identified, so only `ad` appears; its exponent is `mon03`).
* For each index `i ≠ 8` the plain coefficient functional
  `MvPolynomial.lcoeff (bexp i)` vanishes on `Brel` (degree reasons on `𝔪³`, and
  `bexp i ∉ {mon03, mon12}` kills the relation generator), so it descends through
  `Brel` via `Submodule.liftQ` to a functional `B →ₗ[ZMod 2] ZMod 2`.
* The `ad`-coordinate (index `8`) reuses `phiP` from Stage A (already proven to
  vanish on `Brel`), which reads `coeff (X₀X₃) + coeff (X₁X₂)` — exactly the
  well-defined `ad`-coordinate because `ad = bc`.
* Assembled into `Bcoord : B →ₗ[ZMod 2] (Fin 14 → ZMod 2)`, these `14`
  functionals send the `j`-th basis monomial to the `j`-th standard vector
  (`Bcoord_apply_basisMon`), which is a left inverse to the basis family — hence
  linear independence and, with `span_Sset_eq_top`, the basis `B_basis` and the
  coordinate isomorphism `Bcoord ≃ Bequiv : B ≃ₗ[ZMod 2] (Fin 14 → ZMod 2)`.
* Finiteness follows: `instFintypeB : Fintype B` and `instDecidableEqB :
  DecidableEq B` (via the linear equivalence to the finite `Fin 14 → ZMod 2`).

See `BLUEPRINT.md` "Stage A" (A3) and `PROGRESS.md`.
-/

namespace Prob4b

open MvPolynomial Finsupp

/-! ### Degree/exponent combinatorics -/

/-- If `f ≤ e` componentwise and they have the same degree, they are equal. -/
theorem eq_of_le_degree (e f : Fin 4 →₀ ℕ) (hle : f ≤ e)
    (heq : Finsupp.degree e = Finsupp.degree f) : e = f := by
  have hsub : e - f + f = e := by
    ext i; rw [Finsupp.add_apply, Finsupp.tsub_apply]; have := hle i; omega
  have hd : Finsupp.degree (e - f) = 0 := by
    have hadd : Finsupp.degree e = Finsupp.degree (e - f) + Finsupp.degree f := by
      conv_lhs => rw [← hsub]; rw [map_add]
    omega
  have hz : e - f = 0 := (Finsupp.degree_eq_zero_iff _).mp hd
  have : e = 0 + f := by rw [← hz]; exact hsub.symm
  simpa using this

/-- A degree-`2` exponent `f` is not `≤` a distinct exponent `e` of degree `≤ 2`. -/
theorem not_le_of_ne_degree (e f : Fin 4 →₀ ℕ) (hd : Finsupp.degree e ≤ 2)
    (hdf : Finsupp.degree f = 2) (hne : e ≠ f) : ¬ f ≤ e := fun hle =>
  hne (eq_of_le_degree e f hle (by rw [hdf]; exact le_antisymm hd (hdf ▸ Finsupp.degree_mono hle)))

/-! ### `lcoeff` of a degree-`≤ 2` monomial (≠ `mon03`, `mon12`) vanishes on `Brel` -/

/-- The coefficient at a degree-`≤ 2` exponent `e ∉ {mon03, mon12}` of any
multiple of the relation generator `X₀X₃ + X₁X₂` is `0`. -/
theorem lcoeff_gen_mul (e : Fin 4 →₀ ℕ) (hd : Finsupp.degree e ≤ 2)
    (h03 : e ≠ mon03) (h12 : e ≠ mon12) (w : P4) :
    coeff e ((X 0 * X 3 + X 1 * X 2) * w) = 0 := by
  rw [X03_mon, X12_mon, add_mul, coeff_add]
  rw [coeff_monomial_mul' e mon03 1 w, coeff_monomial_mul' e mon12 1 w]
  rw [if_neg (not_le_of_ne_degree e mon03 hd degree_mon03 h03),
      if_neg (not_le_of_ne_degree e mon12 hd degree_mon12 h12), add_zero]

/-- `lcoeff (bexp i)` vanishes on `Brel` for a degree-`≤ 2` exponent `e` distinct
from `mon03` and `mon12`: on `𝔪³` by degree, on `span {X₀X₃ + X₁X₂}` by
`lcoeff_gen_mul`. This is the hypothesis that lets the functional descend. -/
theorem lcoeff_vanish_Brel (e : Fin 4 →₀ ℕ) (hd : Finsupp.degree e ≤ 2)
    (h03 : e ≠ mon03) (h12 : e ≠ mon12) :
    Brel.restrictScalars (ZMod 2) ≤ LinearMap.ker (lcoeff (ZMod 2) e) := by
  intro p hp
  rw [Submodule.restrictScalars_mem] at hp
  rw [LinearMap.mem_ker]
  unfold Brel at hp
  rw [Submodule.add_eq_sup, Submodule.mem_sup] at hp
  obtain ⟨y, hy, z, hz, rfl⟩ := hp
  rw [map_add]
  have hyz : (lcoeff (ZMod 2) e) y = 0 := by
    rw [mP_eq, mem_pow_idealOfVars_iff'] at hy
    simp only [lcoeff_apply]
    exact hy e (by omega)
  have hzz : (lcoeff (ZMod 2) e) z = 0 := by
    rw [Ideal.mem_span_singleton] at hz
    obtain ⟨w, rfl⟩ := hz
    simp only [lcoeff_apply]
    exact lcoeff_gen_mul e hd h03 h12 w
  rw [hyz, hzz, add_zero]

/-- `phiP` vanishes on `Brel`, packaged as a `ker`-inclusion over the restricted
scalars (`ZMod 2`) so it can feed `Submodule.liftQ`. -/
theorem phiP_vanish_restrict :
    Brel.restrictScalars (ZMod 2) ≤ LinearMap.ker phiP := by
  intro p hp
  rw [Submodule.restrictScalars_mem] at hp
  rw [LinearMap.mem_ker]
  exact phiP_vanish_Brel p hp

/-! ### The `14` basis exponents and their normal form -/

/-- The `14` basis monomial exponents, in the order of `Sset`:
`1, a, b, c, d, a², ab, ac, ad, b², bd, c², cd, d²`. Index `8` is `ad = mon03`. -/
noncomputable def bexp : Fin 14 → (Fin 4 →₀ ℕ) :=
  ![0,
    single 0 1, single 1 1, single 2 1, single 3 1,
    single 0 2, single 0 1 + single 1 1, single 0 1 + single 2 1, mon03,
    single 1 2, single 1 1 + single 3 1, single 2 2, single 2 1 + single 3 1, single 3 2]

/-- Concrete coordinate-wise normal form of `bexp`. -/
theorem bexp_apply (j : Fin 14) (k : Fin 4) : bexp j k =
    (![ ![0,0,0,0],
        ![1,0,0,0], ![0,1,0,0], ![0,0,1,0], ![0,0,0,1],
        ![2,0,0,0], ![1,1,0,0], ![1,0,1,0], ![1,0,0,1],
        ![0,2,0,0], ![0,1,0,1], ![0,0,2,0], ![0,0,1,1], ![0,0,0,2]] j) k := by
  fin_cases j <;> fin_cases k <;> simp [bexp, mon03, Finsupp.add_apply]

/-- Each basis exponent has degree `≤ 2`. -/
theorem bexp_degree_le (j : Fin 14) : Finsupp.degree (bexp j) ≤ 2 := by
  rw [degree_eq_sum, bexp_apply, bexp_apply, bexp_apply, bexp_apply]
  fin_cases j <;> decide

/-- `bexp 8 = mon03` (the `ad`-coordinate). -/
theorem bexp_eight : bexp 8 = mon03 := by simp [bexp]

/-- Concrete coordinate-wise normal form of `mon03`. -/
theorem mon03_apply (k : Fin 4) : mon03 k = ![1,0,0,1] k := by
  rw [mon03, Finsupp.add_apply]; fin_cases k <;> simp

/-- Concrete coordinate-wise normal form of `mon12`. -/
theorem mon12_apply (k : Fin 4) : mon12 k = ![0,1,1,0] k := by
  rw [mon12, Finsupp.add_apply]; fin_cases k <;> simp

/-- For `j ≠ 8`, the basis exponent is not `mon03`. -/
theorem bexp_ne_mon03 {j : Fin 14} (hj : j ≠ 8) : bexp j ≠ mon03 := by
  intro h
  apply hj
  have h0 := congrArg (· (0 : Fin 4)) h
  have h1 := congrArg (· (1 : Fin 4)) h
  have h2 := congrArg (· (2 : Fin 4)) h
  have h3 := congrArg (· (3 : Fin 4)) h
  rw [bexp_apply, mon03_apply] at h0 h1 h2 h3
  fin_cases j <;> first | rfl | (revert h0 h1 h2 h3; decide)

/-- No basis exponent equals `mon12` (the monomial `bc`, identified with `ad`). -/
theorem bexp_ne_mon12 (j : Fin 14) : bexp j ≠ mon12 := by
  intro h
  have h0 := congrArg (· (0 : Fin 4)) h
  have h1 := congrArg (· (1 : Fin 4)) h
  have h2 := congrArg (· (2 : Fin 4)) h
  have h3 := congrArg (· (3 : Fin 4)) h
  rw [bexp_apply, mon12_apply] at h0 h1 h2 h3
  fin_cases j <;> revert h0 h1 h2 h3 <;> decide

/-- `bexp` is injective: distinct indices give distinct exponents. -/
theorem bexp_injective : Function.Injective bexp := by
  intro i j h
  have hk : ∀ k, bexp i k = bexp j k := fun k => by rw [h]
  fin_cases i <;> fin_cases j <;>
    first
    | rfl
    | (exfalso
       first
       | (have := hk 0; rw [bexp_apply, bexp_apply] at this; revert this; decide)
       | (have := hk 1; rw [bexp_apply, bexp_apply] at this; revert this; decide)
       | (have := hk 2; rw [bexp_apply, bexp_apply] at this; revert this; decide)
       | (have := hk 3; rw [bexp_apply, bexp_apply] at this; revert this; decide))

/-! ### The `14` coordinate functionals and the coordinate map -/

/-- The `i`-th coordinate functional on `B`. For `i = 8` it is the descent of
`phiP` (the `ad = bc` coordinate); otherwise it is the descent of the plain
coefficient functional `lcoeff (bexp i)`. -/
noncomputable def coordFun (i : Fin 14) : B →ₗ[ZMod 2] ZMod 2 :=
  if h : i = 8 then
    (Brel.restrictScalars (ZMod 2)).liftQ phiP phiP_vanish_restrict
  else
    (Brel.restrictScalars (ZMod 2)).liftQ (lcoeff (ZMod 2) (bexp i))
      (lcoeff_vanish_Brel (bexp i) (bexp_degree_le i) (bexp_ne_mon03 h) (bexp_ne_mon12 i))

/-- Applying `coordFun 8` to `mk p` reads `phiP p` (the `ad`-coordinate). -/
theorem coordFun_eight_apply (p : P4) :
    coordFun 8 (Ideal.Quotient.mk Brel p) = phiP p := by
  rw [coordFun, dif_pos rfl]
  exact Submodule.liftQ_apply _ _ p

/-- Applying `coordFun i` (`i ≠ 8`) to `mk p` reads `coeff (bexp i) p`. -/
theorem coordFun_apply {i : Fin 14} (hi : i ≠ 8) (p : P4) :
    coordFun i (Ideal.Quotient.mk Brel p) = coeff (bexp i) p := by
  rw [coordFun, dif_neg hi]
  exact Submodule.liftQ_apply _ _ p

/-- The coordinate map `Bcoord : B →ₗ[ZMod 2] (Fin 14 → ZMod 2)` assembled from
the `14` coordinate functionals. -/
noncomputable def Bcoord : B →ₗ[ZMod 2] (Fin 14 → ZMod 2) :=
  LinearMap.pi coordFun

@[simp] theorem Bcoord_apply (x : B) (i : Fin 14) : Bcoord x i = coordFun i x := rfl

/-! ### The basis family and the coordinate property `Bcoord (basisMon j) = e_j` -/

/-- The `14` basis monomials of `B`, as the quotient images of `monomial (bexp j) 1`. -/
noncomputable def basisMon (j : Fin 14) : B := Ideal.Quotient.mk Brel (monomial (bexp j) 1)

/-- The basis monomials in explicit product form, in `Sset` order. -/
theorem basisMon_eq (j : Fin 14) : basisMon j =
    ![1, a, b, c, d, a*a, a*b, a*c, a*d, b*b, b*d, c*c, c*d, d*d] j := by
  rw [basisMon, mk_mono_prod, bexp_apply, bexp_apply, bexp_apply, bexp_apply]
  fin_cases j <;> simp [pow_two]

/-- `coordFun i (basisMon j) = δ_{i,j}`: each coordinate functional reads off the
matching basis monomial and kills the others. -/
theorem coordFun_basisMon (i j : Fin 14) :
    coordFun i (basisMon j) = if i = j then 1 else 0 := by
  unfold basisMon
  by_cases hi : i = 8
  · subst hi
    rw [coordFun_eight_apply]
    by_cases hj : (8 : Fin 14) = j
    · rw [if_pos hj, ← hj, bexp_eight, ← X03_mon, phiP_X03]
    · rw [if_neg hj]
      -- bexp j ≠ mon03 and ≠ mon12, so phiP (monomial (bexp j) 1) = 0
      have hj8 : j ≠ 8 := fun h => hj h.symm
      unfold phiP
      rw [LinearMap.add_apply]
      simp only [lcoeff_apply]
      rw [coeff_monomial, coeff_monomial,
        if_neg (bexp_ne_mon03 hj8), if_neg (bexp_ne_mon12 j)]
      simp
  · rw [coordFun_apply hi, coeff_monomial]
    by_cases hij : i = j
    · subst hij; rw [if_pos rfl, if_pos rfl]
    · rw [if_neg hij, if_neg (fun h => hij (bexp_injective h).symm)]

/-- `Bcoord (basisMon j)` is the `j`-th standard basis vector `Pi.single j 1`. -/
theorem Bcoord_basisMon (j : Fin 14) : Bcoord (basisMon j) = Pi.single j 1 := by
  funext i
  rw [Bcoord_apply, coordFun_basisMon, Pi.single_apply]

/-! ### Linear independence, the basis, and the coordinate isomorphism -/

/-- The `14` basis monomials are `ZMod 2`-linearly independent: `Bcoord` is a left
inverse sending `basisMon j` to the standard vector `Pi.single j 1`. -/
theorem basisMon_linearIndependent : LinearIndependent (ZMod 2) basisMon := by
  apply LinearIndependent.of_comp Bcoord
  have : ⇑Bcoord ∘ basisMon = fun j => Pi.single j (1 : ZMod 2) := by
    funext j; exact Bcoord_basisMon j
  rw [this]
  exact Pi.linearIndependent_single_one (Fin 14) (ZMod 2)

/-- The range of `basisMon` is exactly the spanning set `Sset`. -/
theorem range_basisMon_eq_Sset : Set.range basisMon = Sset := by
  ext x
  simp only [Set.mem_range]
  constructor
  · rintro ⟨j, rfl⟩
    rw [basisMon_eq]
    unfold Sset
    fin_cases j <;> simp
  · intro hx
    simp only [Sset, Set.mem_insert_iff, Set.mem_singleton_iff] at hx
    rcases hx with h|h|h|h|h|h|h|h|h|h|h|h|h|h
    · exact ⟨0, by rw [basisMon_eq, h]; rfl⟩
    · exact ⟨1, by rw [basisMon_eq, h]; rfl⟩
    · exact ⟨2, by rw [basisMon_eq, h]; rfl⟩
    · exact ⟨3, by rw [basisMon_eq, h]; rfl⟩
    · exact ⟨4, by rw [basisMon_eq, h]; rfl⟩
    · exact ⟨5, by rw [basisMon_eq, h]; rfl⟩
    · exact ⟨6, by rw [basisMon_eq, h]; rfl⟩
    · exact ⟨7, by rw [basisMon_eq, h]; rfl⟩
    · exact ⟨8, by rw [basisMon_eq, h]; rfl⟩
    · exact ⟨9, by rw [basisMon_eq, h]; rfl⟩
    · exact ⟨10, by rw [basisMon_eq, h]; rfl⟩
    · exact ⟨11, by rw [basisMon_eq, h]; rfl⟩
    · exact ⟨12, by rw [basisMon_eq, h]; rfl⟩
    · exact ⟨13, by rw [basisMon_eq, h]; rfl⟩

/-- The `14` basis monomials span `B`. -/
theorem basisMon_span_top : ⊤ ≤ Submodule.span (ZMod 2) (Set.range basisMon) := by
  rw [range_basisMon_eq_Sset, span_Sset_eq_top]

/-- **The `𝔽₂`-basis of `B`**: the `14` monomials `1, a, …, d²` form a basis. -/
noncomputable def B_basis : Module.Basis (Fin 14) (ZMod 2) B :=
  Module.Basis.mk basisMon_linearIndependent basisMon_span_top

@[simp] theorem B_basis_apply (j : Fin 14) : B_basis j = basisMon j :=
  Module.Basis.mk_apply _ _ j

/-- The coordinate isomorphism `B ≃ₗ[ZMod 2] (Fin 14 → ZMod 2)`, with `Bcoord` as
forward map (the basis representation in standard coordinates). -/
noncomputable def Bequiv : B ≃ₗ[ZMod 2] (Fin 14 → ZMod 2) :=
  B_basis.repr.trans (Finsupp.linearEquivFunOnFinite (ZMod 2) (ZMod 2) (Fin 14))

/-! ### Finiteness corollaries -/

/-- `B` is a `Fintype` (via the coordinate isomorphism to `Fin 14 → ZMod 2`). -/
noncomputable instance instFintypeB : Fintype B :=
  Fintype.ofEquiv (Fin 14 → ZMod 2) Bequiv.toEquiv.symm

/-- `B` has decidable equality (via the coordinate isomorphism). -/
noncomputable instance instDecidableEqB : DecidableEq B :=
  fun x y => decidable_of_iff (Bequiv x = Bequiv y) Bequiv.injective.eq_iff

end Prob4b
