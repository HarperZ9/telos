# Pass 0148 Ledger - Live Source Router Probes

## Outputs

| Artifact | SHA-256 |
| --- | --- |
| schemas/live-source-router-probes-pass-0148.json | FD00A23E76ABF0942739ED80930233386E7D4EF304EE67DF76732CF3240BD372 |
| packets/158-live-source-router-probes.md | 29F0138DCE2E2EBBB2B6CC1ABF9F5136C3C5A94801834D2A732B314016800418 |
| briefs/158-live-source-router-probes-brief.md | 4B2968CAFC93B3A3EDDEA333E70F0CB8962795299D58097B27DB6380AAA0D7CB |
| adversarial/pass-0148-live-source-router-probes-steelman.md | 2920C8E082FF05FA159CF9F0C1132C7D0913865881CE27C9CB40B44C11AB81A0 |
| crucible/pass-0148-thesis.json | 55253C23C5B53D429379DE76EE30E985B3B403B3DE190A0CA7B68B71DCBE2724 |
| crucible/pass-0148-measurements.json | E8E1F3DC4155CD8A0EB477088F8B2E5AB93B01BFF33F4E2C02403C84DDEC692A |
| crucible/pass-0148-report.md | 96A9AB96D60573DC01826F1F52153CF07E1E759A2A6783C6554D16E3D2A39EDD |
| crucible/pass-0148-run.json | 0617533FDF6A24CECE52F9B0D8B416363ECB9A0557F0916B98C61FC64CA4B852 |
| schemas/tool-receipts-pass-0148.json | A0E472FE469C7394C49D5EDBEF18966C4F18987D69CB1BDD1089B09D4B4310C0 |
| fixtures/pass-0148-live-source-router-probes-plan.json | BA1937B1BCB3936960C867C9A36311362667FB9A1CCF5818CCE38340F3EDB851 |
| tools/compose_live_source_router_probes.py | E6B57CC380EB76A61B7F1427480BB14658B3F7038A793AC760D15E4BA9FA17AE |
| tools/test_live_source_router_probes.py | F5392F7F03210454F39E3EA3970A349BC30EDF32B0FEB3706B297F62ED6A0AD7 |
| tools/validate_pass_0148_live_source_router_probes.py | 67CBE1057D2B4EF50EFBFFDB01225FD60DF6F7F158972A20CA8138903B3E1E76 |

## Result Snapshot

| Field | Value |
| --- | --- |
| Schema | `LiveSourceRouterProbeReceipt/v1` |
| Status | `LIVE_SOURCE_ROUTER_PROBES_MATCH_WITH_WARNINGS` |
| Seal | `6fa211ccd91517425f8a33ce9f32fd396dff00067ccbf1e13a328d25b8770944` |
| Routes | `25` |
| Families | `7` |
| Live query matches | `18` |
| Fallback matches | `5` |
| Source-lead-only warnings | `2` |
| Promoted theorems | `0` |

## Source Router Surface

| Surface | Result |
| --- | --- |
| Preprint and archive routes | arXiv, bioRxiv, medRxiv, OSF, and HAL produced live or fallback route receipts; ChemRxiv remained `SOURCE_LEAD_ONLY_WARNING` because the public API/home/policy probes returned 403 from this environment. |
| Scholarly graph routes | Crossref, DataCite, OpenAIRE, Europe PMC, PubMed, and DOAJ produced live metadata samples; OpenAlex returned a retryable 503 and Semantic Scholar returned a retryable 429, both preserved as fallback-doc warnings. |
| Repository directories | re3data docs/search matched live; OpenDOAR stayed source-lead-only because local TLS negotiation failed; BASE OAI was captured through docs because the OAI endpoint is IP-restricted. |
| College and data repositories | MIT DSpace, Harvard DASH, Oxford ORA, Southampton ePrints, Harvard Dataverse, and Zenodo produced route receipts; Cambridge Apollo required endpoint-alias work after the guessed OAI endpoint returned 404 and the homepage fallback matched. |
| Promotion boundary | Live route success is only adapter evidence. This pass does not promote publication truth, full-text access, theorem progress, experimental truth, source completeness, or natural-law discovery. |

## Tool Verification

| Tool | Result |
| --- | --- |
| Gather | `gather corpus verify docs/research/dogfood/gather/pass-0148-live-source-router-probes --json` returned `MATCH` for all 30 captured source bodies during the pass, and the schema records 28 unique source refs. |
| Index | `index context-envelope --root . --budget 1400 --json` returned schema `project-telos.context-envelope/v1`, `verification_verdict=MATCH`, and graph pack SHA-256 `8ee383e19ae9a6141bee70de733fb6aa09201ff9d284ce6778ce58b06e6b68b2`. |
| Forum | `forum route` on the pass-0148 source-router prompt returned no decided lane, confidence `0.018181818181818188`, and `needs_escalation=true`; this is retained as evidence for a dedicated source-adapter/source-router lane. |
| Telos | `node demo/catalog.mjs --summary` reported 65 total and 65 available tools; `node demo/flagship-workflow.mjs` returned `status=MATCH` with `tool_version=0.1.0`. |
| Crucible | `crucible run` with the dogfood registry assessed 5 claims with 5 `MATCH`, 0 `DRIFT`, and 0 `UNVERIFIABLE`, writing report and run JSON. |

## Crucible

| Field | Value |
| --- | --- |
| Thesis id | `749dd0c505fa484d` |
| Thesis seal | `749dd0c505fa484da8e095952a10320760ea30818384718c152605ca7bced29d` |
| Claims | `5` |
| MATCH | `5` |
| DRIFT | `0` |
| UNVERIFIABLE | `0` |
| Verdict seal | `0e6f3e35a8a215158939bb02ed0538880dc12352f5217e927a786b1eb01a6cc1` |
| Measurement seal | `2fa51b67ac0c7bff7f7e73e7c71f3520a846c23f4262838156940f23d1dba7e7` |
| Assessment seal | `785a731aa7f15fcd56030925c1927c67c84db1394a9cfc5f070eb59d963442d2` |

## Next Implementation Targets

| Target | Purpose |
| --- | --- |
| `LiveSourceRouterProbeRunner` | Convert this pass from fixture replay into a reusable runner that emits one route receipt per endpoint attempt. |
| `EndpointAliasRegistry` | Learn alternate OAI/API endpoints for Cambridge, HAL scheme fallback, and stale institutional repository paths without converting drift into absence. |
| `SourceFamilyScheduler` | Schedule retries and backoff for 429/503/403/TLS/404 statuses with policy-specific gates and source-family budgets. |
| `ClaimExtractionGate` | Convert sampled records into claim cards only when source body, metadata, verifier, negative control, and replay path are present. |
| `Forum source-router lane` | Add routing vocabulary so registry/source-adapter work does not fall into low-confidence backend escalation. |
