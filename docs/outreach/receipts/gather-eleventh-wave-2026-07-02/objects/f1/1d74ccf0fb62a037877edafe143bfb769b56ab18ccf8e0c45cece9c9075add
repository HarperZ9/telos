# Packet 102: BuildLang Check Receipt Adapter

Date: 2026-07-01

Status: `BUILDLANG_CHECK_RECEIPT_ADAPTER_MATCH`

Purpose: parse one real `buildc check --receipt` JSON artifact, verify it with
`buildc receipt verify`, and map source digest, policy, effects, and capability
evidence into Crucible-ready measurements.

```text
source = C:\dev\public\pubscan\quantalang\examples\quickstart\hello.bld
profile = console-only
repo_branch = ## main...origin/main
repo_dirty_count = 0
compiler_version = 1.0.6
source_digest = 0e542c60fbd874a38a2a3a87eaf61be04532a0df23e3ea25512d03301883dfae
input_graph_digest = 038a6f3aba486917d0ccbb9e4c0e858d0e79a8d1230450c3c40ca7dd08026d40
policy_profile = console-only
declared_effects = {'main': ['Console']}
observed_capabilities = {'main': {'Console': ['println!']}}
verify_status = passed
verify_check_count = 18
measurement_count = 10
adapter_match = 10
adapter_drift = 0
compose_status = MATCH
test_status = MATCH
```

## Measurements

| Measurement | Status | Claim |
| --- | --- | --- |
| buildc_check.receipt_schema | MATCH | receipt schema is buildlang-check-receipt/v1 |
| buildc_check.receipt_status | MATCH | check receipt status is passed |
| buildc_check.source_digest | MATCH | source digest is sha256 hex |
| buildc_check.input_graph_digest | MATCH | input graph digest is sha256 hex |
| buildc_check.policy_profile | MATCH | policy profile is console-only |
| buildc_check.policy_status | MATCH | policy status is passed |
| buildc_check.declared_effects | MATCH | main declares Console effect |
| buildc_check.observed_capabilities | MATCH | main observes Console println! capability |
| buildc_check.diagnostics | MATCH | diagnostics are empty |
| buildc_check.verify_report | MATCH | receipt verify required checks all passed |

Boundary: this is one source-level compiler receipt adapter. It does not prove
language replacement, scientific discovery, full compiler correctness, or a
natural law.
