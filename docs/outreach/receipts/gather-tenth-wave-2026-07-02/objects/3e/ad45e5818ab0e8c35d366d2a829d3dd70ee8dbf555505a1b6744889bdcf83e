# Pass 0089 Ledger: External Solver Adapter Receipt

Date: 2026-07-01

Status: `MATCH_EXTERNAL_SOLVER_ADAPTER_RECEIPT`

## Purpose

Move from local hand-coded branch comparison into a real installed solver
surface. This pass imports SciPy `dual_annealing` into the pass 0088
optimization receipt contract, records dependency/version evidence, and treats
OR-Tools as an unavailable local dependency instead of silently ignoring it.

## Artifacts

| Artifact | Purpose |
| --- | --- |
| `tools/compose_external_solver_adapter_receipt.py` | SciPy adapter, dependency, Forum, Index, and Telos composer. |
| `tools/test_external_solver_adapter_receipt.py` | Focused adapter, dependency, exact-match, and boundary test. |
| `tools/probe_external_solver_adapter_receipt.py` | Packet, brief, steelman, thesis, measurement, and compact receipt generator. |
| `tools/validate_pass_0089_external_solver_adapter_receipt.py` | Independent validator for seal, dependency receipts, exact comparison, and boundaries. |
| `schemas/external-solver-adapter-receipt-pass-0089.json` | `ExternalSolverAdapterReceipt/v1` artifact. |
| `schemas/pass-0089-external-solver-adapter-receipt-validator-result.json` | Validator receipt. |
| `schemas/tool-receipts-pass-0089.json` | Compact dependency, adapter, Forum, Index, Telos, compose, and test receipts. |
| `packets/099-external-solver-adapter-receipt.md` | Human-readable external solver adapter packet. |
| `briefs/099-external-solver-adapter-brief.md` | Concise product-strategy brief. |
| `adversarial/pass-0089-external-solver-adapter-steelman.md` | Local steelman of the adapter limits. |
| `crucible/pass-0089-thesis.json` | Falsifiable claims. |
| `crucible/pass-0089-measurements.json` | Measurements/evidence. |
| `crucible/pass-0089-report.md` | Crucible report. |
| `crucible/pass-0089-run.json` | Crucible run record. |

## Measurements

| Check | Result |
| --- | --- |
| Prior comparison pass | 0088 |
| Upstream video cluster | `enterprise_quantum_optimization` |
| Adapter | `scipy.optimize.dual_annealing` |
| Python version | 3.12.10 |
| NumPy version | 2.4.5 |
| SciPy version | 1.17.1 |
| OR-Tools available locally | false |
| Seed range | 8900..8915 |
| Run count | 16 |
| Max iterations per run | 128 |
| Function evaluations per run | 3073 |
| Exact optimum value | 162 |
| Adapter best value | 162 |
| Exact value gap | 0 |
| Exact hit count | 10 |
| Value distribution | `[158, 162]` |
| Runs digest | `e93c57f45a8eae67a5c06206e7b74e0b022587b708f8fc55c67c7e936c60d7b5` |
| Artifact seal | `86ef9d4327f0ecf8aa1266a069b149e162f31f03715ddc5bf94260fdf79ed504` |
| Promoted natural laws | 0 |

## Source Anchors

| Source | URL | Status |
| --- | --- | --- |
| SciPy dual annealing | `https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.dual_annealing.html` | `SOURCE_LEAD` |
| OR-Tools MIP example | `https://developers.google.com/optimization/mip/mip_example` | `SOURCE_LEAD` |
| Pass 0088 branch comparison | `docs/research/dogfood/pass-0088-ledger.md` | `LOCAL_BASELINE` |

## Product Finding

The first external-solver adapter proves the receipt shape can capture real
dependency state and stochastic variability. Ten of sixteen SciPy runs hit the
exact solution; six land at value 158. That variance is product-relevant: a
solver adapter should report hit counts and value distributions, not just best
observed output.

The missing OR-Tools dependency is also useful evidence. The megatool should
treat unavailable solver surfaces as explicit dependency receipts, preserving a
clean path for later installation or remote execution rather than letting the
market map imply coverage that is not locally present.

## Tool Findings

- Forum route receipt: `MATCH`, `needs_escalation=true`.
- Index context envelope: `MATCH`, schema `project-telos.context-envelope/v1`,
  graph pack SHA256
  `8ee383e19ae9a6141bee70de733fb6aa09201ff9d284ce6778ce58b06e6b68b2`.
- Telos status receipt: `MATCH`, tool version `0.1.0`.
- Gather packet receipt: SHA256
  `382b201f93e6d2cee8d56076d60f990e83a73150e1e43d6fcf9215ae283101dd`,
  digest seal `a59ab0c6f93ae733bbbb2db2bc57eeb6a95b15cea948d6b4c79edbc64143f877`.
- Gather brief receipt: SHA256
  `a86063d91d1437df43b8432c8d8feeff5d82634c8a96d4f516537196be4c6e9e`,
  digest seal `9564c6d5b0b9deafde77b12e0054a45f33e1f69da69c7d0adcbb164a35fac260`.
- Crucible result: 8 claims, 8 MATCH, 0 DRIFT, 0 UNVERIFIABLE.
- Crucible thesis id: `4055055c1a9659dd`.
- Crucible assessment seal:
  `90d9bbc05a7d6d72752b5b58bbc469ba61454543a0b2c5b0bf793ec25ba1aca0`.
- Crucible registry stats after this pass: 78 theses, 639 claims, 639 MATCH,
  0 DRIFT, 0 UNVERIFIABLE.

## Boundaries

This pass does not claim SciPy is the right solver for binary knapsack, does not
claim solver superiority, and does not claim quantum advantage, hardware
execution, new physics, or a natural law. Rounded continuous optimization is an
adapter exercise; proper discrete optimization remains the OR-Tools follow-up.

## Verification

```powershell
python -m py_compile docs\research\dogfood\tools\compose_external_solver_adapter_receipt.py docs\research\dogfood\tools\test_external_solver_adapter_receipt.py docs\research\dogfood\tools\validate_pass_0089_external_solver_adapter_receipt.py docs\research\dogfood\tools\probe_external_solver_adapter_receipt.py
python docs\research\dogfood\tools\probe_external_solver_adapter_receipt.py
python docs\research\dogfood\tools\test_external_solver_adapter_receipt.py
python docs\research\dogfood\tools\validate_pass_0089_external_solver_adapter_receipt.py
crucible run docs\research\dogfood\crucible\pass-0089-thesis.json --measurements docs\research\dogfood\crucible\pass-0089-measurements.json --registry docs\research\dogfood\crucible\registry --report docs\research\dogfood\crucible\pass-0089-report.md --out docs\research\dogfood\crucible\pass-0089-run.json --json
gather docs docs\research\dogfood\packets\099-external-solver-adapter-receipt.md --json
gather docs docs\research\dogfood\briefs\099-external-solver-adapter-brief.md --json
crucible registry stats docs\research\dogfood\crucible\registry --json
```

## Next Pass

Add an OR-Tools adapter after installing the dependency or build a solver
availability matrix that compares local, remote, and planned adapters across
SciPy, OR-Tools, D-Wave Ocean, MILP/CP-SAT, and BuildLang/buildc-native kernels.
