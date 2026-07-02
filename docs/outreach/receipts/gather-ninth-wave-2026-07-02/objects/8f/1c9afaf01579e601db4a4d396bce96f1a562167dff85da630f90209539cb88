# Packet 041: Lean Replay Environment Contract

Date: 2026-07-01

Status: `PROBE_MATCH_WITH_REPLAY_GAP`

This pass turns the theorem replay preflight into an environment contract. It
does not install Lean and does not replay a theorem. It records the next exact
failure mode in the replay chain.

## Source Binding

```text
path = schemas/theorem-replay-preflight-pass-0030.json
schema = TheoremReplayPreflightPacket/v1
sha256 = da9a0d68491325bd636f876dfca60ab0540be2a9c247931bf22064a5db13a557
seal = fb2428b6a7d960e44fe44768e1864d6fc524e99b9461b7fc64d08012f6760180
```

## Runner Probe

Git Bash exists by absolute path and runs:

```text
git_bash_path_ref = program-files-git-bash
bash_version = GNU bash, version 5.2.37(1)-release (x86_64-pc-msys)
absolute_bash_invocation_status = MATCH
bash_on_path = false
```

This means shell execution is possible only through an explicit runner path in
this session. A replay harness must not assume `bash` is on PATH.

## Verification Script Attempt

Command shape:

```text
program-files-git-bash scripts/verify.sh --no-log --all
```

Result:

```text
exit_code = 1
status = DRIFT
first_failed_check = Frozen SHA pins
failure_class = crlf_pin_file_path_drift
lean_or_lake_reached = false
raw_log_included = false
```

Cause:

```text
scripts/frozen.sha256 is read with CRLF path text, so sha256sum sees
Prob4b/Defs.lean with a trailing carriage return.
```

This is now the first replay gate. The pass 0030 Git blob hashes still matter:
the frozen pins match blob bytes, but the verifier script running against a CRLF
working tree fails before Lake or Lean.

## Toolchain Availability

Available:

```text
git = MATCH
python = MATCH
git_bash_absolute = MATCH
```

Unavailable:

```text
docker = UNAVAILABLE
wsl = UNAVAILABLE_NOT_INSTALLED
podman = UNAVAILABLE
winget = UNAVAILABLE
elan = UNAVAILABLE
lake = UNAVAILABLE
lean = UNAVAILABLE
```

Replay policy:

```text
theorem_replay_status = UNVERIFIABLE_ENVIRONMENT_NOT_READY
lake_build_status = UNVERIFIABLE_ENVIRONMENT_NOT_READY
axiom_check_status = UNVERIFIABLE_ENVIRONMENT_NOT_READY
statement_gate_status = UNVERIFIABLE_ENVIRONMENT_NOT_READY
replay_promotion_allowed = false
```

## Primary Receipt

Receipt:

```text
path = schemas/lean-replay-environment-contract-pass-0031.json
schema = LeanReplayEnvironmentContract/v1
status = LEAN_REPLAY_ENVIRONMENT_CONTRACT_MATCH_WITH_REPLAY_GAP
seal = 4532f819ea8d8f7760323b2920d131b4909bedc05960ad3da553424e1f38a0bc
```

Fixture:

```text
path = fixtures/lean-replay-environment-contract-pass-0031.json
schema = LeanReplayEnvironmentContractFixture/v1
sha256 = 9c8a6ed07113c0880126e3ee5d19b1314a92b9d767c57d896df36e0222a62082
seal = c80c6f03f37ec172e1354293f709d399aa8d80a9c69e0d9e9cc6e697f81be555
```

Validator:

```text
path = schemas/pass-0031-lean-environment-contract-validator-result.json
status = MATCH
absolute_bash_invocation_status = MATCH
bash_on_path = false
verify_script_exit_code = 1
failure_class = crlf_pin_file_path_drift
lean_or_lake_reached = false
missing_runtime_count = 6
theorem_replay_status = UNVERIFIABLE_ENVIRONMENT_NOT_READY
negative_fixture_count = 10
```

## Action Receipt Proposal

```text
schema = ActionReceiptLeanReplayEnvironmentContract/v1
action_id = act_dogfood_0031_lean_environment_contract
event_id = evt_dogfood_0031_lean_environment_contract
event_type = lean_replay_environment_contract_created
authority_class = read_only_environment_probe
external_write_performed = false
toolchain_install_performed = false
replay_promotion_allowed = false
verification_verdict = MATCH
```

## Negative Fixtures

All ten negative fixtures expect validator status `REJECT`:

```text
negative-bash-path-assumed-from-path
negative-crlf-failure-ignored
negative-lean-replay-promoted-after-script-failure
negative-container-available-without-docker-or-wsl
negative-toolchain-install-claimed
negative-source-preflight-link-missing
negative-axiom-check-promoted
negative-lake-build-promoted
negative-external-write-hidden
negative-natural-law-promoted
```

## Market Reading

The useful product behavior is not simply "run Lean." It is:

```text
produce a receipt when replay cannot start, name the exact gate, and block all
downstream correctness promotion.
```

That same environment-contract layer applies to BuildLang/buildc, GPU kernels,
color calibration, finance simulations, biology pipelines, quantum workflows,
and any research automation that depends on a reproducible execution substrate.

## Next Action

The next pass should create a non-mutating replay remediation contract:

- choose blob-byte hashing or LF-preserving checkout;
- specify a reversible Lean `v4.31.0` provisioning path;
- define exact log receipts for `scripts/verify.sh --no-log --all`;
- keep theorem replay blocked until Lake build, axiom checks, and statement
  gates actually run.

## Non-Promotion Boundary

This pass verifies environment readiness and a verifier-script failure mode
only. It does not install Lean, does not run Lake, does not prove any theorem,
and does not promote any natural law.

Current promoted natural laws: none.
