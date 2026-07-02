# Theorem Packet 045: problem4b_false

Date: 2026-07-01

Status: `THEOREM_REPLAY_MATCH`

Theme: headline existential refutation inside the Lean artifact.

## Command Receipt

```text
command = scripts/verify.sh --no-log problem4b_false
exit_code = 0
duration_ms = 43815
result = PASS
transcript = fixtures/pass-0035-theorem-logs/problem4b_false.log
transcript_sha256 = 8a8f2466bf7958d5c9fbb0bf0768c0ba29e53f4bfa5399e4f1fd6eea5db6e7b9
```

## Source Refs

```text
frozen_statement = Prob4b/Theorems.lean:75
solution_decl = Prob4b/Solution.lean:69
discharge_gate = Prob4b/Discharge.lean:43
proof_decl = Prob4b/Proofs/Amplify/Basic.lean:35
```

## Gates

```text
frozen_sha_pins = PASS
banned_keywords = PASS
lake_build = PASS
axiom_check = PASS
statement_gate_discharge = PASS
statement_gate_solution = PASS
```

## Axiom Boundary

```text
Prob4b.Solution.problem4b_false depends on:
[propext, Classical.choice, Quot.sound]
```

## Non-Promotion Boundary

This packet verifies one theorem-specific replay target inside the local Lean
artifact. It does not assert an axiom-free proof, does not validate all public
claims about `pipeline-math`, and does not promote a natural law.
