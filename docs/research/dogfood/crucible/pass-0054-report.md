# crucible report: Dogfood Pass 0054 OTel Trace Receipt Join Adapter

## Summary

- thesis_id: `5290fb197e16630d`
- thesis_seal: `5290fb197e16630d0271a4c78f65e5118fb13bc860649eb8decb91e239395fa5`
- assessment_seal: `263fc41a671dc81e16bf04ca5f7ff3d084666812e3e26ed580ad55045a504c12`
- counts: MATCH 8 / DRIFT 0 / UNVERIFIABLE 0
- integrity: seals_ok=True, thesis_ok=True, verdicts_rederive=True

## Verdicts

| Claim | Status | Disposition | Margin | Method | Grounds |
| --- | --- | --- | ---: | --- | --- |
| Pass 0054 created an OTelTraceReceiptJoinAdapterSet/v1 artifact with status OTEL_TRACE_RECEIPT_JOIN_ADAPTER_MATCH, joined_event_count 4, sha256 b413323fc8392ec36932a780bf7a5629aa3afef04e251f07a88f78e4a08dbe5a, and seal e85049e5d195d6eeda1aeadfea360b06884dfd5a5d93bdaadc1d78ff3d99b763. | MATCH | fenced | 1 | trace-join-adapter-schema-review | deviation 0 within tolerance 0.5 |
| Pass 0054 implements import_otel_trace_receipts.py with sha256 67036eaee6a648736006c355c0c5fe85accb0cac7a863c3e474f4886d39668ef and records implementation_status IMPLEMENTED_LOCAL_TRACE_JOIN_ADAPTER. | MATCH | fenced | 1 | trace-join-adapter-file-review | deviation 0 within tolerance 0.5 |
| Pass 0054 records a trace join adapter test script with sha256 1c06824c0b8ba988f535fcbc7525d2c04e68d072f77e8548a3df6ce3123e5403 and test_receipt status MATCH. | MATCH | fenced | 1 | trace-join-adapter-test-review | deviation 0 within tolerance 0.5 |
| Pass 0054 generated an OTelTraceReceiptJoinSet/v1 output with status OTEL_TRACE_RECEIPT_JOIN_MATCH, joined_event_count 4, trace_span_count 1, trace_replaces_receipt_count 0, and sha256 cbaaf059b6da49cab92fac4bb15ea0b525cc5948ad90c40fc7741371791887ed. | MATCH | fenced | 1 | trace-join-output-review | deviation 0 within tolerance 0.5 |
| Pass 0054 records negative_fixture_count 4, negative_match_count 4, and negative_pass_observed_count 0 from the trace join adapter. | MATCH | fenced | 1 | trace-join-negative-fixture-review | deviation 0 within tolerance 0.5 |
| Pass 0054 binds to pass 0024 action receipt fixture with sha256 9c6402f98774170311d78ea3f6983cae71a665dd38ab2ee7e88d413398990ff4, seal 58ed4ced91f18cbab776729f49f728d47013542cfc2448865bbdb8dccd1228e3, and source status ACTION_RECEIPT_FIXTURE_MATCH. | MATCH | fenced | 1 | upstream-action-receipt-binding-review | deviation 0 within tolerance 0.5 |
| Pass 0054 validator result reports MATCH with joined_event_count 4 and trace_replaces_receipt_count 0. | MATCH | fenced | 1 | validator-result-review | deviation 0 within tolerance 0.5 |
| Pass 0054 records packet 064 sha256 71b39e899e143294fb810a2d335bb11cbeff43abf26114cdda22573dd2502952, steelman sha256 377aabb2b42937e7fa12bcd75b4588f13b2ddcdd1464ecaad145c2f9bf73fdea, uniqueness_claim_status HYPOTHESIS_ONLY, and current_promoted_natural_laws remains none. | MATCH | fenced | 1 | non-promotion-boundary-review | deviation 0 within tolerance 0.5 |

## Measurement Evidence

