# Sixteenth-Wave Content Queue

Date: 2026-07-02

Boundary: These are visibility drafts for the finite cyclic summation-by-parts Lean replay rung. They must not claim smooth periodic integration by parts, Navier-Stokes, source truth, exhaustive coverage, or native BuildLang relation-invariant receipt support.

## Post Draft 1

Project Telos now has a finite paired-stencil theorem checked by Lean 4.31.0:

```text
sum_i u[i] * (phi[i+1] - phi[i])
+ sum_i phi[i] * (u[i] - u[i-1]) = 0
```

This is still discrete integer algebra. It is not the smooth PDE theorem.

But it is a better proof rung than a scalar telescoping sum, and it is receipt-backed.

## Post Draft 2

The important part is the label discipline:

- `CYCLIC_SUMMATION_BY_PARTS_MATCH`: finite paired-stencil theorem replayed
- `NOT_REPLAYED`: smooth periodic integration by parts
- `UNVERIFIABLE`: Navier-Stokes parent problem
- `SOURCE_LEAD_ONLY`: fresh arXiv metadata rows

The point is to move toward hard science without collapsing proof strengths.

## Post Draft 3

The new theorem lives in a separate file:

`CyclicSummationByPartsPreflight.lean`

Earlier Lean receipt files stayed hash-stable. The proof ladder can advance without rewriting old evidence.

That is the product lesson: frontier research tools need durable receipts, not just impressive claims.

## Post Draft 4

The next target is not "solve Navier-Stokes."

The next target is smaller and stricter:

turn the finite paired-stencil theorem into a typed finite-grid theorem with explicit domain, edge operator, and cyclic boundary vocabulary.

That is how a grand problem becomes an accountable proof ladder.

## Do Not Post

- "Lean proved smooth periodic integration by parts."
- "Project Telos solved Navier-Stokes."
- "The finite paired-stencil theorem proves the continuous PDE theorem."
- "arXiv metadata proves paper truth."
- "This is latest or exhaustive literature coverage."
- "BuildLang/buildc natively emits relation-invariant receipts for this theorem today."
- "The website copy is a submitted, accepted, or peer-reviewed paper."
