/-
Copyright (c) 2026 Prob4b formalization. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Prob4b formalization
-/
import Prob4b.Proofs.Amplify.Carrier
import Prob4b.Proofs.Module.Basic

/-!
# Stage E (E2 + D1) — `R` is finite-conductor

This file proves the frozen theorem `R_finite_conductor`: the amplified ring
`R = Δ(B) + C^(ℕ)` is finite-conductor, i.e. every annihilator `annih x` and
every pairwise principal intersection `Ideal.span {x} ⊓ Ideal.span {y}` of `R`
is finitely generated.

**Strategy (BLUEPRINT E2, SKETCH Step 5 positive half).**

* *D1 — control in `C`.* For `x : B`, the idealization-level facts
  `C_annih : annih (inlB x) = (annih x).map inlB` and
  `C_pairwise : span {inlB x} ⊓ span {inlB y} = (span {x} ⊓ span {y}).map inlB`
  reduce annihilators and pairwise intersections of the diagonal copy in `C` to
  `B`-ideals (which are finitely generated, `B` being finite). They come from the
  Stage-B preservation theorems `M_annihilator_proof` /
  `M_pairwise_intersection_proof` and the square-zero split `C = B ⊕ M`.

* *The abstract f.g. lemma (`ideal_fg_of_local`).* An ideal `I ⊆ R` with a finite
  exceptional set `s` and a finite `Gb : Finset B` satisfying four local
  conditions — (h1) `tail I ⊆ span Gb`; (h2) at tail coordinates `g k ∈
  (span Gb).map inlB`; (h3) `I` is closed under placing a single coordinate
  (`singleR k (g k) ∈ I`); (h4) the tail generators `offS s g ∈ I` — is finitely
  generated. The explicit finite generating set is
  `(offS s '' Gb) ∪ (⋃ k ∈ s, singleR k '' {w | singleR k w ∈ I})`. Spanning
  uses: write `g = offS s (tail g) + g''` with `g''` of finite support, decompose
  `g''` coordinatewise, and route interior coordinates through (h3)/(h4) and tail
  coordinates through `singleR_tail_mem`.

* *Both halves.* `annih x` satisfies (h1)–(h4) with `Gb` generating `annih (tail x)`
  (via `C_annih`); `span {x} ⊓ span {y}` with `Gb` generating
  `span {tail x} ⊓ span {tail y}` (via `C_pairwise`). Hence both are f.g., giving
  `FiniteConductor R`.

There is **no** assumption that `R` is Noetherian or coherent — the finite
generating sets are exhibited explicitly from the *finite* exceptional support
plus the finitely generated tail `B`-ideal (Stage-E cheat-watch).

See `BLUEPRINT.md` "Stage E — Amplification" (E2, D1) and `PROGRESS.md`.
-/

namespace Prob4b

open TrivSqZeroExt

set_option maxHeartbeats 1000000 in
-- The deep `Module Bᵐᵒᵖ M` / opposite-action search over the quotient module
-- `M = B⁴/Bv` (and `Subring`/`Finset.univ : C` materialization) needs raised
-- heartbeat and recursion budgets, matching the project-wide instance budget.
set_option maxRecDepth 100000 in
/-- `C = B ⋉ M` is finite (`B`, `M` are finite). -/
instance instFiniteC : Finite C := by unfold C TrivSqZeroExt; infer_instance

/-! ### `offS` — the constant-tail element zeroed on a finite set -/

/-- The sequence equal to `inlB x` off `s` and `0` on `s`, as an element of `R`
(tail constant `x`, exceptional set `s`). The "tail generator" of `R`-ideals. -/
noncomputable def offS (s : Finset ℕ) (x : B) : R :=
  ⟨fun k => if k ∈ s then 0 else inlB x, ⟨x, s, fun k hk => by simp [hk]⟩⟩

theorem offS_apply_mem (s : Finset ℕ) (x : B) {k : ℕ} (hk : k ∈ s) :
    (offS s x : ℕ → C) k = 0 := by simp [offS, hk]

theorem offS_apply_not_mem (s : Finset ℕ) (x : B) {k : ℕ} (hk : k ∉ s) :
    (offS s x : ℕ → C) k = inlB x := by simp [offS, hk]

theorem singleR_apply (n : ℕ) (g : C) (k : ℕ) :
    (singleR n g : ℕ → C) k = if k = n then g else 0 := rfl

/-! ### Coordinate arithmetic of `singleR` and `offS` -/

set_option maxHeartbeats 1000000 in
-- The deep `Module Bᵐᵒᵖ M` / opposite-action search over the quotient module
-- `M = B⁴/Bv` (and `Subring`/`Finset.univ : C` materialization) needs raised
-- heartbeat and recursion budgets, matching the project-wide instance budget.
set_option maxRecDepth 100000 in
theorem singleR_mul_offS (k : ℕ) (c : C) (s : Finset ℕ) (x : B) (hk : k ∉ s) :
    (singleR k c * offS s x : R) = singleR k (c * inlB x) := by
  apply Subtype.ext; funext j
  rw [Subring.coe_mul, Pi.mul_apply, singleR_apply, singleR_apply]
  by_cases h : j = k
  · subst h; rw [if_pos rfl, if_pos rfl, offS_apply_not_mem s x hk]
  · rw [if_neg h, if_neg h, zero_mul]

