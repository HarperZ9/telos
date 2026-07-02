# SAIR Stage 2 Lean Certificate Preflight Brief

Date: 2026-07-02

## Decision

Stage 2 is the first clean bridge from prompt/verdict proof packets to
machine-checkable proof receipts. The right product unit is
`LeanProofReceipt/v1`: source refs, problem id, certificate code hash,
toolchain pin, judge result, rejected-token/declaration policy, and replay
status.

## Result

Pass 0139 binds repo HEAD `6805e2323018fbd8a85f41ca09fc33d74d5a02a5`, Lean
toolchain `leanprover/lean4:v4.30.0-rc2`, Python compileability,
manifest counts, and six negative fixtures. Replay remains fenced because
Lean/lake/elan are unavailable on this workstation.

## Next Push

Containerize the Lean toolchain or use WSL, run `scripts/run_harness.py`, then
promote only accepted fixture certificates into `LeanProofReceipt/v1`.
