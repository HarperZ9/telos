# crucible report: Dogfood Pass 0150 Mixed-Source Protein Proof Packet

## Summary

- thesis_id: `db6e9d587b1ef3bd`
- thesis_seal: `db6e9d587b1ef3bd94a185dfb6c6750f0083689a026d9791543d17954054753f`
- assessment_seal: `fa70c099e59c7fecf86f6dce85aa3f98fe4d6094352c217fc1ecc5dcd06b8b36`
- counts: MATCH 6 / DRIFT 0 / UNVERIFIABLE 0
- integrity: seals_ok=True, thesis_ok=True, verdicts_rederive=True

## Verdicts

| Claim | Status | Disposition | Margin | Method | Grounds |
| --- | --- | --- | ---: | --- | --- |
| Pass 0150 created a MixedSourceProteinProofPacket/v1 artifact with status MIXED_SOURCE_PROTEIN_PROOF_PACKET_MATCH_WITH_WARNINGS and seal fce6663f6526c3436bcdca6be66b7f18ce4098e03d8b900f88a12c7d445e92f4. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |
| Pass 0150 stores 5 Gather-verified source bodies from 5 public URLs. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |
| Pass 0150 verifies UniProt and AlphaFold sequence identity for accession P69905 at length 142. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |
| Pass 0150 verifies RCSB entity 1A3N_1 as a mature-chain match of length 141, not a full canonical sequence match. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |
| Pass 0150 verifies the Europe PMC and PubMed metadata join for PubMed ID 6244294. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |
| Pass 0150 promotes no biological discovery, clinical claim, or protein design result. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |

## Measurement Evidence

| Claim | Method | Evidence |
| --- | --- | --- |
| Pass 0150 created a MixedSourceProteinProofPacket/v1 artifact with status MIXED_SOURCE_PROTEIN_PROOF_PACKET_MATCH_WITH_WARNINGS and seal fce6663f6526c3436bcdca6be66b7f18ce4098e03d8b900f88a12c7d445e92f4. | artifact-review | schema=MixedSourceProteinProofPacket/v1; status=MIXED_SOURCE_PROTEIN_PROOF_PACKET_MATCH_WITH_WARNINGS; seal=fce6663f6526c3436bcdca6be66b7f18ce4098e03d8b900f88a12c7d445e92f4 |
| Pass 0150 stores 5 Gather-verified source bodies from 5 public URLs. | artifact-review | sources=5; gather_verified_sources=5 |
| Pass 0150 verifies UniProt and AlphaFold sequence identity for accession P69905 at length 142. | artifact-review | accession=P69905; sequence_length=142 |
| Pass 0150 verifies RCSB entity 1A3N_1 as a mature-chain match of length 141, not a full canonical sequence match. | artifact-review | rcsb_id=1A3N_1; rcsb_sequence_length=141 |
| Pass 0150 verifies the Europe PMC and PubMed metadata join for PubMed ID 6244294. | artifact-review | pubmed_id=6244294; europepmc_title=Nucleotide sequence of the coding portion of human alpha globin messenger RNA. |
| Pass 0150 promotes no biological discovery, clinical claim, or protein design result. | artifact-review | current_promoted_biological_discoveries=[]; current_promoted_clinical_claims=[] |
