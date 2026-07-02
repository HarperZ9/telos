# Pass 0035 Steelman: Theorem-Specific Proof Packets

Date: 2026-07-01

Status: `LOCAL_STEELMAN_RECORDED`

## Thesis Under Pressure

Pass 0035 claims the pass 0034 replay result has been decomposed into ten
theorem-specific proof packets. Each target-specific run used
`scripts/verify.sh --no-log <theorem>`, exited 0, and recorded a transcript
hash, source refs, axiom boundary, and statement-gate result.

## Strongest Objections

1. The theorem packets are generated from project verifier output.

Correct. They are not independent mathematical reviews. They are durable,
per-theorem replay receipts for the local Lean artifact.

2. The transcripts are short and summarized by the verifier.

Correct. The transcripts are complete for the verifier command output, but they
do not include all Lean elaboration internals. A stronger next pass should bind
raw command, environment, and selected source-file hashes per theorem.

3. The axiom boundary still matters.

Correct. Every theorem packet carries `[propext, Classical.choice, Quot.sound]`.
Any downstream claim that the proofs are axiom-free should be rejected.

4. Source refs are line-based and could drift if the temp clone changes.

Correct. They are tied to the previously recorded commit and local replay
state. A production proof packet should use Git blob IDs plus line spans.

5. Per-theorem runs still re-run project-wide gates.

Correct. This is acceptable for verification but inefficient for product UX.
The product should cache project-wide gates and attach theorem-scoped checks as
children of a replay session.

6. Public novelty is still not established.

Correct. Pass 0035 says the Lean artifact replayed, not that the result is a
historically new theorem, a solved open problem by an LLM, or a market-validated
claim.

7. The statement gate semantics still deserve independent inspection.

Correct. The pass records that `Prob4b.Discharge` and `Prob4b.Solution` compile.
It does not manually prove the gate design is the only possible interpretation.

8. Transcript hashes are durable, but temp runtime state is not.

Correct. The repo now stores the transcript fixtures, but future replay still
needs pinned runtime setup and cache provisioning.

9. The proof-packet generator itself could contain mapping mistakes.

Correct. The validator checks presence, hashes, status fields, and source refs;
the next pass should cross-check refs against `rg` output or Git blob parsing.

10. This is one domain: Lean formal math.

Correct. The product lesson should be generalized next to BuildLang/buildc,
color calibration, scientific compute, or agent-action receipts.

## Product Implication

Pass 0035 is a direct prototype for proof-centered megatools: broad verifier
success becomes per-claim packets, and every packet carries source, transcript,
axioms, gates, and non-promotion boundaries.

## Verdict

Strong evidence for per-theorem replay receipts. Still bounded to one local
Lean artifact and one verifier design.
