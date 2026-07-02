# Navier-Stokes Proof-Packet Program

Author: Project Telos

Date: 2026-07-02

Version: 0.1 official-copy working draft

Status: grand-problem isolation draft with bounded executable packets and finite Lean replay rungs

Evidence boundary: this draft chooses a focused research program and records bounded executable proof packets plus finite theorem-prover replay rungs: a smooth periodic Taylor-Green energy identity, a smooth periodic skew-symmetry witness, integer cancellation lemmas, a cyclic finite-sum theorem, a finite paired-stencil theorem, a typed finite-grid summation-by-parts theorem, and a finite edge/operator summation-by-parts theorem. It does not solve the Navier-Stokes Millennium problem, does not prove global regularity, does not replay smooth periodic integration by parts, and does not validate a physical fluid simulation.

## Abstract

Grand scientific goals fail operationally when ambition is allowed to skip evidence states. This draft proposes a proof-packet program for one canonical grand problem: Navier-Stokes existence and smoothness. The program treats the Millennium problem as `UNVERIFIABLE` until a domain-grade proof exists, while still allowing useful progress through bounded identities, finite-dimensional toy systems, finite theorem-prover replay rungs, compiler/runtime receipts, uncertainty notes, negative fixtures, and publication-ready claim boundaries.

The near-term contribution is a reproducible packet pattern: source-bound statement, subclaim extraction, formal or executable witness, BuildLang/buildc scientific-kernel receipt, Crucible verdict, Learn prooflesson, and public-copy boundary. The first target is not a grand theorem. It is a proof-carrying PDE subclaim that can be checked, taught, and published without misleading readers.

## Claim Ledger

| Claim | Scope | Evidence state | Evidence reference | Missing evidence | Public boundary |
| --- | --- | --- | --- | --- | --- |
| Navier-Stokes is a suitable primary grand target for the next Telos refinement phase. | Strategy decision. | `HYPOTHESIS_SELECTED` | Eleventh-wave scoring packet and public Clay/DOE anchors. | Independent mathematical advisor review. | May say "selected target"; may not say "solution path is proven." |
| Clay marks Navier-Stokes as an unsolved Millennium problem. | Official problem-status anchor. | `SOURCE_LEAD` | Clay Navier-Stokes page. | None for source existence; still missing source-body mathematical formalization. | May cite Clay; do not infer proof progress. |
| A proof-carrying PDE packet can produce publishable merit before a grand solution. | Research thesis. | `HYPOTHESIS` | Prior Telos proof-packet machinery, current source-router receipts, BuildLang/buildc receipts, and first two bounded PDE packets. | Reviewer feedback and theorem-prover replay. | State as thesis until external review and formal replay exist. |
| The eleventh-wave source-router captured 71 rows across 13 lanes. | Local source-intake count. | `PROBE_MATCH` | `docs/outreach/receipts/eleventh-wave/hard-problem-source-router-demotion-gate.json` | JSON parse and corpus verification. | Counts only, not literature coverage. |
| The first bounded Taylor-Green energy-identity packet has a reference kernel receipt and Crucible assessment. | One smooth periodic field under declared assumptions. | `CRUCIBLE_MATCH` | `docs/research/proof-packets/navier-stokes-periodic-energy-identity-v0/run.receipt.json` and `docs/research/proof-packets/navier-stokes-periodic-energy-identity-v0/crucible-run.json` | Formal theorem-prover replay, source-body formalization, BuildLang kernel version. | May claim bounded identity packet; may not claim the Millennium problem. |
| The second bounded skew-symmetry packet has a reference kernel receipt and Crucible assessment. | One deterministic smooth finite-mode periodic two-dimensional field plus written smooth-periodic derivation. | `CRUCIBLE_MATCH` | `docs/research/proof-packets/navier-stokes-periodic-skew-symmetry-v0/run.receipt.json` and `docs/research/proof-packets/navier-stokes-periodic-skew-symmetry-v0/crucible-run.json` | Formal theorem-prover replay, source-body formalization, BuildLang kernel version, and broader symbolic assumptions. | May claim bounded skew-symmetry packet; may not claim the Millennium problem. |
| The formal replay ladder reaches typed finite-grid summation by parts. | Finite discrete Lean theorem over integer samples. | `TYPED_FINITE_GRID_SBP_MATCH` | `docs/research/proof-packets/navier-stokes-periodic-skew-symmetry-v0/formal/lean/TypedFiniteGridSummationByPartsPreflight.lean` and `docs/outreach/receipts/seventeenth-wave/lean-typed-finite-grid-sbp-replay-2026-07-02.json` | Finite edge/operator vocabulary exists separately; vector-valued finite operator vocabulary, smooth periodic integration by parts, and source-body mathematical review remain missing. | May claim typed finite-grid replay; may not claim the smooth theorem. |
| The formal replay ladder now reaches finite edge/operator summation by parts. | Finite discrete Lean theorem over integer edge/operator structures. | `FINITE_EDGE_OPERATOR_SBP_MATCH` | `docs/research/proof-packets/navier-stokes-periodic-skew-symmetry-v0/formal/lean/FiniteEdgeOperatorPreflight.lean` and `docs/outreach/receipts/nineteenth-wave/lean-finite-edge-operator-sbp-replay-2026-07-02.json` | Vector-valued finite operator theorem, smooth periodic integration by parts, source-body mathematical review. | May claim finite edge/operator replay; may not claim the smooth theorem. |
| The current packet solves Navier-Stokes. | Grand theorem. | `UNVERIFIABLE` | No proof artifact, theorem replay, or peer-reviewed proof. | A domain-grade proof and review path. | Must never be stated. |

