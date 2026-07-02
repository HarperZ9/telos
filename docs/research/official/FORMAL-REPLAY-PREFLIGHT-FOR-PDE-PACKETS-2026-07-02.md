# Formal Replay Preflight for PDE Packets

Official local copy for publication packaging.
Author: Zain Dana Harper
Date: 2026-07-02
Status: working draft, not archive-submitted

## Official Status

`VECTOR_FINITE_OPERATOR_SBP_MATCH` applies only to the finite Lean theorem in
`VectorFiniteOperatorPreflight.lean`.

`SOURCE_LEAD_ONLY` applies to the twentieth-wave arXiv intake.

`UNVERIFIABLE` applies to the parent Navier-Stokes problem in this package.

## Abstract

Project Telos is building proof-centered research packets that preserve the
difference between source intake, executable evidence, compiler/runtime
receipts, theorem-prover replay, and public claims. This official local copy
records a finite vector/operator replay rung for a PDE-adjacent packet. The
machine-checked theorem is a discrete cyclic summation-by-parts identity over
two-component integer samples. It is a bounded proof artifact and a staging
point for future formal PDE work, not a proof of a continuous PDE theorem.

## Verified Artifacts

- Lean file:
  `docs/research/proof-packets/navier-stokes-periodic-skew-symmetry-v0/formal/lean/VectorFiniteOperatorPreflight.lean`
- Lean file SHA-256:
  `a4d2682ea6bb4d9a38957a37b95cd9cdc63ba9ae9dedb2a559e8a47c8d12989a`
- Replay receipt:
  `docs/outreach/receipts/twentieth-wave/lean-vector-finite-operator-sbp-replay-2026-07-02.json`
- Source demotion gate:
  `docs/outreach/receipts/twentieth-wave/source-lead-demotion-gate.json`
- Learn packet:
  `docs/outreach/receipts/twentieth-wave/twentieth-wave-vector-finite-operator.learn-packet.json`
- Crucible thesis:
  `docs/outreach/receipts/twentieth-wave-tooling-thesis-2026-07-02.json`
- Crucible run:
  `docs/outreach/receipts/twentieth-wave-tooling-run-2026-07-02.json`
- Crucible report:
  `docs/outreach/receipts/twentieth-wave-tooling-report-2026-07-02.md`
- Learn prooflesson receipt:
  `docs/outreach/receipts/twentieth-wave/learn-prooflesson/tutor/twentieth-wave-vector-finite-operator.prooflesson.json`

## Claim Boundary

The theorem-prover claim is finite and algebraic:

```text
cyclicVectorGradientOperatorSum grid
  + cyclicVectorDivergenceOperatorSum grid = 0
```

It does not define smooth fields, integrals, periodic manifolds, weak solutions,
viscosity, pressure, or Navier-Stokes equations.

## Publication Checklist

- [x] The finite vector/operator Lean theorem exists.
- [x] The theorem was compiled with Lean 4.31.0.
- [x] The source intake was demoted to `SOURCE_LEAD_ONLY`.
- [x] The official copy states the non-claim boundary.
- [x] Crucible assessed the bounded publication claims as `MATCH`.
- [x] Learn reverified the prooflesson receipt as `VERIFIED`.
- [ ] A smooth periodic integration-by-parts theorem exists in Lean.
- [ ] A native buildc relation-invariant receipt exists for the same theorem.
- [ ] An archive submission has been made.

## Next Submission Gate

Do not submit this as a solved-problem paper. The correct submission shape is a
methods or systems working paper about proof-packet discipline for frontier
mathematics: how to move from source intake to bounded replay without
overclaiming.
