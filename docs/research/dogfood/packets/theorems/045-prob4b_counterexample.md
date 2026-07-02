# Theorem Packet 045: prob4b_counterexample

Date: 2026-07-01

Status: `THEOREM_REPLAY_MATCH`

Theme: finite-conductor and not quasi-coherent counterexample pair.

## Command Receipt

```text
command = scripts/verify.sh --no-log prob4b_counterexample
exit_code = 0
duration_ms = 41537
result = PASS
transcript = fixtures/pass-0035-theorem-logs/prob4b_counterexample.log
transcript_sha256 = 4a87e9a1ab38354336fd8cd728b259936a5bfdfc7b8a0bf125240a2bf32ae528
```

## Source Refs

```text
frozen_statement = Prob4b/Theorems.lean:70
solution_decl = Prob4b/Solution.lean:64
discharge_gate = Prob4b/Discharge.lean:42
proof_decl = Prob4b/Proofs/Amplify/Basic.lean:28
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
Prob4b.Solution.prob4b_counterexample depends on:
[propext, Classical.choice, Quot.sound]
```

## Non-Promotion Boundary

This packet verifies one theorem-specific replay target inside the local Lean
artifact. It does not assert an axiom-free proof, does not validate all public
claims about `pipeline-math`, and does not promote a natural law.
