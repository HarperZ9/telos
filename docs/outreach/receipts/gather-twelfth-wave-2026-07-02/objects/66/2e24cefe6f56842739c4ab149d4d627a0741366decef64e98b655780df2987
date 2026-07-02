# crucible report: Dogfood Pass 0011 Color Calibration Proof Kit

## Summary

- thesis_id: `0bf09ff1f6b62d9a`
- thesis_seal: `0bf09ff1f6b62d9a568696ae62b873d473dc01393429a085df20b497af4f9c3a`
- assessment_seal: `991f5f0ee6bb93270cbbde3df1cd9ce13fb032ddd9fbf135c823549ef39b8ea4`
- counts: MATCH 7 / DRIFT 0 / UNVERIFIABLE 0
- integrity: seals_ok=True, thesis_ok=True, verdicts_rederive=True

## Verdicts

| Claim | Status | Disposition | Margin | Method | Grounds |
| --- | --- | --- | ---: | --- | --- |
| Pass 0011 created an eight-row color calibration and rendering market map covering color-standard, color-management, calibration-software, grading-tool, open-source-calibration, and profile-standard categories. | MATCH | fenced | 1 | market-map-review | deviation 0 within tolerance 0.5 |
| Every pass 0011 market-map row includes an HTTPS source URL, proof receipt gap, Build Color wedge hypothesis, gap status, and confidence label. | MATCH | fenced | 1 | market-row-field-review | deviation 0 within tolerance 0.5 |
| Pass 0011 created a BuildColorCalibrationProofKit/v1 artifact with four Build Color software metrics, and each observed value is at or below its declared threshold. | MATCH | fenced | 1 | measurement-threshold-review | deviation 0 within tolerance 0.5 |
| The pass 0011 proof kit preserves a read-only calibration boundary: no hardware measurement, no display mutation, no ICC profile install, no LUT write, and no physical calibration claim. | MATCH | fenced | 1 | boundary-review | deviation 0 within tolerance 0.5 |
| The pass 0011 proof kit rejects the fake claim that this pass calibrated a physical display. | MATCH | fenced | 1 | negative-fixture-review | deviation 0 within tolerance 0.5 |
| The pass 0011 validator reports MATCH with two checks and zero drift. | MATCH | fenced | 1 | validator-run-review | deviation 0 within tolerance 0.5 |
| Pass 0011 promotes zero color science laws, physical calibration claims, display accuracy results, or other scientific discoveries. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |

## Measurement Evidence

| Claim | Method | Evidence |
| --- | --- | --- |
| Pass 0011 created an eight-row color calibration and rendering market map covering color-standard, color-management, calibration-software, grading-tool, open-source-calibration, and profile-standard categories. | market-map-review | schemas/color-calibration-market-map-pass-0011.json rows=8; category color-standard present; category color-management present; category calibration-software present; category grading-tool present; category open-source-calibration present; category profile-standard present |
| Every pass 0011 market-map row includes an HTTPS source URL, proof receipt gap, Build Color wedge hypothesis, gap status, and confidence label. | market-row-field-review | validator required_fields includes source_url; validator required_fields includes proof_receipt_gap; validator required_fields includes build_color_wedge_hypothesis; validator required_fields includes gap_status; validator required_fields includes confidence; validator rejects non-HTTPS source URLs; validator restricts gap_status to verified, inferred, or unverified |
| Pass 0011 created a BuildColorCalibrationProofKit/v1 artifact with four Build Color software metrics, and each observed value is at or below its declared threshold. | measurement-threshold-review | schemas/build-color-calibration-proof-kit-pass-0011.json schema=BuildColorCalibrationProofKit/v1; metric srgb_xyz_max_abs_error observed=0.0000017030280945010406 threshold=0.00001 status=PASS; metric srgb_oklab_max_abs_error observed=0.00000000000001072185665305766 threshold=0.0000000001 status=PASS; metric pq_max_abs_nits_error observed=0.00000000008458300726488233 threshold=0.000001 status=PASS; metric cie2000_pair_1_abs_error observed=0.00004031984342622863 threshold=0.005 status=PASS |
| The pass 0011 proof kit preserves a read-only calibration boundary: no hardware measurement, no display mutation, no ICC profile install, no LUT write, and no physical calibration claim. | boundary-review | hardware_measurement_used=false; display_state_mutated=false; icc_profile_installed=false; lut_written=false; physical_calibration_claim=false; boundary_status=PASS |
| The pass 0011 proof kit rejects the fake claim that this pass calibrated a physical display. | negative-fixture-review | negative_fixture.claim=This pass calibrated a physical display.; negative_fixture.status=REJECTED_BY_BOUNDARY; negative_fixture.reason=No meter, probe, display mutation, ICC install, or LUT write occurred. |
| The pass 0011 validator reports MATCH with two checks and zero drift. | validator-run-review | schemas/pass-0011-color-calibration-validator-result.json status=MATCH; match=2; drift=0; checks include ColorCalibrationMarketMap; checks include BuildColorCalibrationProofKit |
| Pass 0011 promotes zero color science laws, physical calibration claims, display accuracy results, or other scientific discoveries. | artifact-review | packets/021-color-calibration-proof-kit.md Non-Promotion Statement promotes no discovery; schemas/build-color-calibration-proof-kit-pass-0011.json promotion_state=PROOF_KIT_FIXTURE; failure_labels include NOT_A_PHYSICAL_CALIBRATION; failure_labels include NOT_A_NEW_COLOR_SCIENCE_LAW; negative fixture rejects the physical display calibration claim |
