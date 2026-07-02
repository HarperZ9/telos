# crucible report: Project Telos Sixteenth-Wave Cyclic Summation-By-Parts Replay Claims

## Summary

- thesis_id: `f8e58b63d526fd6b`
- thesis_seal: `f8e58b63d526fd6bd233231992432a6341e21e7aa046fccf45d161434146a632`
- assessment_seal: `a4595b5b3e28a9cd9068724cfc1646052a999a292402dfb26c123bd9a860c054`
- counts: MATCH 6 / DRIFT 0 / UNVERIFIABLE 0
- integrity: seals_ok=True, thesis_ok=True, verdicts_rederive=True

## Verdicts

| Claim | Status | Disposition | Margin | Method | Grounds |
| --- | --- | --- | ---: | --- | --- |
| The sixteenth-wave package adds a bounded Lean cyclic summation-by-parts replay rung while keeping smooth periodic integration by parts NOT_REPLAYED and the parent Millennium problem UNVERIFIABLE. | MATCH | fenced | 1 | sixteenth-wave-package-boundary-review | deviation 0 within tolerance 0.5 |
| The sixteenth-wave theorem is stored in a separate Lean file and preserves the fourteenth-wave and fifteenth-wave source hashes. | MATCH | fenced | 1 | historical-receipt-stability-review | deviation 0 within tolerance 0.5 |
| CyclicSummationByPartsPreflight.lean compiles with Lean exit code 0 and replays lastPair, gradientOpen, divergenceInterior, cyclicGradientSum, cyclicDivergenceSum, open_summation_by_parts, and cyclic_summation_by_parts_cancels. | MATCH | fenced | 1 | lean-cyclic-sbp-replay-receipt-review | deviation 0 within tolerance 0.5 |
| The sixteenth-wave source refresh retains 13 arXiv metadata rows, 13 unique IDs, verifies both Gather stores as MATCH, and demotes the rows to SOURCE_LEAD_ONLY. | MATCH | fenced | 1 | source-lead-demotion-review | deviation 0 within tolerance 0.5 |
| The website copy and official-copy scaffold distinguish CYCLIC_SUMMATION_BY_PARTS_MATCH from NOT_REPLAYED smooth theorem claims. | MATCH | fenced | 1 | publication-surface-boundary-review | deviation 0 within tolerance 0.5 |
| The sixteenth-wave content queue includes explicit do-not-post boundaries for Navier-Stokes, smooth periodic integration by parts, source truth, exhaustive coverage, native BuildLang relation receipts, and accepted-publication claims. | MATCH | fenced | 1 | content-boundary-review | deviation 0 within tolerance 0.5 |

## Measurement Evidence

| Claim | Method | Evidence |
| --- | --- | --- |
| The sixteenth-wave package adds a bounded Lean cyclic summation-by-parts replay rung while keeping smooth periodic integration by parts NOT_REPLAYED and the parent Millennium problem UNVERIFIABLE. | sixteenth-wave-package-boundary-review | docs/outreach/SIXTEENTH-WAVE-CYCLIC-SUMMATION-BY-PARTS-REPLAY-2026-07-02.md exists; the package describes one kernel-checked cyclic summation-by-parts replay rung; the package states smooth periodic integration by parts is not replayed; the package states the parent Navier-Stokes Millennium problem remains UNVERIFIABLE |
| The sixteenth-wave theorem is stored in a separate Lean file and preserves the fourteenth-wave and fifteenth-wave source hashes. | historical-receipt-stability-review | docs/research/proof-packets/navier-stokes-periodic-skew-symmetry-v0/formal/lean/CyclicSummationByPartsPreflight.lean exists; PeriodicCancellationPreflight.lean retains SHA-256 77e5cba345adc1fd99003bfc17092750fddca1a9f879b4ac59f99e74c374a936; CyclicFiniteSumPreflight.lean retains SHA-256 e69d314e73710f8ab58e45f1fdf9f353777dfd51e70087ebc575c8913014e115; lean-cyclic-summation-by-parts replay receipt records both prior source hashes as preserved |
| CyclicSummationByPartsPreflight.lean compiles with Lean exit code 0 and replays lastPair, gradientOpen, divergenceInterior, cyclicGradientSum, cyclicDivergenceSum, open_summation_by_parts, and cyclic_summation_by_parts_cancels. | lean-cyclic-sbp-replay-receipt-review | docs/research/proof-packets/navier-stokes-periodic-skew-symmetry-v0/formal/lean/CyclicSummationByPartsPreflight.lean exists; docs/outreach/receipts/sixteenth-wave/lean-cyclic-summation-by-parts-replay-2026-07-02.json records exit_code 0; receipt records ProjectTelos.FormalReplay.lastPair; receipt records ProjectTelos.FormalReplay.gradientOpen; receipt records ProjectTelos.FormalReplay.divergenceInterior; receipt records ProjectTelos.FormalReplay.cyclicGradientSum; receipt records ProjectTelos.FormalReplay.cyclicDivergenceSum; receipt records ProjectTelos.FormalReplay.open_summation_by_parts; receipt records ProjectTelos.FormalReplay.cyclic_summation_by_parts_cancels; receipt records smooth_periodic_integration_by_parts NOT_REPLAYED |
| The sixteenth-wave source refresh retains 13 arXiv metadata rows, 13 unique IDs, verifies both Gather stores as MATCH, and demotes the rows to SOURCE_LEAD_ONLY. | source-lead-demotion-review | docs/outreach/receipts/sixteenth-wave/source-lead-demotion-gate.json exists; source-lead-demotion-gate records retained_rows 13; source-lead-demotion-gate records unique_arxiv_ids 13; source-lead-demotion-gate records all_store_verifications_match true; source-lead-demotion-gate verdict is SOURCE_LEAD_ONLY |
| The website copy and official-copy scaffold distinguish CYCLIC_SUMMATION_BY_PARTS_MATCH from NOT_REPLAYED smooth theorem claims. | publication-surface-boundary-review | research-formal-replay-preflight.html states CYCLIC_SUMMATION_BY_PARTS_MATCH for the finite paired-stencil theorem; research-formal-replay-preflight.html states continuous periodic integration by parts is NOT_REPLAYED; docs/research/official/FORMAL-REPLAY-PREFLIGHT-FOR-PDE-PACKETS-2026-07-02.md includes CYCLIC_SUMMATION_BY_PARTS_MATCH and NOT_REPLAYED terms |
| The sixteenth-wave content queue includes explicit do-not-post boundaries for Navier-Stokes, smooth periodic integration by parts, source truth, exhaustive coverage, native BuildLang relation receipts, and accepted-publication claims. | content-boundary-review | docs/outreach/SIXTEENTH-WAVE-CONTENT-QUEUE-2026-07-02.md exists; Do Not Post forbids Project Telos solved Navier-Stokes; Do Not Post forbids Lean proved smooth periodic integration by parts; Do Not Post forbids arXiv metadata proves paper truth; Do Not Post forbids latest/exhaustive coverage; Do Not Post forbids native BuildLang relation-invariant support; Do Not Post forbids website copy is submitted, accepted, or peer-reviewed |
