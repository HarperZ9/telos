# Formal Replay Preflight For Proof-Carrying PDE Packets

Version: official-copy scaffold v0.1

Date: 2026-07-02

Author: Zain Dana Harper

Status: scaffold for official-copy conversion. Not submitted, accepted, peer-reviewed, archive-posted, or continuous-PDE theorem-prover accepted.

Website copy: `C:\dev\public\portfolio-site\research-formal-replay-preflight.html`

Source working draft: `docs/research/whitepapers/FORMAL-REPLAY-PREFLIGHT-FOR-PDE-PACKETS-2026-07-02.md`

## Evidence Boundary

This scaffold records a publication-ready shape for a proof-carrying PDE packet. It now includes one small Lean algebraic cancellation replay rung, one finite cyclic-sum replay rung, one finite paired-stencil summation-by-parts replay rung, one typed finite-grid replay rung, and one explicit finite edge/operator replay rung. It does not claim continuous periodic integration-by-parts replay, continuous PDE correctness, physical-fluid validation, warning-clean BuildLang/buildc status, or a solution to Navier-Stokes existence and smoothness.

The parent grand problem remains `UNVERIFIABLE`.

## Abstract Draft

Scientific AI systems can produce plausible derivations and runnable witnesses faster than they can produce proof. The gap should be surfaced as a first-class state rather than hidden behind confident prose. This paper proposes a formal replay preflight for proof-carrying PDE packets: each bounded mathematical subclaim is split into source intake, a precise statement, an executable reference witness, compiler/runtime parity, theorem-prover environment admission, source-lead demotion, and public claim boundaries.

The demonstration target is a Project Telos Navier-Stokes periodic skew-symmetry packet. The JavaScript reference witness and BuildLang/buildc parity witness both report near-zero nonlinear energy transfer and zero divergence for one deterministic smooth finite-mode periodic two-dimensional field. Lean 4.31.0, invoked by explicit path, now replays bounded finite rungs through explicit finite edge/operator summation by parts. Fresh arXiv metadata is classified as source leads only.

## Required Evidence-State Terms

| Term | Meaning |
| --- | --- |
| `SOURCE_LEAD_ONLY` | Captured source metadata or pointers worth reviewing; not a claim of truth. |
| `BUILD_PARITY_MATCH` | A bounded witness matched an expected relation through a BuildLang/buildc parity kernel and external receipt. |
| `LEAN_REPLAY_MATCH` | A named Lean file compiled under the recorded Lean toolchain. |
| `CYCLIC_SUM_REPLAY_MATCH` | A finite closed-path first-difference sum theorem compiled under the recorded Lean toolchain. |
| `CYCLIC_SUMMATION_BY_PARTS_MATCH` | A finite paired-stencil cyclic summation-by-parts theorem compiled under the recorded Lean toolchain. |
| `TYPED_FINITE_GRID_SBP_MATCH` | A typed finite-grid cyclic summation-by-parts theorem compiled under the recorded Lean toolchain. |
| `FINITE_EDGE_OPERATOR_SBP_MATCH` | An explicit finite edge/operator cyclic summation-by-parts theorem compiled under the recorded Lean toolchain. |
| `NOT_REPLAYED` | The target theorem has not yet been encoded and accepted by the prover. |
| `BLOCKED_ENVIRONMENT` | The proof or verification stage cannot run because required local tools are absent. |
| `UNVERIFIABLE` | Current evidence does not establish the claim as scoped. |

## Claim Table

