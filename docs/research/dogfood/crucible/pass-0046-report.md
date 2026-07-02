# crucible report: Dogfood Pass 0046 Elan Controlled Install Plan

## Summary

- thesis_id: `8f4e98bce0a0543b`
- thesis_seal: `8f4e98bce0a0543bd5e48212cb6147ff2919d80b24aa6bf03832d1b3562c9f83`
- assessment_seal: `46b0fddd9d9faf7930582d54bea1bcd06715865ffb9a0c59fbccf38faa8f1b4e`
- counts: MATCH 8 / DRIFT 0 / UNVERIFIABLE 0
- integrity: seals_ok=True, thesis_ok=True, verdicts_rederive=True

## Verdicts

| Claim | Status | Disposition | Margin | Method | Grounds |
| --- | --- | --- | ---: | --- | --- |
| Pass 0046 created an ElanControlledInstallPlanSet/v1 artifact with status ELAN_CONTROLLED_INSTALL_PLAN_MATCH, sha256 6620e88e5ed7afe4e4706ae884ff7dd66af2692081d8a135a485dbe80b3c25d5, and seal 0e79d9f03e7029462e50fcd7785d4ff3406cdb8fcd125f9202c51f32ee1e5d57. | MATCH | fenced | 1 | elan-install-plan-schema-review | deviation 0 within tolerance 0.5 |
| Pass 0046 records fixture fixtures/elan-controlled-install-plan-pass-0046.json with sha256 2606465fe4f9a7db9d5357bea153d021ae9350e1a774dd2f9d10233119b9ca08 and seal 77d7c4591915147a289b809d42525224d9d51bb26a94554e429445dc60b5c510. | MATCH | fenced | 1 | fixture-binding-review | deviation 0 within tolerance 0.5 |
| Pass 0046 records installer sha256 1d3c66430d0e7b719b104e1dea80e395a066e96c37b886f2de4b0e9025a037fb, no_prompt_supported true, no_modify_path_supported true, default_toolchain_supported true, and installer_script_executed false. | MATCH | fenced | 1 | installer-control-review | deviation 0 within tolerance 0.5 |
| Pass 0046 records proposed command shape powershell -ExecutionPolicy Bypass -File elan-init.ps1 -NoPrompt 1 -NoModifyPath 1 -DefaultToolchain leanprover/lean4:v4.31.0. | MATCH | fenced | 1 | install-command-shape-review | deviation 0 within tolerance 0.5 |
| Pass 0046 binds to pass 0045 Lean toolchain acquisition sources with sha256 924ef19e25fbaf101001b0cc9caf25d929f13fcb034f2aa6bcc4720101c56117, seal b31f2684d77de7f83ef71ec4b4ef1230d8b265c36758736d03cffade4149868e, and source status LEAN_TOOLCHAIN_ACQUISITION_SOURCES_MATCH. | MATCH | fenced | 1 | source-binding-review | deviation 0 within tolerance 0.5 |
| Pass 0046 validator result reports MATCH. | MATCH | fenced | 1 | validator-result-review | deviation 0 within tolerance 0.5 |
| Pass 0046 records packet 056 with sha256 586e8aff087e602e4c73ade57a20b2842bc197868440c5a6d7103d9e5779ab48 and local steelman with sha256 fdcfafd4eee509acb7a6e9a8349d127edda0c8ec544d17573c940efa6c7cd2cb. | MATCH | fenced | 1 | packet-presence-review | deviation 0 within tolerance 0.5 |
| Pass 0046 preserves non-promotion boundaries: it records an install plan only, does not execute elan-init.ps1, does not install Elan, does not run Lean or lake build, and current_promoted_natural_laws remains none. | MATCH | fenced | 1 | non-promotion-boundary-review | deviation 0 within tolerance 0.5 |

## Measurement Evidence

