# crucible report: Dogfood Pass 0069 Telos Multi-Receipt Joiner

## Summary

- thesis_id: `659eee0820d8802c`
- thesis_seal: `659eee0820d8802c02957d10775b179549e79120a455e1c0d433a75dc089d793`
- assessment_seal: `38ee0b8887ddd0e002623ac7bd7b8b24b72c8d6ba1d77bab2743b110bbb118ef`
- counts: MATCH 8 / DRIFT 0 / UNVERIFIABLE 0
- integrity: seals_ok=True, thesis_ok=True, verdicts_rederive=True

## Verdicts

| Claim | Status | Disposition | Margin | Method | Grounds |
| --- | --- | --- | ---: | --- | --- |
| Pass 0069 created a TelosMultiReceiptJoiner/v1 artifact with status TELOS_MULTIRECEIPT_JOINER_MATCH, sha256 35212426f08143e020eca5146908458d870de862490ba2b3d1558e94068d08a6, and seal 366d4dc9809aeb8e9db70f73c5d89e5bec7df9491939793e3e5f84eae96c87a0. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |
| Pass 0069 contains 6 component receipts covering required classes ['source_intake', 'workspace_context', 'routing', 'verification', 'continuity', 'action']. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |
| Pass 0069 product packet has component_count 6 and unsupported_claim_count 0. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |
| Pass 0069 contains 5 negative fixtures and 7 ablation results. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |
| Pass 0069 raw_private_payload_required is False and model_reasoning_required_for_replay is False. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |
| Pass 0069 previous_pass_binding seal is 10e642fab785fa49d42fc6c1acc2ecca3d9bc3dad78a9b61abdf81e6678a2bf6. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |
| Pass 0069 composer sha256 is acf5a294d2b3268fee47542740376b397d45a6ad839498090bad17a30a2c1abb and compose_receipt status is MATCH. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |
| Pass 0069 packet sha256 is f574a654b9b032c2ef9f8332d6bd000d4eeb8ae7b2f81f6b5279b4ef22c1341d, steelman sha256 is 99efb5f1ef21658adb8be29e64f127bf29291130d0a6e6596edd5f3af791e72e, and test sha256 is baac1d8c9f591fdb75cf1de1e04aa9c1726bc14a28c005bd71523f1df5d75e4a with test_receipt status MATCH. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |

## Measurement Evidence

| Claim | Method | Evidence |
| --- | --- | --- |
| Pass 0069 created a TelosMultiReceiptJoiner/v1 artifact with status TELOS_MULTIRECEIPT_JOINER_MATCH, sha256 35212426f08143e020eca5146908458d870de862490ba2b3d1558e94068d08a6, and seal 366d4dc9809aeb8e9db70f73c5d89e5bec7df9491939793e3e5f84eae96c87a0. | artifact-review | schema=TelosMultiReceiptJoiner/v1; status=TELOS_MULTIRECEIPT_JOINER_MATCH; sha256=35212426f08143e020eca5146908458d870de862490ba2b3d1558e94068d08a6; seal=366d4dc9809aeb8e9db70f73c5d89e5bec7df9491939793e3e5f84eae96c87a0 |
| Pass 0069 contains 6 component receipts covering required classes ['source_intake', 'workspace_context', 'routing', 'verification', 'continuity', 'action']. | artifact-review | component_count=6; required_classes=['source_intake', 'workspace_context', 'routing', 'verification', 'continuity', 'action'] |
| Pass 0069 product packet has component_count 6 and unsupported_claim_count 0. | artifact-review | component_count=6; unsupported_claim_count=0 |
| Pass 0069 contains 5 negative fixtures and 7 ablation results. | artifact-review | negative_fixture_count=5; ablation_count=7 |
| Pass 0069 raw_private_payload_required is False and model_reasoning_required_for_replay is False. | artifact-review | raw_private_payload_required=False; model_reasoning_required_for_replay=False |
| Pass 0069 previous_pass_binding seal is 10e642fab785fa49d42fc6c1acc2ecca3d9bc3dad78a9b61abdf81e6678a2bf6. | artifact-review | previous_pass_binding=10e642fab785fa49d42fc6c1acc2ecca3d9bc3dad78a9b61abdf81e6678a2bf6 |
| Pass 0069 composer sha256 is acf5a294d2b3268fee47542740376b397d45a6ad839498090bad17a30a2c1abb and compose_receipt status is MATCH. | artifact-review | composer_sha256=acf5a294d2b3268fee47542740376b397d45a6ad839498090bad17a30a2c1abb; compose_status=MATCH |
| Pass 0069 packet sha256 is f574a654b9b032c2ef9f8332d6bd000d4eeb8ae7b2f81f6b5279b4ef22c1341d, steelman sha256 is 99efb5f1ef21658adb8be29e64f127bf29291130d0a6e6596edd5f3af791e72e, and test sha256 is baac1d8c9f591fdb75cf1de1e04aa9c1726bc14a28c005bd71523f1df5d75e4a with test_receipt status MATCH. | artifact-review | packet_sha256=f574a654b9b032c2ef9f8332d6bd000d4eeb8ae7b2f81f6b5279b4ef22c1341d; steelman_sha256=99efb5f1ef21658adb8be29e64f127bf29291130d0a6e6596edd5f3af791e72e; test_sha256=baac1d8c9f591fdb75cf1de1e04aa9c1726bc14a28c005bd71523f1df5d75e4a; test_status=MATCH |
