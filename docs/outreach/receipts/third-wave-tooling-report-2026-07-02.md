# crucible report: Project Telos Third-Wave Closed-Loop Demo Claims

## Summary

- thesis_id: `1ac74d0b340bc84d`
- thesis_seal: `1ac74d0b340bc84d59dd6ad19236c05e153df423d97fd5e5b4bd2b41c815fcf4`
- assessment_seal: `50b0134e07987d1b1e05497a4e089d6c39d81ada09cc08f6c883b2cfae6385a0`
- counts: MATCH 5 / DRIFT 0 / UNVERIFIABLE 0
- integrity: seals_ok=True, thesis_ok=True, verdicts_rederive=True

## Verdicts

| Claim | Status | Disposition | Margin | Method | Grounds |
| --- | --- | --- | ---: | --- | --- |
| The BuildLang source checkout produced a ci-review policy-pinned check receipt for examples\quickstart\hello.bld, and buildc receipt verify accepted it with status passed. | MATCH | fenced | 1 | source-checkout-command-review | deviation 0 within tolerance 0.5 |
| The BuildLang receipt was packaged as a Telos-style proof packet that carries source refs and hashes only, then Learn generated and re-verified a prooflesson receipt from that packet. | MATCH | fenced | 1 | proof-packet-and-learning-receipt-review | deviation 0 within tolerance 0.5 |
| Build Color is source-checkout verified as a software-side measurement lane: version 1.0.2, CLI info/convert/difference commands run, and the test suite reports 458 passed. | MATCH | fenced | 1 | source-checkout-command-review | deviation 0 within tolerance 0.5 |
| Telos measurement and display-calibration contracts are wired for this visual proof lane: measurement layers report 10 measurements with MATCH, display calibration is read-only, and the focused tests pass. | MATCH | fenced | 1 | contract-and-test-review | deviation 0 within tolerance 0.5 |
| The third-wave outreach package preserves boundaries: no Julia-replacement claim, no credential-completion claim, no physical calibration claim, and no solved-frontier-science claim. | MATCH | fenced | 1 | document-boundary-review | deviation 0 within tolerance 0.5 |

## Measurement Evidence

| Claim | Method | Evidence |
| --- | --- | --- |
| The BuildLang source checkout produced a ci-review policy-pinned check receipt for examples\quickstart\hello.bld, and buildc receipt verify accepted it with status passed. | source-checkout-command-review | docs/outreach/receipts/third-wave/buildlang-hello-ci-review-receipt.json exists; receipt schema buildlang-check-receipt/v1, compiler buildc, compiler_version 1.0.6, status passed; receipt policy source builtin:ci-review, profile ci-review, profile digest 265584dc495e50171aaa14ab84e0522a34de5b645a703b360c8209068b36f43b, policy status passed, violations []; buildc receipt verify --expect-profile ci-review returned schema buildlang-receipt-verification/v1 and status passed |
| The BuildLang receipt was packaged as a Telos-style proof packet that carries source refs and hashes only, then Learn generated and re-verified a prooflesson receipt from that packet. | proof-packet-and-learning-receipt-review | docs/outreach/receipts/third-wave/buildlang-hello-proof-packet.json exists with version project-telos.proof-packet/v1 and verdicts.overall MATCH; packet sources include only ref and sha256 fields; learn tutor prooflesson buildlang-hello reported verdict MATCH, 4 scaffold steps, and 4 questions; learn tutor reverify buildlang-hello reported VERIFIED with witness digest sha256:c17026d7bba12cf07ef0c8cbf06aab7c549b5f914a0de24c7e76fae488838007 |
| Build Color is source-checkout verified as a software-side measurement lane: version 1.0.2, CLI info/convert/difference commands run, and the test suite reports 458 passed. | source-checkout-command-review | python -m build_color.cli --version: Build Color v1.0.2; python -m build_color.cli info ff6030 returned sRGB, XYZ, Oklab, Oklch, luminance, and contrast values; python -m build_color.cli convert ff6030 --to oklab returned oklab (0.6904, 0.1627, 0.1214); python -m build_color.cli difference ff6030 ff7040 --metric all returned CIEDE2000 3.1581 and other Delta E metrics; python -m pytest tests -q: 458 passed |
| Telos measurement and display-calibration contracts are wired for this visual proof lane: measurement layers report 10 measurements with MATCH, display calibration is read-only, and the focused tests pass. | contract-and-test-review | node demo\measurement-layers.mjs --summary: layers 10, measurements 10, status MATCH; node demo\display-calibration.mjs --summary: hardware read-only, targets 3, patches 4, artifacts 5; node --test demo\measurement-layers.test.mjs demo\display-calibration.test.mjs: 2 pass, 0 fail |
| The third-wave outreach package preserves boundaries: no Julia-replacement claim, no credential-completion claim, no physical calibration claim, and no solved-frontier-science claim. | document-boundary-review | docs/outreach/THIRD-WAVE-CLOSED-LOOP-DEMO-2026-07-02.md includes Do Not Post boundaries; docs/outreach/THIRD-WAVE-CONTENT-QUEUE-2026-07-02.md requires command-backed posting; docs/outreach/PARALLEL-CODEX-HANDOFF-2026-07-02.md lists current boundaries; docs/TOOLING-SHAPE-ASSESSMENT-2026-07-02.md separates source-checkout evidence from PATH-installed evidence |
