# Pass 0137 Ledger - SAIR Stage 1 Competition Proof Packet Fixture

Date: 2026-07-02

## Objective

Move the SAIR intake from source-lead mapping into a runnable local proof-packet adapter. This pass creates a deterministic `CompetitionProofPacket` fixture for SAIR Stage 1-style equation implication tasks, using public source refs, local prompt rendering, verdict parsing, negative controls, and no external model API calls.

This pass does not submit to SAIR, call official models, claim leaderboard performance, prove new mathematics, establish market demand, or promote BuildLang/buildc replacement claims.

## Outputs

| Artifact | Role | SHA-256 |
| --- | --- | --- |
| `schemas/sair-stage1-competition-proof-packet-pass-0137.json` | Main `CompetitionProofPacketFixtureReceipt/v1` artifact. | `1654EEAF8E1636E77D1D90411A11A99F7254B2BF5FBB8BE7929AE9606D3B6C2C` |
| `packets/147-sair-stage1-competition-proof-packet.md` | Human-readable competition proof packet. | `DDB24BA136E6C7ABAA9FBEC9E36859EBC89CB248B527F789C145C37023B0612A` |
| `briefs/147-sair-stage1-competition-proof-packet-brief.md` | Compact strategy brief. | `E315C90DFCD0DC524B29393EA300F3C36E18DF0880BF939F06F6691041AEB3EE` |
| `adversarial/pass-0137-sair-competition-proof-packet-steelman.md` | Failure-mode steelman. | `642157AE3A40630CB0C35C95D1079FDB86FA1CDB6049DA3489F53C7122DC0795` |
| `schemas/tool-receipts-pass-0137.json` | Compact compose/test/validator receipts. | `20D45ECF63CDAA14F4E4B84C8F4F96335A02D235066B3AFF1AC5FB725A2E8D23` |
| `tools/compose_sair_stage1_competition_proof_packet.py` | Deterministic artifact composer. | `F1D1ED0629BF981282C02F905FD2226225CF971F2AE05D44D492CADFE3E63937` |
| `tools/test_sair_stage1_competition_proof_packet.py` | Focused tests. | `DE193AC8022B512FA1B451620E9CD6CFF282C6D9B448B33E84D52622F2ADA852` |
| `tools/validate_pass_0137_sair_stage1_competition_proof_packet.py` | Validator. | `AACA73F66E8E26F0551B58413B3DF275D9C93495DAC8E8D2EB08577B018525B6` |
| `tools/probe_sair_stage1_competition_proof_packet.py` | Packet/brief/steelman/thesis generator. | `78AEF513520D1B3AF4DD0BC3574E7B687F82BFB25955CB0F730269B79F24B96A` |
| `crucible/pass-0137-thesis.json` | Falsifiable thesis claims. | `1DF22D1F27C4903C43A2B5B12C62FB15D919A29B44181CBB13BA6CEC4B0F3C3F` |
| `crucible/pass-0137-measurements.json` | Measurements/evidence for the thesis. | `915EB79EF03954B4C1BA722BD1791D02C7473D526404E64C26D19A01702F40E6` |
| `crucible/pass-0137-report.md` | Crucible report. | `E6476F703AA144EF293E2F3347B926EAB07A216390FCF9A0D24D73A0FE144F2A` |
| `crucible/pass-0137-run.json` | Crucible run record. | `3BA2C21CA4F54D70B20ACD746BF40157DF04BE0E0A4BE003C00EAC18CC702632` |

## Result Snapshot

| Field | Value |
| --- | --- |
| Schema | `CompetitionProofPacketFixtureReceipt/v1` |
| Status | `COMPETITION_PROOF_PACKET_FIXTURE_MATCH` |
| Artifact seal | `57eeba3e2f4048bdec9ec4ac7bcdd6aa67f53885b1a236156da9606ca20a0efb` |
| Source refs | 4 |
| Problem fixtures | 4 |
| Deterministic attempts | 4 |
| Correct parsed verdicts | 4 |
| Incorrect parsed verdicts | 0 |
| External model calls | 0 |
| Parser tests | 5 |
| Negative fixtures rejected | 6 |
| Current promoted results | 0 |

