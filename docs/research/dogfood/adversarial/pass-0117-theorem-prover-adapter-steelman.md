# Pass 0117 Steelman: Theorem-Prover Adapter

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

The strongest objection is that no local theorem prover executed. Correct. The
pass is an adapter receipt and availability fence, not a Lean/Rocq/Isabelle/Agda
proof result.

The second objection is that Lean-style target strings can look stronger than
they are. Correct. They are marked `NOT_EXECUTED_PROVER_UNAVAILABLE`; the only
positive verification is the finite Python model replay.

Non-promotion statement: This pass verifies finite-model theorem targets only. It does not claim Lean, Rocq, Isabelle, or Agda execution when those tools are unavailable.
