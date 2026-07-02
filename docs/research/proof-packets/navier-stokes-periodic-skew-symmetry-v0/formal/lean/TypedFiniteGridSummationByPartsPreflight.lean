import Std

/-!
Project Telos typed finite-grid summation-by-parts preflight.

This file advances the periodic cancellation ladder from an untyped paired
integer stencil to an explicit finite-grid vocabulary:

- `GridSample`: one finite-grid sample carrying velocity and scalar values.
- `CyclicGrid`: a finite path with a starting sample and remaining samples.
- `cyclicGradientSum`: cyclic edge-gradient contribution.
- `cyclicDivergenceSum`: cyclic divergence-like contribution.

The replayed theorem is still finite discrete integer algebra:

```text
cyclicGradientSum grid + cyclicDivergenceSum grid = 0
```

Evidence boundary: this does not define smooth functions, integrals, periodic
domains, finite-volume convergence, weak solutions, or Navier-Stokes equations.
-/

namespace ProjectTelos.FormalReplay

/-- One finite-grid sample in the typed stencil vocabulary. -/
structure GridSample where
  velocity : Int
  scalar : Int

/--
A finite cyclic path: `start` is the first sample and `rest` are the following
samples before the path closes back to `start`.
-/
structure CyclicGrid where
  start : GridSample
  rest : List GridSample

/--
Return the final sample in a finite path, or the starting sample when the path
has no interior samples.
-/
def lastSample (fallback : GridSample) : List GridSample -> GridSample
  | [] => fallback
  | x :: xs => lastSample x xs

/--
Open-path gradient edge sum:

```text
sum_i u[i] * (phi[i+1] - phi[i])
```

without the final cyclic closing edge.
-/
def gradientOpen (current : GridSample) : List GridSample -> Int
  | [] => 0
  | next :: xs =>
      current.velocity * (next.scalar - current.scalar)
        + gradientOpen next xs

/--
Open-path divergence-like interior sum:

```text
sum_i phi[i] * (u[i] - u[i-1])
```

over samples after the starting sample.
-/
def divergenceInterior (previous : GridSample) : List GridSample -> Int
  | [] => 0
  | current :: xs =>
      current.scalar * (current.velocity - previous.velocity)
        + divergenceInterior current xs

/-- Cyclic gradient sum, including the closing edge back to `grid.start`. -/
def cyclicGradientSum (grid : CyclicGrid) : Int :=
  gradientOpen grid.start grid.rest
    + (lastSample grid.start grid.rest).velocity
        * (grid.start.scalar - (lastSample grid.start grid.rest).scalar)

/-- Cyclic divergence-like sum, including the closing predecessor term. -/
def cyclicDivergenceSum (grid : CyclicGrid) : Int :=
  grid.start.scalar
      * (grid.start.velocity - (lastSample grid.start grid.rest).velocity)
    + divergenceInterior grid.start grid.rest

/--
Open-path summation by parts over typed grid samples.

This theorem exposes the endpoint product terms before cyclic closure removes
them.
-/
theorem open_grid_summation_by_parts
    (current : GridSample) (xs : List GridSample) :
    gradientOpen current xs + divergenceInterior current xs =
      (lastSample current xs).velocity * (lastSample current xs).scalar
        - current.velocity * current.scalar := by
  induction xs generalizing current with
  | nil =>
      simp [gradientOpen, divergenceInterior, lastSample]
  | cons next xs ih =>
      cases current with
      | mk u phi =>
          cases next with
          | mk uNext phiNext =>
              simp [gradientOpen, divergenceInterior, lastSample]
              have h := ih { velocity := uNext, scalar := phiNext }
              simp at h
              have hp :
                  (lastSample { velocity := uNext, scalar := phiNext } xs).velocity
                      * (lastSample { velocity := uNext, scalar := phiNext } xs).scalar =
                    gradientOpen { velocity := uNext, scalar := phiNext } xs
                      + divergenceInterior { velocity := uNext, scalar := phiNext } xs
                      + uNext * phiNext := by
                omega
              rw [hp]
              rw [Int.mul_sub, Int.mul_sub]
              repeat rw [Int.sub_eq_add_neg]
              simp [Int.mul_comm, Int.add_assoc, Int.add_comm, Int.add_left_comm]
              omega

/--
Typed finite-grid cyclic summation by parts.

This is the seventeenth-wave typed finite-grid rung. It proves the same finite
identity as the previous paired-stencil file, but with named sample and grid
structures that can later align with BuildLang/buildc relation-invariant
receipts.

Evidence boundary: this is not smooth periodic integration by parts, not a PDE
proof, and not a Navier-Stokes result.
-/
theorem typed_finite_grid_summation_by_parts_cancels
    (grid : CyclicGrid) :
    cyclicGradientSum grid + cyclicDivergenceSum grid = 0 := by
  cases grid with
  | mk start rest =>
      cases start with
      | mk u phi =>
          simp [cyclicGradientSum, cyclicDivergenceSum]
          have h :=
            open_grid_summation_by_parts { velocity := u, scalar := phi } rest
          simp at h
          rw [Int.mul_sub, Int.mul_sub]
          repeat rw [Int.sub_eq_add_neg]
          simp [Int.mul_comm, Int.add_assoc, Int.add_comm, Int.add_left_comm]
          omega

end ProjectTelos.FormalReplay
