# Dogfood Pass 0032 Ledger

Date: 2026-07-01

Status: `CRUCIBLE_MATCH`.

Crucible assessment:

- thesis id: `a7d8d84c56a97301`;
- claims: `10`;
- match: `10`;
- drift: `0`;
- unverifiable: `0`;
- thesis seal: `a7d8d84c56a973015cba5ca02f56a81b7cb4efbe0c51df4718e081b8a305d076`;
- verdict seal: `b770b3216ae3dea07c172dc126af163c63c5c8b4b78f7dd6c58b5654dba9661d`;
- measurement seal: `ef8a8fae49c32275d0b325be9eee93b3fd69be59daab7339758b5cf377e5e19a`;
- assessment seal: `2714d8f63f2b3e2aa55b4df5d204cb9cf3f08b6739ab411d4b72e9cbc1699096`;
- integrity: `seals_ok=True`, `thesis_ok=True`, `verdicts_rederive=True`.

Pass theme: non-mutating Lean replay remediation contract for `pipeline-math`
Problem 4(b), advancing from a CRLF frozen-pin failure to a missing Lake binary
without promoting theorem replay.

No Lean installation, Lake build success, theorem replay, axiom check,
statement-gate compilation, theorem correctness claim, buyer adoption signal,
Telos uniqueness fact, or natural law is promoted in this pass.

## Primary Receipt

Receipt:

```text
path = schemas/lean-replay-remediation-contract-pass-0032.json
schema = LeanReplayRemediationContract/v1
status = LEAN_REPLAY_REMEDIATION_MATCH_WITH_LAKE_GAP
seal = 64e1d89130480d56bb5a54a19ee07e182537f73eca5ca12b29782f4689239b05
```

Fixture:

```text
path = fixtures/lean-replay-remediation-contract-pass-0032.json
sha256 = 27da59a624c60468ebebcd3c19580933f66d82df3a5e289242b7b7351cef02f3
seal = 5bca5d4aa6b3c1b735da0c2e7a10bd1568194723e88781fa4f39955b5dafc08c
```

Source binding:

```text
path = schemas/lean-replay-environment-contract-pass-0031.json
sha256 = e10e07a409bf9a0cde7dcf8aae823b176b44a9b1610fcf133dc228b94219d3f1
seal = 4532f819ea8d8f7760323b2920d131b4909bedc05960ad3da553424e1f38a0bc
```

## Remediation Chain

LF checkout probe:

```text
repo_commit = 69d7df765a8f377a5e0628c6d36c088bce7642c9
checkout_policy = core.autocrlf=false
Prob4b/Defs.lean = i/lf w/lf
Prob4b/Theorems.lean = i/lf w/lf
scripts/frozen.sha256 = i/lf w/lf
```

First verification attempt:

```text
attempt_id = lf_no_python3_shim
exit_code = 1
status = DRIFT
passed_checks = Frozen SHA pins
failed_check = Banned keywords
failure_class = python3_missing_in_git_bash
lake_or_lean_reached = false
```

Temporary Python shim:

```text
shim_kind = reversible_temp_path_wrapper
shim_ref = temp:telos-pass0032-shim/python3
python_version = Python 3.12.10
shim_contents_hash = 191c4de6997d024bf5e53e99274285654c6ac05c66706054b5f8be29ba68476d
temp_write_performed = true
external_write_performed = false
```

Second verification attempt:

```text
attempt_id = lf_with_python3_shim
exit_code = 1
status = DRIFT
passed_checks = Frozen SHA pins, Banned keywords
failed_check = lake build
failure_class = lake_missing
lake_or_lean_reached = false
```

## Public Source Receipts

Verified public source receipts:

```text
elan README -> https://github.com/leanprover/elan
Lean reference manual -> https://lean-lang.org/doc/reference/latest/Build-Tools-and-Distribution/Managing-Toolchains-with-Elan/
Git config manual -> https://git-scm.com/docs/git-config
```

These sources support environment-management and line-ending claims only. They
do not support theorem correctness.

## Validator Result

```text
status = MATCH
lf_clone_eol_match_count = 3
python3_gate_status = RESOLVED_BY_REVERSIBLE_TEMP_SHIM
next_blocker = lake_missing
lake_build_status = UNVERIFIABLE_TOOL_UNAVAILABLE
lean_replay_status = UNVERIFIABLE_TOOL_UNAVAILABLE
negative_fixture_count = 10
```

## Negative Fixtures

All ten negative fixtures expect validator status `REJECT`:

```text
negative-lf-clone-not-required
negative-python3-shim-treated-as-system-install
negative-banned-keywords-promoted-without-shim
negative-lake-build-promoted-without-lake
negative-lean-replay-promoted
negative-source-environment-link-missing
negative-official-source-basis-missing
negative-external-write-hidden
negative-next-blocker-misidentified
negative-natural-law-promoted
```

## Tool Substrate Receipt

Gather docs receipt for packet 042:

```text
sha256 = 0a899851fff621770ffc2cc4c8141c00c45eb94f951a5c3bb21a2096cd3794da
seal = b5bf7a03332117d1d7019e10c44f6daa116bf2a473361bbcf8d9116ab1ed1ec3
chars = 7447
```

Index dogfood substrate map:

```text
root_sha256_prefix = f2f0af39219698a9
top_level_count = 39
```

Tool receipt status:

```text
schemas/tool-receipts-pass-0032.json
status = MATCH_WITH_FORUM_SUBMIT_GAP_AND_LAKE_REPLAY_GAP
```

Forum route:

```text
decided = null
confidence = 0.07954545454545454
needs_escalation = true
top_candidate = model-foundry
second_candidate = project-telos
```

Forum submit attempt:

```text
status = UNVERIFIABLE
error = submit needs a model executor
```

## Artifacts

| Artifact | Role |
| --- | --- |
| `tools/probe_lean_replay_remediation_contract.py` | Lean replay remediation contract generator. |
| `tools/validate_pass_0032_lean_replay_remediation.py` | Validator for LF clone, Python shim, Lake blocker, source receipts, non-promotion, and negative fixtures. |
| `fixtures/lean-replay-remediation-contract-pass-0032.json` | Remediation contract fixture. |
| `packets/042-lean-replay-remediation-contract.md` | Human-readable remediation contract packet. |
| `adversarial/pass-0032-lean-replay-remediation-steelman.md` | Local pass 0032 steelman. |
| `schemas/lean-replay-remediation-contract-pass-0032.json` | `LeanReplayRemediationContract/v1` artifact. |
| `schemas/pass-0032-lean-replay-remediation-validator-result.json` | Validator receipt for pass 0032. |
| `schemas/tool-receipts-pass-0032.json` | Compact Index, Gather, Shell, Telos, Forum, and Crucible receipts. |
| `crucible/pass-0032-thesis.json` | Falsifiable claims for the thirty-second pass. |
| `crucible/pass-0032-measurements.json` | Measurements/evidence for the thirty-second pass. |
| `crucible/pass-0032-report.md` | Crucible report for the thirty-second pass. |
| `crucible/pass-0032-run.json` | Crucible run record for the thirty-second pass. |

## Primary Next Push

Create a reversible Lean `v4.31.0` provisioning contract:

- prefer contained toolchain state over workstation-wide mutation;
- bind installer or archive hashes before execution;
- record PATH, `elan show`, `lean --version`, and `lake --version`;
- rerun `scripts/verify.sh --no-log --all` only after the Lake binary exists;
- keep theorem replay blocked until Lake build, axiom checks, and statement
  gates actually run.

## Natural-Law Promotion

Current promoted natural laws: none.
