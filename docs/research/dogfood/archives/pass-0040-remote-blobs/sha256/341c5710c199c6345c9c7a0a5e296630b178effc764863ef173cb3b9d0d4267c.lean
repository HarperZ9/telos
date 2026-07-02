/-
Copyright (c) 2026 Prob4b formalization. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Prob4b formalization
-/
import Prob4b.Proofs.Amplify.Carrier

/-!
# Stage E (E3) — `R` is not quasi-coherent

This file proves the frozen theorem `R_not_quasi_coherent`: the amplified ring
`R = Δ(B) + C^(ℕ)` is **not** quasi-coherent.

**Strategy (BLUEPRINT E3, SKETCH Step 5 negative half).** Take the family
`triR := ![constR a, constR b, constR (a+b)] : Fin 3 → R` and the triple
intersection `J := ⨅ i, Ideal.span {triR i}`.

* *Every element of `J` has finite support.* The tail-constant ring hom
  `tail : R →+* B` sends `J` into `aB ∩ bB ∩ (a+b)B`, which is `⊥` by
  `B_triple_zero_proof`. So `tail g = 0` for `g ∈ J`, hence `g` is eventually
  `inlB 0 = 0` — finite support (`finite_support_of_mem_J`).

* *The defect can be placed in every coordinate.* For each `n`,
  `singleR n uC ∈ J` (`en_mem_J`), with the lifted defect `uC ≠ 0` (Stage D) at
  coordinate `n` and `0` elsewhere; these have pairwise disjoint supports.

* *No finite generating set works (`J_not_fg`).* If `J = Ideal.span ↑T` for a
  finite `T : Finset R`, then `T ⊆ J` so every generator is supported on the
  finite set `S₀ := T.sup suppOf`, whence `J = span T ⊆ suppIn S₀`. But for
  `n ∉ S₀`, `singleR n uC ∈ J` has nonzero value `uC` at coordinate `n ∉ S₀`,
  contradicting `singleR n uC ∈ suppIn S₀`. So `¬ J.FG`.

Then the `n = 3` instance of `QuasiCoherent`'s second clause fails, so
`¬ QuasiCoherent R`. This is the genuine disjoint-support non-finite-generation
argument (Stage-E cheat-watch: not "couldn't find generators").

See `BLUEPRINT.md` "Stage E — Amplification" (E3) and `PROGRESS.md`.
-/

namespace Prob4b

open TrivSqZeroExt

/-- The three principal generators `a, b, a+b`, lifted to `R` as constant tails. -/
noncomputable def triR : Fin 3 → R := ![constR a, constR b, constR (a + b)]

