# Pass 0078 Ledger: Index Path-Selector Receipt

Date: 2026-07-01

Status: `MATCH_INDEX_PATH_SELECTOR_RECEIPT_FIXTURE`

## Purpose

Produce an executable `IndexPathSelectorReceipt/v1` adapter fixture over the
external BuildLang checkout. This turns the pass 0077 contract into a concrete
source-ref receipt that can be joined into the BuildLang domain envelope.

## Artifacts

| Artifact | Purpose |
| --- | --- |
| `tools/compose_index_path_selector_receipt.py` | Path-selector receipt composer. |
| `tools/test_index_path_selector_receipt.py` | Focused path-selector receipt test. |
| `tools/probe_index_path_selector_receipt.py` | Packet, thesis, and measurement generator. |
| `tools/validate_pass_0078_index_path_selector_receipt.py` | Validator for selector results, source refs, and privacy boundaries. |
| `schemas/index-path-selector-receipt-pass-0078.json` | Generated `IndexPathSelectorReceipt/v1` fixture. |
| `schemas/pass-0078-index-path-selector-receipt-validator-result.json` | Validator receipt. |
| `schemas/tool-receipts-pass-0078.json` | Compact Gather, Crucible, Telos, and shell receipts. |
| `packets/088-index-path-selector-receipt.md` | Human-readable path-selector receipt packet. |
| `adversarial/pass-0078-index-path-selector-receipt-steelman.md` | Local steelman. |
| `crucible/pass-0078-thesis.json` | Falsifiable claims. |
| `crucible/pass-0078-measurements.json` | Measurements/evidence. |
| `crucible/pass-0078-report.md` | Crucible report. |
| `crucible/pass-0078-run.json` | Crucible run record. |

## Selector Results

| Selector | Status | Files | Source Refs | Notes |
| --- | --- | ---: | ---: | --- |
| `buildlang` | `MATCH` | 342 | 64 | Selected source-ref sample. |
| `compiler` | `MATCH` | 145 | 64 | Selected source-ref sample; generated `target` output excluded. |
| `build-universe` | `REJECT` | 0 | 0 | Missing selector in this checkout. |

Total source refs: 128. Raw source payloads are not included. The fixture uses
source refs only and records a graph-pack digest
`d3bae65c0703599721168f6cf6e77fa44bb85445bd03752d1fc2a9c4a04e51d8`.

## Steelman

This pass is an adapter fixture, not native Index path-selection support. It is
still useful because downstream Telos domain envelopes can consume the exact
shape expected from native Index later. The next pass should join this receipt
into `buildlang_buildc` while keeping the adapter label visible, so we do not
overclaim that Index itself has gained the feature.

## Tool Findings

- Gather read packet 088 with SHA256
  `dc0cc324d5648de0f38883977075088c9f80db243c66a66240a9ea890414b76f` and digest
  seal `4eac5f9c577b75fc8cd165dfd6782a585940629de87cf33db196d4e3efb02539`.
- Crucible result: 8 claims, 8 MATCH, 0 DRIFT, 0 UNVERIFIABLE.
- Crucible thesis id: `37e5e0377165e3dd`.
- Crucible assessment seal:
  `0b0739ca537a5376db859659eee7b38fcf54705adce752781004c77d781cd2bd`.
- Crucible registry stats after this pass: 66 theses, 545 claims, 545 MATCH,
  0 DRIFT, 0 UNVERIFIABLE.

## Verification

```powershell
python docs\research\dogfood\tools\test_index_path_selector_receipt.py
python -m py_compile docs\research\dogfood\tools\compose_index_path_selector_receipt.py docs\research\dogfood\tools\probe_index_path_selector_receipt.py docs\research\dogfood\tools\test_index_path_selector_receipt.py docs\research\dogfood\tools\validate_pass_0078_index_path_selector_receipt.py
python docs\research\dogfood\tools\probe_index_path_selector_receipt.py
python docs\research\dogfood\tools\validate_pass_0078_index_path_selector_receipt.py
crucible run docs\research\dogfood\crucible\pass-0078-thesis.json --measurements docs\research\dogfood\crucible\pass-0078-measurements.json --registry docs\research\dogfood\crucible\registry --report docs\research\dogfood\crucible\pass-0078-report.md --out docs\research\dogfood\crucible\pass-0078-run.json --json
gather docs docs\research\dogfood\packets\088-index-path-selector-receipt.md --json
crucible registry stats docs\research\dogfood\crucible\registry --json
```

## Next Pass

Join the pass 0078 `IndexPathSelectorReceipt/v1` into the BuildLang domain
envelope as the workspace-context layer, replacing root-context fallback while
preserving the adapter/non-native boundary.
