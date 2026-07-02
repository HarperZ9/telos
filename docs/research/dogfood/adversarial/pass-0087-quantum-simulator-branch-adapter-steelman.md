# Pass 0087 Steelman: Quantum Simulator Branch Adapter

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

The strongest objection is that a hand-rolled simulated annealer is not a
market-grade D-Wave/Ocean adapter. Correct. This pass is a receipt contract and
seeded replay gate, not a production sampler wrapper.

The second objection is that the toy problem is small enough for exact
enumeration. Correct again. That is the reason the adapter can be held to a
hard replay gate before larger, noisier, or external solver branches are added.

Non-promotion statement: Pass 0087 verifies a seeded simulated-annealing branch against an exact toy baseline; it does not claim hardware execution, quantum advantage, new physics, or a natural law.
