# Pass 0143 - Registry Adapter Contracts

## Summary

Status: `REGISTRY_ADAPTER_CONTRACTS_MATCH`. This pass turns pass 0142 source-registry breadth into `2` adapter contracts, `6` repository-directory fixtures, `8` scholarly-graph fixtures, and `10` rejection fixtures.

The practical goal is a reusable intake spine for massive research: every source row must carry a source hash, identifier policy, freshness boundary, license/terms reference, verifier ref, and explicit failure codes before it can feed proof packets.

## Contracts

### RepositoryDirectoryAdapter

- Product: `ResearchSourceRouter`
- Purpose: Normalize repository-directory and repository-platform evidence into harvestable, source-backed institutional and data repository records.
- Required fields: `18`
- Rejects: repository listing as complete corpus, endpoint candidate as verified endpoint behavior, organization label as endorsement

### ScholarlyGraphAdapter

- Product: `ClaimToExperimentPacket`
- Purpose: Normalize work, citation, author, dataset, repository-location, funder, license, and version metadata into claim-to-proof packet context.
- Required fields: `21`
- Rejects: metadata-only as full text, preprint as peer review, graph relation as causality

## First Workbench

`one_institution_claim_graph`
- choose one university or lab
- resolve ROR identity
- discover repositories through directory records
- harvest OAI-PMH or REST endpoint candidates
- join works through Crossref/DataCite/OpenAlex/Semantic Scholar
- emit claim-to-experiment packet with negative fixtures

## Pipeline

- Gather: capture source URL, body hash, local docs, and warning state
- Index: bind adapter contract to workspace and source-registry context
- Forum: route source, domain, legal/license, and proof-packet validation lanes
- Telos: record adapter actions, admission decisions, and loop-ledger receipts
- Crucible: reject negative fixtures and verify contract measurements

## Boundary

Pass 0143 defines adapter contracts and fixtures. It does not certify live repository coverage, DOI correctness, full-text access, market uniqueness, theorem proof, or natural-law discovery.
