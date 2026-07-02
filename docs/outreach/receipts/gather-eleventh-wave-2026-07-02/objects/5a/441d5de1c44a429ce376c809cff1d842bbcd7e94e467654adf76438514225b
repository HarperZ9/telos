# Pass 0033 Steelman: Lean Provisioning And Build Timeout

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

## Thesis Under Pressure

Pass 0033 claims that the replay environment advanced from `lake_missing` to a
contained Lean/Lake environment, and then stopped at a long-running Mathlib
dependency build. It does not claim build success or theorem replay.

## Strongest Objections

1. This pass did perform a toolchain install.

Correct. The claim is not "no install." The claim is "contained temp install."
The receipt records `ELAN_HOME=temp:telos-pass0033-elan-home`,
`--no-modify-path`, `normal_path_modified=false`, and
`external_write_performed=false`.

2. The install may still have used network and disk heavily.

Correct. It downloaded an Elan zip, installed Lean 4.31.0, and generated a
large partial `.lake` tree. The pass records archive hashes, toolchain versions,
3.20 GB of build artifacts, and a stop receipt.

3. `lake` being available is not the same as `lake build` passing.

Correct. This pass resolves the missing-binary gate only. The actual `lake
build` did not complete inside the bounded window.

4. The timeout could mask a later semantic error.

Correct. Since the build was stopped while compiling dependencies, no theorem or
project semantic verdict can be promoted. The status is
`TIMEOUT_TERMINATED`, not `DRIFT_SEMANTIC_FAILURE`.

5. Killing processes can corrupt the temporary build cache.

Correct. The partial `.lake` state is a cache candidate, not trusted proof
state. Any future pass that resumes from it must treat it as mutable build
state, re-run integrity checks, and produce fresh receipts.

6. The pass relies on a GitHub latest-release observation.

Correct. The artifact records the observed tag and downloaded asset hash on
2026-07-01. A future replay should prefer pinned release URLs and checksums over
unbounded "latest" resolution.

7. The elapsed time is not a portable performance benchmark.

Correct. It is workstation-context evidence only. It should not be used to claim
Mathlib build performance, cache strategy quality, or buyer value without a
controlled benchmark.

8. The temp toolchain is not a production reproducibility story.

Correct. Production should define cache roots, cleanup policy, storage budget,
network retry policy, binary provenance, and signature verification.

9. The build artifact snapshot does not prove all generated files are valid.

Correct. File counts and bytes prove side effects existed, not correctness.
Only successful build exits and post-build checks can promote validity.

10. The pass still has not reached the target theorem files.

Correct. It records worker command lines compiling Mathlib dependencies. It does
not claim the `Prob4b` files compiled.

## Fatal Tests For The Next Pass

The next pass should fail if it:

- treats the partial `.lake` tree as trusted proof state;
- skips dependency cache checks;
- promotes `lake build` success without exit code 0;
- promotes theorem replay without theorem-specific logs;
- leaves temp Lean/Lake worker processes running;
- omits disk footprint and timeout budget;
- hides network or temp writes;
- upgrades from "toolchain available" to "proof correct" without intervening
  gates.

## Product Implication

Pass 0033 shows the proof-packet stack needs a dedicated dependency-build layer.
Research proof packets should distinguish environment provisioning from
dependency hydration, dependency build, project build, and theorem replay. This
same shape applies to BuildLang/buildc, GPU kernels, color calibration,
scientific simulations, biology pipelines, and quant/security workflows.

## Verdict

Pass 0033 is strong evidence for contained provisioning and weak evidence for
the target proof. That boundary is the product.
