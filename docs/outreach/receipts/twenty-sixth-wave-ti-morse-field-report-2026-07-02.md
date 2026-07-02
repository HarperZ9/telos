# crucible report: Twenty-sixth-wave TI Morse field intake packet

## Summary

- thesis_id: `8324b46cc2d915a0`
- thesis_seal: `8324b46cc2d915a0f359e0fcb1912370d38bd11692154fe3f3d46b2a7149c559`
- assessment_seal: `8a19992119728a4db0a20c22fd99a60c4b0c5e99da8a9421e57e9191d0517cc3`
- counts: MATCH 3 / DRIFT 0 / UNVERIFIABLE 0
- integrity: seals_ok=True, thesis_ok=True, verdicts_rederive=True

## Verdicts

| Claim | Status | Disposition | Margin | Method | Grounds |
| --- | --- | --- | ---: | --- | --- |
| The TI Morse field intake ledger records the five requested YouTube videos with metadata and transcript receipts and one bounded channel-list snapshot. | MATCH | publishable | 1 | youtube-field-ledger-shape-test | deviation 0 within tolerance 0.1 |
| The publication copy labels field lanes as inferred and domain claims as unverifiable until primary-source or replay evidence exists. | MATCH | publishable | 1 | claim-boundary-copy-scan | deviation 0 within tolerance 0.1 |
| The tracked ledger stores receipt fields only and does not embed raw transcript bodies, raw video, or channel descriptions. | MATCH | publishable | 1 | raw-payload-boundary-scan | deviation 0 within tolerance 0.1 |

## Measurement Evidence

| Claim | Method | Evidence |
| --- | --- | --- |
| The TI Morse field intake ledger records the five requested YouTube videos with metadata and transcript receipts and one bounded channel-list snapshot. | youtube-field-ledger-shape-test | demo/research/youtube-ti-morse-field-receipts.json; demo/youtube-research-receipts.test.mjs |
| The publication copy labels field lanes as inferred and domain claims as unverifiable until primary-source or replay evidence exists. | claim-boundary-copy-scan | docs/outreach/TWENTY-SIXTH-WAVE-TI-MORSE-FIELD-INTAKE-2026-07-02.md; docs/research/whitepapers/TI-MORSE-FIELD-SCOPE-INTEGRATION-2026-07-02.md; docs/research/official/TI-MORSE-FIELD-SCOPE-INTEGRATION-2026-07-02.md |
| The tracked ledger stores receipt fields only and does not embed raw transcript bodies, raw video, or channel descriptions. | raw-payload-boundary-scan | demo/research/youtube-ti-morse-field-receipts.json; demo/youtube-research-receipts.test.mjs |
