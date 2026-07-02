# Formal Replay Preflight for PDE Packets

Author: Zain Dana Harper
Status: working paper draft, not archive-submitted
Current evidence label: `VECTOR_FINITE_OPERATOR_SBP_MATCH` for one finite Lean theorem only
Updated: 2026-07-02

## Abstract

This working paper records a bounded Project Telos proof-packet pass for a
Navier-Stokes-adjacent identity. The goal is not to claim a solution to the
Navier-Stokes problem. The goal is to show a repeatable publication discipline:
source intake is demoted, executable and compiler evidence are separated from
formal theorem replay, and every public sentence is capped at the strongest
verified artifact.

The current formal replay rung is a Lean 4.31.0 theorem over finite integer
samples. It introduces two-component vector samples, cyclic grids, oriented
finite edges, and componentwise gradient/divergence-like operators. Lean
type-checks the cyclic identity

```text
cyclicVectorGradientOperatorSum grid
  + cyclicVectorDivergenceOperatorSum grid = 0
```

for that finite vocabulary. This is useful substrate work for a future smooth
periodic integration-by-parts theorem, but it is not that theorem.

## Evidence Ledger

| Item | Verdict | Evidence |
| --- | --- | --- |
| Vector finite operator Lean theorem | `VECTOR_FINITE_OPERATOR_SBP_MATCH` | `VectorFiniteOperatorPreflight.lean`, SHA-256 `a4d2682ea6bb4d9a38957a37b95cd9cdc63ba9ae9dedb2a559e8a47c8d12989a` |
| Lean toolchain | `MATCH` | Lean 4.31.0, Lake 5.0.0-src+68218e8, elan 4.2.3 |
| arXiv source intake | `SOURCE_LEAD_ONLY` | 30 retained rows, 25 unique IDs, 5 duplicate rows across three Gather stores |
| Crucible bounded thesis | `MATCH` | `twentieth-wave-tooling-run-2026-07-02.json`, assessment seal `e06f653404cda4f9b3f5a6f979e2884ebe207a396187941729dca29972a65502` |
| Learn prooflesson | `VERIFIED` | `twentieth-wave-vector-finite-operator.prooflesson.json`, head `b4d7fb7fac447e12bf19a2cb521ad7eba48dc7b5454cc684fc6f64dee8e0cee4` |
| Continuous periodic integration by parts | `NOT_REPLAYED` | No theorem-prover definitions for smooth periodic fields or integrals in this packet |
| Navier-Stokes existence/smoothness | `UNVERIFIABLE` | Not attempted by this finite replay package |

## What The Lean Theorem Actually Says

The Lean file defines a finite algebraic vocabulary:

- `Vector2Int`, a two-component integer vector.
- `VectorGridSample`, a finite sample carrying vector velocity and vector test
  components.
- `VectorCyclicGrid`, a finite cyclic path.
- `VectorFiniteEdge`, an oriented edge from one sample to the next.
- `vectorGradientEdgeOperator`, a finite edge contribution.
- `vectorDivergenceNodeOperator`, a finite node contribution.

It then proves an open-path endpoint identity and a cyclic cancellation theorem.
The proof is finite integer algebra. Its value is that the replay ladder has
advanced from scalar and typed-grid vocabulary into explicit vector/operator
vocabulary.

## Source Intake Boundary

The twentieth-wave Gather pass recorded three source stores:

- `arxiv-vector-sbp-formal-pde`
- `arxiv-lean-pde-vector-formalization`
- `arxiv-vector-sbp-numerical-analysis`

The demotion gate keeps these as leads. Highlighted leads include discrete
vector calculus for classical finite-difference SBP operators, structure-
preserving SBP methods for moist compressible Euler equations, formalization of
De Giorgi--Nash--Moser theory in Lean, CAM-Bench for computational and applied
mathematics in Lean, and Lean Copilot.

Those leads help choose the next proof targets. They do not prove the Telos
claim, and they do not license a statement that the continuous theorem has been
formalized.

## Publication Claim

The publishable claim is:

> Project Telos now has a finite vector/operator Lean replay rung for a
> cyclic summation-by-parts identity, plus a source-demotion gate that prevents
> research leads from being promoted into proof claims.

The publishable non-claim is just as important:

> Project Telos has not proved smooth periodic integration by parts in Lean and
> has not proved Navier-Stokes existence, uniqueness, or smoothness.

## Next Formal Target

The next target should be a theorem-prover representation of smooth periodic
two-dimensional vector fields and a deliberately narrow integration-by-parts
identity. Only after that rung exists should this packet talk about weak
solutions, energy estimates, or global regularity.

## Tooling Thesis

This pass tests the broader Telos publication pattern:

1. Gather records source leads with hashes and refs.
2. Index/Forum record context and routing state.
3. Lean provides a machine-checked finite theorem.
4. Crucible receives a thesis and measurements.
5. Learn converts the packet into a prooflesson so the operator can study the
   proof boundary without turning the lesson into an answer dump.
6. Website and official copy inherit the same capped verdicts.

Crucible assessed three bounded claims as `MATCH`: the Lean file compiles, the
three Gather stores verify as content-addressed stores, and the public claim
boundary keeps smooth PDE and Navier-Stokes claims outside the finite theorem.
Learn then converted the proof packet into a prooflesson and reverified the
lesson receipt from its own hash chain.

## Do Not Infer

- Do not infer that finite integer algebra proves a smooth PDE theorem.
- Do not infer that a matching Gather store proves the papers' contents.
- Do not infer that a website copy is an arXiv submission.
- Do not infer that this paper solves a Millennium problem.
- Do not infer that BuildLang/buildc has produced a native proof receipt for
  this finite Lean theorem.
