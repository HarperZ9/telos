# Pass 0138 Ledger - SAIR Stage 1 Judge Repository Adapter

Date: 2026-07-02

## Objective

Move the SAIR Stage 1 lane from a synthetic local proof-packet fixture into a
source-pinned public judge repository adapter. This pass observes the public
repository at a concrete HEAD, runs its local no-secret command surface, and
keeps hosted model calls fenced.

## Outputs

| Artifact | SHA-256 |
| --- | --- |
| schemas/sair-stage1-judge-repo-adapter-pass-0138.json | 3F3BEA0A4E3D4AF3FE1E1395DB0CC1AFF748F95075ACA3B88ED0FD17B67A4FBB |
| packets/148-sair-stage1-judge-repo-adapter.md | 2D14E003BE50E70338EF49C62EA97FA20027ECA902CCCBF9A052AFF8F6640F37 |
| briefs/148-sair-stage1-judge-repo-adapter-brief.md | F9B01EE4AF2603D07DD0EDE2312A2D3054F5AE2C339C93C867EAE421E5C05118 |
| adversarial/pass-0138-sair-stage1-judge-repo-adapter-steelman.md | 358F26DEA733987981D96DF8CD77F0634C643023AC0741D18156148C4B194872 |
| schemas/tool-receipts-pass-0138.json | A0FDE022B05719C51BEB56A14FA2423AD45DE2383D043C42E0C81732792AB1D9 |
| tools/compose_sair_stage1_judge_repo_adapter.py | 453B39580CEA771B9439AB99C3798DE4161CB9A909195E1D827748DE68A59BC5 |
| tools/test_sair_stage1_judge_repo_adapter.py | 8593E77AFEA5A0F81F455A30C7AB05BEF185B06A83F418D72FA3BD9AB30B003B |
| tools/validate_pass_0138_sair_stage1_judge_repo_adapter.py | 508B78ED332C82C7E63713B2684A635AE50AD1703540EE388C34E05E98FB472D |
| tools/probe_sair_stage1_judge_repo_adapter.py | EE7527D5A9643BE19674DF83B04F3E0B08895254C616DC59E3333031DD003709 |
| crucible/pass-0138-thesis.json | 91206FC8751527BE354E005547EF1BB2518B0A74908200DE415018F469C25A39 |
| crucible/pass-0138-measurements.json | CA1D0B8386B7AEAFA146DA1FBA538191F7EAF6E9010EEEEA42A9F2A54E474004 |
| crucible/pass-0138-report.md | 02449A03BD29D803C14025279FF17B01B2D3A010606BDCF80893EB2D2F621FF4 |
| crucible/pass-0138-run.json | 0F1291F0A5EC646F15EAD7FDA03E0BC949B6F16EC83EFEEA631673E744274402 |

## Result Snapshot

| Field | Value |
| --- | --- |
| Schema | `SAIRStage1JudgeRepoAdapterReceipt/v1` |
| Status | `SAIR_STAGE1_JUDGE_REPO_ADAPTER_MATCH` |
| Artifact seal | `2dc78bdbcfd8ec3350cb468ee5820cc3669ed32c2ff266295dd79a6141af8a0a` |
| Repo HEAD | `fe00cf9e9080dba6634882c9316b73d536c4fe60` |
| Observed files | `15` |
| Source hashes | `15` |
| Local command receipts | `4` |
| Negative fixtures | `6` |
| External model calls | `0` |
| Promoted results | `0` |

## Crucible

| Field | Value |
| --- | --- |
| Thesis id | `165b2b80212682d5` |
| Claims | `10` |
| `MATCH` | `10` |
| `DRIFT` | `0` |
| `UNVERIFIABLE` | `0` |
| Verdict seal | `5e6ca203275ca51aed5a524370affad417fa23fc393f58c5de17f686240e0fdf` |
| Measurement seal | `926c179aaa6c03e116f2d6b0e38b1bf137888cbbbeae6a9b2143e29136e6eaac` |

## Tooling Gap

Forum needs a route for formal_math_competition_repo_adapter so source-lead, fixture, public judge repo, hosted-model receipt, and Lean certificate stages are distinguishable.

## Next Pass Queue

1. Add a hosted-model attempt receipt with redacted provider call evidence.
2. Add a Stage 2 Lean certificate receipt adapter.
3. Add a BuildLang/buildc exact equational-reasoning branch.
4. Add Forum routing for `formal_math_competition_repo_adapter`.
