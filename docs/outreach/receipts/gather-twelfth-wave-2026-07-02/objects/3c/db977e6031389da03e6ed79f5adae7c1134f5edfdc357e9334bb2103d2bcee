# Pass 0107 Ledger: Reaction-Network Corpus Harness Receipt

Date: 2026-07-01

Status: `REACTION_NETWORK_CORPUS_HARNESS_RECEIPT_MATCH`

## Purpose

Scale pass 0106 from one stoichiometric invariant into a four-case
reaction-network corpus harness. This pass checks three closed networks, rejects
one open degradation network, and binds the result to the BuildLang/buildc
scientific-runtime lane as a target receipt.

The result is a scoped `LAW_CANDIDATE`, not a promoted natural law.

## Artifacts

| Artifact | Purpose |
| --- | --- |
| `tools/compose_reaction_network_corpus_harness_receipt.py` | Builds the corpus, exact residual checks, numerical probes, BuildLang bridge, YouTube binding, and Forum/Index/Telos receipts. |
| `tools/test_reaction_network_corpus_harness_receipt.py` | Focused TDD test for corpus counts, residuals, open rejection, and BuildLang bridge fields. |
| `tools/probe_reaction_network_corpus_harness_receipt.py` | Packet, brief, steelman, thesis, measurement, and compact receipt generator. |
| `tools/validate_pass_0107_reaction_network_corpus_harness.py` | Independent validator for seal, corpus counts, residuals, bridge fields, and boundaries. |
| `schemas/reaction-network-corpus-harness-receipt-pass-0107.json` | `ReactionNetworkCorpusHarnessReceipt/v1` artifact. |
| `schemas/pass-0107-reaction-network-corpus-harness-validator-result.json` | Validator receipt. |
| `schemas/tool-receipts-pass-0107.json` | Compact corpus, BuildLang bridge, Forum, Index, Telos, compose, and test receipts. |
| `packets/117-reaction-network-corpus-harness-receipt.md` | Human-readable corpus harness packet. |
| `briefs/117-reaction-network-corpus-harness-brief.md` | Buyer-facing corpus harness brief. |
| `adversarial/pass-0107-reaction-network-corpus-harness-steelman.md` | Local pass 0107 steelman. |
| `crucible/pass-0107-thesis.json` | Falsifiable claims. |
| `crucible/pass-0107-measurements.json` | Measurements/evidence. |
| `crucible/pass-0107-report.md` | Crucible report. |
| `crucible/pass-0107-run.json` | Crucible run record. |

## Corpus Measurements

| Check | Result |
| --- | --- |
| Stoichiometric source pass | 0106 |
| BuildLang native source pass | 0095 |
| YouTube scorecard pass | 0096 |
| YouTube roadmap pass | 0102 |
| Valid YouTube videos | 19 |
| BuildLang scientific-runtime videos | 14 |
| Corpus networks | 4 |
| Closed MATCH networks | 3 |
| Expected open rejections | 1 |
| Derived invariant count | 4 |
| Candidate check count | 5 |
| Artifact file SHA256 | `065ee7a1bbf7ae6c5a42ab28fe4c3761d95b5a44b8c1dfdb1e530dc0dcee6f53` |
| Artifact seal | `9f9143003830feb042ae906a61e2313297b92c81688beab1f370fa727395bd27` |

## Network Cases

| Network | Expected | Candidate Invariants | Result |
| --- | --- | --- | --- |
| `closed_cycle_abc` | closed MATCH | `A+B+C`, residual `[0,0,0]` | `MATCH`; max drift `3.9968028886505635e-15` |
| `reversible_dimerization` | closed MATCH | `A+2*B`, residual `[0,0]` | `MATCH`; max drift `2.220446049250313e-15` |
| `enzyme_product_skeleton` | closed MATCH | `E+ES`; `S+ES+P`; residuals `[0,0,0]` | `MATCH`; basis dimension 2 |
| `open_degradation` | open rejection | `A`, residual `[-1]` | `DRIFT_EXPECTED`; max drift `0.7876978722105867` |

## BuildLang Bridge

