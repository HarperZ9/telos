# crucible report: Project Telos Fourteenth-Wave Lean Replay Rung Claims

## Summary

- thesis_id: `ea2bedc8d7bed33e`
- thesis_seal: `ea2bedc8d7bed33e02bf0627ea639ffa15f96b054704465037531c4081202fd7`
- assessment_seal: `110fc5ae33f1128a9036e3704af1fd6aeccaaeecf5fd991cc16f3cd65e3a6f54`
- counts: MATCH 6 / DRIFT 0 / UNVERIFIABLE 0
- integrity: seals_ok=True, thesis_ok=True, verdicts_rederive=True

## Verdicts

| Claim | Status | Disposition | Margin | Method | Grounds |
| --- | --- | --- | ---: | --- | --- |
| The fourteenth-wave package adds a bounded Lean replay rung for the Navier-Stokes periodic skew-symmetry proof packet while keeping the continuous periodic integration-by-parts theorem NOT_REPLAYED and the parent Millennium problem UNVERIFIABLE. | MATCH | fenced | 1 | fourteenth-wave-package-boundary-review | deviation 0 within tolerance 0.5 |
| Elan, Lean, and Lake are available by explicit path in this shell, and the package does not claim globally stable PATH availability. | MATCH | fenced | 1 | explicit-path-toolchain-review | deviation 0 within tolerance 0.5 |
| PeriodicCancellationPreflight.lean compiles with Lean exit code 0 and replays two integer algebraic cancellation lemmas. | MATCH | fenced | 1 | lean-replay-receipt-review | deviation 0 within tolerance 0.5 |
| The fourteenth-wave source refresh retains 20 arXiv metadata rows, 16 unique IDs, verifies all three Gather stores as MATCH, and demotes the rows to SOURCE_LEAD_ONLY. | MATCH | fenced | 1 | source-lead-demotion-review | deviation 0 within tolerance 0.5 |
| The website copy, official-copy scaffold, handoff, and revision queue distinguish LEAN_REPLAY_MATCH from NOT_REPLAYED continuous theorem claims. | MATCH | fenced | 1 | publication-surface-boundary-review | deviation 0 within tolerance 0.5 |
| The fourteenth-wave content queue includes explicit do-not-post boundaries for Navier-Stokes, continuous PDE replay, source truth, exhaustive coverage, native BuildLang relation receipts, and global Lean PATH claims. | MATCH | fenced | 1 | content-boundary-review | deviation 0 within tolerance 0.5 |

## Measurement Evidence

| Claim | Method | Evidence |
| --- | --- | --- |
| The fourteenth-wave package adds a bounded Lean replay rung for the Navier-Stokes periodic skew-symmetry proof packet while keeping the continuous periodic integration-by-parts theorem NOT_REPLAYED and the parent Millennium problem UNVERIFIABLE. | fourteenth-wave-package-boundary-review | docs/outreach/FOURTEENTH-WAVE-LEAN-REPLAY-RUNG-2026-07-02.md exists; the package describes one kernel-checked Lean algebraic cancellation rung; the package states the continuous periodic integration-by-parts theorem is NOT_REPLAYED; the package states the parent Navier-Stokes Millennium problem remains UNVERIFIABLE |
| Elan, Lean, and Lake are available by explicit path in this shell, and the package does not claim globally stable PATH availability. | explicit-path-toolchain-review | lean-periodic-cancellation-replay receipt records elan 4.2.3; lean-periodic-cancellation-replay receipt records Lean 4.31.0; lean-periodic-cancellation-replay receipt records Lake 5.0.0; fourteenth-wave package says explicit path works and does not claim globally stable PATH setup |
| PeriodicCancellationPreflight.lean compiles with Lean exit code 0 and replays two integer algebraic cancellation lemmas. | lean-replay-receipt-review | docs/research/proof-packets/navier-stokes-periodic-skew-symmetry-v0/formal/lean/PeriodicCancellationPreflight.lean exists; docs/outreach/receipts/fourteenth-wave/lean-periodic-cancellation-replay-2026-07-02.json records exit_code 0; receipt records ProjectTelos.FormalReplay.opposite_face_flux_cancels; receipt records ProjectTelos.FormalReplay.two_cell_periodic_flux_stencil_cancels; receipt records continuous_periodic_integration_by_parts NOT_REPLAYED |
| The fourteenth-wave source refresh retains 20 arXiv metadata rows, 16 unique IDs, verifies all three Gather stores as MATCH, and demotes the rows to SOURCE_LEAD_ONLY. | source-lead-demotion-review | docs/outreach/receipts/fourteenth-wave/source-lead-demotion-gate.json exists; source-lead-demotion-gate records retained_rows 20; source-lead-demotion-gate records unique_arxiv_ids 16; source-lead-demotion-gate records all_store_verifications_match true; source-lead-demotion-gate verdict is SOURCE_LEAD_ONLY |
| The website copy, official-copy scaffold, handoff, and revision queue distinguish LEAN_REPLAY_MATCH from NOT_REPLAYED continuous theorem claims. | publication-surface-boundary-review | research-formal-replay-preflight.html states LEAN_REPLAY_MATCH for the algebraic rung; research-formal-replay-preflight.html states the continuous theorem is NOT_REPLAYED; docs/research/official/FORMAL-REPLAY-PREFLIGHT-FOR-PDE-PACKETS-2026-07-02.md includes LEAN_REPLAY_MATCH and NOT_REPLAYED terms; docs/outreach/PARALLEL-CODEX-HANDOFF-2026-07-02.md includes the fourteenth-wave Lean boundary; docs/research/whitepapers/OFFICIAL-PAPER-REVISION-QUEUE-2026-07-02.md includes the fourteenth-wave Lean boundary |
| The fourteenth-wave content queue includes explicit do-not-post boundaries for Navier-Stokes, continuous PDE replay, source truth, exhaustive coverage, native BuildLang relation receipts, and global Lean PATH claims. | content-boundary-review | docs/outreach/FOURTEENTH-WAVE-CONTENT-QUEUE-2026-07-02.md exists; Do Not Post forbids Project Telos solved Navier-Stokes; Do Not Post forbids Lean proved the continuous PDE theorem; Do Not Post forbids arXiv rows prove paper claims; Do Not Post forbids latest/exhaustive coverage; Do Not Post forbids native BuildLang relation-invariant support; Do Not Post forbids Lean globally available on PATH |
