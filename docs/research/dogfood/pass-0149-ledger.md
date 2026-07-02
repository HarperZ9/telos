# Pass 0149 Ledger - Cross-Domain Substrate Expansion

## Outputs

| Artifact | SHA-256 |
| --- | --- |
| schemas/cross-domain-substrate-expansion-pass-0149.json | E1A14585731760A2A413A8E22BB5FA300CDF23F4C1CF042DFEA273D16387BAE8 |
| packets/159-cross-domain-substrate-expansion.md | 3A65A37C603F9127C673F859E551050322CBF9569E4C608C2ABD51DE7D003358 |
| briefs/159-cross-domain-substrate-expansion-brief.md | 2632864683A777846A1190D7142F32E16038B6DD565FC550621EB7F0E2209A7E |
| adversarial/pass-0149-cross-domain-substrate-expansion-steelman.md | 490BE0A80636AF55CB9CBF5213E6372B62E149AD8363D81EB092233CF0D29B42 |
| crucible/pass-0149-thesis.json | 8FB280F2FC587218799B5A4AE79E660C69B270A49CC57D16805F91B0AC4C4277 |
| crucible/pass-0149-measurements.json | A8A8ED9A9143B5C4C75EEF10093A430E58BF67478ACB0ACAE5BD298FF139754A |
| crucible/pass-0149-report.md | AC65FBDFF36D3B9F43BBAFA07078226B207F7B614EEB98C0699DA2192F1214FE |
| crucible/pass-0149-run.json | 4E1A754F6957CEE2D3025C6A8277656031D178F3239238CEFF6F6FC132761769 |
| schemas/tool-receipts-pass-0149.json | F4194F431C68CBBCCA64D2529687B1EB19830A75F460770222F4B34DE28DB53F |
| fixtures/pass-0149-cross-domain-substrate-expansion-plan.json | 3FCEFEF998A8F3F58FFE920634DCF5E3B0D728B17519960140709549027E5EB2 |
| tools/compose_cross_domain_substrate_expansion.py | 6F3AD4DF71BE2E73817DED132707B46E4F394BDBE5389F4EE851F56376D5BFA6 |
| tools/test_cross_domain_substrate_expansion.py | 76E5AC20715F63100525B6403FED46E0C15878045F26063B2D55CF4EC79BB86D |
| tools/validate_pass_0149_cross_domain_substrate_expansion.py | 82FE3D871BEF5E0052CB365FD498CBF7EACECCE16AAD0D2E4B30EB6EFD0E1237 |

## Result Snapshot

| Field | Value |
| --- | --- |
| Schema | `CrossDomainSubstrateExpansionReceipt/v1` |
| Status | `CROSS_DOMAIN_SUBSTRATE_EXPANSION_MATCH_WITH_WARNINGS` |
| Seal | `b1ba4174d2ad293a85924d9cf1536033c60c9d8b549dec3f7d2d3ee8c7235dde` |
| Candidate substrates | `131` |
| Source families | `16` |
| Domains | `49` |
| Capture attempts | `39` |
| Gather verified | `25` |
| Capture warnings | `14` |
| Workbenches | `12` |
| Promoted theorems | `0` |

## Source Expansion Surface

| Surface | Result |
| --- | --- |
| Breadth | The pass queues 131 candidate substrates across 16 source families and 49 domain labels, including publishing graphs, preprint presses, college repositories, repository protocols, biomedical and clinical databases, climate/earth systems, materials/chemistry, physics/astronomy, AI/ML benchmarks, formal-math libraries, economics/policy, patents/legal, general data repositories, and software archives. |
| Current captures | 39 official-source capture attempts produced 25 non-empty `GATHER_VERIFIED` captures, plus 14 warning states covering empty captures, scope drops, HTTP/platform warnings, and PDF fetch warnings. |
| Scheduler policy | `open_http`, `key_required`, `rate_limited`, `restricted_or_registered`, `endpoint_alias_needed`, `source_lead_only`, and `empty_capture` are explicit adapter policies; none are promoted to source truth by themselves. |
| Workbench queue | 12 workbenches define first experiments for formal theorem work, biomedical mechanisms, protein design, materials discovery, climate resilience, robotics world models, economics policy, prior art, college knowledge graphs, AI benchmark receipts, software supply, and cross-family world-problem routing. |
| Promotion boundary | This is a substrate scheduler and source map. It does not prove complete archive coverage, endpoint availability for uncaptured leads, source correctness, full-text access, experimental truth, theorem progress, or natural-law discovery. |

## Tool Verification

| Tool | Result |
| --- | --- |
| Gather | `gather corpus verify docs/research/dogfood/gather/pass-0149-cross-domain-substrate-expansion --json` returned `MATCH` for all 29 stored source bodies; the pass artifact distinguishes non-empty captures from empty and missing capture attempts. |
| Index | `index context-envelope --root . --budget 1400 --json` returned schema `project-telos.context-envelope/v1`, `verification_verdict=MATCH`, graph pack SHA-256 `8ee383e19ae9a6141bee70de733fb6aa09201ff9d284ce6778ce58b06e6b68b2`, and workspace root SHA-256 `7f976523b958831edd79f112f8f62f796eb8f26b8fabd1285372f468ca272fe6`. |
| Forum | `forum route` on the pass-0149 substrate scheduler prompt decided `project-telos`, confidence `0.5`, and `needs_escalation=false`; the richer tool/source vocabulary improved routing compared with pass 0148. |
| Telos | `node demo/catalog.mjs --summary` reported 65 total and 65 available tools; `node demo/flagship-workflow.mjs` returned `status=MATCH` with `tool_version=0.1.0`. |
| Crucible | `crucible run` with the dogfood registry assessed 6 claims with 6 `MATCH`, 0 `DRIFT`, and 0 `UNVERIFIABLE`, writing report and run JSON. |

## Crucible

| Field | Value |
| --- | --- |
| Thesis id | `08d55f66281ea1a2` |
| Thesis seal | `08d55f66281ea1a263f85198c24a1b636fcfb87d7bf648686c1d73dcb41964d1` |
| Claims | `6` |
| MATCH | `6` |
| DRIFT | `0` |
| UNVERIFIABLE | `0` |
| Verdict seal | `2c5aeffc650e3650ef8e3d1171a0e9c14e70c877f8cddbd864217ac0dc6926b0` |
| Measurement seal | `99e1f7600b1cc6010f107587b4b9d93ae8b1f8b7388ab047171bbbcc917101d8` |
| Assessment seal | `7c94ce63464bd8cb1c6d6a22dc9c74bc62f9277a224d8721bdeae2813fde7e97` |

## Next Implementation Targets

| Target | Purpose |
| --- | --- |
| `MixedSourceProofPacketRunner` | Select one workbench and join paper/preprint, dataset, code, domain database, institutional source, verifier, negative control, and replay receipt. |
| `SubstrateScheduler` | Turn the 131 candidate rows into retryable, policy-aware route jobs with budgets, admission gates, and source-family quotas. |
| `AdapterPolicyCompiler` | Compile `key_required`, `rate_limited`, `endpoint_alias_needed`, and `empty_capture` into executable Gather/Index/Forum routing policy. |
| `ClaimExtractionGate` | Reject any claim card missing body or metadata source, field-specific verifier, negative fixture, and replay path. |
| `WorkbenchScorecard` | Rank the 12 domain workbenches by proof-demo readiness, societal upside, compute feasibility, and source availability. |
