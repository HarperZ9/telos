# Packet 040: Theorem Replay Preflight

Date: 2026-07-01

Status: `PROBE_MATCH_WITH_TOOLCHAIN_GAP`

This pass moves the `pipeline-math` research claim packet one level closer to
real theorem replay. It does not verify the theorem. It verifies the replay
preconditions and records why this workstation cannot yet claim replay success.

## Source Repository

Public repository:

```text
https://github.com/Pengbinghui/pipeline-math.git
```

Clone receipt:

```text
commit = 69d7df765a8f377a5e0628c6d36c088bce7642c9
clone_method = git clone --depth 1
observed_on = 2026-07-01
lean_file_count = 66
formalization_project_count = 4
```

Formalization projects observed:

```text
lean/problem-20-formalization
lean/problem-27b-form
lean/problem-30c-formalization
lean/problem-4b-formalization
```

## Selected Project

Selected project:

```text
lean/problem-4b-formalization
```

Reason: Problem 4(b) includes a verification harness, frozen SHA pins, and ten
named solution theorems.

Toolchain pin:

```text
leanprover/lean4:v4.31.0
```

Named solution theorems:

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

## Frozen Pins

Frozen pin file:

```text
lean/problem-4b-formalization/scripts/frozen.sha256
```

Pinned Git blob hashes:

```text
Prob4b/Defs.lean = f596023b79726b87da05ccaf825e512bd17237f29a43df3ce31dc01c7646868a
Prob4b/Theorems.lean = cb80242d1bfd9e9b142e442dac9d0784081dabefbf7bd400dd0a27cd0e8bd3ae
```

The pins match Git blob bytes. The Windows working tree checked out those files
with CRLF line endings, producing different working-tree file hashes:

```text
Prob4b/Defs.lean = 4d3285bae57a53a42c33311745f5afdf6990d483cf0d1a0ffd796101a8051b2d
Prob4b/Theorems.lean = 70356618935d908762980a8dc0aead297f8d02a1ebdb997b5caaa1bfdfaa1b2e
```

Replay requirement:

```text
Use Git blob bytes, enforce LF checkout, or normalize before frozen SHA validation.
```

## Toolchain Probe

Available:

```text
git = MATCH
python = MATCH
```

Unavailable on PATH:

```text
bash = UNAVAILABLE
lake = UNAVAILABLE
lean = UNAVAILABLE
```

Replay verdict:

```text
lean_replay_status = UNVERIFIABLE_TOOL_UNAVAILABLE
replay_promotion_allowed = false
```

The provided `scripts/verify.sh --no-log --all` could not be run because
`bash` is unavailable. Lean/Lake replay could not be run because `lake` and
`lean` are unavailable.

## Primary Receipt

Receipt schema:

```text
TheoremReplayPreflightPacket/v1
```

Receipt:

```text
path = schemas/theorem-replay-preflight-pass-0030.json
status = THEOREM_REPLAY_PREFLIGHT_MATCH_WITH_TOOLCHAIN_GAP
seal = fb2428b6a7d960e44fe44768e1864d6fc524e99b9461b7fc64d08012f6760180
```

Fixture:

```text
path = fixtures/pipeline-math-problem4b-preflight-pass-0030.json
sha256 = 8164e622fcafc9a8220674530e7d64ff664dfdb298c564eadd9d5fd2fdb26624
seal = 87114d508a057eab4a4011b3670ae7a2844689fdd9bda1d2fca573ffb1dfccba
```

Validator:

```text
path = schemas/pass-0030-theorem-replay-preflight-validator-result.json
status = MATCH
repo_commit = 69d7df765a8f377a5e0628c6d36c088bce7642c9
formalization_project_count = 4
lean_file_count = 66
selected_theorem_count = 10
pin_matches_git_blob_bytes = true
pin_matches_windows_worktree_bytes = false
line_ending_drift_detected = true
missing_commands = bash, lake, lean
negative_fixture_count = 10
```

## Action Receipt Proposal

The pass defines `ActionReceiptTheoremReplayPreflight/v1`:

```text
action_id = act_dogfood_0030_theorem_replay_preflight
event_id = evt_dogfood_0030_theorem_replay_preflight
event_type = theorem_replay_preflight_created
authority_class = read_only_public_repo_preflight
external_write_performed = false
toolchain_install_performed = false
replay_promotion_allowed = false
verification_verdict = MATCH
```

## Negative Fixtures

All ten negative fixtures expect validator status `REJECT`:

```text
negative-lean-replay-promoted-without-lean
negative-lake-build-promoted-without-lake
negative-verify-script-promoted-without-bash
negative-frozen-pin-worktree-mismatch-ignored
negative-git-commit-missing
negative-theorem-names-missing
negative-toolchain-pin-missing
negative-source-packet-link-missing
negative-axiom-check-promoted
negative-natural-law-promoted
```

## Market Reading

This is a better wedge than a generic "AI proves math" claim. The buyer problem
is operational:

```text
Before trusting automated proof discovery, a lab needs exact source commit,
toolchain pin, file hashes, theorem names, build commands, axiom checks,
failure modes, and proof-promotion gates.
```

Telos can own that receipt layer across math, scientific computing, BuildLang,
compiler proofs, color/rendering measurements, and AI4Science experiments.

## Next Replay Requirements

To convert this preflight into theorem replay:

1. Provision `bash`, `elan`, `lake`, and Lean `v4.31.0` in an isolated
   environment.
2. Clone with LF-preserving checkout or validate frozen hashes from Git blob
   bytes.
3. Run `scripts/verify.sh --no-log --all` from
   `lean/problem-4b-formalization`.
4. Capture Lake build output, `#print axioms` output, statement-gate output,
   and exit code.
5. Bind completed replay logs through action receipts and Crucible
   measurements.

## Non-Promotion Boundary

This pass verifies theorem-replay preconditions only. It does not run Lean, does
not run Lake, does not prove any Problem 4(b) theorem, does not prove
`pipeline-math` proof correctness, and does not promote any natural law.

Current promoted natural laws: none.
