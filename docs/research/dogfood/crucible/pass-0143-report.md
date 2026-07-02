# crucible report: Dogfood Pass 0143 Registry Adapter Contracts

## Summary

- thesis_id: `c6c79e6bab8b0290`
- thesis_seal: `c6c79e6bab8b0290b6982201d5aed8a1e1e1e985225f8f3f44ea538ab507a483`
- assessment_seal: `ad707fff5a92284a4a1022ddf68a4fb8a36ef61dba1a35b940dc2432b318510e`
- counts: MATCH 6 / DRIFT 0 / UNVERIFIABLE 0
- integrity: seals_ok=True, thesis_ok=True, verdicts_rederive=True

## Verdicts

| Claim | Status | Disposition | Margin | Method | Grounds |
| --- | --- | --- | ---: | --- | --- |
| Pass 0143 created a RegistryAdapterContractsReceipt/v1 artifact with status REGISTRY_ADAPTER_CONTRACTS_MATCH and seal 6d0ad15f379bb9bc4f971b1ec0c564a112e2fd9f80ad523fb88dac54905da88b. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |
| Pass 0143 records 2 adapter contracts, 6 repository fixtures, and 8 scholarly graph fixtures. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |
| Pass 0143 records 15 join keys and 10 negative fixtures. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |
| Pass 0143 references pass 0142 source registry seal e683c908d5b0e4a3c6b2b6ffba3061198bb496ab9b7ce59a92a9a7c26db8f03b with 33 source rows. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |
| Pass 0143 observed 5 updated tool-floor receipts with 0 version mismatches. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |
| Pass 0143 promotes no theorem or natural law. | MATCH | fenced | 1 | artifact-review | deviation 0 within tolerance 0.5 |

## Measurement Evidence

| Claim | Method | Evidence |
| --- | --- | --- |
| Pass 0143 created a RegistryAdapterContractsReceipt/v1 artifact with status REGISTRY_ADAPTER_CONTRACTS_MATCH and seal 6d0ad15f379bb9bc4f971b1ec0c564a112e2fd9f80ad523fb88dac54905da88b. | artifact-review | schema=RegistryAdapterContractsReceipt/v1; status=REGISTRY_ADAPTER_CONTRACTS_MATCH; seal=6d0ad15f379bb9bc4f971b1ec0c564a112e2fd9f80ad523fb88dac54905da88b |
| Pass 0143 records 2 adapter contracts, 6 repository fixtures, and 8 scholarly graph fixtures. | artifact-review | contracts=2; repo_records=6; graph_records=8 |
| Pass 0143 records 15 join keys and 10 negative fixtures. | artifact-review | join_keys=15; negative_fixtures=10 |
| Pass 0143 references pass 0142 source registry seal e683c908d5b0e4a3c6b2b6ffba3061198bb496ab9b7ce59a92a9a7c26db8f03b with 33 source rows. | artifact-review | source_registry_ref={'schema': 'SourceRegistryFederationReceipt/v1', 'pass': '0142', 'status': 'SOURCE_REGISTRY_FEDERATION_MATCH', 'seal': 'e683c908d5b0e4a3c6b2b6ffba3061198bb496ab9b7ce59a92a9a7c26db8f03b', 'source_rows': 33, 'usable_captures': 27} |
| Pass 0143 observed 5 updated tool-floor receipts with 0 version mismatches. | artifact-review | observed_tool_floor={'gather': {'command': 'gather --version', 'exit_code': 0, 'stdout_first_line': 'gather 1.5.0', 'stdout_sha256': '4d6ad2661e845c0cc04012d80b3bc4b2f376508b7854f73a932470f9e33b860f', 'stderr_sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'observed_version': '1.5.0', 'status': 'MATCH', 'tool': 'gather'}, 'index': {'command': 'index --version', 'exit_code': 0, 'stdout_first_line': 'index 2.8.0', 'stdout_sha256': '9952767d2790c2471796bc4d1b7980f55428298965835d9edb070b240d8060d3', 'stderr_sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'observed_version': '2.8.0', 'status': 'MATCH', 'tool': 'index'}, 'forum': {'command': 'forum --version', 'exit_code': 0, 'stdout_first_line': 'forum 1.12.0', 'stdout_sha256': 'c08e4475db0dea46f86c0441af54c7d13387881ae2557dcddcaeb2fdf5e8d18c', 'stderr_sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'observed_version': '1.12.0', 'status': 'MATCH', 'tool': 'forum'}, 'crucible': {'command': 'crucible --version', 'exit_code': 0, 'stdout_first_line': 'crucible 1.1.0', 'stdout_sha256': 'c9a3c2e0a32c682af3a84e8ee4bbf32231c964dfe7dd961b946d197a743bdb75', 'stderr_sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'observed_version': '1.1.0', 'status': 'MATCH', 'tool': 'crucible'}, 'telos': {'command': "node -p 'telos '+JSON.parse(require('fs').readFileSync('package.json','utf8')).version", 'exit_code': 0, 'stdout_first_line': 'telos 0.1.0', 'stdout_sha256': '0b8f3464457976df17a6545e76c55c1bb45d56376761c26195f999f3e5279e36', 'stderr_sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'observed_version': '0.1.0', 'status': 'MATCH', 'tool': 'telos'}}; mismatches=[] |
| Pass 0143 promotes no theorem or natural law. | artifact-review | current_promoted_theorems=[]; current_promoted_natural_laws=[] |
