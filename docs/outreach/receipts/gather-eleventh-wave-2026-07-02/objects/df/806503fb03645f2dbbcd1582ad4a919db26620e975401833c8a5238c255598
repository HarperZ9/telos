# crucible report: Dogfood Pass 0036 Theorem Source-Ref Integrity

## Summary

- thesis_id: `7dbf304cafffbe06`
- thesis_seal: `7dbf304cafffbe06190074cab390daf6f489fb285867b68bb05130507567d72d`
- assessment_seal: `fabd053f026990a950db512f2f03278abff787f2e03f47f7daeccf423068570d`
- counts: MATCH 8 / DRIFT 0 / UNVERIFIABLE 0
- integrity: seals_ok=True, thesis_ok=True, verdicts_rederive=True

## Verdicts

| Claim | Status | Disposition | Margin | Method | Grounds |
| --- | --- | --- | ---: | --- | --- |
| Pass 0036 created a TheoremSourceRefIntegritySet/v1 artifact with status SOURCE_REF_INTEGRITY_MATCH, source_ref_count 40, unique_file_count 10, sha256 74d89981ae7598f7a7381f6fdbb1196cf9be97ca854688a49c4e3c4bce9f6f6f, and seal 68382866e7e78895eb3d7fd0d613fcc8b17afc30398b7823cb198702262da2fb. | MATCH | fenced | 1 | source-ref-schema-review | deviation 0 within tolerance 0.5 |
| Pass 0036 records fixture fixtures/theorem-source-ref-integrity-pass-0036.json with sha256 f89011da69ee6d28e2a67827e9f3d45cea37a2d0b3a85289cc1d34170e1e8830 and seal 06a1fd9729ab2d03d12623c84d4867626a118524b2a438c47f3ca3391e4dbdd3. | MATCH | fenced | 1 | fixture-binding-review | deviation 0 within tolerance 0.5 |
| Pass 0036 records the pipeline-math source checkout at commit 69d7df765a8f377a5e0628c6d36c088bce7642c9 with git_status_clean true and worktree_eol_lf true. | MATCH | fenced | 1 | repo-receipt-review | deviation 0 within tolerance 0.5 |
| Pass 0036 records all 40 theorem source refs with line_status MATCH and symbol_present true. | MATCH | fenced | 1 | source-ref-row-review | deviation 0 within tolerance 0.5 |
| Pass 0036 binds every source-ref row to Git path, Git blob id, Git blob SHA-256, worktree SHA-256, line SHA-256, line span, and context SHA-256. | MATCH | fenced | 1 | hash-binding-review | deviation 0 within tolerance 0.5 |
| Pass 0036 validator result reports MATCH with source_ref_count 40 and unique_file_count 10. | MATCH | fenced | 1 | validator-result-review | deviation 0 within tolerance 0.5 |
| Pass 0036 records packet 046 with sha256 50aa1770aaeb66b2dd3e54f8239207ae4bb4f4f29e5827622fe1384aeb4f339c and local steelman with sha256 4911f4b39fae658a17b1922acfd3fe4f354f3d54769835886252a58556e48a44. | MATCH | fenced | 1 | packet-presence-review | deviation 0 within tolerance 0.5 |
| Pass 0036 preserves non-promotion boundaries: it verifies source-reference integrity only, does not re-run Lean, does not claim semantic proof review, and current_promoted_natural_laws remains none. | MATCH | fenced | 1 | non-promotion-boundary-review | deviation 0 within tolerance 0.5 |

## Measurement Evidence

| Claim | Method | Evidence |
| --- | --- | --- |
| Pass 0036 created a TheoremSourceRefIntegritySet/v1 artifact with status SOURCE_REF_INTEGRITY_MATCH, source_ref_count 40, unique_file_count 10, sha256 74d89981ae7598f7a7381f6fdbb1196cf9be97ca854688a49c4e3c4bce9f6f6f, and seal 68382866e7e78895eb3d7fd0d613fcc8b17afc30398b7823cb198702262da2fb. | source-ref-schema-review | schema=TheoremSourceRefIntegritySet/v1; status=SOURCE_REF_INTEGRITY_MATCH; source_ref_count=40; unique_file_count=10; sha256=74d89981ae7598f7a7381f6fdbb1196cf9be97ca854688a49c4e3c4bce9f6f6f; seal=68382866e7e78895eb3d7fd0d613fcc8b17afc30398b7823cb198702262da2fb |
| Pass 0036 records fixture fixtures/theorem-source-ref-integrity-pass-0036.json with sha256 f89011da69ee6d28e2a67827e9f3d45cea37a2d0b3a85289cc1d34170e1e8830 and seal 06a1fd9729ab2d03d12623c84d4867626a118524b2a438c47f3ca3391e4dbdd3. | fixture-binding-review | fixture sha256=f89011da69ee6d28e2a67827e9f3d45cea37a2d0b3a85289cc1d34170e1e8830; fixture seal=06a1fd9729ab2d03d12623c84d4867626a118524b2a438c47f3ca3391e4dbdd3 |
| Pass 0036 records the pipeline-math source checkout at commit 69d7df765a8f377a5e0628c6d36c088bce7642c9 with git_status_clean true and worktree_eol_lf true. | repo-receipt-review | repo_receipt.commit=69d7df765a8f377a5e0628c6d36c088bce7642c9; repo_receipt.git_status_clean=true; verifier_measurements.worktree_eol_lf=true |
| Pass 0036 records all 40 theorem source refs with line_status MATCH and symbol_present true. | source-ref-row-review | source_ref_count=40; all line_status=MATCH; all symbol_present=true |
| Pass 0036 binds every source-ref row to Git path, Git blob id, Git blob SHA-256, worktree SHA-256, line SHA-256, line span, and context SHA-256. | hash-binding-review | all rows include git_path; all rows include file_git_blob_id; all rows include file_git_blob_sha256; all rows include file_worktree_sha256; all rows include line_text_sha256; all rows include line_span; all rows include context_sha256 |
| Pass 0036 validator result reports MATCH with source_ref_count 40 and unique_file_count 10. | validator-result-review | schemas/pass-0036-theorem-source-ref-validator-result.json status=MATCH; source_ref_count=40; unique_file_count=10 |
| Pass 0036 records packet 046 with sha256 50aa1770aaeb66b2dd3e54f8239207ae4bb4f4f29e5827622fe1384aeb4f339c and local steelman with sha256 4911f4b39fae658a17b1922acfd3fe4f354f3d54769835886252a58556e48a44. | packet-presence-review | packets/046-theorem-source-ref-integrity.md sha256=50aa1770aaeb66b2dd3e54f8239207ae4bb4f4f29e5827622fe1384aeb4f339c; adversarial/pass-0036-source-ref-integrity-steelman.md sha256=4911f4b39fae658a17b1922acfd3fe4f354f3d54769835886252a58556e48a44 |
| Pass 0036 preserves non-promotion boundaries: it verifies source-reference integrity only, does not re-run Lean, does not claim semantic proof review, and current_promoted_natural_laws remains none. | non-promotion-boundary-review | non_promotion_statement present; current_promoted_natural_laws=[]; steelman states declaration-line binding is not full semantic proof review |
