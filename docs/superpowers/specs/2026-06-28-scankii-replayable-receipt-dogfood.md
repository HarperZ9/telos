# Spec: scankii Replayable Receipt Dogfood

## Objective
Dogfood the scankii `feature/replayable-receipt` branch against a public synthetic corpus that exercises the three requested static-boundary cases: stdout/logging leak, network sink requiring runtime witness, and unresolved/cross-modal boundary. Preserve the result as a Telos-side receipt artifact without scanning private skills or workstation data.

## Requirements
- [x] Create a public synthetic skill corpus under `demo/integrations/scankii-synthetic-corpus/`.
- [x] Include stdout/logging, network sink, and unresolved/cross-modal boundary cases.
- [x] Run scankii from `ashp15205/scankii@feature/replayable-receipt` in an isolated temp environment.
- [x] Save the scanner JSON output as `demo/integrations/scankii-synthetic-receipt.json`.
- [x] Add a Node verifier that checks replayable receipt fields: scanner version, file hash, fragment hash, static observation flag, runtime-witness flag, unverifiable boundary flag, and containment recommendation.
- [x] Record any field-shape drift explicitly rather than claiming full fit.

## Technical Approach
The test will inspect the generated scankii JSON flexibly enough to tolerate a top-level list or a `findings` list, but strictly enough to require stable replay fields on every finding. The corpus stays synthetic and public. The scanner is run from a temp venv outside the repository; only the corpus, generated public receipt, verifier, and spec are committed.

## Files to Modify
- `demo/scankii-replayable-receipt.test.mjs` - receipt-output verifier.
- `demo/integrations/scankii-synthetic-corpus/**` - synthetic skill corpus.
- `demo/integrations/scankii-synthetic-receipt.json` - generated scanner output.
- `demo/integrations/README.md` - note the fixture.

## Success Criteria
- [x] `node demo\scankii-replayable-receipt.test.mjs` fails before scanner output exists.
- [x] scankii installs and runs from `feature/replayable-receipt` against only the synthetic corpus.
- [x] `node demo\scankii-replayable-receipt.test.mjs` passes against the generated scanner output, or records explicit field-shape drift if it cannot.
- [x] Adjacent Telos fixture tests continue to pass.
- [x] `git diff --check` passes.

## Observed Drift

- `pip install git+https://github.com/ashp15205/scankii.git@feature/replayable-receipt` failed on Windows because the branch contains a `.cursorrules ` path with a trailing space.
- Installing from a raw-file export of the package subset worked, but the wheel excluded `rules/*.yaml`; the temp venv needed rules copied beside `site-packages`.
- The synthetic corpus produced three NL findings with replay fields, but AST sink correlation did not fire for the synthetic Python sink snippets.
- Raw scankii output included absolute Windows paths and bare hash hex strings; the committed Telos receipt normalizes paths and prefixes hashes with `sha256:`.

## Blockers
None identified.

## Status: IMPLEMENTED_DRIFT_RECORDED
