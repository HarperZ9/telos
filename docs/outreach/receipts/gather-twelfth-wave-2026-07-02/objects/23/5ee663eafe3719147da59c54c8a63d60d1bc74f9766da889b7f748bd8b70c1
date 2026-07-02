# Packet 044: Lean Replay Verification

Date: 2026-07-01

Status: `REPLAY_MATCH_WITH_AXIOM_BOUNDARY`

Pass 0034 completes the local replay chain for `pipeline-math`
`lean/problem-4b-formalization` after hydrating Mathlib cache artifacts. The
repository verifier exits 0 and reports PASS across frozen pins, banned keyword
scan, Lake build, ten axiom checks, and statement gates.

This verifies the local Lean artifact under the recorded toolchain, source
commit, cache, and verifier-script boundaries. It does not validate every public
claim about `pipeline-math`, does not prove a new theorem outside the Lean
artifact, and does not promote any natural law.

## Source Binding

Pass 0034 is bound to pass 0033:

```text
path = schemas/lean-provisioning-build-timeout-pass-0033.json
schema = LeanProvisioningBuildTimeoutContract/v1
sha256 = e4a4085f9711d672ee18a08e85aa55b6fabe8f64807daad53eff382506b9a366
seal = 8871fe5c59a75d81f24e6396a62d6cf484c7504d3304c695861c4b4799c16a9c
```

## Cache Hydration

Command:

```text
lake exe cache get
```

Receipt:

```text
exit_code = 0
downloaded_files = 8542
decompressed_files = 8542
cache_dir_ref = temp:telos-pass0034-mathlib-cache
cache_file_count = 8542
cache_byte_sum = 432264798
external_call_performed = true
temp_write_performed = true
```

This resolves the pass 0033 dependency-build timeout by using the project’s
Mathlib cache path instead of rebuilding all dependencies from source.

## Verifier Run

Command:

```text
scripts/verify.sh --no-log --all
```

Receipt:

```text
exit_code = 0
duration_seconds = 1184
result = PASS
result_issue_count = 0
build_jobs = 8574
```

Check statuses:

```text
frozen_sha_pins_status = PASS
banned_keywords_status = PASS
lake_build_status = PASS
theorem_axiom_status = PASS
statement_gate_count = 2
remaining_temp_processes = 0
```

Statement gates:

```text
Prob4b.Discharge = PASS
Prob4b.Solution = PASS
```

## Axiom Boundary

All ten `Prob4b.Solution.*` axiom checks passed with this exact axiom set:

```text
[propext, Classical.choice, Quot.sound]
```

Theorem names checked:

```text
B_triple_zero
M_triple_defect
M_annihilator
M_pairwise_intersection
triple_defect_survives
R_finite_conductor
R_not_quasi_coherent
prob4b_counterexample
problem4b_false
quasiCoherent_imp_finiteConductor
```

This is a meaningful replay result, but it is not "axiom-free" and must not be
reported that way.

## Build Artifact Snapshot

```text
.lake file_count = 123892
.lake byte_sum = 8009101293
Prob4b build file_count = 75
Prob4b build byte_sum = 10048128
Prob4b outputs = 15 .olean, 15 .ilean, 15 .trace, 30 .hash
```

## Primary Receipt

Receipt:

```text
path = schemas/lean-replay-verification-pass-0034.json
schema = LeanReplayVerificationPacket/v1
status = LEAN_REPLAY_VERIFIED_WITH_AXIOM_BOUNDARY
seal = bbe72907f7bc745c4bdc19f2162050d0dc7e48ea9382bc0b09f226f2500539bd
```

Fixture:

```text
path = fixtures/lean-replay-verification-pass-0034.json
schema = LeanReplayVerificationFixture/v1
sha256 = eef39b1caa78dd2d996589b08c40b93881cfe45d17e2b15479ec9aa8d5b9fafb
seal = fd38f5abf22c501b06e28321e9408d5562e154eb4a012c4988a64b910a6ffa2f
```

Validator:

```text
path = schemas/pass-0034-lean-replay-validator-result.json
status = MATCH
verifier_exit_code = 0
verifier_result = PASS
lake_build_status = PASS
theorem_axiom_status = PASS
axiom_check_count = 10
cache_file_count = 8542
prob4b_build_file_count = 75
remaining_temp_processes = 0
```

## Negative Fixtures

All ten negative fixtures expect validator status `REJECT`:

```text
negative-cache-get-promoted-without-exit-zero
negative-lake-build-promoted-without-pass
negative-axiom-check-omitted
negative-axiom-set-missing
negative-statement-gate-omitted
negative-banned-keywords-ignored
negative-frozen-pins-ignored
negative-processes-left-running
negative-public-claim-overpromoted
negative-natural-law-promoted
```

## Product Reading

This is the first end-to-end proof packet in the chain:

```text
source receipt -> LF checkout -> temp python3 shim -> temp Lean/Lake toolchain
-> Mathlib cache hydration -> Lake build -> theorem axiom checks
-> statement gates -> non-promotion boundary
```

The same structure should become the template for BuildLang/buildc, color
calibration, rendering, finance/quant, security, biology, robotics, and AI/ML
proof packets: every claim must name the source, runtime, cache, build, verifier
exit, permitted axioms/assumptions, output artifacts, and promotion boundary.

## Next Action

Create theorem-specific proof packets for each of the ten names, with command
transcript digests and per-theorem receipts. Then compare the verified Lean
artifact to `pipeline-math` public claims without overpromoting beyond what the
Lean run establishes.

## Non-Promotion Boundary

This pass verifies the local Lean replay harness for `pipeline-math` Problem
4(b) under the stated boundaries. It does not validate every public
`pipeline-math` claim, does not establish a natural law, and does not remove the
recorded axiom dependencies.

Current promoted natural laws: none.