| Claim | Scope | Status | Evidence | Missing evidence | Falsifier |
| --- | --- | --- | --- | --- | --- |
| The skew-symmetry packet has a compiled BuildLang parity witness. | One deterministic smooth finite-mode periodic two-dimensional field. | `BUILD_PARITY_MATCH` | `docs/research/proof-packets/navier-stokes-periodic-skew-symmetry-v0/kernel.buildlang.bld`; `docs/research/proof-packets/navier-stokes-periodic-skew-symmetry-v0/buildlang-parity.receipt.json`; observed output `1.41311e-14` and `0`. | Native buildc relation-invariant receipt; negative fixtures; broader field family. | Re-run emits output above tolerance or divergent field fails to block. |
| A small Lean algebraic cancellation rung replays. | Integer cancellation lemmas only. | `LEAN_REPLAY_MATCH` | `docs/research/proof-packets/navier-stokes-periodic-skew-symmetry-v0/formal/lean/PeriodicCancellationPreflight.lean`; `docs/outreach/receipts/fourteenth-wave/lean-periodic-cancellation-replay-2026-07-02.json`; Lean exit code `0`. | Cyclic finite-sum theorem; smooth periodic integration-by-parts theorem. | Lean compile fails or the receipt hash no longer matches the source. |
| A finite cyclic first-difference sum replays. | Discrete `List Int` closed path. | `CYCLIC_SUM_REPLAY_MATCH` | `docs/research/proof-packets/navier-stokes-periodic-skew-symmetry-v0/formal/lean/CyclicFiniteSumPreflight.lean`; `docs/outreach/receipts/fifteenth-wave/lean-cyclic-finite-sum-replay-2026-07-02.json`; Lean exit code `0`. | Paired finite-stencil theorem; smooth periodic integration-by-parts theorem. | Lean compile fails or the receipt hash no longer matches the source. |
| A finite cyclic paired-stencil summation-by-parts theorem replays. | Discrete `List (Prod Int Int)` closed path. | `CYCLIC_SUMMATION_BY_PARTS_MATCH` | `docs/research/proof-packets/navier-stokes-periodic-skew-symmetry-v0/formal/lean/CyclicSummationByPartsPreflight.lean`; `docs/outreach/receipts/sixteenth-wave/lean-cyclic-summation-by-parts-replay-2026-07-02.json`; Lean exit code `0`. | Typed finite-grid theorem; smooth periodic integration-by-parts theorem. | Lean compile fails or the receipt hash no longer matches the source. |
| A typed finite-grid summation-by-parts theorem replays. | Discrete integer `GridSample` and `CyclicGrid` vocabulary. | `TYPED_FINITE_GRID_SBP_MATCH` | `docs/research/proof-packets/navier-stokes-periodic-skew-symmetry-v0/formal/lean/TypedFiniteGridSummationByPartsPreflight.lean`; `docs/outreach/receipts/seventeenth-wave/lean-typed-finite-grid-sbp-replay-2026-07-02.json`; Lean exit code `0`. | Explicit finite edge/operator vocabulary exists separately; smooth periodic integration-by-parts theorem remains missing. | Lean compile fails or the receipt hash no longer matches the source. |
| A finite edge/operator summation-by-parts theorem replays. | Discrete integer `FiniteEdge`, `ForwardScalarDifference`, and `BackwardVelocityDifference` vocabulary. | `FINITE_EDGE_OPERATOR_SBP_MATCH` | `docs/research/proof-packets/navier-stokes-periodic-skew-symmetry-v0/formal/lean/FiniteEdgeOperatorPreflight.lean`; `docs/outreach/receipts/nineteenth-wave/lean-finite-edge-operator-sbp-replay-2026-07-02.json`; Lean exit code `0`; warning-clean replay. | Vector-valued finite operator theorem; smooth periodic integration-by-parts theorem. | Lean compile fails, warnings reappear, or the receipt hash no longer matches the source. |
| Continuous periodic integration by parts is replayed. | Smooth periodic vector fields and integrals. | `NOT_REPLAYED` | No Lean definitions for smooth fields, integrals, periodic domains, or divergence-free vector fields yet. | Formal theorem artifact accepted by Lean or another prover. | Any attempt to infer the continuous theorem from the integer or cyclic finite-sum lemmas. |
| Fresh source intake produced PDE, finite-operator, and formalization leads. | Two Gather arXiv stores from the nineteenth wave. | `SOURCE_LEAD_ONLY` | `docs/outreach/receipts/nineteenth-wave/source-lead-demotion-gate.json`; 20 retained rows, 19 unique IDs. | Source-body review, citation reconciliation, official-status checking. | Any row is posted as paper truth without body review or citation verification. |
| Parent Navier-Stokes proof. | Parent Millennium problem. | `UNVERIFIABLE` | No theorem replay, no domain review, no official acceptance, no global regularity proof. | Full proof artifact and independent review. | Any attempt to infer the parent theorem from this bounded witness. |

## Method

