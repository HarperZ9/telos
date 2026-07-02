# Pass 0145 Ledger - Multi-Institution Claim Graph

## Outputs

| Artifact | SHA-256 |
| --- | --- |
| schemas/multi-institution-claim-graph-pass-0145.json | A3A03D947E135657585A401010AD2EA7C7010CCFDC726157808E786CECEAF7A3 |
| packets/155-multi-institution-claim-graph.md | 8DE0E7A46EA788971C0916C6CAD7DE9E288A000107195D38C2F3E018F384EA11 |
| briefs/155-multi-institution-claim-graph-brief.md | A39B8B1889147EB823FFFA794F20A053276A375FB4E7FBF8643AA84FC33EAC3D |
| adversarial/pass-0145-multi-institution-claim-graph-steelman.md | 233F390276EAB32E76B04E36194975ED29E1B2D90AC96A806DC014AF5689AAE3 |
| crucible/pass-0145-thesis.json | E4AD238CB7684F776D5A0BAF7844AA9B815C0898F045DDFDADCB532F94A8B2C9 |
| crucible/pass-0145-measurements.json | D7B06987E7584B9C7E6201898492188112631DA35634CAD0B8372702283B4C78 |
| crucible/pass-0145-report.md | 1EBCE58995ABDC056B4C5EF68EBDF3142F2697B175581A6FDD2CF671134ECCD4 |
| crucible/pass-0145-run.json | 5FF537F2E536F220773234A5F8B7E4F4CE075B5279F2352E1A1000BD62710A74 |
| schemas/tool-receipts-pass-0145.json | AD6B5657994191DCDEDC474645B6615CADA86FEC528888A32A3FA2A081D63510 |
| fixtures/pass-0145-multi-institution-claim-graph-plan.json | 6A0FD9BB29782242DFF8A7B69BB6ED7D455BAAAC58CB96D26F40FC14A51239C1 |
| tools/compose_multi_institution_claim_graph.py | ED3ADFEF1FC08501C5A05D2059EB29079A3D261CA7AD5AA9622C10FB08842088 |
| tools/multi_institution_claim_graph_render.py | D1BD3D6886C3A0EE0AFACDC45A6550EDF384845ADB1627E38959FEDE20E4A49A |
| tools/test_multi_institution_claim_graph.py | C9AB159B3C167266AEC50EA7A35A49D662E451115D66173F5D309AB86B481CFE |
| tools/validate_pass_0145_multi_institution_claim_graph.py | F0A197B219E976A372E123EBFC9CCFDD69C9837B998FE40518D669E430D955E4 |

## Result Snapshot

| Field | Value |
| --- | --- |
| Schema | `MultiInstitutionClaimGraphReceipt/v1` |
| Status | `MULTI_INSTITUTION_CLAIM_GRAPH_MATCH_WITH_WARNINGS` |
| Seal | `ce64d5e9acfe20e097ca18a42d30cc8076cacfe07890282fe00bf8b74fa0308a` |
| Institutions | `4` |
| Stored captures | `18` |
| Identity matches | `4` |
| Repository matches | `4` |
| Crossref matches | `3` |
| Warnings | `3` |
| Promoted theorems | `0` |

## Live Source Surface

| Surface | Result |
| --- | --- |
| MIT | ROR/OpenAlex identity, DSpace OAI-PMH `Identify`, and Crossref affiliation sample all matched. |
| Harvard | ROR/OpenAlex identity, DASH OAI-PMH `Identify`, and Crossref affiliation sample all matched. |
| Cornell | ROR/OpenAlex identity and eCommons OAI-PMH `Identify` matched; Crossref stayed `SOURCE_LEAD_ONLY` after HTTP 429. |
| Caltech | ROR/OpenAlex identity, current CaltechAUTHORS `/oai2d` `Identify`, and Crossref affiliation sample matched; old/current endpoint documentation drift stayed a warning. |

## Tool Verification

| Tool | Result |
| --- | --- |
| Gather | MCP `gather.docs` verified packet 155, brief 155, and this ledger; `gather corpus verify` returned `MATCH` for all 18 stored source captures. |
| Index | MCP `index.context-envelope` with root-only selector returned `verification_verdict=MATCH`; a prior free-form focus string returned `unknown focus repo`, recorded as an interface sharp edge. |
| Forum | `forum route` escalated with no decided lane, confidence `0.4`, and top candidate `deep-research`; institution graph adapters still need dedicated routing vocabulary. |
| Telos | MCP catalog and `node demo/catalog.mjs --summary` reported 65 total and 65 available tools; `node demo/flagship-workflow.mjs` returned `MATCH`. |
| Crucible | `crucible run` assessed 5 claims with 5 `MATCH`, 0 `DRIFT`, and 0 `UNVERIFIABLE`, writing report and run JSON. |

## Crucible

| Field | Value |
| --- | --- |
| Thesis id | `c5ad4c7e77908b5a` |
| Thesis seal | `c5ad4c7e77908b5ad5b6784065d686b71ed35959838d7a67c66e750d324ece56` |
| Claims | `5` |
| MATCH | `5` |
| DRIFT | `0` |
| UNVERIFIABLE | `0` |
| Verdict seal | `844a0499328ae99faa52e3db64db0c2629b746459c0dd1a45b3b5a695adcc461` |
| Measurement seal | `c48b6f181ed4f5c72c0f2835120c288e67ed3b8b01c3b766b659623694c45e6a` |
| Assessment seal | `5098df53e2523212971e003b109ee8ebb84dfafdcdd9018bf9dd9e24d8bd7fbb` |

## Next Implementation Targets

| Target | Purpose |
| --- | --- |
| `institution_adapter_retry_policy` | Turn HTTP 429, stale endpoint, and selector-contract warnings into typed retry/backoff/fallback receipts. |
| `institution_queue_expansion` | Replay the same graph over non-US, multilingual, and less API-friendly institutions before promoting registry-scale claims. |
| `Forum route vocabulary repair` | Add a lane for institution graph adapters and registry-scale research substrate intake. |
