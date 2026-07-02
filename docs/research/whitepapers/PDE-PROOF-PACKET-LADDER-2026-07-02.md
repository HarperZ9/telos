# Proof-Carrying PDE Research Packets

Subtitle: a Navier-Stokes subclaim ladder for accountable scientific AI

Date: 2026-07-02

Status: working paper draft for website-copy and official-copy conversion.

Evidence boundary: this draft proposes and demonstrates a proof-packet ladder. It does not solve Navier-Stokes existence and smoothness, does not prove global regularity, and does not validate physical-fluid simulations.

## Abstract

Scientific AI systems increasingly assist with literature review, conjecture generation, code execution, and proof search. The operational failure mode is evidence collapse: a source lead, a numerical witness, a formal theorem, a model-generated explanation, and a publication claim are treated as interchangeable. We propose proof-carrying PDE research packets: a layered evidence structure that binds problem statements, scoped mathematical subclaims, executable witnesses, runtime receipts, verifier verdicts, learning receipts, and publication boundaries.

We demonstrate the pattern on a Navier-Stokes subclaim ladder. The parent Millennium problem remains `UNVERIFIABLE`. Two bounded periodic subclaims are packaged as reproducible artifacts: a Taylor-Green energy identity and a finite-mode skew-symmetry witness for the nonlinear advection term. We additionally connect the ladder to BuildLang/buildc scientific-runtime receipts through a heat-equation energy monotonicity receipt. The contribution is not a grand theorem; it is a method for making partial scientific evidence precise enough to publish without laundering it into a solved-problem claim.

## Claim Ledger

| Claim | Evidence state | Evidence | Missing work | Public wording |
| --- | --- | --- | --- | --- |
| Clay treats Navier-Stokes as an unsolved Millennium problem. | `SOURCE_LEAD` | Clay Navier-Stokes and Millennium pages. | None for source existence; still requires exact source-body statement extraction. | "Official problem anchor." |
| Taylor-Green periodic energy identity packet matches its bounded receipt. | `CRUCIBLE_MATCH` | `navier-stokes-periodic-energy-identity-v0`. | Theorem-prover replay. | "A bounded smooth-periodic identity packet matched." |
| Finite-mode periodic advection skew-symmetry packet matches its bounded receipt. | `CRUCIBLE_MATCH` | `navier-stokes-periodic-skew-symmetry-v0`, nonlinear transfer abs `7.792811534956812e-14`, divergence `0`, Crucible seal `4b51ecd5703231b5e80f566d2d41a5780b09447e38b1a348cc4f310e26fb31c8`. | Formal proof replay and broader negative fixtures. | "A second bounded Navier-Stokes subclaim matched." |
| BuildLang/buildc can emit a scientific-runtime receipt for a PDE-adjacent heat-equation energy witness. | `RUNTIME_RECEIPT_PASS` | `docs/outreach/receipts/twelfth-wave/buildlang-heat-equation-energy.receipt.json`, verify `status: match`, `receipt_status: PASS`, `violation_count: 0`, seal `e05d80773f8cc0400ff37abed44290e978dab1aec224760bc969c91932c5473e`. | BuildLang parity implementation for the Navier-Stokes skew-symmetry packet. | "buildc can witness observed invariant satisfaction for a compiled PDE-adjacent kernel." |
| arXiv rows gathered in this pass identify current source leads. | `SOURCE_LEAD_ONLY` | Two Gather arXiv metadata batches, seals `b328d373e8102b6e2637cc1ba3ac8930fbc5a65b1fc709cbb07792afe3e7eada` and `bf73ac9e3aa9418ed768577a0e7518f7bb28edf5bfd09ecdaf22dd087f6c9c54`. | Source-body review, relevance triage, citation verification. | "Source leads for review." |
| Project Telos solved Navier-Stokes. | `UNVERIFIABLE` | No proof artifact, no theorem-prover replay, no peer-reviewed proof. | Domain-grade proof and review. | Must not be stated. |

## Packet Schema

Each PDE proof packet should include:

