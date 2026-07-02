# Pass 0092 Ledger: BuildLang Check Receipt Adapter

Date: 2026-07-01

Status: `BUILDLANG_CHECK_RECEIPT_ADAPTER_MATCH`

## Purpose

Convert one real `buildc check --receipt` JSON artifact into
Crucible-ready measurements. This advances the BuildLang/buildc lane from
corpus-output witnessing into source-level compiler receipt witnessing:
source digest, input graph digest, policy profile, declared effects, observed
capabilities, diagnostics, and receipt-verification checks are all captured.

## Artifacts

| Artifact | Purpose |
| --- | --- |
| `tools/compose_buildlang_check_receipt_adapter.py` | Runs `buildc check --receipt`, verifies the receipt, and composes the adapter artifact. |
| `tools/test_buildlang_check_receipt_adapter.py` | Focused artifact, receipt, policy, and boundary test. |
| `tools/probe_buildlang_check_receipt_adapter.py` | Packet, brief, steelman, thesis, measurement, and compact receipt generator. |
| `tools/validate_pass_0092_buildlang_check_receipt_adapter.py` | Independent validator for seal, compiler receipt, verification report, and boundaries. |
| `schemas/buildlang-check-receipt-pass-0092.json` | Raw `buildc check --receipt` output. |
| `schemas/buildlang-receipt-verification-pass-0092.json` | Raw `buildc receipt verify --json` output. |
| `schemas/buildlang-check-receipt-adapter-pass-0092.json` | `BuildLangCheckReceiptAdapter/v1` artifact. |
| `schemas/pass-0092-buildlang-check-receipt-adapter-validator-result.json` | Validator receipt. |
| `schemas/tool-receipts-pass-0092.json` | Compact compose, test, Forum, Index, Telos, check, verify, and adapter receipt set. |
| `packets/102-buildlang-check-receipt-adapter.md` | Human-readable BuildLang check receipt packet. |
| `briefs/102-buildlang-check-receipt-adapter-brief.md` | Concise product-strategy brief. |
| `adversarial/pass-0092-buildlang-check-receipt-adapter-steelman.md` | Local steelman of adapter limits. |
| `crucible/pass-0092-thesis.json` | Falsifiable claims. |
| `crucible/pass-0092-measurements.json` | Measurements/evidence. |
| `crucible/pass-0092-report.md` | Crucible report. |
| `crucible/pass-0092-run.json` | Crucible run record. |

## Measurements

| Check | Result |
| --- | --- |
| Prior pass | 0091 |
| BuildLang repo | `C:\dev\public\pubscan\quantalang` |
| BuildLang branch | `## main...origin/main` |
| BuildLang dirty count | 0 |
| Source fixture | `C:\dev\public\pubscan\quantalang\examples\quickstart\hello.bld` |
| Profile | `console-only` |
| Compiler version | `1.0.6` |
| Check command exit code | 0 |
| Verify command exit code | 0 |
| Receipt status | `passed` |
| Verify status | `passed` |
| Verify check count | 18 |
| Source digest | `0e542c60fbd874a38a2a3a87eaf61be04532a0df23e3ea25512d03301883dfae` |
| Input graph digest | `038a6f3aba486917d0ccbb9e4c0e858d0e79a8d1230450c3c40ca7dd08026d40` |
| Policy profile digest | `30462cb37d20d7c5cd2e156b62a8deeb53fc89f647e913b22c9e42033b53c4ce` |
| Declared effects | `{'main': ['Console']}` |
| Observed capabilities | `{'main': {'Console': ['println!']}}` |
| Adapter measurement count | 10 |
| Adapter measurement MATCH count | 10 |
| Adapter measurement DRIFT count | 0 |
| Artifact seal | `acae9b8ed2c0763e1f2e03f95ab05c316331da6f535932744561ba9114e7b361` |
| Promoted natural laws | 0 |

## Adapter Measurements

