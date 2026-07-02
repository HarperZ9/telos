# crucible report: Navier-Stokes Periodic Energy Identity Bounded Subclaim

## Summary

- thesis_id: `1a771e171c3b7f52`
- thesis_seal: `1a771e171c3b7f527243c16057fb197efda05e6863f41730a7d054fc33963c35`
- assessment_seal: `c65b234f56f85720c1dc322c7c15f44bdc782f48ab0541f7e815d2e89e06ed06`
- counts: MATCH 3 / DRIFT 0 / UNVERIFIABLE 0
- integrity: seals_ok=True, thesis_ok=True, verdicts_rederive=True

## Verdicts

| Claim | Status | Disposition | Margin | Method | Grounds |
| --- | --- | --- | ---: | --- | --- |
| The Navier-Stokes periodic energy identity packet has a reference kernel receipt whose bounded Taylor-Green identity probe reports MATCH within declared tolerances. | MATCH | fenced | 1 | reference-kernel-run-receipt-review | deviation 0 within tolerance 0.5 |
| The Navier-Stokes periodic energy identity packet explicitly keeps the parent Navier-Stokes Millennium problem UNVERIFIABLE. | MATCH | fenced | 1 | grand-claim-boundary-review | deviation 0 within tolerance 0.5 |
| The packet includes negative boundaries that block promoting a finite grid or smooth-field identity check into a global regularity theorem. | MATCH | fenced | 1 | negative-boundary-review | deviation 0 within tolerance 0.5 |

## Measurement Evidence

| Claim | Method | Evidence |
| --- | --- | --- |
| The Navier-Stokes periodic energy identity packet has a reference kernel receipt whose bounded Taylor-Green identity probe reports MATCH within declared tolerances. | reference-kernel-run-receipt-review | docs/research/proof-packets/navier-stokes-periodic-energy-identity-v0/run.receipt.json exists; bounded_identity_probe is MATCH; energy_abs_error 1.8385293287792592e-13 <= 1e-10; dissipation_abs_error 7.460698725481052e-14 <= 1e-10; residual_numeric_abs 7.460698725481052e-14 <= 1e-10; max_divergence_abs 0 <= 1e-12 |
| The Navier-Stokes periodic energy identity packet explicitly keeps the parent Navier-Stokes Millennium problem UNVERIFIABLE. | grand-claim-boundary-review | run receipt parent_millennium_problem is UNVERIFIABLE; problem.statement.json grand_claim_status is UNVERIFIABLE; subclaim.energy_identity.md says it does not prove existence and smoothness for arbitrary Navier-Stokes solutions |
| The packet includes negative boundaries that block promoting a finite grid or smooth-field identity check into a global regularity theorem. | negative-boundary-review | problem.statement.json negative_boundaries include no grand-proof promotion; subclaim.energy_identity.md What This Does Not Prove section blocks global regularity and physical-simulator claims; run receipt boundaries block arbitrary simulation and physical-fluid validation claims |
