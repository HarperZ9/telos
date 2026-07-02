# BuildLang Scientific Runtime Receipts

Pass: `0010`

Status: schema fixture, not a compiled buildc execution.

## Purpose

Pass 0009 proved that a scientific claim packet can bind a classical PDE identity, a bounded positive numerical witness, a bounded negative fixture, market context, and verifier receipts. Pass 0010 turns that into the receipt contract BuildLang/buildc should emit directly.

The product wedge is not "another scientific language." The wedge is an accountable scientific runtime where a result is born with the source, compiler, runtime, problem, invariant, measurement, and external-verdict facts needed for review.

## Minimum Receipt Layers

| Layer | Required Evidence |
| --- | --- |
| source | workspace, head, source files, source refs, source hash |
| build | compiler, compiler status, target, flags, dependencies, build hash |
| runtime | runtime, OS, hardware class, deterministic seed, environment hash |
| problem | equation/model, domain, boundary conditions, discretization |
| measurement | metric, observed values, thresholds, units |
| invariant | expectation, observed result, tolerance, status |
| external verdict | validator, Crucible, formal checker, reviewer, or lab verdict |

## Fixture Receipts

The fixture set contains two receipts:

- `buildlang-scirun-heat-energy-stable-pass-0010`: positive receipt, stable CFL, energy monotone, status `PASS`.
- `buildlang-scirun-heat-energy-unstable-negative-pass-0010`: negative fixture, unstable CFL, energy growth detected, status `FAIL_EXPECTED`.

Both receipts honestly label the compiler state as `ADAPTER_FIXTURE_NOT_BUILDC_EXECUTED`. This keeps the pass useful without overstating implementation maturity.

## BuildLang/buildc Implication

The next buildc integration should not only produce numbers. It should emit receipts as a first-class runtime product:

1. compile kernel;
2. seal source and build inputs;
3. execute deterministic fixture;
4. compute invariant checks;
5. preserve expected failures;
6. export a proof-packet-compatible JSON receipt;
7. run Crucible or another verifier against the receipt.

## Non-Promotion Statement

This pass promotes no new mathematical theorem, physical law, biological result, material result, medical result, safety result, or finance result. It is a systems architecture pass for accountable scientific compute.
