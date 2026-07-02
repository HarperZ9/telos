# Packet 098: Optimization Branch Comparison Receipt

Date: 2026-07-01

Status: `OPTIMIZATION_BRANCH_COMPARISON_RECEIPT_MATCH`

Purpose: compare exact, simulated annealing, greedy, and random-search branches
on a larger exact-enumerable optimization benchmark.

```text
upstream_video_cluster = enterprise_quantum_optimization
upstream_video_count = 13
candidate_count = 4096
feasible_count = 1275
exact_value = 162
exact_weight = 29
branch_count = 4
exact_hit_branches = ['seeded_simulated_annealing', 'seeded_random_search']
max_value_gap = 16
compose_status = MATCH
test_status = MATCH
```

## Branch Comparison

| Branch | Value | Weight | Energy | Gap To Exact | Hit Exact Bits |
| --- | ---: | ---: | ---: | ---: | --- |
| exact_enumeration | 162 | 29 | -162 | 0 | true |
| seeded_simulated_annealing | 162 | 29 | -162 | 0 | True |
| value_density_greedy | 146 | 25 | -146 | 16 | False |
| seeded_random_search | 162 | 29 | -162 | 0 | True |

## Source Anchors

- or-tools-knapsack: https://developers.google.com/optimization/pack/knapsack
- or-tools-mip: https://developers.google.com/optimization/mip/mip_example
- scipy-dual-annealing: https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.dual_annealing.html
- dwave-samplers: https://docs.dwavequantum.com/en/latest/ocean/api_ref_samplers/index.html

Boundary: this pass is a bounded benchmark comparison. It does not prove solver
superiority, quantum advantage, hardware execution, new physics, or a natural
law.
