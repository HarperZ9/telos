# Packet 099: External Solver Adapter Receipt

Date: 2026-07-01

Status: `EXTERNAL_SOLVER_ADAPTER_RECEIPT_MATCH`

Purpose: admit a real local solver surface into the pass 0088 branch-comparison
contract without promoting solver superiority.

```text
adapter = scipy.optimize.dual_annealing
scipy_version = 1.17.1
ortools_available = False
run_count = 16
seed_range = [8900, 8915]
maxiter = 128
best_value = 162
best_weight = 29
exact_value_gap = 0
exact_hit_count = 10
value_distribution = [158, 162]
compose_status = MATCH
test_status = MATCH
```

## Dependencies

| Dependency | Available | Version |
| --- | --- | --- |
| python | runtime | 3.12.10 |
| numpy | True | 2.4.5 |
| scipy | True | 1.17.1 |
| ortools | False | None |

## Source Anchors

- scipy-dual-annealing: https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.dual_annealing.html
- or-tools-mip: https://developers.google.com/optimization/mip/mip_example
- pass-0088-branch-comparison: docs/research/dogfood/pass-0088-ledger.md

Boundary: this is an adapter receipt for a bounded benchmark. It does not prove
solver superiority, quantum advantage, hardware execution, new physics, or a
natural law.
