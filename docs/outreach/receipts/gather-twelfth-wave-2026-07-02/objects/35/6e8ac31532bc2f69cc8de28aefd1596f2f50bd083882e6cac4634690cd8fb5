# crucible report: Dogfood Pass 0022 OpenTelemetry SDK Dry-Run Lock

## Summary

- thesis_id: `f46a54165456f4c1`
- thesis_seal: `f46a54165456f4c180ce80823fc2d155db90a51d3caed07a206a3a76725b05ae`
- assessment_seal: `beacd4419e654dc1966a8a4ec1cfef62d9212193fcade4d405593d71ba86a406`
- counts: MATCH 10 / DRIFT 0 / UNVERIFIABLE 0
- integrity: seals_ok=True, thesis_ok=True, verdicts_rederive=True

## Verdicts

| Claim | Status | Disposition | Margin | Method | Grounds |
| --- | --- | --- | ---: | --- | --- |
| Pass 0022 created an OTelSdkDryRunLockReceiptSet/v1 artifact with status OTEL_SDK_DRYRUN_LOCK_MATCH, two resolved install rows, five negative fixtures, post_dryrun_sdk_available=false, and seal 678d201ea634eeea2786f0c4effb22d4e38528a80d7cb05c9abe18b446ba3f3c. | MATCH | fenced | 1 | otel-sdk-dryrun-artifact-review | deviation 0 within tolerance 0.5 |
| Pass 0022 pip dry-run command returned 0, used --dry-run and --report -, targeted opentelemetry-sdk==1.41.0, and preserved no_install_boundary=true. | MATCH | fenced | 1 | pip-dryrun-command-review | deviation 0 within tolerance 0.5 |
| Pass 0022 resolved opentelemetry-sdk 1.41.0 as the requested wheel with SHA-256 a596f5687964a3e0d7f8edfdcf5b79cbca9c93c7025ebf5fb00f398a9443b0bd and dependency opentelemetry-api==1.41.0. | MATCH | fenced | 1 | sdk-wheel-review | deviation 0 within tolerance 0.5 |
| Pass 0022 resolved opentelemetry-semantic-conventions 0.62b0 as a transitive wheel with SHA-256 0ddac1ce59eaf1a827d9987ab60d9315fb27aea23304144242d1fcad9e16b489. | MATCH | fenced | 1 | semantic-conventions-wheel-review | deviation 0 within tolerance 0.5 |
| Pass 0022 records local opentelemetry-api 1.41.0 as already satisfied and records opentelemetry.sdk as NOT_INSTALLED_AFTER_DRY_RUN. | MATCH | fenced | 1 | post-dryrun-import-review | deviation 0 within tolerance 0.5 |
| Pass 0022 records three pip invalid-distribution warnings with labels ~, ~arden-shell, and ~~rden-shell. | MATCH | fenced | 1 | invalid-distribution-warning-review | deviation 0 within tolerance 0.5 |
| Pass 0022 negative fixtures reject treating dry-run as install, missing wheel hash, unmatched API/SDK versions, ignored invalid-distribution warnings, and recording-span claims without SDK import. | MATCH | fenced | 1 | negative-fixture-review | deviation 0 within tolerance 0.5 |
| Pass 0022 validator reports MATCH with one matched check and zero drift. | MATCH | fenced | 1 | validator-run-review | deviation 0 within tolerance 0.5 |
| Pass 0022 records tool receipts showing Index, Gather, Telos, Forum status/verify, and Crucible status as MATCH while preserving Forum submit as UNVERIFIABLE due to executor JSON parsing. | MATCH | fenced | 1 | tool-receipt-review | deviation 0 within tolerance 0.5 |
| Pass 0022 promotes zero package installations, opentelemetry.sdk imports, recording spans, environment modifications, trace evidence, natural laws, or scientific discoveries. | MATCH | fenced | 1 | non-promotion-review | deviation 0 within tolerance 0.5 |

## Measurement Evidence

