# Pass 0150 Ledger - Mixed-Source Protein Proof Packet

## Outputs

| Artifact | SHA-256 |
| --- | --- |
| schemas/mixed-source-protein-proof-packet-pass-0150.json | 64EFC7BF0A193BCA046C7B3F44D25EA17214DC9B377DF5AF0C87FA5AAD5FBC6D |
| packets/160-mixed-source-protein-proof-packet.md | 41D171549F2C6A3477A0F3041036E38E24CA357395701F071B3FF61519F7F3A2 |
| briefs/160-mixed-source-protein-proof-packet-brief.md | 6DD4141E7C669BA81DC03D667805DA263075C42FB4A45BC64BB5395C5B2421CE |
| adversarial/pass-0150-mixed-source-protein-proof-packet-steelman.md | 57D75B8C33258EDDC5E54EA5F026E735F45E4056DF749DA97B944E7A721A3CD1 |
| crucible/pass-0150-thesis.json | 1B7F1A23C3BE503B95358B6EC920419F302C511E17982B62D21B0598DCD8555C |
| crucible/pass-0150-measurements.json | 3AC4596665689E48C704524EDC5EE9A37516828AB542903A4CE327668340A6AA |
| crucible/pass-0150-report.md | E056010656276F498F6B3166B80696C8F5187C5D6754A4ABA226B59282C721A2 |
| crucible/pass-0150-run.json | 88B7A42698F02ECAAF7EC04EEB821672BF161E6E809E493F4F3962C0A8679975 |
| schemas/tool-receipts-pass-0150.json | 39D3A3A9D54CBBBF031987D9E50BBD999576AE720726720B9259C7D86A30CC66 |
| schemas/index-context-envelope-pass-0150.json | E13720C76BF211969E395C619B26B2211E6FD9D17C1BDF0442CE543122D9E372 |
| forum-ledger/pass-0150-route.json | 6AFCFB1B4E4831EECA47EDE70FC8585401883891633D77DFBB0CC68137E79D6D |
| fixtures/pass-0150-mixed-source-protein-proof-packet-plan.json | C3FC5EE983DA7CEB0E42A52F1201CA8C7A1EF3553A9F164A053A7FEFE8C06C3B |
| tools/compose_mixed_source_protein_proof_packet.py | 30CD97522C2D8C678ED45B0D5D70A9525E5B058D970DF226AD0BEA7D9F4D279F |
| tools/test_mixed_source_protein_proof_packet.py | 830A886BC9731C20EA7CE14B88621839D6EAA639728BB39362EAA1D69BA99CAF |
| tools/validate_pass_0150_mixed_source_protein_proof_packet.py | 353428980CC7CAAB9AD430FF21262C0F711FB094F59C04C82BF2DCFEBCE8AB4D |

## Result Snapshot

| Field | Value |
| --- | --- |
| Schema | `MixedSourceProteinProofPacket/v1` |
| Status | `MIXED_SOURCE_PROTEIN_PROOF_PACKET_MATCH_WITH_WARNINGS` |
| Seal | `fce6663f6526c3436bcdca6be66b7f18ce4098e03d8b900f88a12c7d445e92f4` |
| Sources | `5` |
| Gather verified | `5` |
| Checks matched | `7/7` |
| Sequence length | `142` |
| RCSB mature-chain length | `141` |
| Warnings | `3` |

## Boundary

Pass 0150 proves only a mixed-source protein identity and sequence-consistency packet for one bounded public record. It does not prove biological function, clinical relevance, wet-lab result validity, protein design success, literature completeness, or discovery.

## Source Receipts

| Source | Capture status |
| --- | --- |
| https://rest.uniprot.org/uniprotkb/P69905.json | Gather `MATCH` |
| https://alphafold.ebi.ac.uk/api/prediction/P69905 | Gather `MATCH` |
| https://data.rcsb.org/rest/v1/core/polymer_entity/1A3N/1 | Gather `MATCH` |
| https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:6244294&format=json&pageSize=1 | Gather `MATCH` |
| https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id=6244294&retmode=json | Gather `MATCH` |

## Tool Verification

| Tool | Result |
| --- | --- |
| Gather | `gather corpus verify docs/research/dogfood/gather/pass-0150-mixed-source-protein-proof-packet --json` returned `MATCH` for all 5 stored source bodies. |
| Index | `index context-envelope --root . --budget 1400 --json` returned `verification_verdict=MATCH`, graph pack `8ee383e19ae9a6141bee70de733fb6aa09201ff9d284ce6778ce58b06e6b68b2`, and freshness root `2a669207002db34dc10e72a26f2a33511f7d11f7b23e841e4dea1fe722b580f5`. |
| Forum | `forum route` split between `deep-research` and `project-telos`; `decided=null`, confidence `0.018181818181818188`, and `needs_escalation=true`. This is a useful product signal: mixed-source science packets span research and Telos infrastructure. |
| Crucible | `crucible run` returned 6 `MATCH`, 0 `DRIFT`, 0 `UNVERIFIABLE`, thesis id `db6e9d587b1ef3bd`, assessment seal `fa70c099e59c7fecf86f6dce85aa3f98fe4d6094352c217fc1ecc5dcd06b8b36`. |
| Telos | `node demo/catalog.mjs --summary` reported 65/65 tools available; `node demo/flagship-workflow.mjs` returned `status=MATCH`. |

## Product Finding

This pass turns the pass-0149 `protein_design_lab` queue into an actual replay lane: Gather stores source bodies, the runner recomputes source joins and sequence boundaries, Crucible evaluates falsifiable claims, Index preserves workspace context, Forum exposes routing ambiguity, and Telos demonstrates catalog availability. The immediate megatool improvement is a field-aware claim admission gate that separates identifier match, canonical sequence, mature experimental chain, predicted structure, literature metadata, wet-lab assay, clinical claim, and design success before any model can promote a biological conclusion.
