# Pass 0031 Adversarial Steelman

Date: 2026-07-01

## Strongest Objection

This pass still does not install Lean or replay a theorem. It only proves that
the verifier script fails earlier than expected.

## Response

Accepted. That is precisely the value of this pass. A proof-packet system must
make early environment failures first-class:

```text
absolute shell runner works, CRLF pin file breaks frozen-hash check, Lean/Lake
not reached, theorem replay not promoted.
```

Without this receipt, an agent might skip directly from "repo has Lean files" to
"formal replay is close" or even "formal replay succeeded." That would be false.

## Operational Risks

| Risk | Required gate |
| --- | --- |
| `bash` not on PATH | Use explicit runner path or amend PATH with a receipt. |
| CRLF pin file paths | Enforce LF checkout, normalize verifier input, or hash Git blobs. |
| no Docker / WSL / Podman | Do not claim container replay. |
| no Elan / Lake / Lean | Do not claim theorem replay, Lake build, or axiom checks. |
| no log capture | Do not claim durable replay evidence. |
| environment mutation | Record action receipt and reversibility before installation. |

## Product Implication

The environment contract is a reusable megatool layer. It should be used before:

- Lean theorem replay;
- BuildLang/buildc compiler proofs;
- GPU/HPC numerical benchmark replay;
- color calibration measurement replay;
- formal security proof replay;
- wet-lab protocol execution.

Current promoted natural laws: none.
