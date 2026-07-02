# Research Archive Substrate Atlas Brief

Date: 2026-07-02

## Decision

The next scale move is an `ArchiveAdapterSDK`: every source system should
produce the same minimum receipt fields before it can feed claim packets,
experiment packets, theorem packets, model-foundry runs, or BuildLang kernels.

## Result

Pass 0140 records `30` source systems, `14` substrate families, `18` domain queues, and `6` megatool routes. It also keeps empty and failed captures out of the evidence lane.

## Primary Push

Build two concrete adapters next: `ScholarlyGraphAdapter` for OpenAlex/Crossref/Semantic Scholar and `BioExperimentAdapter` for PubMed/PMC/GEO/SRA/ClinicalTrials.
