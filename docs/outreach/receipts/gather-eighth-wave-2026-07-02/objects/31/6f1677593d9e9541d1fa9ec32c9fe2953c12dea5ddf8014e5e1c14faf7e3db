# Pass 0146 Ledger - Adapter Retry Policy

## Outputs

| Artifact | SHA-256 |
| --- | --- |
| schemas/adapter-retry-policy-pass-0146.json | E49B644331562292FA51F4F7F1EF7CA6F179E4BF964EC0E790803AF533C5DACE |
| packets/156-adapter-retry-policy.md | 7B801F05EF64FEDD7753CCB50BC25D9E17617D07EFBBA85030B717208C28A15D |
| briefs/156-adapter-retry-policy-brief.md | 5D7918D87B91D575AF63B8FE49875DEB8E728EF010282A5DA48A8049C16184DF |
| adversarial/pass-0146-adapter-retry-policy-steelman.md | 030CC3C2142CF54EFF78D24CD873AEDA40DD80D5E2097AF9DE4F42AF5ACF0298 |
| crucible/pass-0146-thesis.json | 679A0AA5513ABF9545863431975226172940A1BD6372B0EDF617DBA4B545E507 |
| crucible/pass-0146-measurements.json | 1EFFC44F520E37345B32B77EABB61F66E97912F3E1F22EE5654FC5F48DBF5C64 |
| crucible/pass-0146-report.md | 790CA77791DC8C8F0C518CD9D93880B258E1030619B5D72AA05C09B3ACA5164F |
| crucible/pass-0146-run.json | 24FC05BD24A6B88F233184803518F250AE156025326360F6771485E5AD4FD496 |
| schemas/tool-receipts-pass-0146.json | 200BDB99335AD5E1EBBFC239A092E5C1D848D79CFC3DECA93DCCC483D789BE82 |
| fixtures/pass-0146-adapter-retry-policy-plan.json | 4CD08CB0267A3852DB6EDF6C9CD1FCD8259714839F5152AA2500123EB94DF1A7 |
| tools/compose_adapter_retry_policy.py | 9D80A5FE47855565FD33EDC7A362EBDF0DDAE98A413A7DFBE4C86BF8A89DB50F |
| tools/test_adapter_retry_policy.py | 6D7B46C36243B02800F7012C39915F40F5011E6608B1D9D10AC8B78A31619667 |
| tools/validate_pass_0146_adapter_retry_policy.py | 66CB7D9C07F2E731E20BEF6050610AAC82C463C676B7287E2775597123373B03 |

## Result Snapshot

| Field | Value |
| --- | --- |
| Schema | `AdapterRetryPolicyReceipt/v1` |
| Status | `ADAPTER_RETRY_POLICY_MATCH` |
| Seal | `8a20aae5a90e77621ecb7498d90665b17e53393b33109768e92eab17feaea4a5` |
| Policy sources | `11` |
| Source systems | `6` |
| Policy rules | `12` |
| Scenario fixtures | `10` |
| Negative fixtures | `10` |
| Promoted theorems | `0` |

## Source Policy Surface

| Source family | Result |
| --- | --- |
| Crossref | Captured access/authentication, tips, and December 2025 rate-limit change docs; 429 becomes retryable source-lead evidence, 403 becomes access escalation. |
| OpenAlex | Captured authentication, error, and deprecation docs; mailto-only polite-pool logic is rejected as stale, API-key/backoff policy is recorded. |
| ROR | Captured REST API docs; current and upcoming client-id rate-limit behavior and local Docker fallback are recorded. |
| OAI-PMH | Captured protocol and harvester guidelines; 503 `Retry-After`, headerless 503, and resumption-token checkpoint behavior are recorded. |
| HTTP | Captured RFC 6585 and RFC 9110 anchors for 429 and `Retry-After` parsing. |
| Index | Pass 0145 selector failure is carried forward as `INDEX_SELECTOR_ROOT_FALLBACK`. |

## Tool Verification

| Tool | Result |
| --- | --- |
| Gather | `gather corpus verify` returned `MATCH` for all 11 source-policy captures; MCP `gather.docs` verified packet 156, brief 156, and this ledger. |
| Index | MCP `index.context-envelope` returned `verification_verdict=MATCH`. |
| Forum | `forum route` escalated with no decided lane, confidence `0.2`, and top candidate `deep-research`; source-adapter retry policy still lacks a dedicated Forum route. |
| Telos | `node demo/catalog.mjs --summary` reported 65 total and 65 available tools; `node demo/flagship-workflow.mjs` returned `MATCH`. |
| Crucible | `crucible run` assessed 5 claims with 5 `MATCH`, 0 `DRIFT`, and 0 `UNVERIFIABLE`, writing report and run JSON. |

## Crucible

| Field | Value |
| --- | --- |
| Thesis id | `cf876c6097fcee75` |
| Thesis seal | `cf876c6097fcee75a15f226f2467f59f8433f063dfa15bbde0a11f63654a11f5` |
| Claims | `5` |
| MATCH | `5` |
| DRIFT | `0` |
| UNVERIFIABLE | `0` |
| Verdict seal | `d168e3702e58ad2ee60adf6628d7e774120d0bb95dda8f65b6ee570483212a92` |
| Measurement seal | `87576070c6caa6264036eae19784ab28c5acf2e83125a6791517814ac46fb0f1` |
| Assessment seal | `3fe6ff933e7b3b0c3da7df341902dc1b27cf0441ce7decb163eaa0f7ee1f541b` |

## Next Implementation Targets

| Target | Purpose |
| --- | --- |
| `policy_aware_institution_queue` | Replay pass 0145 over non-US and less API-friendly institutions while writing retry, wait, fallback, and demotion receipts. |
| `SourceFamilyScheduler` | Turn these rules into a scheduler contract with token buckets, per-host concurrency, retry-after parsing, checkpoint restart, and source-family verdicts. |
| `Forum source-adapter lane` | Add routing vocabulary for registry-scale source adapters, retry policy, and research substrate intake. |
