# Pass 0091 Ledger: BuildLang Corpus Crucible Adapter

Date: 2026-07-01

Status: `MATCH_BUILDLANG_CORPUS_CRUCIBLE_ADAPTER`

## Purpose

Convert live `buildc corpus verify` output into Crucible-ready measurements.
This pass advances the BuildLang/buildc proof-packet lane from a demo surface to
a concrete adapter: every expected corpus-verification line becomes a structured
measurement with evidence, deviation, tolerance, and status.

## Artifacts

| Artifact | Purpose |
| --- | --- |
| `tools/compose_buildlang_corpus_crucible_adapter.py` | BuildLang corpus, repo-state, Forum, Index, and Telos composer. |
| `tools/test_buildlang_corpus_crucible_adapter.py` | Focused corpus, adapter-count, repo-state, and boundary test. |
| `tools/probe_buildlang_corpus_crucible_adapter.py` | Packet, brief, steelman, thesis, measurement, and compact receipt generator. |
| `tools/validate_pass_0091_buildlang_corpus_crucible_adapter.py` | Independent validator for seal, corpus run, adapter measurements, and boundaries. |
| `schemas/buildlang-corpus-crucible-adapter-pass-0091.json` | `BuildLangCorpusCrucibleAdapterReceipt/v1` artifact. |
| `schemas/pass-0091-buildlang-corpus-crucible-adapter-validator-result.json` | Validator receipt. |
| `schemas/tool-receipts-pass-0091.json` | Compact BuildLang corpus, adapter, Forum, Index, Telos, compose, and test receipts. |
| `packets/101-buildlang-corpus-crucible-adapter.md` | Human-readable BuildLang corpus adapter packet. |
| `briefs/101-buildlang-corpus-crucible-adapter-brief.md` | Concise product-strategy brief. |
| `adversarial/pass-0091-buildlang-corpus-crucible-adapter-steelman.md` | Local steelman of the adapter limits. |
| `crucible/pass-0091-thesis.json` | Falsifiable claims. |
| `crucible/pass-0091-measurements.json` | Measurements/evidence. |
| `crucible/pass-0091-report.md` | Crucible report. |
| `crucible/pass-0091-run.json` | Crucible run record. |

## Measurements

| Check | Result |
| --- | --- |
| Prior solver matrix pass | 0090 |
| BuildLang proof-surface pass | 0080 |
| BuildLang repo | `C:\dev\public\pubscan\quantalang` |
| BuildLang branch | `## fix/module-double-register` |
| BuildLang dirty count | 0 |
| `buildc corpus verify` status | MATCH |
| `buildc corpus verify` exit code | 0 |
| Corpus expected-line match count | 10 |
| Corpus expected-line drift count | 0 |
| Adapter measurement count | 10 |
| Adapter measurement MATCH count | 10 |
| Adapter measurement DRIFT count | 0 |
| Corpus stdout SHA256 | `fbe2daff8da1804b00cafe9a9fff36fc649429071b25f6a2561003255f6310d3` |
| Artifact seal | `0ecba8c12f9c041ed6dc3a126e5722afae3afe8881cd262f69adcafda4ca60ac` |
| Promoted natural laws | 0 |

## Adapter Measurements

| Measurement | Expected Line | Status |
| --- | --- | --- |
| `buildc_corpus.manifest_programs` | `manifest: 8 program(s)` | MATCH |
| `buildc_corpus.c_receipt` | `c receipt: ok` | MATCH |
| `buildc_corpus.rust_receipt` | `rust receipt: ok` | MATCH |
| `buildc_corpus.substrate_receipt` | `substrate receipt: ok` | MATCH |
| `buildc_corpus.mir_representation_receipt` | `mir representation receipt: ok` | MATCH |
| `buildc_corpus.memory_layout_receipt` | `memory layout receipt: ok` | MATCH |
| `buildc_corpus.module_graph_receipt` | `module graph receipt: ok` | MATCH |
| `buildc_corpus.symbol_graph_receipt` | `symbol graph receipt: ok` | MATCH |
| `buildc_corpus.lsp_dispatch_receipt` | `lsp dispatch receipt: ok` | MATCH |
| `buildc_corpus.c_execution` | `c execution: 8 passed` | MATCH |

