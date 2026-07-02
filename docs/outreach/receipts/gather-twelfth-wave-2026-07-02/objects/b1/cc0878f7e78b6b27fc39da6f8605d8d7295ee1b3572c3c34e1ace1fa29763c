# Packet 117: Reaction-Network Corpus Harness Receipt

Date: 2026-07-01

Status: `REACTION_NETWORK_CORPUS_HARNESS_RECEIPT_MATCH`

Purpose: scale the pass 0106 stoichiometric invariant checker from one network
to a four-case corpus and bind the result to the BuildLang/buildc scientific
runtime lane as a target receipt.

```text
stoichiometric_source_pass = 0106
buildlang_native_pass = 0095
youtube_scorecard_pass = 0096
network_count = 4
match_count = 3
drift_expected_count = 1
derived_invariant_count = 4
buildlang_bridge_status = TARGET_SPECIFIED_WITH_EXISTING_BUILDC_RECEIPT
buildlang_source_digest = 2480f503aa672459ccdd437a93f8d50c71dbc9b90d1ce236a52259727e1e29e9
buildlang_verify_check_count = 18
youtube_valid_videos = 19
buildlang_runtime_video_count = 14
compose_status = MATCH
test_status = MATCH
```

## Corpus

| Network | Status | Basis dim | Max drift | Candidate residuals |
| --- | --- | ---: | ---: | --- |
| closed_cycle_abc | MATCH | 1 | 3.9968028886505635e-15 | A+B+C:[0, 0, 0] |
| reversible_dimerization | MATCH | 1 | 2.220446049250313e-15 | A+2*B:[0, 0] |
| enzyme_product_skeleton | MATCH | 2 | 1.7763568394002505e-15 | E+ES:[0, 0, 0]; S+ES+P:[0, 0, 0] |
| open_degradation | DRIFT_EXPECTED | 0 | 0.7876978722105867 | A:[-1] |

## BuildLang Runtime Bridge

This pass does not compile a new chemistry kernel. It binds the existing pass
0095 buildc receipt and records the required next receipts:
`stoichiometric_matrix_digest, conservation_vector_receipt, residual_zero_check, numeric_tolerance_receipt, negative_fixture_receipt`.

## Boundary

This pass proves only a bounded corpus harness and target BuildLang runtime bridge. It does not prove a new natural law, biological discovery, wet-lab result, or compiled chemistry kernel.
