# Formal Replay Preflight For Proof-Carrying PDE Packets

Subtitle: from executable witnesses to theorem-prover obligations in Project Telos

Date: 2026-07-02

Status: working paper draft for website-copy and official-copy conversion.

Evidence boundary: this draft records a method and a preflight state. It now contains bounded Lean replay rungs for integer cancellation, finite cyclic telescoping, finite cyclic summation by parts, typed finite-grid summation by parts, and explicit finite edge/operator summation by parts. It does not contain a smooth periodic integration-by-parts replay, does not solve Navier-Stokes, does not prove global regularity, and does not validate a physical-fluid simulation.

## Abstract

Scientific AI systems can produce plausible derivations and runnable witnesses faster than they can produce proof. The gap is not a reason to stop; it is a reason to label evidence precisely. We propose a formal replay preflight for proof-carrying PDE packets: every bounded mathematical subclaim is split into a source-bound statement, an executable reference witness, a compiler/runtime parity witness, a theorem-prover environment check, a source-lead demotion gate, and a public claim boundary.

We demonstrate the preflight on the Project Telos Navier-Stokes periodic skew-symmetry packet. The JavaScript reference kernel and BuildLang/buildc parity kernel both produce near-zero nonlinear energy transfer and zero divergence for one deterministic smooth periodic finite-mode field. Lean 4.31.0 now replays bounded finite algebraic rungs, including an explicit finite edge/operator summation-by-parts theorem. The continuous theorem remains `NOT_REPLAYED`, and fresh arXiv metadata is classified as source leads only.

## Claim Ledger

| Claim | Evidence state | Evidence | Missing work | Public wording |
| --- | --- | --- | --- | --- |
| The skew-symmetry packet has a compiled BuildLang parity witness. | `BUILD_PARITY_MATCH` | `kernel.buildlang.bld` and `buildlang-parity.receipt.json`; output transfer `1.41311e-14`, divergence `0`. | Native relation-invariant buildc receipt and negative fixtures. | "BuildLang can run a bounded parity witness for the packet." |
| Bounded theorem-prover replay rungs exist. | `FINITE_EDGE_OPERATOR_SBP_MATCH` | `FiniteEdgeOperatorPreflight.lean`; `lean-finite-edge-operator-sbp-replay-2026-07-02.json`; Lean exit code `0`; warning-clean replay. | Vector-valued finite operator theorem and smooth periodic integration-by-parts theorem. | "Lean replays a finite edge/operator identity, not the smooth theorem." |
| Fresh source intake produced formal-replay, finite-operator, and PDE review leads. | `SOURCE_LEAD_ONLY` | Nineteenth-wave Gather stores; 20 retained rows, 19 unique IDs; demotion gate classification. | Source-body review and citation verification. | "New source leads were queued and classified." |
| The packet proves Navier-Stokes existence and smoothness. | `UNVERIFIABLE` | No theorem proof, no official acceptance, no domain-grade review. | A proof meeting the grand problem standard. | Must not be stated. |

## Method

The preflight uses six gates.

1. `SOURCE_GATE`: official statement anchors and paper leads are captured but not promoted.
2. `SUBCLAIM_GATE`: a bounded mathematical statement is extracted with assumptions.
3. `WITNESS_GATE`: at least one deterministic executable witness measures the subclaim.
4. `RUNTIME_PARITY_GATE`: a second runtime or language implementation checks whether the witness survives a different toolchain.
5. `FORMAL_ENV_GATE`: a theorem-prover runner is required before proof replay can be claimed.
6. `PUBLIC_COPY_GATE`: outreach and paper drafts inherit the strongest proven evidence state and no stronger one.

## Demonstration

The target subclaim is:

```text
integral_Omega u dot ((u dot grad)u) dx dy = 0
```

for smooth divergence-free periodic two-dimensional velocity fields.

The current BuildLang parity kernel uses the same finite-mode streamfunction design as the JavaScript reference kernel. It computes analytic velocity and derivatives on a periodic grid and sums the nonlinear energy-transfer term.

Observed BuildLang output:

```text
1.41311e-14
0
```

Interpretation:

- `1.41311e-14` is below the `1e-10` nonlinear-transfer tolerance.
- `0` is below the `1e-12` divergence tolerance.
- The parent Navier-Stokes Millennium problem remains `UNVERIFIABLE`.

## BuildLang Advancement Target

The current buildc scientific-runtime receipt is valuable but too narrow for this packet. It supports output-series invariants such as monotone energy and conservation. PDE proof packets need named relation invariants:

```text
abs(nonlinear_energy_transfer) <= 1e-10
max_divergence_abs <= 1e-12
parent_claim == UNVERIFIABLE
```

This is a concrete language/runtime roadmap item. It would also generalize to:

- color calibration delta thresholds
- finance risk drift limits
- security policy conformance checks
- robotics state-estimation residuals
- biology model validation metrics

## Formal Replay Obligation

Bounded theorem-prover replay is now claimed only for finite discrete rungs. The next replay target should still be intentionally smaller than the full PDE problem:

> For smooth periodic vector fields with divergence zero, the integral of `u dot grad(|u|^2)` over the periodic domain is zero.

The immediate next step is a vector-valued finite operator vocabulary over the finite edge/operator theorem. Only after that should the smooth periodic theorem be encoded. This isolates the integration-by-parts and periodic-boundary obligation before touching global regularity, weak solutions, turbulence, or 3D existence.

## Source Review Queue

The nineteenth-wave demotion gate classified 19 unique arXiv IDs:

- 8 formalization-infrastructure leads
- 2 formal-PDE or analysis leads
- 3 adjacent scientific-computing leads
- 6 query-noise rows
- 0 high-risk grand-claim rows

These rows are metadata leads only. They should feed source-body review and citation reconciliation, not paper-truth claims.

## Publication Plan

Website copy should emphasize the tool-method contribution:

> executable witness, BuildLang parity, formal replay preflight, source demotion, and explicit non-resolution boundary.

Official copy should include:

- claim ledger
- mathematical subclaim and assumptions
- reference-kernel appendix
- BuildLang parity appendix
- theorem-prover environment preflight
- bounded Lean replay appendices
- source-demotion appendix
- limitation section with the parent problem kept `UNVERIFIABLE`

## Do Not Claim

- Do not claim smooth theorem-prover replay exists.
- Do not claim the bounded Lean replay rungs prove the smooth periodic theorem.
- Do not claim the BuildLang parity kernel proves the continuous PDE theorem.
- Do not claim native buildc scientific-runtime receipts support relation invariants yet.
- Do not claim arXiv metadata proves paper truth.
- Do not claim this solves Navier-Stokes or any Millennium problem.
- Do not claim buildc is warning-clean.
