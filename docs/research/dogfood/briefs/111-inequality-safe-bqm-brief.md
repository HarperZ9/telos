# Inequality-Safe BQM Brief

Date: 2026-07-01

## Result

Pass 0101 found a real encoding hazard: equality-to-capacity BQM penalties can
select infeasible overweight knapsack states. A slack-variable encoding fixes
the bounded counterexample.

## Product Meaning

The optimization workbench now needs an encoding-safety layer before any BQM,
quantum, or hybrid branch is allowed to claim a valid inequality-constrained
result.
