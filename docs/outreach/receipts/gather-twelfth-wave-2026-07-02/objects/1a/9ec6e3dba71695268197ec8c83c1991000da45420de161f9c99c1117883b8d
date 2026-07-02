# crucible report: Dogfood Pass 0100 Ocean/dimod BQM Branch

## Summary

- thesis_id: `47a02c9e50476cf6`
- thesis_seal: `47a02c9e50476cf64348cb5ef580bffc4252e178d27f9d5bac1f67a94cae2f48`
- assessment_seal: `06c4034fe9266336240c5e525e62b9f65d917ef6f9bab79eaf461f58e07fd3d9`
- counts: MATCH 9 / DRIFT 0 / UNVERIFIABLE 0
- integrity: seals_ok=True, thesis_ok=True, verdicts_rederive=True

## Verdicts

| Claim | Status | Disposition | Margin | Method | Grounds |
| --- | --- | --- | ---: | --- | --- |
| Pass 0100 created an OceanDimodBQMBranchReceipt/v1 artifact with status OCEAN_DIMOD_BQM_BRANCH_RECEIPT_MATCH, sha256 4f13f2776b6c5681a5968aecc6cdace0ae34225777e03f5162a320211adcc28c, and seal f387d6efcef2e71273f577213aa1db00afa00f225f4f32b8fe646680f2f3872b. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |
| Pass 0100 binds OR-Tools pass 0099 and records global dimod/dwave availability as false. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |
| Pass 0100 created a temp venv, installed dimod, executed ExactSolver, and cleaned the temp venv. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |
| Pass 0100 records dimod version 0.12.22. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |
| Pass 0100 SolverBranchReceipt/v1 branch ocean_dimod_exact_bqm records value 162, weight 29, mask 2347, and gap 0. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |
| Pass 0100 records BQM term counts linear=12 and quadratic=66. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |
| Pass 0100 flagship receipts for Forum, Index, and Telos all have MATCH status. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |
| Pass 0100 records unsupported_claim_count 0 and current_promoted_natural_laws length 0. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |
| Pass 0100 composer sha256 is 3145dcda98180e6674b5b1c282b6f3436d2cd5d5384539eb1a54f9f8a34758a7, packet sha256 is c3b0b7e0c210a87763e3b40baf886918f797a16ce306c6b7db6c8a7d16dc03d0, brief sha256 is e7bd4d8aa3254acff995fd0af8947712734a6fe6e57d56f31d06b7c0fa5a103e, steelman sha256 is 4ade01ec7f33e4541bf21e187f0e1147ca458a2843528c984f5e4f3629792f3a, test sha256 is 5069c6584f823dd4d928e290a4053c5ca8a54717095f5c49fd31ae0a75e2c201, and tool_receipts sha256 is 7e96c78177c7a554698cc0fae7a4e6b0afba6041ff7237b2dc57cf93eeef9359 with test_receipt status MATCH. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |

## Measurement Evidence

| Claim | Method | Evidence |
| --- | --- | --- |
| Pass 0100 created an OceanDimodBQMBranchReceipt/v1 artifact with status OCEAN_DIMOD_BQM_BRANCH_RECEIPT_MATCH, sha256 4f13f2776b6c5681a5968aecc6cdace0ae34225777e03f5162a320211adcc28c, and seal f387d6efcef2e71273f577213aa1db00afa00f225f4f32b8fe646680f2f3872b. | artifact-review | schema=OceanDimodBQMBranchReceipt/v1; status=OCEAN_DIMOD_BQM_BRANCH_RECEIPT_MATCH; sha256=4f13f2776b6c5681a5968aecc6cdace0ae34225777e03f5162a320211adcc28c; seal=f387d6efcef2e71273f577213aa1db00afa00f225f4f32b8fe646680f2f3872b |
| Pass 0100 binds OR-Tools pass 0099 and records global dimod/dwave availability as false. | artifact-review | source_bindings={'interop_pass': '0098', 'ortools_pass': '0099', 'prior_dwave_status': 'NOT_EXECUTED_DEPENDENCY_MISSING'}; dimod_available=False; dwave_available=False |
| Pass 0100 created a temp venv, installed dimod, executed ExactSolver, and cleaned the temp venv. | artifact-review | venv_create=0; install=0; run=0; cleaned=True |
| Pass 0100 records dimod version 0.12.22. | artifact-review | dimod_version=0.12.22 |
| Pass 0100 SolverBranchReceipt/v1 branch ocean_dimod_exact_bqm records value 162, weight 29, mask 2347, and gap 0. | artifact-review | branch_id=ocean_dimod_exact_bqm; value=162; weight=29; mask=2347; gap=0 |
| Pass 0100 records BQM term counts linear=12 and quadratic=66. | artifact-review | linear_terms=12; quadratic_terms=66 |
| Pass 0100 flagship receipts for Forum, Index, and Telos all have MATCH status. | artifact-review | forum=MATCH; index=MATCH; telos=MATCH |
| Pass 0100 records unsupported_claim_count 0 and current_promoted_natural_laws length 0. | artifact-review | unsupported_claim_count=0; natural_law_count=0 |
| Pass 0100 composer sha256 is 3145dcda98180e6674b5b1c282b6f3436d2cd5d5384539eb1a54f9f8a34758a7, packet sha256 is c3b0b7e0c210a87763e3b40baf886918f797a16ce306c6b7db6c8a7d16dc03d0, brief sha256 is e7bd4d8aa3254acff995fd0af8947712734a6fe6e57d56f31d06b7c0fa5a103e, steelman sha256 is 4ade01ec7f33e4541bf21e187f0e1147ca458a2843528c984f5e4f3629792f3a, test sha256 is 5069c6584f823dd4d928e290a4053c5ca8a54717095f5c49fd31ae0a75e2c201, and tool_receipts sha256 is 7e96c78177c7a554698cc0fae7a4e6b0afba6041ff7237b2dc57cf93eeef9359 with test_receipt status MATCH. | artifact-review | composer_sha256=3145dcda98180e6674b5b1c282b6f3436d2cd5d5384539eb1a54f9f8a34758a7; packet_sha256=c3b0b7e0c210a87763e3b40baf886918f797a16ce306c6b7db6c8a7d16dc03d0; brief_sha256=e7bd4d8aa3254acff995fd0af8947712734a6fe6e57d56f31d06b7c0fa5a103e; steelman_sha256=4ade01ec7f33e4541bf21e187f0e1147ca458a2843528c984f5e4f3629792f3a; test_sha256=5069c6584f823dd4d928e290a4053c5ca8a54717095f5c49fd31ae0a75e2c201; tool_receipts_sha256=7e96c78177c7a554698cc0fae7a4e6b0afba6041ff7237b2dc57cf93eeef9359; test_status=MATCH; compose_status=MATCH |