set_option maxHeartbeats 1000000 in
-- The deep `Module Bᵐᵒᵖ M` / opposite-action search over the quotient module
-- `M = B⁴/Bv` (and `Subring`/`Finset.univ : C` materialization) needs raised
-- heartbeat and recursion budgets, matching the project-wide instance budget.
set_option maxRecDepth 100000 in
theorem singleR_add (n : ℕ) (g h : C) : singleR n (g + h) = singleR n g + singleR n h := by
  apply Subtype.ext; funext j
  rw [Subring.coe_add, Pi.add_apply, singleR_apply, singleR_apply, singleR_apply]
  by_cases hj : j = n
  · subst hj; simp
  · simp [hj]

set_option maxHeartbeats 1000000 in
-- The deep `Module Bᵐᵒᵖ M` / opposite-action search over the quotient module
-- `M = B⁴/Bv` (and `Subring`/`Finset.univ : C` materialization) needs raised
-- heartbeat and recursion budgets, matching the project-wide instance budget.
set_option maxRecDepth 100000 in
theorem singleR_zero (n : ℕ) : singleR n (0 : C) = 0 := by
  apply Subtype.ext; funext j; rw [singleR_apply, Subring.coe_zero]
  by_cases hj : j = n <;> simp [hj]

set_option maxHeartbeats 1000000 in
-- The deep `Module Bᵐᵒᵖ M` / opposite-action search over the quotient module
-- `M = B⁴/Bv` (and `Subring`/`Finset.univ : C` materialization) needs raised
-- heartbeat and recursion budgets, matching the project-wide instance budget.
set_option maxRecDepth 100000 in
theorem singleR_mul (n : ℕ) (g h : C) : singleR n (g * h) = singleR n g * singleR n h := by
  apply Subtype.ext; funext j
  rw [Subring.coe_mul, Pi.mul_apply, singleR_apply, singleR_apply, singleR_apply]
  by_cases hj : j = n
  · subst hj; simp
  · simp [hj]

set_option maxHeartbeats 1000000 in
-- The deep `Module Bᵐᵒᵖ M` / opposite-action search over the quotient module
-- `M = B⁴/Bv` (and `Subring`/`Finset.univ : C` materialization) needs raised
-- heartbeat and recursion budgets, matching the project-wide instance budget.
set_option maxRecDepth 100000 in
/-- For `k ∉ s` and `w ∈ (span Gb).map inlB`, the placed element `singleR k w`
lies in the `R`-ideal generated by the tail generators `offS s '' Gb`. -/
theorem singleR_tail_mem (s : Finset ℕ) (Gb : Set B) (k : ℕ) (hk : k ∉ s) (w : C)
    (hw : w ∈ (Ideal.span Gb).map inlB) :
    singleR k w ∈ Ideal.span ((fun g => offS s g) '' Gb) := by
  rw [Ideal.map_span, Ideal.span] at hw
  refine Submodule.span_induction ?_ ?_ ?_ ?_ hw
  · rintro _ ⟨g, hg, rfl⟩
    rw [show singleR k (inlB g) = singleR k 1 * offS s g from by
      rw [singleR_mul_offS k 1 s g hk, one_mul]]
    exact Ideal.mul_mem_left _ _ (Ideal.subset_span ⟨g, hg, rfl⟩)
  · rw [singleR_zero]; exact Submodule.zero_mem _
  · intro p q _ _ hp hq; rw [singleR_add]; exact Submodule.add_mem _ hp hq
  · intro c p _ hp
    rw [show c • p = c * p from rfl, singleR_mul]
    exact Ideal.mul_mem_left _ _ hp

set_option maxHeartbeats 1000000 in
-- The deep `Module Bᵐᵒᵖ M` / opposite-action search over the quotient module
-- `M = B⁴/Bv` (and `Subring`/`Finset.univ : C` materialization) needs raised
-- heartbeat and recursion budgets, matching the project-wide instance budget.
set_option maxRecDepth 100000 in
/-- Finite-support reconstruction: if `h` is supported on a finite set `T` and
each placed coordinate `singleR k (h k)` lies in the ideal `I`, then `h ∈ I`. -/
theorem mem_of_support_finite (I : Ideal R) (T : Finset ℕ) (h : R)
    (hsupp : ∀ k ∉ T, (h : ℕ → C) k = 0)
    (hcoord : ∀ k ∈ T, singleR k ((h : ℕ → C) k) ∈ I) : h ∈ I := by
  have key : h = ∑ k ∈ T, singleR k ((h : ℕ → C) k) := by
    apply Subtype.ext
    funext j
    rw [show ((∑ k ∈ T, singleR k ((h : ℕ → C) k) : R) : ℕ → C) j
        = ∑ k ∈ T, ((singleR k ((h : ℕ → C) k) : R) : ℕ → C) j from by
      rw [AddSubmonoidClass.coe_finsetSum, Finset.sum_apply]]
    by_cases hj : j ∈ T
    · rw [Finset.sum_eq_single j]
      · rw [singleR_apply_self]
      · intro k _ hkj
        rw [singleR_apply, if_neg (fun heq => hkj heq.symm)]
      · intro hjj; exact absurd hj hjj
    · rw [hsupp j hj, Finset.sum_eq_zero]
      intro k hk
      rw [singleR_apply, if_neg ?_]
      rintro rfl; exact hj hk
  rw [key]
  exact Ideal.sum_mem _ (fun k hk => hcoord k hk)

set_option maxHeartbeats 1000000 in
-- The deep `Module Bᵐᵒᵖ M` / opposite-action search over the quotient module
-- `M = B⁴/Bv` (and `Subring`/`Finset.univ : C` materialization) needs raised
-- heartbeat and recursion budgets, matching the project-wide instance budget.
set_option maxRecDepth 100000 in
theorem offS_add (s : Finset ℕ) (x y : B) : offS s (x + y) = offS s x + offS s y := by
  apply Subtype.ext; funext j
  rw [Subring.coe_add, Pi.add_apply]
  by_cases hj : j ∈ s
  · simp [offS_apply_mem s _ hj]
  · rw [offS_apply_not_mem s _ hj, offS_apply_not_mem s _ hj, offS_apply_not_mem s _ hj, map_add]

