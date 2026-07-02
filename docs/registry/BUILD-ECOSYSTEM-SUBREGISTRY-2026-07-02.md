# Build Ecosystem Subregistry

Date: 2026-07-02
Status: first Build ecosystem consolidation pass

Machine-readable registry:
`docs/registry/build-ecosystem-subregistry-2026-07-02.json`

This subregistry keeps BuildLang/buildc and the adjacent Build repos from being
flattened into one vague "compiler ecosystem" claim. BuildLang/buildc is the
receipt-bearing compute layer. Build Universe is the alpha domain-module
ledger. The Python Build apps are market and proof-demo lanes. The editor
packages are support surfaces only.

## Evidence Read

| Evidence | What it supports | Boundary |
| --- | --- | --- |
| `C:/dev/public/pubscan/quantalang/README.md` | BuildLang product names, `buildc`, C backend, experimental backends, receipts. | Do not infer production maturity for every backend. |
| `C:/dev/public/pubscan/quantalang/STATUS.md` | Scientific-runtime status, invariant family, partial/aspirational surfaces. | Do not claim self-hosting or full linear-type soundness. |
| `C:/dev/public/pubscan/quantalang/docs/SCIENTIFIC-RECEIPT.md` | Receipt schema, invariant checks, re-run verification, non-claims. | Does not prove a physical law or PDE correctness. |
| `C:/dev/public/build-universe/README.md` and `STATUS.md` | Alpha ecosystem reality, module tiers, BuildOS boundary, self-hosting goal. | Does not prove whole-ecosystem compilation. |
| Build app READMEs | Color, calibration, finance, forecasting, adaptive paper loops, shared UI, meta-package. | Product-surface docs need receipt gates before stronger claims. |
| Build editor READMEs | Syntax highlighting and grammar support. | No compiler/runtime capability. |

## Current Build Shape

| Row | Role | Maturity | Telos integration | Publication boundary |
| --- | --- | --- | --- | --- |
| BuildLang/buildc | Accountable scientific compute and compiler layer. | Active compiler with shipped receipt lane and experimental surfaces. | Import `buildlang-scientific-runtime-receipt/v0` into Telos and Crucible. | Methods-paper-ready for receipts; no language-replacement claim without benchmarks. |
| Build Universe | Build family and domain-module ledger. | Alpha mixed-maturity ecosystem. | Use as module and domain map. | Cite only with alpha and module-tier caveats. |
| Build Color | Color-science workbench. | Public Python tool. | Color/rendering measurement proof kit. | Needs measured outputs and profile hashes for proof demos. |
| Calibrate Pro | Display calibration and verification. | Public tool with measurement caveats. | Device/display side of color proof kit. | Sensorless mode remains estimate; measured claims need instrument reports. |
| Build Finance | Quant/backtesting toolkit. | Public money-adjacent tool. | Backtest/strategy proof packets. | Paper/backtest-only unless separately reviewed. |
| Build Oracle | Forecasting workbench. | Public time-series tool. | Forecast evaluation receipts. | Needs dataset boundaries, baselines, horizon, and leakage checks. |
| Build Engine | Adaptive prediction and paper-trading loop. | Public paper-first loop. | Objective Monitor and loop-ledger quant instantiation. | No advice, no live-mode proof demo by default. |
| Build UI | Shared PyQt UI layer. | Support package. | Build app shell consistency. | Product-support doc only. |
| Build Ecosystem | Meta-package. | Distribution wrapper. | Onboarding/package lane. | Not evidence of domain correctness. |
| BuildLang VS Code | Editor support. | Syntax/language config only. | Developer experience. | Not compiler maturity evidence. |
| BuildLang TextMate Grammar | Editor grammar. | Grammar support only. | Developer experience. | Not runtime evidence. |

## Priority Integration Work

1. **BuildLang receipt import into Telos and Crucible.**
   First artifact: a Telos fixture that consumes
   `buildlang-scientific-runtime-receipt/v0`, exports a Crucible measurement
   row, and keeps the non-claim labels attached.

2. **Color/rendering measurement proof kit.**
   First artifact: a profile/transform/device-state packet joining Build Color,
   Calibrate Pro, Telos display calibration, artifact hashes, and Delta E.

3. **Quant and forecast proof packets.**
   First artifact: a paper-mode forecast-to-backtest loop receipt joining Build
   Oracle, Build Finance, Build Engine, Objective Monitor, and loop ledger.

4. **Build Universe module-tier import.**
   First artifact: a machine row per Build Universe module with tier, score,
   real core, scaffolding, and Telos lane.

## Hard Non-Claims

- BuildLang scientific receipts witness observed output series against declared
  invariants. They do not prove physical law, PDE correctness, or model truth.
- Build Universe is alpha. Whole-ecosystem compilation and self-hosting remain
  goals unless a current receipt proves otherwise.
- Build Color and Calibrate Pro do not create universal color correctness.
  Public proof demos need measured outputs, device state, and profile hashes.
- Build Finance, Build Oracle, and Build Engine do not provide investment
  advice or expected-return guarantees.
- Build UI, BuildLang VS Code, and BuildLang TextMate Grammar are support
  surfaces, not proof of compiler/runtime behavior.

## Next Passes

1. Create `buildlang-scientific-runtime-receipt/v0` import fixture in Telos.
2. Create `build-universe-module-tier-subregistry.json` from
   `build-universe/STATUS.md`.
3. Create a color/rendering proof-kit schema from Build Color and Calibrate Pro.
4. Create a finance/forecast receipt schema from Build Finance, Build Oracle,
   and Build Engine.
5. Resolve Calibrate Pro version wording drift before citing exact release
   numbers in public front-door docs.
