# Packet 097: Quantum Simulator Branch Adapter

Date: 2026-07-01

Status: `QUANTUM_SIMULATOR_BRANCH_ADAPTER_MATCH`

Purpose: add a seeded simulated-annealing branch to the exact pass 0086
optimization receipt, while preserving the exact baseline as the replay gate.

```text
baseline_pass = 0086
run_count = 32
seed_range = 8700..8731
optimum_hit_count = 30
constraint_violation_rate = 0.0
best_bits = [0, 0, 1, 1, 1, 1]
best_energy = -36
comparison_status = MATCH
compose_status = MATCH
test_status = MATCH
```

## Source Anchors

- dwave-samplers-simulated-annealing: https://docs.dwavequantum.com/en/latest/ocean/api_ref_samplers/index.html
- dwave-dimod-bqm-models: https://docs.dwavequantum.com/en/latest/ocean/api_ref_dimod/models.html

## Distribution

- Objective values: `[34, 34, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36]`.
- Run digest: `4df12bbe1c5b3ee42d05f5ccce708bd5880f4d1d4c1c5a90f3f9528656d912b7`.
- Exact baseline energy: `-36`.
- Simulator best energy: `-36`.

Boundary: this pass verifies a simulator branch against a toy exact baseline.
It does not claim quantum hardware execution, quantum advantage, new physics,
or a natural law.
