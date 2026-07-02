# Dogfood Pass 0033 Ledger

Date: 2026-07-01

Status: `CRUCIBLE_MATCH`.

Crucible assessment:

- thesis id: `e0fbf2e80a5bb575`;
- claims: `10`;
- match: `10`;
- drift: `0`;
- unverifiable: `0`;
- thesis seal: `e0fbf2e80a5bb57507ac827d4273b024059c3a5cd91950da7596e6e8b29ae7b4`;
- verdict seal: `01c8238db7bf4945322a4aafc844170aa6f0efd234c22c0c6840459e1c7d38bf`;
- measurement seal: `50199bb646d896426d1465ddc5e84355253ce7c8a2d14d1ba7eb9c46066a9242`;
- assessment seal: `996d0fb95c0e4e2e9f81eefe8d5871fdbd94531bc641e9a77d2e82e339669f8b`;
- integrity: `seals_ok=True`, `thesis_ok=True`, `verdicts_rederive=True`.

Pass theme: contained Lean provisioning for `pipeline-math` Problem 4(b),
advancing from `lake_missing` to a bounded long-running Mathlib dependency
build timeout.

No Lake build success, theorem replay, axiom check, statement-gate compilation,
theorem correctness claim, buyer adoption signal, system install claim, Telos
uniqueness fact, or natural law is promoted in this pass.

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
sha256 = 0fdac6d4a3e787b78c9bb11bbc19f089e87c1f3b694fde89ef8ec1a2c782dc91
seal = 253454846e935adc19ad0cb1ff251eaeef33d00b40dc00e0473f4644fa8adf7d
```

Source binding:

```text
path = schemas/lean-replay-remediation-contract-pass-0032.json
sha256 = fd35080a7d14c8be0fcb96cea88293d2ca106977080a4eeae687228ce77e3a62
seal = 64e1d89130480d56bb5a54a19ee07e182537f73eca5ca12b29782f4689239b05
```

## Provisioning Chain

Elan release and installer:

```text
release_tag = v4.2.3
published_at = 2026-06-08T07:27:27Z
asset = elan-x86_64-pc-windows-msvc.zip
asset_sha256 = be5e92a2dfdd8176099b2db0b810c27237c9054f1e5db1126f4f2a1134773b25
elan_init_sha256 = 175089915efc623126a1560ed517cd52ec2d4d09f2adc1c10f22f56568fed5ad
```

Contained install:

```text
command = elan-init.exe -y --no-modify-path --default-toolchain leanprover/lean4:v4.31.0
elan_home_ref = temp:telos-pass0033-elan-home
install_exit_code = 0
normal_path_modified = false
external_write_performed = false
temp_write_performed = true
```

Toolchain:

```text
elan_version = elan 4.2.3 (b6cec7e10 2026-06-08)
lean_version = Lean 4.31.0 commit 68218e876d2a38b1985b8590fff244a83c321783
lake_version = Lake version 5.0.0-src+68218e8
```

## Build Timeout

Verifier attempt:

```text
command = scripts/verify.sh --no-log --all
status = TIMEOUT_TERMINATED
failure_class = mathlib_build_long_running_timeout
elapsed_timeout_seconds = 604
monitor_window_seconds = 600
lake_reached = true
lean_workers_reached = true
semantic_failure_observed = false
theorem_replay_completed = false
```

Stop receipt:

```text
stopped_count = 27
remaining_count_after_stop = 0
```

Partial build artifact snapshot:

```text
file_count = 46930
byte_sum = 3208367614
.olean_count = 2659
```

## Validator Result

```text
status = MATCH
contained_install_status = MATCH
lake_reached = true
lean_version = Lean 4.31.0
lake_version = Lake 5.0.0-src+68218e8
theorem_replay_completed = false
processes_remaining_after_stop = 0
negative_fixture_count = 10
```

## Tool Substrate Receipt

Gather docs receipt for packet 043:

```text
sha256 = 9b0c93f54649561d3d523c39385b2ecaf2d52650a4a9241c9012f7274a14dc3a
seal = 4ebfdf2754b5a08375d23d6f1270a583475a23321e1378b98d183aa463f185be
chars = 6162
```

Index dogfood substrate map:

```text
root_sha256_prefix = f2f0af39219698a9
top_level_count = 40
```

Tool receipt status:

```text
schemas/tool-receipts-pass-0033.json
status = MATCH_WITH_FORUM_SUBMIT_GAP_AND_BUILD_TIMEOUT
```

Forum route:

```text
decided = null
confidence = 0.0
needs_escalation = true
top_candidates = ci-cd, cloud-infra, model-foundry, project-telos
```

Forum submit attempt:

```text
status = UNVERIFIABLE
error = submit needs a model executor
```

## Artifacts

| Artifact | Role |
| --- | --- |
| `tools/probe_lean_provisioning_build_timeout.py` | Lean provisioning and build-timeout contract generator. |
| `tools/validate_pass_0033_lean_provisioning.py` | Validator for pass 0033 source binding, release hashes, temp install scope, toolchain versions, timeout classification, process stop, and negative fixtures. |
| `fixtures/lean-provisioning-build-timeout-pass-0033.json` | Provisioning and timeout fixture. |
| `packets/043-lean-provisioning-build-timeout.md` | Human-readable provisioning and build-timeout packet. |
| `adversarial/pass-0033-lean-provisioning-steelman.md` | Local pass 0033 steelman. |
| `schemas/lean-provisioning-build-timeout-pass-0033.json` | `LeanProvisioningBuildTimeoutContract/v1` artifact. |
| `schemas/pass-0033-lean-provisioning-validator-result.json` | Validator receipt for pass 0033. |
| `schemas/tool-receipts-pass-0033.json` | Compact Index, Gather, Shell, Telos, Forum, and Crucible receipts. |
| `crucible/pass-0033-thesis.json` | Falsifiable claims for the thirty-third pass. |
| `crucible/pass-0033-measurements.json` | Measurements/evidence for the thirty-third pass. |
| `crucible/pass-0033-report.md` | Crucible report for the thirty-third pass. |
| `crucible/pass-0033-run.json` | Crucible run record for the thirty-third pass. |

## Primary Next Push

Avoid rebuilding Mathlib from source if a cache exists:

- run the project-supported cache path, likely `lake exe cache get`, under the
  contained temp Elan home;
- hash any downloaded cache material;
- separate dependency-cache hydration from project build;
- rerun `scripts/verify.sh --no-log --all` under a larger but bounded budget;
- promote nothing until exit code 0 and theorem-specific checks exist.

## Natural-Law Promotion

Current promoted natural laws: none.
