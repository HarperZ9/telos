# Quantum Simulator Branch Adapter Brief

Date: 2026-07-01

## Result

Pass 0087 adds a seeded simulated-annealing branch to the pass 0086 exact
baseline. Across 32 runs, the branch hit the exact optimum
30 times and records every seed and run output.

## Product Meaning

This is the adapter contract future quantum/simulator integrations need:
source anchors, solver parameters, seed records, run digest, distribution
summary, exact-baseline comparison, and non-promotion gates.

## Next Adapter

Add a larger synthetic optimization instance where exact enumeration is still
possible but nontrivial, then compare exact, simulated annealing, and greedy
baselines through the same receipt shape.
