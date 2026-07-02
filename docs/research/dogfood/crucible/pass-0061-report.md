# crucible report: Dogfood Pass 0061 Buyer Evidence Intake Ledger

## Summary

- thesis_id: `e1978070b31198fe`
- thesis_seal: `e1978070b31198fea6b386535e0058a9ef4982b15089d4753149f2b41d804464`
- assessment_seal: `cec8e2ca942fbf0dc212686d78f47a3c1a4c83d34aad79727aecf6877a063958`
- counts: MATCH 8 / DRIFT 0 / UNVERIFIABLE 0
- integrity: seals_ok=True, thesis_ok=True, verdicts_rederive=True

## Verdicts

| Claim | Status | Disposition | Margin | Method | Grounds |
| --- | --- | --- | ---: | --- | --- |
| Pass 0061 created a BuyerEvidenceIntakeLedger/v1 artifact with status BUYER_EVIDENCE_INTAKE_LEDGER_MATCH, record_count 3, evidence_field_count 24, private_field_count 21, gate_count 18, sha256 2a236310e23d64ba0bcbf440916b44fc9ff37a9b199fd17baa0e830077336491, and seal d074d80cd84659f735b81dc5161d58f5b4212142723f97463a35ba0965bb6220. | MATCH | fenced | 1 | artifact-schema-review | deviation 0 within tolerance 0.5 |
| Pass 0061 implements compose_buyer_evidence_intake_ledger.py with sha256 56f3c46fe2c6f3c6ae0af7f9ff841b168f713f6ad1e669ad647c6be83d6c66f1 and compose_receipt status MATCH. | MATCH | fenced | 1 | composer-file-review | deviation 0 within tolerance 0.5 |
| Pass 0061 records a buyer evidence intake test with sha256 266d184c91a1f5a7c1fb812993c52ee24158908c70773a9a5cf77dea1c5a05e1 and test_receipt status MATCH. | MATCH | fenced | 1 | composer-test-review | deviation 0 within tolerance 0.5 |
| Pass 0061 binds upstream pass 0060 seal 2bf5704d5e2065ee55732533a4f9bca3e5d892dc43e33fba676e5c56325c93ee and status BUYER_OUTREACH_PACKETS_MATCH. | MATCH | fenced | 1 | upstream-binding-review | deviation 0 within tolerance 0.5 |
| Pass 0061 buyer_response_status is AWAITING_REAL_RESPONSES, crm_write_status is NOT_WRITTEN, and send_status is NOT_SENT. | MATCH | fenced | 1 | open-status-review | deviation 0 within tolerance 0.5 |
| Pass 0061 forbids private contact data in model context and records private_field_count 21. | MATCH | fenced | 1 | privacy-boundary-review | deviation 0 within tolerance 0.5 |
| Pass 0061 unsupported_claim_count is 0, market_claim_boundary is HYPOTHESIS_ONLY, and current_promoted_natural_laws remains none. | MATCH | fenced | 1 | non-promotion-boundary-review | deviation 0 within tolerance 0.5 |
| Pass 0061 records packet 071 sha256 020110248f5126a4f0e835deebb0d3804ba1d63c2ab18c95050ef95aea84330d and steelman sha256 c4a053cad91b4a973c20e34f791e5733eba54aacbcbd5a98affb8cea7bf1978e. | MATCH | fenced | 1 | packet-steelman-review | deviation 0 within tolerance 0.5 |

## Measurement Evidence

| Claim | Method | Evidence |
| --- | --- | --- |
| Pass 0061 created a BuyerEvidenceIntakeLedger/v1 artifact with status BUYER_EVIDENCE_INTAKE_LEDGER_MATCH, record_count 3, evidence_field_count 24, private_field_count 21, gate_count 18, sha256 2a236310e23d64ba0bcbf440916b44fc9ff37a9b199fd17baa0e830077336491, and seal d074d80cd84659f735b81dc5161d58f5b4212142723f97463a35ba0965bb6220. | artifact-schema-review | schema=BuyerEvidenceIntakeLedger/v1; status=BUYER_EVIDENCE_INTAKE_LEDGER_MATCH; record_count=3; evidence_field_count=24; private_field_count=21; gate_count=18; sha256=2a236310e23d64ba0bcbf440916b44fc9ff37a9b199fd17baa0e830077336491; seal=d074d80cd84659f735b81dc5161d58f5b4212142723f97463a35ba0965bb6220 |
| Pass 0061 implements compose_buyer_evidence_intake_ledger.py with sha256 56f3c46fe2c6f3c6ae0af7f9ff841b168f713f6ad1e669ad647c6be83d6c66f1 and compose_receipt status MATCH. | composer-file-review | composer_sha256=56f3c46fe2c6f3c6ae0af7f9ff841b168f713f6ad1e669ad647c6be83d6c66f1; compose_status=MATCH |
| Pass 0061 records a buyer evidence intake test with sha256 266d184c91a1f5a7c1fb812993c52ee24158908c70773a9a5cf77dea1c5a05e1 and test_receipt status MATCH. | composer-test-review | test_sha256=266d184c91a1f5a7c1fb812993c52ee24158908c70773a9a5cf77dea1c5a05e1; test_status=MATCH |
| Pass 0061 binds upstream pass 0060 seal 2bf5704d5e2065ee55732533a4f9bca3e5d892dc43e33fba676e5c56325c93ee and status BUYER_OUTREACH_PACKETS_MATCH. | upstream-binding-review | upstream_seal=2bf5704d5e2065ee55732533a4f9bca3e5d892dc43e33fba676e5c56325c93ee; upstream_status=BUYER_OUTREACH_PACKETS_MATCH |
| Pass 0061 buyer_response_status is AWAITING_REAL_RESPONSES, crm_write_status is NOT_WRITTEN, and send_status is NOT_SENT. | open-status-review | buyer_response_status=AWAITING_REAL_RESPONSES; crm_write_status=NOT_WRITTEN; send_status=NOT_SENT |
| Pass 0061 forbids private contact data in model context and records private_field_count 21. | privacy-boundary-review | private_field_count=21; privacy_boundary=NO_PRIVATE_CONTACT_DATA_IN_MODEL_CONTEXT |
| Pass 0061 unsupported_claim_count is 0, market_claim_boundary is HYPOTHESIS_ONLY, and current_promoted_natural_laws remains none. | non-promotion-boundary-review | unsupported_claim_count=0; market_claim_boundary=HYPOTHESIS_ONLY; current_promoted_natural_laws=[] |
| Pass 0061 records packet 071 sha256 020110248f5126a4f0e835deebb0d3804ba1d63c2ab18c95050ef95aea84330d and steelman sha256 c4a053cad91b4a973c20e34f791e5733eba54aacbcbd5a98affb8cea7bf1978e. | packet-steelman-review | packet_sha256=020110248f5126a4f0e835deebb0d3804ba1d63c2ab18c95050ef95aea84330d; steelman_sha256=c4a053cad91b4a973c20e34f791e5733eba54aacbcbd5a98affb8cea7bf1978e |
