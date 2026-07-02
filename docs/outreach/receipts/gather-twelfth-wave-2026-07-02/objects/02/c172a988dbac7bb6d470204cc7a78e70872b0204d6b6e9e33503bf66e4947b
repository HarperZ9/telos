# Third-Wave Visibility Content Queue

Date: 2026-07-02

Use these after posts 13-19. They are based on the closed-loop BuildLang -> proof packet -> Learn -> Build Color/Telos measurement pass.

## Post 20: Compiler Receipt To Lesson

Short post:

> A BuildLang receipt can become a Learn prooflesson without becoming an answer dump. Current local loop: `hello.bld` checks under `ci-review`, the receipt verifies, a Telos proof packet binds source + receipt hashes, and Learn re-verifies the lesson receipt as `VERIFIED`.

Evidence:

- `docs/outreach/THIRD-WAVE-CLOSED-LOOP-DEMO-2026-07-02.md`
- `docs/outreach/receipts/third-wave/buildlang-hello-ci-review-receipt.json`
- `docs/outreach/receipts/third-wave/tutor/buildlang-hello.prooflesson.json`

## Post 21: Policy-Pinned BuildLang

Short post:

> The useful compiler demo is not just "it ran." It is "it ran under a named policy." `buildc receipt verify` checks schema, compiler version, source digest, input graph digest, `ci-review` profile, effect rows, observed capabilities, diagnostics, policy status, and violations.

Evidence:

- `buildc receipt verify <receipt> --source examples\quickstart\hello.bld --expect-profile ci-review --json`

## Post 22: Build Color As Visible Proof Lane

Short post:

> Build Color is a strong public proof lane because the outputs are numeric and inspectable: color spaces, Delta E, tone/gamut assumptions, and known boundaries. Current local checkout: 1.0.2, CLI commands working, 458 tests passing.

Evidence:

- `docs/outreach/receipts/third-wave/build-color-cli-measurement.json`
- `python -m pytest tests -q`

## Post 23: Read-Only Display Calibration

Short post:

> The right first display-calibration demo is read-only. Telos can package targets, patch sets, artifact types, measurement gates, and failure codes before touching hardware. Current contract: hardware mutation disabled, 3 targets, 4 patch sets, 5 artifact types.

Evidence:

- `node demo\display-calibration.mjs --summary`
- `demo/integrations/display-calibration.json`

## Post 24: Measurement Bus

Short post:

> Telos measurement packets are not only for color. The current measurement bus has 10 layers: visual histogram, dither spectrum, splat probe, light clusters, audio spectrum, temporal flicker, geometry curvature, interaction trace, uncertainty budget, and performance budget.

Evidence:

- `node demo\measurement-layers.mjs --summary`
- `node --test demo\measurement-layers.test.mjs`

## Post 25: The Reusable Pattern

Short post:

> The reusable Telos pattern is: source -> receipt -> proof packet -> lesson -> measurement -> external verification -> outreach packet. That path scales across math, physics, biology, robotics, finance, security, and visual systems only if each step keeps its own boundary.

Evidence:

- `docs/outreach/THIRD-WAVE-CLOSED-LOOP-DEMO-2026-07-02.md`

## Operating Rule

Do not post any number from this queue without rerunning the associated command or citing the generated artifact from the same posting session.
