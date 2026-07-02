# crucible report: Dogfood Pass 0040 Content-Addressed Archive Statement Replay

## Summary

- thesis_id: `f8c3ceef96196513`
- thesis_seal: `f8c3ceef96196513d74e9692a6290412c98a33301f45e1137667a93dd03290a9`
- assessment_seal: `78269c9f53d96b30121ba4311adcf57a63925cf5ef043eb8bca69c5b8ab3452e`
- counts: MATCH 8 / DRIFT 0 / UNVERIFIABLE 0
- integrity: seals_ok=True, thesis_ok=True, verdicts_rederive=True

## Verdicts

| Claim | Status | Disposition | Margin | Method | Grounds |
| --- | --- | --- | ---: | --- | --- |
| Pass 0040 created a TheoremArchivedBlobStatementReplaySet/v1 artifact with status ARCHIVED_BLOB_STATEMENT_REPLAY_MATCH, theorem_count 10, archive_check_count 10, unique_archive_file_count 10, sha256 e45620662cc30976f8b1f814e5b0ceb3815c16f6e86e091364220fa286bfe654, and seal c38574335633bb119b7c14b8f7a69db44751f04f44bb3fd74c71df4e2a74818d. | MATCH | fenced | 1 | archive-blob-schema-review | deviation 0 within tolerance 0.5 |
| Pass 0040 records fixture fixtures/theorem-archived-blob-statement-replay-pass-0040.json with sha256 cc76916c782838deda0c4c19b5324279e0a3524497d3b75728459e9cedeea1f7 and seal e81a919446ab3e8184ad74cc444a8cbe628490c51a83d41edccb261a021c3a95. | MATCH | fenced | 1 | fixture-binding-review | deviation 0 within tolerance 0.5 |
| Pass 0040 binds to pass 0039 remote raw-blob statement replay with sha256 0e13f8c76728c20d3cfdb298638da8c5054f9b2bdf4e6fd8db0f74065fb20376, seal c01eb59d75eb418f551e302b19dbaf47c4193373f72c4af5d229567fa96ebc58, and source status REMOTE_BLOB_STATEMENT_REPLAY_MATCH. | MATCH | fenced | 1 | source-binding-review | deviation 0 within tolerance 0.5 |
| Pass 0040 records all ten theorem archive statement checks with archive frozen-solution, frozen-proof, discharge-gate, and overall signature statuses MATCH. | MATCH | fenced | 1 | archive-statement-row-review | deviation 0 within tolerance 0.5 |
| Pass 0040 records all ten unique archive files under archives/pass-0040-remote-blobs/sha256 with archive SHA-256 matching pass 0039 remote raw bytes and external_call_required_for_replay false. | MATCH | fenced | 1 | archive-file-binding-review | deviation 0 within tolerance 0.5 |
| Pass 0040 validator result reports MATCH with theorem_count 10, archive_check_count 10, and unique_archive_file_count 10 using local archive files. | MATCH | fenced | 1 | validator-result-review | deviation 0 within tolerance 0.5 |
| Pass 0040 records packet 050 with sha256 4cb465d14bc4672b67ecaec6827f6bf0d2fabab1b4a36bd93fa18adf35f27ef9 and local steelman with sha256 e0f96bce831a6f06a6e07f61e1361e430db31d61345d66557eada0fefc8c0f4f. | MATCH | fenced | 1 | packet-presence-review | deviation 0 within tolerance 0.5 |
| Pass 0040 preserves non-promotion boundaries: it checks archived raw-source replay by digest only, does not re-run Lean, does not claim semantic proof review, and current_promoted_natural_laws remains none. | MATCH | fenced | 1 | non-promotion-boundary-review | deviation 0 within tolerance 0.5 |

## Measurement Evidence

