# Sixteenth-Wave Cyclic Summation-By-Parts Replay

Date: 2026-07-02

Purpose: advance the formal replay ladder from scalar cyclic finite sums to a paired finite stencil in Lean, while preserving the boundary that smooth periodic integration by parts and Navier-Stokes remain unproved.

## Decision

The next publishable rung is now:

> a Lean-checked finite cyclic summation-by-parts theorem over paired integer samples.

This is closer to the periodic integration-by-parts identity used in PDE energy estimates than the scalar cyclic-sum theorem. It is still finite discrete algebra. The smooth theorem remains `NOT_REPLAYED`; the parent Navier-Stokes problem remains `UNVERIFIABLE`.

## Lean Artifact

Source:

`docs/research/proof-packets/navier-stokes-periodic-skew-symmetry-v0/formal/lean/CyclicSummationByPartsPreflight.lean`

Receipt:

`docs/outreach/receipts/sixteenth-wave/lean-cyclic-summation-by-parts-replay-2026-07-02.json`

Command:

```powershell
C:\Users\Zain\.elan\bin\lean.exe docs\research\proof-packets\navier-stokes-periodic-skew-symmetry-v0\formal\lean\CyclicSummationByPartsPreflight.lean
```

Observed result: exit code `0`.

Replayed theorem:

```text
ProjectTelos.FormalReplay.cyclic_summation_by_parts_cancels
```

Formal shape:

```text
cyclicGradientSum u phi xs + cyclicDivergenceSum u phi xs = 0
```

Readable stencil:

```text
sum_i u[i] * (phi[i+1] - phi[i])
+ sum_i phi[i] * (u[i] - u[i-1]) = 0
```

## Historical Receipt Preservation

The prior Lean files remain hash-stable:

| File | SHA-256 |
| --- | --- |
| `PeriodicCancellationPreflight.lean` | `77e5cba345adc1fd99003bfc17092750fddca1a9f879b4ac59f99e74c374a936` |
| `CyclicFiniteSumPreflight.lean` | `e69d314e73710f8ab58e45f1fdf9f353777dfd51e70087ebc575c8913014e115` |

The sixteenth-wave theorem is a new file, not a mutation of earlier receipt sources.

## Evidence States

| Claim | Evidence state | Evidence | Boundary |
| --- | --- | --- | --- |
| A finite cyclic paired-stencil summation-by-parts identity replays in Lean. | `CYCLIC_SUMMATION_BY_PARTS_MATCH` | Lean exit code `0`; replay receipt; source SHA-256 `f70b9df9da80e97b825ffbbf1bc30dbfe389bcee574167e4a18e36a12583f1a5`. | Discrete `List (Prod Int Int)` path only. |
| Smooth periodic integration by parts is replayed. | `NOT_REPLAYED` | No smooth functions, integrals, periodic domains, or divergence-free vector fields in Lean yet. | Next theorem target after finite-stencil scaffolding. |
| BuildLang parity witness remains bounded evidence. | `BUILD_PARITY_MATCH` | Existing BuildLang parity receipt with nonlinear transfer `1.41311e-14` and divergence `0`. | Compiled finite-mode witness, not theorem proof. |
| Parent Navier-Stokes problem is solved. | `UNVERIFIABLE` | No global regularity proof, domain review, or accepted theorem artifact. | Must not be stated. |

## Source-Lead Refresh

Two Gather stores were added:

| Store | Rows | Seal |
| --- | ---: | --- |
| `arxiv-summation-by-parts-formal` | 5 | `a668509b61e3c40bde913765bb0f506467ace6f864b7ff705c1ccb90a84e0c75` |
| `arxiv-discrete-integration-by-parts-lean` | 8 | `28ab33f153ba909edcb089f9da6fb952de9801a3758f9120682ff9735133b1e8` |

Both stores verified as `MATCH`.

Demotion gate:

`docs/outreach/receipts/sixteenth-wave/source-lead-demotion-gate.json`

Counts:

- 13 retained metadata rows
- 13 unique arXiv IDs
- 12 formal-replay infrastructure leads
- 1 formal-PDE or analysis lead
- 0 high-risk grand-claim rows

Verdict: `SOURCE_LEAD_ONLY`.

## Product Insight

The formal replay ladder now has a real finite-stencil rung:

1. `LEAN_REPLAY_MATCH`: small integer algebraic cancellation.
2. `CYCLIC_SUM_REPLAY_MATCH`: scalar finite cyclic telescoping.
3. `CYCLIC_SUMMATION_BY_PARTS_MATCH`: paired finite cyclic summation by parts.
4. `CONTINUOUS_THEOREM_TARGET_OPEN`: smooth periodic integration by parts is named but not replayed.

This is the shape the larger Telos system needs for frontier research: a proof ladder that can advance without flattening a toy identity, a finite stencil, a smooth theorem, and a Millennium problem into the same claim class.

## Next Formal Target

Move from integer paired samples to a typed finite grid vocabulary:

```text
GridPoint -> VectorField -> ScalarField -> CyclicBoundary
```

The next proof should keep the same finite identity but make the domain, edge operator, and cyclic boundary explicit enough that BuildLang/buildc can emit matching relation-invariant receipts later.

## Do Not Claim

- Do not claim the finite cyclic summation-by-parts theorem proves smooth periodic integration by parts.
- Do not claim Project Telos solved Navier-Stokes.
- Do not claim source leads prove paper truth.
- Do not claim latest or exhaustive literature coverage.
- Do not claim BuildLang/buildc has native relation-invariant receipts yet.
- Do not claim Lean is globally stable on PATH; this pass used explicit paths.
