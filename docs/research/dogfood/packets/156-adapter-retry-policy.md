# Pass 0146 - Adapter Retry Policy

Status: `ADAPTER_RETRY_POLICY_MATCH` with seal `8a20aae5a90e77621ecb7498d90665b17e53393b33109768e92eab17feaea4a5`.

## Policy Rows

| Rule | Status | Action |
| --- | --- | --- |
| `RATE_LIMITED_429` | `SOURCE_LEAD_ONLY_RETRYABLE` | honor Retry-After if present; otherwise exponential backoff and lower concurrency |
| `RETRY_AFTER_PARSE` | `SCHEDULER_REQUIRED` | accept HTTP-date or delay-seconds and record the parsed wait |
| `NO_AUTO_RETRY_ON_HEADERLESS_503` | `HALT_OR_OPERATOR_POLICY` | do not tight-loop when a repository omits Retry-After |
| `CROSSREF_POLITE_MAILTO` | `CONTACTABILITY_REQUIRED` | include mailto or user-agent for Crossref public/polite pool accountability |
| `CROSSREF_403_BLOCKED` | `ACCESS_ESCALATION` | stop retries and record block/support path |
| `OPENALEX_API_KEY_CURRENT` | `AUTH_POLICY` | treat mailto-only OpenAlex polite-pool logic as stale after the API-key shift |
| `OPENALEX_BACKOFF` | `SCHEDULER_REQUIRED` | read rate headers and use exponential backoff on 429 |
| `ROR_CLIENT_ID_READY` | `AUTH_POLICY` | prepare client-id field for Q3 2026 rate-limit split |
| `ROR_LOCAL_DOCKER_FALLBACK` | `BULK_FALLBACK` | route high-volume ROR work to local Docker mirror when needed |
| `OAI_RESUMPTION_TOKEN_CHAIN` | `PAGINATION_CONTRACT` | persist token, cursor, completeListSize, and expiration when supplied |
| `OAI_BAD_RESUMPTION_RESTART` | `CHECKPOINT_REQUIRED` | restart from bounded date/set checkpoint, not from an arbitrary token |
| `INDEX_SELECTOR_ROOT_FALLBACK` | `CONTEXT_SELECTOR_DRIFT` | retry root-only context and record selector failure as tool-interface evidence |

## What Changed

- Cornell-style 429s become retryable source leads, not absence evidence.
- Caltech-style endpoint drift becomes an endpoint alias warning, not repository absence.
- OpenAlex mailto-only logic is rejected as stale after its API-key shift.
- OAI-PMH resumption tokens become checkpointed pagination state.
- Index selector failures become context-selector drift receipts with root fallback.

## Boundary

Pass 0146 defines scheduler and promotion policy for source adapters. It does not prove source correctness, complete coverage, market uniqueness, theorem progress, or natural-law discovery.
