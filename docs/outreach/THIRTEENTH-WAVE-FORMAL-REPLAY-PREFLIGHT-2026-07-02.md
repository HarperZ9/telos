# Thirteenth-Wave Formal Replay Preflight

Date: 2026-07-02

Purpose: move the Navier-Stokes proof-packet ladder from bounded executable witnesses toward a publishable formal-replay program. This pass adds a BuildLang/buildc parity kernel for the periodic skew-symmetry packet, records that theorem-prover replay is blocked by the current local environment, and demotes fresh arXiv metadata into a review queue instead of treating it as evidence.

## Decision

The next publishable unit is not another broad market map. It is a narrow, checkable method paper:

> how to take a grand-problem target, extract a bounded PDE subclaim, bind it to reference and BuildLang witnesses, preflight theorem-prover replay, and keep every non-proof claim demoted.

The parent Navier-Stokes Millennium problem remains `UNVERIFIABLE`.

## Current Tool Shape

| Layer | Current evidence | Verdict | Boundary |
| --- | --- | --- | --- |
| Telos | `node demo/operator-doctor.mjs --summary` reports 70 tools, 24 commands, 14/14 checks, `MATCH`. | `MATCH` | Operator/tool readiness only. |
| Gather | Four fresh arXiv stores retained 32 metadata rows, 27 unique IDs, with all store digests verified. | `SOURCE_LEAD_ONLY` | Metadata does not prove papers or literature coverage. |
| BuildLang/buildc | `kernel.buildlang.bld` compiled and ran through buildc 1.0.6; output nonlinear transfer `1.41311e-14`, divergence `0`. | `BUILD_PARITY_MATCH` | External parity receipt only; not native scientific-runtime receipt. |
| Learn | `learn doctor` reports `MATCH`; thirteenth-wave prooflesson is pending after package stabilization. | `MATCH` | Learn can preserve boundaries; it does not prove theorem content. |
| Theorem prover | `lean`, `lake`, `coqc`, and `isabelle` are not on PATH. | `BLOCKED_ENVIRONMENT` | No theorem-prover replay is claimed. |

## BuildLang Parity Kernel

New file:

`docs/research/proof-packets/navier-stokes-periodic-skew-symmetry-v0/kernel.buildlang.bld`

The kernel mirrors the JavaScript reference witness with the same finite Fourier-mode streamfunction family and analytic derivatives. It prints:

1. nonlinear energy transfer
2. maximum divergence magnitude

Observed run:

| Field | Value |
| --- | --- |
| nonlinear energy transfer | `1.41311e-14` |
| maximum divergence magnitude | `0` |
| transfer tolerance | `1e-10` |
| divergence tolerance | `1e-12` |
| verdict | `MATCH` |
| parent problem | `UNVERIFIABLE` |

Receipt:

`docs/research/proof-packets/navier-stokes-periodic-skew-symmetry-v0/buildlang-parity.receipt.json`

The key gap is productive: buildc scientific-runtime receipt v0 supports output-series invariants such as `energy-monotone` and `conservation`; this PDE packet needs relation/tolerance invariants over named measurements. That is now a concrete BuildLang/buildc advancement target.

## Source-Lead Demotion Gate

Four arXiv queries were run through Gather:

| Store | Rows | Seal |
| --- | ---: | --- |
| `arxiv-navier-stokes-formal-verification` | 8 | `1e8e6105cdd2e77403c9360ebb7065a48f4f21e0e281790a1c42001c6adab16b` |
| `arxiv-energy-estimate-proof-assistant` | 8 | `67875c378e484133141680732ab0f137da0d7ed3f3d10d7efc9386cbdb95e023` |
| `arxiv-periodic-integration-formal` | 8 | `daa35a9ed5a79bcc588ffbc1b45bcc5c480e8b23a97e2dd5ef25a0be5519b385` |
| `arxiv-verified-numerics-navier-stokes` | 8 | `a7311915780ea1c932ae614db208825ad7b20198a8a985d2f049176ba8f19411` |

Demotion result:

| Class | Count | Use |
| --- | ---: | --- |
| direct PDE leads | 6 | Source-body review for energy, regularity, stability, and boundary estimates. |
| formalization infrastructure | 11 | Lean/HOL/prover workflow ideas, not PDE evidence. |
| adjacent PDE or numerics | 7 | Keep in backlog until source-body review. |
| unverified grand-claim or high-risk rows | 3 | Do not promote without expert review and official-status reconciliation. |

Receipt:

`docs/outreach/receipts/thirteenth-wave/source-lead-demotion-gate.json`

## Formal Replay Preflight

Receipt:

`docs/outreach/receipts/thirteenth-wave/theorem-prover-preflight-2026-07-02.json`

Result: no local theorem prover executable was found.

Required next steps:

1. Install Lean 4 and Lake, or bind a remote theorem-prover runner with receipt capture.
2. Create a minimal project for the smooth periodic integration-by-parts identity.
3. Formalize the analytic identity separately from the finite-grid witness.
4. Emit a theorem-replay receipt only after the proof assistant accepts the statement.

## Product/Research Wedge

The market/research wedge sharpened again:

> Telos does not just run experiments. It shows where an experiment stops, what proof obligation remains, and which tool layer must advance next.

For BuildLang/buildc, the next valuable feature is a relation-invariant scientific receipt:

```text
named_measurement <= tolerance
abs(measurement_a - measurement_b) <= tolerance
parent_claim = UNVERIFIABLE
```

That would make PDE packets, finance risk checks, color calibration deltas, and security proof obligations all more naturally expressible.

## Seven-Day Push

1. Add a BuildLang relation-invariant receipt mode or an external adapter that exports Crucible measurements from named numeric stdout lines.
2. Install or bind Lean 4/Lake and produce the first accepted toy formalization for periodic integration by parts in a simplified finite-dimensional setting.
3. Convert the PDE proof-packet paper into website copy with a diagram of evidence states.
4. Source-body review the six direct PDE leads and two strongest formalization-infrastructure leads.
5. Add negative BuildLang fixtures: non-divergence-free field and boundary-condition mismatch.

## Do Not Claim

- Do not claim Project Telos solved Navier-Stokes.
- Do not claim theorem-prover replay exists.
- Do not claim BuildLang scientific-runtime receipts natively verify the skew-symmetry relation yet.
- Do not claim arXiv metadata proves paper claims.
- Do not claim source intake is latest or exhaustive.
- Do not claim buildc is warning-clean.
