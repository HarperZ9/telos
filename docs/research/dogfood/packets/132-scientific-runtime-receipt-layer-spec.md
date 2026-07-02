# Packet 132: Scientific Runtime Receipt Layer Spec

Date: 2026-07-01

Status: `SCIENTIFIC_RUNTIME_RECEIPT_LAYER_MATCH`

Purpose: turn the pass 0121 `scientific_runtime_receipt_layer` push into a
concrete source-backed receipt contract and a long-horizon Hamiltonian runtime
experiment.

```text
source_rows = 17
gather_verified_sources = 15
receipt_contract_fields = 8
compose_status = MATCH
test_status = MATCH
validator_status = MATCH
```

## Source Matrix

| Category | Tool | Gather status | Gap status |
| --- | --- | --- | --- |
| compiler_ir | OpenXLA XLA | GATHER_VERIFIED | inferred |
| compiler_ir | StableHLO | GATHER_VERIFIED | inferred |
| compiler_ir | MLIR | GATHER_VERIFIED | inferred |
| array_runtime | JAX | GATHER_VERIFIED_SHORT_TEXT | inferred |
| scientific_runtime | SciML SymplecticRK | GATHER_VERIFIED | inferred |
| array_runtime | NumPy det | GATHER_VERIFIED | inferred |
| array_runtime | SciPy det | GATHER_VERIFIED | inferred |
| gpu_kernel | Triton | GATHER_VERIFIED | inferred |
| ai_runtime | Modular MAX | GATHER_VERIFIED | inferred |
| formal_prover | Lean | GATHER_VERIFIED | inferred |
| formal_prover | Rocq | OFFICIAL_ANCHOR_UNVERIFIED_LOCALLY | inferred |
| formal_prover | Isabelle | OFFICIAL_ANCHOR_UNVERIFIED_LOCALLY | inferred |
| formal_prover | Agda | GATHER_VERIFIED | inferred |
| observability | OpenTelemetry | GATHER_VERIFIED | inferred |
| experiment_tracking | MLflow Tracking | GATHER_VERIFIED | inferred |
| experiment_tracking | Weights and Biases | GATHER_VERIFIED | inferred |
| lineage | OpenLineage | GATHER_VERIFIED | inferred |

## Receipt Contract

| Field | Required |
| --- | --- |
| source_receipts | required |
| oracle | required |
| runtime_branch | required |
| compiler_branch | required |
| telemetry_branch | required |
| lineage_branch | required |
| verifier_verdict | required |
| non_promotion_boundary | required |

## Hamiltonian Long-Horizon Experiment

| h | Exact invariant all steps | Max float drift | Status |
| --- | --- | ---: | --- |
| 1/3 | True | 1.4854784069484595e-12 | MATCH |
| 1/2 | True | 2.275957200481571e-14 | MATCH |
| 2/3 | True | 5.486722187697524e-13 | MATCH |

## Boundary

Pass 0122 strengthens a scoped Hamiltonian law candidate and defines a receipt layer. It does not prove BuildLang/buildc execution, solve arbitrary physics, verify all external tool claims, or promote a natural law.
