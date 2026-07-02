# Pass 0120 Ledger: Hamiltonian Runtime Branch Receipt

Date: 2026-07-01

## Objective

Bridge pass 0119's exact Hamiltonian/symplectic oracle into available local
runtime branches, then record explicit fences for runtime branches that are
not available in this workstation session.

This pass is a runtime replay and receipt-packaging pass. It does not claim
BuildLang/buildc, JAX, GPU, or Julia execution.

## Result

| Field | Value |
| --- | --- |
| Artifact schema | `HamiltonianRuntimeBranchReceipt/v1` |
| Artifact | `schemas/hamiltonian-runtime-branch-receipt-pass-0120.json` |
| Status | `HAMILTONIAN_RUNTIME_BRANCH_MATCH` |
| Artifact sha256 | `f16b1a61e135ecacfd4a31b6e70690918d95f8a5daff29f5a99c416bcaf1c759` |
| Artifact seal | `9100835b059bd5d8d5d21f3e899bfd78c36d68f27d76bdc09b0cfb561d9fe0e5` |
| Source binding | pass 0119 Hamiltonian symplectic receipt |
| Source binding seal | `8fb6fe8a7b9155318c4e4512c9ef3c916e816365186d3566ea6bbf5c317ca05c` |
| Runtime branch count | 10 |
| Unsupported claim count | 0 |
| Current promoted natural laws | none |

## Runtime Branches

| Branch | Runtime | Status | Note |
| --- | --- | --- | --- |
| `numpy_float64_h_1/3` | NumPy | `MATCH` | Positive replay against exact oracle. |
| `numpy_float64_h_1/2` | NumPy | `MATCH` | Positive replay against exact oracle. |
| `numpy_float64_h_2/3` | NumPy | `MATCH` | Positive replay against exact oracle. |
| `numpy_explicit_euler_negative` | NumPy | `MATCH` | Negative fixture: determinant above 1 and energy growth. |
| `scipy_linalg_det_h_1/3` | SciPy `linalg.det` | `MATCH` | Determinant replay. |
| `scipy_linalg_det_h_1/2` | SciPy `linalg.det` | `MATCH` | Determinant replay. |
| `scipy_linalg_det_h_2/3` | SciPy `linalg.det` | `MATCH` | Determinant replay. |
| `jax_runtime_branch` | JAX | `UNAVAILABLE_FENCED` | JAX was not available locally. |
| `buildlang_runtime_branch` | BuildLang/buildc | `UNAVAILABLE_FENCED` | `build` and `buildc` were not available locally. |
| `julia_sciml_branch` | Julia/SciML | `UNAVAILABLE_FENCED` | Julia was not available locally. |

## Availability Snapshot

| Runtime | Status |
| --- | --- |
| Python | `AVAILABLE` |
| NumPy | `AVAILABLE` |
| SciPy | `AVAILABLE` |
| JAX | `MISSING` |
| BuildLang `build` | `MISSING` |
| BuildLang `buildc` | `MISSING` |
| Julia | `MISSING` |

## Source Surface

The artifact records four source-surface anchors. Each market or proof-layer
gap is marked `inferred`, not verified as exclusive.

| Tool | URL | Gap status |
| --- | --- | --- |
| NumPy linalg | https://numpy.org/doc/stable/reference/generated/numpy.linalg.det.html | `inferred` |
| SciPy `linalg.det` | https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.det.html | `inferred` |
| JAX Quickstart | https://docs.jax.dev/en/latest/quickstart.html | `inferred` |
| Python `decimal` | https://docs.python.org/3/library/decimal.html | `inferred` |

## Flagship Receipts

| Tool | Status | Notes |
| --- | --- | --- |
| Forum | `MATCH` | Routed to `model-foundry` with low confidence and escalation flag. |
| Index | `MATCH` | Context envelope verified. |
| Telos | `MATCH` | Status receipt recorded. |
| Telos catalog | `MATCH` | Catalog summary detected. |
| Gather packet | `MATCH` | Packet hash `fd09fbc08621984ba199245b7c74fde1e13b915b6af0b01acd835af2daca8137`; seal `e0d891d4d100f3ef351b8067396786b9e4d1a4cca07fa3dec623679448eef533`. |
| Gather brief | `MATCH` | Brief hash `f702c0aa7dedbe394a1bb75f058ce68ee1952f1fb2f925c2b80513c3f82442c3`; seal `03b897cb5650f92ed445f6b5d20d3f2a251b44b29899c982308724a200b8ab6d`. |

## Crucible

