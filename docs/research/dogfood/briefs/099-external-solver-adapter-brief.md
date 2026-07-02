# External Solver Adapter Brief

Date: 2026-07-01

## Result

Pass 0089 imports SciPy `dual_annealing` into the proof-packet path. The local
adapter runs 16 seeded attempts and records an exact-value
gap of 0 against pass 0088.

## Product Meaning

The system can now distinguish an installed solver adapter from an unavailable
solver target. OR-Tools is recorded as unavailable locally instead of silently
excluded.

## Next Adapter

Add OR-Tools when installed, or create a no-ground-truth large-instance lane
that requires independent replay and solver-version receipts.
