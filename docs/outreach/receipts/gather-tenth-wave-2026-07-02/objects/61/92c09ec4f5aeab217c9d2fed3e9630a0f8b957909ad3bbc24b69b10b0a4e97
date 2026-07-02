# Packet 108: SolverBranchReceipt Interop Schema

Date: 2026-07-01

Status: `SOLVER_BRANCH_RECEIPT_INTEROP_SCHEMA_MATCH`

Purpose: extract a shared `SolverBranchReceipt/v1` shape from the BuildLang
workbench and Python workflow so exact, heuristic, graph, external, and
quantum/simulator branches can be compared without hiding dependency gaps.

```text
branch_count = 8
executed_count = 6
dependency_boundary_count = 2
best_value = 162
max_observed_gap = 16
compose_status = MATCH
test_status = MATCH
```

## Branch Receipts

| Branch | Runtime | Execution | Value | Gap | Claim Status |
| --- | --- | --- | ---: | ---: | --- |
| python_exact_enumeration | python | EXECUTED | 162 | 0 | LOCAL_RECEIPT_MATCH |
| scipy_dual_annealing | python/scipy | EXECUTED | 162 | 0 | LOCAL_RECEIPT_MATCH |
| networkx_capacity_dag_longest_path | python/networkx | EXECUTED | 162 | 0 | LOCAL_RECEIPT_MATCH |
| ortools_knapsack | python/ortools | NOT_EXECUTED_DEPENDENCY_MISSING | n/a | n/a | DEPENDENCY_BOUNDARY |
| dwave_ocean_sampler | python/dwave-ocean | NOT_EXECUTED_DEPENDENCY_MISSING | n/a | n/a | DEPENDENCY_BOUNDARY |
| buildlang_exact_enumeration | buildlang/buildc | EXECUTED | 162 | 0 | LOCAL_RECEIPT_MATCH |
| buildlang_greedy_ratio_order | buildlang/buildc | EXECUTED | 146 | 16 | LOCAL_RECEIPT_MATCH |
| buildlang_bounded_prefix_2048 | buildlang/buildc | EXECUTED | 157 | 5 | LOCAL_RECEIPT_MATCH |

## Source Anchors

| Source | URL | Bound Claim |
| --- | --- | --- |
| SciPy dual_annealing | https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.dual_annealing.html | Find the global minimum of a function using Dual Annealing. |
| NetworkX dag_longest_path | https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.dag.dag_longest_path.html | Returns the longest path in a directed acyclic graph. |
| OR-Tools knapsack | https://developers.google.com/optimization/pack/knapsack | Choose a subset of maximum total value that fits capacity. |
| D-Wave Ocean samplers | https://docs.dwavequantum.com/en/latest/ocean/api_ref_samplers/index.html | Ocean provides quantum, classical, and hybrid samplers. |

Boundary: this pass defines an interop schema and binds official source
anchors. It does not prove external dependency execution, solver superiority,
quantum advantage, market adoption, or a natural law.