1. `SOURCE_GATE`: capture source candidates and official statements without promoting metadata into truth.
2. `SUBCLAIM_GATE`: extract a bounded mathematical statement with assumptions.
3. `WITNESS_GATE`: run a deterministic executable reference witness.
4. `RUNTIME_PARITY_GATE`: run a second implementation through BuildLang/buildc.
5. `FORMAL_ENV_GATE`: verify theorem-prover availability before replay is claimed.
6. `PUBLIC_COPY_GATE`: keep website copy, outreach copy, and official copy at the strongest proven evidence state and no stronger.

## Demonstration Subclaim

Target statement:

```text
integral_Omega u dot ((u dot grad)u) dx dy = 0
```

Scope:

- smooth periodic two-dimensional velocity fields
- divergence-free by construction through a finite-mode streamfunction
- deterministic grid witness
- bounded numerical tolerance only

Observed BuildLang/buildc parity output:

```text
1.41311e-14
0
```

Interpretation:

- `1.41311e-14` is below the `1e-10` nonlinear-transfer tolerance.
- `0` is below the `1e-12` divergence tolerance.
- This is evidence for a bounded parity witness only.

## Lean Replay Rung

The first replayed theorem file is intentionally small:

```text
docs/research/proof-packets/navier-stokes-periodic-skew-symmetry-v0/formal/lean/PeriodicCancellationPreflight.lean
```

Replayed declarations:

- `ProjectTelos.FormalReplay.opposite_face_flux_cancels`
- `ProjectTelos.FormalReplay.two_cell_periodic_flux_stencil_cancels`

Receipt:

```text
docs/outreach/receipts/fourteenth-wave/lean-periodic-cancellation-replay-2026-07-02.json
```

This proves only integer algebraic cancellation. It establishes the prover lane and the receipt shape; it does not establish the continuous mathematical identity.

## Cyclic Finite-Sum Replay Rung

The second replayed theorem file is still discrete, but closer to periodic integration-by-parts bookkeeping:

```text
docs/research/proof-packets/navier-stokes-periodic-skew-symmetry-v0/formal/lean/CyclicFiniteSumPreflight.lean
```

Replayed theorem:

```text
ProjectTelos.FormalReplay.cyclic_pathDiffSum_cancels
```

Formal shape:

```text
pathDiffSum start xs + (start - lastValue start xs) = 0
```

Receipt:

```text
docs/outreach/receipts/fifteenth-wave/lean-cyclic-finite-sum-replay-2026-07-02.json
```

This proves a finite closed-path first-difference identity over `List Int`. It does not establish smooth periodic integration by parts.

## Cyclic Summation-By-Parts Replay Rung

The third replayed theorem file adds a finite paired-stencil identity:

```text
docs/research/proof-packets/navier-stokes-periodic-skew-symmetry-v0/formal/lean/CyclicSummationByPartsPreflight.lean
```

Replayed theorem:

```text
ProjectTelos.FormalReplay.cyclic_summation_by_parts_cancels
```

Formal shape:

```text
cyclicGradientSum u phi xs + cyclicDivergenceSum u phi xs = 0
```

Receipt:

```text
docs/outreach/receipts/sixteenth-wave/lean-cyclic-summation-by-parts-replay-2026-07-02.json
```

This proves a finite cyclic summation-by-parts identity over `List (Prod Int Int)`. It does not establish smooth periodic integration by parts.

## Typed Finite-Grid Replay Rung

The fourth replayed theorem file adds typed finite-grid vocabulary:

```text
docs/research/proof-packets/navier-stokes-periodic-skew-symmetry-v0/formal/lean/TypedFiniteGridSummationByPartsPreflight.lean
```

Replayed theorem:

```text
ProjectTelos.FormalReplay.typed_finite_grid_summation_by_parts_cancels
```

Formal shape:

```text
cyclicGradientSum grid + cyclicDivergenceSum grid = 0
```

Receipt:

```text
docs/outreach/receipts/seventeenth-wave/lean-typed-finite-grid-sbp-replay-2026-07-02.json
```

This proves a typed finite-grid summation-by-parts identity over integer samples. It does not establish smooth periodic integration by parts.

## Finite Edge/Operator Replay Rung

The fifth replayed theorem file adds explicit finite edge and difference-operator vocabulary:

```text
docs/research/proof-packets/navier-stokes-periodic-skew-symmetry-v0/formal/lean/FiniteEdgeOperatorPreflight.lean
```

Replayed theorem:

```text
ProjectTelos.FormalReplay.finite_edge_operator_summation_by_parts_cancels
```

Formal shape:

