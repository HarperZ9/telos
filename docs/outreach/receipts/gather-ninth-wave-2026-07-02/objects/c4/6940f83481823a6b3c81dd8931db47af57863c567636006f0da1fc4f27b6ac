# Packet 150: Research Archive Substrate Atlas

Date: 2026-07-02

Status: `RESEARCH_ARCHIVE_SUBSTRATE_ATLAS_MATCH`

Purpose: create the first broad, receipt-backed substrate atlas for sourcing
research across publishing archives, preprint servers, scholarly graphs,
domain databases, institutional repositories, and public data portals.

```text
captured_sources = 28
usable_captures = 26
source_systems = 30
source_quality_warnings = 4
substrate_families = 14
domain_queue = 18
megatool_routes = 6
negative_fixtures = 10
seal = 2f3e0d8715396aeda6823b937a141664e8372e273c735d9d05429dffa4edb1ff
```

## Source Systems

| System | Category | Protocol | Evidence |
| --- | --- | --- | --- |
| BASE | academic_search_index | browser_or_oai_followup_required | STATIC_CAPTURE_FAILED_SOURCE_LEAD |
| NCBI E-utilities | biomedical_api | entrez_api | GATHER_VERIFIED |
| ClinicalTrials.gov | clinical_registry | rest_json_openapi | GATHER_VERIFIED |
| DataCite | doi_metadata_graph | rest_jsonapi | GATHER_VERIFIED |
| NASA ADS | domain_literature_index | rest_json_api_key | GATHER_VERIFIED_EMPTY_CAPTURE |
| PMC OAI-PMH | full_text_open_access | oai_pmh | GATHER_VERIFIED |
| NCBI GEO | functional_genomics_repository | web_api_download | GATHER_VERIFIED |
| NCBI SRA | genomics_archive | ncbi_cloud_tools | GATHER_VERIFIED |
| Materials Project | materials_database | python_client_api | GATHER_VERIFIED |
| OpenML | ml_dataset_benchmark_repository | rest_api | GATHER_VERIFIED |
| Hugging Face Dataset Viewer | ml_dataset_hub | rest_api | GATHER_VERIFIED |
| ENA | nucleotide_archive | browser_api | GATHER_VERIFIED |
| CORE | open_access_aggregator | api_bulk | GATHER_VERIFIED |
| OSF API | open_science_repository | rest_json | GATHER_VERIFIED_EMPTY_CAPTURE |
| arXiv | preprint_archive | api_oai_bulk | GATHER_VERIFIED |
| arXiv | preprint_archive | api_oai_bulk | GATHER_VERIFIED |
| bioRxiv | preprint_archive | api_interval_cursor | GATHER_VERIFIED |
| medRxiv | preprint_archive | api_interval_cursor | GATHER_VERIFIED |
| UniProt | protein_knowledgebase | rest_download | GATHER_VERIFIED |
| Crossref | publisher_metadata_graph | rest_json | GATHER_VERIFIED |
| OAI-PMH | repository_interop_protocol | oai_pmh | GATHER_VERIFIED |
| Zenodo | research_data_repository | rest_oai | GATHER_VERIFIED |
| OpenAlex | scholarly_graph | rest_json_snapshot | GATHER_VERIFIED |
| Semantic Scholar | scholarly_graph | rest_json_datasets | GATHER_VERIFIED |
| RCSB PDB Data API | structure_database | rest_graphql | GATHER_VERIFIED |
| RCSB PDB Search API | structure_search | rest_json | GATHER_VERIFIED |
| Caltech repository OAI endpoints | university_repository | oai_pmh | GATHER_VERIFIED |
| DSpace@MIT | university_repository | browser_or_oai_followup_required | STATIC_CAPTURE_FAILED_SOURCE_LEAD |
| Harvard DASH | university_repository | repository_oai | GATHER_VERIFIED |
| Stanford Digital Repository | university_repository | repository_web | GATHER_VERIFIED |

## Source Quality Warnings

| System | Status | URL |
| --- | --- | --- |
| BASE | STATIC_CAPTURE_FAILED_SOURCE_LEAD | https://www.base-search.net/ |
| NASA ADS | GATHER_VERIFIED_EMPTY_CAPTURE | https://ui.adsabs.harvard.edu/help/api/ |
| OSF API | GATHER_VERIFIED_EMPTY_CAPTURE | https://developer.osf.io/ |
| DSpace@MIT | STATIC_CAPTURE_FAILED_SOURCE_LEAD | https://dspace.mit.edu/ |

## Substrate Families

| Family | Tooling target |
| --- | --- |
| preprint_archives | rapid frontier claim intake |
| publisher_metadata_graphs | provenance, references, licenses, funders |
| scholarly_graphs | literature graph and institutional coverage |
| open_full_text | text mining and claim extraction |
| clinical_registries | protocol and endpoint receipts |
| biomedical_databases | bio/medicine experiment substrate |
| materials_chemistry | property prediction and simulation receipts |
| ml_dataset_hubs | benchmark provenance and contamination checks |
| general_data_repositories | data DOI and reproducibility packets |
| university_repositories | institutional thesis/report/article harvesting |
| government_science_data | public measurement substrates |
| formal_math_repositories | machine-checkable proof receipts |
| standards_and_patents | engineering constraints and prior art |
| policy_and_law | governance claim provenance |

## Domain Expansion Queue

| Domain | First product |
| --- | --- |
| math_formal_methods | ProofPacket and LeanProofReceipt |
| physics_quantum_cosmology | simulator and law-boundary receipts |
| biology_genomics | claim-to-experiment packets |
| medicine_clinical | clinical endpoint receipts |
| materials_chemistry | property replay packets |
| robotics_embodied_ai | embodied action receipts |
| ai_ml | dataset/model contamination receipts |
| climate_energy | earth/energy simulation receipts |
| security_cryptography | exploit/fix proof packets |
| finance_economics | risk and causal evidence packets |
| education_learning | learning graph receipts |
| law_policy_governance | decision provenance receipts |
| neuroscience_bci | closed-loop experiment packets |
| agriculture_food | crop/system optimization receipts |
| transportation_cities | infrastructure optimization packets |
| semiconductors_hpc | compiler/runtime receipts |
| color_rendering_media | measurement truth kits |
| philosophy_cognitive_science | functional learning maps |

## Megatool Routes

| Route | Tools | Output |
| --- | --- | --- |
| archive_to_claim_packet | Gather + Index + Crucible | source-backed claim with verification state |
| claim_to_experiment_packet | Gather + Telos + Crucible + BuildLang/buildc | protocol, runtime receipt, measurement, verifier |
| dataset_to_model_receipt | Gather + Index + Model Foundry + Crucible | dataset lineage, contamination gate, eval receipt |
| paper_to_formal_proof | Gather + Index + Lean/ATP adapter + Crucible | machine-checkable theorem replay packet |
| university_repo_to_learning_graph | Gather + Index + Forum + Learning Forge | source-backed lesson and prerequisite graph |
| domain_database_to_build_kernel | Gather + BuildLang/buildc + Crucible | compiled scientific kernel with data provenance |

## Boundary

Pass 0140 is a first-wave archive substrate atlas. It does not claim complete world coverage, source correctness, publication validity, market demand, theorem proof, experimental truth, or natural-law promotion.
