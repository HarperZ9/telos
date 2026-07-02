# Theorem Packet 045: R_not_quasi_coherent

Date: 2026-07-01

Status: `THEOREM_REPLAY_MATCH`

Theme: amplified ring is not quasi-coherent.

## Command Receipt

```text
command = scripts/verify.sh --no-log R_not_quasi_coherent
exit_code = 0
duration_ms = 42994
result = PASS
transcript = fixtures/pass-0035-theorem-logs/R_not_quasi_coherent.log
transcript_sha256 = 3a4933d41fc3f91fdb1ef7c3c0f71f6dc5cd8be7df2689d748bc9557f4ea613c
```

## Source Refs

```text
frozen_statement = Prob4b/Theorems.lean:66
solution_decl = Prob4b/Solution.lean:61
discharge_gate = Prob4b/Discharge.lean:39
proof_decl = Prob4b/Proofs/Amplify/NotQuasiCoherent.lean:138
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
Prob4b.Solution.R_not_quasi_coherent depends on:
[propext, Classical.choice, Quot.sound]
```

## Non-Promotion Boundary

This packet verifies one theorem-specific replay target inside the local Lean
artifact. It does not assert an axiom-free proof, does not validate all public
claims about `pipeline-math`, and does not promote a natural law.