set_option maxHeartbeats 1000000 in
-- The deep `Module Bᵐᵒᵖ M` / opposite-action search over the quotient module
-- `M = B⁴/Bv` (and `Subring`/`Finset.univ : C` materialization) needs raised
-- heartbeat and recursion budgets, matching the project-wide instance budget.
set_option maxRecDepth 100000 in
theorem offS_zero (s : Finset ℕ) : offS s (0 : B) = 0 := by
  apply Subtype.ext; funext j
  by_cases hj : j ∈ s
  · rw [offS_apply_mem s _ hj]; rfl
  · rw [offS_apply_not_mem s _ hj, Subring.coe_zero]; simp

set_option maxHeartbeats 1000000 in
-- The deep `Module Bᵐᵒᵖ M` / opposite-action search over the quotient module
-- `M = B⁴/Bv` (and `Subring`/`Finset.univ : C` materialization) needs raised
-- heartbeat and recursion budgets, matching the project-wide instance budget.
set_option maxRecDepth 100000 in
theorem constR_mul_offS (s : Finset ℕ) (b x : B) :
    (constR b * offS s x : R) = offS s (b * x) := by
  apply Subtype.ext; funext j
  rw [Subring.coe_mul, Pi.mul_apply]
  by_cases hj : j ∈ s
  · rw [offS_apply_mem s _ hj, offS_apply_mem s _ hj, mul_zero]
  · rw [offS_apply_not_mem s _ hj, offS_apply_not_mem s _ hj, constR_apply, ← map_mul]

set_option maxHeartbeats 1000000 in
-- The deep `Module Bᵐᵒᵖ M` / opposite-action search over the quotient module
-- `M = B⁴/Bv` (and `Subring`/`Finset.univ : C` materialization) needs raised
-- heartbeat and recursion budgets, matching the project-wide instance budget.
set_option maxRecDepth 100000 in
/-- `offS s` carries `span Gb` into the `R`-ideal generated by `offS s '' Gb`. -/
theorem offS_mem_span (s : Finset ℕ) (Gb : Set B) (x : B) (hx : x ∈ Ideal.span Gb) :
    offS s x ∈ Ideal.span ((fun g => offS s g) '' Gb) := by
  refine Submodule.span_induction ?_ ?_ ?_ ?_ hx
  · intro g hg; exact Ideal.subset_span ⟨g, hg, rfl⟩
  · rw [offS_zero]; exact Submodule.zero_mem _
  · intro p q _ _ hp hq; rw [offS_add]; exact Submodule.add_mem _ hp hq
  · intro b p _ hp
    rw [show b • p = b * p from rfl, ← constR_mul_offS]
    exact Ideal.mul_mem_left _ _ hp

set_option maxHeartbeats 1000000 in
-- The deep `Module Bᵐᵒᵖ M` / opposite-action search over the quotient module
-- `M = B⁴/Bv` (and `Subring`/`Finset.univ : C` materialization) needs raised
-- heartbeat and recursion budgets, matching the project-wide instance budget.
set_option maxRecDepth 100000 in
/-- `offS s` carries `span Gb` into any ideal `I` containing the tail generators. -/
theorem offS_mem_ideal (I : Ideal R) (s : Finset ℕ) (Gb : Set B)
    (h4 : ∀ g ∈ Gb, offS s g ∈ I) (x : B) (hx : x ∈ Ideal.span Gb) : offS s x ∈ I := by
  refine Submodule.span_induction ?_ ?_ ?_ ?_ hx
  · intro g hg; exact h4 g hg
  · rw [offS_zero]; exact Submodule.zero_mem _
  · intro p q _ _ hp hq; rw [offS_add]; exact Submodule.add_mem _ hp hq
  · intro b p _ hp; rw [show b • p = b * p from rfl, ← constR_mul_offS]
    exact Ideal.mul_mem_left _ _ hp

/-! ### The finite generating set -/

/-- The interior generators of an ideal `I` over a finite coordinate set `s`:
all placed elements `singleR k w` (`k ∈ s`, `singleR k w ∈ I`). Finite, as `C` is
finite. -/
noncomputable def intGenSet (I : Ideal R) (s : Finset ℕ) : Set R :=
  ⋃ k ∈ s, (fun w => singleR k w) '' {w : C | singleR k w ∈ I}

theorem intGenSet_finite (I : Ideal R) (s : Finset ℕ) : (intGenSet I s).Finite := by
  apply Set.Finite.biUnion s.finite_toSet
  intro k _
  exact Set.Finite.image _ (Set.Finite.subset Set.finite_univ (Set.subset_univ _))

theorem singleR_mem_intGenSet (I : Ideal R) (s : Finset ℕ) (k : ℕ) (hk : k ∈ s) (w : C)
    (hw : singleR k w ∈ I) : singleR k w ∈ intGenSet I s := by
  rw [intGenSet, Set.mem_iUnion₂]
  exact ⟨k, hk, ⟨w, hw, rfl⟩⟩

/-- The full finite generating set: tail generators `offS s '' Gb` plus the
interior generators. -/
noncomputable def genSet (I : Ideal R) (s : Finset ℕ) (Gb : Set B) : Set R :=
  (fun g => offS s g) '' Gb ∪ intGenSet I s