## Source Anchors

| Source | URL | Status |
| --- | --- | --- |
| BuildLang local README | `C:\dev\public\pubscan\quantalang\README.md` | `LOCAL_SOURCE` |
| Pass 0090 solver matrix | `docs/research/dogfood/pass-0090-ledger.md` | `LOCAL_BASELINE` |
| Pass 0080 BuildLang proof surface | `docs/research/dogfood/pass-0080-ledger.md` | `LOCAL_BASELINE` |

## Product Finding

BuildLang/buildc now has the first explicit bridge from compiler corpus
verification to Crucible measurements. The adapter is intentionally simple:
line-presence measurements over known corpus-verification output. That is enough
to establish the contract shape, not enough to claim deep compiler correctness.

The next higher-value adapter should parse a `buildc check --receipt` JSON
object and emit measurements for source digests, policy profile, observed
effects, generated target, and receipt verification. That would move from
terminal-output witnessing to structured compiler-receipt witnessing.

## Tool Findings

- Forum route receipt: `MATCH`, `needs_escalation=true`.
- Index context envelope: `MATCH`, schema `project-telos.context-envelope/v1`,
  graph pack SHA256
  `8ee383e19ae9a6141bee70de733fb6aa09201ff9d284ce6778ce58b06e6b68b2`.
- Telos status receipt: `MATCH`, tool version `0.1.0`.
- Gather packet receipt: SHA256
  `4cba65f534c59c82b6827c9c259789d5896beb700f1443a87f69401fdbf708b7`,
  digest seal `87da3a99183b7f8d16617d7f00183cb92fa7b3149447fbb15dea64a4d51833bd`.
- Gather brief receipt: SHA256
  `d33ac6ab6c71ad6ee93468a73da23d0f14e89d3c86397ae984d0decfbdc8fedd`,
  digest seal `20c9c1a354820473d670db57153d309ca830f40a82eaff36755644f996be72cc`.
- Crucible result: 8 claims, 8 MATCH, 0 DRIFT, 0 UNVERIFIABLE.
- Crucible thesis id: `925dda9fef050ba8`.
- Crucible assessment seal:
  `20882ec1cd23c058b7542166d86e6382c9b6b712b1bb2752df0fb834116fe203`.
- Crucible registry stats after this pass: 80 theses, 656 claims, 656 MATCH,
  0 DRIFT, 0 UNVERIFIABLE.

## Boundaries

This pass is a compiler-verification adapter. It does not prove BuildLang
replaces Julia, does not prove scientific discovery, does not prove full
compiler correctness, and does not promote a natural law.

## Verification

```powershell
python -m py_compile docs\research\dogfood\tools\compose_buildlang_corpus_crucible_adapter.py docs\research\dogfood\tools\test_buildlang_corpus_crucible_adapter.py docs\research\dogfood\tools\validate_pass_0091_buildlang_corpus_crucible_adapter.py docs\research\dogfood\tools\probe_buildlang_corpus_crucible_adapter.py
python docs\research\dogfood\tools\probe_buildlang_corpus_crucible_adapter.py
python docs\research\dogfood\tools\test_buildlang_corpus_crucible_adapter.py
python docs\research\dogfood\tools\validate_pass_0091_buildlang_corpus_crucible_adapter.py
crucible run docs\research\dogfood\crucible\pass-0091-thesis.json --measurements docs\research\dogfood\crucible\pass-0091-measurements.json --registry docs\research\dogfood\crucible\registry --report docs\research\dogfood\crucible\pass-0091-report.md --out docs\research\dogfood\crucible\pass-0091-run.json --json
gather docs docs\research\dogfood\packets\101-buildlang-corpus-crucible-adapter.md --json
gather docs docs\research\dogfood\briefs\101-buildlang-corpus-crucible-adapter-brief.md --json
crucible registry stats docs\research\dogfood\crucible\registry --json
```

## Next Pass

Create a source-level `buildc check --receipt` adapter for one `.bld` fixture.
The adapter should parse the emitted JSON receipt, verify it with
`buildc receipt verify`, and map source digest, policy, effects, and target
metadata into Crucible measurements.
