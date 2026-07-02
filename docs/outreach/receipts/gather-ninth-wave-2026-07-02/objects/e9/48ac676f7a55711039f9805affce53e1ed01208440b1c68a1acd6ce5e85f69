# Pass 0142 - Source Registry Federation

## Summary

Status: `SOURCE_REGISTRY_FEDERATION_MATCH`. The pass records `33` source rows, `27` usable captures, `10` source families, and `6` warnings.

The strategic shift is from individual archive discovery to registry federation: use repository directories, scholarly graphs, organization identifiers, preprint APIs, platform protocols, and domain databases to scale toward hundreds of substrates.

## Registry Layers

### repository_directories

- Adapter: `RepositoryDirectoryAdapter`
- Purpose: Find institutional, disciplinary, and data repositories before adapter work begins.
- Sources: OpenDOAR, re3data, OpenAIRE data sources, BASE

### research_org_identity

- Adapter: `OrganizationIdentityAdapter`
- Purpose: Connect university, lab, funder, hospital, and institute identities to outputs and repositories.
- Sources: ROR

### scholarly_graphs

- Adapter: `ScholarlyGraphAdapter`
- Purpose: Map works, authors, institutions, citations, funders, licenses, datasets, and repository links.
- Sources: OpenAlex, Semantic Scholar, Crossref, DataCite, CORE

### open_access_and_journals

- Adapter: `OpenAccessStateAdapter`
- Purpose: Classify open access state, journal metadata, license state, and legal full-text routes.
- Sources: DOAJ, Unpaywall

### preprint_press

- Adapter: `PreprintIntakeAdapter`
- Purpose: Capture fast-moving claims before peer review while fencing publication and replication state.
- Sources: arXiv, bioRxiv, medRxiv, OSF Preprints

### biomedical_literature

- Adapter: `BiomedicalLiteratureAdapter`
- Purpose: Route biomedical literature, grants, clinical links, full text, and annotations into claim cards.
- Sources: Europe PMC, NCBI APIs, PubMed, PMC

### repository_platforms

- Adapter: `RepositoryPlatformAdapter`
- Purpose: Normalize institutional repository platform protocols into one ingest and replay contract.
- Sources: Dataverse, DSpace, InvenioRDM, OAI-PMH

### domain_data_systems

- Adapter: `DomainDataAdapter`
- Purpose: Capture domain databases where claims depend on sequences, structures, materials, and measured properties.
- Sources: UniProt, RCSB PDB, Materials Project

### ml_dataset_hubs

- Adapter: `MLDatasetHubAdapter`
- Purpose: Track dataset rows, splits, tasks, model-eval context, contamination risk, and benchmark provenance.
- Sources: OpenML, Hugging Face Dataset Viewer

### interoperability_protocols

- Adapter: `ProtocolNegotiationAdapter`
- Purpose: Choose the cheapest reliable route for massive, repeatable, source-bounded harvesting.
- Sources: OAI-PMH, REST, Graph APIs, bulk dumps

## Cross-Industry Underpinnings

- Every field needs source identity, organization identity, version identity, license state, access route, and freshness receipts.
- Every scientific claim must separate source existence, claim text, measurement, computation, proof, replication, and market relevance.
- Preprint, dataset, registry, and repository records are leads until paired with verification, replay, or independent measurement.
- A universal research substrate needs adapters for metadata graphs, repository protocols, full text, domain databases, executable kernels, and review verdicts.
- Hard-problem work should start with falsifiable claim cards and negative controls before synthesis or theorem promotion.

## World-Problem Workbenches

- `formal_math_theorem_factory`: Convert one theorem source cluster into statement variants, proof obligations, Lean replay gates, and counterexample search receipts.
- `physics_law_candidate_lab`: Build law-candidate packets with units, invariants, simulation replay, uncertainty, and falsification criteria.
- `biology_mechanism_lab`: Join paper claims to sequence, protein, structure, pathway, and experiment records before biological synthesis.
- `clinical_evidence_lab`: Separate protocol, endpoint, cohort, result, replication, and safety evidence into clinical claim packets.
- `materials_discovery_lab`: Build property-prediction packets that join source claim, computed property, structure, code, and error bounds.
- `ai_benchmark_truth_lab`: Create contamination, split, license, model-output, and verifier receipts for benchmark claims.
- `institutional_knowledge_graph`: Map one university from organization identity to repository endpoints, datasets, theses, papers, grants, and labs.
- `buildlang_scientific_runtime`: Compile one exact scientific kernel with source, data, units, benchmark, runtime, and verifier receipts.

## Boundary

This pass maps scalable discovery substrate. It does not claim complete world coverage, source correctness, publication validity, theorem proof, experimental truth, or market uniqueness.
