# crucible report: Dogfood Pass 0076 BuildLang Index Focus Bridge

## Summary

- thesis_id: `f3bbaf7d62e6976b`
- thesis_seal: `f3bbaf7d62e6976b51a6855591d2cbf295d3ed9157f51227e3446a0149ef208f`
- assessment_seal: `826ad241c446d4129dd94a444ff19f270a856b8b387c42fe5c0f7702f143af61`
- counts: MATCH 8 / DRIFT 0 / UNVERIFIABLE 0
- integrity: seals_ok=True, thesis_ok=True, verdicts_rederive=True

## Verdicts

| Claim | Status | Disposition | Margin | Method | Grounds |
| --- | --- | --- | ---: | --- | --- |
| Pass 0076 created a BuildLangIndexFocusBridge/v1 artifact with status BUILDLANG_INDEX_FOCUS_BRIDGE_REQUIRED, sha256 c6298c0ef61683f1a6fd31254ca1356aa5ffe9a288795347e1568fe218b1114d, and seal 9cf57e0ee809d246a97a6d5a6b6490836fb196c553dca86b8a66b1d14655e7e7. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |
| Pass 0076 root Index context status is MATCH with source_ref_count 1. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |
| Pass 0076 records path_scoped_context False and bridge_required True. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |
| Pass 0076 focus probes contain 4 probes and 4 expected rejections. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |
| Pass 0076 Index map presence is buildlang=True, compiler=True, build-universe=False. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |
| Pass 0076 source receipt pass is 0074 with source_ref_count 13. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |
| Pass 0076 contains 8 negative fixtures and unsupported_claim_count 0. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |
| Pass 0076 composer sha256 is 91536517ef0c05e6d2fd59c1805b2521c9cd64e42bae37a11e7c869aab36bebd, packet sha256 is 8f4c4dffd18347461fb28ade23200a3feeb35f93290fc9d642efa8546c83764d, steelman sha256 is bf0afc44096a85464e40c8890028d6cf1e974d21b808d4fd48898977ad46538f, and test sha256 is db27988901e9d7b1ff3b6b10bd4e7c92761a13ad2706f8d50a37e07ff082ab28 with test_receipt status MATCH. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |

## Measurement Evidence

| Claim | Method | Evidence |
| --- | --- | --- |
| Pass 0076 created a BuildLangIndexFocusBridge/v1 artifact with status BUILDLANG_INDEX_FOCUS_BRIDGE_REQUIRED, sha256 c6298c0ef61683f1a6fd31254ca1356aa5ffe9a288795347e1568fe218b1114d, and seal 9cf57e0ee809d246a97a6d5a6b6490836fb196c553dca86b8a66b1d14655e7e7. | artifact-review | schema=BuildLangIndexFocusBridge/v1; status=BUILDLANG_INDEX_FOCUS_BRIDGE_REQUIRED; sha256=c6298c0ef61683f1a6fd31254ca1356aa5ffe9a288795347e1568fe218b1114d; seal=9cf57e0ee809d246a97a6d5a6b6490836fb196c553dca86b8a66b1d14655e7e7 |
| Pass 0076 root Index context status is MATCH with source_ref_count 1. | artifact-review | root_context_status=MATCH; source_ref_count=1 |
| Pass 0076 records path_scoped_context False and bridge_required True. | artifact-review | path_scoped_context=False; bridge_required=True |
| Pass 0076 focus probes contain 4 probes and 4 expected rejections. | artifact-review | focus_probe_count=4; expected_reject_count=4 |
| Pass 0076 Index map presence is buildlang=True, compiler=True, build-universe=False. | artifact-review | buildlang=True; compiler=True; build-universe=False |
| Pass 0076 source receipt pass is 0074 with source_ref_count 13. | artifact-review | source_receipt_pass=0074; source_ref_count=13 |
| Pass 0076 contains 8 negative fixtures and unsupported_claim_count 0. | artifact-review | negative_fixture_count=8; unsupported_claim_count=0 |
| Pass 0076 composer sha256 is 91536517ef0c05e6d2fd59c1805b2521c9cd64e42bae37a11e7c869aab36bebd, packet sha256 is 8f4c4dffd18347461fb28ade23200a3feeb35f93290fc9d642efa8546c83764d, steelman sha256 is bf0afc44096a85464e40c8890028d6cf1e974d21b808d4fd48898977ad46538f, and test sha256 is db27988901e9d7b1ff3b6b10bd4e7c92761a13ad2706f8d50a37e07ff082ab28 with test_receipt status MATCH. | artifact-review | composer_sha256=91536517ef0c05e6d2fd59c1805b2521c9cd64e42bae37a11e7c869aab36bebd; packet_sha256=8f4c4dffd18347461fb28ade23200a3feeb35f93290fc9d642efa8546c83764d; steelman_sha256=bf0afc44096a85464e40c8890028d6cf1e974d21b808d4fd48898977ad46538f; test_sha256=db27988901e9d7b1ff3b6b10bd4e7c92761a13ad2706f8d50a37e07ff082ab28; test_status=MATCH; compose_status=MATCH |
