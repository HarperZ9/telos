# Sixth-Wave Live OSS Scout Demo

Date: 2026-07-02

Purpose: move the OSS Proof Showcase from fixture-only to a read-only live scout. The live GitHub query succeeded and produced current candidate intake, then the PR-readiness gate correctly blocked the handoff because no local reproduction, patch, passing test, or verifier evidence exists yet.

## Verified Results

| Segment | Evidence | Boundary |
| --- | --- | --- |
| Live scout | `node demo\showcase.mjs scout --query "repo:pandas-dev/pandas is:issue is:open label:Bug pd.array masked array" --limit 5 --json --out docs\outreach\receipts\sixth-wave\oss-showcase-live-scout` wrote `scout.json` with schema `project-telos.oss-scout/v1`, status `MATCH`, and 3 candidates. | Read-only GitHub CLI search only. It does not clone pandas, inspect source, run tests, or contact maintainers. |
| Top candidate | `oss-showcase-live-top-candidate.json` was generated from the first live scout candidate: `pandas-dev/pandas#63458`, priority `60`, updated `2026-06-27T23:25:33Z`. | Priority is a Telos scout heuristic. It is not a correctness, feasibility, or maintainer-interest claim. |
| Blocked readiness packet | `node demo\showcase.mjs record --candidate docs\outreach\receipts\sixth-wave\oss-showcase-live-top-candidate.json --evidence docs\outreach\receipts\sixth-wave\oss-showcase-live-blocked-evidence.json --now 2026-07-02T09:32:58.402Z --json` wrote `oss-showcase-live-blocked-packet.json` with `pr_ready: false`, `operator_next_action: revise`, verdict `UNVERIFIABLE`, and blockers for missing reproduction command, missing passing test evidence, non-`MATCH` verifier verdict, and missing patch summary. | This is the desired current state: live intake has not become a PR-ready claim. |
| Unit coverage | `node --test demo\showcase.test.mjs` passed. | Unit scope only. It covers the scout/record packet logic, not the pandas issue itself. |

## Artifact Map

| Artifact | Role |
| --- | --- |
| `docs/outreach/receipts/sixth-wave/oss-showcase-live-scout/scout.json` | Live read-only GitHub scout output. |
| `docs/outreach/receipts/sixth-wave/oss-showcase-live-top-candidate.json` | Generated candidate record for the top live scout result. |
| `docs/outreach/receipts/sixth-wave/oss-showcase-live-blocked-evidence.json` | Explicit missing-evidence record for the live candidate. |
| `docs/outreach/receipts/sixth-wave/oss-showcase-live-blocked-packet.json` | Generated blocked PR-readiness packet. |
| `docs/outreach/receipts/sixth-wave-tooling-thesis-2026-07-02.json` | Crucible thesis for this pass. |
| `docs/outreach/receipts/sixth-wave-tooling-measurements-2026-07-02.json` | Measurement rows for the thesis. |

## Re-run Commands

From `C:\dev\public\telos`:

```powershell
node demo\showcase.mjs scout --query "repo:pandas-dev/pandas is:issue is:open label:Bug pd.array masked array" --limit 5 --json --out docs\outreach\receipts\sixth-wave\oss-showcase-live-scout

node demo\showcase.mjs record --candidate docs\outreach\receipts\sixth-wave\oss-showcase-live-top-candidate.json --evidence docs\outreach\receipts\sixth-wave\oss-showcase-live-blocked-evidence.json --now 2026-07-02T09:32:58.402Z --json

node --test demo\showcase.test.mjs
```

Crucible package check:

```powershell
crucible run docs\outreach\receipts\sixth-wave-tooling-thesis-2026-07-02.json --measurements docs\outreach\receipts\sixth-wave-tooling-measurements-2026-07-02.json --out docs\outreach\receipts\sixth-wave-tooling-run-2026-07-02.json --report docs\outreach\receipts\sixth-wave-tooling-report-2026-07-02.md --json
```

## Public Post Angle

> The live OSS scout works now: Telos queried GitHub read-only, found current pandas candidates, ranked one, and then refused to call it PR-ready because no reproduction, patch, test, or verifier evidence exists. That is the loop we want for public work: intake can be live; readiness stays evidence-gated.

## Do Not Post

- Do not claim Project Telos fixed `pandas-dev/pandas#63458`.
- Do not claim the candidate is easy to fix.
- Do not claim maintainers want a PR.
- Do not claim repository stars, language, or open-issue counts from this scout; the current live-scout schema sets those fields to `0` or `unknown` because `gh search issues` did not provide them.
- Do not post a PR-ready claim until local reproduction, patch summary, passing tests, and a `MATCH` verifier verdict exist.
