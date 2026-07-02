# Packet 002: Formal Math and Theorem Proving

Status: `SOURCE_LEAD` plus `HYPOTHESIS`

## Question

Can Telos produce research proof packets around theorem-proving attempts, including failures, without pretending an AI proof attempt is a proof?

## Source Anchors

- LeanDojo: https://leandojo.org/leandojo.html
- Lean: https://lean-lang.org/
- DeepSeek-Prover-V2: https://arxiv.org/abs/2504.21801
- pipeline-math: https://github.com/Pengbinghui/pipeline-math

## Working Thesis

The useful object is not just a generated proof. It is a packet containing source problem, informal reasoning, formal statement, proof attempt, checker output, failure trace, and next decomposition.

Confidence: moderate-high for packet usefulness; low for any claim of solving frontier math without a checker.

## Initial Proof Target

Start with a small theorem where failure is still useful:

```text
For natural numbers n, n + 0 = n.
```

This is intentionally trivial. The first dogfood step should prove the packet pipeline, not the theorem frontier.

## Adversarial Steelman

Objection: pipeline-math and LeanDojo already expose prover-verifier loops. Telos may add ceremony without improving proof search.

Response: valid. Telos should not claim better theorem proving until it measures better proof search. The first differentiator is evidence packaging across sources, workspace state, route decisions, attempts, checker results, and reviewer report.

## Next Proof Attempt

1. Detect local Lean availability.
2. If available, run a tiny Lean proof and capture output.
3. If unavailable, emit `UNVERIFIABLE` with exact missing tool evidence.
4. Convert the result into a proof-surface packet.

