-- Pass 0118 generated target. Source artifact only; not executed here.
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
