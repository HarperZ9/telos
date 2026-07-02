# crucible report: Dogfood Pass 0148 Live Source Router Probes

## Summary

- thesis_id: `749dd0c505fa484d`
- thesis_seal: `749dd0c505fa484da8e095952a10320760ea30818384718c152605ca7bced29d`
- assessment_seal: `785a731aa7f15fcd56030925c1927c67c84db1394a9cfc5f070eb59d963442d2`
- counts: MATCH 5 / DRIFT 0 / UNVERIFIABLE 0
- integrity: seals_ok=True, thesis_ok=True, verdicts_rederive=True

## Verdicts

| Claim | Status | Disposition | Margin | Method | Grounds |
| --- | --- | --- | ---: | --- | --- |
| Pass 0148 created a LiveSourceRouterProbeReceipt/v1 artifact with status LIVE_SOURCE_ROUTER_PROBES_MATCH_WITH_WARNINGS and seal 6fa211ccd91517425f8a33ce9f32fd396dff00067ccbf1e13a328d25b8770944. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |
| Pass 0148 records 25 routes across 7 source families. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |
| Pass 0148 records 18 live query matches, 5 fallback matches, and 2 source-lead-only warnings. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |
| Pass 0148 rejects 10 negative fixtures. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |
| Pass 0148 promotes no theorem or natural law. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |

## Measurement Evidence

| Claim | Method | Evidence |
| --- | --- | --- |
| Pass 0148 created a LiveSourceRouterProbeReceipt/v1 artifact with status LIVE_SOURCE_ROUTER_PROBES_MATCH_WITH_WARNINGS and seal 6fa211ccd91517425f8a33ce9f32fd396dff00067ccbf1e13a328d25b8770944. | artifact-review | schema=LiveSourceRouterProbeReceipt/v1; status=LIVE_SOURCE_ROUTER_PROBES_MATCH_WITH_WARNINGS; seal=6fa211ccd91517425f8a33ce9f32fd396dff00067ccbf1e13a328d25b8770944 |
| Pass 0148 records 25 routes across 7 source families. | artifact-review | routes=25; families=7 |
| Pass 0148 records 18 live query matches, 5 fallback matches, and 2 source-lead-only warnings. | artifact-review | live=18; fallback=5; source_lead_only=2 |
| Pass 0148 rejects 10 negative fixtures. | artifact-review | negative_fixtures=10 |
| Pass 0148 promotes no theorem or natural law. | artifact-review | current_promoted_theorems=[]; current_promoted_natural_laws=[] |
