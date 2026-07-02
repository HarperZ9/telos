# Packet 109: OR-Tools Branch Execution Receipt

Date: 2026-07-01

Status: `ORTOOLS_BRANCH_EXECUTION_RECEIPT_MATCH`

Purpose: upgrade the pass 0098 OR-Tools dependency boundary into an executed
`SolverBranchReceipt/v1` branch using an isolated temporary virtual
environment.

```text
global_ortools_available = False
temp_venv_cleaned = True
ortools_version = 9.15.6755
branch_id = ortools_knapsack_dynamic_programming
value = 162
weight = 29
mask = 2347
gap_to_exact = 0
compose_status = MATCH
test_status = MATCH
```

## Result

OR-Tools solved the 12-item knapsack fixture with value 162, weight 29, and
mask 2347. That matches the exact baseline and BuildLang exact branch.

## Source Anchors

- https://developers.google.com/optimization/install
- https://developers.google.com/optimization/pack/knapsack
- https://pypi.org/project/ortools/

Boundary: this proves one isolated OR-Tools execution branch. It does not prove
solver superiority, production coverage, quantum advantage, or a natural law.
