# Pass 0122 Ledger: Scientific Runtime Receipt Layer

Date: 2026-07-01

## Objective

Turn the pass 0121 `scientific_runtime_receipt_layer` push into a concrete
source-backed receipt contract and a long-horizon Hamiltonian runtime
experiment. The pass connects market/tool research to an executable proof lane:
source receipts, exact oracle, runtime branch, compiler branch, telemetry,
lineage, verifier verdict, and non-promotion boundary.

## Result

| Field | Value |
| --- | --- |
| Artifact schema | `ScientificRuntimeReceiptLayerSpec/v1` |
| Artifact | `schemas/scientific-runtime-receipt-layer-spec-pass-0122.json` |
| Status | `SCIENTIFIC_RUNTIME_RECEIPT_LAYER_MATCH` |
| Artifact sha256 | `cf964fa274918811b9010d2e760fadb70bd4c0949d72de501419af0a232e90ba` |
| Artifact seal | `135c16c1f6d840cbb26ae6ba9257b3863844035c90975e9248aa13ffc1899312` |
| Official source rows | 17 |
| Local Gather-verified web receipts | 15 |
| Required receipt fields | 8 |
| Primary push | `scientific_runtime_receipt_layer` |
| Unsupported claim count | 0 |
| Current promoted natural laws | none |

## Source Matrix

All gap claims are `inferred` hypotheses. This matrix does not assert that any
external tool cannot build similar features; it records where the Telos/Build
receipt layer should bind capabilities together.

| Category | Tool | Official anchor | Local Gather status | Gap status |
| --- | --- | --- | --- | --- |
| compiler IR | OpenXLA XLA | https://openxla.org/xla | `GATHER_VERIFIED` | `inferred` |
| compiler IR | StableHLO | https://openxla.org/stablehlo | `GATHER_VERIFIED` | `inferred` |
| compiler IR | MLIR | https://mlir.llvm.org/ | `GATHER_VERIFIED` | `inferred` |
| array runtime | JAX | https://docs.jax.dev/en/latest/quickstart.html | `GATHER_VERIFIED_SHORT_TEXT` | `inferred` |
| scientific runtime | SciML SymplecticRK | https://docs.sciml.ai/DiffEqDocs/latest/api/ordinarydiffeq/dynamicalodeexplicit/SymplecticRK/ | `GATHER_VERIFIED` | `inferred` |
| array runtime | NumPy determinant | https://numpy.org/doc/stable/reference/generated/numpy.linalg.det.html | `GATHER_VERIFIED` | `inferred` |
| array runtime | SciPy determinant | https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.det.html | `GATHER_VERIFIED` | `inferred` |
| GPU kernel | Triton | https://triton-lang.org/main/programming-guide/chapter-1/introduction.html | `GATHER_VERIFIED` | `inferred` |
| AI runtime | Modular MAX | https://www.modular.com/open-source/max | `GATHER_VERIFIED` | `inferred` |
| formal prover | Lean | https://lean-lang.org/doc/reference/latest/ | `GATHER_VERIFIED` | `inferred` |
| formal prover | Rocq | https://rocq-prover.org/docs | `OFFICIAL_ANCHOR_UNVERIFIED_LOCALLY` | `inferred` |
| formal prover | Isabelle | https://isabelle.in.tum.de/ | `OFFICIAL_ANCHOR_UNVERIFIED_LOCALLY` | `inferred` |
| formal prover | Agda | https://agda.readthedocs.io/ | `GATHER_VERIFIED` | `inferred` |
| observability | OpenTelemetry | https://opentelemetry.io/docs/concepts/observability-primer/ | `GATHER_VERIFIED` | `inferred` |
| experiment tracking | MLflow Tracking | https://mlflow.org/docs/latest/ml/tracking/ | `GATHER_VERIFIED` | `inferred` |
| experiment tracking | Weights and Biases | https://docs.wandb.ai/models/track | `GATHER_VERIFIED` | `inferred` |
| lineage | OpenLineage | https://openlineage.io/docs/ | `GATHER_VERIFIED` | `inferred` |

Gather failed for the Rocq and Isabelle pages with local certificate
verification errors. They remain official anchors, not local Gather receipts.

