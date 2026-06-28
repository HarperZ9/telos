# Spec: SmallHarness External Fixture Pack Dogfood

## Objective
Create a tiny data-only fixture pack that SmallHarness can use as a dogfood case for external fixture loading, root-bounded path resolution, routing-only pack metadata, built-in fixture compatibility, and a minimal run receipt that is explicit about what is not captured yet.

## Requirements
- [x] Provide pack metadata with `packId`, `packVersion`, `workspaceRoot`, and fixture entries.
- [x] Keep pack and fixture files data-only: no commands, scripts, hooks, or executable setup fields.
- [x] Include at least one passing fixture, one structured failing fixture, and one rejected out-of-root fixture.
- [x] Include a minimal receipt fixture with deterministic cheap fields and explicit `notCapturedYet` entries.
- [x] Add a Node test that enforces root-bounded paths, data-only metadata, built-in compatibility, and receipt omissions.

## Technical Approach
Add a fixture pack under `demo/integrations/smallharness-dogfood-pack/` and a focused test at `demo/smallharness-fixture-pack.test.mjs`. The test will use the same resolver for fixture, workspace, and receipt paths and will assert that the deliberately escaping fixture is rejected.

## Files to Modify
- `demo/smallharness-fixture-pack.test.mjs` - validation test for the pack contract.
- `demo/integrations/smallharness-dogfood-pack/pack.json` - routing-only pack metadata.
- `demo/integrations/smallharness-dogfood-pack/fixtures/*.json` - data-only fixture examples.
- `demo/integrations/smallharness-dogfood-pack/receipts/*.json` - expected minimal receipt examples.

## Success Criteria
- [x] `node demo\smallharness-fixture-pack.test.mjs` fails before the pack exists.
- [x] `node demo\smallharness-fixture-pack.test.mjs` passes after pack files are added.
- [x] The fixture pack contains no executable command/hook/script fields.
- [x] Out-of-root fixture workspace resolution is detected as `path_escape_denied`.
- [x] `git diff --check` passes.

## Blockers
None identified.

## Status: IMPLEMENTED
