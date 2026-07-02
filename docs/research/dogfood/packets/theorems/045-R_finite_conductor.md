# Theorem Packet 045: R_finite_conductor

Date: 2026-07-01

Status: `THEOREM_REPLAY_MATCH`

Theme: amplified ring is finite-conductor.

## Command Receipt

```text
command = scripts/verify.sh --no-log R_finite_conductor
exit_code = 0
duration_ms = 42717
result = PASS
transcript = fixtures/pass-0035-theorem-logs/R_finite_conductor.log
transcript_sha256 = 4acb957e018da4cec85bd212266f8b2eb624a78a6b2217d5c8f918ef5b5a0643
```

## Source Refs

```text
frozen_statement = Prob4b/Theorems.lean:61
solution_decl = Prob4b/Solution.lean:58
discharge_gate = Prob4b/Discharge.lean:38
proof_decl = Prob4b/Proofs/Amplify/FiniteConductor.lean:676
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
Prob4b.Solution.R_finite_conductor depends on:
[propext, Classical.choice, Quot.sound]
```

## Non-Promotion Boundary

This packet verifies one theorem-specific replay target inside the local Lean
artifact. It does not assert an axiom-free proof, does not validate all public
claims about `pipeline-math`, and does not promote a natural law.