## Program Schema

`FrontierProblem`

| Field | Meaning |
| --- | --- |
| `id` | Stable problem identifier, such as `navier-stokes-existence-smoothness`. |
| `official_statement_refs` | Clay, source papers, or theorem statement references. |
| `grand_claim_status` | Always `UNVERIFIABLE` until proof/review standards are met. |
| `subclaims` | Bounded identity, finite model, numerical probe, or formal-statement cards. |
| `falsifiers` | What would refute the subclaim or block promotion. |
| `receipts` | Gather, Index, Forum, BuildLang, Crucible, Learn, and publication receipts. |
| `publication_boundary` | Exact wording allowed in public copy. |

`PDESubclaim`

| Field | Meaning |
| --- | --- |
| `statement` | A precise mathematical or computational statement. |
| `domain_assumptions` | Smoothness, boundary conditions, incompressibility, basis, projection, viscosity, dimensions. |
| `proof_obligation` | What must be proved or checked. |
| `computational_witness` | Command, environment, seed, data, hash, and output. |
| `verdict` | `SOURCE_LEAD`, `HYPOTHESIS`, `IDENTITY`, `PROBE_MATCH`, `CRUCIBLE_MATCH`, or `UNVERIFIABLE`. |
| `parent_problem_boundary` | Why the subclaim does not solve the grand problem. |

## First Packet

Packet id: `navier-stokes-periodic-energy-identity-v0`

Target statement:

Under explicitly stated smoothness, incompressibility, viscosity, and periodic-boundary assumptions, the kinetic-energy relation for the incompressible Navier-Stokes equations can be represented as a source-bound identity packet and checked against a small executable witness.

Required artifacts:

- `problem.statement.json`: source refs, equation form, assumptions, and parent-problem boundary.
- `subclaim.energy_identity.md`: derivation, missing formalization notes, and allowed public claim.
- `kernel.reference.mjs` or `kernel.reference.py`: minimal deterministic reference check.
- `kernel.buildlang.bld`: BuildLang version if compiler/runtime support is sufficient.
- `run.receipt.json`: command, seed, environment, output hash, and measured invariants.
- `crucible.measurements.json`: identity result, failure fixture, and grand-claim negative fixture.
- `navier-stokes-periodic-energy-identity.learn-packet.json`: teachable prooflesson packet preserving the verdict boundary.
- `learn-prooflesson/tutor/navier-stokes-periodic-energy-identity.prooflesson.json`: Learn prooflesson receipt; `learn tutor reverify` returned `VERIFIED`, witness digest `sha256:a5c2aa452645de360ce515b9444f886c9d117ea450358c6592c7c06f9f07158f`.

Promotion rule:

- The bounded identity may become `IDENTITY` or `CRUCIBLE_MATCH`.
- The parent Navier-Stokes Millennium problem remains `UNVERIFIABLE`.

Current receipt state:

