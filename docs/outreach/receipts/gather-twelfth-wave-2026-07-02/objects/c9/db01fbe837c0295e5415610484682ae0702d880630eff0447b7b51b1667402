# Pass 0090 Ledger: Solver Availability Matrix Receipt

Date: 2026-07-01

Status: `MATCH_SOLVER_AVAILABILITY_MATRIX_RECEIPT`

## Purpose

Build a factual solver/runtime availability map before expanding into larger
scientific, optimization, quantum, and BuildLang proof work. This pass records
which solver surfaces are locally installed, which are missing, which local
Build ecosystem sources exist, and which adapter lane should come next.

## Artifacts

| Artifact | Purpose |
| --- | --- |
| `tools/compose_solver_availability_matrix_receipt.py` | Package, CLI, repo, BuildLang corpus, Forum, Index, and Telos composer. |
| `tools/test_solver_availability_matrix_receipt.py` | Focused availability, count-invariant, BuildLang, and boundary test. |
| `tools/probe_solver_availability_matrix_receipt.py` | Packet, brief, steelman, thesis, measurement, and compact receipt generator. |
| `tools/validate_pass_0090_solver_availability_matrix_receipt.py` | Independent validator for seal, row counts, package state, BuildLang, and boundaries. |
| `schemas/solver-availability-matrix-receipt-pass-0090.json` | `SolverAvailabilityMatrixReceipt/v1` artifact. |
| `schemas/pass-0090-solver-availability-matrix-receipt-validator-result.json` | Validator receipt. |
| `schemas/tool-receipts-pass-0090.json` | Compact BuildLang, matrix, Forum, Index, Telos, compose, and test receipts. |
| `packets/100-solver-availability-matrix-receipt.md` | Human-readable solver availability matrix. |
| `briefs/100-solver-availability-matrix-brief.md` | Concise product-strategy brief. |
| `adversarial/pass-0090-solver-availability-matrix-steelman.md` | Local steelman of the matrix limits. |
| `crucible/pass-0090-thesis.json` | Falsifiable claims. |
| `crucible/pass-0090-measurements.json` | Measurements/evidence. |
| `crucible/pass-0090-report.md` | Crucible report. |
| `crucible/pass-0090-run.json` | Crucible run record. |

## Measurements

| Check | Result |
| --- | --- |
| Prior adapter pass | 0089 |
| Upstream video cluster | `enterprise_quantum_optimization` |
| Matrix row count | 28 |
| Local available/source-present rows | 11 |
| Local unavailable/missing rows | 17 |
| Count invariant | 11 + 17 = 28 |
| NumPy | available, version 2.4.5 |
| SciPy | available, version 1.17.1 |
| NetworkX | available, version 3.6.1 |
| pandas | available, version 3.0.3 |
| OR-Tools | unavailable |
| D-Wave Ocean / `dwave.system` | unavailable |
| Qiskit | unavailable |
| SymPy | unavailable |
| Z3 | unavailable |
| Torch/JAX | unavailable |
| BuildLang source | present at `C:\dev\public\pubscan\quantalang` |
| `buildc` on PATH | unavailable |
| `buildc corpus verify` | MATCH, exit code 0 |
| BuildLang corpus stdout SHA256 | `fbe2daff8da1804b00cafe9a9fff36fc649429071b25f6a2561003255f6310d3` |
| Artifact seal | `d32050ec5d7ef77d6eafdc555118938cdac546580fdfaa90c479299507d4ead1` |
| Promoted natural laws | 0 |

## Source Anchors

| Source | URL | Status |
| --- | --- | --- |
| SciPy dual annealing | `https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.dual_annealing.html` | `WEB_VERIFIED_2026_07_01` |
| OR-Tools CP-SAT | `https://developers.google.com/optimization/cp/cp_solver` | `WEB_VERIFIED_2026_07_01` |
| D-Wave Ocean | `https://docs.dwavequantum.com/en/latest/ocean/index.html` | `WEB_VERIFIED_2026_07_01` |
| CVXPY | `https://www.cvxpy.org/` | `WEB_VERIFIED_2026_07_01` |
| Pyomo | `https://www.pyomo.org/` | `WEB_VERIFIED_2026_07_01` |
| Qiskit | `https://quantum.cloud.ibm.com/docs/en/guides` | `WEB_VERIFIED_2026_07_01` |
| SymPy | `https://docs.sympy.org/latest/index.html` | `WEB_VERIFIED_2026_07_01` |
| NetworkX | `https://networkx.org/documentation/stable/` | `WEB_VERIFIED_2026_07_01` |
| Pass 0089 external adapter | `docs/research/dogfood/pass-0089-ledger.md` | `LOCAL_BASELINE` |
| BuildLang local README | `C:\dev\public\pubscan\quantalang\README.md` | `LOCAL_SOURCE` |
| Build Universe local STATUS | `C:\dev\public\build-universe\STATUS.md` | `LOCAL_SOURCE` |

