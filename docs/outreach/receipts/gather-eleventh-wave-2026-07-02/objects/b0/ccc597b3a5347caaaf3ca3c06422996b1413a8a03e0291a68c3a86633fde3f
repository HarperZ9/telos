# crucible report: Dogfood Pass 0041 Lean Toolchain Import Binding

## Summary

- thesis_id: `e8953b637df93b2f`
- thesis_seal: `e8953b637df93b2fc960e3cd089ea95b57eb4e2e9ed766646a098f79e585bbb1`
- assessment_seal: `0bfb7a2bd820fde1a43cba2553e2a2ed50eb83bd0fb2a790c36becb812831ebb`
- counts: MATCH 8 / DRIFT 0 / UNVERIFIABLE 0
- integrity: seals_ok=True, thesis_ok=True, verdicts_rederive=True

## Verdicts

| Claim | Status | Disposition | Margin | Method | Grounds |
| --- | --- | --- | ---: | --- | --- |
| Pass 0041 created a LeanToolchainImportBindingSet/v1 artifact with status LEAN_TOOLCHAIN_IMPORT_BINDING_MATCH, build_file_count 6, lean_module_count 16, sha256 ae72dadc5da817622374a9b5654f7389242f3e4f7b218e4c89387d364ef2b0e7, and seal e932959ff41df5260e5af88942184e45c2e9620b878db02b4ccbb609387c78b6. | MATCH | fenced | 1 | lean-toolchain-schema-review | deviation 0 within tolerance 0.5 |
| Pass 0041 records fixture fixtures/lean-toolchain-import-binding-pass-0041.json with sha256 5d4ff58b42595c47d1d8fccfec4fb6b913186cedc1e2894410a6784b584c5ea9 and seal 98ed8df0f610d30b445ee365c4198b8b3e62fbd43d6514ad3920106ea10b8eb6. | MATCH | fenced | 1 | fixture-binding-review | deviation 0 within tolerance 0.5 |
| Pass 0041 binds to pass 0040 archived blob statement replay with sha256 e45620662cc30976f8b1f814e5b0ceb3815c16f6e86e091364220fa286bfe654, seal c38574335633bb119b7c14b8f7a69db44751f04f44bb3fd74c71df4e2a74818d, and source status ARCHIVED_BLOB_STATEMENT_REPLAY_MATCH. | MATCH | fenced | 1 | source-binding-review | deviation 0 within tolerance 0.5 |
| Pass 0041 binds lean-toolchain leanprover/lean4:v4.31.0, mathlib inputRev v4.31.0, mathlib rev fabf563a7c95a166b8d7b6efca11c8b4dc9d911f, and Lake manifest package count 9. | MATCH | fenced | 1 | toolchain-summary-review | deviation 0 within tolerance 0.5 |
| Pass 0041 records 16 local Lean modules, 41 local import edges, one external import edge, and the external edge targets Mathlib. | MATCH | fenced | 1 | import-graph-review | deviation 0 within tolerance 0.5 |
| Pass 0041 records six local files needed beyond the pass 0040 archive for compiled replay planning, and compiled_replay_status remains NOT_RUN. | MATCH | fenced | 1 | compiled-replay-delta-review | deviation 0 within tolerance 0.5 |
| Pass 0041 records packet 051 with sha256 7a139d1eab8c4383765473b2fc23df50165b51e103b9f1a8cdafd813cf19ef79, local steelman with sha256 93d6b2638a709f4833f4ae1d8efb28e875d6fe8a1b1aec5c0d04b50e4af0c425, and validator result sha256 9ac1b3f6708a74850c98e96a18695e08fa2a4138045350ab35b2752834bac2b5. | MATCH | fenced | 1 | packet-presence-review | deviation 0 within tolerance 0.5 |
| Pass 0041 preserves non-promotion boundaries: it discovers toolchain/import metadata only, does not run Lean, does not claim semantic proof review, and current_promoted_natural_laws remains none. | MATCH | fenced | 1 | non-promotion-boundary-review | deviation 0 within tolerance 0.5 |

## Measurement Evidence

