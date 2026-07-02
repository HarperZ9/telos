# Theorem Packet 045: M_annihilator

Date: 2026-07-01

Status: `THEOREM_REPLAY_MATCH`

Theme: module preserves annihilators.

## Command Receipt

```text
command = scripts/verify.sh --no-log M_annihilator
exit_code = 0
duration_ms = 47766
result = PASS
transcript = fixtures/pass-0035-theorem-logs/M_annihilator.log
transcript_sha256 = ff2351b9df9fe1787c628c424c531f91c00b23219402e75bcc196a4db78bd813
```

## Source Refs

```text
frozen_statement = Prob4b/Theorems.lean:43
solution_decl = Prob4b/Solution.lean:40
discharge_gate = Prob4b/Discharge.lean:31
proof_decl = Prob4b/Proofs/Module/Basic.lean:1494
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
Prob4b.Solution.M_annihilator depends on:
[propext, Classical.choice, Quot.sound]
```

## Non-Promotion Boundary

This packet verifies one theorem-specific replay target inside the local Lean
artifact. It does not assert an axiom-free proof, does not validate all public
claims about `pipeline-math`, and does not promote a natural law.