## Product Finding

The next proof lane should use what is already executable. BuildLang/buildc has
a live corpus verifier and source-present ecosystem, while NetworkX is locally
installed and can support graph optimization receipts without adding external
dependencies. OR-Tools, D-Wave Ocean, SymPy, Z3, Qiskit, Torch, JAX, CVXPY, and
Pyomo should be handled as dependency or remote-adapter receipts before any
claim implies local coverage.

Recommended next adapters:

1. `buildlang_corpus_receipt_adapter`
2. `networkx_graph_optimization_adapter`
3. `ortools_cp_sat_dependency_receipt`
4. `sympy_symbolic_math_dependency_receipt`

## Tool Findings

- Forum route receipt: `MATCH`, `needs_escalation=true`.
- Index context envelope: `MATCH`, schema `project-telos.context-envelope/v1`,
  graph pack SHA256
  `8ee383e19ae9a6141bee70de733fb6aa09201ff9d284ce6778ce58b06e6b68b2`.
- Telos status receipt: `MATCH`, tool version `0.1.0`.
- Gather packet receipt: SHA256
  `6840e9bd307370ec90639ef9a35cbb7de11bec52611d3047972c77aed6fade84`,
  digest seal `64264883339eead5d0e0a5ad853c5b8ae05f9869cfdee212ae7fd4fd2e7295c1`.
- Gather brief receipt: SHA256
  `e03d124a0ab8343c43d93fb1c4d79ed9094e263311e778d7e2fcf05701101b0a`,
  digest seal `4d3dd77318ee3ec9eb952b74e2c0baef4910bbbb646b2738b203b3f5232d9032`.
- Crucible result: 9 claims, 9 MATCH, 0 DRIFT, 0 UNVERIFIABLE.
- Crucible thesis id: `f5c9fb47421acb93`.
- Crucible assessment seal:
  `e03f6b1ef528a6f12fe3a421910bb73351f0a8dc74a3aec7f4e3be99f50104a4`.
- Crucible registry stats after this pass: 79 theses, 648 claims, 648 MATCH,
  0 DRIFT, 0 UNVERIFIABLE.

## Boundaries

This pass is an availability and adapter-priority receipt. It does not claim
solver superiority, local coverage for missing dependencies, a world-scale
problem solution, a BuildLang replacement result, or a natural law.

## Verification

```powershell
python -m py_compile docs\research\dogfood\tools\compose_solver_availability_matrix_receipt.py docs\research\dogfood\tools\test_solver_availability_matrix_receipt.py docs\research\dogfood\tools\validate_pass_0090_solver_availability_matrix_receipt.py docs\research\dogfood\tools\probe_solver_availability_matrix_receipt.py
python docs\research\dogfood\tools\probe_solver_availability_matrix_receipt.py
python docs\research\dogfood\tools\test_solver_availability_matrix_receipt.py
python docs\research\dogfood\tools\validate_pass_0090_solver_availability_matrix_receipt.py
crucible run docs\research\dogfood\crucible\pass-0090-thesis.json --measurements docs\research\dogfood\crucible\pass-0090-measurements.json --registry docs\research\dogfood\crucible\registry --report docs\research\dogfood\crucible\pass-0090-report.md --out docs\research\dogfood\crucible\pass-0090-run.json --json
gather docs docs\research\dogfood\packets\100-solver-availability-matrix-receipt.md --json
gather docs docs\research\dogfood\briefs\100-solver-availability-matrix-brief.md --json
crucible registry stats docs\research\dogfood\crucible\registry --json
```

## Next Pass

Build a NetworkX graph-optimization receipt or a BuildLang corpus-to-Crucible
adapter. The NetworkX path is fastest for another mathematical proof packet; the
BuildLang path is more strategically aligned with the compiler/runtime substrate.
