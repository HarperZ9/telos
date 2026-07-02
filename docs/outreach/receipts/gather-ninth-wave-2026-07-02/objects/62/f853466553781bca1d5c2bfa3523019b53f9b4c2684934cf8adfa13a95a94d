# Pass 0150 - Mixed-Source Protein Proof Packet

Status: `MIXED_SOURCE_PROTEIN_PROOF_PACKET_MATCH_WITH_WARNINGS` with seal `fce6663f6526c3436bcdca6be66b7f18ce4098e03d8b900f88a12c7d445e92f4`.

## Bounded Claim

For UniProt accession `P69905`, this packet verifies that gathered UniProt, AlphaFold DB, RCSB PDB, Europe PMC, and PubMed records join on the same protein identity or cited PubMed identifier, and that local sequence checks reproduce the expected canonical and mature-chain relationships.

## Evidence Snapshot

| Source | Status | SHA-256 |
| --- | --- | --- |
| uniprot_record | `MATCH` | `a9de50570a2c69e3b5593c82e290c31403682bcdecb19ba04e5632ac8771601a` |
| alphafold_prediction | `MATCH` | `af907bb73c411790ac6a24764314287e5cd331c0ed5b13eae9924ce45b27d8f9` |
| rcsb_polymer_entity | `MATCH` | `4f3aacd17cc3affa3d9f9a33f505ea4b1e8015d294f00e84c5e8f68c64f6e7db` |
| europepmc_pubmed_join | `MATCH` | `00420415d04d7b7436bbfb24bb476690189f4c09300cd4238575e4e601bfc7fb` |
| pubmed_summary | `MATCH` | `cac675eed618c24d758e401e2f8085f04d3cbaec2c723233645ac44db6c13733` |

## Computation Receipt

- UniProt/AlphaFold sequence length: `142`
- RCSB mature-chain length: `141`
- Sequence SHA-256: `14725a10598943a7aa719eed7d24c7fee599192a6c63c75b051ee6f156341242`
- AlphaFold latest version: `6`
- RCSB reference sequence coverage: `0.9929577464788732`

## Verification Checks

- `MATCH` all_sources_gather_verified: sources=5
- `MATCH` uniprot_primary_accession_match: P69905
- `MATCH` alphafold_accession_and_sequence_match: len=142
- `MATCH` rcsb_uniprot_cross_reference_match: {'database_accession': 'P69905', 'database_name': 'UniProt', 'entity_sequence_coverage': 1.0, 'provenance_source': 'SIFTS', 'reference_sequence_coverage': 0.9929577464788732}
- `MATCH` rcsb_mature_chain_matches_uniprot_positions_2_142: rcsb_len=141;uniprot_len=142
- `MATCH` literature_identifier_join_match: Nucleotide sequence of the coding portion of human alpha globin messenger RNA.
- `MATCH` no_design_or_clinical_claim_promotion: boundary only; no promoted design, assay, or clinical claim

## Warnings

- gather_api_required_GATHER_API_TOKEN_for_public_api_lane; gather_web captured public bodies instead
- rcsb_polymer_entity_matches_mature_chain_not_full_142_residue_canonical_sequence
- literature_metadata_join_is_not_a_literature_review_or_functional_assay

## Boundary

Pass 0150 proves only a mixed-source protein identity and sequence-consistency packet for one bounded public record. It does not prove biological function, clinical relevance, wet-lab result validity, protein design success, literature completeness, or discovery.
