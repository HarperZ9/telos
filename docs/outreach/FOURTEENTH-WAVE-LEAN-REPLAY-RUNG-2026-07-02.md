# Fourteenth-Wave Lean Replay Rung

Date: 2026-07-02

Purpose: convert the thirteenth-wave theorem-prover blocker into the first bounded Lean replay receipt, while keeping the continuous PDE theorem and Navier-Stokes parent problem unproved.

## Decision

The next proof ladder rung is now:

> one kernel-checked Lean algebraic cancellation lemma, then a later smooth-periodic integration-by-parts formalization.

This is progress from `BLOCKED_ENVIRONMENT`, but only inside a narrow formal scope. The parent Navier-Stokes Millennium problem remains `UNVERIFIABLE`.

## New Formal Replay Artifact

Lean source:

`docs/research/proof-packets/navier-stokes-periodic-skew-symmetry-v0/formal/lean/PeriodicCancellationPreflight.lean`

Receipt:

`docs/outreach/receipts/fourteenth-wave/lean-periodic-cancellation-replay-2026-07-02.json`

Command:

```powershell
C:\Users\Zain\.elan\bin\lean.exe docs\research\proof-packets\navier-stokes-periodic-skew-symmetry-v0\formal\lean\PeriodicCancellationPreflight.lean
```

Observed result: exit code `0`.

Replayed declarations:

- `ProjectTelos.FormalReplay.opposite_face_flux_cancels`
- `ProjectTelos.FormalReplay.two_cell_periodic_flux_stencil_cancels`

## Toolchain

| Tool | Version evidence |
| --- | --- |
| elan | `elan 4.2.3 (b6cec7e10 2026-06-08)` |
| Lean | `Lean (version 4.31.0, x86_64-w64-windows-gnu, commit 68218e876d2a38b1985b8590fff244a83c321783, Release)` |
| Lake | `Lake version 5.0.0-src+68218e8 (Lean version 4.31.0)` |

Install boundary: elan was installed locally under `C:\Users\Zain\.elan\bin` with `-NoModifyPath`. The explicit path works; this pass does not claim a globally stable PATH setup.

## Evidence States

| Claim | Evidence state | Evidence | Boundary |
| --- | --- | --- | --- |
| A Lean theorem prover can replay a small cancellation rung in this environment. | `LEAN_REPLAY_MATCH` | Lean command exit code `0`; replay receipt; source SHA-256 `77e5cba345adc1fd99003bfc17092750fddca1a9f879b4ac59f99e74c374a936`. | Algebraic integer cancellation only. |
| The continuous periodic integration-by-parts identity has been replayed. | `NOT_REPLAYED` | No Lean definitions for smooth functions, integrals, periodic domains, or divergence-free vector fields yet. | Next formalization target. |
| The BuildLang parity witness remains valid. | `BUILD_PARITY_MATCH` | Existing thirteenth-wave parity receipt with nonlinear transfer `1.41311e-14` and divergence `0`. | Finite-mode compiled witness, not a theorem proof. |
| The Navier-Stokes parent problem is solved. | `UNVERIFIABLE` | No global regularity proof, no domain review, no accepted theorem artifact. | Must not be stated. |

## Source-Lead Refresh

Three Gather arXiv stores were added:

| Store | Rows | Seal |
| --- | ---: | --- |
| `arxiv-lean-formal-pde` | 8 | `594b82b15ea0b6fd6d32ff86aa6253429f7c0141fad9ef1cceef3ffdc5cd9ce7` |
| `arxiv-formal-pde-proof-assistant` | 5 | `cafa73fa623854051f2900b826b94954c31cf605ea7379eede19d4090017168b` |
| `arxiv-lean-agent-provers` | 7 | `dc77ff68f274734a98f909557919a5adce761026404674c5d4542cff8f426ff3` |

All three stores verified as `MATCH`.

Demotion gate:

`docs/outreach/receipts/fourteenth-wave/source-lead-demotion-gate.json`

Counts:

- 20 retained metadata rows
- 16 unique arXiv IDs
- 8 formal-replay infrastructure leads
- 6 PDE domain leads
- 1 adjacent or noisy lead
- 1 high-risk grand-claim row

Verdict: `SOURCE_LEAD_ONLY`.

## Product Insight

The formal replay lane now has three distinct product states:

1. `BLOCKED_ENVIRONMENT`: no prover runner is available.
2. `LEAN_REPLAY_MATCH`: a small prover replay succeeds inside an explicit theorem scope.
3. `THEOREM_TARGET_OPEN`: the real mathematical target is named but not yet replayed.

This is the point of Telos: evidence states become product states, not vague prose.

## Next Formal Target

Move from integer cancellation to a theorem over a finite indexed periodic sum:

```text
sum_i (a[i+1] - a[i]) = 0
```

for a cyclic index type. That is still not the continuous PDE theorem, but it is much closer to periodic integration by parts and avoids pretending the full analytic stack is ready.

## Do Not Claim

- Do not claim Lean replay proves the continuous PDE identity.
- Do not claim Project Telos solved Navier-Stokes.
- Do not claim source leads prove paper truth.
- Do not claim latest or exhaustive literature coverage.
- Do not claim BuildLang/buildc has native relation-invariant receipts yet.
- Do not claim Lean is installed on PATH globally; this pass used explicit paths.
