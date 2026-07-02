# Packet 148: SAIR Stage 1 Judge Repository Adapter

Date: 2026-07-02

Status: `SAIR_STAGE1_JUDGE_REPO_ADAPTER_MATCH`

Purpose: bind the public SAIR Stage 1 judge repository to our proof-packet
lane without making hosted model calls, exporting secrets, or claiming official
competition performance.

```text
repo_head = fe00cf9e9080dba6634882c9316b73d536c4fe60
observed_files = 15
source_hashes = 15
official_model_aliases = 3
local_command_receipts = 4
negative_fixtures = 6
external_model_calls = 0
seal = 2dc78bdbcfd8ec3350cb468ee5820cc3669ed32c2ff266295dd79a6141af8a0a
```

## Source Basis

| Ref |
| --- |
| `https://github.com/SAIRcompetition/equational-theories-stage1-judge` |
| `https://competition.sair.foundation/competitions/mathematics-distillation-challenge-equational-theories-stage1/overview` |
| `https://sair.foundation/` |
| `docs/research/dogfood/schemas/sair-stage1-competition-proof-packet-pass-0137.json` |

## Official Command Surface Observed

The public repository describes prompt rendering, OpenRouter routed model
calls, verdict extraction, and a local smoke test. This pass executes only the
local no-secret surface: repository tests, prompt rendering, verdict parsing,
and the missing-key boundary.

## Model Configuration

| Alias | Model | Provider | Tokens | Temperature | Seed |
| --- | --- | --- | ---: | ---: | --- |
| gemma-4-31b-it | google/gemma-4-31b-it | novita/bf16 | 8192 | 0.0 | 0 |
| gpt-oss-120b | openai/gpt-oss-120b | deepinfra/bf16 | 8192 | 0.0 | 0 |
| llama-3-3-70b-instruct | meta-llama/llama-3.3-70b-instruct | deepinfra/fp8 | 8192 | 0.0 | 0 |

## Local Command Receipts

| Command | Status | Exit |
| --- | --- | ---: |
| judge_cli | MATCH | 0 |
| missing_key_boundary | MATCH | 2 |
| prompt_cli | MATCH | 0 |
| pytest | MATCH | 0 |

## Negative Controls

| Fixture | Observed | Failures |
| --- | --- | --- |
| head_commit_mismatch | REJECTED | head_commit_mismatch |
| missing_source_hashes | REJECTED | missing_observed_source_hashes |
| fallbacks_enabled | REJECTED | fallbacks_not_disabled |
| hidden_external_model_call | REJECTED | external_model_call_present |
| missing_key_boundary_ignored | REJECTED | local_command_receipt_drift |
| leaderboard_claim_promoted | REJECTED | promoted_result_present |

## Boundary

This pass verifies the public judge repository command surface and local no-secret gates. It does not claim official SAIR evaluation, model accuracy, leaderboard standing, theorem proof, market fit, or a promoted natural law.