- `problem.statement.json`: parent problem, subclaim, assumptions, negative boundaries.
- `subclaim.<name>.md`: derivation and exact proof obligations.
- `kernel.reference.*`: deterministic witness implementation.
- `run.receipt.json`: command, assumptions, measurements, tolerances, verdicts.
- `crucible-thesis.json`: falsifiable claims.
- `crucible-measurements.json`: measurement evidence.
- `crucible-run.json`: cleanroom verdict.
- `learn-packet.json` and prooflesson receipt: teachable boundary-preserving lesson.
- optional BuildLang/buildc source and scientific-runtime receipt.
- publication appendix: allowed wording and do-not-claim list.

## Demonstration 1: Taylor-Green Energy Identity

The first Navier-Stokes packet uses a smooth two-dimensional Taylor-Green velocity field on the periodic domain. It checks the energy identity for that field. The bounded identity matches; the parent problem remains `UNVERIFIABLE`.

This packet establishes the first rung: a single known smooth field can be bound to a source statement, executable receipt, Crucible verdict, and Learn prooflesson without claiming the Millennium problem.

## Demonstration 2: Periodic Skew-Symmetry

The second packet targets the nonlinear term:

```text
integral_Omega u dot ((u dot grad)u) dx dy = 0.
```

The derivation uses:

```text
u dot ((u dot grad)u) = (1/2) u dot grad(|u|^2)
```

and periodic integration by parts. For divergence-free `u`, the integral is zero.

The executable witness constructs a finite Fourier-mode streamfunction and derives `u = (partial_y psi, -partial_x psi)`, making the field analytically divergence-free. On a `256 x 256` grid, the reference kernel reports:

- `bounded_skew_symmetry_probe: MATCH`
- `parent_millennium_problem: UNVERIFIABLE`
- `nonlinear_energy_transfer_abs: 7.792811534956812e-14`
- `max_divergence_abs: 0`

Crucible assessed three claims and returned 3 `MATCH`, 0 `DRIFT`, 0 `UNVERIFIABLE`.

## BuildLang/buildc Role

BuildLang/buildc is not the whole Telos system. In this lane it is the accountable scientific runtime layer.

Current verified role:

- `buildc` 1.0.6 can compile and run a heat-equation energy kernel.
- `buildc run --emit-receipt` emits a sealed scientific-runtime receipt.
- `buildc receipt verify` re-runs the program and re-checks the invariant.
- The twelfth-wave heat-equation receipt verifies with `status: match`, `receipt_status: PASS`, and `violation_count: 0`.

Boundary:

- This proves an observed output-series invariant for one compiled program.
- It does not prove the continuous PDE.
- It does not prove the discretization is convergent.
- It does not prove a physical law.
- This pass observed a Rust dead-code warning, so warning-clean status is not claimed.

## Research Automation Pattern

The repeatable pattern is:

1. Gather source leads.
2. Demote metadata to `SOURCE_LEAD_ONLY`.
3. Extract one exact subclaim.
4. Write the derivation and proof obligations.
5. Build one deterministic witness.
6. Bind measurements to a Crucible thesis.
7. Convert the packet to Learn prooflesson.
8. Write website-copy and official-copy drafts from the same claim ledger.
9. Add theorem-prover replay or runtime parity in the next pass.

## Publication Plan

Website copy:

- short public-facing narrative
- diagrams of the evidence ladder
- receipt links
- strong do-not-claim box

Official copy:

- abstract and method
- claim ledger
- derivation
- reproducibility appendix
- verifier appendix
- limitation section

First target title:

> Proof-Carrying PDE Research Packets: A Navier-Stokes Subclaim Ladder for Accountable Scientific AI

## Do Not Claim

- Do not claim this solves Navier-Stokes.
- Do not claim a finite-mode witness proves global regularity.
- Do not claim a runtime receipt proves PDE correctness.
- Do not claim arXiv metadata validates paper truth.
- Do not claim a new law of physics.
- Do not claim warning-clean buildc output from this pass.

