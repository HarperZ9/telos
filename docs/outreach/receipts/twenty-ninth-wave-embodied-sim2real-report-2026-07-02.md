# crucible report: Twenty-ninth-wave embodied sim-to-real preflight

## Summary

- thesis_id: `5b1c52ca9000ef30`
- thesis_seal: `5b1c52ca9000ef305a84e2f46f45a5b310585b9f65f75c1bf1eef90e3e66f756`
- assessment_seal: `32d76f695ad10049d4503afec8176e550499b17ad4aa01847fc2ca417c7e34d1`
- counts: MATCH 3 / DRIFT 0 / UNVERIFIABLE 0
- integrity: seals_ok=True, thesis_ok=True, verdicts_rederive=True

## Verdicts

| Claim | Status | Disposition | Margin | Method | Grounds |
| --- | --- | --- | ---: | --- | --- |
| The embodied sim-to-real fixture emits EMBODIED_SIM2REAL_FIXTURE_MATCH, satisfies the nominal trajectory, safety, latency, and unit checks, and rejects the configured negative controls. | MATCH | publishable | 1 | embodied-sim2real-fixture-replay | deviation 0 within tolerance 0.1 |
| The embodied source ledger stores arXiv metadata and digest receipts as source leads rather than promoted robotics, medical, safety, foundation-model, or sim-to-real claims. | MATCH | publishable | 1 | source-ledger-boundary-scan | deviation 0 within tolerance 0.1 |
| The publication copy labels the preflight as a local deterministic fixture and blocks real robot safety, surgical/medical, VLA/foundation-model, sim-to-real-at-scale, and BuildLang/buildc-native runtime claims for this pass. | MATCH | publishable | 1 | claim-boundary-copy-scan | deviation 0 within tolerance 0.1 |

## Measurement Evidence

| Claim | Method | Evidence |
| --- | --- | --- |
| The embodied sim-to-real fixture emits EMBODIED_SIM2REAL_FIXTURE_MATCH, satisfies the nominal trajectory, safety, latency, and unit checks, and rejects the configured negative controls. | embodied-sim2real-fixture-replay | demo/embodied-sim2real-proof-packet.mjs; demo/embodied-sim2real-proof-packet.test.mjs; docs/outreach/receipts/twenty-ninth-wave/embodied-sim2real-proof-packet-2026-07-02.json |
| The embodied source ledger stores arXiv metadata and digest receipts as source leads rather than promoted robotics, medical, safety, foundation-model, or sim-to-real claims. | source-ledger-boundary-scan | demo/research/embodied-sim2real-source-receipts.json; docs/research/whitepapers/EMBODIED-SIM2REAL-PROOF-PACKETS-FOR-ROBOTICS-2026-07-02.md |
| The publication copy labels the preflight as a local deterministic fixture and blocks real robot safety, surgical/medical, VLA/foundation-model, sim-to-real-at-scale, and BuildLang/buildc-native runtime claims for this pass. | claim-boundary-copy-scan | docs/outreach/TWENTY-NINTH-WAVE-EMBODIED-SIM2REAL-PREFLIGHT-2026-07-02.md; docs/research/official/EMBODIED-SIM2REAL-PROOF-PACKETS-FOR-ROBOTICS-2026-07-02.md; docs/research/whitepapers/EMBODIED-SIM2REAL-PROOF-PACKETS-FOR-ROBOTICS-2026-07-02.md |
