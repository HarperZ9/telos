# crucible report: Dogfood Pass 0044 Lean/Lake Executable Preflight

## Summary

- thesis_id: `2a61d018b04208e7`
- thesis_seal: `2a61d018b04208e7380b792f260a0a90c875c042bd3028a7fb0fc6e45493eb8e`
- assessment_seal: `07766394f2a3f056e117bffe51ce4ede154715f348903c1cf273399846b827be`
- counts: MATCH 8 / DRIFT 0 / UNVERIFIABLE 0
- integrity: seals_ok=True, thesis_ok=True, verdicts_rederive=True

## Verdicts

| Claim | Status | Disposition | Margin | Method | Grounds |
| --- | --- | --- | ---: | --- | --- |
| Pass 0044 created a LeanLakeExecutablePreflightSet/v1 artifact with status LEAN_LAKE_EXECUTABLE_PREFLIGHT_BLOCKED, compiled_replay_admissible false, sha256 d98513f50b384ed38e4d52d6379916bc6b43dacc318571e0299ecd1d3dcc055f, and seal 7139ea2e8ed154dcb5069fd5d5433fec85103b88d9bf309450dfd1193a6de607. | MATCH | fenced | 1 | lean-lake-preflight-schema-review | deviation 0 within tolerance 0.5 |
| Pass 0044 records fixture fixtures/lean-lake-executable-preflight-pass-0044.json with sha256 51f60da2e6581cf87b26111818060e37c59af0dec859f43df8b67bbe9e1b8898 and seal 7eb73ddc3f379c7c51a31fe570be2430171a8ad3242ad0e7bc582998f7959746. | MATCH | fenced | 1 | fixture-binding-review | deviation 0 within tolerance 0.5 |
| Pass 0044 binds to pass 0043 Lake dependency cache binding with sha256 393f71b91fb69d800aff7f81751517eb62af2ee0d098670ae97d4f16a869de22, seal 8e88cd761c7ae0996c6d20bfeb78fb5cf9bf6083a3de1f09601a62463a5d665b, and source status LAKE_DEPENDENCY_CACHE_BINDING_MATCH. | MATCH | fenced | 1 | source-binding-review | deviation 0 within tolerance 0.5 |
| Pass 0044 records expected toolchain leanprover/lean4:v4.31.0, lake_on_path false, lean_on_path false, elan_on_path false, and common_elan_candidates_present 0. | MATCH | fenced | 1 | executable-availability-review | deviation 0 within tolerance 0.5 |
| Pass 0044 records lakefile_name Prob4b, manifest_name Prob27b, and project_name_match false as a preflight signal. | MATCH | fenced | 1 | lake-project-name-review | deviation 0 within tolerance 0.5 |
| Pass 0044 validator result reports MATCH with compiled_replay_admissible false. | MATCH | fenced | 1 | validator-result-review | deviation 0 within tolerance 0.5 |
| Pass 0044 records packet 054 with sha256 91e38389327c8daee3c939e605a43213f8001707d3ade0a9ca2bfaa3107db570 and local steelman with sha256 daf30c73299f750087984036939bcc8b77f23b59cc083bb1b2838c221273155f. | MATCH | fenced | 1 | packet-presence-review | deviation 0 within tolerance 0.5 |
| Pass 0044 preserves non-promotion boundaries: it is an executable preflight only, does not run Lean or lake build, and current_promoted_natural_laws remains none. | MATCH | fenced | 1 | non-promotion-boundary-review | deviation 0 within tolerance 0.5 |

## Measurement Evidence

| Claim | Method | Evidence |
| --- | --- | --- |
| Pass 0044 created a LeanLakeExecutablePreflightSet/v1 artifact with status LEAN_LAKE_EXECUTABLE_PREFLIGHT_BLOCKED, compiled_replay_admissible false, sha256 d98513f50b384ed38e4d52d6379916bc6b43dacc318571e0299ecd1d3dcc055f, and seal 7139ea2e8ed154dcb5069fd5d5433fec85103b88d9bf309450dfd1193a6de607. | lean-lake-preflight-schema-review | schema=LeanLakeExecutablePreflightSet/v1; status=LEAN_LAKE_EXECUTABLE_PREFLIGHT_BLOCKED; compiled_replay_admissible=false; sha256=d98513f50b384ed38e4d52d6379916bc6b43dacc318571e0299ecd1d3dcc055f; seal=7139ea2e8ed154dcb5069fd5d5433fec85103b88d9bf309450dfd1193a6de607 |
| Pass 0044 records fixture fixtures/lean-lake-executable-preflight-pass-0044.json with sha256 51f60da2e6581cf87b26111818060e37c59af0dec859f43df8b67bbe9e1b8898 and seal 7eb73ddc3f379c7c51a31fe570be2430171a8ad3242ad0e7bc582998f7959746. | fixture-binding-review | fixture sha256=51f60da2e6581cf87b26111818060e37c59af0dec859f43df8b67bbe9e1b8898; fixture seal=7eb73ddc3f379c7c51a31fe570be2430171a8ad3242ad0e7bc582998f7959746 |
| Pass 0044 binds to pass 0043 Lake dependency cache binding with sha256 393f71b91fb69d800aff7f81751517eb62af2ee0d098670ae97d4f16a869de22, seal 8e88cd761c7ae0996c6d20bfeb78fb5cf9bf6083a3de1f09601a62463a5d665b, and source status LAKE_DEPENDENCY_CACHE_BINDING_MATCH. | source-binding-review | dependency_cache_binding_sha256=393f71b91fb69d800aff7f81751517eb62af2ee0d098670ae97d4f16a869de22; dependency_cache_binding_seal=8e88cd761c7ae0996c6d20bfeb78fb5cf9bf6083a3de1f09601a62463a5d665b; dependency_cache_binding_status=LAKE_DEPENDENCY_CACHE_BINDING_MATCH |
| Pass 0044 records expected toolchain leanprover/lean4:v4.31.0, lake_on_path false, lean_on_path false, elan_on_path false, and common_elan_candidates_present 0. | executable-availability-review | expected_toolchain=leanprover/lean4:v4.31.0; lake_on_path=false; lean_on_path=false; elan_on_path=false; common_elan_candidates_present=0 |
| Pass 0044 records lakefile_name Prob4b, manifest_name Prob27b, and project_name_match false as a preflight signal. | lake-project-name-review | lakefile_name=Prob4b; manifest_name=Prob27b; project_name_match=false |
| Pass 0044 validator result reports MATCH with compiled_replay_admissible false. | validator-result-review | schemas/pass-0044-lean-lake-executable-preflight-validator-result.json status=MATCH; compiled_replay_admissible=false |
| Pass 0044 records packet 054 with sha256 91e38389327c8daee3c939e605a43213f8001707d3ade0a9ca2bfaa3107db570 and local steelman with sha256 daf30c73299f750087984036939bcc8b77f23b59cc083bb1b2838c221273155f. | packet-presence-review | packets/054-lean-lake-executable-preflight.md sha256=91e38389327c8daee3c939e605a43213f8001707d3ade0a9ca2bfaa3107db570; adversarial/pass-0044-lean-lake-executable-preflight-steelman.md sha256=daf30c73299f750087984036939bcc8b77f23b59cc083bb1b2838c221273155f |
| Pass 0044 preserves non-promotion boundaries: it is an executable preflight only, does not run Lean or lake build, and current_promoted_natural_laws remains none. | non-promotion-boundary-review | non_promotion_statement present; current_promoted_natural_laws=[]; compiled_replay_status=NOT_RUN; steelman states pass is not compilation |