| Field | Result |
| --- | --- |
| Bridge status | `TARGET_SPECIFIED_WITH_EXISTING_BUILDC_RECEIPT` |
| Compiler | `buildc` |
| Compiler version | `1.0.6` |
| Native pass | 0095 |
| Native status | `BUILDLANG_NATIVE_OPTIMIZATION_KERNEL_RECEIPT_MATCH` |
| Source digest | `2480f503aa672459ccdd437a93f8d50c71dbc9b90d1ce236a52259727e1e29e9` |
| Verify check count | 18 |
| Target kernel | `reaction_network_invariant_kernel.bld` |
| Required receipts | `stoichiometric_matrix_digest`, `conservation_vector_receipt`, `residual_zero_check`, `numeric_tolerance_receipt`, `negative_fixture_receipt` |

## Product Finding

The useful strategic move is to turn single proof packets into corpus harnesses.
The YouTube critical-data set points toward AI4Science and accountable
scientific runtime. Pass 0107 answers that by proving the corpus harness shape
first, then explicitly naming the BuildLang runtime receipt gap.

This avoids a common failure mode: claiming a scientific language bridge before
there is a repeatable corpus and negative fixture. The bridge is valuable only
when it carries matrix digest, vector receipt, residual-zero check, tolerance
receipt, and negative-fixture receipt together.

## Tool Findings

- TDD red observed before the composer existed: `FileNotFoundError`.
- Forum route receipt: `MATCH`.
- Index context envelope: `MATCH`.
- Telos status receipt: `MATCH`, tool version `0.1.0`.
- Gather packet receipt: SHA256
  `b1cc0878f7e78b6b27fc39da6f8605d8d7295ee1b3572c3c34e1ace1fa29763c`,
  digest seal `bbe86bee8efe68f8ab4dc28b9ab0efe7d9c8057f53a5c94b017e57f1ca269283`.
- Gather brief receipt: SHA256
  `b9353271ca10785a529cfcfc305f36941589c90dc9bde6fb72baa5f9aa61a108`,
  digest seal `adf870bd6fe46d80786bb7d356b4b689e8ca9a072a7874a6f6e049c074d6b339`.
- Crucible result: 11 claims, 11 MATCH, 0 DRIFT, 0 UNVERIFIABLE.
- Crucible thesis id: `eb2708352f968db5`.
- Crucible assessment seal:
  `9b8c08a0fbbe648328914b47e62c9367a75a99c1187e5c8eab6add05f84096d6`.
- Crucible registry stats after this pass: 96 theses, 807 claims, 807 MATCH,
  0 DRIFT, 0 UNVERIFIABLE.

## Boundaries

This pass does not compile a new BuildLang chemistry kernel, prove scientific
language replacement, promote a natural law, or claim biological discovery. It
proves a bounded corpus harness and specifies the missing runtime bridge.

## Verification

```powershell
python docs\research\dogfood\tools\test_reaction_network_corpus_harness_receipt.py
python -m py_compile docs\research\dogfood\tools\compose_reaction_network_corpus_harness_receipt.py docs\research\dogfood\tools\test_reaction_network_corpus_harness_receipt.py docs\research\dogfood\tools\validate_pass_0107_reaction_network_corpus_harness.py docs\research\dogfood\tools\probe_reaction_network_corpus_harness_receipt.py
python docs\research\dogfood\tools\probe_reaction_network_corpus_harness_receipt.py
python docs\research\dogfood\tools\validate_pass_0107_reaction_network_corpus_harness.py
crucible run docs\research\dogfood\crucible\pass-0107-thesis.json --measurements docs\research\dogfood\crucible\pass-0107-measurements.json --registry docs\research\dogfood\crucible\registry --report docs\research\dogfood\crucible\pass-0107-report.md --out docs\research\dogfood\crucible\pass-0107-run.json --json
gather docs docs\research\dogfood\packets\117-reaction-network-corpus-harness-receipt.md --json
gather docs docs\research\dogfood\briefs\117-reaction-network-corpus-harness-brief.md --json
crucible registry stats docs\research\dogfood\crucible\registry --json
```

## Next Pass

Create a generated BuildLang target fixture or explicit non-execution adapter
for `reaction_network_invariant_kernel.bld`, then require buildc receipt
verification before the chemistry kernel can be considered more than a target
spec.
