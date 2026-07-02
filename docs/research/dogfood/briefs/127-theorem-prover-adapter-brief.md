# Theorem-Prover Adapter Brief

Date: 2026-07-01

## Decision

Create an adapter receipt for theorem-prover targets before claiming prover
execution. The pass records Lean-style target strings, finite-model witnesses,
countermodel fields, local tool availability, and explicit unavailable fences.

## Wedge

The market gap is not theorem proving itself. The wedge is durable proof
packet plumbing: source, target prover, local availability, proof-object status,
countermodel slot, replay witness, and action receipt in one portable record.

Source anchors recorded: 7.
