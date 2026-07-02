# crucible report: Dogfood Pass 0042 Full Lean Source Archive

## Summary

- thesis_id: `c97a7cc65ccdafec`
- thesis_seal: `c97a7cc65ccdafec761d01a8055680ce7fa4f44ae6d5d524f5077ead61c2ebc2`
- assessment_seal: `2da430cbbf545e82930b893c9bbc5be224ed27fedc91b71c5e4f2581e8c37011`
- counts: MATCH 8 / DRIFT 0 / UNVERIFIABLE 0
- integrity: seals_ok=True, thesis_ok=True, verdicts_rederive=True

## Verdicts

| Claim | Status | Disposition | Margin | Method | Grounds |
| --- | --- | --- | ---: | --- | --- |
| Pass 0042 created a FullLeanSourceArchiveSet/v1 artifact with status FULL_LEAN_SOURCE_ARCHIVE_MATCH, role_record_count 22, unique_archive_file_count 21, sha256 83eefbfeab7e258aae80c8bb405bd93cc9dd7117804a3e84d3c74e1534142343, and seal 0c5b4d29bf7ea2e72398278fd57c0cf23e5e297ce2d5d99cec84aab60e528d7c. | MATCH | fenced | 1 | full-source-archive-schema-review | deviation 0 within tolerance 0.5 |
| Pass 0042 records fixture fixtures/full-lean-source-archive-pass-0042.json with sha256 2a397cee6f014ee2a6c1113637d880de264324c6591d7898533d8047e8b1e83c and seal db500e73b024ef1b1af29c4b32efeafb19faf4de3ad3e85234c75c93e1ceb9e8. | MATCH | fenced | 1 | fixture-binding-review | deviation 0 within tolerance 0.5 |
| Pass 0042 binds to pass 0041 Lean toolchain/import binding with sha256 ae72dadc5da817622374a9b5654f7389242f3e4f7b218e4c89387d364ef2b0e7, seal e932959ff41df5260e5af88942184e45c2e9620b878db02b4ccbb609387c78b6, and source status LEAN_TOOLCHAIN_IMPORT_BINDING_MATCH. | MATCH | fenced | 1 | source-binding-review | deviation 0 within tolerance 0.5 |
| Pass 0042 records 16 Lean module records, 6 build file records, 22 role records, 21 unique archived files, and exactly one module/build overlap. | MATCH | fenced | 1 | archive-count-review | deviation 0 within tolerance 0.5 |
| Pass 0042 records all archived file SHA-256 values matching pass 0041 and archives all six pass 0041 files needed for compiled replay planning. | MATCH | fenced | 1 | source-archive-integrity-review | deviation 0 within tolerance 0.5 |
| Pass 0042 validator result reports MATCH with role_record_count 22 and unique_archive_file_count 21 using local archive files. | MATCH | fenced | 1 | validator-result-review | deviation 0 within tolerance 0.5 |
| Pass 0042 records packet 052 with sha256 85c149c0167b4d94efd3e86f8d338f2906f2fefe633ceaed41ff613b76665cfa and local steelman with sha256 dbd810db88510ad61c57854d63e2db73d07d9b346b97c0a1cac9153f5353ed1e. | MATCH | fenced | 1 | packet-presence-review | deviation 0 within tolerance 0.5 |
| Pass 0042 preserves non-promotion boundaries: it archives source/build inputs only, does not run Lean, does not claim semantic proof review, and current_promoted_natural_laws remains none. | MATCH | fenced | 1 | non-promotion-boundary-review | deviation 0 within tolerance 0.5 |

## Measurement Evidence

