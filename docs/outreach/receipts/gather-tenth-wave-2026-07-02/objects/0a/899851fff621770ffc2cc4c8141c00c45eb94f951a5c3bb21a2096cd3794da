# Packet 042: Lean Replay Remediation Contract

Date: 2026-07-01

Status: `PROBE_MATCH_WITH_LAKE_GAP`

This pass advances the `pipeline-math` theorem replay chain by removing two
earlier environment blockers without installing a Lean toolchain or promoting a
theorem replay. It records the exact next blocker: `lake` is not available in
the current shell environment.

## Source Binding

Pass 0032 is bound to the pass 0031 environment contract:

```text
path = schemas/lean-replay-environment-contract-pass-0031.json
schema = LeanReplayEnvironmentContract/v1
sha256 = e10e07a409bf9a0cde7dcf8aae823b176b44a9b1610fcf133dc228b94219d3f1
seal = 4532f819ea8d8f7760323b2920d131b4909bedc05960ad3da553424e1f38a0bc
```

The pass 0031 contract identified a CRLF path-text failure before Lean or Lake
could run. Pass 0032 tests a non-mutating remediation path for that gate.

## Public Source Basis

Verified source receipts:

```text
source = elan README
url = https://github.com/leanprover/elan
claim = Elan manages Lean installations and places lean and lake binaries on PATH, selecting the version from lean-toolchain when needed.
verification_status = verified
```

```text
source = Lean reference manual
url = https://lean-lang.org/doc/reference/latest/Build-Tools-and-Distribution/Managing-Toolchains-with-Elan/
claim = Elan installs and runs Lean toolchains; projects can use lean-toolchain files to select a Lean version.
verification_status = verified
```

```text
source = Git config manual
url = https://git-scm.com/docs/git-config
claim = core.autocrlf=true converts working-directory text files to CRLF; core.eol is ignored when core.autocrlf is true or input.
verification_status = verified
```

Confidence: high for source existence and measured local command results; high
for local receipt hashes; moderate for market interpretation.

## Remediation Probe 1: LF Checkout

Command shape:

```text
git -c core.autocrlf=false clone --depth 1 https://github.com/Pengbinghui/pipeline-math.git temp:pipeline-math-pass0032-lf
```

Result:

```text
repo_commit = 69d7df765a8f377a5e0628c6d36c088bce7642c9
checkout_policy = core.autocrlf=false
status = MATCH
```

EOL probe:

```text
Prob4b/Defs.lean = i/lf w/lf
Prob4b/Theorems.lean = i/lf w/lf
scripts/frozen.sha256 = i/lf w/lf
```

Interpretation: the frozen SHA gate that failed in pass 0031 is resolved in a
temporary LF-preserving checkout. This does not modify the source repository and
does not prove the Lean files compile.

## Remediation Probe 2: Reversible Python3 Shim

Git Bash can find `python`, but not `python3`, in this workstation environment.
The verification script expects `python3`.

Temporary shim:

```text
shim_ref = temp:telos-pass0032-shim/python3
shim_kind = reversible_temp_path_wrapper
python3_resolution = temp:telos-pass0032-shim/python3
python_version = Python 3.12.10
shim_contents_hash = 191c4de6997d024bf5e53e99274285654c6ac05c66706054b5f8be29ba68476d
temp_write_performed = true
external_write_performed = false
status = MATCH
```

Interpretation: the Python naming gate is resolved with a reversible temporary
PATH wrapper. It is not a system install and must not be reported as one.

## Verification Attempts

Attempt 1: LF checkout without `python3` shim.

```text
attempt_id = lf_no_python3_shim
exit_code = 1
status = DRIFT
passed_checks = Frozen SHA pins
failed_check = Banned keywords
failure_class = python3_missing_in_git_bash
lake_or_lean_reached = false
```

Attempt 2: LF checkout with reversible `python3` shim.

```text
attempt_id = lf_with_python3_shim
exit_code = 1
status = DRIFT
passed_checks = Frozen SHA pins, Banned keywords
failed_check = lake build
failure_class = lake_missing
lake_or_lean_reached = false
```

Measured advancement:

```text
pass_0031_first_failed_check = Frozen SHA pins
pass_0032_attempt_1_first_failed_check = Banned keywords
pass_0032_attempt_2_first_failed_check = lake build
next_blocker = lake_missing
```

The chain progressed from line-ending failure to Python command-name failure to
missing Lake. Theorem replay remains blocked.

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
schema = LeanReplayRemediationContractFixture/v1
sha256 = 27da59a624c60468ebebcd3c19580933f66d82df3a5e289242b7b7351cef02f3
seal = 5bca5d4aa6b3c1b735da0c2e7a10bd1568194723e88781fa4f39955b5dafc08c
```

Validator:

```text
path = schemas/pass-0032-lean-replay-remediation-validator-result.json
status = MATCH
lf_clone_eol_match_count = 3
python3_gate_status = RESOLVED_BY_REVERSIBLE_TEMP_SHIM
next_blocker = lake_missing
lake_build_status = UNVERIFIABLE_TOOL_UNAVAILABLE
lean_replay_status = UNVERIFIABLE_TOOL_UNAVAILABLE
negative_fixture_count = 10
```

## Action Receipt Proposal

```text
schema = ActionReceiptLeanReplayRemediation/v1
action_id = act_dogfood_0032_lean_replay_remediation
event_id = evt_dogfood_0032_lean_replay_remediation
event_type = lean_replay_remediation_contract_created
authority_class = non_mutating_temp_remediation_probe
side_effect_class = temp_write
external_write_performed = false
toolchain_install_performed = false
replay_promotion_allowed = false
verification_verdict = MATCH
```

This is a concrete instance of the Telos action-receipt thesis: even failed
execution attempts can become durable product evidence when the receipt binds
inputs, exact command attempts, failure class, and non-promotion boundaries.

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

## Market Reading

The market-relevant capability is not "we ran Lean." The capability is:

```text
move a high-stakes research replay through reproducibility gates one by one,
record exact blockers, and prevent any downstream claim promotion until the
compiler/runtime/prover gates actually pass.
```

This is the same architecture needed for BuildLang/buildc, color calibration,
rendering, finance simulations, biology pipelines, robotics, quantum toolchains,
and AI/ML benchmarks. A proof-centered megatool should turn every blocked run
into a reusable environment contract rather than a lost terminal transcript.

## Next Action

The next pass should define and test a reversible Lean `v4.31.0` provisioning
path. It should prefer a contained toolchain location, hash every downloaded or
installed artifact, avoid mutating the operator workstation without an explicit
action receipt, and keep theorem replay blocked until `lake build`, axiom
checks, and statement gates actually run.

## Non-Promotion Boundary

This pass verifies a remediation sequence and the next environment blocker
only. It does not install Lean, does not run Lake successfully, does not replay
any theorem, does not prove correctness of `pipeline-math`, and does not promote
any natural law.

Current promoted natural laws: none.
