/-
Copyright (c) 2026 Prob4b formalization. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Prob4b formalization
-/
import Prob4b.Proofs.Idealization.Basic

/-!
# Stage E (E1) — Carrier plumbing for the amplification `R = Δ(B) + C^(ℕ)`

This file pins down the coordinatewise structure of the frozen subring
`R = Rsub ⊆ (ℕ → C)` of sequences that are *eventually equal to a constant
element `inlB x` of the diagonal copy `Δ(B)`*.

Main contents:

* `tail : R →+* B` — the **tail-constant** ring homomorphism. Every `f : R` is
  eventually `inlB (tail f)` off a finite exceptional set; this value is unique
  (because `inlB` is injective and `ℕ` is infinite), so `tail` is a well-defined
  ring hom. This is the bridge to the base ring `B` used throughout Stage E.
* `constR x : R` — the constant sequence `inlB x` (`tail (constR x) = x`).
* `singleR n g : R` — the sequence equal to `g : C` at coordinate `n` and `0`
  elsewhere (tail constant `0`, finite support `{n}`); the "place the defect in
  coordinate `n`" building block for E3.
* `suppIn S : Ideal R` — the ideal of sequences supported on a finite set `S`.

See `BLUEPRINT.md` "Stage E — Amplification" (E1) and `PROGRESS.md`.
-/

namespace Prob4b

open TrivSqZeroExt

/-! ### `inlB` is injective -/

/-- The diagonal embedding `inlB : B →+* C` is injective (its first component is
the identity: `(inlB x).fst = x`). -/
theorem inlB_injective : Function.Injective inlB := fun x y h => by
  have : (inlB x).fst = (inlB y).fst := by rw [h]
  rwa [show (inlB x).fst = x from rfl, show (inlB y).fst = y from rfl] at this

/-! ### The tail-constant value and its uniqueness -/

/-- The eventual-constant tail value `tailVal f ∈ B` of `f : R`: the unique
`x : B` with `f n = inlB x` off a finite set. Chosen from the carrier witness. -/
noncomputable def tailVal (f : R) : B := Classical.choose f.2

/-- `f` is eventually equal to `inlB (tailVal f)`. -/
theorem tailVal_spec (f : R) :
    ∃ s : Finset ℕ, ∀ n ∉ s, (f : ℕ → C) n = inlB (tailVal f) :=
  Classical.choose_spec f.2

/-- Uniqueness of the tail value: any constant `x` valid off a finite set equals
`tailVal f`. -/
theorem tailVal_unique (f : R) (x : B) (s : Finset ℕ)
    (h : ∀ n ∉ s, (f : ℕ → C) n = inlB x) : x = tailVal f := by
  obtain ⟨t, ht⟩ := tailVal_spec f
  obtain ⟨n, hn⟩ := Infinite.exists_notMem_finset (s ∪ t)
  have h1 := h n (fun hm => hn (Finset.mem_union_left _ hm))
  have h2 := ht n (fun hm => hn (Finset.mem_union_right _ hm))
  exact inlB_injective (h1 ▸ h2 ▸ rfl)

/-! ### `tail : R →+* B` -/

theorem tailVal_one : tailVal (1 : R) = 1 :=
  (tailVal_unique 1 1 ∅ (fun n _ => by change (1 : ℕ → C) n = inlB 1; simp)).symm

theorem tailVal_zero : tailVal (0 : R) = 0 :=
  (tailVal_unique 0 0 ∅ (fun n _ => by change (0 : ℕ → C) n = inlB 0; simp)).symm

theorem tailVal_add (f g : R) : tailVal (f + g) = tailVal f + tailVal g := by
  obtain ⟨s, hs⟩ := tailVal_spec f
  obtain ⟨t, ht⟩ := tailVal_spec g
  refine (tailVal_unique (f + g) _ (s ∪ t) (fun n hn => ?_)).symm
  change ((f : ℕ → C) + (g : ℕ → C)) n = inlB (tailVal f + tailVal g)
  rw [Pi.add_apply, hs n (fun hm => hn (Finset.mem_union_left _ hm)),
    ht n (fun hm => hn (Finset.mem_union_right _ hm)), map_add]

