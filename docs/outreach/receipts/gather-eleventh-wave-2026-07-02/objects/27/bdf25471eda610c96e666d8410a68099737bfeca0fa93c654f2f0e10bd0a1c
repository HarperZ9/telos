# Pass 0074 Ledger: BuildLang Source-Ref Receipt

Date: 2026-07-01

Status: `MATCH_BUILDLANG_SOURCE_REF_RECEIPT`

## Purpose

Bind the BuildLang/buildc domain to actual source refs and a live executable
corpus verification receipt. This moves the BuildLang domain from strategy and
root-context fallback toward an evidence-carrying proof-packet input.

## Artifacts

| Artifact | Purpose |
| --- | --- |
| `tools/compose_buildlang_source_ref_receipt.py` | BuildLang source-ref and corpus verifier composer. |
| `tools/test_buildlang_source_ref_receipt.py` | Focused source-ref receipt test. |
| `tools/probe_buildlang_source_ref_receipt.py` | Packet, thesis, and measurement generator. |
| `tools/validate_pass_0074_buildlang_source_ref_receipt.py` | Validator for source refs, corpus verification, and scope boundaries. |
| `schemas/buildlang-source-ref-receipt-pass-0074.json` | `BuildLangSourceRefReceipt/v1` artifact. |
| `schemas/pass-0074-buildlang-source-ref-receipt-validator-result.json` | Validator receipt. |
| `schemas/tool-receipts-pass-0074.json` | Compact BuildLang, Gather, Crucible, Telos, and shell receipts. |
| `packets/084-buildlang-source-ref-receipt.md` | Human-readable BuildLang source-ref receipt packet. |
| `adversarial/pass-0074-buildlang-source-ref-receipt-steelman.md` | Local steelman. |
| `crucible/pass-0074-thesis.json` | Falsifiable claims. |
| `crucible/pass-0074-measurements.json` | Measurements/evidence. |
| `crucible/pass-0074-report.md` | Crucible report. |
| `crucible/pass-0074-run.json` | Crucible run record. |

## Measurements

| Check | Result |
| --- | --- |
| BuildLang root | `C:/dev/public/pubscan/quantalang` |
| Source refs | 13 |
| Live command | `cargo run --quiet --bin buildc -- corpus verify` |
| Corpus verifier status | `MATCH` |
| Expected verifier lines | 10 MATCH, 0 DRIFT |
| Semantic programs | 8 |
| Production backend claim | `C backend only` |
| Negative fixtures | 8 |
| Unsupported claims | 0 |

## Corpus Verify Output

The live command reported:

```text
manifest: 8 program(s)
c receipt: ok
rust receipt: ok
substrate receipt: ok
mir representation receipt: ok
memory layout receipt: ok
module graph receipt: ok
symbol graph receipt: ok
lsp dispatch receipt: ok
c execution: 8 passed
```

## Steelman

This is a strong BuildLang proof-packet input, but the scope is bounded. It
does not prove that all backends are production-ready. It does not prove
self-hosting. It does not prove Julia replacement. It proves source refs plus a
live semantic corpus receipt path over 8 programs, with C as the production
execution anchor and the other receipt surfaces held to their own maturity
lanes.

## Tool Findings

- Gather read packet 084 with SHA256 `ae02477ce37cb9d01b27a3ca3eca9bb57a4bb25dff32f4eabbe8292e3a7a8b0c` and digest seal `4b9de4c923e322d292788e2f03e1c6bf153cb4886a154482a42468e04bcd004f`.
- Crucible result: 8 claims, 8 MATCH, 0 DRIFT, 0 UNVERIFIABLE.
- Crucible thesis id: `4ba9bb823fa2a749`.
- Crucible assessment seal: `6698934b24693c6962f01c7f352ca315d9afd4140fee84ebf18bdf68039c46ee`.
- Crucible registry stats after this pass: 62 theses, 513 claims, 513 MATCH, 0 DRIFT, 0 UNVERIFIABLE.

## Verification

```powershell
python docs\research\dogfood\tools\test_buildlang_source_ref_receipt.py
python docs\research\dogfood\tools\probe_buildlang_source_ref_receipt.py
python docs\research\dogfood\tools\validate_pass_0074_buildlang_source_ref_receipt.py
crucible run docs\research\dogfood\crucible\pass-0074-thesis.json --measurements docs\research\dogfood\crucible\pass-0074-measurements.json --registry docs\research\dogfood\crucible\registry --report docs\research\dogfood\crucible\pass-0074-report.md --out docs\research\dogfood\crucible\pass-0074-run.json --json
```

## Next Pass

Join this BuildLang source-ref receipt into the `TelosDomainFocusEnvelope/v1`
for `buildlang_buildc`, replacing the generic source-intake layer for that
domain while keeping the Index root-context limitation visible.
