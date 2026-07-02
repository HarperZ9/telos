# crucible report: Dogfood Pass 0034 Lean Replay Verification

## Summary

- thesis_id: `e3ad254908aef8ef`
- thesis_seal: `e3ad254908aef8ef374691fca1de455d7de3b1a951186f73bf6e83eb53d233f8`
- assessment_seal: `79407783c76966bea42da1ef031f26aaac1b965d762fab2113965e8cf63d0b06`
- counts: MATCH 10 / DRIFT 0 / UNVERIFIABLE 0
- integrity: seals_ok=True, thesis_ok=True, verdicts_rederive=True

## Verdicts

| Claim | Status | Disposition | Margin | Method | Grounds |
| --- | --- | --- | ---: | --- | --- |
| Pass 0034 created a LeanReplayVerificationPacket/v1 artifact with status LEAN_REPLAY_VERIFIED_WITH_AXIOM_BOUNDARY, source_provisioning_sha256 e4a4085f9711d672ee18a08e85aa55b6fabe8f64807daad53eff382506b9a366, verifier_exit_code 0, axiom_check_count 10, and seal bbe72907f7bc745c4bdc19f2162050d0dc7e48ea9382bc0b09f226f2500539bd. | MATCH | fenced | 1 | lean-replay-verification-review | deviation 0 within tolerance 0.5 |
| Pass 0034 records fixture fixtures/lean-replay-verification-pass-0034.json with sha256 eef39b1caa78dd2d996589b08c40b93881cfe45d17e2b15479ec9aa8d5b9fafb and seal fd38f5abf22c501b06e28321e9408d5562e154eb4a012c4988a64b910a6ffa2f. | MATCH | fenced | 1 | fixture-binding-review | deviation 0 within tolerance 0.5 |
| Pass 0034 cache hydration records lake exe cache get exit_code 0, downloaded_files 8542, decompressed_files 8542, cache_file_count 8542, and cache_byte_sum 432264798. | MATCH | fenced | 1 | cache-hydration-review | deviation 0 within tolerance 0.5 |
| Pass 0034 verifier run records scripts/verify.sh --no-log --all exit_code 0, result PASS, result_issue_count 0, duration_seconds 1184, and build_jobs 8574. | MATCH | fenced | 1 | verifier-run-review | deviation 0 within tolerance 0.5 |
| Pass 0034 verifier checks record frozen_sha_pins_status PASS, banned_keywords_status PASS, and lake_build_status PASS. | MATCH | fenced | 1 | verifier-check-review | deviation 0 within tolerance 0.5 |
| Pass 0034 records ten Prob4b.Solution axiom checks, all PASS, each with axiom set propext, Classical.choice, and Quot.sound. | MATCH | fenced | 1 | axiom-check-review | deviation 0 within tolerance 0.5 |
| Pass 0034 statement gates record Prob4b.Discharge PASS and Prob4b.Solution PASS. | MATCH | fenced | 1 | statement-gate-review | deviation 0 within tolerance 0.5 |
| Pass 0034 build artifact snapshot records .lake file_count 123892, .lake byte_sum 8009101293, cache_file_count 8542, Prob4b build file_count 75, and remaining_temp_processes 0. | MATCH | fenced | 1 | build-artifact-review | deviation 0 within tolerance 0.5 |
| Pass 0034 validator result reports MATCH with verifier_exit_code 0, verifier_result PASS, lake_build_status PASS, theorem_axiom_status PASS, axiom_check_count 10, cache_file_count 8542, prob4b_build_file_count 75, and remaining_temp_processes 0. | MATCH | fenced | 1 | validator-result-review | deviation 0 within tolerance 0.5 |
| Pass 0034 preserves non-promotion boundaries: it verifies the local Lean replay harness under recorded toolchain, cache, axiom, and statement-gate boundaries while current_promoted_natural_laws remains none and public-claim overpromotion remains rejected. | MATCH | fenced | 1 | non-promotion-boundary-review | deviation 0 within tolerance 0.5 |

## Measurement Evidence

