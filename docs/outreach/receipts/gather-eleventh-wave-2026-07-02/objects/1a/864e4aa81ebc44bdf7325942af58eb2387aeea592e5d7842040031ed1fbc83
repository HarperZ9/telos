# Pass 0062 Ledger: Heat Equation Energy Identity

Date: 2026-07-01

Status: `MATCH_HEAT_EQUATION_IDENTITY_NOT_PROMOTED_LAW`

## Purpose

Create the first proof/equation packet after the buyer-evidence passes: a
bounded analytic identity for the one-dimensional heat equation on a periodic
domain.

Identity:

```text
d/dt ||u||_L2^2 = -2*kappa*||u_x||_L2^2
```

Scope: smooth finite Fourier-series solutions of `u_t = kappa * u_xx` on
`[0, 2*pi]` with periodic boundary conditions and `kappa > 0`.

This pass does not claim a new natural law, empirical physics result, or
general PDE theorem outside the stated assumptions.

## Artifacts

| Artifact | Purpose |
| --- | --- |
| `tools/compose_heat_equation_energy_identity.py` | Deterministic heat-equation identity composer and numerical probe. |
| `tools/test_heat_equation_energy_identity.py` | Focused RED/GREEN identity test. |
| `tools/probe_heat_equation_energy_identity.py` | Pass 0062 packet, thesis, and measurement generator. |
| `tools/validate_pass_0062_heat_equation_energy_identity.py` | Validator for identity scope, residuals, monotonicity, and non-promotion controls. |
| `schemas/heat-equation-energy-identity-pass-0062.json` | `HeatEquationEnergyIdentity/v1` artifact. |
| `schemas/pass-0062-heat-equation-energy-identity-validator-result.json` | Validator receipt. |
| `schemas/tool-receipts-pass-0062.json` | Index, Gather, Forum, Crucible, Telos, and shell receipts. |
| `packets/072-heat-equation-energy-identity.md` | Human-readable heat-equation identity packet. |
| `adversarial/pass-0062-heat-equation-energy-identity-steelman.md` | Local steelman. |
| `crucible/pass-0062-thesis.json` | Falsifiable claims. |
| `crucible/pass-0062-measurements.json` | Measurements/evidence. |
| `crucible/pass-0062-report.md` | Crucible report. |
| `crucible/pass-0062-run.json` | Crucible run record. |

## Measurements

| Check | Result |
| --- | --- |
| Promotion state | `IDENTITY_NOT_PROMOTED_LAW` |
| Law candidate status | `BOUNDED_MATHEMATICAL_IDENTITY` |
| Fourier modes in probe | 3 |
| Max symbolic residual | 0.0 |
| Max finite-difference residual | 2.7235955712967552e-09 |
| Energy monotone nonincreasing | true |
| Source anchors | 3 |
| Current promoted natural laws | none |

## Source Anchors

- MIT OCW 18.303 heat-equation notes: `https://ocw.mit.edu/courses/18-303-linear-partial-differential-equations-fall-2006/d11b374a85c3fde55ec971fe587f8a50_heateqni.pdf`
- Stanford Math 220B heat-equation notes: `https://web.stanford.edu/class/math220b/handouts/heateqn.pdf`
- UT finite-difference heat-equation teaching material: `https://www-udc.ig.utexas.edu/external/becker/teaching/557/problem_sets/problem_set_fd_explicit.pdf`

## Verification

```powershell
python docs\research\dogfood\tools\test_heat_equation_energy_identity.py
python docs\research\dogfood\tools\probe_heat_equation_energy_identity.py
python docs\research\dogfood\tools\validate_pass_0062_heat_equation_energy_identity.py
crucible run docs\research\dogfood\crucible\pass-0062-thesis.json --measurements docs\research\dogfood\crucible\pass-0062-measurements.json --registry docs\research\dogfood\crucible\registry --report docs\research\dogfood\crucible\pass-0062-report.md --out docs\research\dogfood\crucible\pass-0062-run.json --json
```

Crucible result: 8 claims, 8 MATCH, 0 DRIFT, 0 UNVERIFIABLE.

Thesis id: `233dc9ba5d536495`

Assessment seal: `fab185ee5ed40c1228565bd2552cd0ebb8b16e3f6c618b0df1a1456a0b9e144f`

## Tool Findings

- Telos operator doctor returned `MATCH`.
- Index status returned `MATCH`.
- Gather read `packets/072-heat-equation-energy-identity.md` with digest seal `3e731ca80aa562640fcc49961b7f7b6631f6d375c7bf28068e2ddf4878b413ee`.
- Forum routed the pass 0062 prompt to `project-telos`, `needs_escalation=false`.
- Crucible registry stats after this pass: 50 theses, 416 claims, 416 MATCH, 0 DRIFT, 0 UNVERIFIABLE.

## Next Pass

Build pass 0063 as a second equation/proof packet, preferably extending from
linear heat dissipation to a conservation or entropy identity with a different
failure mode: e.g. inviscid Burgers conservation before shock formation,
Fokker-Planck entropy dissipation, or a discrete symplectic invariant.