| Field | Value |
| --- | --- |
| Thesis id | `6223fe036e9baeb3` |
| Thesis seal | `6223fe036e9baeb3d3cf6fa02b9d8d4012bdee27ab8640f14ca39fd2d47eac5b` |
| Assessment seal | `37b10b109b413fa356a543497cfd4ac8377e75083a2753f576b4383f3f3eb586` |
| Counts | `MATCH 12 / DRIFT 0 / UNVERIFIABLE 0` |
| Registry after pass | 111 theses, 982 claims, 948 unique claims, 114 assessments, 111 latest assessments, 0 invalid latest assessments |

## File Hashes

| File | SHA-256 |
| --- | --- |
| `tools/compose_hamiltonian_runtime_branch_receipt.py` | `eb981b2e7380423e9bfc12f873922da332663fe8ce16297307cda222dc6f5025` |
| `tools/test_hamiltonian_runtime_branch_receipt.py` | `75c61c3770a6b6bcb99ff5485ab47a06686a0d3ad7b0074361115649aae6731b` |
| `tools/validate_pass_0120_hamiltonian_runtime_branch.py` | `2a3f0333ff29e682011600c7b4f5fff2474074c35d5981ca9d9d01e96a3d6ba6` |
| `tools/probe_hamiltonian_runtime_branch_receipt.py` | `7e9fff08803ba071940c3f2ca33ca42cb0a5037e07b22fc1b6a9c7d019718a7f` |
| `schemas/hamiltonian-runtime-branch-receipt-pass-0120.json` | `f16b1a61e135ecacfd4a31b6e70690918d95f8a5daff29f5a99c416bcaf1c759` |
| `schemas/pass-0120-hamiltonian-runtime-branch-validator-result.json` | `7047ad1055b8eed1526225ffec40de400661dabfcef837a26ff7693a633f2dd8` |
| `schemas/tool-receipts-pass-0120.json` | `00533ae287da71c27b706a1303aff6ffcd0fe810601996a535cda6f09c752969` |
| `packets/130-hamiltonian-runtime-branch-receipt.md` | `fd09fbc08621984ba199245b7c74fde1e13b915b6af0b01acd835af2daca8137` |
| `briefs/130-hamiltonian-runtime-branch-brief.md` | `f702c0aa7dedbe394a1bb75f058ce68ee1952f1fb2f925c2b80513c3f82442c3` |
| `adversarial/pass-0120-hamiltonian-runtime-branch-steelman.md` | `75ca700ff9af0c7a53c7523f66f02987fea455dc51b57272d1f2c53d964ef8c5` |
| `crucible/pass-0120-thesis.json` | `3617aa533b6ddc87a00a2441eb2f39de805130d0ed440a3fa4d136ca59aab7f2` |
| `crucible/pass-0120-measurements.json` | `b9a78d66e0b4b7ac717698ce2f62a3eca869eb7cd2c837fcddfbf8b3a1918f69` |
| `crucible/pass-0120-report.md` | `5f4d40d34a0ac6fccb7fe519714c965606cf29c62c33c3d5429c8f387506757e` |
| `crucible/pass-0120-run.json` | `376ee338c42f31072674c99c4cb5fc92d6fbbd886677590cd2ea9297ae9bb72c` |

## Verification Commands

```powershell
python -m py_compile docs\research\dogfood\tools\compose_hamiltonian_runtime_branch_receipt.py docs\research\dogfood\tools\test_hamiltonian_runtime_branch_receipt.py docs\research\dogfood\tools\validate_pass_0120_hamiltonian_runtime_branch.py docs\research\dogfood\tools\probe_hamiltonian_runtime_branch_receipt.py
python docs\research\dogfood\tools\test_hamiltonian_runtime_branch_receipt.py
python docs\research\dogfood\tools\validate_pass_0120_hamiltonian_runtime_branch.py
node demo\catalog.mjs --summary
gather docs docs\research\dogfood\packets\130-hamiltonian-runtime-branch-receipt.md --json
gather docs docs\research\dogfood\briefs\130-hamiltonian-runtime-branch-brief.md --json
crucible run docs\research\dogfood\crucible\pass-0120-thesis.json --measurements docs\research\dogfood\crucible\pass-0120-measurements.json --registry docs\research\dogfood\crucible\registry --report docs\research\dogfood\crucible\pass-0120-report.md --out docs\research\dogfood\crucible\pass-0120-run.json --json
crucible registry stats docs\research\dogfood\crucible\registry --json
```

## Next Pass Queue

1. Extend the runtime replay to longer horizons and interval or decimal
   arithmetic so numerical drift has a stronger tolerance story.
2. Add a BuildLang/buildc execution branch when `build` or `buildc` is
   available locally, with explicit compile hash, target hash, runtime hash,
   and result receipt.
3. Add JAX and Julia/SciML adapters when the runtimes are installed, without
   promoting the proof unless their branch receipts match.
4. Bind the new YouTube source leads to the next domain-growth pass as
   source leads, then extract only claims that can be transcript-backed or
   manually cited.