## Receipt Contract

| Field | Purpose |
| --- | --- |
| `source_receipts` | Gather/OpenLineage references for papers, docs, datasets, and source leads. |
| `oracle` | Exact proof, reference implementation, formal theorem, or declared unavailable oracle. |
| `runtime_branch` | Runtime name, version, target, seed, hardware, input hash, output hash, and drift metric. |
| `compiler_branch` | Compiler, IR, flags, target triple/device, build hash, and executable hash when compiled. |
| `telemetry_branch` | OpenTelemetry-style traces, spans, and logs for action provenance. |
| `lineage_branch` | Dataset, job, and run lineage references where data pipelines are involved. |
| `verifier_verdict` | Crucible `MATCH` / `DRIFT` / `UNVERIFIABLE` verdict and falsifier. |
| `non_promotion_boundary` | Statement of what the packet does not prove. |

## Hamiltonian Long-Horizon Experiment

The exact proof branch checks `M^T S M = S` and `det(M)=1` for each rational
kick-drift harmonic oscillator case, then records an induction claim inside
the scoped map. The float branch measures runtime drift only.

| h | Exact determinant | Exact invariant all steps | Horizons | Max float drift | Status |
| --- | --- | --- | --- | ---: | --- |
| `1/3` | `1` | true | 24, 240, 2400, 24000 | `1.4854784069484595e-12` | `MATCH` |
| `1/2` | `1` | true | 24, 240, 2400, 24000 | `2.275957200481571e-14` | `MATCH` |
| `2/3` | `1` | true | 24, 240, 2400, 24000 | `5.486722187697524e-13` | `MATCH` |

Negative fixture: explicit Euler with determinant `10/9` records area-growth
log10 of `10.981797734562035` at 240 steps and
`1098.1797734562035` at 24000 steps.

Status: `LAW_CANDIDATE`, not `PROMOTED_LAW`.

## Flagship Receipts

| Tool | Status | Notes |
| --- | --- | --- |
| Gather web | `MATCH` | 15 local web receipts under `gather/pass-0122-runtime-sources`. |
| Gather packet | `MATCH` | Packet hash `5e2e310aa4c698de5bbd025798b5804a51a9e5ef8e4930377f414b2fb48fbdc4`; seal `ec54b7412471536f4229305dff90c10d2f9e866b41d3fa9e23e6c73d4e20228d`. |
| Gather brief | `MATCH` | Brief hash `21aea20092616e134a83a22c79c8fc2aed4e008a42f9b1c6d293e83b92cd822b`; seal `71f94782d14289a225708fe77134548f872b37c02a518b227199bbc211fe27f1`. |
| Forum | `MATCH` | Route receipt captured in the artifact. |
| Index | `MATCH` | Context envelope verified. |
| Telos | `MATCH` | Status receipt recorded. |
| Telos catalog | `MATCH` | Catalog summary detected. |

## Crucible

| Field | Value |
| --- | --- |
| Thesis id | `0e1f7937fd2e9ba8` |
| Thesis seal | `0e1f7937fd2e9ba8a194c19dcba3bbab7c7a5823cff9cb6e78323e763b662c93` |
| Verdict seal | `199d480dea516ee151f9bdd7266902624709697fe0284615a54ae98853702c43` |
| Measurement seal | `c67c8c151b80de9220c66455bb163dad03ea45ea024b66991b171c22f05daaf1` |
| Assessment seal | `fc605b10dd97a6465bb136bd4616fd9cfb9e100fcd90564728bfa2916c0fb9f3` |
| Counts | `MATCH 12 / DRIFT 0 / UNVERIFIABLE 0` |
| Registry after pass | 113 theses, 1005 claims, 971 unique claims, 116 assessments, 113 latest assessments, 0 invalid latest assessments |

## File Hashes

