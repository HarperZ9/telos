# crucible report: Dogfood Pass 0056 Buyer Demo Manifest

## Summary

- thesis_id: `eff1906cf0dc79a8`
- thesis_seal: `eff1906cf0dc79a888c503221683bf50de21eb31a35e37dcb2e86f93d33d66a9`
- assessment_seal: `c0857e4ebd0481be36b69c1fd31894a6452efa1867f4532f1e900613de862bdb`
- counts: MATCH 8 / DRIFT 0 / UNVERIFIABLE 0
- integrity: seals_ok=True, thesis_ok=True, verdicts_rederive=True

## Verdicts

| Claim | Status | Disposition | Margin | Method | Grounds |
| --- | --- | --- | ---: | --- | --- |
| Pass 0056 created a BuyerDemoManifestSet/v1 artifact with status BUYER_DEMO_MANIFEST_SET_MATCH, review_pane_count 4, output_match_count 6, sha256 35ba395764d99729e4295ae672da15c3d6c7613f8a8588e7fa74933cec90db8c, and seal 9cd9b52cde63edf035e90cb69d2828f02dbebf8127924b476d03250a20fad2c9. | MATCH | fenced | 1 | manifest-schema-review | deviation 0 within tolerance 0.5 |
| Pass 0056 implements compose_buyer_demo_manifest.py with sha256 2e990435cfc4f2022dea15f2d6ad8d57590f97af5f0ac9f4cff69f0c94a06340 and implementation_status IMPLEMENTED_LOCAL_BUYER_DEMO_MANIFEST. | MATCH | fenced | 1 | composer-file-review | deviation 0 within tolerance 0.5 |
| Pass 0056 records a buyer demo manifest test script with sha256 af40206db09b3eef82a165a9d2ed3cca00b5a816e81924cc001c192c7ecc7ec2 and test_receipt status MATCH. | MATCH | fenced | 1 | composer-test-review | deviation 0 within tolerance 0.5 |
| Pass 0056 generated a demo bundle with output_count 6, output_match_count 6, review_pane_count 4, and failure_verdict_count 5. | MATCH | fenced | 1 | bundle-output-review | deviation 0 within tolerance 0.5 |
| Pass 0056 records replay_command_count 3, production_ready False, and public_review_ready True. | MATCH | fenced | 1 | review-readiness-boundary-review | deviation 0 within tolerance 0.5 |
| Pass 0056 binds to pass 0055 graph sha256 254f3bfc2b2e03cd4c0599956b17f79ec349ec2d9a1f207aa02a1619572834aa and source status MULTITRACE_CAUSALITY_GRAPH_MATCH. | MATCH | fenced | 1 | upstream-graph-binding-review | deviation 0 within tolerance 0.5 |
| Pass 0056 validator result reports MATCH with review_pane_count 4 and output_match_count 6. | MATCH | fenced | 1 | validator-result-review | deviation 0 within tolerance 0.5 |
| Pass 0056 records packet 066 sha256 b46db01901f6dc3f15410811dac40e992eca8bad8e0ae8635f333b0e4cbcb382, steelman sha256 61818c1c5e1552d417c6fe6896ad1a26022dbf3d9a779758485c5cb3a7323fdd, uniqueness_claim_status HYPOTHESIS_ONLY, and current_promoted_natural_laws remains none. | MATCH | fenced | 1 | non-promotion-boundary-review | deviation 0 within tolerance 0.5 |

## Measurement Evidence

| Claim | Method | Evidence |
| --- | --- | --- |
| Pass 0056 created a BuyerDemoManifestSet/v1 artifact with status BUYER_DEMO_MANIFEST_SET_MATCH, review_pane_count 4, output_match_count 6, sha256 35ba395764d99729e4295ae672da15c3d6c7613f8a8588e7fa74933cec90db8c, and seal 9cd9b52cde63edf035e90cb69d2828f02dbebf8127924b476d03250a20fad2c9. | manifest-schema-review | schema=BuyerDemoManifestSet/v1; status=BUYER_DEMO_MANIFEST_SET_MATCH; review_pane_count=4; output_match_count=6; sha256=35ba395764d99729e4295ae672da15c3d6c7613f8a8588e7fa74933cec90db8c; seal=9cd9b52cde63edf035e90cb69d2828f02dbebf8127924b476d03250a20fad2c9 |
| Pass 0056 implements compose_buyer_demo_manifest.py with sha256 2e990435cfc4f2022dea15f2d6ad8d57590f97af5f0ac9f4cff69f0c94a06340 and implementation_status IMPLEMENTED_LOCAL_BUYER_DEMO_MANIFEST. | composer-file-review | composer_sha256=2e990435cfc4f2022dea15f2d6ad8d57590f97af5f0ac9f4cff69f0c94a06340; implementation_status=IMPLEMENTED_LOCAL_BUYER_DEMO_MANIFEST |
| Pass 0056 records a buyer demo manifest test script with sha256 af40206db09b3eef82a165a9d2ed3cca00b5a816e81924cc001c192c7ecc7ec2 and test_receipt status MATCH. | composer-test-review | test_sha256=af40206db09b3eef82a165a9d2ed3cca00b5a816e81924cc001c192c7ecc7ec2; test_status=MATCH |
| Pass 0056 generated a demo bundle with output_count 6, output_match_count 6, review_pane_count 4, and failure_verdict_count 5. | bundle-output-review | output_count=6; output_match_count=6; review_pane_count=4; failure_verdict_count=5 |
| Pass 0056 records replay_command_count 3, production_ready False, and public_review_ready True. | review-readiness-boundary-review | replay_command_count=3; production_ready=False; public_review_ready=True |
| Pass 0056 binds to pass 0055 graph sha256 254f3bfc2b2e03cd4c0599956b17f79ec349ec2d9a1f207aa02a1619572834aa and source status MULTITRACE_CAUSALITY_GRAPH_MATCH. | upstream-graph-binding-review | graph_sha256=254f3bfc2b2e03cd4c0599956b17f79ec349ec2d9a1f207aa02a1619572834aa; source_status=MULTITRACE_CAUSALITY_GRAPH_MATCH |
| Pass 0056 validator result reports MATCH with review_pane_count 4 and output_match_count 6. | validator-result-review | validator_status=MATCH; review_pane_count=4; output_match_count=6 |
| Pass 0056 records packet 066 sha256 b46db01901f6dc3f15410811dac40e992eca8bad8e0ae8635f333b0e4cbcb382, steelman sha256 61818c1c5e1552d417c6fe6896ad1a26022dbf3d9a779758485c5cb3a7323fdd, uniqueness_claim_status HYPOTHESIS_ONLY, and current_promoted_natural_laws remains none. | non-promotion-boundary-review | packet_sha256=b46db01901f6dc3f15410811dac40e992eca8bad8e0ae8635f333b0e4cbcb382; steelman_sha256=61818c1c5e1552d417c6fe6896ad1a26022dbf3d9a779758485c5cb3a7323fdd; uniqueness_claim_status=HYPOTHESIS_ONLY; current_promoted_natural_laws=[] |
