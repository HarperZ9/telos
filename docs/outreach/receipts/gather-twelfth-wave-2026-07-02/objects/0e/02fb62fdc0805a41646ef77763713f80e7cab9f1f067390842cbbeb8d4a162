# crucible report: Dogfood Pass 0065 OTel Trace to Action Receipt Fixture

## Summary

- thesis_id: `41af816e4556a37c`
- thesis_seal: `41af816e4556a37ce758700629eb2ea1b4998c0367b72a95c897d0aff0c261ab`
- assessment_seal: `cd383c2757ad996649a083b4ba516cf6cfb2aebabaef34bac87ecd612e1929e7`
- counts: MATCH 7 / DRIFT 0 / UNVERIFIABLE 0
- integrity: seals_ok=True, thesis_ok=True, verdicts_rederive=True

## Verdicts

| Claim | Status | Disposition | Margin | Method | Grounds |
| --- | --- | --- | ---: | --- | --- |
| Pass 0065 created an OtelTraceToTelosActionReceiptFixture/v1 artifact with status OTEL_TRACE_TO_ACTION_RECEIPT_FIXTURE_MATCH, sha256 798fb31522a117d97b84816fa84440e79e6ffe4c82425c3cb37f0ba596991d87, and seal cb3c38e0568793121fb80660d9e584c574b54d69375a82d6337f033193ce199a. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |
| Pass 0065 trace fixture has trace_id 4f7e65b0c6c34c2aa1d6f64e08b03a65 and 4 spans. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |
| Pass 0065 action receipt uses schema project-telos.action-receipt/v1, receipt_status MATCH, verification_verdict MATCH, and side_effect_class local_read_only_fixture. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |
| Pass 0065 action receipt trace_refs preserve trace_id 4f7e65b0c6c34c2aa1d6f64e08b03a65 and 4 span ids. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |
| Pass 0065 negative fixture status is FAIL_EXPECTED with expected failures missing_authority_scope,missing_action_admission,missing_verification_verdict,missing_side_effect_class. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |
| Pass 0065 composer sha256 is c59debbd63f4355dfc01bad6919effa8086222e6cd94f7b09767fcb46dbe76f5 and compose_receipt status is MATCH. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |
| Pass 0065 packet sha256 is 99f2ff824ab1b7825084e3764d4d85ff97e94a0b0687a3030654c58892ca83b1, steelman sha256 is e2e2feb46b77a203771d46316bd4aae61d264eb1dda9b692af13775f3019f2a2, and test sha256 is be2c5e87b290efbf03ab393702f2a78bed7f58c390289ce0e7d05a4384013fca with test_receipt status MATCH. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |

## Measurement Evidence

| Claim | Method | Evidence |
| --- | --- | --- |
| Pass 0065 created an OtelTraceToTelosActionReceiptFixture/v1 artifact with status OTEL_TRACE_TO_ACTION_RECEIPT_FIXTURE_MATCH, sha256 798fb31522a117d97b84816fa84440e79e6ffe4c82425c3cb37f0ba596991d87, and seal cb3c38e0568793121fb80660d9e584c574b54d69375a82d6337f033193ce199a. | artifact-review | schema=OtelTraceToTelosActionReceiptFixture/v1; status=OTEL_TRACE_TO_ACTION_RECEIPT_FIXTURE_MATCH; sha256=798fb31522a117d97b84816fa84440e79e6ffe4c82425c3cb37f0ba596991d87; seal=cb3c38e0568793121fb80660d9e584c574b54d69375a82d6337f033193ce199a |
| Pass 0065 trace fixture has trace_id 4f7e65b0c6c34c2aa1d6f64e08b03a65 and 4 spans. | artifact-review | trace_id=4f7e65b0c6c34c2aa1d6f64e08b03a65; span_count=4 |
| Pass 0065 action receipt uses schema project-telos.action-receipt/v1, receipt_status MATCH, verification_verdict MATCH, and side_effect_class local_read_only_fixture. | artifact-review | receipt_schema=project-telos.action-receipt/v1; receipt_status=MATCH; verification_verdict=MATCH; side_effect_class=local_read_only_fixture |
| Pass 0065 action receipt trace_refs preserve trace_id 4f7e65b0c6c34c2aa1d6f64e08b03a65 and 4 span ids. | artifact-review | trace_ref=4f7e65b0c6c34c2aa1d6f64e08b03a65; span_ref_count=4 |
| Pass 0065 negative fixture status is FAIL_EXPECTED with expected failures missing_authority_scope,missing_action_admission,missing_verification_verdict,missing_side_effect_class. | artifact-review | negative_status=FAIL_EXPECTED; missing_authority_scope,missing_action_admission,missing_verification_verdict,missing_side_effect_class |
| Pass 0065 composer sha256 is c59debbd63f4355dfc01bad6919effa8086222e6cd94f7b09767fcb46dbe76f5 and compose_receipt status is MATCH. | artifact-review | composer_sha256=c59debbd63f4355dfc01bad6919effa8086222e6cd94f7b09767fcb46dbe76f5; compose_status=MATCH |
| Pass 0065 packet sha256 is 99f2ff824ab1b7825084e3764d4d85ff97e94a0b0687a3030654c58892ca83b1, steelman sha256 is e2e2feb46b77a203771d46316bd4aae61d264eb1dda9b692af13775f3019f2a2, and test sha256 is be2c5e87b290efbf03ab393702f2a78bed7f58c390289ce0e7d05a4384013fca with test_receipt status MATCH. | artifact-review | packet_sha256=99f2ff824ab1b7825084e3764d4d85ff97e94a0b0687a3030654c58892ca83b1; steelman_sha256=e2e2feb46b77a203771d46316bd4aae61d264eb1dda9b692af13775f3019f2a2; test_sha256=be2c5e87b290efbf03ab393702f2a78bed7f58c390289ce0e7d05a4384013fca; test_status=MATCH |
