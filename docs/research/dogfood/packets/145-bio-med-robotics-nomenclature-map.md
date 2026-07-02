# Packet 145: Wide Research Substrate and Bio/Med/Robotics Nomenclature Map

Date: 2026-07-02

Status: `BIO_MED_ROBOTICS_NOMENCLATURE_MAP_MATCH`

Purpose: turn the current request into a scalable source substrate: current
biology, medicine, robotics, and adjacent research signals, plus archive and
database intake routes for future hundreds-source pulls across domains.

```text
source_receipts = 32
usable_sources = 26
source_warnings = 6
archive_substrates = 12
domain_lanes = 8
domain_queue = 14
terminology_bridges = 8
compose_status = MATCH
test_status = MATCH
validator_status = MATCH
```

## Domain Lanes

| Lane | Biology terms | Medicine terms | Robotics terms | Tool target |
| --- | --- | --- | --- | --- |
| morphogenesis_bioelectricity_collective_intelligence | bioelectricity, morphogenesis | regenerative medicine, morphoceutics | swarm intelligence, morphogenetic robotics | Morphogenesis claim-to-experiment packet |
| virtual_cell_single_cell_spatial_omics | single-cell foundation model, spatial omics | patient stratification, preclinical virtual cell | world model, state representation | Virtual-cell evidence packet |
| bioelectronic_closed_loop_therapy | bioelectronic medicine, neuromodulation | closed-loop therapy, adaptive stimulation | feedback control, sensor-actuator loop | Therapy action receipt |
| organ_chip_organoid_human_on_chip | microphysiological system, organoid | drug testing, toxicity | sim-to-real testbed, embodied benchmark | Experiment reproducibility packet |
| physical_ai_robot_foundation_models | VLA, robot foundation model | assistive robotics, rehabilitation robotics | generalist policy, embodied AI | Robot policy proof packet |
| surgical_ai_medical_robotics_continuum | continuum robot, soft robot | minimally invasive surgery, surgical autonomy | compliant body control, teleoperation | Operating-room evidence packet |
| thermodynamic_probabilistic_biophysical_compute | stochastic dynamics, thermodynamic compute | Bayesian medicine, scientific simulation | probabilistic controller, sampling hardware | Stochastic compute receipt |
| translation_and_nomenclature | same mechanism, different vocabulary | clinical endpoint, regulatory evidence | task success, safety case | Cross-domain nomenclature resolver |

## Archive Substrates

| Source | Kind | Coverage |
| --- | --- | --- |
| OpenAlex | metadata_graph | works, authors, sources, institutions, topics |
| Crossref | metadata_graph | works, funders, licenses, references, ORCID/ROR |
| Semantic Scholar | metadata_graph | papers, authors, citations, recommendations, datasets |
| CORE | full_text_aggregator | repository metadata and open full-text access points |
| arXiv | preprint_archive | math, physics, computer science, quantitative biology, statistics |
| bioRxiv/medRxiv | preprint_archive | preprints, publication links, interval feeds |
| NCBI/PubMed/PMC | biomedical_archive | PubMed, PMC, Gene, Nuccore, Protein |
| NASA ADS | domain_archive | search, metrics, export functions |
| Dataverse | data_repository | datasets, files, metadata, permissions |
| Zenodo | data_repository | records, files, deposits, OAI-PMH |
| OSF | data_repository | projects, study designs, data, manuscripts, materials |
| Materials Project | domain_database | computed material properties and API client |

## Expansion Queue

| Domain | First tooling target |
| --- | --- |
| biology | claim-to-experiment packets |
| medicine | safety and endpoint receipts |
| robotics | embodied action replay |
| mathematics | prover-verifier packets |
| physics | law-boundary and simulator receipts |
| materials | materials property proof packets |
| chemistry | stoichiometry and synthesis receipts |
| climate_energy | simulation provenance packets |
| security | exploit/fix proof packets |
| finance | model-risk and optimization receipts |
| education | source-backed lesson receipts |
| governance_law | claim provenance and decision receipts |
| neuroscience | closed-loop experiment receipts |
| economics | causal evidence packets |

## Source Quality Warnings

| Source | Warning |
| --- | --- |
| OSF APIv2 Documentation | empty_capture |
| https://ui.adsabs.harvard.edu/help/api/ | empty_capture |
| Client Challenge | client_challenge |
| Client Challenge | client_challenge |
| Client Challenge | client_challenge |
| Client Challenge | client_challenge |

## Boundary

Pass 0135 maps current source terminology across biology, medicine, robotics, AI, controls, and scientific compute. It does not claim that shared vocabulary proves shared mechanism, clinical efficacy, robot safety, or natural law.