| File | SHA-256 |
| --- | --- |
| `tools/compose_scientific_runtime_receipt_layer_spec.py` | `bf61c6537db49e829ba72ee485ae923964bb89265eaef7b3b2d3f1ba57908ef2` |
| `tools/test_scientific_runtime_receipt_layer_spec.py` | `3a737d6e0cc1f9e46b63fb97fcb83e1ebdf4df5605140a3961f0b4a0112e1975` |
| `tools/validate_pass_0122_scientific_runtime_layer.py` | `508723b0fb139dbf01f81c624240d1421f0a7568933ca941342847a2a09a5b07` |
| `tools/probe_scientific_runtime_receipt_layer_spec.py` | `3191d632dd8a4ac26f3f47b5e106bb25d46545e5b91e662c0d80973d2c7c80ab` |
| `schemas/scientific-runtime-receipt-layer-spec-pass-0122.json` | `cf964fa274918811b9010d2e760fadb70bd4c0949d72de501419af0a232e90ba` |
| `schemas/pass-0122-scientific-runtime-layer-validator-result.json` | `e71bbd65b700d173804b95e42e102de1e92f0532d60cb8f2e1c2cbd1bcbd0680` |
| `schemas/tool-receipts-pass-0122.json` | `31ab74a9e9d6b4be2b788b69002a038b29dda0fe5c0e85bc6314230df4f39ba0` |
| `packets/132-scientific-runtime-receipt-layer-spec.md` | `5e2e310aa4c698de5bbd025798b5804a51a9e5ef8e4930377f414b2fb48fbdc4` |
| `briefs/132-scientific-runtime-receipt-layer-brief.md` | `21aea20092616e134a83a22c79c8fc2aed4e008a42f9b1c6d293e83b92cd822b` |
| `adversarial/pass-0122-scientific-runtime-receipt-layer-steelman.md` | `093de478cb7106a3d109be8d7f6d2761c21ad0cef5ab477e47b8603182eb1214` |
| `crucible/pass-0122-thesis.json` | `539f2a1d78ebc95f87ee8e0035381ca8b6bdda30e7557d75b1033248d990499a` |
| `crucible/pass-0122-measurements.json` | `2bae3071dc419bc788fad40dbd393ba764f96852ae5ff95b1ae6a52a940197d6` |
| `crucible/pass-0122-report.md` | `16327d2ff9f2b6c226548ec556b93b61380a2d0fd19ae1cc733b53b5b371e1cd` |
| `crucible/pass-0122-run.json` | `5b782b9d866ff49c943d8605950531449b3113892790bbb9727023a52f1cec76` |

## Verification Commands

```powershell
python -m py_compile docs\research\dogfood\tools\compose_scientific_runtime_receipt_layer_spec.py docs\research\dogfood\tools\test_scientific_runtime_receipt_layer_spec.py docs\research\dogfood\tools\validate_pass_0122_scientific_runtime_layer.py docs\research\dogfood\tools\probe_scientific_runtime_receipt_layer_spec.py
python docs\research\dogfood\tools\probe_scientific_runtime_receipt_layer_spec.py
python docs\research\dogfood\tools\test_scientific_runtime_receipt_layer_spec.py
python docs\research\dogfood\tools\validate_pass_0122_scientific_runtime_layer.py
gather docs docs\research\dogfood\packets\132-scientific-runtime-receipt-layer-spec.md --json
gather docs docs\research\dogfood\briefs\132-scientific-runtime-receipt-layer-brief.md --json
crucible run docs\research\dogfood\crucible\pass-0122-thesis.json --measurements docs\research\dogfood\crucible\pass-0122-measurements.json --registry docs\research\dogfood\crucible\registry --report docs\research\dogfood\crucible\pass-0122-report.md --out docs\research\dogfood\crucible\pass-0122-run.json --json
crucible registry stats docs\research\dogfood\crucible\registry --json
```

## Next Pass Queue

1. Build `ScientificRuntimeReceipt/v1` fixtures for NumPy, SciPy, JAX,
   Julia/SciML, BuildLang/buildc, MLIR/OpenXLA, Triton, and color calibration.
2. Add `compiler_branch` negative fixtures that reject claims without compiler
   hash, IR hash, target device, and executable digest.
3. Turn the long-horizon Hamiltonian result into an adapter benchmark that
   compares exact oracle, float replay, interval/decimal replay, and compiled
   runtime replay.
4. Add a counterexample-revision workbench pass for theoretical CS claims.
