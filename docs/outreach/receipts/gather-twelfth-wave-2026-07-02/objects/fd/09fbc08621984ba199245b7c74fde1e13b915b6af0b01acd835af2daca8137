# Packet 130: Hamiltonian Runtime Branch Receipt

Date: 2026-07-01

Status: `HAMILTONIAN_RUNTIME_BRANCH_MATCH`

Purpose: replay pass 0119's exact Hamiltonian/symplectic oracle through
available local runtime branches and fence unavailable branches.

```text
hamiltonian_symplectic_pass = 0119
runtime_branches = 10
compose_status = MATCH
test_status = MATCH
validator_status = MATCH
```

## Runtime Branches

| Branch | Runtime | Status |
| --- | --- | --- |
| numpy_float64_h_1/3 | numpy | MATCH |
| numpy_float64_h_1/2 | numpy | MATCH |
| numpy_float64_h_2/3 | numpy | MATCH |
| numpy_explicit_euler_negative | numpy | MATCH |
| scipy_linalg_det_h_1/3 | scipy.linalg.det | MATCH |
| scipy_linalg_det_h_1/2 | scipy.linalg.det | MATCH |
| scipy_linalg_det_h_2/3 | scipy.linalg.det | MATCH |
| jax_runtime_branch | jax | UNAVAILABLE_FENCED |
| buildlang_runtime_branch | buildc | UNAVAILABLE_FENCED |
| julia_sciml_branch | julia | UNAVAILABLE_FENCED |

## Availability

| Runtime | Status |
| --- | --- |
| build | MISSING |
| buildc | MISSING |
| jax | MISSING |
| julia | MISSING |
| numpy | AVAILABLE |
| python | AVAILABLE |
| scipy | AVAILABLE |

## Boundary

Pass 0120 measures runtime replay drift against pass 0119's exact oracle. It does not prove BuildLang, JAX, GPU, or Julia execution when those branches are unavailable.
