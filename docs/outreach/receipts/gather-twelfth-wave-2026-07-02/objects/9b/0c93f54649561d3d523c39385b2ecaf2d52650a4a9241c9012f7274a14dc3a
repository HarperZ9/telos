# Packet 043: Lean Provisioning And Build Timeout

Date: 2026-07-01

Status: `PROVISIONING_MATCH_WITH_BUILD_TIMEOUT`

Pass 0033 advances the `pipeline-math` replay chain beyond `lake_missing` by
provisioning a contained Lean toolchain under `%TEMP%`. The verifier then
reaches `lake build`, starts compiling Mathlib, and is stopped after a bounded
long-running build window. This is not a theorem replay success and not a Lake
build success.

## Source Binding

Pass 0033 is bound to pass 0032:

```text
path = schemas/lean-replay-remediation-contract-pass-0032.json
schema = LeanReplayRemediationContract/v1
sha256 = fd35080a7d14c8be0fcb96cea88293d2ca106977080a4eeae687228ce77e3a62
seal = 64e1d89130480d56bb5a54a19ee07e182537f73eca5ca12b29782f4689239b05
```

Pass 0032 identified `lake_missing` as the next replay gate. Pass 0033 resolves
that gate in a contained temp environment and records the next gate.

## Release And Installer Receipt

Observed Elan release:

```text
api_url = https://api.github.com/repos/leanprover/elan/releases/latest
release_tag = v4.2.3
published_at = 2026-06-08T07:27:27Z
asset = elan-x86_64-pc-windows-msvc.zip
asset_bytes = 2389007
asset_sha256 = be5e92a2dfdd8176099b2db0b810c27237c9054f1e5db1126f4f2a1134773b25
elan_init_bytes = 5842944
elan_init_sha256 = 175089915efc623126a1560ed517cd52ec2d4d09f2adc1c10f22f56568fed5ad
```

Installer help confirmed:

```text
-y
--no-modify-path
--default-toolchain <default-toolchain>
```

Public source receipts:

```text
elan release = https://github.com/leanprover/elan/releases/tag/v4.2.3
elan README = https://github.com/leanprover/elan
Lean Elan manual = https://lean-lang.org/doc/reference/latest/Build-Tools-and-Distribution/Managing-Toolchains-with-Elan/
```

## Contained Install Probe

Command shape:

```text
elan-init.exe -y --no-modify-path --default-toolchain leanprover/lean4:v4.31.0
```

Receipt:

```text
elan_home_ref = temp:telos-pass0033-elan-home
install_exit_code = 0
normal_path_modified = false
external_write_performed = false
temp_write_performed = true
status = MATCH
```

Installed temp proxy files:

```text
elan.exe
lake.exe
lean.exe
leanc.exe
leanchecker.exe
leanmake.exe
leanpkg.exe
```

## Toolchain Probe

```text
elan_version = elan 4.2.3 (b6cec7e10 2026-06-08)
lean_toolchain = leanprover/lean4:v4.31.0
lean_version = Lean (version 4.31.0, x86_64-w64-windows-gnu, commit 68218e876d2a38b1985b8590fff244a83c321783, Release)
lake_version = Lake version 5.0.0-src+68218e8 (Lean version 4.31.0)
status = MATCH
```

This proves the pass 0032 `lake_missing` gate is resolved inside the temp
environment. It does not prove the project builds.

## Verifier Attempt

Command shape:

```text
scripts/verify.sh --no-log --all
```

Runner environment:

```text
ELAN_HOME = temp:telos-pass0033-elan-home
PATH includes temp:telos-pass0032-shim
PATH includes temp:telos-pass0033-elan-home/bin
source clone = temp:pipeline-math-pass0032-lf
```

Result:

```text
status = TIMEOUT_TERMINATED
failure_class = mathlib_build_long_running_timeout
elapsed_timeout_seconds = 604
monitor_window_seconds = 600
lake_reached = true
lean_workers_reached = true
semantic_failure_observed = false
theorem_replay_completed = false
```

Process stop receipt:

```text
stopped_count = 27
remaining_count_after_stop = 0
stop_scope = processes whose command lines referenced temp Elan home, temp pipeline-math clone, or temp python3 shim
```

Build artifact snapshot at stop:

```text
file_count = 46930
byte_sum = 3208367614
.hash = 15955
.lean = 9341
.json = 2702
.trace = 2679
.olean = 2659
.c = 2657
.server = 2657
.ir = 2657
.ilean = 2657
.private = 2657
```

## Primary Receipt

Receipt:

```text
path = schemas/lean-provisioning-build-timeout-pass-0033.json
schema = LeanProvisioningBuildTimeoutContract/v1
status = LEAN_PROVISIONING_MATCH_WITH_BUILD_TIMEOUT
seal = 8871fe5c59a75d81f24e6396a62d6cf484c7504d3304c695861c4b4799c16a9c
```

Fixture:

```text
path = fixtures/lean-provisioning-build-timeout-pass-0033.json
schema = LeanProvisioningBuildTimeoutFixture/v1
sha256 = 0fdac6d4a3e787b78c9bb11bbc19f089e87c1f3b694fde89ef8ec1a2c782dc91
seal = 253454846e935adc19ad0cb1ff251eaeef33d00b40dc00e0473f4644fa8adf7d
```

Validator:

```text
path = schemas/pass-0033-lean-provisioning-validator-result.json
status = MATCH
contained_install_status = MATCH
lake_reached = true
lean_version = Lean 4.31.0
lake_version = Lake 5.0.0-src+68218e8
theorem_replay_completed = false
processes_remaining_after_stop = 0
negative_fixture_count = 10
```

## Negative Fixtures

All ten negative fixtures expect validator status `REJECT`:

```text
negative-temp-install-claimed-system-install
negative-no-modify-path-omitted
negative-elan-home-not-temp
negative-zip-hash-missing
negative-lean-version-promoted-without-probe
negative-lake-build-promoted-after-timeout
negative-timeout-processes-left-running
negative-theorem-replay-promoted
negative-build-timeout-called-semantic-failure
negative-natural-law-promoted
```

## Product Reading

The useful megatool behavior is now sharper:

```text
convert "missing compiler/runtime" into "contained compiler/runtime exists",
then convert "build did not finish" into a typed dependency-build budget gate.
```

For BuildLang/buildc, color calibration, rendering, quant, finance, security,
biology, robotics, and AI/ML, this means the proof packet must separate:

- source checkout;
- dependency provisioning;
- dependency build/cache acquisition;
- project build;
- theorem or numerical replay;
- post-build proof checks;
- action receipt and non-promotion policy.

## Next Action

The next pass should avoid rebuilding all of Mathlib from source if a cache is
available. Test `lake exe cache get` or an equivalent project-supported cache
path under the same contained temp toolchain, then rerun `scripts/verify.sh
--no-log --all` with a longer but still bounded receipt.

## Non-Promotion Boundary

This pass verifies contained provisioning and a long-running dependency build
timeout only. It does not prove Lake build success, theorem replay, theorem
correctness, `pipeline-math` proof correctness, or any natural law.

Current promoted natural laws: none.
