# Pass 0076 Ledger: BuildLang Index Focus Bridge

Date: 2026-07-01

Status: `MATCH_BUILDLANG_INDEX_FOCUS_BRIDGE_REQUIRED`

## Purpose

Probe whether Index can produce path-scoped context for the external
BuildLang/buildc checkout today. The result is a verified negative finding:
repo-root context works, but explicit path selectors for `buildlang`,
`compiler`, and `build-universe` are rejected by the current focus interface.

## Artifacts

| Artifact | Purpose |
| --- | --- |
| `tools/compose_buildlang_index_focus_bridge.py` | Live Index probe and bridge composer. |
| `tools/test_buildlang_index_focus_bridge.py` | Focused bridge test. |
| `tools/probe_buildlang_index_focus_bridge.py` | Packet, thesis, and measurement generator. |
| `tools/validate_pass_0076_buildlang_index_focus_bridge.py` | Validator for root context, focus rejections, and bridge boundaries. |
| `schemas/buildlang-index-focus-bridge-pass-0076.json` | `BuildLangIndexFocusBridge/v1` artifact. |
| `schemas/pass-0076-buildlang-index-focus-bridge-validator-result.json` | Validator receipt. |
| `schemas/tool-receipts-pass-0076.json` | Compact Index, Forum, BuildLang, Gather, Crucible, Telos, and shell receipts. |
| `packets/086-buildlang-index-focus-bridge.md` | Human-readable bridge packet. |
| `adversarial/pass-0076-buildlang-index-focus-bridge-steelman.md` | Local steelman. |
| `crucible/pass-0076-thesis.json` | Falsifiable claims. |
| `crucible/pass-0076-measurements.json` | Measurements/evidence. |
| `crucible/pass-0076-report.md` | Crucible report. |
| `crucible/pass-0076-run.json` | Crucible run record. |

## Measurements

| Check | Result |
| --- | --- |
| BuildLang root | `C:/dev/public/pubscan/quantalang` |
| Root Index context | `MATCH` |
| Root context source refs | 1 (`README.md`) |
| Path-scoped context | `false` |
| Bridge required | `true` |
| Focus probes | 4 expected rejections |
| `buildlang` top-level path | present |
| `compiler` top-level path | present |
| `build-universe` top-level path | absent |
| Source receipt pass | 0074 |
| Source refs in BuildLang receipt | 13 |
| Negative fixtures | 8 |
| Unsupported claims | 0 |

## Focus Probe Results

```text
index context --root C:\dev\public\pubscan\quantalang --json --focus buildlang -> unknown project: 'buildlang'
index context --root C:\dev\public\pubscan\quantalang --json --focus compiler -> unknown project: 'compiler'
index context --root C:\dev\public\pubscan\quantalang --json --focus build-universe -> unknown project: 'build-universe'
index context-envelope --root C:\dev\public\pubscan\quantalang --json --focus buildlang --budget 3000 -> unknown focus repo: buildlang
```

## Steelman

This pass is valuable because it turns a vague integration gap into a concrete
tooling feature: Index needs a path-selector source-ref bridge. A proof packet
for BuildLang/buildc cannot rely only on root repo context once the product
promise becomes scientific compute, compiler receipts, color/rendering
measurements, finance/security kernels, and large codebase research.

The bridge should accept filesystem path selectors under `--root`, emit
source-ref manifests for selected directories/files, preserve source-ref-only
privacy, reject missing selections such as `build-universe`, and carry graph
and freshness receipts for the selected path manifest.

## Tool Findings

- Index status was `MATCH` at version `2.8.0`; root context works and focus
  path selectors reject as expected.
- Forum status was `MATCH` at version `1.12.0`; the next routed action is to
  assess verified bridge claims before public use.
- The external BuildLang checkout had local changes when probed:
  `M STATUS.md` and `?? docs/MATH-SYNTAX.md`. These were not modified by this
  pass.
- Gather read packet 086 with SHA256
  `8f4c4dffd18347461fb28ade23200a3feeb35f93290fc9d642efa8546c83764d` and digest
  seal `0df36a39323e829d0b9cc17b8794c822cfa711122034e01dfeab6a2608399e4a`.
- Crucible result: 8 claims, 8 MATCH, 0 DRIFT, 0 UNVERIFIABLE.
- Crucible thesis id: `f3bbaf7d62e6976b`.
- Crucible assessment seal:
  `470448b5532feb03f09608ebf321de735a81367b89c1d351408cb348db6e0d88`.
- Crucible registry stats after this pass: 64 theses, 529 claims, 529 MATCH,
  0 DRIFT, 0 UNVERIFIABLE.

## Verification

```powershell
python docs\research\dogfood\tools\test_buildlang_index_focus_bridge.py
python -m py_compile docs\research\dogfood\tools\compose_buildlang_index_focus_bridge.py docs\research\dogfood\tools\probe_buildlang_index_focus_bridge.py docs\research\dogfood\tools\test_buildlang_index_focus_bridge.py docs\research\dogfood\tools\validate_pass_0076_buildlang_index_focus_bridge.py
python docs\research\dogfood\tools\probe_buildlang_index_focus_bridge.py
python docs\research\dogfood\tools\validate_pass_0076_buildlang_index_focus_bridge.py
crucible run docs\research\dogfood\crucible\pass-0076-thesis.json --measurements docs\research\dogfood\crucible\pass-0076-measurements.json --registry docs\research\dogfood\crucible\registry --report docs\research\dogfood\crucible\pass-0076-report.md --out docs\research\dogfood\crucible\pass-0076-run.json --json
gather docs docs\research\dogfood\packets\086-buildlang-index-focus-bridge.md --json
crucible registry stats docs\research\dogfood\crucible\registry --json
index status --json
forum status --json
```

## Next Pass

Define the minimum `IndexPathSelectorReceipt/v1` contract and use it to score
three product motions: BuildLang proof packets, color/rendering measurement
packets, and AI4Science research packets.