| Claim | Method | Evidence |
| --- | --- | --- |
| Pass 0042 created a FullLeanSourceArchiveSet/v1 artifact with status FULL_LEAN_SOURCE_ARCHIVE_MATCH, role_record_count 22, unique_archive_file_count 21, sha256 83eefbfeab7e258aae80c8bb405bd93cc9dd7117804a3e84d3c74e1534142343, and seal 0c5b4d29bf7ea2e72398278fd57c0cf23e5e297ce2d5d99cec84aab60e528d7c. | full-source-archive-schema-review | schema=FullLeanSourceArchiveSet/v1; status=FULL_LEAN_SOURCE_ARCHIVE_MATCH; role_record_count=22; unique_archive_file_count=21; sha256=83eefbfeab7e258aae80c8bb405bd93cc9dd7117804a3e84d3c74e1534142343; seal=0c5b4d29bf7ea2e72398278fd57c0cf23e5e297ce2d5d99cec84aab60e528d7c |
| Pass 0042 records fixture fixtures/full-lean-source-archive-pass-0042.json with sha256 2a397cee6f014ee2a6c1113637d880de264324c6591d7898533d8047e8b1e83c and seal db500e73b024ef1b1af29c4b32efeafb19faf4de3ad3e85234c75c93e1ceb9e8. | fixture-binding-review | fixture sha256=2a397cee6f014ee2a6c1113637d880de264324c6591d7898533d8047e8b1e83c; fixture seal=db500e73b024ef1b1af29c4b32efeafb19faf4de3ad3e85234c75c93e1ceb9e8 |
| Pass 0042 binds to pass 0041 Lean toolchain/import binding with sha256 ae72dadc5da817622374a9b5654f7389242f3e4f7b218e4c89387d364ef2b0e7, seal e932959ff41df5260e5af88942184e45c2e9620b878db02b4ccbb609387c78b6, and source status LEAN_TOOLCHAIN_IMPORT_BINDING_MATCH. | source-binding-review | lean_toolchain_import_binding_sha256=ae72dadc5da817622374a9b5654f7389242f3e4f7b218e4c89387d364ef2b0e7; lean_toolchain_import_binding_seal=e932959ff41df5260e5af88942184e45c2e9620b878db02b4ccbb609387c78b6; lean_toolchain_import_binding_status=LEAN_TOOLCHAIN_IMPORT_BINDING_MATCH |
| Pass 0042 records 16 Lean module records, 6 build file records, 22 role records, 21 unique archived files, and exactly one module/build overlap. | archive-count-review | lean_module_count=16; build_file_count=6; role_record_count=22; unique_archive_file_count=21; module_build_overlap_count=1 |
| Pass 0042 records all archived file SHA-256 values matching pass 0041 and archives all six pass 0041 files needed for compiled replay planning. | source-archive-integrity-review | all_archived_sha_match_pass0041=true; needed_for_compiled_replay_count=6; needed_for_compiled_replay_archived_count=6; external_call_required_for_replay=false |
| Pass 0042 validator result reports MATCH with role_record_count 22 and unique_archive_file_count 21 using local archive files. | validator-result-review | schemas/pass-0042-full-lean-source-archive-validator-result.json status=MATCH; role_record_count=22; unique_archive_file_count=21; local_archive_files=true |
| Pass 0042 records packet 052 with sha256 85c149c0167b4d94efd3e86f8d338f2906f2fefe633ceaed41ff613b76665cfa and local steelman with sha256 dbd810db88510ad61c57854d63e2db73d07d9b346b97c0a1cac9153f5353ed1e. | packet-presence-review | packets/052-full-lean-source-archive.md sha256=85c149c0167b4d94efd3e86f8d338f2906f2fefe633ceaed41ff613b76665cfa; adversarial/pass-0042-full-lean-source-archive-steelman.md sha256=dbd810db88510ad61c57854d63e2db73d07d9b346b97c0a1cac9153f5353ed1e |
| Pass 0042 preserves non-promotion boundaries: it archives source/build inputs only, does not run Lean, does not claim semantic proof review, and current_promoted_natural_laws remains none. | non-promotion-boundary-review | non_promotion_statement present; current_promoted_natural_laws=[]; compiled_replay_status=NOT_RUN; steelman states source archive is not a successful Lean build |
