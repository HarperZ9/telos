# Pass 0143 Ledger - Registry Adapter Contracts

## Outputs

| Artifact | SHA-256 |
| --- | --- |
| schemas/registry-adapter-contracts-pass-0143.json | B62E35BBD10B4CD080242608068018CD9A1DF2D60355BBA15A00A42D54BC9B8D |
| packets/153-registry-adapter-contracts.md | E902C271898DAA4F264168FCCD5C4D486701DDA9F2325E1FB96D0E1EF6E2936A |
| briefs/153-registry-adapter-contracts-brief.md | ADDC4D8F5D6BD588125C30FD1E33098B9ABD6AF17601848AAD97C5178E7AE925 |
| adversarial/pass-0143-registry-adapter-contracts-steelman.md | 17C92EFC6916BF03F500EFFC37C16BFF7E2D18CB32195ED8B7EA1A65E0AAD533 |
| crucible/pass-0143-thesis.json | 7AAEDC2AB3F5B841168B718FF536C025B32C1D50FB4F2741411CE0659F344A7B |
| crucible/pass-0143-measurements.json | 7BE3C2A36D8E030BDB8B3B08759C443085452E9C9B472083E0517C7657759797 |
| schemas/tool-receipts-pass-0143.json | 7B5252DC9CBA5CBA6B37D872911E7CB9A1B17ADD0B8D4DFB89373A674CDCE109 |
| fixtures/pass-0143-adapter-contract-fixtures.json | CFD82B56841318B84BD02D67E8E5B45D1F79857E335653DD53F87126F97C832C |
| tools/compose_registry_adapter_contracts.py | 994E6FF5939D9B652A5CD31C81ABE191ED96904E7B2E32998DF8AD38356C3692 |
| tools/test_registry_adapter_contracts.py | A04C383F7D89A1415FC7AE624207F56355ED92C50FB31494CA8ABC5B3488483E |
| tools/validate_pass_0143_registry_adapter_contracts.py | E0A5FB8E8699AAD6B1BA3B652E8D3C6136D9FDAF53460C70A95DC4322C9099D2 |
| crucible/pass-0143-report.md | 285B8272828B2BCFF6E543579CE966339986A309DB1288EB1981D3B4EF388AFF |
| crucible/pass-0143-run.json | CFB29B3BF87358C0E9B87BD03C03A1FB53906D7F1D449D9EE26D0C326B95FB64 |

## Result Snapshot

| Field | Value |
| --- | --- |
| Schema | `RegistryAdapterContractsReceipt/v1` |
| Status | `REGISTRY_ADAPTER_CONTRACTS_MATCH` |
| Seal | `6d0ad15f379bb9bc4f971b1ec0c564a112e2fd9f80ad523fb88dac54905da88b` |
| Contracts | `2` |
| Repository fixtures | `6` |
| Scholarly fixtures | `8` |
| Join keys | `15` |
| Negative fixtures | `10` |
| Tool floor mismatches | `0` |
| Promoted theorems | `0` |

## Tool Verification

| Tool | Result |
| --- | --- |
| Gather | `gather docs` verified packet 153 and brief 153. |
| Index | `index context-envelope --root . --budget 1200 --json` returned `verification_verdict=MATCH`. |
| Forum | `forum route` escalated with no decided lane and top candidate `project-telos` at confidence `0.045454545454545456`; this is a route vocabulary gap for registry adapter contracts. |
| Telos | `node demo/catalog.mjs --summary` reported 65 total and 65 available MCP tools, including 37 Telos tools. |
| Crucible | `crucible run` assessed 6 claims with 6 MATCH, 0 DRIFT, and 0 UNVERIFIABLE. |

## Crucible

| Field | Value |
| --- | --- |
| Thesis id | `c6c79e6bab8b0290` |
| Thesis seal | `c6c79e6bab8b0290b6982201d5aed8a1e1e1e985225f8f3f44ea538ab507a483` |
| Claims | `6` |
| MATCH | `6` |
| DRIFT | `0` |
| UNVERIFIABLE | `0` |
| Verdict seal | `991916e692f09eaaa01830cb2d16e86ea01e9fe86aaf2c7604ad069d39c8f20b` |
| Measurement seal | `f8b140beff79a3ee77544ac57ddbef134777a527b8a983bc7b40aad8ddf70166` |
| Assessment seal | `ad707fff5a92284a4a1022ddf68a4fb8a36ef61dba1a35b940dc2432b318510e` |

## Next Implementation Targets

| Target | Purpose |
| --- | --- |
| `one_institution_claim_graph` | Run a bounded live graph that joins ROR identity, repository directory evidence, endpoint candidate, scholarly work metadata, dataset relation, license state, and verifier verdict. |
| `Forum route vocabulary repair` | Add a native route or prompt bridge for registry adapter contracts so source-intake work no longer escalates as generic Project Telos work. |
