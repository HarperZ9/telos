# crucible report: Twenty-second-wave hyphal context benchmark packet

## Summary

- thesis_id: `7460fe9c785c7889`
- thesis_seal: `7460fe9c785c788964a197cbfc7f839ca77eca5aac0267a2c2a967dd37589c1c`
- assessment_seal: `ccfb0ee4c6033b28d7d13fe4d9d73da41263606eead2c0fbb9ef6191a4ee282b`
- counts: MATCH 3 / DRIFT 0 / UNVERIFIABLE 0
- integrity: seals_ok=True, thesis_ok=True, verdicts_rederive=True

## Verdicts

| Claim | Status | Disposition | Margin | Method | Grounds |
| --- | --- | --- | ---: | --- | --- |
| The hyphal context benchmark CLI emits HYPHAL_CONTEXT_FIXTURE_MATCH with equal required evidence-class recovery, equal guardrail recovery, and fewer estimated prompt tokens than the full-context route. | MATCH | publishable | 1 | hyphal-context-benchmark-cli | deviation 0 within tolerance 0.1 |
| The publication copy states the benchmark as one deterministic fixture and does not claim universal route superiority or measured model answer quality. | MATCH | publishable | 1 | benchmark-boundary-scan | deviation 0 within tolerance 0.1 |
| The benchmark receipt carries refs, hashes, coverage, and retrieval reasons without embedding raw source bodies or raw context. | MATCH | publishable | 1 | raw-payload-boundary-scan | deviation 0 within tolerance 0.1 |

## Measurement Evidence

| Claim | Method | Evidence |
| --- | --- | --- |
| The hyphal context benchmark CLI emits HYPHAL_CONTEXT_FIXTURE_MATCH with equal required evidence-class recovery, equal guardrail recovery, and fewer estimated prompt tokens than the full-context route. | hyphal-context-benchmark-cli | demo/hyphal-context-benchmark.mjs; demo/hyphal-context-benchmark.test.mjs; docs/outreach/receipts/twenty-second-wave/hyphal-context-benchmark-2026-07-02.json |
| The publication copy states the benchmark as one deterministic fixture and does not claim universal route superiority or measured model answer quality. | benchmark-boundary-scan | docs/research/whitepapers/HYPHAL-CONTEXT-BENCHMARK-FOR-RECEIPT-ROUTING-2026-07-02.md; docs/research/official/HYPHAL-CONTEXT-BENCHMARK-FOR-RECEIPT-ROUTING-2026-07-02.md; docs/outreach/TWENTY-SECOND-WAVE-HYPHAL-CONTEXT-BENCHMARK-2026-07-02.md |
| The benchmark receipt carries refs, hashes, coverage, and retrieval reasons without embedding raw source bodies or raw context. | raw-payload-boundary-scan | docs/outreach/receipts/twenty-second-wave/hyphal-context-benchmark-2026-07-02.json; demo/hyphal-context-benchmark.test.mjs |
