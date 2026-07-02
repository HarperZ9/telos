import Std

/-!
Project Telos vector-valued finite operator summation-by-parts preflight.

This file advances the replay ladder from scalar finite edge/operator
vocabulary to a two-component finite vector operator vocabulary:

- `Vector2Int`: a two-component integer vector.
- `VectorGridSample`: one finite-grid sample carrying vector velocity and
  vector scalar/test-field components.
- `VectorFiniteEdge`: an oriented edge from one vector sample to the next.
- `vectorGradientEdgeOperator`: a finite dot-product-like edge contribution.
- `vectorDivergenceNodeOperator`: a finite componentwise divergence-like node
  contribution.

The replayed theorem is still finite discrete integer algebra:

```text
cyclicVectorGradientOperatorSum grid
  + cyclicVectorDivergenceOperatorSum grid = 0
```

Evidence boundary: this does not define smooth functions, integrals, periodic
domains, convergence, weak solutions, or Navier-Stokes equations.
-/

namespace ProjectTelos.FormalReplay

/-- A two-component integer vector used only for finite replay preflight. -/
structure Vector2Int where
  x : Int
  y : Int

/-- One finite-grid sample in the vector operator vocabulary. -/
structure VectorGridSample where
  velocity : Vector2Int
  scalar : Vector2Int

/--
A finite cyclic vector path: `start` is the first sample and `rest` are the
following samples before the path closes back to `start`.
-/
structure VectorCyclicGrid where
  start : VectorGridSample
  rest : List VectorGridSample

/-- An oriented finite edge from one vector sample to the next sample. -/
structure VectorFiniteEdge where
  source : VectorGridSample
  target : VectorGridSample

/-- Componentwise product pairing at a finite vector sample. -/
def vectorPairProduct (sample : VectorGridSample) : Int :=
  sample.velocity.x * sample.scalar.x + sample.velocity.y * sample.scalar.y

/--
Return the final sample in a finite vector path, or the starting sample when the
path has no interior samples.
-/
def lastVectorSample
    (fallback : VectorGridSample) : List VectorGridSample -> VectorGridSample
  | [] => fallback
  | x :: xs => lastVectorSample x xs

/-- Finite dot-product-like edge-gradient contribution. -/
def vectorGradientEdgeOperator (edge : VectorFiniteEdge) : Int :=
  edge.source.velocity.x * (edge.target.scalar.x - edge.source.scalar.x)
    + edge.source.velocity.y * (edge.target.scalar.y - edge.source.scalar.y)

/-- Finite componentwise divergence-like node contribution. -/
def vectorDivergenceNodeOperator
    (previous current : VectorGridSample) : Int :=
  current.scalar.x * (current.velocity.x - previous.velocity.x)
    + current.scalar.y * (current.velocity.y - previous.velocity.y)

/--
Open-path vector gradient operator sum:

```text
sum_i u_x[i] * (phi_x[i+1] - phi_x[i])
  + u_y[i] * (phi_y[i+1] - phi_y[i])
```

without the final cyclic closing edge.
-/
def vectorGradientOperatorOpen
    (current : VectorGridSample) : List VectorGridSample -> Int
  | [] => 0
  | next :: xs =>
      vectorGradientEdgeOperator { source := current, target := next }
        + vectorGradientOperatorOpen next xs

/--
Open-path vector divergence-like operator sum over samples after the starting
sample.
-/
def vectorDivergenceOperatorInterior
    (previous : VectorGridSample) : List VectorGridSample -> Int
  | [] => 0
  | current :: xs =>
      vectorDivergenceNodeOperator previous current
        + vectorDivergenceOperatorInterior current xs

/-- Cyclic vector gradient operator sum, including the closing edge. -/
def cyclicVectorGradientOperatorSum (grid : VectorCyclicGrid) : Int :=
  vectorGradientOperatorOpen grid.start grid.rest
    + vectorGradientEdgeOperator
        { source := lastVectorSample grid.start grid.rest, target := grid.start }