| Claim | Method | Evidence |
| --- | --- | --- |
| Pass 0034 created a LeanReplayVerificationPacket/v1 artifact with status LEAN_REPLAY_VERIFIED_WITH_AXIOM_BOUNDARY, source_provisioning_sha256 e4a4085f9711d672ee18a08e85aa55b6fabe8f64807daad53eff382506b9a366, verifier_exit_code 0, axiom_check_count 10, and seal bbe72907f7bc745c4bdc19f2162050d0dc7e48ea9382bc0b09f226f2500539bd. | lean-replay-verification-review | schema=LeanReplayVerificationPacket/v1; status=LEAN_REPLAY_VERIFIED_WITH_AXIOM_BOUNDARY; source_provisioning_sha256=e4a4085f9711d672ee18a08e85aa55b6fabe8f64807daad53eff382506b9a366; verifier_exit_code=0; axiom_check_count=10; seal=bbe72907f7bc745c4bdc19f2162050d0dc7e48ea9382bc0b09f226f2500539bd |
| Pass 0034 records fixture fixtures/lean-replay-verification-pass-0034.json with sha256 eef39b1caa78dd2d996589b08c40b93881cfe45d17e2b15479ec9aa8d5b9fafb and seal fd38f5abf22c501b06e28321e9408d5562e154eb4a012c4988a64b910a6ffa2f. | fixture-binding-review | fixture sha256=eef39b1caa78dd2d996589b08c40b93881cfe45d17e2b15479ec9aa8d5b9fafb; fixture seal=fd38f5abf22c501b06e28321e9408d5562e154eb4a012c4988a64b910a6ffa2f |
| Pass 0034 cache hydration records lake exe cache get exit_code 0, downloaded_files 8542, decompressed_files 8542, cache_file_count 8542, and cache_byte_sum 432264798. | cache-hydration-review | exit_code=0; downloaded_files=8542; decompressed_files=8542; cache_file_count=8542; cache_byte_sum=432264798 |
| Pass 0034 verifier run records scripts/verify.sh --no-log --all exit_code 0, result PASS, result_issue_count 0, duration_seconds 1184, and build_jobs 8574. | verifier-run-review | exit_code=0; result=PASS; result_issue_count=0; duration_seconds=1184; build_jobs=8574 |
| Pass 0034 verifier checks record frozen_sha_pins_status PASS, banned_keywords_status PASS, and lake_build_status PASS. | verifier-check-review | frozen_sha_pins_status=PASS; banned_keywords_status=PASS; lake_build_status=PASS |
| Pass 0034 records ten Prob4b.Solution axiom checks, all PASS, each with axiom set propext, Classical.choice, and Quot.sound. | axiom-check-review | axiom_check_count=10; theorem_axiom_status=PASS; axiom_set=[propext, Classical.choice, Quot.sound] |
| Pass 0034 statement gates record Prob4b.Discharge PASS and Prob4b.Solution PASS. | statement-gate-review | Prob4b.Discharge=PASS; Prob4b.Solution=PASS |
| Pass 0034 build artifact snapshot records .lake file_count 123892, .lake byte_sum 8009101293, cache_file_count 8542, Prob4b build file_count 75, and remaining_temp_processes 0. | build-artifact-review | lake_file_count=123892; lake_byte_sum=8009101293; cache_file_count=8542; prob4b_build_file_count=75; remaining_temp_processes=0 |
| Pass 0034 validator result reports MATCH with verifier_exit_code 0, verifier_result PASS, lake_build_status PASS, theorem_axiom_status PASS, axiom_check_count 10, cache_file_count 8542, prob4b_build_file_count 75, and remaining_temp_processes 0. | validator-result-review | validator status=MATCH; verifier_exit_code=0; verifier_result=PASS; lake_build_status=PASS; theorem_axiom_status=PASS; axiom_check_count=10; cache_file_count=8542; prob4b_build_file_count=75; remaining_temp_processes=0 |
| Pass 0034 preserves non-promotion boundaries: it verifies the local Lean replay harness under recorded toolchain, cache, axiom, and statement-gate boundaries while current_promoted_natural_laws remains none and public-claim overpromotion remains rejected. | non-promotion-boundary-review | current_promoted_natural_laws=[]; non_promotion_statement present; negative-public-claim-overpromoted expected_validator_status=REJECT; negative-natural-law-promoted expected_validator_status=REJECT |