theorem genSet_finite (I : Ideal R) (s : Finset ℕ) (Gb : Set B) (hGb : Gb.Finite) :
    (genSet I s Gb).Finite :=
  Set.Finite.union (Set.Finite.image _ hGb) (intGenSet_finite I s)

/-! ### The abstract finite-generation lemma -/

set_option maxHeartbeats 1000000 in
-- The deep `Module Bᵐᵒᵖ M` / opposite-action search over the quotient module
-- `M = B⁴/Bv` (and `Subring`/`Finset.univ : C` materialization) needs raised
-- heartbeat and recursion budgets, matching the project-wide instance budget.
set_option maxRecDepth 100000 in
/-- **The abstract f.g. lemma.** An ideal `I ⊆ R` with finite exceptional set `s`
and finite `Gb : Finset B` meeting the four local conditions is finitely
generated, with explicit generating set `genSet I s Gb`. -/
theorem ideal_fg_of_local (I : Ideal R) (s : Finset ℕ) (Gb : Finset B)
    (h1 : ∀ g ∈ I, tail g ∈ Ideal.span (↑Gb : Set B))
    (h2 : ∀ g ∈ I, ∀ k ∉ s, (g : ℕ → C) k ∈ (Ideal.span (↑Gb : Set B)).map inlB)
    (h3 : ∀ g ∈ I, ∀ k, singleR k ((g : ℕ → C) k) ∈ I)
    (h4 : ∀ g ∈ Gb, offS s g ∈ I) :
    I.FG := by
  have h4' : ∀ g ∈ (↑Gb : Set B), offS s g ∈ I := fun g hg => h4 g hg
  refine Submodule.fg_def.mpr ⟨genSet I s (↑Gb), genSet_finite I s (↑Gb) (Set.toFinite _), ?_⟩
  apply le_antisymm
  · rw [Ideal.span_le]
    rintro w (⟨g, hg, rfl⟩ | hw)
    · exact h4 g hg
    · rw [intGenSet, Set.mem_iUnion₂] at hw
      obtain ⟨k, _, w', hw', rfl⟩ := hw
      exact hw'
  · intro g hg
    have hty : tail g ∈ Ideal.span (↑Gb : Set B) := h1 g hg
    obtain ⟨sg, hsg⟩ := tail_spec g
    have htail_I : offS s (tail g) ∈ I := offS_mem_ideal I s (↑Gb) h4' (tail g) hty
    have htail_span : offS s (tail g) ∈ Ideal.span (genSet I s (↑Gb)) :=
      Ideal.span_mono (fun z hz => Or.inl hz) (offS_mem_span s (↑Gb) (tail g) hty)
    set g'' : R := g - offS s (tail g) with hg''def
    have hg''I : g'' ∈ I := Ideal.sub_mem _ hg htail_I
    have hcoeff : ∀ k, (g'' : ℕ → C) k = (g : ℕ → C) k - (offS s (tail g) : ℕ → C) k := by
      intro k; rw [hg''def, AddSubgroupClass.coe_sub]; rfl
    have hsupp : ∀ k ∉ (s ∪ sg), (g'' : ℕ → C) k = 0 := by
      intro k hk
      rw [Finset.mem_union, not_or] at hk
      obtain ⟨hks, hksg⟩ := hk
      rw [hcoeff, hsg k hksg, offS_apply_not_mem s _ hks, sub_self]
    have hcoord : ∀ k ∈ (s ∪ sg),
        singleR k ((g'' : ℕ → C) k) ∈ Ideal.span (genSet I s (↑Gb)) := by
      intro k _
      by_cases hks : k ∈ s
      · have hin : singleR k ((g'' : ℕ → C) k) ∈ I := h3 g'' hg''I k
        exact Ideal.subset_span (Or.inr (singleR_mem_intGenSet I s k hks _ hin))
      · have hk2 : (g : ℕ → C) k ∈ (Ideal.span (↑Gb : Set B)).map inlB := h2 g hg k hks
        have hk3 : (offS s (tail g) : ℕ → C) k = inlB (tail g) := offS_apply_not_mem s _ hks
        have hinlBmem : inlB (tail g) ∈ (Ideal.span (↑Gb : Set B)).map inlB :=
          Ideal.mem_map_of_mem inlB hty
        have hmem : (g'' : ℕ → C) k ∈ (Ideal.span (↑Gb : Set B)).map inlB := by
          rw [hcoeff, hk3]; exact Ideal.sub_mem _ hk2 hinlBmem
        have := singleR_tail_mem s (↑Gb) k hks _ hmem
        exact Ideal.span_mono (fun z hz => Or.inl hz) this
    have hg''span : g'' ∈ Ideal.span (genSet I s (↑Gb)) :=
      mem_of_support_finite _ (s ∪ sg) g'' hsupp hcoord
    have hsplit : g = offS s (tail g) + g'' := by rw [hg''def]; ring
    rw [hsplit]
    exact Ideal.add_mem _ htail_span hg''span

/-! ### D1 — annihilators and pairwise intersections in `C` -/

set_option maxHeartbeats 1000000 in
-- The deep `Module Bᵐᵒᵖ M` / opposite-action search over the quotient module
-- `M = B⁴/Bv` (and `Subring`/`Finset.univ : C` materialization) needs raised
-- heartbeat and recursion budgets, matching the project-wide instance budget.
set_option maxRecDepth 100000 in
theorem fst_inlB_mul (x : B) (c : C) : (inlB x * c).fst = x * c.fst := by
  rw [show inlB x = TrivSqZeroExt.inl x from rfl, TrivSqZeroExt.fst_mul, TrivSqZeroExt.fst_inl]

