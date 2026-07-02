"""Generated prover source templates for pass 0118."""
from __future__ import annotations

from pathlib import Path
from typing import Any


def lean_source() -> str:
    return """-- Pass 0118 generated target. Source artifact only; not executed here.
inductive A where
  | a0
  | a1
deriving DecidableEq, Repr

inductive B where
  | b0
  | b1
deriving DecidableEq, Repr

inductive C where
  | c0
  | c1
deriving DecidableEq, Repr

inductive D where
  | d0
  | d1
deriving DecidableEq, Repr

def idA : A -> A
  | A.a0 => A.a0
  | A.a1 => A.a1

def idB : B -> B
  | B.b0 => B.b0
  | B.b1 => B.b1

def f : A -> B
  | A.a0 => B.b0
  | A.a1 => B.b1

def g : B -> C
  | B.b0 => C.c1
  | B.b1 => C.c0

def h : C -> D
  | C.c0 => D.d0
  | C.c1 => D.d1

def comp {X Y Z : Type} (g0 : Y -> Z) (f0 : X -> Y) : X -> Z :=
  fun x => g0 (f0 x)

theorem idB_comp_f_eq_f (x : A) : comp idB f x = f x := by
  cases x <;> rfl

theorem f_comp_idA_eq_f (x : A) : comp f idA x = f x := by
  cases x <;> rfl

theorem h_comp_g_comp_f_assoc (x : A) :
    comp h (comp g f) x = comp (comp h g) f x := by
  cases x <;> rfl
"""


def rocq_source() -> str:
    return """(* Pass 0118 generated target. Source artifact only; not executed here. *)
Inductive A : Type := a0 | a1.
Inductive B : Type := b0 | b1.
Inductive C : Type := c0 | c1.
Inductive D : Type := d0 | d1.

Definition idA (x : A) : A :=
  match x with a0 => a0 | a1 => a1 end.

Definition idB (x : B) : B :=
  match x with b0 => b0 | b1 => b1 end.

Definition f (x : A) : B :=
  match x with a0 => b0 | a1 => b1 end.

Definition g (x : B) : C :=
  match x with b0 => c1 | b1 => c0 end.

Definition h (x : C) : D :=
  match x with c0 => d0 | c1 => d1 end.

Definition comp {X Y Z : Type} (g0 : Y -> Z) (f0 : X -> Y) : X -> Z :=
  fun x => g0 (f0 x).

Theorem idB_comp_f_eq_f : forall x : A, comp idB f x = f x.
Proof. intros x; destruct x; reflexivity. Qed.

Theorem f_comp_idA_eq_f : forall x : A, comp f idA x = f x.
Proof. intros x; destruct x; reflexivity. Qed.

Theorem h_comp_g_comp_f_assoc :
  forall x : A, comp h (comp g f) x = comp (comp h g) f x.
Proof. intros x; destruct x; reflexivity. Qed.
"""


def isabelle_source() -> str:
    return """(* Pass 0118 generated target. Source artifact only; not executed here. *)
theory Pass0118_Finite_Category
  imports Main
begin

datatype A = a0 | a1
datatype B = b0 | b1
datatype C = c0 | c1
datatype D = d0 | d1

fun idA :: "A => A" where
  "idA a0 = a0" |
  "idA a1 = a1"

fun idB :: "B => B" where
  "idB b0 = b0" |
  "idB b1 = b1"

fun f :: "A => B" where
  "f a0 = b0" |
  "f a1 = b1"

fun g :: "B => C" where
  "g b0 = c1" |
  "g b1 = c0"

fun h :: "C => D" where
  "h c0 = d0" |
  "h c1 = d1"

definition comp where "comp g0 f0 x = g0 (f0 x)"

theorem idB_comp_f_eq_f: "comp idB f x = f x"
  by (cases x) (simp_all add: comp_def)

theorem f_comp_idA_eq_f: "comp f idA x = f x"
  by (cases x) (simp_all add: comp_def)

theorem h_comp_g_comp_f_assoc:
  "comp h (comp g f) x = comp (comp h g) f x"
  by (cases x) (simp_all add: comp_def)

end
"""


def agda_source() -> str:
    return """-- Pass 0118 generated target. Source artifact only; not executed here.
module Pass0118FiniteCategory where

data A : Set where
  a0 : A
  a1 : A

data B : Set where
  b0 : B
  b1 : B

data C : Set where
  c0 : C
  c1 : C

data D : Set where
  d0 : D
  d1 : D

data Eq {X : Set} (x : X) : X -> Set where
  refl : Eq x x

idA : A -> A
idA a0 = a0
idA a1 = a1

idB : B -> B
idB b0 = b0
idB b1 = b1

f : A -> B
f a0 = b0
f a1 = b1

g : B -> C
g b0 = c1
g b1 = c0

h : C -> D
h c0 = d0
h c1 = d1

comp : {X Y Z : Set} -> (Y -> Z) -> (X -> Y) -> X -> Z
comp g0 f0 x = g0 (f0 x)

idB_comp_f_eq_f : (x : A) -> Eq (comp idB f x) (f x)
idB_comp_f_eq_f a0 = refl
idB_comp_f_eq_f a1 = refl

f_comp_idA_eq_f : (x : A) -> Eq (comp f idA x) (f x)
f_comp_idA_eq_f a0 = refl
f_comp_idA_eq_f a1 = refl

h_comp_g_comp_f_assoc : (x : A) -> Eq (comp h (comp g f) x) (comp (comp h g) f x)
h_comp_g_comp_f_assoc a0 = refl
h_comp_g_comp_f_assoc a1 = refl
"""


def source_specs(target_dir: Path) -> list[dict[str, Any]]:
    return [
        {"language": "lean4", "path": target_dir / "FiniteCategory.lean", "executable": "lean", "command": "lean FiniteCategory.lean", "source": lean_source()},
        {"language": "rocq", "path": target_dir / "FiniteCategory.v", "executable": "coqc", "command": "coqc FiniteCategory.v", "source": rocq_source()},
        {"language": "isabelle", "path": target_dir / "Pass0118_Finite_Category.thy", "executable": "isabelle", "command": "isabelle process -T Pass0118_Finite_Category", "source": isabelle_source()},
        {"language": "agda", "path": target_dir / "Pass0118FiniteCategory.agda", "executable": "agda", "command": "agda Pass0118FiniteCategory.agda", "source": agda_source()},
    ]
