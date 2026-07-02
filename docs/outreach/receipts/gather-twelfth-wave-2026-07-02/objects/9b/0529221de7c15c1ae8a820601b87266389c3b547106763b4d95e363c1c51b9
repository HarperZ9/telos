# Seventh-Wave Issue Detail And Reproduction Lead Demo

Date: 2026-07-02

Purpose: deepen the sixth-wave live scout from issue metadata into issue-detail evidence without crossing the line into a local reproduction claim. The GitHub issue body for `pandas-dev/pandas#63458` was captured, summarized, and converted into a reproduction-lead packet. The readiness gate still blocks because the reproduction command has not been executed locally and no patch or passing test exists.

## Verified Results

| Segment | Evidence | Boundary |
| --- | --- | --- |
| Issue detail capture | `gh issue view 63458 --repo pandas-dev/pandas --json number,title,url,state,body,author,labels,comments,createdAt,updatedAt` succeeded and wrote `oss-showcase-live-issue-63458-gh.json`; `oss-showcase-live-issue-63458-capture.json` records status `MATCH`. | Public GitHub issue detail only. It does not clone the repo, inspect source, run the issue body, or prove the report is valid on current main. |
| Issue summary | `oss-showcase-live-issue-63458-summary.json` records issue `63458`, state `OPEN`, labels `Bug`, `API - Consistency`, `Arrow`, comments count `11`, updated `2026-06-27T23:25:33Z`, body length `2963`, 4 code fences, and `has_reproduction_lead: true`. | Summary is derived from the captured issue body and hashes the body. It does not include a local execution result. |
| Readiness gate improvement | `demo\showcase\record.mjs` now requires reproduction evidence status `failed-before-patch`; `node --test demo\showcase.test.mjs` covers the `status: not-run` case. | This is a local gate improvement. It does not verify pandas behavior. |
| Reproduction-lead packet | `oss-showcase-live-reproduction-lead-blocked-packet.json` returns `pr_ready: false`, `operator_next_action: revise`, verdict `UNVERIFIABLE`, and blockers `missing failing reproduction evidence`, `missing passing test evidence`, `crucible verdict is not MATCH`, and `missing patch summary`. | The packet has an issue-authored reproduction command, but it was not executed. |

## Artifact Map

| Artifact | Role |
| --- | --- |
| `docs/outreach/receipts/seventh-wave/oss-showcase-live-issue-63458-gh.json` | Raw public GitHub issue-detail JSON captured by `gh issue view`. |
| `docs/outreach/receipts/seventh-wave/oss-showcase-live-issue-63458-capture.json` | Command capture receipt with status and summary hashes. |
| `docs/outreach/receipts/seventh-wave/oss-showcase-live-issue-63458-summary.json` | Derived issue-detail summary with body hash and boundary flags. |
| `docs/outreach/receipts/seventh-wave/oss-showcase-live-reproduction-lead-evidence.json` | Evidence packet containing the issue-authored reproduction lead with `status: not-run`. |
| `docs/outreach/receipts/seventh-wave/oss-showcase-live-reproduction-lead-blocked-packet.json` | Generated blocked PR-readiness packet. |
| `docs/outreach/receipts/seventh-wave-tooling-thesis-2026-07-02.json` | Crucible thesis for this pass. |
| `docs/outreach/receipts/seventh-wave-tooling-measurements-2026-07-02.json` | Measurement rows for the thesis. |

## Re-run Commands

From `C:\dev\public\telos`:

```powershell
gh issue view 63458 --repo pandas-dev/pandas --json number,title,url,state,body,author,labels,comments,createdAt,updatedAt

node demo\showcase.mjs record --candidate docs\outreach\receipts\sixth-wave\oss-showcase-live-top-candidate.json --evidence docs\outreach\receipts\seventh-wave\oss-showcase-live-reproduction-lead-evidence.json --now 2026-07-02T00:00:00Z --json

node --test demo\showcase.test.mjs
```

Crucible package check:

```powershell
crucible run docs\outreach\receipts\seventh-wave-tooling-thesis-2026-07-02.json --measurements docs\outreach\receipts\seventh-wave-tooling-measurements-2026-07-02.json --out docs\outreach\receipts\seventh-wave-tooling-run-2026-07-02.json --report docs\outreach\receipts\seventh-wave-tooling-report-2026-07-02.md --json
```

## Public Post Angle

> The next OSS proof step is issue-detail capture, not a patch claim. Telos captured the issue body for the top live candidate, found an issue-authored reproduction lead, and still blocked readiness because the command has not been run locally. The gate now requires failing reproduction evidence, not just a command string.

## Do Not Post

- Do not claim Project Telos reproduced `pandas-dev/pandas#63458`.
- Do not claim pandas source was inspected.
- Do not claim a patch exists.
- Do not claim tests passed.
- Do not claim the issue is valid on current pandas main.
- Do not paste the full issue body as outreach copy; cite the summary, hash, and raw receipt path instead.