| Claim | Method | Evidence |
| --- | --- | --- |
| Pass 0054 created an OTelTraceReceiptJoinAdapterSet/v1 artifact with status OTEL_TRACE_RECEIPT_JOIN_ADAPTER_MATCH, joined_event_count 4, sha256 b413323fc8392ec36932a780bf7a5629aa3afef04e251f07a88f78e4a08dbe5a, and seal e85049e5d195d6eeda1aeadfea360b06884dfd5a5d93bdaadc1d78ff3d99b763. | trace-join-adapter-schema-review | schema=OTelTraceReceiptJoinAdapterSet/v1; status=OTEL_TRACE_RECEIPT_JOIN_ADAPTER_MATCH; joined_event_count=4; sha256=b413323fc8392ec36932a780bf7a5629aa3afef04e251f07a88f78e4a08dbe5a; seal=e85049e5d195d6eeda1aeadfea360b06884dfd5a5d93bdaadc1d78ff3d99b763 |
| Pass 0054 implements import_otel_trace_receipts.py with sha256 67036eaee6a648736006c355c0c5fe85accb0cac7a863c3e474f4886d39668ef and records implementation_status IMPLEMENTED_LOCAL_TRACE_JOIN_ADAPTER. | trace-join-adapter-file-review | adapter_sha256=67036eaee6a648736006c355c0c5fe85accb0cac7a863c3e474f4886d39668ef; implementation_status=IMPLEMENTED_LOCAL_TRACE_JOIN_ADAPTER |
| Pass 0054 records a trace join adapter test script with sha256 1c06824c0b8ba988f535fcbc7525d2c04e68d072f77e8548a3df6ce3123e5403 and test_receipt status MATCH. | trace-join-adapter-test-review | test_sha256=1c06824c0b8ba988f535fcbc7525d2c04e68d072f77e8548a3df6ce3123e5403; test_status=MATCH |
| Pass 0054 generated an OTelTraceReceiptJoinSet/v1 output with status OTEL_TRACE_RECEIPT_JOIN_MATCH, joined_event_count 4, trace_span_count 1, trace_replaces_receipt_count 0, and sha256 cbaaf059b6da49cab92fac4bb15ea0b525cc5948ad90c40fc7741371791887ed. | trace-join-output-review | join_status=OTEL_TRACE_RECEIPT_JOIN_MATCH; joined_event_count=4; trace_span_count=1; trace_replaces_receipt_count=0; sha256=cbaaf059b6da49cab92fac4bb15ea0b525cc5948ad90c40fc7741371791887ed |
| Pass 0054 records negative_fixture_count 4, negative_match_count 4, and negative_pass_observed_count 0 from the trace join adapter. | trace-join-negative-fixture-review | negative_fixture_count=4; negative_match_count=4; negative_pass_observed_count=0 |
| Pass 0054 binds to pass 0024 action receipt fixture with sha256 9c6402f98774170311d78ea3f6983cae71a665dd38ab2ee7e88d413398990ff4, seal 58ed4ced91f18cbab776729f49f728d47013542cfc2448865bbdb8dccd1228e3, and source status ACTION_RECEIPT_FIXTURE_MATCH. | upstream-action-receipt-binding-review | upstream_sha256=9c6402f98774170311d78ea3f6983cae71a665dd38ab2ee7e88d413398990ff4; upstream_seal=58ed4ced91f18cbab776729f49f728d47013542cfc2448865bbdb8dccd1228e3; source_status=ACTION_RECEIPT_FIXTURE_MATCH |
| Pass 0054 validator result reports MATCH with joined_event_count 4 and trace_replaces_receipt_count 0. | validator-result-review | validator_status=MATCH; joined_event_count=4; trace_replaces_receipt_count=0 |
| Pass 0054 records packet 064 sha256 71b39e899e143294fb810a2d335bb11cbeff43abf26114cdda22573dd2502952, steelman sha256 377aabb2b42937e7fa12bcd75b4588f13b2ddcdd1464ecaad145c2f9bf73fdea, uniqueness_claim_status HYPOTHESIS_ONLY, and current_promoted_natural_laws remains none. | non-promotion-boundary-review | packet_sha256=71b39e899e143294fb810a2d335bb11cbeff43abf26114cdda22573dd2502952; steelman_sha256=377aabb2b42937e7fa12bcd75b4588f13b2ddcdd1464ecaad145c2f9bf73fdea; uniqueness_claim_status=HYPOTHESIS_ONLY; current_promoted_natural_laws=[] |