- `docs/research/proof-packets/navier-stokes-periodic-energy-identity-v0/problem.statement.json`
- `docs/research/proof-packets/navier-stokes-periodic-energy-identity-v0/subclaim.energy_identity.md`
- `docs/research/proof-packets/navier-stokes-periodic-energy-identity-v0/kernel.reference.mjs`
- `docs/research/proof-packets/navier-stokes-periodic-energy-identity-v0/run.receipt.json`
- `docs/research/proof-packets/navier-stokes-periodic-energy-identity-v0/crucible-run.json`

The reference kernel run reports `bounded_identity_probe: MATCH`, `parent_millennium_problem: UNVERIFIABLE`, `residual_numeric_abs` about `7.46e-14`, and `max_divergence_abs: 0`. Crucible assesses the packet with 3 `MATCH`, 0 `DRIFT`, and 0 `UNVERIFIABLE` for the scoped identity and boundary claims only.

## Second Packet

Packet id: `navier-stokes-periodic-skew-symmetry-v0`

Target statement:

Under explicitly stated smoothness, incompressibility, and periodic-boundary assumptions, the nonlinear advection term has zero direct kinetic-energy contribution:

`integral u dot ((u dot grad)u) dx = 0`.

Required artifacts:

- `problem.statement.json`: source refs, domain assumptions, and parent-problem boundary.
- `subclaim.skew_symmetry.md`: written derivation, missing formalization notes, and allowed public claim.
- `kernel.reference.mjs`: deterministic finite-mode periodic reference check.
- `run.receipt.json`: command, environment, output hash, and measured invariants.
- `crucible-measurements.json`: subclaim result and negative-boundary fixtures.
- `navier-stokes-periodic-skew-symmetry.learn-packet.json`: prooflesson packet preserving the verdict boundary.
- `learn-prooflesson/tutor/navier-stokes-periodic-skew-symmetry.prooflesson.json`: Learn prooflesson receipt; `learn tutor reverify` returned `VERIFIED`, witness digest `sha256:cd3b2bc67e2658422589ae3835fe545b4d28aeb1e7a46dfc2b6028f54ccbb782`.

Promotion rule:

- The bounded skew-symmetry witness may become `IDENTITY` or `CRUCIBLE_MATCH`.
- The parent Navier-Stokes Millennium problem remains `UNVERIFIABLE`.

Current receipt state:

- `docs/research/proof-packets/navier-stokes-periodic-skew-symmetry-v0/problem.statement.json`
- `docs/research/proof-packets/navier-stokes-periodic-skew-symmetry-v0/subclaim.skew_symmetry.md`
- `docs/research/proof-packets/navier-stokes-periodic-skew-symmetry-v0/kernel.reference.mjs`
- `docs/research/proof-packets/navier-stokes-periodic-skew-symmetry-v0/run.receipt.json`
- `docs/research/proof-packets/navier-stokes-periodic-skew-symmetry-v0/crucible-run.json`

The reference kernel run reports `bounded_skew_symmetry_probe: MATCH`, `parent_millennium_problem: UNVERIFIABLE`, `nonlinear_energy_transfer_abs: 7.792811534956812e-14`, and `max_divergence_abs: 0`. Crucible assesses the packet with 3 `MATCH`, 0 `DRIFT`, and 0 `UNVERIFIABLE` for the scoped subclaim and boundary claims only.

## Negative Fixtures

| Fixture | Expected verdict | Why |
| --- | --- | --- |
| Missing incompressibility assumption | `UNVERIFIABLE` | Energy cancellation relies on the stated assumption. |
| Non-periodic boundary with no boundary term accounting | `UNVERIFIABLE` | Boundary terms change the identity. |
| Numerical-only blow-up headline | `UNVERIFIABLE` | Numerical behavior is not a theorem. |
| Galerkin finite model promoted as full PDE proof | `UNVERIFIABLE` | Finite truncation does not prove global regularity. |
| Grand theorem claim with only source metadata | `UNVERIFIABLE` | Metadata is not mathematical evidence. |

## BuildLang Role

BuildLang/buildc should not be presented as the whole system. Its role in this program is narrower and stronger:

1. Compile deterministic scientific kernels.
2. Emit runtime and policy receipts.
3. Make assumptions, units, seeds, and numeric types visible.
4. Provide a future path to interval arithmetic, exact rational checks, tensor kernels, spectral methods, GPU kernels, and proof-adjacent compiler witnesses.

The first BuildLang target is not performance. It is accountable reproducibility.

## Telos Megatool Composition

