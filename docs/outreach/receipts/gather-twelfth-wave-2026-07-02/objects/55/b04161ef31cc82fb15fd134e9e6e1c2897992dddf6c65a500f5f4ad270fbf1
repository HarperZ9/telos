# Pass 0032 Steelman: Lean Replay Remediation Contract

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

## Thesis Under Pressure

Pass 0032 claims that two reproducibility gates were advanced without promoting
the theorem replay:

- an LF-preserving checkout resolves the frozen SHA pin failure;
- a reversible temporary `python3` shim resolves the Git Bash Python command
  naming failure;
- the next measured blocker is `lake_missing`;
- no theorem replay, Lake success, toolchain install, or natural law is
  promoted.

## Strongest Objections

1. The LF checkout is only a temporary clone.

The objection is correct. The pass does not claim the upstream repository, the
operator checkout, or any future workspace will remain LF-clean. It only claims
that `git -c core.autocrlf=false clone` produced LF working-tree files in the
temporary probe and that this allowed the verifier to pass the frozen SHA gate.

2. The Python shim is a workaround, not a dependency solution.

Correct. The shim proves command-name compatibility in Git Bash only. It is not
a system install, does not guarantee reproducibility on other machines, and must
be replaced by a declared replay environment contract before public demo use.

3. The failed `lake build` means the pass still has no theorem evidence.

Correct. Theorem replay remains `UNVERIFIABLE_TOOL_UNAVAILABLE`. Any claim that
Problem 4(b) was replayed, that Lake ran successfully, or that theorem names are
verified by Lean should be rejected.

4. The official source receipts are about environment management, not the
correctness of `pipeline-math`.

Correct. The external sources support environment assumptions about Elan, Lean
toolchain selection, and Git line endings. They do not validate theorem
correctness, proof completeness, or the authors' broad public claims.

5. A temporary write still changes local state.

Correct. The pass records `temp_write_performed=true` and
`external_write_performed=false`. A production action receipt should include
the temp path, cleanup policy, and hash of the shim contents.

6. `lake_missing` could hide earlier Lake/Lean configuration drift.

Correct. Since `lake` is not available, later gates are untested. The next pass
must avoid claiming anything about `lake build` warnings, Lean imports, theorem
statements, axioms, or proof replay until the binary is available and run logs
are captured.

7. The pass may overfit to Windows plus Git Bash.

Correct. This is a workstation-specific environment receipt. The product
lesson generalizes; the exact commands do not. A portable demo needs a matrix
for Windows Git Bash, Windows native PowerShell, WSL, Linux, and containerized
execution.

8. The replay chain still depends on public GitHub availability.

Correct. The pass records the observed repository commit and fixture hashes,
but a robust product path should mirror source archives, bind Git object hashes,
and make replay possible when the network is unavailable.

9. The market reading is interpretive.

Correct. It is a hypothesis: failed replay attempts are valuable product
evidence when typed, sealed, and connected to next actions. It is not market
proof until buyer interviews, demos, and competitive comparisons confirm it.

10. The negative fixtures are declared, not executed against a general-purpose
validator.

Partly correct. The pass-specific validator checks the declared rejection
conditions inside this artifact family. It is not yet a general adversarial
mutation harness. A later pass should auto-materialize mutated negative JSON and
prove that each mutation fails.

## Fatal Tests For The Next Pass

The next pass should be considered failed if it does any of the following:

- installs Lean or Elan without an explicit action receipt;
- records a system mutation as read-only;
- treats a temporary shim as a durable environment contract;
- claims `lake build` success without a captured exit code and log digest;
- claims theorem replay without theorem-specific Lean command evidence;
- omits source commit, file hashes, or replay environment hashes;
- skips axiom and statement checks after a successful build;
- hides any failed gate behind a generic "environment issue" label.

## Product Implication

This steelman reinforces the same architectural requirement across Telos,
BuildLang/buildc, color calibration, rendering, quant, biology, and AI/ML:
blocked runs must produce durable contracts. The failed run is not waste if it
names the gate precisely, records evidence, and prevents false promotion.

## Verdict

Pass 0032 is strong as an environment-remediation receipt and weak as theorem
evidence. That is the correct boundary.
