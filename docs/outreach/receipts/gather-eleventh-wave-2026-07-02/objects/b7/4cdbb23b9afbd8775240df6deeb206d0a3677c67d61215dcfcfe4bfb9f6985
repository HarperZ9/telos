# Packet 149: SAIR Stage 2 Lean Certificate Preflight

Date: 2026-07-02

Status: `SAIR_STAGE2_LEAN_CERTIFICATE_PREFLIGHT_MATCH_WITH_TOOLCHAIN_GAP`

Purpose: bind the public SAIR Stage 2 Lean certificate repository into the
proof-packet lane while keeping Lean replay fenced until the Lean toolchain is
available.

```text
repo_head = 6805e2323018fbd8a85f41ca09fc33d74d5a02a5
lean_toolchain = leanprover/lean4:v4.30.0-rc2
tracked_files = 187
lean_files = 5
python_files = 41
harness_cases = 66
challenger_cases = 79
marathon_cases = 24
lean_replay_status = UNVERIFIABLE_TOOL_UNAVAILABLE
external_model_calls = 0
seal = cfbd948929bab2dc33efc1ba25c8068649623330fa0f2ea35131e5640db002eb
```

## Source Basis

| Ref |
| --- |
| `https://github.com/SAIRcompetition/equational-theories-lean-stage2` |
| `https://competition.sair.foundation/competitions/mathematics-distillation-challenge-equational-theories-stage2/overview` |
| `https://teorth.github.io/equational_theories/` |
| `docs/research/dogfood/schemas/sair-stage1-judge-repo-adapter-pass-0138.json` |

## Certificate Contract

| Field | Value |
| --- | --- |
| Answer keys | `verdict, code` |
| Statuses | `accepted, unparsed, malformed, incomplete_proof, incorrect` |
| Solver size limit | `500000` bytes |
| Lean code limit | `100000` bytes |
| False-certificate limit | `10000` bytes |

## Local Command Receipts

| Tool | Status | Exit |
| --- | --- | ---: |
| elan | UNVERIFIABLE_TOOL_UNAVAILABLE | 127 |
| lake | UNVERIFIABLE_TOOL_UNAVAILABLE | 127 |
| lean | UNVERIFIABLE_TOOL_UNAVAILABLE | 127 |
| python_compileall | MATCH | 0 |
| run_harness | UNVERIFIABLE_TOOL_UNAVAILABLE | 2 |

## Negative Controls

| Fixture | Observed | Failures |
| --- | --- | --- |
| head_commit_mismatch | REJECTED | head_commit_mismatch |
| missing_source_hashes | REJECTED | missing_observed_source_hashes |
| missing_toolchain_pin | REJECTED | missing_lean_toolchain |
| lean_replay_promoted_without_lean | REJECTED | lean_replay_promoted |
| harness_claim_promoted | REJECTED | unexpected_harness_status |
| leaderboard_claim_promoted | REJECTED | promoted_result_present |

## Boundary

This pass verifies the public Stage 2 repository preflight surface only. It does not replay Lean proofs, accept certificates, claim official evaluation, or promote a theorem or natural law.
