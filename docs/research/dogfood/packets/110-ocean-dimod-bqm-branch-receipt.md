# Packet 110: Ocean/dimod BQM Branch Receipt

Date: 2026-07-01

Status: `OCEAN_DIMOD_BQM_BRANCH_RECEIPT_MATCH`

Purpose: upgrade the remaining D-Wave/Ocean lane from a dependency boundary
into an executed local-CPU Ocean-compatible BQM branch using `dimod.ExactSolver`.

```text
global_dimod_available = False
global_dwave_available = False
temp_venv_cleaned = True
dimod_version = 0.12.22
branch_id = ocean_dimod_exact_bqm
value = 162
weight = 29
mask = 2347
gap_to_exact = 0
bqm_linear_terms = 12
bqm_quadratic_terms = 66
compose_status = MATCH
test_status = MATCH
```

Boundary: this is local CPU exact BQM execution, not QPU execution, quantum
advantage, production solver coverage, or a natural law.