/-- `singleR n uC ∈ Ideal.span {constR x}` whenever `u ∈ smulSub x`: since
`uC = c · inlB x` in `C`, the element `singleR n c · constR x = singleR n uC`. -/
theorem singleR_uC_mem_span (n : ℕ) {x : B} (hx : u ∈ smulSub x) :
    singleR n uC ∈ Ideal.span {constR x} := by
  obtain ⟨c, hc⟩ := Ideal.mem_span_singleton'.mp (uC_mem_span_inlB hx)
  rw [Ideal.mem_span_singleton']
  exact ⟨singleR n c, by rw [singleR_mul_constR, hc]⟩

/-- For every coordinate `n`, the placed defect `singleR n uC` lies in the triple
intersection `J`. -/
theorem en_mem_J (n : ℕ) : singleR n uC ∈ ⨅ i, Ideal.span {triR i} := by
  rw [Ideal.mem_iInf]
  intro i
  fin_cases i
  · exact singleR_uC_mem_span n u_mem_a
  · exact singleR_uC_mem_span n u_mem_b
  · exact singleR_uC_mem_span n u_mem_ab

/-- The tail constant of any `J`-element lies in `aB ∩ bB ∩ (a+b)B`. -/
theorem tail_mem_triple (g : R) (hg : g ∈ ⨅ i, Ideal.span {triR i}) :
    tail g ∈ Ideal.span {a} ⊓ Ideal.span {b} ⊓ Ideal.span {a + b} := by
  rw [Ideal.mem_iInf] at hg
  have ha := hg 0
  have hb := hg 1
  have hab := hg 2
  simp only [triR, Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.head_cons,
    Matrix.cons_val_two, Matrix.tail_cons] at ha hb hab
  rw [Submodule.mem_inf, Submodule.mem_inf]
  refine ⟨⟨?_, ?_⟩, ?_⟩
  · obtain ⟨r, hr⟩ := Ideal.mem_span_singleton'.mp ha
    rw [Ideal.mem_span_singleton']
    exact ⟨tail r, by rw [show a = tail (constR a) from (tail_constR a).symm, ← map_mul, hr]⟩
  · obtain ⟨r, hr⟩ := Ideal.mem_span_singleton'.mp hb
    rw [Ideal.mem_span_singleton']
    exact ⟨tail r, by rw [show b = tail (constR b) from (tail_constR b).symm, ← map_mul, hr]⟩
  · obtain ⟨r, hr⟩ := Ideal.mem_span_singleton'.mp hab
    rw [Ideal.mem_span_singleton']
    exact ⟨tail r,
      by rw [show a + b = tail (constR (a + b)) from (tail_constR (a + b)).symm, ← map_mul, hr]⟩

/-- The tail constant of any `J`-element is `0` (by `B_triple_zero_proof`). -/
theorem tail_zero_of_mem_J (g : R) (hg : g ∈ ⨅ i, Ideal.span {triR i}) : tail g = 0 := by
  have := tail_mem_triple g hg
  rwa [B_triple_zero_proof, Ideal.mem_bot] at this

/-- Every element of `J` has finite support: off the exceptional set it is
`inlB (tail g) = inlB 0 = 0`. -/
theorem finite_support_of_mem_J (g : R) (hg : g ∈ ⨅ i, Ideal.span {triR i}) :
    ∃ s : Finset ℕ, ∀ k ∉ s, (g : ℕ → C) k = 0 := by
  obtain ⟨s, hs⟩ := tail_spec g
  refine ⟨s, fun k hk => ?_⟩
  rw [hs k hk, tail_zero_of_mem_J g hg, map_zero]

open Classical in
/-- A finite support set for `g` (the chosen one when `g ∈ J`, else `∅`). -/
noncomputable def suppOf (g : R) : Finset ℕ :=
  if h : g ∈ ⨅ i, Ideal.span {triR i} then (finite_support_of_mem_J g h).choose else ∅

theorem suppOf_spec (g : R) (hg : g ∈ ⨅ i, Ideal.span {triR i}) :
    ∀ k ∉ suppOf g, (g : ℕ → C) k = 0 := by
  rw [suppOf, dif_pos hg]
  exact (finite_support_of_mem_J g hg).choose_spec

/-- **The disjoint-support non-finite-generation argument.** The triple
intersection `J = ⨅ i, Ideal.span {triR i}` is not finitely generated: any
finite generating set is supported on finitely many coordinates, but `J` contains
the defect placed in *every* coordinate. -/
theorem J_not_fg : ¬ (⨅ i, Ideal.span {triR i}).FG := by
  rintro ⟨T, hT⟩
  set S₀ : Finset ℕ := T.sup suppOf with hS₀
  -- `J = span T` is contained in the sequences supported on `S₀`.
  have hsub : (⨅ i, Ideal.span {triR i}) ≤ suppIn S₀ := by
    rw [← hT, Ideal.span_le]
    intro t htmem
    have htJ : t ∈ ⨅ i, Ideal.span {triR i} := by rw [← hT]; exact Ideal.subset_span htmem
    rw [SetLike.mem_coe, mem_suppIn]
    intro k hk
    have hle : suppOf t ≤ S₀ := Finset.le_sup htmem
    exact suppOf_spec t htJ k (fun h => hk (hle h))
  -- A coordinate beyond `S₀` exhibits a `J`-element not supported on `S₀`.
  obtain ⟨n, hn⟩ := Infinite.exists_notMem_finset S₀
  have hmem : singleR n uC ∈ suppIn S₀ := hsub (en_mem_J n)
  rw [mem_suppIn] at hmem
  have hval := hmem n hn
  rw [singleR_apply_self] at hval
  exact uC_ne_zero hval

/-- **E3 — `R_not_quasi_coherent` (frozen type).** The amplified ring `R` is not
quasi-coherent: the `n = 3` instance of the arbitrary-finite principal
intersection clause fails on `triR`, since `⨅ i, Ideal.span {triR i}` is not
finitely generated (`J_not_fg`). -/
theorem R_not_quasi_coherent_proof : ¬ QuasiCoherent R := by
  intro h
  exact J_not_fg (h.2 3 triR)

end Prob4b
