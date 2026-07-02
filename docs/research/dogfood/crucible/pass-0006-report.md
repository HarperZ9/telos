# crucible report: Dogfood Pass 0006 Executable Validator and Minimal Proof Packet

## Summary

- thesis_id: `968e1d7e97fc5245`
- thesis_seal: `968e1d7e97fc524528efa1491dd48b9d049b3a1ad25d202e0bc90882049fc39a`
- assessment_seal: `4b780f21291c7d4464ec07a10b3feb8130d0951e5b0ef6bd3f716343cedcebc1`
- counts: MATCH 6 / DRIFT 0 / UNVERIFIABLE 0
- integrity: seals_ok=True, thesis_ok=True, verdicts_rederive=True

## Verdicts

| Claim | Status | Disposition | Margin | Method | Grounds |
| --- | --- | --- | ---: | --- | --- |
| Pass 0006 created a local read-only dogfood validator script that checks existing schema artifacts plus the pass 0006 ProofPacket and OpenTelemetry normalization map. | MATCH | fenced | 1 | script-structure-review | deviation 0 within tolerance 0.5 |
| The pass 0006 ProofPacket artifact includes the ProofPacket/v1 minimum fields: packet id, domain, claim set, source receipts, action receipts, authority receipts, workspace state, verification verdicts, failure labels, and decision summary. | MATCH | fenced | 1 | json-structure-review | deviation 0 within tolerance 0.5 |
| The pass 0006 OpenTelemetry normalization artifact contains at least 8 field mappings and explicitly marks authority, workspace state, verification verdict, and decision summary as non-inferable from trace spans alone. | MATCH | fenced | 1 | json-structure-review | deviation 0 within tolerance 0.5 |
| The Build Color pass 0006 measurement receipt reports bounded probe values under declared thresholds and a targeted pytest slice with 88 passing tests. | MATCH | fenced | 1 | measurement-and-test-review | deviation 0 within tolerance 0.5 |
| The dogfood validator run for pass 0006 reports MATCH with 9 checks and zero drift. | MATCH | fenced | 1 | validator-run-review | deviation 0 within tolerance 0.5 |
| Pass 0006 promotes zero natural-law discoveries; all outputs remain schema, adapter, proof-packet, measurement, or verification artifacts. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |

## Measurement Evidence

| Claim | Method | Evidence |
| --- | --- | --- |
| Pass 0006 created a local read-only dogfood validator script that checks existing schema artifacts plus the pass 0006 ProofPacket and OpenTelemetry normalization map. | script-structure-review | tools/validate_dogfood_artifacts.py exists; validator references market-rows-pass-0003.json; validator references wedge-scores-pass-0003.json; validator references megatool-nodes-pass-0003.json; validator references research-claims-pass-0004.json; validator references proof-packet-adapters-pass-0005.json; validator references buyer-objections-pass-0005.json; validator references validator-contracts-pass-0005.json; validator references otel-action-normalization-pass-0006.json; validator references proof-packet-pass-0006.json |
| The pass 0006 ProofPacket artifact includes the ProofPacket/v1 minimum fields: packet id, domain, claim set, source receipts, action receipts, authority receipts, workspace state, verification verdicts, failure labels, and decision summary. | json-structure-review | proof-packet-pass-0006.json includes packet_id; proof-packet-pass-0006.json includes domain; proof-packet-pass-0006.json includes claim_set; proof-packet-pass-0006.json includes source_receipts; proof-packet-pass-0006.json includes action_receipts; proof-packet-pass-0006.json includes authority_receipts; proof-packet-pass-0006.json includes workspace_state; proof-packet-pass-0006.json includes verification_verdicts; proof-packet-pass-0006.json includes failure_labels; proof-packet-pass-0006.json includes decision_summary |
| The pass 0006 OpenTelemetry normalization artifact contains at least 8 field mappings and explicitly marks authority, workspace state, verification verdict, and decision summary as non-inferable from trace spans alone. | json-structure-review | otel-action-normalization-pass-0006.json mappings=10; non_inferable_telos_fields includes authority_receipt; non_inferable_telos_fields includes workspace_state; non_inferable_telos_fields includes verification_verdict; non_inferable_telos_fields includes decision_summary |
| The Build Color pass 0006 measurement receipt reports bounded probe values under declared thresholds and a targeted pytest slice with 88 passing tests. | measurement-and-test-review | srgb_xyz_max_abs_error=0.0000017030280945010406 under threshold 0.00001; srgb_oklab_max_abs_error=0.00000000000001072185665305766 under threshold 0.0000000001; pq_max_abs_nits_error=0.00000000008458300726488233 under threshold 0.000001; cie2000_pair_1_abs_error=0.00004031984342622863 under threshold 0.005; targeted pytest slice: 88 passed in 0.39s; measurement seal=c97850b96f0813b80bfdf084d9c8d63c22bf089a3f59f9a6f39283b1fe86400f |
| The dogfood validator run for pass 0006 reports MATCH with 9 checks and zero drift. | validator-run-review | schema-validator-results-pass-0006.json status=MATCH; schema-validator-results-pass-0006.json match=9; schema-validator-results-pass-0006.json drift=0 |
| Pass 0006 promotes zero natural-law discoveries; all outputs remain schema, adapter, proof-packet, measurement, or verification artifacts. | artifact-review | pass-0006-ledger.md says current promoted natural laws: none; README says current promoted natural laws: none; proof-packet-pass-0006.json failure_labels include NOT_A_NATURAL_LAW |