/-- Cyclic vector divergence-like operator sum, including the closing term. -/
def cyclicVectorDivergenceOperatorSum (grid : VectorCyclicGrid) : Int :=
  vectorDivergenceNodeOperator (lastVectorSample grid.start grid.rest) grid.start
    + vectorDivergenceOperatorInterior grid.start grid.rest

/--
Open-path vector summation by parts over explicit finite operator vocabulary.

This exposes the vector endpoint pairing before cyclic closure removes it.
-/
theorem open_vector_operator_summation_by_parts
    (current : VectorGridSample) (xs : List VectorGridSample) :
    vectorGradientOperatorOpen current xs
        + vectorDivergenceOperatorInterior current xs =
      vectorPairProduct (lastVectorSample current xs)
        - vectorPairProduct current := by
  induction xs generalizing current with
  | nil =>
      simp [
        vectorGradientOperatorOpen,
        vectorDivergenceOperatorInterior,
        lastVectorSample
      ]
  | cons next xs ih =>
      cases current with
      | mk currentVelocity currentScalar =>
          cases currentVelocity with
          | mk ux uy =>
              cases currentScalar with
              | mk phix phiy =>
                  cases next with
                  | mk nextVelocity nextScalar =>
                      cases nextVelocity with
                      | mk uxNext uyNext =>
                          cases nextScalar with
                          | mk phixNext phiyNext =>
                              simp [
                                vectorGradientOperatorOpen,
                                vectorDivergenceOperatorInterior,
                                lastVectorSample,
                                vectorGradientEdgeOperator,
                                vectorDivergenceNodeOperator,
                                vectorPairProduct
                              ]
                              have h :=
                                ih
                                  { velocity := { x := uxNext, y := uyNext },
                                    scalar := { x := phixNext, y := phiyNext } }
                              simp [vectorPairProduct] at h
                              repeat rw [Int.sub_eq_add_neg] at h
                              rw [Int.mul_sub, Int.mul_sub, Int.mul_sub, Int.mul_sub]
                              repeat rw [Int.sub_eq_add_neg]
                              simp [
                                Int.mul_comm,
                                Int.add_assoc,
                                Int.add_comm,
                                Int.add_left_comm
                              ]
                              omega

/--
Vector-valued finite operator cyclic summation by parts.

This is the twentieth-wave finite vector/operator rung. It proves a two-component
finite identity over integer samples, oriented finite edges, and componentwise
operator contributions.

Evidence boundary: this is not smooth periodic integration by parts, not a PDE
proof, and not a Navier-Stokes result.
-/
theorem vector_finite_operator_summation_by_parts_cancels
    (grid : VectorCyclicGrid) :
    cyclicVectorGradientOperatorSum grid
        + cyclicVectorDivergenceOperatorSum grid = 0 := by
  cases grid with
  | mk start rest =>
      cases start with
      | mk startVelocity startScalar =>
          cases startVelocity with
          | mk ux uy =>
              cases startScalar with
              | mk phix phiy =>
                  simp [
                    cyclicVectorGradientOperatorSum,
                    cyclicVectorDivergenceOperatorSum,
                    vectorGradientEdgeOperator,
                    vectorDivergenceNodeOperator
                  ]
                  have h :=
                    open_vector_operator_summation_by_parts
                      { velocity := { x := ux, y := uy },
                        scalar := { x := phix, y := phiy } }
                      rest
                  simp [vectorPairProduct] at h
                  repeat rw [Int.sub_eq_add_neg] at h
                  rw [Int.mul_sub, Int.mul_sub, Int.mul_sub, Int.mul_sub]
                  repeat rw [Int.sub_eq_add_neg]
                  simp [
                    Int.mul_comm,
                    Int.add_assoc,
                    Int.add_comm,
                    Int.add_left_comm
                  ]
                  omega

end ProjectTelos.FormalReplay
