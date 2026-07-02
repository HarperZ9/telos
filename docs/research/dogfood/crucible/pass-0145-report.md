# crucible report: Dogfood Pass 0145 Multi-Institution Claim Graph

## Summary

- thesis_id: `c5ad4c7e77908b5a`
- thesis_seal: `c5ad4c7e77908b5ad5b6784065d686b71ed35959838d7a67c66e750d324ece56`
- assessment_seal: `5098df53e2523212971e003b109ee8ebb84dfafdcdd9018bf9dd9e24d8bd7fbb`
- counts: MATCH 5 / DRIFT 0 / UNVERIFIABLE 0
- integrity: seals_ok=True, thesis_ok=True, verdicts_rederive=True

## Verdicts

| Claim | Status | Disposition | Margin | Method | Grounds |
| --- | --- | --- | ---: | --- | --- |
| Pass 0145 created a MultiInstitutionClaimGraphReceipt/v1 artifact with status MULTI_INSTITUTION_CLAIM_GRAPH_MATCH_WITH_WARNINGS and seal ce64d5e9acfe20e097ca18a42d30cc8076cacfe07890282fe00bf8b74fa0308a. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |
| Pass 0145 records 4 institutions and 18 stored captures. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |
| Pass 0145 records 4 identity matches, 4 repository matches, and 3 Crossref matches. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |
| Pass 0145 rejects 10 negative fixtures and records 3 warnings. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |
| Pass 0145 promotes no theorem or natural law. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |

## Measurement Evidence

| Claim | Method | Evidence |
| --- | --- | --- |
| Pass 0145 created a MultiInstitutionClaimGraphReceipt/v1 artifact with status MULTI_INSTITUTION_CLAIM_GRAPH_MATCH_WITH_WARNINGS and seal ce64d5e9acfe20e097ca18a42d30cc8076cacfe07890282fe00bf8b74fa0308a. | artifact-review | schema=MultiInstitutionClaimGraphReceipt/v1; status=MULTI_INSTITUTION_CLAIM_GRAPH_MATCH_WITH_WARNINGS; seal=ce64d5e9acfe20e097ca18a42d30cc8076cacfe07890282fe00bf8b74fa0308a |
| Pass 0145 records 4 institutions and 18 stored captures. | artifact-review | summary={'institutions': 4, 'stored_captures': 18, 'distinct_bodies': 18, 'support_docs': 3, 'identity_matches': 4, 'repository_matches': 4, 'crossref_matches': 3, 'warnings': 3} |
| Pass 0145 records 4 identity matches, 4 repository matches, and 3 Crossref matches. | artifact-review | join_verdicts=[{'institution': 'mit', 'join': 'identity', 'status': 'MATCH'}, {'institution': 'mit', 'join': 'repository', 'status': 'MATCH'}, {'institution': 'mit', 'join': 'crossref', 'status': 'MATCH'}, {'institution': 'harvard', 'join': 'identity', 'status': 'MATCH'}, {'institution': 'harvard', 'join': 'repository', 'status': 'MATCH'}, {'institution': 'harvard', 'join': 'crossref', 'status': 'MATCH'}, {'institution': 'cornell', 'join': 'identity', 'status': 'MATCH'}, {'institution': 'cornell', 'join': 'repository', 'status': 'MATCH'}, {'institution': 'cornell', 'join': 'crossref', 'status': 'SOURCE_LEAD_ONLY'}, {'institution': 'caltech', 'join': 'identity', 'status': 'MATCH'}, {'institution': 'caltech', 'join': 'repository', 'status': 'MATCH'}, {'institution': 'caltech', 'join': 'crossref', 'status': 'MATCH'}] |
| Pass 0145 rejects 10 negative fixtures and records 3 warnings. | artifact-review | negative_fixtures=10; source_warnings=3 |
| Pass 0145 promotes no theorem or natural law. | artifact-review | current_promoted_theorems=[]; current_promoted_natural_laws=[] |
