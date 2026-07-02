# Packet 107: BuildLang Optimization Proof Workbench

Date: 2026-07-01

Status: `BUILDLANG_OPTIMIZATION_PROOF_WORKBENCH_MATCH`

Purpose: execute the pass 0096 primary push by running exact, greedy, and
bounded-search optimization branches directly in BuildLang and binding the run
to `buildc check --receipt`, `buildc receipt verify`, Forum, Index, Telos, and
Crucible.

```text
source = C:\dev\public\telos\docs\research\dogfood\fixtures\buildlang-knapsack-branch-comparison-pass-0097.bld
exact_value = 162
exact_weight = 29
exact_mask = 2347
greedy_value = 146
bounded_value = 157
greedy_gap = 16
bounded_gap = 5
verify_checks = 18
compose_status = MATCH
test_status = MATCH
```

## Branches

| Branch | Value | Weight | Mask | Gap | Method |
| --- | ---: | ---: | ---: | ---: | --- |
| exact_enumeration | 162 | 29 | 2347 | 0 | full 4096-mask enumeration |
| greedy_ratio_order | 146 | 25 | 2331 | 16 | fixed value/weight ratio order |
| bounded_prefix_2048 | 157 | 27 | 299 | 5 | enumerates masks below 2048 |

Boundary: this is one BuildLang fixture. It proves receipt-backed branch
comparison, not production optimization, language replacement, quantum
advantage, or a natural law.
