# Spec: ATP v1.2.0 Adapter Validation Fixture

## Objective
Add a public/synthetic Telos validation fixture for the Haystack ATP v1.2.0 feedback loop. The fixture should test whether ATP-style transaction receipts can preserve Telos workflow evidence without claiming production readiness, signing, anchoring, or backend integration.

## Requirements
- [x] Record current source evidence for ATP v1.2.0 branch, transaction spec, and examples.
- [x] Cover gather-style intake, index-style workspace map, forum-style action, verdict/unverifiable boundary, and append-only compensation.
- [x] Require digest refs instead of raw payloads for inputs/materials/evidence.
- [x] Keep policy decision separate from verification verdict.
- [x] Assert side-effect class, component version, config hash, typed stop reason, and verification verdict.
- [x] Assert compensation is a new event with `compensates`, while the original completed action remains immutable.
- [x] Include negative cases for mutation rollback, missing digest, missing verdict, collapsed policy/verdict, and untyped stop reason.

## Technical Approach
Create `demo/integrations/atp-adapter-validation.json` and `demo/atp-adapter-validation.test.mjs`. The test will validate the fixture as a Telos-side adapter profile, not as a formal ATP schema implementation. Public outreach can then report the exact fixture cases and tests run.

## Files to Modify
- `demo/atp-adapter-validation.test.mjs` - validation test for the synthetic ATP adapter profile.
- `demo/integrations/atp-adapter-validation.json` - source-backed fixture profile and cases.
- `demo/integrations/README.md` - mention the new fixture.

## Success Criteria
- [x] `node demo\atp-adapter-validation.test.mjs` fails before the fixture exists.
- [x] `node demo\atp-adapter-validation.test.mjs` passes after adding the fixture.
- [x] Adjacent tests continue to pass.
- [x] `git diff --check` passes.

## Blockers
None identified.

## Status: IMPLEMENTED