set_option maxHeartbeats 1000000 in
-- The deep `Module Bᵐᵒᵖ M` / opposite-action search over the quotient module
-- `M = B⁴/Bv` (and `Subring`/`Finset.univ : C` materialization) needs raised
-- heartbeat and recursion budgets, matching the project-wide instance budget.
set_option maxRecDepth 100000 in
theorem snd_inlB_mul (x : B) (c : C) : (inlB x * c).snd = x • c.snd := by
  rw [show inlB x = TrivSqZeroExt.inl x from rfl, TrivSqZeroExt.snd_mul, TrivSqZeroExt.fst_inl,
    TrivSqZeroExt.snd_inl]; simp

set_option maxHeartbeats 1000000 in
-- The deep `Module Bᵐᵒᵖ M` / opposite-action search over the quotient module
-- `M = B⁴/Bv` (and `Subring`/`Finset.univ : C` materialization) needs raised
-- heartbeat and recursion budgets, matching the project-wide instance budget.
set_option maxRecDepth 100000 in
theorem mem_annih_inlB (x : B) (c : C) :
    c ∈ annih (inlB x) ↔ x * c.fst = 0 ∧ x • c.snd = 0 := by
  rw [show (c ∈ annih (inlB x)) ↔ (inlB x) * c = 0 from by
    unfold annih
    rw [LinearMap.mem_ker, show LinearMap.lsmul C C (inlB x) c = inlB x * c from rfl]]
  constructor
  · intro h
    exact ⟨by rw [← fst_inlB_mul, h]; rfl, by rw [← snd_inlB_mul, h]; rfl⟩
  · intro ⟨h1, h2⟩
    exact TrivSqZeroExt.ext (by rw [fst_inlB_mul, h1]; rfl) (by rw [snd_inlB_mul, h2]; rfl)

set_option maxHeartbeats 1000000 in
-- The deep `Module Bᵐᵒᵖ M` / opposite-action search over the quotient module
-- `M = B⁴/Bv` (and `Subring`/`Finset.univ : C` materialization) needs raised
-- heartbeat and recursion budgets, matching the project-wide instance budget.
set_option maxRecDepth 100000 in
/-- **D1 (annihilator).** `annih (inlB x) = (annih x).map inlB` in `C`. -/
theorem C_annih (x : B) : annih (inlB x) = (annih x).map inlB := by
  apply le_antisymm
  · intro c hc
    rw [mem_annih_inlB] at hc
    obtain ⟨hfst, hsnd⟩ := hc
    have hfstmem : c.fst ∈ annih x := by rw [mem_annih_iff]; rw [mul_comm] at hfst; exact hfst
    have hsndmem : c.snd ∈ annihM x := by
      unfold annihM
      rw [LinearMap.mem_ker, show LinearMap.lsmul B M x c.snd = x • c.snd from rfl]
      exact hsnd
    rw [M_annihilator_proof] at hsndmem
    rw [show c = TrivSqZeroExt.inl c.fst + TrivSqZeroExt.inr c.snd from
      (TrivSqZeroExt.inl_fst_add_inr_snd_eq c).symm]
    apply Ideal.add_mem
    · exact Ideal.mem_map_of_mem inlB hfstmem
    · refine Submodule.smul_induction_on hsndmem ?_ ?_
      · intro r hr n _
        rw [show (TrivSqZeroExt.inr (r • n) : C) = inlB r * TrivSqZeroExt.inr n from
          (inlB_mul_inr r n).symm]
        exact Ideal.mul_mem_right _ _ (Ideal.mem_map_of_mem inlB hr)
      · intro p q hp hq
        rw [TrivSqZeroExt.inr_add]; exact Ideal.add_mem _ hp hq
  · rw [Ideal.map_le_iff_le_comap]
    intro g hg
    rw [Ideal.mem_comap, mem_annih_inlB]
    rw [mem_annih_iff] at hg
    refine ⟨?_, ?_⟩
    · show x * (inlB g).fst = 0; rw [show (inlB g).fst = g from rfl, mul_comm]; exact hg
    · show x • (inlB g).snd = 0; rw [show (inlB g).snd = 0 from rfl, smul_zero]

set_option maxHeartbeats 1000000 in
-- The deep `Module Bᵐᵒᵖ M` / opposite-action search over the quotient module
-- `M = B⁴/Bv` (and `Subring`/`Finset.univ : C` materialization) needs raised
-- heartbeat and recursion budgets, matching the project-wide instance budget.
set_option maxRecDepth 100000 in
theorem span_inlB (x : B) : Ideal.span {inlB x} = (Ideal.span {x}).map inlB := by
  rw [Ideal.map_span]; simp