## Source Refs

| Ref | Role |
| --- | --- |
| `https://github.com/SAIRcompetition/equational-theories-stage1-judge` | Public Stage 1 local judge/toolkit source lead. |
| `https://competition.sair.foundation/competitions/mathematics-distillation-challenge-equational-theories-stage1/overview` | Official Stage 1 competition page ref; static Gather body was empty in pass 0136, so it remains a source ref, not body evidence. |
| `https://github.com/teorth/equational_theories` | Upstream Equational Theories project source lead. |
| `docs/research/dogfood/schemas/sair-math-research-infrastructure-source-leads-pass-0136.json` | Prior SAIR source-lead artifact. |

## Local Problem Fixtures

| Problem | Equation 1 | Equation 2 | Expected | Oracle |
| --- | --- | --- | --- | --- |
| `singleton_implies_commutative` | `x = y` | `x * y = y * x` | `TRUE` | human curated fixture |
| `commutative_not_associative` | `x * y = y * x` | `(x * y) * z = x * (y * z)` | `FALSE` | finite counterexample fixture |
| `associative_not_commutative` | `(x * y) * z = x * (y * z)` | `x * y = y * x` | `FALSE` | finite counterexample fixture |
| `left_projection_implies_associative` | `x * y = x` | `(x * y) * z = x * (y * z)` | `TRUE` | human curated fixture |

## Parser Coverage

| Case | Expected |
| --- | --- |
| `boxed_beats_labeled` | boxed final answer overrides earlier labeled answer |
| `last_labeled_wins` | last explicit `VERDICT:` line wins |
| `instruction_pattern_ignored` | prompt instructions are not parsed as answers |
| `bare_last_line` | bare edge line can be parsed only when no stronger marker exists |
| `malformed_unparseable` | malformed output is unparseable |

## Negative Controls

| Fixture | Rejection |
| --- | --- |
| `missing_source_refs` | rejects packets without source refs |
| `unrendered_prompt_placeholder` | rejects prompts with unreplaced placeholders |
| `malformed_verdict` | rejects unparseable/incorrect attempt verdicts |
| `wrong_answer` | rejects incorrect parsed answers |
| `external_model_claim_without_receipt` | rejects hidden external model calls |
| `promoted_theorem_result` | rejects result promotion from a local fixture |

## Crucible

| Field | Value |
| --- | --- |
| Thesis id | `aa7f5d30890b0b37` |
| Thesis seal | `aa7f5d30890b0b379fbadcfae7f1e009fdfeea1347a1228bf055059c4de38449` |
| Claims | 10 |
| `MATCH` | 10 |
| `DRIFT` | 0 |
| `UNVERIFIABLE` | 0 |
| Verdict seal | `154dfe2e127d9425a116b7ee8e83b91446c3513f6d45e8ed5522e7dcffa01f02` |
| Measurement seal | `61e994fd9f981bdf57f426aa446756f4c9867f31253c909d8101dafbfca4fdc4` |
| Assessment seal | `d6981d946f1d7a4b859ebca78a8a17b5e4789b8c0a4df6c5d7838d44ef790bd4` |

Registry after pass 0137:

| Metric | Value |
| --- | ---: |
| Theses | 130 |
| Claims | 1193 |
| Unique claims | 1141 |
| Assessments | 136 |
| Latest assessments | 130 |
| Invalid latest assessments | 0 |
| `MATCH` verdicts | 1193 |
| `DRIFT` verdicts | 0 |
| `UNVERIFIABLE` verdicts | 0 |

## Tooling Gap

Forum routed the exact adapter request with `needs_escalation=true` and no decided lane. That means this proof-packet lane should be added to Forum routing as something like `formal_math_competition_proof_packet`.

## Next Pass Queue

1. Check out or vendor a minimal public Stage 1 judge fixture and run an actual command path instead of a synthetic local fixture.
2. Add `LeanProofReceipt/v1` for Stage 2-style proof certificates.
3. Add a BuildLang/buildc exact modular arithmetic branch using the same packet shape.
4. Add contamination and model provenance fields before any hosted-model attempt is recorded.
5. Add Forum routing support for competition proof packets.
