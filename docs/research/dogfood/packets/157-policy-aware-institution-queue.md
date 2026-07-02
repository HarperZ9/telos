# Pass 0147 - Policy-Aware Institution Queue

Status: `POLICY_AWARE_INSTITUTION_QUEUE_MATCH_WITH_WARNINGS` with seal `a03477888d31ffe286ec4ea38620342f4ab08480acf202412a590c8da10416f3`.

## Institution Queue

| Institution | Identity | Repository | Crossref | Warning Count |
| --- | --- | --- | --- | --- |
| ETH Zurich | `MATCH` | `OAI_IDENTIFY_MATCH` | `SAMPLED_AFFILIATION_MATCH` | `0` |
| University of Tokyo | `RANKED_ALIAS_MATCH_WITH_WARNING` | `OAI_IDENTIFY_MATCH` | `SAMPLED_AFFILIATION_MATCH` | `1` |
| University of Cape Town | `MATCH` | `OAI_IDENTIFY_MATCH` | `SAMPLED_AFFILIATION_MATCH` | `0` |
| Universidade de Sao Paulo | `MATCH` | `SOURCE_LEAD_ONLY_ENDPOINT_DRIFT` | `SAMPLED_AFFILIATION_MATCH` | `1` |

## Queue Policies

- ranked ROR/OpenAlex identity joins before promotion
- OAI endpoint drift remains a source lead, not absence evidence
- Crossref affiliation samples remain sample-only metadata
- non-US institution coverage is a queue seed, not global coverage

## Key Warnings

- Identity ranking warnings: `1`.
- Repository endpoint warnings: `1`.
- University of Tokyo demonstrates that first ROR hit is not safe enough for promotion.
- Universidade de Sao Paulo demonstrates that an OAI-looking page can still be endpoint drift.

## Boundary

Pass 0147 proves a policy-aware queue receipt over four institution source leads. It does not prove repository completeness, global coverage, research quality, theorem progress, or natural-law discovery.
