/-
Copyright (c) 2026 Prob4b formalization. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Prob4b formalization
-/
import Mathlib

/-!
# Frozen definitions for the Problem 4(b) counterexample

This file is **frozen** after the SETUP stage. It pins every object of the
construction in `SKETCH.md`:

* `B = 𝔽₂[a,b,c,d] / ((a,b,c,d)³, ad+bc)` — the local Artinian base ring, modeled
  as an `MvPolynomial` quotient (so `CommRing B` is free);
* `M = B⁴ / B·v` (`v = (a,b,c,d)`) — the module with the triple-intersection
  defect, with `smulSub x = xM`, `annihM x = (0 :_M x)`, and the defect `u`;
* `C = TrivSqZeroExt B M` — the idealization `B ⋉ M`, with `inlB : B →+* C`;
* `R = Rsub` — the amplification `Δ(B) + C^(ℕ)`, a `Subring` of `ℕ → C`;
* `annih`, `FiniteConductor`, `QuasiCoherent` — the textbook predicates the
  headline `problem4b_false` is stated in.

See `BLUEPRINT.md` Part −1 §2 for the modeling decisions and `PROGRESS.md`.
-/

namespace Prob4b

open MvPolynomial

/-- The polynomial ring `𝔽₂[a,b,c,d]`. -/
abbrev P4 : Type := MvPolynomial (Fin 4) (ZMod 2)

/-- The maximal ideal `(a,b,c,d)` of the polynomial ring. -/
noncomputable def mP : Ideal P4 := Ideal.span {X 0, X 1, X 2, X 3}

/-- The defining ideal `((a,b,c,d)³, ad + bc)`. -/
noncomputable def Brel : Ideal P4 := mP ^ 3 + Ideal.span {X 0 * X 3 + X 1 * X 2}

/-- The base ring `B = 𝔽₂[a,b,c,d] / ((a,b,c,d)³, ad + bc)`. -/
abbrev B : Type := P4 ⧸ Brel

/-- Generator `a ∈ B`. -/
noncomputable def a : B := Ideal.Quotient.mk Brel (X 0)
/-- Generator `b ∈ B`. -/
noncomputable def b : B := Ideal.Quotient.mk Brel (X 1)
/-- Generator `c ∈ B`. -/
noncomputable def c : B := Ideal.Quotient.mk Brel (X 2)
/-- Generator `d ∈ B`. -/
noncomputable def d : B := Ideal.Quotient.mk Brel (X 3)

/-- The maximal ideal `𝔪 = (a,b,c,d)` of `B`. -/
noncomputable def m : Ideal B := Ideal.span {a, b, c, d}


/-- The vector `v = (a,b,c,d) ∈ B⁴`. -/
noncomputable def v : Fin 4 → B := ![a, b, c, d]

/-- The cyclic submodule `B·v ⊆ B⁴`. -/
noncomputable def Bv : Submodule B (Fin 4 → B) := Submodule.span B {v}

/-- The module `M = B⁴ / B·v`. -/
abbrev M : Type := (Fin 4 → B) ⧸ Bv

/-- The triple-intersection defect element `u = [(0, ab+b², 0, bc+bd)] ∈ M`. -/
noncomputable def u : M := Submodule.Quotient.mk (![0, a * b + b ^ 2, 0, b * c + b * d] : Fin 4 → B)

/-- `xM` as a submodule of `M`: `(x) • ⊤`. -/
noncomputable def smulSub (x : B) : Submodule B M := (Ideal.span {x}) • (⊤ : Submodule B M)

/-- The annihilator `(0 :_M x) = {p : M | x • p = 0}` as a submodule. -/
noncomputable def annihM (x : B) : Submodule B M := LinearMap.ker (LinearMap.lsmul B M x)

/-- The right `B`-action on `M` (via `Bᵐᵒᵖ`), needed so that `TrivSqZeroExt B M`
is a ring. We take the canonical quotient module structure, so it is
definitionally compatible with the ambient scalar action. -/
noncomputable instance instModuleOpM : Module Bᵐᵒᵖ M := Submodule.Quotient.module' Bv

/-- The left and right `B`-actions on `M` coincide (`B` is commutative). -/
instance instCentralScalarM : IsCentralScalar B M :=
  ⟨fun r m => by
    induction m using Submodule.Quotient.induction_on with
    | H x =>
        change Submodule.Quotient.mk (MulOpposite.op r • x) = Submodule.Quotient.mk (r • x)
        congr 1
        funext i
        exact mul_comm _ _⟩

/-- The idealization `C = B ⋉ M` (trivial square-zero extension). -/
abbrev C : Type := TrivSqZeroExt B M

/-- The diagonal ring embedding `inlB : B →+* C`, `x ↦ (x, 0)`. -/
noncomputable def inlB : B →+* C := TrivSqZeroExt.inlHom B M

/-- Image of `a` in `C`. -/
noncomputable def aC : C := inlB a
/-- Image of `b` in `C`. -/
noncomputable def bC : C := inlB b

/-- The amplified ring `R = Δ(B) + C^(ℕ) ⊆ Cᴺ`: sequences into `C` that are
equal to a single constant `inlB x` (`x ∈ B`, the diagonal copy of `B`) off a
finite set of coordinates. -/
def Rsub : Subring (ℕ → C) where
  carrier := {f | ∃ (x : B) (s : Finset ℕ), ∀ n ∉ s, f n = inlB x}
  zero_mem' := ⟨0, ∅, by intro n _; simp⟩
  one_mem' := ⟨1, ∅, by intro n _; simp⟩
  add_mem' := by
    rintro f g ⟨x, s, hf⟩ ⟨y, t, hg⟩
    refine ⟨x + y, s ∪ t, fun n hn => ?_⟩
    rw [Pi.add_apply, hf n (fun h => hn (Finset.mem_union_left _ h)),
      hg n (fun h => hn (Finset.mem_union_right _ h)), ← map_add]
  mul_mem' := by
    rintro f g ⟨x, s, hf⟩ ⟨y, t, hg⟩
    refine ⟨x * y, s ∪ t, fun n hn => ?_⟩
    rw [Pi.mul_apply, hf n (fun h => hn (Finset.mem_union_left _ h)),
      hg n (fun h => hn (Finset.mem_union_right _ h)), ← map_mul]
  neg_mem' := by
    rintro f ⟨x, s, hf⟩
    exact ⟨-x, s, fun n hn => by rw [Pi.neg_apply, hf n hn, map_neg]⟩

/-- The amplified ring as a type (with its inherited `CommRing` structure). -/
abbrev R : Type := Rsub

/-- The annihilator ideal `(0 : x) = {y | y * x = 0}` of an element. -/
def annih {S : Type*} [CommRing S] (x : S) : Ideal S := LinearMap.ker (LinearMap.lsmul S S x)

/-- A commutative ring is **finite-conductor**: every annihilator and every
*pairwise* principal intersection is finitely generated. -/
def FiniteConductor (S : Type*) [CommRing S] : Prop :=
  (∀ x : S, (annih x).FG) ∧ (∀ x y : S, (Ideal.span {x} ⊓ Ideal.span {y}).FG)

/-- A commutative ring is **quasi-coherent**: every annihilator and every
*arbitrary finite* principal intersection is finitely generated. -/
def QuasiCoherent (S : Type*) [CommRing S] : Prop :=
  (∀ x : S, (annih x).FG) ∧
    (∀ (n : ℕ) (f : Fin n → S), (⨅ i, Ideal.span {f i}).FG)

end Prob4b
