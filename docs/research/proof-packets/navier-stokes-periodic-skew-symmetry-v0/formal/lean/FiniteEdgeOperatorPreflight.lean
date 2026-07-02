import Std

/-!
Project Telos finite edge/operator summation-by-parts preflight.

This file advances the periodic cancellation ladder from typed finite-grid
samples to explicit finite edge and operator vocabulary:

- `GridSample`: one finite-grid sample carrying velocity and scalar values.
- `FiniteEdge`: an oriented edge from a source sample to a target sample.
- `ForwardScalarDifference`: the scalar difference across an oriented edge.
- `BackwardVelocityDifference`: the velocity jump from a predecessor sample.
- `gradientEdgeOperator`: the edge contribution `u[i] * (phi[i+1] - phi[i])`.
- `divergenceNodeOperator`: the node contribution `phi[i] * (u[i] - u[i-1])`.

The replayed theorem is still finite discrete integer algebra:

```text
cyclicGradientOperatorSum grid + cyclicDivergenceOperatorSum grid = 0
```

Evidence boundary: this does not define smooth functions, integrals, periodic
domains, finite-volume convergence, weak solutions, or Navier-Stokes equations.
-/

namespace ProjectTelos.FormalReplay

/-- One finite-grid sample in the edge/operator vocabulary. -/
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

/-- An oriented finite edge from one sample to the next sample. -/
structure FiniteEdge where
  source : GridSample
  target : GridSample

/-- Scalar forward difference across an oriented finite edge. -/
structure ForwardScalarDifference where
  edge : FiniteEdge

/-- Velocity backward difference from a previous sample into a current sample. -/
structure BackwardVelocityDifference where
  previous : GridSample
  current : GridSample

/--
Return the final sample in a finite path, or the starting sample when the path
has no interior samples.
-/
def lastSample (fallback : GridSample) : List GridSample -> GridSample
  | [] => fallback
  | x :: xs => lastSample x xs

/-- Evaluate a forward scalar difference across an edge. -/
def ForwardScalarDifference.value (difference : ForwardScalarDifference) : Int :=
  difference.edge.target.scalar - difference.edge.source.scalar

/-- Evaluate a backward velocity difference into a node. -/
def BackwardVelocityDifference.value (difference : BackwardVelocityDifference) : Int :=
  difference.current.velocity - difference.previous.velocity

/-- Edge-gradient operator contribution on one oriented edge. -/
def gradientEdgeOperator (edge : FiniteEdge) : Int :=
  edge.source.velocity * (ForwardScalarDifference.value { edge := edge })

/-- Divergence-like node operator contribution against a predecessor sample. -/
def divergenceNodeOperator (previous current : GridSample) : Int :=
  current.scalar
    * (BackwardVelocityDifference.value { previous := previous, current := current })

/--
Open-path gradient operator sum:

```text
sum_i u[i] * (phi[i+1] - phi[i])
```

without the final cyclic closing edge.
-/
def gradientOperatorOpen (current : GridSample) : List GridSample -> Int
  | [] => 0
  | next :: xs =>
      gradientEdgeOperator { source := current, target := next }
        + gradientOperatorOpen next xs

/--
Open-path divergence-like operator sum:

```text
sum_i phi[i] * (u[i] - u[i-1])
```

over samples after the starting sample.
-/
def divergenceOperatorInterior (previous : GridSample) : List GridSample -> Int
  | [] => 0
  | current :: xs =>
      divergenceNodeOperator previous current
        + divergenceOperatorInterior current xs

/-- Cyclic gradient operator sum, including the closing edge back to `grid.start`. -/
def cyclicGradientOperatorSum (grid : CyclicGrid) : Int :=
  gradientOperatorOpen grid.start grid.rest
    + gradientEdgeOperator
        { source := lastSample grid.start grid.rest, target := grid.start }

/-- Cyclic divergence-like operator sum, including the closing predecessor term. -/
def cyclicDivergenceOperatorSum (grid : CyclicGrid) : Int :=
  divergenceNodeOperator (lastSample grid.start grid.rest) grid.start
    + divergenceOperatorInterior grid.start grid.rest

/--
Open-path summation by parts over explicit finite edge/operator vocabulary.

This exposes the endpoint product terms before cyclic closure removes them.
-/
theorem open_edge_operator_summation_by_parts
    (current : GridSample) (xs : List GridSample) :
    gradientOperatorOpen current xs + divergenceOperatorInterior current xs =
      (lastSample current xs).velocity * (lastSample current xs).scalar
        - current.velocity * current.scalar := by
  induction xs generalizing current with
  | nil =>
      simp [
        gradientOperatorOpen,
        divergenceOperatorInterior,
        lastSample
      ]
  | cons next xs ih =>
      cases current with
      | mk u phi =>
          cases next with
          | mk uNext phiNext =>
              simp [
                gradientOperatorOpen,
                divergenceOperatorInterior,
                lastSample,
                gradientEdgeOperator,
                divergenceNodeOperator,
                ForwardScalarDifference.value,
                BackwardVelocityDifference.value
              ]
              have h := ih { velocity := uNext, scalar := phiNext }
              simp at h
              have hp :
                  (lastSample { velocity := uNext, scalar := phiNext } xs).velocity
                      * (lastSample { velocity := uNext, scalar := phiNext } xs).scalar =
                    gradientOperatorOpen { velocity := uNext, scalar := phiNext } xs
                      + divergenceOperatorInterior { velocity := uNext, scalar := phiNext } xs
                      + uNext * phiNext := by
                omega
              rw [hp]
              rw [Int.mul_sub, Int.mul_sub]
              repeat rw [Int.sub_eq_add_neg]
              simp [Int.mul_comm, Int.add_assoc, Int.add_comm, Int.add_left_comm]
              omega

/--
Finite edge/operator cyclic summation by parts.

This is the nineteenth-wave explicit finite edge/operator rung. It proves the
same finite identity as the previous typed finite-grid file, but with named
edge and difference-operator structures that can later align with BuildLang/
buildc relation-invariant receipts.

Evidence boundary: this is not smooth periodic integration by parts, not a PDE
proof, and not a Navier-Stokes result.
-/
theorem finite_edge_operator_summation_by_parts_cancels
    (grid : CyclicGrid) :
    cyclicGradientOperatorSum grid + cyclicDivergenceOperatorSum grid = 0 := by
  cases grid with
  | mk start rest =>
      cases start with
      | mk u phi =>
          simp [
            cyclicGradientOperatorSum,
            cyclicDivergenceOperatorSum,
            gradientEdgeOperator,
            divergenceNodeOperator,
            ForwardScalarDifference.value,
            BackwardVelocityDifference.value
          ]
          have h :=
            open_edge_operator_summation_by_parts
              { velocity := u, scalar := phi } rest
          simp at h
          rw [Int.mul_sub, Int.mul_sub]
          repeat rw [Int.sub_eq_add_neg]
          simp [Int.mul_comm, Int.add_assoc, Int.add_comm, Int.add_left_comm]
          omega

end ProjectTelos.FormalReplay
