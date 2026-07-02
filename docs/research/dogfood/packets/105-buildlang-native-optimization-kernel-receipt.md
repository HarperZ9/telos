# Packet 105: BuildLang Native Optimization Kernel Receipt

Date: 2026-07-01

Status: `BUILDLANG_NATIVE_OPTIMIZATION_KERNEL_RECEIPT_MATCH`

Purpose: run a BuildLang-native exact-enumeration optimization source and bind
its run output to `buildc check --receipt` and `buildc receipt verify`.

```text
source = C:\dev\public\telos\docs\research\dogfood\fixtures\buildlang-knapsack-exact-pass-0095.bld
profile = console-only
compiler_version = 1.0.6
source_digest = 2480f503aa672459ccdd437a93f8d50c71dbc9b90d1ce236a52259727e1e29e9
best_value = 162
best_weight = 29
best_mask = 2347
feasible_count = 1275
verify_check_count = 18
compose_status = MATCH
test_status = MATCH
```

## Measurements

| Measurement | Status | Claim |
| --- | --- | --- |
| `buildlang_native_opt.check_receipt` | MATCH | buildc check receipt passed |
| `buildlang_native_opt.verify_report` | MATCH | receipt verify passed all required checks |
| `buildlang_native_opt.run_output_best_value` | MATCH | BuildLang run finds exact best value 162 |
| `buildlang_native_opt.run_output_best_weight` | MATCH | BuildLang run finds exact best weight 29 |
| `buildlang_native_opt.run_output_feasible_count` | MATCH | BuildLang run enumerates 1275 feasible masks |
| `buildlang_native_opt.matches_prior_workflow` | MATCH | BuildLang output matches pass 0094 exact baseline |
| `buildlang_native_opt.source_digest` | MATCH | source digest is sha256 hex |
| `buildlang_native_opt.console_policy` | MATCH | console-only policy passes |
| `buildlang_native_opt.flagships` | MATCH | Forum, Index, and Telos receipts match |
| `buildlang_native_opt.promotion_boundary` | MATCH | no replacement, discovery, or natural-law claim is promoted |

Boundary: this pass proves one BuildLang exact-enumeration fixture can run and
emit receipts. It does not prove language replacement, production optimization,
scientific discovery, or a natural law.