| Claim | Method | Evidence |
| --- | --- | --- |
| Pass 0040 created a TheoremArchivedBlobStatementReplaySet/v1 artifact with status ARCHIVED_BLOB_STATEMENT_REPLAY_MATCH, theorem_count 10, archive_check_count 10, unique_archive_file_count 10, sha256 e45620662cc30976f8b1f814e5b0ceb3815c16f6e86e091364220fa286bfe654, and seal c38574335633bb119b7c14b8f7a69db44751f04f44bb3fd74c71df4e2a74818d. | archive-blob-schema-review | schema=TheoremArchivedBlobStatementReplaySet/v1; status=ARCHIVED_BLOB_STATEMENT_REPLAY_MATCH; theorem_count=10; archive_check_count=10; unique_archive_file_count=10; sha256=e45620662cc30976f8b1f814e5b0ceb3815c16f6e86e091364220fa286bfe654; seal=c38574335633bb119b7c14b8f7a69db44751f04f44bb3fd74c71df4e2a74818d |
| Pass 0040 records fixture fixtures/theorem-archived-blob-statement-replay-pass-0040.json with sha256 cc76916c782838deda0c4c19b5324279e0a3524497d3b75728459e9cedeea1f7 and seal e81a919446ab3e8184ad74cc444a8cbe628490c51a83d41edccb261a021c3a95. | fixture-binding-review | fixture sha256=cc76916c782838deda0c4c19b5324279e0a3524497d3b75728459e9cedeea1f7; fixture seal=e81a919446ab3e8184ad74cc444a8cbe628490c51a83d41edccb261a021c3a95 |
| Pass 0040 binds to pass 0039 remote raw-blob statement replay with sha256 0e13f8c76728c20d3cfdb298638da8c5054f9b2bdf4e6fd8db0f74065fb20376, seal c01eb59d75eb418f551e302b19dbaf47c4193373f72c4af5d229567fa96ebc58, and source status REMOTE_BLOB_STATEMENT_REPLAY_MATCH. | source-binding-review | remote_statement_replay_sha256=0e13f8c76728c20d3cfdb298638da8c5054f9b2bdf4e6fd8db0f74065fb20376; remote_statement_replay_seal=c01eb59d75eb418f551e302b19dbaf47c4193373f72c4af5d229567fa96ebc58; remote_statement_replay_status=REMOTE_BLOB_STATEMENT_REPLAY_MATCH |
| Pass 0040 records all ten theorem archive statement checks with archive frozen-solution, frozen-proof, discharge-gate, and overall signature statuses MATCH. | archive-statement-row-review | archive_check_count=10; all_archive_frozen_solution_match=true; all_archive_frozen_proof_match=true; all_archive_discharge_gates_match=true; all_archive_statement_checks_match=true |
| Pass 0040 records all ten unique archive files under archives/pass-0040-remote-blobs/sha256 with archive SHA-256 matching pass 0039 remote raw bytes and external_call_required_for_replay false. | archive-file-binding-review | unique_archive_file_count=10; all_archive_file_sha_match_pass0039=true; archive_root=archives/pass-0040-remote-blobs/sha256; external_call_performed_for_capture=true; external_call_required_for_replay=false; worktree_text_used_for_signatures=false |
| Pass 0040 validator result reports MATCH with theorem_count 10, archive_check_count 10, and unique_archive_file_count 10 using local archive files. | validator-result-review | schemas/pass-0040-theorem-archived-blob-statement-replay-validator-result.json status=MATCH; theorem_count=10; archive_check_count=10; unique_archive_file_count=10; local_archive_files=true |
| Pass 0040 records packet 050 with sha256 4cb465d14bc4672b67ecaec6827f6bf0d2fabab1b4a36bd93fa18adf35f27ef9 and local steelman with sha256 e0f96bce831a6f06a6e07f61e1361e430db31d61345d66557eada0fefc8c0f4f. | packet-presence-review | packets/050-theorem-archived-blob-statement-replay.md sha256=4cb465d14bc4672b67ecaec6827f6bf0d2fabab1b4a36bd93fa18adf35f27ef9; adversarial/pass-0040-archived-blob-statement-replay-steelman.md sha256=e0f96bce831a6f06a6e07f61e1361e430db31d61345d66557eada0fefc8c0f4f |
| Pass 0040 preserves non-promotion boundaries: it checks archived raw-source replay by digest only, does not re-run Lean, does not claim semantic proof review, and current_promoted_natural_laws remains none. | non-promotion-boundary-review | non_promotion_statement present; current_promoted_natural_laws=[]; steelman states archive replay is not semantic proof verification |