| Measurement | Status | Claim |
| --- | --- | --- |
| `buildc_check.receipt_schema` | MATCH | receipt schema is buildlang-check-receipt/v1 |
| `buildc_check.receipt_status` | MATCH | check receipt status is passed |
| `buildc_check.source_digest` | MATCH | source digest is sha256 hex |
| `buildc_check.input_graph_digest` | MATCH | input graph digest is sha256 hex |
| `buildc_check.policy_profile` | MATCH | policy profile is console-only |
| `buildc_check.policy_status` | MATCH | policy status is passed |
| `buildc_check.declared_effects` | MATCH | main declares Console effect |
| `buildc_check.observed_capabilities` | MATCH | main observes Console println! capability |
| `buildc_check.diagnostics` | MATCH | diagnostics are empty |
| `buildc_check.verify_report` | MATCH | receipt verify required checks all passed |

## Source Anchors

| Source | URL | Status |
| --- | --- | --- |
| BuildLang local usage | `C:\dev\public\pubscan\quantalang\USAGE.md` | `LOCAL_SOURCE` |
| BuildLang local README | `C:\dev\public\pubscan\quantalang\README.md` | `LOCAL_SOURCE` |
| Pass 0091 corpus adapter | `docs/research/dogfood/pass-0091-ledger.md` | `LOCAL_BASELINE` |

## Product Finding

This is the first structured compiler-receipt bridge in the dogfood lane. The
market-relevant piece is not that the hello-world fixture is hard. It is that a
language/runtime receipt can now move into the same proof machinery as market
research packets, agent action receipts, and scientific measurement packets.

The next proof step should use a richer effect surface and a negative policy
fixture, so the packet demonstrates both admission and rejection behavior.

## Tool Findings

- Forum route receipt: `MATCH`, `needs_escalation=true`.
- Index context envelope: `MATCH`, graph pack SHA256
  `8ee383e19ae9a6141bee70de733fb6aa09201ff9d284ce6778ce58b06e6b68b2`.
- Telos status receipt: `MATCH`, tool version `0.1.0`.
- Gather packet receipt: SHA256
  `f11d74ccf0fb62a037877edafe143bfb769b56ab18ccf8e0c45cece9c9075add`,
  digest seal `e8797c0931b88da08e9b42e4200caa119a6ed4562187fb06205700b41f430be8`.
- Gather brief receipt: SHA256
  `0823a3fa902fd8d7f05eea82f319e5c3a0525c1a4cb1eb3663fad0f3cc478d7c`,
  digest seal `aa0e4ccf7ddaabe7cade5d323f39fe0142459cf4cbcd35561ef0147cde4a8a6f`.
- Crucible result: 10 claims, 10 MATCH, 0 DRIFT, 0 UNVERIFIABLE.
- Crucible thesis id: `aa661216c790e6c0`.
- Crucible assessment seal:
  `dbdd01d28d6998d64755addb0043573a8c280213e6aa1be86d33a2f2bc2ee74f`.
- Crucible registry stats after this pass: 81 theses, 666 claims, 666 MATCH,
  0 DRIFT, 0 UNVERIFIABLE.

## Boundaries

This pass is a source-level compiler receipt adapter. It does not prove
BuildLang replaces Julia, does not prove scientific discovery, does not prove
full compiler correctness, and does not promote a natural law.

## Verification

```powershell
python -m py_compile docs\research\dogfood\tools\compose_buildlang_check_receipt_adapter.py docs\research\dogfood\tools\test_buildlang_check_receipt_adapter.py docs\research\dogfood\tools\validate_pass_0092_buildlang_check_receipt_adapter.py docs\research\dogfood\tools\probe_buildlang_check_receipt_adapter.py
python docs\research\dogfood\tools\probe_buildlang_check_receipt_adapter.py
python docs\research\dogfood\tools\test_buildlang_check_receipt_adapter.py
python docs\research\dogfood\tools\validate_pass_0092_buildlang_check_receipt_adapter.py
crucible run docs\research\dogfood\crucible\pass-0092-thesis.json --measurements docs\research\dogfood\crucible\pass-0092-measurements.json --registry docs\research\dogfood\crucible\registry --report docs\research\dogfood\crucible\pass-0092-report.md --out docs\research\dogfood\crucible\pass-0092-run.json --json
gather docs docs\research\dogfood\packets\102-buildlang-check-receipt-adapter.md --json
gather docs docs\research\dogfood\briefs\102-buildlang-check-receipt-adapter-brief.md --json
crucible registry stats docs\research\dogfood\crucible\registry --json
```

## Next Pass

Normalize the supplied YouTube research URLs into source-lead receipts, separate
metadata from technical claims, and map the resulting themes into the next
BuildLang/Telos growth-vector experiments.
