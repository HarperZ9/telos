# Packet 147: SAIR Stage 1 Competition Proof Packet Fixture

Date: 2026-07-02

Status: `COMPETITION_PROOF_PACKET_FIXTURE_MATCH`

Purpose: turn the SAIR Stage 1-style math-distillation source lead into a
local, replayable `CompetitionProofPacket` fixture. This packet does not call
external model APIs, does not submit to SAIR, does not claim leaderboard
performance, and does not prove new mathematics.

```text
source_refs = 4
problem_fixtures = 4
attempts = 4
correct_attempts = 4
external_model_calls = 0
parser_tests = 5
negative_fixtures = 6
seal = 57eeba3e2f4048bdec9ec4ac7bcdd6aa67f53885b1a236156da9606ca20a0efb
```

## Source Basis

| Ref |
| --- |
| `https://github.com/SAIRcompetition/equational-theories-stage1-judge` |
| `https://competition.sair.foundation/competitions/mathematics-distillation-challenge-equational-theories-stage1/overview` |
| `https://github.com/teorth/equational_theories` |
| `docs/research/dogfood/schemas/sair-math-research-infrastructure-source-leads-pass-0136.json` |

## Problem Fixtures

| Problem | Equation 1 | Equation 2 | Expected | Oracle |
| --- | --- | --- | --- | --- |
| singleton_implies_commutative | x = y | x * y = y * x | TRUE | human_curated_fixture |
| commutative_not_associative | x * y = y * x | (x * y) * z = x * (y * z) | FALSE | finite_counterexample_fixture |
| associative_not_commutative | (x * y) * z = x * (y * z) | x * y = y * x | FALSE | finite_counterexample_fixture |
| left_projection_implies_associative | x * y = x | (x * y) * z = x * (y * z) | TRUE | human_curated_fixture |

## Attempt Receipts

| Problem | Parsed | Expected | Correct | Runner |
| --- | --- | --- | --- | --- |
| singleton_implies_commutative | TRUE | TRUE | True | deterministic_local_fixture_no_model_call |
| commutative_not_associative | FALSE | FALSE | True | deterministic_local_fixture_no_model_call |
| associative_not_commutative | FALSE | FALSE | True | deterministic_local_fixture_no_model_call |
| left_projection_implies_associative | TRUE | TRUE | True | deterministic_local_fixture_no_model_call |

## Negative Controls

| Fixture | Observed | Failures |
| --- | --- | --- |
| missing_source_refs | REJECTED | missing_source_refs |
| unrendered_prompt_placeholder | REJECTED | unrendered_prompt_placeholder |
| malformed_verdict | REJECTED | incorrect_attempt_verdict |
| wrong_answer | REJECTED | incorrect_attempt_verdict |
| external_model_claim_without_receipt | REJECTED | external_model_call_present |
| promoted_theorem_result | REJECTED | promoted_result_present |

## Boundary

This packet verifies local fixture mechanics only. It does not submit to SAIR, call official models, claim leaderboard performance, or prove new mathematics.