theorem tailVal_mul (f g : R) : tailVal (f * g) = tailVal f * tailVal g := by
  obtain ⟨s, hs⟩ := tailVal_spec f
  obtain ⟨t, ht⟩ := tailVal_spec g
  refine (tailVal_unique (f * g) _ (s ∪ t) (fun n hn => ?_)).symm
  change ((f : ℕ → C) * (g : ℕ → C)) n = inlB (tailVal f * tailVal g)
  rw [Pi.mul_apply, hs n (fun hm => hn (Finset.mem_union_left _ hm)),
    ht n (fun hm => hn (Finset.mem_union_right _ hm)), map_mul]

/-- The **tail-constant ring homomorphism** `tail : R →+* B`, `f ↦ tailVal f`. -/
noncomputable def tail : R →+* B where
  toFun := tailVal
  map_one' := tailVal_one
  map_mul' := tailVal_mul
  map_zero' := tailVal_zero
  map_add' := tailVal_add

@[simp] theorem tail_apply (f : R) : tail f = tailVal f := rfl

theorem tail_spec (f : R) : ∃ s : Finset ℕ, ∀ n ∉ s, (f : ℕ → C) n = inlB (tail f) :=
  tailVal_spec f

/-! ### Constant and single-coordinate elements -/

/-- The constant sequence `inlB x : ℕ → C`, as an element of `R` (tail constant
`x`, empty exceptional set). -/
noncomputable def constR (x : B) : R := ⟨fun _ => inlB x, ⟨x, ∅, fun _ _ => rfl⟩⟩

@[simp] theorem constR_apply (x : B) (n : ℕ) : (constR x : ℕ → C) n = inlB x := rfl

@[simp] theorem tail_constR (x : B) : tail (constR x) = x :=
  (tailVal_unique (constR x) x ∅ (fun _ _ => rfl)).symm

/-- The sequence equal to `g : C` at coordinate `n` and `0` elsewhere, as an
element of `R` (tail constant `0`, exceptional set `{n}`). -/
noncomputable def singleR (n : ℕ) (g : C) : R :=
  ⟨fun k => if k = n then g else 0, ⟨0, {n}, fun k hk => by
    simp only; rw [if_neg (by simpa using hk)]; simp⟩⟩

@[simp] theorem singleR_apply_self (n : ℕ) (g : C) : (singleR n g : ℕ → C) n = g := by
  simp [singleR]

theorem singleR_apply_of_ne (n : ℕ) (g : C) {k : ℕ} (h : k ≠ n) :
    (singleR n g : ℕ → C) k = 0 := by simp [singleR, h]

/-- Multiplying a single-coordinate element by a constant keeps it single. -/
theorem singleR_mul_constR (n : ℕ) (c : C) (x : B) :
    (singleR n c * constR x : R) = singleR n (c * inlB x) := by
  apply Subtype.ext; funext k
  change (if k = n then c else 0) * inlB x = if k = n then c * inlB x else 0
  by_cases h : k = n <;> simp [h]

/-! ### Sequences supported on a finite set -/

/-- The ideal of `R` of sequences supported on a fixed finite set `S`:
`{ g | ∀ k ∉ S, g k = 0 }`. -/
noncomputable def suppIn (S : Finset ℕ) : Ideal R where
  carrier := {g : R | ∀ k ∉ S, (g : ℕ → C) k = 0}
  add_mem' := by
    intro f g hf hg k hk
    change ((f : ℕ → C) + (g : ℕ → C)) k = 0
    rw [Pi.add_apply, hf k hk, hg k hk, add_zero]
  zero_mem' := by intro k _; rfl
  smul_mem' := by
    intro r g hg k hk
    change ((r : ℕ → C) * (g : ℕ → C)) k = 0
    rw [Pi.mul_apply, hg k hk, mul_zero]

theorem mem_suppIn (S : Finset ℕ) (g : R) :
    g ∈ suppIn S ↔ ∀ k ∉ S, (g : ℕ → C) k = 0 := Iff.rfl

end Prob4b
