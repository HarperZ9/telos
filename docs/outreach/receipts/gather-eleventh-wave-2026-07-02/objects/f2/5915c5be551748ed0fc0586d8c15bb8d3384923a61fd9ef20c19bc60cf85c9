# Pass 0077 Ledger: Path-Selector Contract Scorecard

Date: 2026-07-01

Status: `MATCH_PATH_SELECTOR_CONTRACT_SCORECARD`

## Purpose

Turn the pass 0076 Index focus gap into a minimum
`IndexPathSelectorReceipt/v1` contract, then rank the next product motions
using local dogfood evidence instead of strategy prose alone.

## Artifacts

| Artifact | Purpose |
| --- | --- |
| `tools/compose_path_selector_contract_scorecard.py` | Contract and scorecard composer. |
| `tools/test_path_selector_contract_scorecard.py` | Focused scorecard test. |
| `tools/probe_path_selector_contract_scorecard.py` | Packet, thesis, and measurement generator. |
| `tools/validate_pass_0077_path_selector_contract_scorecard.py` | Validator for contract, evidence, rankings, and promotion boundaries. |
| `schemas/path-selector-contract-scorecard-pass-0077.json` | `PathSelectorContractGrowthScorecard/v1` artifact. |
| `schemas/pass-0077-path-selector-contract-scorecard-validator-result.json` | Validator receipt. |
| `schemas/tool-receipts-pass-0077.json` | Compact Index, Forum, Gather, Crucible, Telos, and shell receipts. |
| `packets/087-path-selector-contract-scorecard.md` | Human-readable contract scorecard packet. |
| `adversarial/pass-0077-path-selector-contract-scorecard-steelman.md` | Local steelman. |
| `crucible/pass-0077-thesis.json` | Falsifiable claims. |
| `crucible/pass-0077-measurements.json` | Measurements/evidence. |
| `crucible/pass-0077-report.md` | Crucible report. |
| `crucible/pass-0077-run.json` | Crucible run record. |

## Contract

`IndexPathSelectorReceipt/v1` should emit source-ref-only context receipts for
explicit path selectors under a workspace root. Minimum required fields:
`root`, `selectors`, `selector_results`, `source_refs`, `graph_pack_sha256`,
`freshness_root_sha256`, `raw_source_included`, `source_refs_only`,
`missing_selector_rejections`, and `join_key`.

The contract rejects three overclaims:

- repo-root context is not path-scoped context;
- missing paths such as `build-universe` are not silently covered;
- the bridge is not implemented until Index emits this receipt natively or an
  adapter emits an equivalent receipt.

## Ranked Motions

| Rank | Motion | Score | Interpretation |
| --- | --- | ---: | --- |
| 1 | `buildlang_proof_packets` | 4.38 | Highest current demo readiness because passes 0074-0076 already bind source refs, live `buildc` corpus verification, a domain-envelope join, and a precise Index path-selector gap. |
| 2 | `ai4science_research_packets` | 3.96 | Highest mission upside, but harder domain validation and lower near-term demo readiness. |
| 3 | `visual_truth_packets` | 3.88 | Distinctive and credible with existing color proof-kit work, but hardware calibration claims must stay fenced until sensor-backed receipts exist. |

Primary 30-day push hypothesis: ship the Index path-selector receipt and wrap
the live `buildc` corpus receipt into a public BuildLang proof-packet demo
first. This is not a retreat from the larger mission; it is the shortest
verified path to improving the shared substrate that AI4Science and visual
truth packets also need.

## Growth Vectors

- `path_scoped_source_ref_receipts`: selected subsystem source refs for large
  monorepos and scientific codebases.
- `proof_packet_builder_cli`: one command joining Gather source, Index context,
  Forum route, action receipts, and Crucible verdicts.
- `negative_fixture_market_positioning`: make overclaim refusal visible as a
  product trust feature.
- `visual_truth_foundry`: connect color/rendering/display evidence to AI and
  scientific proof systems.
- `ai4science_claim_ledger`: maintain claim-level continuity across literature,
  model runs, proof attempts, and experiments.

## Tool Findings

- Index status was `MATCH` at version `2.8.0`; pass 0077 defines the receipt
  contract that would close the pass 0076 path-selector gap.
- Forum status was `MATCH` at version `1.12.0`.
- Gather read packet 087 with SHA256
  `6045953f70190af604e29b84cebf0fb9b15a765ceff75853af756365ec1acd2d` and digest
  seal `48f1aac7794bde1aa4bfa2020cee6d84b2220c582f6a83d9d9a5f40363b69a00`.
- Crucible result: 8 claims, 8 MATCH, 0 DRIFT, 0 UNVERIFIABLE.
- Crucible thesis id: `0f27f2c98b0530ce`.
- Crucible assessment seal:
  `361364ecc91a70d10f6483b5bd2f7bcf7733dc652424da055dbe65b3da9ef5af`.
- Crucible registry stats after this pass: 65 theses, 537 claims, 537 MATCH,
  0 DRIFT, 0 UNVERIFIABLE.

## Verification

```powershell
python docs\research\dogfood\tools\test_path_selector_contract_scorecard.py
python -m py_compile docs\research\dogfood\tools\compose_path_selector_contract_scorecard.py docs\research\dogfood\tools\probe_path_selector_contract_scorecard.py docs\research\dogfood\tools\test_path_selector_contract_scorecard.py docs\research\dogfood\tools\validate_pass_0077_path_selector_contract_scorecard.py
python docs\research\dogfood\tools\probe_path_selector_contract_scorecard.py
python docs\research\dogfood\tools\validate_pass_0077_path_selector_contract_scorecard.py
crucible run docs\research\dogfood\crucible\pass-0077-thesis.json --measurements docs\research\dogfood\crucible\pass-0077-measurements.json --registry docs\research\dogfood\crucible\registry --report docs\research\dogfood\crucible\pass-0077-report.md --out docs\research\dogfood\crucible\pass-0077-run.json --json
gather docs docs\research\dogfood\packets\087-path-selector-contract-scorecard.md --json
crucible registry stats docs\research\dogfood\crucible\registry --json
index status --json
forum status --json
```

## Next Pass

Produce an executable `IndexPathSelectorReceipt/v1` fixture for `buildlang` and
`compiler`, with `build-universe` rejected, then join that receipt back into the
BuildLang domain envelope as a replacement for root-context fallback.
