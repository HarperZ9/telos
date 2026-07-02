# Pass 0030 Adversarial Steelman

Date: 2026-07-01

## Strongest Objection

This pass still does not replay a theorem. It clones a repo, counts files,
extracts theorem names, checks hashes, and reports missing tools. A research
lab will ultimately need the actual Lean result, not a preflight.

## Response

Accepted. The pass is valuable only because it prevents a worse failure:

```text
claiming formal replay success when the environment cannot run bash, lake, or lean.
```

The line-ending finding is also material. The repository's frozen pins match
Git blob bytes, while the Windows working tree has CRLF hashes. A naive verifier
that hashes checked-out files on Windows would report false drift unless it
normalizes line endings or hashes Git blob bytes.

## Preserved Gaps

| Gap | Status |
| --- | --- |
| `scripts/verify.sh` execution | `UNVERIFIABLE_TOOL_UNAVAILABLE` because `bash` is unavailable. |
| `lake build` | `UNVERIFIABLE_TOOL_UNAVAILABLE` because `lake` is unavailable. |
| `lean --version` and theorem checks | `UNVERIFIABLE_TOOL_UNAVAILABLE` because `lean` is unavailable. |
| `#print axioms` output | Not run. |
| statement-gate compilation | Not run. |
| Problem 4(b) theorem correctness | Not proven by this pass. |

## What Would Falsify The Preflight

- The recorded commit does not match the cloned repository.
- The repo no longer has four Lean formalization projects at that commit.
- Problem 4(b) no longer has ten named solution theorems.
- The frozen pins do not match Git blob bytes.
- The validator allows replay promotion while `bash`, `lake`, or `lean` is
  unavailable.
- The packet omits the line-ending drift boundary.

## Product Implication

The proof-packet megatool must make preflight failure useful. A blocked theorem
replay is not a failure of the product; it is a correct artifact if it says:

```text
source found, theorem names found, hashes bound, toolchain absent, replay not promoted.
```

That same pattern transfers to BuildLang/buildc, color calibration, numerical
finance, quantum workflows, and wet-lab protocols: source and environment
readiness are separate from successful verification.

Current promoted natural laws: none.
