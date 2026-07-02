# crucible report: Dogfood Pass 0104 AI4Science Claim-to-Experiment Receipt

## Summary

- thesis_id: `f674ecfdd5520582`
- thesis_seal: `f674ecfdd55205829ca99b174d3995542d768da1bc533a45adeeb08aa0f2689b`
- assessment_seal: `2c314992f88142674757db033692170a0e40b352ba6b86d945963c0c81f5fb28`
- counts: MATCH 9 / DRIFT 0 / UNVERIFIABLE 0
- integrity: seals_ok=True, thesis_ok=True, verdicts_rederive=True

## Verdicts

| Claim | Status | Disposition | Margin | Method | Grounds |
| --- | --- | --- | ---: | --- | --- |
| Pass 0104 created an AI4ScienceClaimToExperimentReceipt/v1 artifact with status AI4SCIENCE_CLAIM_TO_EXPERIMENT_RECEIPT_MATCH, sha256 1e46530dfba2b532b5c4f4769d3d019ca45e9dd0a068a8bb04646d36fa26c844, and seal cdc127d906c82e1a485c434f2cea03c47902842a5182f7bac69e7d57205b6593. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |
| Pass 0104 binds source passes {'roadmap_pass': '0102', 'roadmap_top_priority': 'optimization_proof_workbench', 'youtube_pass': '0085'} and records 11 sources. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |
| Pass 0104 records 11 official or primary sources and 1 YouTube AI4Science source video. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |
| Pass 0104 defines 11 minimum packet fields. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |
| Pass 0104 maps 11 sources to receipt requirements. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |
| Pass 0104 defines 3 next experiments and promotion gates {'rejects_unmeasured_discovery_claim': True, 'requires_human_review': True, 'requires_reproduction_status': True}. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |
| Pass 0104 flagship receipts for Forum, Index, and Telos all have MATCH status. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |
| Pass 0104 records unsupported_claim_count 0 and current_promoted_natural_laws length 0. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |
| Pass 0104 composer sha256 is a67e1df8683af74db16b19a9b9ee9d248dae3d728dbb89a5ee56cd808c4455bd, packet sha256 is c8dc36bad51dcc14480bf4a1f2c3533fc46df7fed1fe768e26c960877710c234, brief sha256 is 4bb052f7ffe58fcbe02020c655cde4878d522be7e594bc9fac1eb3368e29eec8, steelman sha256 is 80a71223ebfdc474d7e5b6c1eafb523ff0e6578e8d6d231bacbf68c9e4f24c31, test sha256 is bcf5453b0fa292aa84dc1445bc232a9ec03263ad9cc252677c0464fb10160b8c, and tool_receipts sha256 is bc749ed592d5e747b70ce3c8c3cf5fed9b3f0702386216d7d5a0a8aee7bfda9b with test_receipt status MATCH. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |

## Measurement Evidence

| Claim | Method | Evidence |
| --- | --- | --- |
| Pass 0104 created an AI4ScienceClaimToExperimentReceipt/v1 artifact with status AI4SCIENCE_CLAIM_TO_EXPERIMENT_RECEIPT_MATCH, sha256 1e46530dfba2b532b5c4f4769d3d019ca45e9dd0a068a8bb04646d36fa26c844, and seal cdc127d906c82e1a485c434f2cea03c47902842a5182f7bac69e7d57205b6593. | artifact-review | schema=AI4ScienceClaimToExperimentReceipt/v1; status=AI4SCIENCE_CLAIM_TO_EXPERIMENT_RECEIPT_MATCH; sha256=1e46530dfba2b532b5c4f4769d3d019ca45e9dd0a068a8bb04646d36fa26c844; seal=cdc127d906c82e1a485c434f2cea03c47902842a5182f7bac69e7d57205b6593 |
| Pass 0104 binds source passes {'roadmap_pass': '0102', 'roadmap_top_priority': 'optimization_proof_workbench', 'youtube_pass': '0085'} and records 11 sources. | artifact-review | source_bindings={'roadmap_pass': '0102', 'roadmap_top_priority': 'optimization_proof_workbench', 'youtube_pass': '0085'}; source_count=11 |
| Pass 0104 records 11 official or primary sources and 1 YouTube AI4Science source video. | artifact-review | official_or_primary_count=11; youtube_ai4science_video_count=1 |
| Pass 0104 defines 11 minimum packet fields. | artifact-review | minimum_packet_fields=['source_claim', 'source_receipts', 'model_or_agent_actions', 'experiment_or_simulation_protocol', 'workflow_runtime_receipt', 'measurement_receipt', 'statistical_or_scoring_plan', 'reproduction_status', 'negative_result_path', 'reviewer_objections', 'promotion_verdict'] |
| Pass 0104 maps 11 sources to receipt requirements. | artifact-review | source_to_receipt_map_count=11 |
| Pass 0104 defines 3 next experiments and promotion gates {'rejects_unmeasured_discovery_claim': True, 'requires_human_review': True, 'requires_reproduction_status': True}. | artifact-review | next_experiments=3; promotion_gates={'rejects_unmeasured_discovery_claim': True, 'requires_human_review': True, 'requires_reproduction_status': True} |
| Pass 0104 flagship receipts for Forum, Index, and Telos all have MATCH status. | artifact-review | forum=MATCH; index=MATCH; telos=MATCH |
| Pass 0104 records unsupported_claim_count 0 and current_promoted_natural_laws length 0. | artifact-review | unsupported_claim_count=0; natural_law_count=0 |
| Pass 0104 composer sha256 is a67e1df8683af74db16b19a9b9ee9d248dae3d728dbb89a5ee56cd808c4455bd, packet sha256 is c8dc36bad51dcc14480bf4a1f2c3533fc46df7fed1fe768e26c960877710c234, brief sha256 is 4bb052f7ffe58fcbe02020c655cde4878d522be7e594bc9fac1eb3368e29eec8, steelman sha256 is 80a71223ebfdc474d7e5b6c1eafb523ff0e6578e8d6d231bacbf68c9e4f24c31, test sha256 is bcf5453b0fa292aa84dc1445bc232a9ec03263ad9cc252677c0464fb10160b8c, and tool_receipts sha256 is bc749ed592d5e747b70ce3c8c3cf5fed9b3f0702386216d7d5a0a8aee7bfda9b with test_receipt status MATCH. | artifact-review | composer_sha256=a67e1df8683af74db16b19a9b9ee9d248dae3d728dbb89a5ee56cd808c4455bd; packet_sha256=c8dc36bad51dcc14480bf4a1f2c3533fc46df7fed1fe768e26c960877710c234; brief_sha256=4bb052f7ffe58fcbe02020c655cde4878d522be7e594bc9fac1eb3368e29eec8; steelman_sha256=80a71223ebfdc474d7e5b6c1eafb523ff0e6578e8d6d231bacbf68c9e4f24c31; test_sha256=bcf5453b0fa292aa84dc1445bc232a9ec03263ad9cc252677c0464fb10160b8c; tool_receipts_sha256=bc749ed592d5e747b70ce3c8c3cf5fed9b3f0702386216d7d5a0a8aee7bfda9b; test_status=MATCH; compose_status=MATCH |
