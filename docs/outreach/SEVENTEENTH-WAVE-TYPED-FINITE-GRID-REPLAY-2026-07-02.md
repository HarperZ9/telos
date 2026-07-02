# Seventeenth-Wave Typed Finite-Grid Replay

Date: 2026-07-02

Purpose: advance the formal replay ladder from an untyped paired-stencil identity to a typed finite-grid Lean theorem, while preserving the boundary that smooth periodic integration by parts and Navier-Stokes remain unproved.

## Decision

The next publishable rung is now:

> a Lean-checked typed finite-grid cyclic summation-by-parts theorem.

This adds explicit `GridSample` and `CyclicGrid` structures around the finite algebraic identity. It is closer to a reusable grid/operator vocabulary for BuildLang/buildc relation receipts, but it is still finite discrete integer algebra. The smooth theorem remains `NOT_REPLAYED`; the parent Navier-Stokes problem remains `UNVERIFIABLE`.

## Lean Artifact

Source:

`docs/research/proof-packets/navier-stokes-periodic-skew-symmetry-v0/formal/lean/TypedFiniteGridSummationByPartsPreflight.lean`

Receipt:

`docs/outreach/receipts/seventeenth-wave/lean-typed-finite-grid-sbp-replay-2026-07-02.json`

Command:

```powershell
C:\Users\Zain\.elan\bin\lean.exe docs\research\proof-packets\navier-stokes-periodic-skew-symmetry-v0\formal\lean\TypedFiniteGridSummationByPartsPreflight.lean
```

Observed result: exit code `0`.

Replayed theorem:

```text
ProjectTelos.FormalReplay.typed_finite_grid_summation_by_parts_cancels
```

Formal shape:

```text
cyclicGradientSum grid + cyclicDivergenceSum grid = 0
```

## Evidence States

| Claim | Evidence state | Evidence | Boundary |
| --- | --- | --- | --- |
| A typed finite-grid cyclic summation-by-parts theorem replays in Lean. | `TYPED_FINITE_GRID_SBP_MATCH` | Lean exit code `0`; replay receipt; source SHA-256 `4789ffa95f4bc1eecd8b917025815ce20eac1e06c8b0445f4e1731ea92793609`. | Discrete integer grid samples only. |
| Smooth periodic integration by parts is replayed. | `NOT_REPLAYED` | No smooth functions, integrals, periodic domains, or divergence-free vector fields in Lean yet. | Next theorem target after typed-grid scaffolding. |
| Parent Navier-Stokes problem is solved. | `UNVERIFIABLE` | No global regularity proof, domain review, or accepted theorem artifact. | Must not be stated. |

## Source-Lead Refresh

Two Gather stores were added:

| Store | Rows | Seal |
| --- | ---: | --- |
| `arxiv-typed-finite-grid-lean` | 7 | `679f79fdae67e278cda7a00b4e0a90f58991ae75476ae7b209ca4272b0974e66` |
| `arxiv-cyclic-boundary-grid-formal` | 1 | `2cea033037dc16273c9c02979772860c25392c7c8c3bf7873cc3df2739ea0d22` |

Both stores verified as `MATCH`.

Demotion gate:

`docs/outreach/receipts/seventeenth-wave/source-lead-demotion-gate.json`

Counts:

- 8 retained metadata rows
- 8 unique arXiv IDs
- 6 formal-replay infrastructure leads
- 1 formal-PDE or analysis lead
- 1 adjacent scientific-computing lead
- 0 high-risk grand-claim rows

Verdict: `SOURCE_LEAD_ONLY`.

## Product Insight

The replay ladder now has four typed labels:

1. `LEAN_REPLAY_MATCH`: small integer cancellation.
2. `CYCLIC_SUM_REPLAY_MATCH`: scalar finite cyclic telescoping.
3. `CYCLIC_SUMMATION_BY_PARTS_MATCH`: paired finite cyclic summation by parts.
4. `TYPED_FINITE_GRID_SBP_MATCH`: named grid/sample vocabulary around the finite identity.

This matters because BuildLang/buildc relation receipts need stable domain words. A generic algebra proof is useful; a typed finite-grid proof is easier to connect to compiler/runtime receipts.

## Next Formal Target

Move from typed integer samples to an operator vocabulary:

```text
edgeGradient : CyclicGrid -> Edge -> Int
cyclicBoundary : CyclicGrid -> BoundaryEvidence
```

Then move to smooth periodic integration by parts only after the finite operator vocabulary is stable.

## Do Not Claim

- Do not claim the typed finite-grid theorem proves smooth periodic integration by parts.
- Do not claim Project Telos solved Navier-Stokes.
- Do not claim source leads prove paper truth.
- Do not claim latest or exhaustive literature coverage.
- Do not claim BuildLang/buildc has native relation-invariant receipts yet.
- Do not claim Lean is globally stable on PATH; this pass used explicit paths.
