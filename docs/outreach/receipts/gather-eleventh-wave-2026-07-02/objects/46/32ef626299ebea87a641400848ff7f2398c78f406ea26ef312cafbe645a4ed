# crucible report: Dogfood Pass 0043 Lake Dependency Cache Binding

## Summary

- thesis_id: `dfb13dcdd32a219f`
- thesis_seal: `dfb13dcdd32a219fa471c2aa10fd145a13651af1e5ed6fcea30a8c3e890a1114`
- assessment_seal: `a55bb92be117989e0e04d8e1b2202ea4f42a90f4f58a44d1e432e5b2ef175ef2`
- counts: MATCH 8 / DRIFT 0 / UNVERIFIABLE 0
- integrity: seals_ok=True, thesis_ok=True, verdicts_rederive=True

## Verdicts

| Claim | Status | Disposition | Margin | Method | Grounds |
| --- | --- | --- | ---: | --- | --- |
| Pass 0043 created a LakeDependencyCacheBindingSet/v1 artifact with status LAKE_DEPENDENCY_CACHE_BINDING_MATCH, package_count 9, sha256 393f71b91fb69d800aff7f81751517eb62af2ee0d098670ae97d4f16a869de22, and seal 8e88cd761c7ae0996c6d20bfeb78fb5cf9bf6083a3de1f09601a62463a5d665b. | MATCH | fenced | 1 | lake-dependency-schema-review | deviation 0 within tolerance 0.5 |
| Pass 0043 records fixture fixtures/lake-dependency-cache-binding-pass-0043.json with sha256 f5873cca174833d9f8e8e655586774d2a46487ee07a8b1710660e80eef5e3c5b and seal 4eb29447aeb8870d281f61e422bd4d4c0629dc3f812ec77368b5e11712e3f94d. | MATCH | fenced | 1 | fixture-binding-review | deviation 0 within tolerance 0.5 |
| Pass 0043 binds to pass 0042 full Lean source archive with sha256 83eefbfeab7e258aae80c8bb405bd93cc9dd7117804a3e84d3c74e1534142343, seal 0c5b4d29bf7ea2e72398278fd57c0cf23e5e297ce2d5d99cec84aab60e528d7c, and source status FULL_LEAN_SOURCE_ARCHIVE_MATCH. | MATCH | fenced | 1 | source-binding-review | deviation 0 within tolerance 0.5 |
| Pass 0043 records nine Lake manifest packages, nine present local caches, nine package HEADs matching the manifest, and nine clean package worktrees. | MATCH | fenced | 1 | dependency-cache-count-review | deviation 0 within tolerance 0.5 |
| Pass 0043 records all nine package origin URLs matching the Lake manifest URLs after .git suffix normalization. | MATCH | fenced | 1 | dependency-url-review | deviation 0 within tolerance 0.5 |
| Pass 0043 validator result reports MATCH with package_count 9 using local dependency cache checks. | MATCH | fenced | 1 | validator-result-review | deviation 0 within tolerance 0.5 |
| Pass 0043 records packet 053 with sha256 96228fb6991631c4f84466bef2111e67143efe86434170f8931ca0cea6413473 and local steelman with sha256 9138c8b3b1682a56afb2afba86b5de8a7fafba19e6f782eb3119fb1e252156ae. | MATCH | fenced | 1 | packet-presence-review | deviation 0 within tolerance 0.5 |
| Pass 0043 preserves non-promotion boundaries: it checks dependency cache identity only, does not run Lean, does not compile dependencies, and current_promoted_natural_laws remains none. | MATCH | fenced | 1 | non-promotion-boundary-review | deviation 0 within tolerance 0.5 |

## Measurement Evidence

| Claim | Method | Evidence |
| --- | --- | --- |
| Pass 0043 created a LakeDependencyCacheBindingSet/v1 artifact with status LAKE_DEPENDENCY_CACHE_BINDING_MATCH, package_count 9, sha256 393f71b91fb69d800aff7f81751517eb62af2ee0d098670ae97d4f16a869de22, and seal 8e88cd761c7ae0996c6d20bfeb78fb5cf9bf6083a3de1f09601a62463a5d665b. | lake-dependency-schema-review | schema=LakeDependencyCacheBindingSet/v1; status=LAKE_DEPENDENCY_CACHE_BINDING_MATCH; package_count=9; sha256=393f71b91fb69d800aff7f81751517eb62af2ee0d098670ae97d4f16a869de22; seal=8e88cd761c7ae0996c6d20bfeb78fb5cf9bf6083a3de1f09601a62463a5d665b |
| Pass 0043 records fixture fixtures/lake-dependency-cache-binding-pass-0043.json with sha256 f5873cca174833d9f8e8e655586774d2a46487ee07a8b1710660e80eef5e3c5b and seal 4eb29447aeb8870d281f61e422bd4d4c0629dc3f812ec77368b5e11712e3f94d. | fixture-binding-review | fixture sha256=f5873cca174833d9f8e8e655586774d2a46487ee07a8b1710660e80eef5e3c5b; fixture seal=4eb29447aeb8870d281f61e422bd4d4c0629dc3f812ec77368b5e11712e3f94d |
| Pass 0043 binds to pass 0042 full Lean source archive with sha256 83eefbfeab7e258aae80c8bb405bd93cc9dd7117804a3e84d3c74e1534142343, seal 0c5b4d29bf7ea2e72398278fd57c0cf23e5e297ce2d5d99cec84aab60e528d7c, and source status FULL_LEAN_SOURCE_ARCHIVE_MATCH. | source-binding-review | full_source_archive_sha256=83eefbfeab7e258aae80c8bb405bd93cc9dd7117804a3e84d3c74e1534142343; full_source_archive_seal=0c5b4d29bf7ea2e72398278fd57c0cf23e5e297ce2d5d99cec84aab60e528d7c; full_source_archive_status=FULL_LEAN_SOURCE_ARCHIVE_MATCH |
| Pass 0043 records nine Lake manifest packages, nine present local caches, nine package HEADs matching the manifest, and nine clean package worktrees. | dependency-cache-count-review | package_count=9; present_package_count=9; head_match_count=9; clean_package_count=9; all_package_heads_match_manifest=true |
| Pass 0043 records all nine package origin URLs matching the Lake manifest URLs after .git suffix normalization. | dependency-url-review | all_package_urls_match_manifest=true; url_normalization=.git_suffix |
| Pass 0043 validator result reports MATCH with package_count 9 using local dependency cache checks. | validator-result-review | schemas/pass-0043-lake-dependency-cache-binding-validator-result.json status=MATCH; package_count=9; local_dependency_cache_checks=true |
| Pass 0043 records packet 053 with sha256 96228fb6991631c4f84466bef2111e67143efe86434170f8931ca0cea6413473 and local steelman with sha256 9138c8b3b1682a56afb2afba86b5de8a7fafba19e6f782eb3119fb1e252156ae. | packet-presence-review | packets/053-lake-dependency-cache-binding.md sha256=96228fb6991631c4f84466bef2111e67143efe86434170f8931ca0cea6413473; adversarial/pass-0043-lake-dependency-cache-binding-steelman.md sha256=9138c8b3b1682a56afb2afba86b5de8a7fafba19e6f782eb3119fb1e252156ae |
| Pass 0043 preserves non-promotion boundaries: it checks dependency cache identity only, does not run Lean, does not compile dependencies, and current_promoted_natural_laws remains none. | non-promotion-boundary-review | non_promotion_statement present; current_promoted_natural_laws=[]; compiled_replay_status=NOT_RUN; steelman states matching package HEADs is not compilation |
