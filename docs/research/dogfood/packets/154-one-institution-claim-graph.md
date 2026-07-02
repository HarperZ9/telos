# Pass 0144 - One Institution Claim Graph

## Summary

Status: `ONE_INSTITUTION_CLAIM_GRAPH_MATCH_WITH_WARNINGS`. The pass records `6` live captures and `5` protocol docs for `Massachusetts Institute of Technology`.

## Join Verdicts

- `ror_openalex_identity`: `MATCH`
- `dspace_oai_identify`: `MATCH`
- `dspace_recent_record_sample`: `MATCH`
- `crossref_affiliation_sample`: `MATCH`
- `datacite_dataset_relation`: `SOURCE_LEAD_ONLY`

## What Promoted

- ROR and OpenAlex identity join for MIT.
- MIT DSpace OAI-PMH endpoint reachability and a date-filtered record sample.
- Crossref sample containing MIT affiliation strings.

## What Stayed Fenced

- DataCite keyword-query results stay `SOURCE_LEAD_ONLY` until explicit affiliation or ROR links are verified.
- Semantic Scholar stays a rate-limit warning, not absence evidence.
- No full text, dataset relation, publication truth, theorem, or natural law was promoted.

## Boundary

Pass 0144 is a bounded live adapter run for one institution. It does not claim complete MIT coverage, dataset linkage, publication truth, full-text access, world coverage, theorem proof, market uniqueness, or natural-law discovery.