| Layer | Role in the Navier-Stokes program |
| --- | --- |
| Gather | Capture Clay sources, arXiv PDE/formalization leads, source-body refs, and digest seals. |
| Index | Select local packet, kernel, proof, and receipt context under a bounded budget. |
| Forum | Route packet work to proof, scientific-compute, publishing, or education lanes. |
| Crucible | Separate bounded identity matches from grand-theorem overclaims. |
| Telos | Join action receipts, context packs, model-foundry notes, browser evidence, and publication state. |
| Learn | Convert the packet into a prooflesson with the same verdict boundary. |
| BuildLang/buildc | Execute accountable scientific kernels and emit compiler/runtime receipts. |
| Build Color / rendering | Later visualize fluid/projection artifacts without converting visuals into proof. |
| Emet / witness layer | Later add external byte/view consistency receipts for publication artifacts. |

## Publication Plan

Working title:

> Proof-Carrying PDE Research Packets: A Navier-Stokes Subclaim Program for Accountable Scientific AI

Minimum publishable contribution:

- a clear claim-state ladder for grand-problem work
- a source-bound Navier-Stokes statement card
- two bounded PDE identity packets or one bounded identity plus a precise blocked proof packet
- at least one bounded theorem-prover replay rung with source and receipt hashes
- one negative fixture demonstrating overclaim rejection
- a BuildLang or reference-kernel run receipt
- a Crucible verdict
- a Learn prooflesson
- public-copy language that does not imply a solution

Target outlets:

- website working-paper page
- arXiv-style preprint draft after vector-valued finite operator replay, source-body statement review, or native BuildLang/buildc relation-invariant receipts strengthen the current finite replay ladder
- reproducibility/evaluation workshop if the packet is more tooling-centered than theorem-centered
- AI-for-science or scientific-computing venue after BuildLang receipts and negative fixtures are stronger

## Revision Gate

This draft can move from `HYPOTHESIS` to `PROBE_READY` only when:

- the first statement card exists
- the bounded identity is written in a formal, symbolic, or executable form
- a verifier can reject at least one negative fixture
- the public copy says exactly what is and is not proved

Current state: two bounded statement cards, executable reference kernels, run receipts, Crucible boundary assessments, Learn prooflesson receipts, BuildLang parity evidence, and five finite Lean replay rungs exist. A BuildLang/buildc heat-equation scientific-runtime receipt also exists as a nearby compiler/runtime proof object, but it is not a Navier-Stokes proof. The next gate is vector-valued finite operator vocabulary over the finite edge/operator theorem, then a smooth periodic integration-by-parts theorem, plus a stricter negative fixture that programmatically fails when an overbroad grand-theorem claim is submitted.

## Do Not Claim

- Do not claim a proof of Navier-Stokes existence and smoothness.
- Do not claim the program has found a new law of physics.
- Do not claim a numerical or Galerkin result proves the continuous PDE theorem.
- Do not claim source metadata is source-body review.
- Do not claim a working-paper draft is an accepted publication.
- Do not claim the BuildLang/buildc heat-equation receipt proves Navier-Stokes or PDE correctness.
- Do not claim the typed finite-grid Lean replay proves smooth periodic integration by parts.
- Do not claim the finite edge/operator Lean replay proves smooth periodic integration by parts.

## Revision Log

| Version | Date | Change | Evidence boundary |
| --- | --- | --- | --- |
| 0.1 | 2026-07-02 | Initial grand-problem isolation draft plus first bounded Taylor-Green identity packet. | Scoped executable identity and package-boundary receipts only. |
| 0.2 | 2026-07-02 | Added the bounded periodic skew-symmetry packet and connected it to the PDE proof ladder. | Scoped executable finite-mode witness, written smooth-periodic derivation, Learn prooflesson, and Crucible receipts only. |
| 0.3 | 2026-07-02 | Added the finite Lean replay ladder through the typed finite-grid summation-by-parts rung and narrowed the next publishable target to explicit finite edge/operator vocabulary. | Finite theorem-prover replay only; smooth periodic integration by parts and the parent Millennium problem remain unproved. |
| 0.4 | 2026-07-02 | Added the finite edge/operator Lean replay rung and narrowed the next publishable target to vector-valued finite operator vocabulary. | Finite theorem-prover replay only; smooth periodic integration by parts and the parent Millennium problem remain unproved. |
