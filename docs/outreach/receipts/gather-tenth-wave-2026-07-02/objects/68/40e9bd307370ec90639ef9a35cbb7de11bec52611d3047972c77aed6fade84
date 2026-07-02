# Packet 100: Solver Availability Matrix Receipt

Date: 2026-07-01

Status: `SOLVER_AVAILABILITY_MATRIX_RECEIPT_MATCH`

Purpose: map installed, missing, source-present, and planned solver/runtime
surfaces before choosing the next proof expansion.

```text
row_count = 28
local_available_rows = 11
local_unavailable_rows = 17
buildc_corpus_status = MATCH
scipy_available = True
networkx_available = True
ortools_available = False
dwave_system_available = False
recommended_next = ['buildlang_corpus_receipt_adapter', 'networkx_graph_optimization_adapter', 'ortools_cp_sat_dependency_receipt', 'sympy_symbolic_math_dependency_receipt']
compose_status = MATCH
test_status = MATCH
```

## Matrix Rows

| Row | Category | Local Status | Proof Gap | Next Action |
| --- | --- | --- | --- | --- |
| numpy | array_baseline | LOCAL_AVAILABLE | adapter_needed | build_adapter_receipt |
| scipy | continuous_global_optimization | LOCAL_AVAILABLE | adapter_needed | build_adapter_receipt |
| networkx | graph_algorithms | LOCAL_AVAILABLE | adapter_needed | build_adapter_receipt |
| pandas | table_ingest | LOCAL_AVAILABLE | adapter_needed | build_adapter_receipt |
| sympy | symbolic_math | LOCAL_UNAVAILABLE | dependency_missing | install_or_remote_adapter_receipt |
| cvxpy | convex_optimization | LOCAL_UNAVAILABLE | dependency_missing | install_or_remote_adapter_receipt |
| pyomo | algebraic_modeling | LOCAL_UNAVAILABLE | dependency_missing | install_or_remote_adapter_receipt |
| ortools | cp_sat_mip | LOCAL_UNAVAILABLE | dependency_missing | install_or_remote_adapter_receipt |
| dimod | qubo_bqm_modeling | LOCAL_UNAVAILABLE | dependency_missing | install_or_remote_adapter_receipt |
| dwave_system | quantum_hybrid_samplers | LOCAL_UNAVAILABLE | dependency_missing | install_or_remote_adapter_receipt |
| qiskit | quantum_circuits | LOCAL_UNAVAILABLE | dependency_missing | install_or_remote_adapter_receipt |
| qutip | quantum_dynamics | LOCAL_UNAVAILABLE | dependency_missing | install_or_remote_adapter_receipt |
| z3 | smt_solving | LOCAL_UNAVAILABLE | dependency_missing | install_or_remote_adapter_receipt |
| torch | ml_tensor_training | LOCAL_UNAVAILABLE | dependency_missing | install_or_remote_adapter_receipt |
| jax | accelerated_autodiff | LOCAL_UNAVAILABLE | dependency_missing | install_or_remote_adapter_receipt |
| buildlang_buildc | compiler_runtime_receipts | SOURCE_AVAILABLE_CORPUS_MATCH | adapter_to_solver_matrix_needed | convert_buildc_corpus_receipt_to_solver_runtime_packet |
| build_universe | domain_module_ecosystem | LOCAL_SOURCE_PRESENT | whole_ecosystem_compilation_not_claimed | module_level_availability_matrix |
| build_color | visual_measurement_kernel | LOCAL_SOURCE_PRESENT | connect_color_metrics_to_solver_receipts | measurement_kernel_receipt_join |
| calibrate_pro | instrumentation_measurement | LOCAL_SOURCE_PRESENT | display_instrument_receipts_not_solver_receipts | instrumentation_receipt_join |
| cli_buildc | cli_surface | CLI_UNAVAILABLE | cli_missing | install_or_remote_cli_adapter |
| cli_julia | cli_surface | CLI_UNAVAILABLE | cli_missing | install_or_remote_cli_adapter |
| cli_mojo | cli_surface | CLI_UNAVAILABLE | cli_missing | install_or_remote_cli_adapter |
| cli_dwave | cli_surface | CLI_UNAVAILABLE | cli_missing | install_or_remote_cli_adapter |
| cli_qiskit | cli_surface | CLI_UNAVAILABLE | cli_missing | install_or_remote_cli_adapter |
| cli_z3 | cli_surface | CLI_UNAVAILABLE | cli_missing | install_or_remote_cli_adapter |
| cli_cmake | cli_surface | CLI_AVAILABLE | cli_adapter_needed | record_cli_version_and_adapter |
| cli_cargo | cli_surface | CLI_AVAILABLE | cli_adapter_needed | record_cli_version_and_adapter |
| cli_node | cli_surface | CLI_AVAILABLE | cli_adapter_needed | record_cli_version_and_adapter |

## Source Anchors

- scipy-dual-annealing: https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.dual_annealing.html
- ortools-cp-sat: https://developers.google.com/optimization/cp/cp_solver
- dwave-ocean: https://docs.dwavequantum.com/en/latest/ocean/index.html
- cvxpy: https://www.cvxpy.org/
- pyomo: https://www.pyomo.org/
- qiskit: https://quantum.cloud.ibm.com/docs/en/guides
- sympy: https://docs.sympy.org/latest/index.html
- networkx: https://networkx.org/documentation/stable/
- pass-0089-external-adapter: docs/research/dogfood/pass-0089-ledger.md
- buildlang-local: C:\dev\public\pubscan\quantalang\README.md
- build-universe-local: C:\dev\public\build-universe\STATUS.md

Boundary: this is an availability and adapter-priority packet. It does not
prove solver superiority, solve a world-scale problem, or promote a natural
law.
