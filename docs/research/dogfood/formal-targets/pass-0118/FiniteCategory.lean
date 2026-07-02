-- Pass 0118 generated target. Source artifact only; not executed here.
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