| Claim | Method | Evidence |
| --- | --- | --- |
| Pass 0041 created a LeanToolchainImportBindingSet/v1 artifact with status LEAN_TOOLCHAIN_IMPORT_BINDING_MATCH, build_file_count 6, lean_module_count 16, sha256 ae72dadc5da817622374a9b5654f7389242f3e4f7b218e4c89387d364ef2b0e7, and seal e932959ff41df5260e5af88942184e45c2e9620b878db02b4ccbb609387c78b6. | lean-toolchain-schema-review | schema=LeanToolchainImportBindingSet/v1; status=LEAN_TOOLCHAIN_IMPORT_BINDING_MATCH; build_file_count=6; lean_module_count=16; sha256=ae72dadc5da817622374a9b5654f7389242f3e4f7b218e4c89387d364ef2b0e7; seal=e932959ff41df5260e5af88942184e45c2e9620b878db02b4ccbb609387c78b6 |
| Pass 0041 records fixture fixtures/lean-toolchain-import-binding-pass-0041.json with sha256 5d4ff58b42595c47d1d8fccfec4fb6b913186cedc1e2894410a6784b584c5ea9 and seal 98ed8df0f610d30b445ee365c4198b8b3e62fbd43d6514ad3920106ea10b8eb6. | fixture-binding-review | fixture sha256=5d4ff58b42595c47d1d8fccfec4fb6b913186cedc1e2894410a6784b584c5ea9; fixture seal=98ed8df0f610d30b445ee365c4198b8b3e62fbd43d6514ad3920106ea10b8eb6 |
| Pass 0041 binds to pass 0040 archived blob statement replay with sha256 e45620662cc30976f8b1f814e5b0ceb3815c16f6e86e091364220fa286bfe654, seal c38574335633bb119b7c14b8f7a69db44751f04f44bb3fd74c71df4e2a74818d, and source status ARCHIVED_BLOB_STATEMENT_REPLAY_MATCH. | source-binding-review | archive_statement_replay_sha256=e45620662cc30976f8b1f814e5b0ceb3815c16f6e86e091364220fa286bfe654; archive_statement_replay_seal=c38574335633bb119b7c14b8f7a69db44751f04f44bb3fd74c71df4e2a74818d; archive_statement_replay_status=ARCHIVED_BLOB_STATEMENT_REPLAY_MATCH |
| Pass 0041 binds lean-toolchain leanprover/lean4:v4.31.0, mathlib inputRev v4.31.0, mathlib rev fabf563a7c95a166b8d7b6efca11c8b4dc9d911f, and Lake manifest package count 9. | toolchain-summary-review | toolchain=leanprover/lean4:v4.31.0; mathlib_input_rev=v4.31.0; mathlib_rev=fabf563a7c95a166b8d7b6efca11c8b4dc9d911f; lake_manifest_package_count=9 |
| Pass 0041 records 16 local Lean modules, 41 local import edges, one external import edge, and the external edge targets Mathlib. | import-graph-review | lean_module_count=16; local_import_edge_count=41; external_import_edge_count=1; external_import=Mathlib |
| Pass 0041 records six local files needed beyond the pass 0040 archive for compiled replay planning, and compiled_replay_status remains NOT_RUN. | compiled-replay-delta-review | archived_source_file_count=10; needed_for_compiled_replay_count=6; compiled_replay_status=NOT_RUN |
| Pass 0041 records packet 051 with sha256 7a139d1eab8c4383765473b2fc23df50165b51e103b9f1a8cdafd813cf19ef79, local steelman with sha256 93d6b2638a709f4833f4ae1d8efb28e875d6fe8a1b1aec5c0d04b50e4af0c425, and validator result sha256 9ac1b3f6708a74850c98e96a18695e08fa2a4138045350ab35b2752834bac2b5. | packet-presence-review | packets/051-lean-toolchain-import-binding.md sha256=7a139d1eab8c4383765473b2fc23df50165b51e103b9f1a8cdafd813cf19ef79; adversarial/pass-0041-lean-toolchain-import-binding-steelman.md sha256=93d6b2638a709f4833f4ae1d8efb28e875d6fe8a1b1aec5c0d04b50e4af0c425; schemas/pass-0041-lean-toolchain-import-binding-validator-result.json sha256=9ac1b3f6708a74850c98e96a18695e08fa2a4138045350ab35b2752834bac2b5 |
| Pass 0041 preserves non-promotion boundaries: it discovers toolchain/import metadata only, does not run Lean, does not claim semantic proof review, and current_promoted_natural_laws remains none. | non-promotion-boundary-review | non_promotion_statement present; current_promoted_natural_laws=[]; compiled_replay_status=NOT_RUN; steelman states toolchain discovery is not compilation |
