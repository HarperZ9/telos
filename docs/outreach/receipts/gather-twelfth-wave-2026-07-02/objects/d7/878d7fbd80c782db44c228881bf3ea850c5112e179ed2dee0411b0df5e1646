# Packet 016: Formal Tooling and Build Availability

Status: `HYPOTHESIS` plus `PROBE_MATCH`

## Market Context

The `pipeline-math` repository presents a concrete reference point: GPT-generated proof discovery via a prover-verifier pipeline, author verification, and Lean formalization for some results. Its public README lists open-problem writeups and Lean artifacts where available.

Source URL: https://github.com/Pengbinghui/pipeline-math

The relevant lesson is not that Telos should clone the repo. The lesson is that proof discovery, formalization, source references, and author/reviewer verification are now becoming product-shaped workflows.

## Local Availability

| Item | Result | Label |
| --- | --- | --- |
| `lean` on PATH | not found | `verified` |
| `buildc` on PATH | not found | `verified` |
| `build-universe` | present at `C:\dev\public\build-universe` | `verified` |
| Build Universe README | describes BuildLang, Rust compiler, `.bld` modules, and C backend | `verified` |
| Build Universe STATUS | reports 612 cargo tests passing for compiler and honest limitations around whole-ecosystem compilation/self-hosting | `verified local docs` |
| Build Color import | local Python import probe succeeded | `verified` |
| Calibrate Pro CLI | `python -m calibrate_pro --help` succeeded and exposed the command surface | `verified` |

## Build Family Substrate

Observed local projects:

- `C:\dev\public\build-ecosystem`: meta-package for Build family tools.
- `C:\dev\public\build-engine`: paper-first adaptive prediction/trading engine.
- `C:\dev\public\build-universe`: BuildLang ecosystem, compiler, OS kernel, `.bld` modules.
- `C:\dev\public\build-color`: color-science workbench.
- `C:\dev\public\calibrate-pro`: display calibration and verification product.

This is materially larger than a single BuildLang/buildc plan. BuildLang is one strategic pillar inside a larger proof-centered ecosystem.

## Build Color Probe

The pass ran local `build_color` functions:

- sRGB to Oklab and back;
- roundtrip max error `3.3306690738754696e-16`;
- Delta E 2000 sample `10.177916277801318`;
- ACES filmic monotonic check `true`;
- PQ EOTF monotonic check `true`;
- PQ peak output `10000.0` nits.

Classification: `PROBE_MATCH`.

## Telos Wedge

Hypothesis: BuildLang/buildc should become the typed receipt and deterministic kernel layer for scientific compute, not the whole product by itself.

Megatool shape:

- `BuildProofKernel`: deterministic color/math/finance/security kernels.
- `BuildReceiptCompiler`: compile `.bld` kernels and emit source/build/runtime receipts.
- `TelosResearchPacket`: attach source intake, claim labels, model/tool actions, and Crucible verdicts.
- `CalibrateProMeasurementPacket`: attach real-world display measurements, LUT/ICC artifacts, report hashes, and drift status.
- `IndexAtlas`: map all local source, docs, and test receipts.

## Gaps

| Gap | Label | Note |
| --- | --- | --- |
| `buildc` was not callable from PATH. | `verified` | Next pass should locate or build the compiler binary. |
| `lean` was not callable from PATH. | `verified` | Formal math demo cannot claim Lean verification locally yet. |
| Build Universe reports strong compiler progress but also explicit open limitations. | `verified local docs` | The plan must preserve honesty labels. |
| Calibrate Pro enterprise receipts are specified, but implementation was not verified here. | `inferred` | Need direct source/test pass. |
| Cross-layer packet schema is not yet implemented as a single product. | `verified` | Current work is research and architecture. |

## Demo Candidate

Create `build-color-proof-kit`:

1. Run deterministic Build Color golden vectors.
2. Emit `ScientificRuntimeProofKit` JSON with source paths and function names.
3. Attach Calibrate Pro CLI surface receipt.
4. Attach Build Universe STATUS/ARCHITECTURE source refs.
5. Crucible checks roundtrip error and monotonic transfer functions.
6. Later add `buildc` compilation receipt when callable.

## Market Read

Buyers: visual effects studios, color pipeline teams, AI dataset QA teams, scientific-compute teams, finance/security teams that need reproducibility.

Primary wedge: measurable truth at the runtime edge. BuildLang/buildc provides long-term language leverage; Build Color and Calibrate Pro provide near-term evidence.
