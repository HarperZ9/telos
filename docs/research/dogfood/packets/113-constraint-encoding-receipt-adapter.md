# Packet 113: Constraint-Encoding Receipt Adapter

Date: 2026-07-01

Status: `CONSTRAINT_ENCODING_RECEIPT_ADAPTER_MATCH`

Purpose: apply pass 0101's BQM counterexample to the solver branch stack. The
adapter records whether each branch has a visible constraint encoding and
feasibility check, and blocks promotion when an executed BQM branch relies on
equality-to-capacity penalty without a slack or inequality receipt.

```text
receipt_count = 10
executed_receipt_count = 8
safe_executed_count = 7
promotion_blocked_executed_count = 1
unsafe_executed_branch_ids = ocean_dimod_exact_bqm
compose_status = MATCH
test_status = MATCH
```

## Encoding Receipts

| Branch | Execution | Encoding | Feasible | Promotion Blocked | Adapter Status |
| --- | --- | --- | --- | --- | --- |
| `python_exact_enumeration` | EXECUTED | explicit_feasibility_filter | True | False | MATCH |
| `scipy_dual_annealing` | EXECUTED | explicit_feasibility_filter | True | False | MATCH |
| `networkx_capacity_dag_longest_path` | EXECUTED | capacity_state_graph | True | False | MATCH |
| `ortools_knapsack` | NOT_EXECUTED_DEPENDENCY_MISSING | solver_native_knapsack_capacity | None | False | BOUNDARY_ONLY |
| `dwave_ocean_sampler` | NOT_EXECUTED_DEPENDENCY_MISSING | provider_boundary_unknown | None | True | BOUNDARY_ONLY |
| `buildlang_exact_enumeration` | EXECUTED | explicit_feasibility_filter | True | False | MATCH |
| `buildlang_greedy_ratio_order` | EXECUTED | explicit_feasibility_filter | True | False | MATCH |
| `buildlang_bounded_prefix_2048` | EXECUTED | explicit_feasibility_filter | True | False | MATCH |
| `ortools_knapsack_dynamic_programming` | EXECUTED_ISOLATED_TEMP_VENV | solver_native_knapsack_capacity | True | False | MATCH |
| `ocean_dimod_exact_bqm` | EXECUTED_LOCAL_CPU_EXACT_SOLVER | bqm_equality_penalty_to_capacity | True | True | MATCH_WITH_PROMOTION_BLOCK |

## Rule

An optimization branch can match the fixture and still be unsafe as a general
encoding. Pass 0103 therefore separates `feasible_under_capacity` from
`encoding_safety`; both must be visible before a solver branch is promoted.
