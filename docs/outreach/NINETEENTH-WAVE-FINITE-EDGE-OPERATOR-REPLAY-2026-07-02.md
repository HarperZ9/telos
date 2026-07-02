# Nineteenth-Wave Finite Edge/Operator Replay

Date: 2026-07-02

Purpose: advance the formal replay ladder from typed finite-grid samples to explicit finite edge and difference-operator vocabulary, while preserving the boundary that smooth periodic integration by parts and Navier-Stokes remain unproved.

## Decision

The next publishable rung is now:

> a Lean-checked finite edge/operator cyclic summation-by-parts theorem.

This adds explicit `FiniteEdge`, `ForwardScalarDifference`, and `BackwardVelocityDifference` structures around the same finite cancellation identity. It is closer to a reusable operator vocabulary for BuildLang/buildc relation receipts, but it is still finite discrete integer algebra. The smooth theorem remains `NOT_REPLAYED`; the parent Navier-Stokes problem remains `UNVERIFIABLE`.

## Lean Artifact

Source:

`docs/research/proof-packets/navier-stokes-periodic-skew-symmetry-v0/formal/lean/FiniteEdgeOperatorPreflight.lean`

Receipt:

`docs/outreach/receipts/nineteenth-wave/lean-finite-edge-operator-sbp-replay-2026-07-02.json`

Command:

```powershell
C:\Users\Zain\.elan\bin\lean.exe docs\research\proof-packets\navier-stokes-periodic-skew-symmetry-v0\formal\lean\FiniteEdgeOperatorPreflight.lean
```

Observed result: exit code `0`, no Lean stdout/stderr.

Replayed theorem:

```text
ProjectTelos.FormalReplay.finite_edge_operator_summation_by_parts_cancels
```

Formal shape:

```text
cyclicGradientOperatorSum grid + cyclicDivergenceOperatorSum grid = 0
```

## Evidence States

| Claim | Evidence state | Evidence | Boundary |
| --- | --- | --- | --- |
| A finite edge/operator cyclic summation-by-parts theorem replays in Lean. | `FINITE_EDGE_OPERATOR_SBP_MATCH` | Lean exit code `0`; replay receipt; source SHA-256 `afc5b4d4aef3ca745a383fbaba686082feae9633bda579ab30674e4224ec67aa`. | Discrete integer samples, finite edges, and difference operators only. |
| Smooth periodic integration by parts is replayed. | `NOT_REPLAYED` | No smooth functions, integrals, periodic domains, or divergence-free vector fields in Lean yet. | Next theorem target after finite operator vocabulary. |
| Parent Navier-Stokes problem is solved. | `UNVERIFIABLE` | No global regularity proof, domain review, or accepted theorem artifact. | Must not be stated. |

## Source-Lead Refresh

Two Gather stores were added:

| Store | Rows | Seal |
| --- | ---: | --- |
| `arxiv-finite-operator-sbp-lean` | 10 | `d56d81f0fd01a5ad5eed375bbc70c71ea1d5aa43c0b7e79a60b5fcb1b5687242` |
| `arxiv-finite-volume-formal-pde` | 10 | `4651683b8bcb1cf1f43c7b6e118ddc62cee55b2de04b09d4509bd980eb544911` |

Both stores verified as `MATCH`.

Demotion gate:

`docs/outreach/receipts/nineteenth-wave/source-lead-demotion-gate.json`

Counts:

- 20 retained metadata rows
- 19 unique arXiv IDs
- 8 formal-replay infrastructure leads
- 2 formal-PDE or analysis leads
- 3 adjacent scientific-computing leads
- 6 query-noise rows
- 0 high-risk grand-claim rows

Verdict: `SOURCE_LEAD_ONLY`.

## Routing And Context

Forum routed the pass to `project-telos` with no escalation.

Index evidence:

- installed `index.exe` wrapper failed with `ModuleNotFoundError: No module named 'index_graph'`
- source-checkout `python -m index_graph status --json` returned `MATCH`
- source-checkout `python -m index_graph doctor --json` returned `MATCH`
- broad focus returned `unresolved-focus`
- concrete focus `telos` returned context-envelope `verification_verdict: MATCH`

Route summary:

`docs/outreach/receipts/nineteenth-wave/forum-index-route-2026-07-02.json`

## Product Insight

The replay ladder now has five typed labels:

1. `LEAN_REPLAY_MATCH`: small integer cancellation.
2. `CYCLIC_SUM_REPLAY_MATCH`: scalar finite cyclic telescoping.
3. `CYCLIC_SUMMATION_BY_PARTS_MATCH`: paired finite cyclic summation by parts.
4. `TYPED_FINITE_GRID_SBP_MATCH`: named grid/sample vocabulary around the finite identity.
5. `FINITE_EDGE_OPERATOR_SBP_MATCH`: explicit finite edge and difference-operator vocabulary around the finite identity.

This matters because compiler/runtime receipts need stable domain words. A proof over named edges and difference operators is easier to map into BuildLang/buildc relation-invariant receipts than a proof over anonymous pairs.

## Next Formal Target

Move from finite edge/operator algebra to one of these two targets:

1. a finite-dimensional vector-field operator vocabulary with vector-valued samples and dot products, or
2. a first smooth periodic integration-by-parts statement in Lean or another prover.

The safer next step is the vector-valued finite operator theorem, because it keeps the proof ladder mechanical while moving closer to the actual Navier-Stokes skew-symmetry expression.

## Do Not Claim

- Do not claim the finite edge/operator theorem proves smooth periodic integration by parts.
- Do not claim Project Telos solved Navier-Stokes.
- Do not claim source leads prove paper truth.
- Do not claim latest or exhaustive literature coverage.
- Do not claim BuildLang/buildc has native relation-invariant receipts yet.
- Do not claim the installed `index.exe` wrapper is healthy; this pass used source-checkout `index_graph`.
- Do not claim the `telos` wrapper is on PATH in this shell.
- Do not claim Lean is globally stable on PATH; this pass used explicit paths.
