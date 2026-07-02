# Theorem Packet 045: triple_defect_survives

Date: 2026-07-01

Status: `THEOREM_REPLAY_MATCH`

Theme: triple-intersection defect survives idealization.

## Command Receipt

```text
command = scripts/verify.sh --no-log triple_defect_survives
exit_code = 0
duration_ms = 44064
result = PASS
transcript = fixtures/pass-0035-theorem-logs/triple_defect_survives.log
transcript_sha256 = 9c55fec0e9d5eecc4b12a8b357e91cbf8c29a81bdb25de9b5ec30f48d16e13e6
```

## Source Refs

```text
frozen_statement = Prob4b/Theorems.lean:55
solution_decl = Prob4b/Solution.lean:52
discharge_gate = Prob4b/Discharge.lean:35
proof_decl = Prob4b/Proofs/Idealization/Basic.lean:88
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
Prob4b.Solution.triple_defect_survives depends on:
[propext, Classical.choice, Quot.sound]
```

## Non-Promotion Boundary

This packet verifies one theorem-specific replay target inside the local Lean
artifact. It does not assert an axiom-free proof, does not validate all public
claims about `pipeline-math`, and does not promote a natural law.
