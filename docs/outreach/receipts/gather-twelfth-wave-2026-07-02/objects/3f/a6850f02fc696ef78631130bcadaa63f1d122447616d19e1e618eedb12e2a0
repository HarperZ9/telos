# Pass 0147 Ledger - Policy-Aware Institution Queue

## Outputs

| Artifact | SHA-256 |
| --- | --- |
| schemas/policy-aware-institution-queue-pass-0147.json | F3D240371F77FE58A15581DB8DB1A8F217AC8E97DE7916E7DE79C27F9693AB15 |
| packets/157-policy-aware-institution-queue.md | 5F385AEE4AFE435B43A742924C053D3B64B4F11EF9A01D51D8D72CA216DF55D6 |
| briefs/157-policy-aware-institution-queue-brief.md | A2FD85EDC931EF91DA7541A956ACDE69056CF0D33450B4D8A34A4C4E3884B98B |
| adversarial/pass-0147-policy-aware-institution-queue-steelman.md | 643F5581CA3A4363E2DA1B6906B7438790D73A47E818DAFCD2AE461C5B3AF8BD |
| crucible/pass-0147-thesis.json | 280ADDF0A3F00065CF5B3741CE19E5E4F383F53E7464EF3CA47B5B25CE59A1DE |
| crucible/pass-0147-measurements.json | 5878C762E3BC8E756366308D38828B5A70D168B290C4E53C8277CD7F115C7E46 |
| crucible/pass-0147-report.md | A30D69E53F6641E6EF23EB9B6A8A8EC8236E6013308F24AAC625F71D485EAE8F |
| crucible/pass-0147-run.json | 876007BFB44B6E3F2145A34D9C38A0558CDD3742B2C31B1DAFF0B23DD272382C |
| schemas/tool-receipts-pass-0147.json | C6731326ED228989B518CEEE9EDFA32073C6A4964FE9151B26F522B68E9232A9 |
| fixtures/pass-0147-policy-aware-institution-queue-plan.json | 277CAE4A088D3E8102E531C6973F7EE561594174BEE5E2EB5714ABB3B291CCB1 |
| tools/compose_policy_aware_institution_queue.py | 51FE5926F6F91CCF47ABF4FF13F0CA166CF711E2E29368D640F905F71544B4B3 |
| tools/test_policy_aware_institution_queue.py | 5C86988D60A329C2DB4A70F21F0E189310CE6F125F4628A9B62CB4297D9A552E |
| tools/validate_pass_0147_policy_aware_institution_queue.py | D6C03A4C666D3EE02C854FD9AEEDB9DC5C755B6CFEA6B53520CEB9FDF7B9CFC2 |

## Result Snapshot

| Field | Value |
| --- | --- |
| Schema | `PolicyAwareInstitutionQueueReceipt/v1` |
| Status | `POLICY_AWARE_INSTITUTION_QUEUE_MATCH_WITH_WARNINGS` |
| Seal | `a03477888d31ffe286ec4ea38620342f4ab08480acf202412a590c8da10416f3` |
| Institutions | `4` |
| Source captures | `16` |
| Identity warnings | `1` |
| Repository warnings | `1` |
| Crossref samples | `4` |
| Promoted theorems | `0` |

## Source Policy Surface

| Surface | Result |
| --- | --- |
| ROR/OpenAlex identity | ETH Zurich, University of Cape Town, and Universidade de Sao Paulo joined cleanly; University of Tokyo required ranked identity resolution because the first ROR result was Tokyo University of Agriculture while OpenAlex joined to The University of Tokyo at ROR rank 2. |
| OAI-PMH repository leads | ETH Research Collection, UTokyo Repository, and OpenUCT produced Identify-style source leads; Universidade de Sao Paulo returned an OAI-PMH sample/provider page and remains `SOURCE_LEAD_ONLY_ENDPOINT_DRIFT`. |
| Crossref affiliation samples | All four Crossref calls returned sampled DOI and affiliation evidence; all remain `SAMPLED_METADATA_ONLY`, not publication truth or institutional coverage. |
| Adapter policy inheritance | Pass 0147 carries the pass 0146 policies for stale endpoints, retryable source leads, selector drift, and no absence promotion. |

## Tool Verification

| Tool | Result |
| --- | --- |
| Gather | `gather corpus verify` returned `MATCH` for all 16 source captures; MCP `gather.docs` verified packet 157, brief 157, and this ledger. |
| Index | MCP `index.context-envelope` rejected the specific focus selector, then root-only fallback returned `verification_verdict=MATCH`; selector drift is kept as interface evidence. |
| Forum | MCP `forum.route` escalated with no decided lane, confidence `0.0`, and weak backend/deep-research candidates; this supports adding a source-adapter lane. |
| Telos | `node demo/catalog.mjs --summary` reported 65 total and 65 available tools; `node demo/flagship-workflow.mjs` returned `MATCH`; MCP `telos.room` reported 5/5 tools ready. |
| Crucible | `crucible run` with the dogfood registry assessed 5 claims with 5 `MATCH`, 0 `DRIFT`, and 0 `UNVERIFIABLE`, writing report and run JSON. |

## Crucible

| Field | Value |
| --- | --- |
| Thesis id | `4e557391c4ce9cf3` |
| Thesis seal | `4e557391c4ce9cf38c9ce98c8d746fd11c42c9f96fdcf8a4b893ed7a7f8b21c7` |
| Claims | `5` |
| MATCH | `5` |
| DRIFT | `0` |
| UNVERIFIABLE | `0` |
| Verdict seal | `43ad628e6458f8e899b30956817e813c9e6c450f0b78c33204c1d51e2a6a6798` |
| Measurement seal | `da14d5aa82716467d2d66eff904c0861c8121c4a64dda37de17deb6063c8e863` |
| Assessment seal | `6e42b90ebf64dd64496131c2f8df42afd5fa4cfd5a099a1e775696984d951f2d` |

## Next Implementation Targets

| Target | Purpose |
| --- | --- |
| `PolicyAwareInstitutionQueueRunner` | Convert this replay fixture into a reusable queue runner with per-source status receipts. |
| `EndpointAliasRegistry` | Discover and preserve alternate OAI endpoints instead of demoting stale endpoint evidence to absence. |
| `MultilingualInstitutionNameResolver` | Resolve translated, accented, and abbreviated institution names before ROR/OpenAlex promotion. |
| `Forum source-adapter lane` | Route registry-scale source adapter tasks without low-confidence backend/deep-research escalation. |