| Claim | Method | Evidence |
| --- | --- | --- |
| Pass 0022 created an OTelSdkDryRunLockReceiptSet/v1 artifact with status OTEL_SDK_DRYRUN_LOCK_MATCH, two resolved install rows, five negative fixtures, post_dryrun_sdk_available=false, and seal 678d201ea634eeea2786f0c4effb22d4e38528a80d7cb05c9abe18b446ba3f3c. | otel-sdk-dryrun-artifact-review | schemas/otel-sdk-dryrun-lock-pass-0022.json schema=OTelSdkDryRunLockReceiptSet/v1; status=OTEL_SDK_DRYRUN_LOCK_MATCH; resolved_install_count=2; negative_fixture_count=5; post_dryrun_import_audit find_spec_available=false; seal=678d201ea634eeea2786f0c4effb22d4e38528a80d7cb05c9abe18b446ba3f3c |
| Pass 0022 pip dry-run command returned 0, used --dry-run and --report -, targeted opentelemetry-sdk==1.41.0, and preserved no_install_boundary=true. | pip-dryrun-command-review | dry_run returncode=0; dry_run command includes --dry-run; dry_run command includes --report -; target_requirement=opentelemetry-sdk==1.41.0; no_install_boundary=true |
| Pass 0022 resolved opentelemetry-sdk 1.41.0 as the requested wheel with SHA-256 a596f5687964a3e0d7f8edfdcf5b79cbca9c93c7025ebf5fb00f398a9443b0bd and dependency opentelemetry-api==1.41.0. | sdk-wheel-review | resolved wheel opentelemetry-sdk present; version=1.41.0; requested=true; sha256=a596f5687964a3e0d7f8edfdcf5b79cbca9c93c7025ebf5fb00f398a9443b0bd; requires_dist includes opentelemetry-api==1.41.0 |
| Pass 0022 resolved opentelemetry-semantic-conventions 0.62b0 as a transitive wheel with SHA-256 0ddac1ce59eaf1a827d9987ab60d9315fb27aea23304144242d1fcad9e16b489. | semantic-conventions-wheel-review | resolved wheel opentelemetry-semantic-conventions present; version=0.62b0; requested=false; sha256=0ddac1ce59eaf1a827d9987ab60d9315fb27aea23304144242d1fcad9e16b489 |
| Pass 0022 records local opentelemetry-api 1.41.0 as already satisfied and records opentelemetry.sdk as NOT_INSTALLED_AFTER_DRY_RUN. | post-dryrun-import-review | already_satisfied includes opentelemetry-api version=1.41.0; post_dryrun_import_audit distribution=opentelemetry-sdk; post_dryrun_import_audit module=opentelemetry.sdk; find_spec_available=false; install_performed=false; expected_status=NOT_INSTALLED_AFTER_DRY_RUN |
| Pass 0022 records three pip invalid-distribution warnings with labels ~, ~arden-shell, and ~~rden-shell. | invalid-distribution-warning-review | invalid_distribution_warning_count=3; invalid_distribution_warning_labels include ~; invalid_distribution_warning_labels include ~arden-shell; invalid_distribution_warning_labels include ~~rden-shell |
| Pass 0022 negative fixtures reject treating dry-run as install, missing wheel hash, unmatched API/SDK versions, ignored invalid-distribution warnings, and recording-span claims without SDK import. | negative-fixture-review | negative-dryrun-treated-as-install expected_validator_status=REJECT; negative-wheel-without-hash expected_validator_status=REJECT; negative-unmatched-api-sdk-version expected_validator_status=REJECT; negative-ignore-invalid-distribution-warnings expected_validator_status=REJECT; negative-recording-span-without-sdk-import expected_validator_status=REJECT |
| Pass 0022 validator reports MATCH with one matched check and zero drift. | validator-run-review | schemas/pass-0022-otel-sdk-dryrun-lock-validator-result.json status=MATCH; match=1; drift=0; checks include OTelSdkDryRunLockReceiptSet status MATCH |
| Pass 0022 records tool receipts showing Index, Gather, Telos, Forum status/verify, and Crucible status as MATCH while preserving Forum submit as UNVERIFIABLE due to executor JSON parsing. | tool-receipt-review | schemas/tool-receipts-pass-0022.json status=MATCH_WITH_FORUM_SUBMIT_GAP; index status MATCH; gather status MATCH; gather docs verified=true; telos operator_doctor status MATCH; forum status MATCH entries=14; forum verify chain=true deep=true; forum submit status=UNVERIFIABLE; crucible status MATCH |
| Pass 0022 promotes zero package installations, opentelemetry.sdk imports, recording spans, environment modifications, trace evidence, natural laws, or scientific discoveries. | non-promotion-review | schemas/otel-sdk-dryrun-lock-pass-0022.json non_promotion_statement states dry-run resolution only; packets/032-otel-sdk-dryrun-lock.md states no package was installed and opentelemetry.sdk remains unavailable; schemas/tool-receipts-pass-0022.json non_promotion_statement states no package installation, SDK import, recording export, or discovery; Current promoted natural laws: none |