set_option maxHeartbeats 1000000 in
-- The deep `Module Bᵐᵒᵖ M` / opposite-action search over the quotient module
-- `M = B⁴/Bv` (and `Subring`/`Finset.univ : C` materialization) needs raised
-- heartbeat and recursion budgets, matching the project-wide instance budget.
set_option maxRecDepth 100000 in
theorem mem_span_inlB (x : B) (g : C) :
    g ∈ Ideal.span {inlB x} ↔ g.fst ∈ Ideal.span {x} ∧ g.snd ∈ smulSub x := by
  constructor
  · intro hg
    rw [Ideal.mem_span_singleton'] at hg
    obtain ⟨cc, rfl⟩ := hg
    refine ⟨?_, ?_⟩
    · rw [show (cc * inlB x).fst = cc.fst * x from by
        rw [show inlB x = TrivSqZeroExt.inl x from rfl, TrivSqZeroExt.fst_mul,
          TrivSqZeroExt.fst_inl]]
      exact Ideal.mul_mem_left _ _ (Ideal.mem_span_singleton_self x)
    · rw [show (cc * inlB x).snd = x • cc.snd from by
        rw [show inlB x = TrivSqZeroExt.inl x from rfl, TrivSqZeroExt.snd_mul,
          TrivSqZeroExt.fst_inl, TrivSqZeroExt.snd_inl]; simp]
      exact Submodule.smul_mem_smul (Ideal.mem_span_singleton_self x) Submodule.mem_top
  · intro ⟨h1, h2⟩
    rw [Ideal.mem_span_singleton'] at h1 ⊢
    obtain ⟨r, hr⟩ := h1
    obtain ⟨mm, hm⟩ := exists_smul_eq_of_mem_smulSub h2
    refine ⟨TrivSqZeroExt.inl r + TrivSqZeroExt.inr mm, ?_⟩
    apply TrivSqZeroExt.ext
    · rw [TrivSqZeroExt.fst_mul]
      simp only [TrivSqZeroExt.fst_add, TrivSqZeroExt.fst_inl, TrivSqZeroExt.fst_inr, add_zero]
      rw [show (inlB x).fst = x from rfl, hr]
    · rw [TrivSqZeroExt.snd_mul]
      simp only [TrivSqZeroExt.snd_add, TrivSqZeroExt.snd_inl, TrivSqZeroExt.snd_inr,
        TrivSqZeroExt.fst_add, TrivSqZeroExt.fst_inl, TrivSqZeroExt.fst_inr, add_zero, zero_add]
      rw [show (inlB x).fst = x from rfl, show (inlB x).snd = 0 from rfl]
      simp [hm]

set_option maxHeartbeats 1000000 in
-- The deep `Module Bᵐᵒᵖ M` / opposite-action search over the quotient module
-- `M = B⁴/Bv` (and `Subring`/`Finset.univ : C` materialization) needs raised
-- heartbeat and recursion budgets, matching the project-wide instance budget.
set_option maxRecDepth 100000 in
/-- **D1 (pairwise intersection).**
`span {inlB x} ⊓ span {inlB y} = (span {x} ⊓ span {y}).map inlB` in `C`. -/
theorem C_pairwise (x y : B) :
    Ideal.span {inlB x} ⊓ Ideal.span {inlB y}
      = (Ideal.span {x} ⊓ Ideal.span {y}).map inlB := by
  apply le_antisymm
  · intro g hg
    rw [Submodule.mem_inf, mem_span_inlB, mem_span_inlB] at hg
    obtain ⟨⟨hf1, hs1⟩, hf2, hs2⟩ := hg
    have hfst : g.fst ∈ Ideal.span {x} ⊓ Ideal.span {y} := ⟨hf1, hf2⟩
    have hsnd : g.snd ∈ smulSub x ⊓ smulSub y := ⟨hs1, hs2⟩
    rw [M_pairwise_intersection_proof] at hsnd
    rw [show g = TrivSqZeroExt.inl g.fst + TrivSqZeroExt.inr g.snd from
      (TrivSqZeroExt.inl_fst_add_inr_snd_eq g).symm]
    apply Ideal.add_mem
    · exact Ideal.mem_map_of_mem inlB hfst
    · refine Submodule.smul_induction_on hsnd ?_ ?_
      · intro r hr n _
        rw [show (TrivSqZeroExt.inr (r • n) : C) = inlB r * TrivSqZeroExt.inr n from
          (inlB_mul_inr r n).symm]
        exact Ideal.mul_mem_right _ _ (Ideal.mem_map_of_mem inlB hr)
      · intro p q hp hq
        rw [TrivSqZeroExt.inr_add]; exact Ideal.add_mem _ hp hq
  · rw [Ideal.map_le_iff_le_comap]
    intro w hw
    rw [Submodule.mem_inf] at hw
    obtain ⟨hwx, hwy⟩ := hw
    rw [Ideal.mem_comap, Submodule.mem_inf]
    constructor
    · rw [span_inlB]; exact Ideal.mem_map_of_mem inlB hwx
    · rw [span_inlB]; exact Ideal.mem_map_of_mem inlB hwy

/-! ### Coordinatewise membership in `R` -/

set_option maxHeartbeats 1000000 in
-- The deep `Module Bᵐᵒᵖ M` / opposite-action search over the quotient module
-- `M = B⁴/Bv` (and `Subring`/`Finset.univ : C` materialization) needs raised
-- heartbeat and recursion budgets, matching the project-wide instance budget.
set_option maxRecDepth 100000 in
theorem mem_annih_R (x y : R) : y ∈ annih x ↔ ∀ k, (y : ℕ → C) k * (x : ℕ → C) k = 0 := by
  rw [show (y ∈ annih x) ↔ x * y = 0 from by
    unfold annih
    rw [LinearMap.mem_ker, show LinearMap.lsmul R R x y = x * y from rfl]]
  constructor
  · intro h k
    have : ((x * y : R) : ℕ → C) k = 0 := by rw [h]; rfl
    rwa [Subring.coe_mul, Pi.mul_apply, mul_comm] at this
  · intro h
    apply Subtype.ext; funext k
    rw [Subring.coe_mul, Pi.mul_apply, Subring.coe_zero, Pi.zero_apply, mul_comm]
    exact h k

set_option maxHeartbeats 1000000 in
-- The deep `Module Bᵐᵒᵖ M` / opposite-action search over the quotient module
-- `M = B⁴/Bv` (and `Subring`/`Finset.univ : C` materialization) needs raised
-- heartbeat and recursion budgets, matching the project-wide instance budget.
set_option maxRecDepth 100000 in
theorem mem_span_R_singleton (x g : R) : g ∈ Ideal.span {x} ↔ ∃ r : R, g = r * x := by
  rw [Ideal.mem_span_singleton']
  constructor
  · rintro ⟨r, rfl⟩; exact ⟨r, by rw [mul_comm]⟩
  · rintro ⟨r, rfl⟩; exact ⟨r, by rw [mul_comm]⟩

set_option maxHeartbeats 1000000 in
-- The deep `Module Bᵐᵒᵖ M` / opposite-action search over the quotient module
-- `M = B⁴/Bv` (and `Subring`/`Finset.univ : C` materialization) needs raised
-- heartbeat and recursion budgets, matching the project-wide instance budget.
set_option maxRecDepth 100000 in
theorem coord_mem_span_C (x g : R) (hg : g ∈ Ideal.span {x}) (k : ℕ) :
    (g : ℕ → C) k ∈ Ideal.span {(x : ℕ → C) k} := by
  obtain ⟨r, rfl⟩ := (mem_span_R_singleton x g).mp hg
  rw [Subring.coe_mul, Pi.mul_apply, Ideal.mem_span_singleton']
  exact ⟨(r : ℕ → C) k, rfl⟩

set_option maxHeartbeats 1000000 in
-- The deep `Module Bᵐᵒᵖ M` / opposite-action search over the quotient module
-- `M = B⁴/Bv` (and `Subring`/`Finset.univ : C` materialization) needs raised
-- heartbeat and recursion budgets, matching the project-wide instance budget.
set_option maxRecDepth 100000 in
theorem singleR_coord_mem_span (x g : R) (hg : g ∈ Ideal.span {x}) (k : ℕ) :
    singleR k ((g : ℕ → C) k) ∈ Ideal.span {x} := by
  obtain ⟨r, rfl⟩ := (mem_span_R_singleton x g).mp hg
  rw [mem_span_R_singleton]
  refine ⟨singleR k ((r : ℕ → C) k), ?_⟩
  apply Subtype.ext; funext j
  simp only [Subring.coe_mul, Pi.mul_apply, singleR_apply]
  by_cases hj : j = k
  · subst hj; rw [if_pos rfl, if_pos rfl]
  · rw [if_neg hj, if_neg hj, zero_mul]

set_option maxHeartbeats 1000000 in
-- The deep `Module Bᵐᵒᵖ M` / opposite-action search over the quotient module
-- `M = B⁴/Bv` (and `Subring`/`Finset.univ : C` materialization) needs raised
-- heartbeat and recursion budgets, matching the project-wide instance budget.
set_option maxRecDepth 100000 in
theorem offS_one_mul_eq (x : R) (s : Finset ℕ) (hs : ∀ n ∉ s, (x : ℕ → C) n = inlB (tail x)) :
    (offS s (1 : B) * x : R) = offS s (tail x) := by
  apply Subtype.ext; funext j
  rw [Subring.coe_mul, Pi.mul_apply]
  by_cases hj : j ∈ s
  · rw [offS_apply_mem s _ hj, offS_apply_mem s _ hj, zero_mul]
  · rw [offS_apply_not_mem s _ hj, offS_apply_not_mem s _ hj, hs j hj, map_one, one_mul]

set_option maxHeartbeats 1000000 in
-- The deep `Module Bᵐᵒᵖ M` / opposite-action search over the quotient module
-- `M = B⁴/Bv` (and `Subring`/`Finset.univ : C` materialization) needs raised
-- heartbeat and recursion budgets, matching the project-wide instance budget.
set_option maxRecDepth 100000 in
theorem offS_mem_span_R (x : R) (s : Finset ℕ) (hs : ∀ n ∉ s, (x : ℕ → C) n = inlB (tail x))
    (g : B) (hg : g ∈ Ideal.span {tail x}) : offS s g ∈ Ideal.span {x} := by
  obtain ⟨b, hb⟩ := Ideal.mem_span_singleton'.mp hg
  rw [← hb, ← constR_mul_offS, ← offS_one_mul_eq x s hs]
  rw [mem_span_R_singleton]
  exact ⟨constR b * offS s 1, by ring⟩

/-! ### The two finite-conductor halves -/

set_option maxHeartbeats 1000000 in
-- The deep `Module Bᵐᵒᵖ M` / opposite-action search over the quotient module
-- `M = B⁴/Bv` (and `Subring`/`Finset.univ : C` materialization) needs raised
-- heartbeat and recursion budgets, matching the project-wide instance budget.
set_option maxRecDepth 100000 in
/-- Every annihilator `annih x` of `R` is finitely generated. -/
theorem R_annih_fg (x : R) : (annih x).FG := by
  haveI : IsNoetherian B B := isNoetherian_of_finite B B
  obtain ⟨Gb, hGb⟩ := (isNoetherian_def.mp inferInstance) (annih (tail x))
  obtain ⟨s, hs⟩ := tail_spec x
  apply ideal_fg_of_local (annih x) s Gb
  · intro y hy
    rw [show Ideal.span (↑Gb : Set B) = annih (tail x) from hGb, mem_annih_iff]
    rw [mem_annih_R] at hy
    have hyx : x * y = 0 := by
      apply Subtype.ext; funext k
      rw [Subring.coe_mul, Pi.mul_apply, Subring.coe_zero, Pi.zero_apply, mul_comm]
      exact hy k
    have : tail x * tail y = 0 := by rw [← map_mul, hyx, map_zero]
    rw [mul_comm]; exact this
  · intro y hy k hk
    rw [show Ideal.span (↑Gb : Set B) = annih (tail x) from hGb, ← C_annih]
    rw [mem_annih_R] at hy
    rw [show (y : ℕ → C) k ∈ annih (inlB (tail x)) ↔ inlB (tail x) * (y : ℕ → C) k = 0 from by
      unfold annih
      rw [LinearMap.mem_ker, show LinearMap.lsmul C C (inlB (tail x)) ((y : ℕ → C) k)
        = inlB (tail x) * (y : ℕ → C) k from rfl]]
    rw [← hs k hk, mul_comm]; exact hy k
  · intro y hy k
    rw [mem_annih_R] at hy ⊢
    intro j
    rw [singleR_apply]
    by_cases hj : j = k
    · subst hj; rw [if_pos rfl]; exact hy j
    · rw [if_neg hj, zero_mul]
  · intro g hg
    have hgann : g ∈ annih (tail x) := by
      rw [show annih (tail x) = Ideal.span (↑Gb : Set B) from hGb.symm]; exact Ideal.subset_span hg
    rw [mem_annih_iff] at hgann
    rw [mem_annih_R]
    intro k
    by_cases hks : k ∈ s
    · rw [offS_apply_mem s g hks, zero_mul]
    · rw [offS_apply_not_mem s g hks, hs k hks, ← map_mul]
      rw [show g * tail x = 0 from hgann, map_zero]

set_option maxHeartbeats 1000000 in
-- The deep `Module Bᵐᵒᵖ M` / opposite-action search over the quotient module
-- `M = B⁴/Bv` (and `Subring`/`Finset.univ : C` materialization) needs raised
-- heartbeat and recursion budgets, matching the project-wide instance budget.
set_option maxRecDepth 100000 in
/-- Every pairwise principal intersection `span {x} ⊓ span {y}` of `R` is
finitely generated. -/
theorem R_inter_fg (x y : R) : (Ideal.span {x} ⊓ Ideal.span {y}).FG := by
  haveI : IsNoetherian B B := isNoetherian_of_finite B B
  obtain ⟨Gb, hGb⟩ := (isNoetherian_def.mp inferInstance)
    (Ideal.span {tail x} ⊓ Ideal.span {tail y})
  obtain ⟨sx, hsx⟩ := tail_spec x
  obtain ⟨sy, hsy⟩ := tail_spec y
  apply ideal_fg_of_local (Ideal.span {x} ⊓ Ideal.span {y}) (sx ∪ sy) Gb
  · intro g hg
    rw [Submodule.mem_inf] at hg
    obtain ⟨hgx, hgy⟩ := hg
    rw [show Ideal.span (↑Gb : Set B) = Ideal.span {tail x} ⊓ Ideal.span {tail y} from hGb,
      Submodule.mem_inf]
    obtain ⟨rx, hrx⟩ := (mem_span_R_singleton x g).mp hgx
    obtain ⟨ry, hry⟩ := (mem_span_R_singleton y g).mp hgy
    refine ⟨?_, ?_⟩
    · rw [Ideal.mem_span_singleton']
      exact ⟨tail rx, by rw [← map_mul, ← hrx]⟩
    · rw [Ideal.mem_span_singleton']
      exact ⟨tail ry, by rw [← map_mul, ← hry]⟩
  · intro g hg k hk
    rw [Finset.mem_union, not_or] at hk
    obtain ⟨hkx, hky⟩ := hk
    rw [Submodule.mem_inf] at hg
    obtain ⟨hgx, hgy⟩ := hg
    rw [show Ideal.span (↑Gb : Set B) = Ideal.span {tail x} ⊓ Ideal.span {tail y} from hGb,
      ← C_pairwise, Submodule.mem_inf]
    refine ⟨?_, ?_⟩
    · have := coord_mem_span_C x g hgx k
      rwa [hsx k hkx] at this
    · have := coord_mem_span_C y g hgy k
      rwa [hsy k hky] at this
  · intro g hg k
    rw [Submodule.mem_inf] at hg ⊢
    obtain ⟨hgx, hgy⟩ := hg
    exact ⟨singleR_coord_mem_span x g hgx k, singleR_coord_mem_span y g hgy k⟩
  · intro gg hgg
    have hggmem : gg ∈ Ideal.span {tail x} ⊓ Ideal.span {tail y} := by
      rw [show Ideal.span {tail x} ⊓ Ideal.span {tail y} = Ideal.span (↑Gb : Set B) from hGb.symm]
      exact Ideal.subset_span hgg
    rw [Submodule.mem_inf] at hggmem
    obtain ⟨hggx, hggy⟩ := hggmem
    rw [Submodule.mem_inf]
    constructor
    · apply offS_mem_span_R x (sx ∪ sy) _ gg hggx
      intro n hn; exact hsx n (fun h => hn (Finset.mem_union_left _ h))
    · apply offS_mem_span_R y (sx ∪ sy) _ gg hggy
      intro n hn; exact hsy n (fun h => hn (Finset.mem_union_right _ h))

set_option maxHeartbeats 1000000 in
-- The deep `Module Bᵐᵒᵖ M` / opposite-action search over the quotient module
-- `M = B⁴/Bv` (and `Subring`/`Finset.univ : C` materialization) needs raised
-- heartbeat and recursion budgets, matching the project-wide instance budget.
set_option maxRecDepth 100000 in
/-- **E2 — `R_finite_conductor` (frozen type).** The amplified ring `R` is
finite-conductor: every annihilator (`R_annih_fg`) and every pairwise principal
intersection (`R_inter_fg`) is finitely generated. -/
theorem R_finite_conductor_proof : FiniteConductor R := ⟨R_annih_fg, R_inter_fg⟩

end Prob4b
