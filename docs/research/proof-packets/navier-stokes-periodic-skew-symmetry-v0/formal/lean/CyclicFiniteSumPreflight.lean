import Std

/-!
Project Telos finite cyclic-sum preflight.

This file advances the periodic cancellation ladder from a two-face integer
stencil to a generic finite cyclic integer path:

```text
sum_i (a[i+1] - a[i]) = 0
```

for a finite path closed back to its starting value.

Evidence boundary: this is still discrete algebra. It does not define smooth
periodic functions, integrals, weak solutions, or Navier-Stokes equations.
-/

namespace ProjectTelos.FormalReplay

/--
Return the final sampled value in a finite path, or the starting value when the
path has no interior samples.

This is a deliberately discrete stand-in for a periodic path endpoint. It keeps
the theorem independent of Mathlib, topology, smoothness, and integration.
-/
def lastValue (fallback : Int) : List Int -> Int
  | [] => fallback
  | x :: xs => lastValue x xs

/--
Sum the first differences along a finite integer path beginning at `start`.

For samples `[a1, a2, ..., an]`, this is:

```text
(a1 - start) + (a2 - a1) + ... + (an - a(n-1))
```
-/
def pathDiffSum (start : Int) : List Int -> Int
  | [] => 0
  | x :: xs => (x - start) + pathDiffSum x xs

/--
The finite path first-difference sum telescopes to endpoint minus start.

This is a discrete precursor to periodic integration-by-parts bookkeeping, not
the continuous theorem itself.
-/
theorem pathDiffSum_telescopes (start : Int) (xs : List Int) :
    pathDiffSum start xs = lastValue start xs - start := by
  induction xs generalizing start with
  | nil =>
      simp [pathDiffSum, lastValue]
  | cons x xs ih =>
      simp [pathDiffSum, lastValue]
      have h := ih x
      omega

/--
Closing the finite path back to the starting value cancels the telescoping sum.

This is the fifteenth-wave finite cyclic-sum rung:

```text
sum_i (a[i+1] - a[i]) = 0
```

over a finite integer path closed by the final edge back to `start`.

Evidence boundary: this proves a discrete algebraic finite-sum identity only.
It does not define or prove smooth periodic integration by parts, PDE
regularity, Navier-Stokes existence, or physical-fluid validity.
-/
theorem cyclic_pathDiffSum_cancels (start : Int) (xs : List Int) :
    pathDiffSum start xs + (start - lastValue start xs) = 0 := by
  rw [pathDiffSum_telescopes]
  omega

end ProjectTelos.FormalReplay
