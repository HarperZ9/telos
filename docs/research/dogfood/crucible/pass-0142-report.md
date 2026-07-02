# crucible report: Dogfood Pass 0142 Source Registry Federation

## Summary

- thesis_id: `e659e49eba6a2273`
- thesis_seal: `e659e49eba6a2273e084114a248f32d96c882361be4fb00d204554dc69fac3a9`
- assessment_seal: `a45bde3b104af579d3f059956617f6dc8dc26aba2d3635fbf9a24226b06709b9`
- counts: MATCH 6 / DRIFT 0 / UNVERIFIABLE 0
- integrity: seals_ok=True, thesis_ok=True, verdicts_rederive=True

## Verdicts

| Claim | Status | Disposition | Margin | Method | Grounds |
| --- | --- | --- | ---: | --- | --- |
| Pass 0142 created a SourceRegistryFederationReceipt/v1 artifact with status SOURCE_REGISTRY_FEDERATION_MATCH and seal e683c908d5b0e4a3c6b2b6ffba3061198bb496ab9b7ce59a92a9a7c26db8f03b. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |
| Pass 0142 records 33 source rows and 27 usable captures. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |
| Pass 0142 records 10 registry layers and 15 adapter requirements. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |
| Pass 0142 records 8 world-problem workbenches. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |
| Pass 0142 rejects 10 negative fixtures. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |
| Pass 0142 promotes no theorem or natural law. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |

## Measurement Evidence

| Claim | Method | Evidence |
| --- | --- | --- |
| Pass 0142 created a SourceRegistryFederationReceipt/v1 artifact with status SOURCE_REGISTRY_FEDERATION_MATCH and seal e683c908d5b0e4a3c6b2b6ffba3061198bb496ab9b7ce59a92a9a7c26db8f03b. | artifact-review | schema=SourceRegistryFederationReceipt/v1; status=SOURCE_REGISTRY_FEDERATION_MATCH; seal=e683c908d5b0e4a3c6b2b6ffba3061198bb496ab9b7ce59a92a9a7c26db8f03b |
| Pass 0142 records 33 source rows and 27 usable captures. | artifact-review | gather_summary={'captured_sources': 30, 'total_source_rows': 33, 'usable_captures': 27, 'warning_count': 6, 'families': 10} |
| Pass 0142 records 10 registry layers and 15 adapter requirements. | artifact-review | registry_layers=10; adapter_requirements=15 |
| Pass 0142 records 8 world-problem workbenches. | artifact-review | world_problem_workbenches=8 |
| Pass 0142 rejects 10 negative fixtures. | artifact-review | negative_fixtures=10 |
| Pass 0142 promotes no theorem or natural law. | artifact-review | current_promoted_theorems=[]; current_promoted_natural_laws=[] |
