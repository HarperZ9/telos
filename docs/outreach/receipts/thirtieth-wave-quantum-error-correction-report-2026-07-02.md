# crucible report: Thirtieth-wave quantum error-correction preflight

## Summary

- thesis_id: `9d1d8e89d9fa0735`
- thesis_seal: `9d1d8e89d9fa07350fbb4ae983f504da601b168153a5fcc947fae241f6bc8ea4`
- assessment_seal: `28839fe8adda04f277030e8d238e92122b9c8ea5db89afe88b7bdf6834c0a21c`
- counts: MATCH 3 / DRIFT 0 / UNVERIFIABLE 0
- integrity: seals_ok=True, thesis_ok=True, verdicts_rederive=True

## Verdicts

| Claim | Status | Disposition | Margin | Method | Grounds |
| --- | --- | --- | ---: | --- | --- |
| The QEC fixture emits QEC_STABILIZER_FIXTURE_MATCH, corrects no-error and single Pauli-X errors for both logical basis states, and rejects or marks unverifiable the configured negative controls. | MATCH | publishable | 1 | qec-stabilizer-fixture-replay | deviation 0 within tolerance 0.1 |
| The quantum source ledger stores arXiv metadata and digest receipts as source leads rather than promoted hardware, decoder, surface-code, resource-estimation, quantum-advantage, or fault-tolerant computation claims. | MATCH | publishable | 1 | source-ledger-boundary-scan | deviation 0 within tolerance 0.1 |
| The publication copy labels the preflight as a local deterministic fixture and blocks surface-code, hardware QEC, fault-tolerant computation, quantum advantage, cryptographic, and BuildLang/buildc-native runtime claims for this pass. | MATCH | publishable | 1 | claim-boundary-copy-scan | deviation 0 within tolerance 0.1 |

## Measurement Evidence

| Claim | Method | Evidence |
| --- | --- | --- |
| The QEC fixture emits QEC_STABILIZER_FIXTURE_MATCH, corrects no-error and single Pauli-X errors for both logical basis states, and rejects or marks unverifiable the configured negative controls. | qec-stabilizer-fixture-replay | demo/quantum-error-correction-proof-packet.mjs; demo/quantum-error-correction-proof-packet.test.mjs; docs/outreach/receipts/thirtieth-wave/quantum-error-correction-proof-packet-2026-07-02.json |
| The quantum source ledger stores arXiv metadata and digest receipts as source leads rather than promoted hardware, decoder, surface-code, resource-estimation, quantum-advantage, or fault-tolerant computation claims. | source-ledger-boundary-scan | demo/research/quantum-error-correction-source-receipts.json; docs/research/whitepapers/QUANTUM-ERROR-CORRECTION-PROOF-PACKETS-2026-07-02.md |
| The publication copy labels the preflight as a local deterministic fixture and blocks surface-code, hardware QEC, fault-tolerant computation, quantum advantage, cryptographic, and BuildLang/buildc-native runtime claims for this pass. | claim-boundary-copy-scan | docs/outreach/THIRTIETH-WAVE-QUANTUM-ERROR-CORRECTION-PREFLIGHT-2026-07-02.md; docs/research/official/QUANTUM-ERROR-CORRECTION-PROOF-PACKETS-2026-07-02.md; docs/research/whitepapers/QUANTUM-ERROR-CORRECTION-PROOF-PACKETS-2026-07-02.md |
