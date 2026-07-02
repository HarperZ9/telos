# crucible report: Dogfood Pass 0005 Adapter Strategy and Validator Contracts

## Summary

- thesis_id: `d51b7984f1d1e194`
- thesis_seal: `d51b7984f1d1e194761fea93b1d2e9563c81f6ffa4b7c73539af1eadfffe6935`
- assessment_seal: `39cd8c3bb74519e94eb8d916917035dbd9d98176ead08121fc18dc36f56629c7`
- counts: MATCH 7 / DRIFT 0 / UNVERIFIABLE 0
- integrity: seals_ok=True, thesis_ok=True, verdicts_rederive=True

## Verdicts

| Claim | Status | Disposition | Margin | Method | Grounds |
| --- | --- | --- | ---: | --- | --- |
| Pass 0005 recorded official source anchors for at least 10 incumbent evidence surfaces that can become proof-packet adapters. | MATCH | fenced | 1 | source-anchor-review | deviation 0 within tolerance 0.5 |
| The pass 0005 adapter artifact contains 10 adapters, and every adapter includes source URLs, evidence inputs, Telos outputs, and a missing-binding field. | MATCH | fenced | 1 | json-structure-review | deviation 0 within tolerance 0.5 |
| The pass 0005 buyer-objection matrix contains at least 7 objections, each with a buyer question, required demo evidence, and product response. | MATCH | fenced | 1 | json-structure-review | deviation 0 within tolerance 0.5 |
| The pass 0005 validator contract artifact contains at least 8 validators and includes ProofPacketMinimumValidator. | MATCH | fenced | 1 | json-structure-review | deviation 0 within tolerance 0.5 |
| Pass 0005 records Gather web-config friction and a successful unscoped Gather docs intake with 23 kept documents, zero drops, and seal 8afe8c29d704aff1ca6255e81704722bb5a347c9bed237e9ecca34facdeb09a3. | MATCH | fenced | 1 | gather-receipt-review | deviation 0 within tolerance 0.5 |
| Pass 0005 records a low-confidence Forum route escalation while Forum ledger verification remained chain=true and deep=true. | MATCH | fenced | 1 | forum-receipt-review | deviation 0 within tolerance 0.5 |
| Pass 0005 promotes zero natural-law discoveries; all outputs remain strategy, evidence, or validator-planning artifacts. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |

## Measurement Evidence

| Claim | Method | Evidence |
| --- | --- | --- |
| Pass 0005 recorded official source anchors for at least 10 incumbent evidence surfaces that can become proof-packet adapters. | source-anchor-review | source anchors=11; OpenTelemetry traces official docs; LangSmith Observability official docs; Langfuse Observability official docs; MLflow Tracking official docs; W&B Artifacts official docs; DVC Versioning Data and Models official docs; Nextflow Reports official docs; Snakemake Reports official docs; OpenLineage docs; SLSA Provenance spec; in-toto official site |
| The pass 0005 adapter artifact contains 10 adapters, and every adapter includes source URLs, evidence inputs, Telos outputs, and a missing-binding field. | json-structure-review | proof-packet-adapters-pass-0005.json adapters=10; all adapters include source_urls; all adapters include evidence_inputs; all adapters include telos_outputs; all adapters include missing_binding |
| The pass 0005 buyer-objection matrix contains at least 7 objections, each with a buyer question, required demo evidence, and product response. | json-structure-review | buyer-objections-pass-0005.json objections=8; all objections include buyer_question; all objections include required_demo_evidence; all objections include product_response |
| The pass 0005 validator contract artifact contains at least 8 validators and includes ProofPacketMinimumValidator. | json-structure-review | validator-contracts-pass-0005.json contracts=8; contract names include ProofPacketMinimumValidator |
| Pass 0005 records Gather web-config friction and a successful unscoped Gather docs intake with 23 kept documents, zero drops, and seal 8afe8c29d704aff1ca6255e81704722bb5a347c9bed237e9ecca34facdeb09a3. | gather-receipt-review | web config attempt 1 rejected: non-empty jobs list required; web config attempt 2 rejected: each job needs source and target; web config attempt 3 rejected: unknown source for raw URL; unscoped gather_docs kept=23; unscoped gather_docs dropped=0; unscoped gather_docs seal=8afe8c29d704aff1ca6255e81704722bb5a347c9bed237e9ecca34facdeb09a3 |
| Pass 0005 records a low-confidence Forum route escalation while Forum ledger verification remained chain=true and deep=true. | forum-receipt-review | forum route decided=null; forum route needs_escalation=true; forum route confidence=0.17297297297297298; forum verify chain=true; forum verify deep=true |
| Pass 0005 promotes zero natural-law discoveries; all outputs remain strategy, evidence, or validator-planning artifacts. | artifact-review | pass-0005-ledger.md says current promoted natural laws: none; README says current promoted natural laws: none; pass 0005 artifacts are adapter, buyer-objection, validator, thesis, measurement, or ledger artifacts |
