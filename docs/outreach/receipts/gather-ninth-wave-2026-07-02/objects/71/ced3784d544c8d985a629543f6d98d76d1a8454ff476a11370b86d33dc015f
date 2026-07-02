# Pass 0148 - Live Source Router Probes

Status: `LIVE_SOURCE_ROUTER_PROBES_MATCH_WITH_WARNINGS` with seal `6fa211ccd91517425f8a33ce9f32fd396dff00067ccbf1e13a328d25b8770944`.

## Route Matrix

| Family | System | Status | Warning |
| --- | --- | --- | --- |
| preprint_press | arXiv | `LIVE_QUERY_MATCH` | `` |
| preprint_press | bioRxiv | `LIVE_QUERY_MATCH` | `` |
| preprint_press | medRxiv | `LIVE_QUERY_MATCH` | `` |
| preprint_press | ChemRxiv | `SOURCE_LEAD_ONLY_WARNING` | `HTTP_403_SOURCE_LEAD_ONLY` |
| preprint_press | OSF Preprints | `LIVE_QUERY_MATCH` | `` |
| preprint_press | HAL | `FALLBACK_DOCS_MATCH_WITH_PRIMARY_WARNING` | `HTTPS_TRANSPORT_FALLBACK` |
| scholarly_graph | Crossref | `LIVE_QUERY_MATCH` | `` |
| scholarly_graph | OpenAlex | `FALLBACK_DOCS_MATCH_WITH_PRIMARY_WARNING` | `HTTP_503_RETRYABLE` |
| scholarly_graph | DataCite | `LIVE_QUERY_MATCH` | `` |
| biomedical_literature | Europe PMC | `LIVE_QUERY_MATCH` | `` |
| biomedical_literature | NCBI PubMed | `LIVE_QUERY_MATCH` | `` |
| scholarly_graph | Semantic Scholar | `FALLBACK_DOCS_MATCH_WITH_PRIMARY_WARNING` | `HTTP_429_RETRYABLE` |
| open_access | DOAJ | `LIVE_QUERY_MATCH` | `` |
| repository_directory | re3data docs | `LIVE_QUERY_MATCH` | `` |
| repository_directory | re3data search | `LIVE_QUERY_MATCH` | `` |
| repository_directory | OpenDOAR | `SOURCE_LEAD_ONLY_WARNING` | `TLS_HANDSHAKE_SOURCE_LEAD_ONLY` |
| repository_directory | BASE OAI | `FALLBACK_DOCS_MATCH_WITH_PRIMARY_WARNING` | `HTTP_403_RESTRICTED_INTERFACE` |
| scholarly_graph | OpenAIRE | `LIVE_QUERY_MATCH` | `` |
| college_repository | MIT DSpace | `LIVE_QUERY_MATCH` | `` |
| college_repository | Harvard DASH | `LIVE_QUERY_MATCH` | `` |
| college_repository | Oxford ORA | `LIVE_QUERY_MATCH` | `` |
| college_repository | Cambridge Apollo | `FALLBACK_DOCS_MATCH_WITH_PRIMARY_WARNING` | `HTTP_404_ENDPOINT_ALIAS_REQUIRED` |
| college_repository | Southampton ePrints | `LIVE_QUERY_MATCH` | `` |
| research_data_repository | Harvard Dataverse | `LIVE_QUERY_MATCH` | `` |
| research_data_repository | Zenodo | `LIVE_QUERY_MATCH` | `` |

## Router Policies

- live query success is a route receipt, not source correctness
- fallback docs bind adapter contracts when live routes fail
- HTTP 429, 503, 403, TLS, and 404 become scheduler or endpoint-alias statuses
- preprint and repository records stay sample-only until claim extraction and verification

## Strategic Result

- `18` live query routes matched.
- `5` routes matched through fallback docs or alternate endpoints.
- `2` routes remained source-lead-only warnings.
- The next implementation should schedule retries, endpoint aliases, and claim extraction as separate receipts.

## Boundary

Pass 0148 tests live source-router routes across archive, preprint, scholarly graph, biomedical, repository-directory, college repository, and data repository surfaces. It does not prove source correctness, full-text access, domain coverage, peer review, theorem progress, or natural-law discovery.
