# Fifteenth-Wave Cyclic Finite-Sum Replay

Date: 2026-07-02

Purpose: advance the formal replay ladder from two integer cancellation lemmas to a generic finite cyclic-sum cancellation theorem in Lean, while preserving the boundary that smooth periodic integration by parts and Navier-Stokes remain unproved.

## Decision

The next publishable rung is now:

> a Lean-checked finite cyclic first-difference sum cancellation theorem.

This is closer to periodic integration by parts than the two-face integer stencil, but it is still discrete algebra. The continuous theorem remains `NOT_REPLAYED`; the parent Navier-Stokes problem remains `UNVERIFIABLE`.

## Lean Artifact

Source:

`docs/research/proof-packets/navier-stokes-periodic-skew-symmetry-v0/formal/lean/CyclicFiniteSumPreflight.lean`

Receipt:

`docs/outreach/receipts/fifteenth-wave/lean-cyclic-finite-sum-replay-2026-07-02.json`

Command:

```powershell
C:\Users\Zain\.elan\bin\lean.exe docs\research\proof-packets\navier-stokes-periodic-skew-symmetry-v0\formal\lean\CyclicFiniteSumPreflight.lean
```

Observed result: exit code `0`.

Replayed theorem:

```text
ProjectTelos.FormalReplay.cyclic_pathDiffSum_cancels
```

Formal shape:

```text
pathDiffSum start xs + (start - lastValue start xs) = 0
```

This is the finite closed-path version of:

```text
sum_i (a[i+1] - a[i]) = 0
```

## Historical Receipt Preservation

The fourteenth-wave Lean file remains hash-stable:

`docs/research/proof-packets/navier-stokes-periodic-skew-symmetry-v0/formal/lean/PeriodicCancellationPreflight.lean`

SHA-256:

`77e5cba345adc1fd99003bfc17092750fddca1a9f879b4ac59f99e74c374a936`

The fifteenth-wave theorem is a new file, not a mutation of the earlier receipt source.

## Evidence States

| Claim | Evidence state | Evidence | Boundary |
| --- | --- | --- | --- |
| A finite cyclic first-difference sum cancels in Lean. | `CYCLIC_SUM_REPLAY_MATCH` | Lean exit code `0`; cyclic finite-sum receipt; source SHA-256 `e69d314e73710f8ab58e45f1fdf9f353777dfd51e70087ebc575c8913014e115`. | Discrete `List Int` path only. |
| Continuous periodic integration by parts is replayed. | `NOT_REPLAYED` | No smooth functions, integrals, periodic domains, or divergence-free vector fields in Lean yet. | Next theorem target after finite-sum scaffolding. |
| BuildLang parity witness remains bounded evidence. | `BUILD_PARITY_MATCH` | Existing BuildLang parity receipt with nonlinear transfer `1.41311e-14` and divergence `0`. | Compiled finite-mode witness, not theorem proof. |
| Parent Navier-Stokes problem is solved. | `UNVERIFIABLE` | No global regularity proof, domain review, or accepted theorem artifact. | Must not be stated. |

## Source-Lead Refresh

Two Gather stores were added:

| Store | Rows | Seal |
| --- | ---: | --- |
| `arxiv-lean-finite-sum` | 8 | `ea60721de78b6c1bd33e0ce2b578c4f87ed58fb3fa7ea78e6c0cc5373c58ecec` |
| `arxiv-periodic-finite-difference-formal` | 7 | `64ce5fc387f96e59895e47602ca192e74d6369604d3680c9b9fd311aa8e1b1c7` |

Both stores verified as `MATCH`.

Demotion gate:

`docs/outreach/receipts/fifteenth-wave/source-lead-demotion-gate.json`

Counts:

- 15 retained metadata rows
- 15 unique arXiv IDs
- 12 formal-replay infrastructure leads
- 3 formal-PDE or periodic-boundary leads
- 0 high-risk grand-claim rows

Verdict: `SOURCE_LEAD_ONLY`.

## Product Insight

The formal replay ladder now has sharper gradations:

1. `LEAN_REPLAY_MATCH`: a small algebraic prover rung exists.
2. `CYCLIC_SUM_REPLAY_MATCH`: a finite telescoping/cyclic sum prover rung exists.
3. `CONTINUOUS_THEOREM_TARGET_OPEN`: smooth periodic integration by parts is named but not replayed.

This is exactly the product behavior Telos needs for science-scale work: the system can move forward without collapsing different proof strengths into one label.

## Next Formal Target

Move from finite `List Int` paths to a finite-dimensional vector-field stencil:

```text
sum_i u[i] * (phi[i+1] - phi[i]) = - sum_i phi[i] * (u[i] - u[i-1])
```

under cyclic indexing. That is still not smooth analysis, but it is much closer to integration by parts and connects directly to numerical PDE proof packets.

## Do Not Claim

- Do not claim the finite cyclic-sum theorem proves smooth periodic integration by parts.
- Do not claim Project Telos solved Navier-Stokes.
- Do not claim source leads prove paper truth.
- Do not claim latest or exhaustive literature coverage.
- Do not claim BuildLang/buildc has native relation-invariant receipts yet.
- Do not claim Lean is globally stable on PATH; this pass used explicit paths.
