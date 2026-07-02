# crucible report: Dogfood Pass 0038 Git Blob Statement Replay

## Summary

- thesis_id: `d6d119b3e807945b`
- thesis_seal: `d6d119b3e807945b2405f0b48da345fa221ef4477232b26431e26ad48fd3deba`
- assessment_seal: `be23d83f3ae1a2c366630fc95291baf7ecc4e6434c63cb99ea1d03d44938ae97`
- counts: MATCH 8 / DRIFT 0 / UNVERIFIABLE 0
- integrity: seals_ok=True, thesis_ok=True, verdicts_rederive=True

## Verdicts

| Claim | Status | Disposition | Margin | Method | Grounds |
| --- | --- | --- | ---: | --- | --- |
| Pass 0038 created a TheoremBlobStatementReplaySet/v1 artifact with status BLOB_STATEMENT_REPLAY_MATCH, theorem_count 10, blob_check_count 10, unique_blob_file_count 10, sha256 9ee5d5c8330911c04cc5de9a8a5856d18a46373a8a641e6f3fe3c2cffa4c2915, and seal 53541e1bdcb049e8823dff70b6f20b873a5dabea3ce63a854bdcdd53133e43bd. | MATCH | fenced | 1 | blob-statement-schema-review | deviation 0 within tolerance 0.5 |
| Pass 0038 records fixture fixtures/theorem-blob-statement-replay-pass-0038.json with sha256 9d6bef985d4440d10110b7398bee1fbb74059b9ac6f55512910e36932edbaf26 and seal ca0214a4d5693a02d5fac1d441058ea3c773f30307abcfec3514004f71c12848. | MATCH | fenced | 1 | fixture-binding-review | deviation 0 within tolerance 0.5 |
| Pass 0038 binds to pass 0037 statement equivalence and pass 0036 source-ref integrity with the recorded SHA-256 and seals, and source statuses STATEMENT_EQUIVALENCE_MATCH and SOURCE_REF_INTEGRITY_MATCH. | MATCH | fenced | 1 | source-binding-review | deviation 0 within tolerance 0.5 |
| Pass 0038 records all ten theorem blob statement checks with frozen-solution, frozen-proof, discharge-gate, and overall blob signature statuses MATCH. | MATCH | fenced | 1 | blob-statement-row-review | deviation 0 within tolerance 0.5 |
| Pass 0038 records all ten unique blob files with Git blob SHA-256 and blob id matching pass 0036 source-ref integrity rows. | MATCH | fenced | 1 | blob-file-binding-review | deviation 0 within tolerance 0.5 |
| Pass 0038 validator result reports MATCH with theorem_count 10, blob_check_count 10, and unique_blob_file_count 10. | MATCH | fenced | 1 | validator-result-review | deviation 0 within tolerance 0.5 |
| Pass 0038 records packet 048 with sha256 751c40c4ad423e60ee375452cccbf3624ef6fd7e3c5ddf8ffd12356babef50ad and local steelman with sha256 09b2d1e186fbfcbfdfcfe64473a915b66eaf409f36786940a87ae06b7fc2b52c. | MATCH | fenced | 1 | packet-presence-review | deviation 0 within tolerance 0.5 |
| Pass 0038 preserves non-promotion boundaries: it checks source-signature replay from Git blob bytes only, does not re-run Lean, does not claim semantic proof review, and current_promoted_natural_laws remains none. | MATCH | fenced | 1 | non-promotion-boundary-review | deviation 0 within tolerance 0.5 |

## Measurement Evidence