| Claim | Method | Evidence |
| --- | --- | --- |
| Pass 0046 created an ElanControlledInstallPlanSet/v1 artifact with status ELAN_CONTROLLED_INSTALL_PLAN_MATCH, sha256 6620e88e5ed7afe4e4706ae884ff7dd66af2692081d8a135a485dbe80b3c25d5, and seal 0e79d9f03e7029462e50fcd7785d4ff3406cdb8fcd125f9202c51f32ee1e5d57. | elan-install-plan-schema-review | schema=ElanControlledInstallPlanSet/v1; status=ELAN_CONTROLLED_INSTALL_PLAN_MATCH; sha256=6620e88e5ed7afe4e4706ae884ff7dd66af2692081d8a135a485dbe80b3c25d5; seal=0e79d9f03e7029462e50fcd7785d4ff3406cdb8fcd125f9202c51f32ee1e5d57 |
| Pass 0046 records fixture fixtures/elan-controlled-install-plan-pass-0046.json with sha256 2606465fe4f9a7db9d5357bea153d021ae9350e1a774dd2f9d10233119b9ca08 and seal 77d7c4591915147a289b809d42525224d9d51bb26a94554e429445dc60b5c510. | fixture-binding-review | fixture sha256=2606465fe4f9a7db9d5357bea153d021ae9350e1a774dd2f9d10233119b9ca08; fixture seal=77d7c4591915147a289b809d42525224d9d51bb26a94554e429445dc60b5c510 |
| Pass 0046 records installer sha256 1d3c66430d0e7b719b104e1dea80e395a066e96c37b886f2de4b0e9025a037fb, no_prompt_supported true, no_modify_path_supported true, default_toolchain_supported true, and installer_script_executed false. | installer-control-review | installer_script_sha256=1d3c66430d0e7b719b104e1dea80e395a066e96c37b886f2de4b0e9025a037fb; no_prompt_supported=true; no_modify_path_supported=true; default_toolchain_supported=true; installer_script_executed=false |
| Pass 0046 records proposed command shape powershell -ExecutionPolicy Bypass -File elan-init.ps1 -NoPrompt 1 -NoModifyPath 1 -DefaultToolchain leanprover/lean4:v4.31.0. | install-command-shape-review | proposed_command_shape=powershell -ExecutionPolicy Bypass -File elan-init.ps1 -NoPrompt 1 -NoModifyPath 1 -DefaultToolchain leanprover/lean4:v4.31.0; default_toolchain=leanprover/lean4:v4.31.0 |
| Pass 0046 binds to pass 0045 Lean toolchain acquisition sources with sha256 924ef19e25fbaf101001b0cc9caf25d929f13fcb034f2aa6bcc4720101c56117, seal b31f2684d77de7f83ef71ec4b4ef1230d8b265c36758736d03cffade4149868e, and source status LEAN_TOOLCHAIN_ACQUISITION_SOURCES_MATCH. | source-binding-review | acquisition_source_sha256=924ef19e25fbaf101001b0cc9caf25d929f13fcb034f2aa6bcc4720101c56117; acquisition_source_seal=b31f2684d77de7f83ef71ec4b4ef1230d8b265c36758736d03cffade4149868e; acquisition_source_status=LEAN_TOOLCHAIN_ACQUISITION_SOURCES_MATCH |
| Pass 0046 validator result reports MATCH. | validator-result-review | schemas/pass-0046-elan-controlled-install-plan-validator-result.json status=MATCH |
| Pass 0046 records packet 056 with sha256 586e8aff087e602e4c73ade57a20b2842bc197868440c5a6d7103d9e5779ab48 and local steelman with sha256 fdcfafd4eee509acb7a6e9a8349d127edda0c8ec544d17573c940efa6c7cd2cb. | packet-presence-review | packets/056-elan-controlled-install-plan.md sha256=586e8aff087e602e4c73ade57a20b2842bc197868440c5a6d7103d9e5779ab48; adversarial/pass-0046-elan-controlled-install-plan-steelman.md sha256=fdcfafd4eee509acb7a6e9a8349d127edda0c8ec544d17573c940efa6c7cd2cb |
| Pass 0046 preserves non-promotion boundaries: it records an install plan only, does not execute elan-init.ps1, does not install Elan, does not run Lean or lake build, and current_promoted_natural_laws remains none. | non-promotion-boundary-review | non_promotion_statement present; installer_script_executed=false; current_promoted_natural_laws=[]; steelman states pass does not prove install safety or build success |
