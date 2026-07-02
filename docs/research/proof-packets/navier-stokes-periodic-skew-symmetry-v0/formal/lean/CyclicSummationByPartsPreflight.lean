import Std

/-!
Project Telos finite cyclic summation-by-parts preflight.

This file advances the periodic cancellation ladder from a scalar finite
cyclic first-difference sum to a paired finite stencil:

```text
sum_i u[i] * (phi[i+1] - phi[i])
+ sum_i phi[i] * (u[i] - u[i-1]) = 0
```

under cyclic closure on a finite integer path.

Evidence boundary: this is still discrete integer algebra. It does not define
smooth periodic functions, integrals, weak solutions, finite-volume
convergence, or Navier-Stokes equations.
-/

namespace ProjectTelos.FormalReplay

/--
Return the final `(u, phi)` sample in a finite path, or the starting sample
when the path has no interior samples.
-/
def lastPair (fallback : Prod Int Int) : List (Prod Int Int) -> Prod Int Int
  | [] => fallback
  | x :: xs => lastPair x xs

/--
Open-path gradient edge sum:

```text
sum_i u[i] * (phi[i+1] - phi[i])
```

without the final cyclic closing edge.
-/
def gradientOpen (u phi : Int) : List (Prod Int Int) -> Int
  | [] => 0
  | (uNext, phiNext) :: xs =>
      u * (phiNext - phi) + gradientOpen uNext phiNext xs

/--
Open-path divergence-like interior sum:

```text
sum_i phi[i] * (u[i] - u[i-1])
```

over samples after the starting pair.
-/
def divergenceInterior (prevU : Int) : List (Prod Int Int) -> Int
  | [] => 0
  | (u, phi) :: xs =>
      phi * (u - prevU) + divergenceInterior u xs

/-- Cyclic gradient sum, including the closing edge back to `phi`. -/
def cyclicGradientSum (u phi : Int) (xs : List (Prod Int Int)) : Int :=
  gradientOpen u phi xs
    + (lastPair (u, phi) xs).1 * (phi - (lastPair (u, phi) xs).2)

/-- Cyclic divergence-like sum, including the closing predecessor term. -/
def cyclicDivergenceSum (u phi : Int) (xs : List (Prod Int Int)) : Int :=
  phi * (u - (lastPair (u, phi) xs).1) + divergenceInterior u xs

/--
Open-path summation by parts with explicit endpoint product terms.

This is the finite product-rule/telescoping core that the cyclic theorem closes.
-/
theorem open_summation_by_parts (u phi : Int) (xs : List (Prod Int Int)) :
    gradientOpen u phi xs + divergenceInterior u xs =
      (lastPair (u, phi) xs).1 * (lastPair (u, phi) xs).2 - u * phi := by
  induction xs generalizing u phi with
  | nil =>
      simp [gradientOpen, divergenceInterior, lastPair]
  | cons x xs ih =>
      cases x with
      | mk uNext phiNext =>
          simp [gradientOpen, divergenceInterior, lastPair]
          have h := ih uNext phiNext
          have hp :
              (lastPair (uNext, phiNext) xs).1
                  * (lastPair (uNext, phiNext) xs).2 =
                gradientOpen uNext phiNext xs
                  + divergenceInterior uNext xs
                  + uNext * phiNext := by
            omega
          rw [hp]
          rw [Int.mul_sub, Int.mul_sub]
          repeat rw [Int.sub_eq_add_neg]
          simp [Int.mul_comm, Int.add_assoc, Int.add_comm, Int.add_left_comm]
          omega

/--
Cyclic finite summation by parts.

This is the sixteenth-wave finite paired-stencil rung:

```text
sum_i u[i] * (phi[i+1] - phi[i])
+ sum_i phi[i] * (u[i] - u[i-1]) = 0
```

over a finite integer path closed by the final edge back to the starting
sample.

Evidence boundary: this proves a discrete algebraic finite-stencil identity
only. It does not define or prove smooth periodic integration by parts, PDE
regularity, Navier-Stokes existence, or physical-fluid validity.
-/
theorem cyclic_summation_by_parts_cancels
    (u phi : Int) (xs : List (Prod Int Int)) :
    cyclicGradientSum u phi xs + cyclicDivergenceSum u phi xs = 0 := by
  simp [cyclicGradientSum, cyclicDivergenceSum]
  have h := open_summation_by_parts u phi xs
  rw [Int.mul_sub, Int.mul_sub]
  repeat rw [Int.sub_eq_add_neg]
  simp [Int.mul_comm, Int.add_assoc, Int.add_comm, Int.add_left_comm]
  omega

end ProjectTelos.FormalReplay