```text
cyclicGradientOperatorSum grid + cyclicDivergenceOperatorSum grid = 0
```

Receipt:

```text
docs/outreach/receipts/nineteenth-wave/lean-finite-edge-operator-sbp-replay-2026-07-02.json
```

This proves a finite edge/operator summation-by-parts identity over integer samples. It does not establish smooth periodic integration by parts.

## Formal Replay Target

The first replay target should avoid the full Navier-Stokes parent theorem:

```text
For smooth periodic vector fields with div u = 0,
the integral over the periodic domain of u dot grad(|u|^2) is zero.
```

This isolates:

- product-rule expansion
- divergence-free cancellation
- periodic integration by parts
- boundary-term elimination

It intentionally excludes:

- three-dimensional global regularity
- existence and uniqueness
- weak solution theory
- turbulence
- physical-fluid validation
- numerical convergence claims

## BuildLang/buildc Advancement Requirement

The current parity receipt is external to native buildc scientific-runtime relation receipts. The compiler/runtime target is first-class relation invariants:

```text
abs(nonlinear_energy_transfer) <= 1e-10
max_divergence_abs <= 1e-12
parent_claim == UNVERIFIABLE
```

Acceptance gate for the next paper revision:

- buildc emits relation-invariant receipts directly.
- at least one negative fixture fails closed.
- the receipt includes program hash, toolchain version, invariant expression, tolerance, observed value, and verdict.
- Crucible can ingest the native receipt without hand-written translation.

## Source Review Requirement

The source demotion gate is not enough for an official citation layer. Before external publication:

- read and summarize the direct PDE leads.
- read and summarize the formalization-infrastructure leads.
- classify each as background, method dependency, contradiction, or unrelated.
- capture DOI/arXiv IDs and official versions.
- keep high-risk grand-claim rows in a cautionary appendix only unless independently validated.

## Publication Checklist

- [ ] Website copy exists and preserves all evidence boundaries.
- [ ] Official-copy scaffold exists with claim table, method, missing evidence, and falsifiers.
- [x] Lean theorem-prover environment receipt exists for the small algebraic rung.
- [x] A small Lean algebraic cancellation replay artifact exists.
- [x] Finite cyclic-sum Lean replay artifact exists.
- [x] Finite cyclic summation-by-parts stencil replay artifact exists.
- [x] Typed finite-grid cyclic summation-by-parts replay artifact exists.
- [x] Explicit finite edge/operator vocabulary replay artifact exists.
- [ ] Smooth periodic integration-by-parts replay artifact exists.
- [ ] Native buildc relation-invariant receipt exists or the runtime gap remains explicit.
- [ ] Negative fixtures exist for parity and claim-boundary failure.
- [ ] Source-body review exists for cited leads.
- [ ] External reviewer or domain expert feedback is recorded.
- [ ] Submission target is chosen.
- [ ] Archive/submission status is updated only after actual submission.

## Do Not Claim

- Do not claim continuous theorem-prover replay until a continuous-theorem replay artifact succeeds.
- Do not claim the integer cancellation lemmas prove the continuous PDE theorem.
- Do not claim the finite cyclic-sum theorem proves smooth periodic integration by parts.
- Do not claim the finite paired-stencil theorem proves smooth periodic integration by parts.
- Do not claim the typed finite-grid theorem proves smooth periodic integration by parts.
- Do not claim the finite edge/operator theorem proves smooth periodic integration by parts.
- Do not claim the BuildLang parity kernel proves the continuous PDE theorem.
- Do not claim native buildc relation-invariant receipts exist until buildc emits them.
- Do not claim arXiv metadata proves paper truth.
- Do not claim latest or exhaustive literature coverage.
- Do not claim this solves Navier-Stokes or any Millennium problem.
- Do not claim buildc is warning-clean.

## Next Thirty-Day Push

The most valuable next push is one small prover-replayed theorem:

1. Promote the finite edge/operator theorem into a vector-valued finite operator theorem.
2. Encode the smooth periodic integration-by-parts target only after the finite vector/operator vocabulary is stable.
3. Attach each proof artifact to the packet.
4. Add one negative theorem or failed-assumption fixture.
5. Add native BuildLang relation-invariant receipt support.
6. Re-run Crucible and Learn on the revised packet.

The target is not to solve the grand problem in one step. The target is to make one bounded rung of the proof ladder mechanically replayable, inspectable, and public without overclaiming.
