# Pass 0144 Ledger - One Institution Claim Graph

## Outputs

| Artifact | SHA-256 |
| --- | --- |
| schemas/one-institution-claim-graph-pass-0144.json | 42E1E1D34E550F158C27117CC89BB02DCB88F01F1A64657D4DD1442EE927102F |
| packets/154-one-institution-claim-graph.md | AABA1D61F312B6EB99B17AC8BDDA5E486A7C1B8095BF45B8411C393F86C49E4E |
| briefs/154-one-institution-claim-graph-brief.md | 430137D9EC23644FAE844F2001521202C79F7DA52792A62BD1532DD4CB61F686 |
| adversarial/pass-0144-one-institution-claim-graph-steelman.md | 5A123A3E52197DB32D1FB37142DBCF777F8A54AC4BA9A57F761B4387BB80683B |
| crucible/pass-0144-thesis.json | A2994C2C6050BF6A397D1D647993BAD95AAF0C4858FD7B5D52124D4C9E6EB1A7 |
| crucible/pass-0144-measurements.json | 1971C7DF3B53D9D5724B7A25563CD587ECFF210B5FC6F75D5F4038C23CADEF4D |
| schemas/tool-receipts-pass-0144.json | 0BCCE387154949F235DCB466063A359ABF4B8A324587F3B0F288439A322372B0 |
| fixtures/pass-0144-one-institution-claim-graph-plan.json | 16DE57D1321FED27BAAA43DED8B86C437358687FCE1CD62B98F4DF964851973E |
| tools/compose_one_institution_claim_graph.py | 09F00DCA058F151347192579F2D53336B5F1A0B3FFB5B970304CD4AD50804199 |
| tools/test_one_institution_claim_graph.py | 4FA41652F1E82339754F749C45DC310E24D15839FDFCC419C01EEB5D3AEDCB10 |
| tools/validate_pass_0144_one_institution_claim_graph.py | 9672A27D9A9BF66E10C4B3713B4C9A1F38EBA36895EB4FE34D703DF8BF090A8E |
| crucible/pass-0144-report.md | 07693F8CD9FB77968DD1D44652A051561D64FCF3A3E6500E032A09847888CC8C |
| crucible/pass-0144-run.json | D64A9803DBE6A77CECF41376E9204356A91BF44D45027CEA1CFDDAFA765DC09E |

## Result Snapshot

| Field | Value |
| --- | --- |
| Schema | `OneInstitutionClaimGraphReceipt/v1` |
| Status | `ONE_INSTITUTION_CLAIM_GRAPH_MATCH_WITH_WARNINGS` |
| Seal | `548a8fd61058c8dfd38765b7e9b61e2f382eacc6e759b6774f1d911efd8ac2eb` |
| Live captures | `6` |
| Protocol docs | `5` |
| Join verdicts | `5` |
| Negative fixtures | `10` |
| Promoted theorems | `0` |

## Live Source Surface

| Surface | Result |
| --- | --- |
| ROR | MIT resolved to `https://ror.org/042nb2s44`. |
| OpenAlex | MIT resolved to `https://openalex.org/I63966007` and carried the same ROR id. |
| MIT DSpace OAI-PMH | `Identify` and date-filtered `ListRecords` captures matched. |
| Crossref | Sample work metadata included author affiliation strings for Massachusetts Institute of Technology. |
| DataCite | Query records stayed `SOURCE_LEAD_ONLY`; sampled records did not prove explicit MIT dataset relation. |
| Semantic Scholar | Public request hit HTTP 429 and stayed a warning, not absence evidence. |

## Tool Verification

| Tool | Result |
| --- | --- |
| Gather | Stored 11 distinct web captures and verified packet 154 plus brief 154. |
| Index | `index context-envelope --root . --budget 1200 --json` returned `verification_verdict=MATCH`. |
| Forum | `forum route` escalated with no decided lane and confidence `0.0`; this reinforces the route vocabulary gap for institution graph adapters. |
| Telos | `node demo/catalog.mjs --summary` reported 65 total and 65 available MCP tools, including 37 Telos tools. |
| Crucible | `crucible run` assessed 5 claims with 5 MATCH, 0 DRIFT, and 0 UNVERIFIABLE. |

## Crucible

| Field | Value |
| --- | --- |
| Thesis id | `dc8dfef69a298991` |
| Thesis seal | `dc8dfef69a298991065cc21da60e2b926fd5f040ab2f8120b4702ecfe6d79351` |
| Claims | `5` |
| MATCH | `5` |
| DRIFT | `0` |
| UNVERIFIABLE | `0` |
| Verdict seal | `b915a47d250e4f153c93857efb97c26e333e6f31a870a5e7d739f40dc8bd773b` |
| Measurement seal | `a60ebf438a8f6209c62656445add98f4d7538b48742e96121cd131493e23fd64` |
| Assessment seal | `3b42465e6698a23835dc541995cad22b42244f4839fcfcfd10dade027dd220a4` |

## Next Implementation Targets

| Target | Purpose |
| --- | --- |
| `multi_institution_claim_graph_runner` | Replay the same graph contract across three to five institutions and compare identity, repository, work, dataset, warning, and negative-fixture behavior. |
| `Forum route vocabulary repair` | Add a route for institution graph adapters and registry-scale source intake so these runs no longer escalate as zero-confidence generic work. |
