# Sixth-Wave Visibility Content Queue

Date: 2026-07-02

Use these after the fifth-wave fixture-first OSS posts. This queue is about the live read-only scout and the readiness gate staying blocked.

## Post 35: Live Scout

Short post:

> The OSS Proof Showcase is no longer fixture-only. A read-only GitHub scout query returned 3 current `pandas-dev/pandas` bug candidates. Top candidate in this run: `pandas-dev/pandas#63458`, priority `60`.

Evidence:

- `docs/outreach/SIXTH-WAVE-LIVE-OSS-SCOUT-2026-07-02.md`
- `docs/outreach/receipts/sixth-wave/oss-showcase-live-scout/scout.json`
- `node demo\showcase.mjs scout --query "repo:pandas-dev/pandas is:issue is:open label:Bug pd.array masked array" --limit 5 --json`

## Post 36: Intake Is Not Readiness

Short post:

> Live issue intake is useful, but it is not a PR. The top live candidate immediately becomes a blocked readiness packet until reproduction, patch, passing tests, and verifier evidence exist.

Evidence:

- `docs/outreach/receipts/sixth-wave/oss-showcase-live-top-candidate.json`
- `docs/outreach/receipts/sixth-wave/oss-showcase-live-blocked-evidence.json`
- `docs/outreach/receipts/sixth-wave/oss-showcase-live-blocked-packet.json`

## Post 37: Blockers Are Product Surface

Short post:

> The blocked packet names the missing work: reproduction command, passing test evidence, `MATCH` verifier verdict, and patch summary. That list is the product surface for contributors: here is what must be proven before anyone posts upstream.

Evidence:

- `docs/outreach/receipts/sixth-wave/oss-showcase-live-blocked-packet.json`
- `demo\showcase\record.mjs`
- `node --test demo\showcase.test.mjs`

## Post 38: Honest Live Boundary

Short post:

> The live scout reads GitHub issue metadata through `gh search issues`. It does not clone pandas, inspect code, run tests, contact maintainers, or infer repository stars/language/open-issue counts. That boundary is explicit in the sixth-wave docs.

Evidence:

- `docs/outreach/SIXTH-WAVE-LIVE-OSS-SCOUT-2026-07-02.md`
- `docs/outreach/receipts/sixth-wave/oss-showcase-live-scout/scout.json`

## Post 39: Growth Loop

Short post:

> The public growth loop is now visible: fixture scout -> live scout -> blocked readiness packet -> local reproduction -> patch -> tests -> Crucible -> operator-gated PR. Each step can have a receipt. Each missing step can block.

Evidence:

- `docs/outreach/FIFTH-WAVE-OSS-PROOF-SHOWCASE-2026-07-02.md`
- `docs/outreach/SIXTH-WAVE-LIVE-OSS-SCOUT-2026-07-02.md`
- `docs/outreach/receipts/sixth-wave-tooling-report-2026-07-02.md`

## Operating Rule

Never let "live candidate found" collapse into "PR ready." The next useful demo is a local reproduction packet for the top live candidate, not a public upstream claim.
