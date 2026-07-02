# Pass 0145 - Multi-Institution Claim Graph

## Summary

Status: `MULTI_INSTITUTION_CLAIM_GRAPH_MATCH_WITH_WARNINGS` with seal `ce64d5e9acfe20e097ca18a42d30cc8076cacfe07890282fe00bf8b74fa0308a`.
The replay covers `4` institutions and `18` stored Gather captures.

## Institution Verdicts

| Institution | Identity | Repository | Crossref |
| --- | --- | --- | --- |
| Massachusetts Institute of Technology | `MATCH` | `MATCH` | `MATCH` |
| Harvard University | `MATCH` | `MATCH` | `MATCH` |
| Cornell University | `MATCH` | `MATCH` | `SOURCE_LEAD_ONLY` |
| California Institute of Technology | `MATCH` | `MATCH` | `MATCH` |

## What Promoted

- Four ROR/OpenAlex identity joins matched expected institution identifiers.
- Four repository `Identify` captures matched expected OAI-PMH identity and protocol signals.
- Three Crossref affiliation samples matched expected affiliation strings.

## What Stayed Fenced

- Cornell Crossref stayed `SOURCE_LEAD_ONLY` after rate limiting.
- Caltech OAI endpoint documentation drift stayed a warning, not a silent normalization.
- No publication truth, full-text access, repository completeness, theorem, or natural law was promoted.

## Market Implication

A registry-scale research proof product needs reusable institution adapters with source-family receipts, rate-limit policy, endpoint-drift handling, and per-claim promotion gates.

## Boundary

Pass 0145 is a bounded four-institution replay over identity, repository Identify, and sampled scholarly graph surfaces. It does not claim complete institutional coverage, publication truth, repository harvest completeness, solved theorem status, market uniqueness, or natural-law discovery.
