(* Pass 0118 generated target. Source artifact only; not executed here. *)
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
