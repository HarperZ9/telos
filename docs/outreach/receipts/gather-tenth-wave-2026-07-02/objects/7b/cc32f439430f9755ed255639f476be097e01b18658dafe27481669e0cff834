# Pass 0100 Ledger: Ocean/dimod BQM Branch Receipt

Date: 2026-07-01

Status: `OCEAN_DIMOD_BQM_BRANCH_RECEIPT_MATCH`

## Purpose

Upgrade the remaining D-Wave/Ocean dependency-boundary lane into an executed
local Ocean-compatible branch. This pass uses `dimod.ExactSolver` over a
penalized binary quadratic model in an isolated temporary virtual environment.
It is explicitly local CPU execution, not QPU or hybrid-provider execution.

## Artifacts

| Artifact | Purpose |
| --- | --- |
| `tools/compose_ocean_dimod_bqm_branch_receipt.py` | Creates temp venv, installs `dimod`, runs BQM exact solver, records Forum/Index/Telos receipts, and cleans temp state. |
| `tools/test_ocean_dimod_bqm_branch_receipt.py` | Focused BQM branch-output, term-count, temp-cleanup, and boundary test. |
| `tools/probe_ocean_dimod_bqm_branch_receipt.py` | Packet, brief, steelman, thesis, measurement, and compact receipt generator. |
| `tools/validate_pass_0100_ocean_dimod_bqm_branch.py` | Independent validator for seal, branch result, BQM shape, cleanup, and boundaries. |
| `schemas/ocean-dimod-bqm-branch-receipt-pass-0100.json` | `OceanDimodBQMBranchReceipt/v1` artifact. |
| `schemas/pass-0100-ocean-dimod-bqm-branch-validator-result.json` | Validator receipt. |
| `schemas/tool-receipts-pass-0100.json` | Compact compose, test, Forum, Index, Telos, dimod version, and branch receipts. |
| `packets/110-ocean-dimod-bqm-branch-receipt.md` | Human-readable Ocean/dimod BQM branch packet. |
| `briefs/110-ocean-dimod-bqm-branch-brief.md` | Concise product-strategy brief. |
| `adversarial/pass-0100-ocean-dimod-bqm-branch-steelman.md` | Local steelman of local-CPU and BQM-encoding limits. |
| `crucible/pass-0100-thesis.json` | Falsifiable claims. |
| `crucible/pass-0100-measurements.json` | Measurements/evidence. |
| `crucible/pass-0100-report.md` | Crucible report. |
| `crucible/pass-0100-run.json` | Crucible run record. |

## Measurements

| Check | Result |
| --- | --- |
| Interop pass | 0098 |
| OR-Tools pass | 0099 |
| Global dimod available | false |
| Global dwave namespace available | false |
| Temporary venv path | `C:\Users\Zain\AppData\Local\Temp\telos-dimod-pass0100` |
| Temporary venv created | true |
| Temporary venv cleaned | true |
| dimod install exit code | 0 |
| dimod run exit code | 0 |
| dimod version | `0.12.22` |
| Branch schema | `SolverBranchReceipt/v1` |
| Branch id | `ocean_dimod_exact_bqm` |
| Execution status | `EXECUTED_LOCAL_CPU_EXACT_SOLVER` |
| BQM penalty | 200 |
| BQM linear terms | 12 |
| BQM quadratic terms | 66 |
| BQM best energy | -162.0 |
| Value | 162 |
| Weight | 29 |
| Mask | 2347 |
| Selected items | `A,B,D,F,I,L` |
| Gap to exact | 0 |
| Artifact seal | `f387d6efcef2e71273f577213aa1db00afa00f225f4f32b8fe646680f2f3872b` |
| Promoted natural laws | 0 |

## Source Anchors

| Source | URL | Bound Claim |
| --- | --- | --- |
| Installing Ocean SDK | `https://docs.dwavequantum.com/en/latest/ocean/install.html` | Ocean requires Python and supports Python 3.10+. |
| dimod | `https://docs.dwavequantum.com/en/latest/ocean/api_ref_dimod/index.html` | dimod is a shared API for samplers and BQMs. |
| dimod ExactSolver | `https://docs.dwavequantum.com/en/latest/ocean/api_ref_dimod/generated/dimod.reference.samplers.ExactSolver.sample.html` | ExactSolver samples all possible solutions to a BQM. |

## Product Finding

`OptimizationProofWorkbench/v1` now has local executed receipts across Python
exact enumeration, SciPy, NetworkX, OR-Tools, BuildLang, and Ocean/dimod. The
remaining gap is provider-backed D-Wave QPU or hybrid execution. That gap should
stay explicit until credentials, provider receipts, hardware target metadata,
and billing/runtime evidence are available.

## Tool Findings

- Forum route receipt: `MATCH`.
- Index context envelope: `MATCH`.
- Telos status receipt: `MATCH`, tool version `0.1.0`.
- Gather packet receipt: SHA256
  `c3b0b7e0c210a87763e3b40baf886918f797a16ce306c6b7db6c8a7d16dc03d0`,
  digest seal `afc59f35888f4408eadb340344972802c394790448c53d543c6b43e1f58a2683`.
- Gather brief receipt: SHA256
  `e7bd4d8aa3254acff995fd0af8947712734a6fe6e57d56f31d06b7c0fa5a103e`,
  digest seal `69ca12890509ede92b44d90b32de7f3576bad1f2e7a58d1c42d02500e001b4f0`.
- Crucible result: 9 claims, 9 MATCH, 0 DRIFT, 0 UNVERIFIABLE.
- Crucible thesis id: `47a02c9e50476cf6`.
- Crucible assessment seal:
  `06c4034fe9266336240c5e525e62b9f65d917ef6f9bab79eaf461f58e07fd3d9`.
- Crucible registry stats after this pass: 89 theses, 740 claims, 740 MATCH,
  0 DRIFT, 0 UNVERIFIABLE.

## Boundaries

This pass does not prove QPU execution, quantum advantage, production solver
coverage, provider integration, market adoption, or a natural law. The branch is
local CPU exact BQM execution.

## Verification

```powershell
python -m py_compile docs\research\dogfood\tools\compose_ocean_dimod_bqm_branch_receipt.py docs\research\dogfood\tools\test_ocean_dimod_bqm_branch_receipt.py docs\research\dogfood\tools\validate_pass_0100_ocean_dimod_bqm_branch.py docs\research\dogfood\tools\probe_ocean_dimod_bqm_branch_receipt.py
python docs\research\dogfood\tools\probe_ocean_dimod_bqm_branch_receipt.py
python docs\research\dogfood\tools\test_ocean_dimod_bqm_branch_receipt.py
python docs\research\dogfood\tools\validate_pass_0100_ocean_dimod_bqm_branch.py
crucible run docs\research\dogfood\crucible\pass-0100-thesis.json --measurements docs\research\dogfood\crucible\pass-0100-measurements.json --registry docs\research\dogfood\crucible\registry --report docs\research\dogfood\crucible\pass-0100-report.md --out docs\research\dogfood\crucible\pass-0100-run.json --json
gather docs docs\research\dogfood\packets\110-ocean-dimod-bqm-branch-receipt.md --json
gather docs docs\research\dogfood\briefs\110-ocean-dimod-bqm-branch-brief.md --json
crucible registry stats docs\research\dogfood\crucible\registry --json
```

## Next Pass

Create a provider-backed quantum/hybrid execution boundary schema or pivot the
optimization proof workbench into a larger fixture that stresses branch scaling
without overstating hardware access.