| Claim | Method | Evidence |
| --- | --- | --- |
| Pass 0038 created a TheoremBlobStatementReplaySet/v1 artifact with status BLOB_STATEMENT_REPLAY_MATCH, theorem_count 10, blob_check_count 10, unique_blob_file_count 10, sha256 9ee5d5c8330911c04cc5de9a8a5856d18a46373a8a641e6f3fe3c2cffa4c2915, and seal 53541e1bdcb049e8823dff70b6f20b873a5dabea3ce63a854bdcdd53133e43bd. | blob-statement-schema-review | schema=TheoremBlobStatementReplaySet/v1; status=BLOB_STATEMENT_REPLAY_MATCH; theorem_count=10; blob_check_count=10; unique_blob_file_count=10; sha256=9ee5d5c8330911c04cc5de9a8a5856d18a46373a8a641e6f3fe3c2cffa4c2915; seal=53541e1bdcb049e8823dff70b6f20b873a5dabea3ce63a854bdcdd53133e43bd |
| Pass 0038 records fixture fixtures/theorem-blob-statement-replay-pass-0038.json with sha256 9d6bef985d4440d10110b7398bee1fbb74059b9ac6f55512910e36932edbaf26 and seal ca0214a4d5693a02d5fac1d441058ea3c773f30307abcfec3514004f71c12848. | fixture-binding-review | fixture sha256=9d6bef985d4440d10110b7398bee1fbb74059b9ac6f55512910e36932edbaf26; fixture seal=ca0214a4d5693a02d5fac1d441058ea3c773f30307abcfec3514004f71c12848 |
| Pass 0038 binds to pass 0037 statement equivalence and pass 0036 source-ref integrity with the recorded SHA-256 and seals, and source statuses STATEMENT_EQUIVALENCE_MATCH and SOURCE_REF_INTEGRITY_MATCH. | source-binding-review | statement_equivalence_sha256=a0928a953f609aa5ea96aecc79e355a0d5aaab949761d4efa4b1b704210986bf; statement_equivalence_seal=78ede605591460b7a2aa8fee7e2ebca0f56688575e5c9ce7ab919f2948a0934f; statement_equivalence_status=STATEMENT_EQUIVALENCE_MATCH; source_ref_integrity_sha256=74d89981ae7598f7a7381f6fdbb1196cf9be97ca854688a49c4e3c4bce9f6f6f; source_ref_integrity_seal=68382866e7e78895eb3d7fd0d613fcc8b17afc30398b7823cb198702262da2fb; source_ref_integrity_status=SOURCE_REF_INTEGRITY_MATCH |
| Pass 0038 records all ten theorem blob statement checks with frozen-solution, frozen-proof, discharge-gate, and overall blob signature statuses MATCH. | blob-statement-row-review | blob_check_count=10; all_blob_frozen_solution_match=true; all_blob_frozen_proof_match=true; all_blob_discharge_gates_match=true; all_blob_statement_checks_match=true |
| Pass 0038 records all ten unique blob files with Git blob SHA-256 and blob id matching pass 0036 source-ref integrity rows. | blob-file-binding-review | unique_blob_file_count=10; all_blob_file_sha_match_pass0036=true; worktree_text_used_for_signatures=false |
| Pass 0038 validator result reports MATCH with theorem_count 10, blob_check_count 10, and unique_blob_file_count 10. | validator-result-review | schemas/pass-0038-theorem-blob-statement-replay-validator-result.json status=MATCH; theorem_count=10; blob_check_count=10; unique_blob_file_count=10 |
| Pass 0038 records packet 048 with sha256 751c40c4ad423e60ee375452cccbf3624ef6fd7e3c5ddf8ffd12356babef50ad and local steelman with sha256 09b2d1e186fbfcbfdfcfe64473a915b66eaf409f36786940a87ae06b7fc2b52c. | packet-presence-review | packets/048-theorem-blob-statement-replay.md sha256=751c40c4ad423e60ee375452cccbf3624ef6fd7e3c5ddf8ffd12356babef50ad; adversarial/pass-0038-blob-statement-replay-steelman.md sha256=09b2d1e186fbfcbfdfcfe64473a915b66eaf409f36786940a87ae06b7fc2b52c |
| Pass 0038 preserves non-promotion boundaries: it checks source-signature replay from Git blob bytes only, does not re-run Lean, does not claim semantic proof review, and current_promoted_natural_laws remains none. | non-promotion-boundary-review | non_promotion_statement present; current_promoted_natural_laws=[]; steelman states blob replay is not semantic proof verification |
