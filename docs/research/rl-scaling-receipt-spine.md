# RL Scaling Receipt Spine

## Current Source Check

Checked on 2026-06-29 with fresh GitHub metadata.

- THUDM/slime is described as "an LLM post-training framework for RL Scaling."
- Fresh public metadata observed: 7,077 stars, 1,002 forks, default branch `main`, latest release `v0.3.0` published 2026-05-31, repository updated 2026-06-29.
- README themes observed: Megatron training, SGLang rollout/router integration, custom data generation, reward/verifier outputs, environment/sandbox interaction, delta weight sync, PD disaggregation, router policies, trace viewer, profiling, fault tolerance, reproducibility, and agentic RL examples.

Claim state: `MATCH` for the observed public repository metadata and README themes. Technical superiority claims are `UNVERIFIABLE` until benchmarked against a runnable workload.

## Telos Competitive Target

Telos should not clone a post-training framework as a first move. The stronger target is a receipt spine that can wrap post-training systems, including Slime-like stacks, with durable evidence:

- Every prompt, rollout, verifier result, reward computation, sandbox interaction, dataset mutation, weight sync, eval, checkpoint promotion, and deployment decision gets an `action_intent_id`.
- Admission decisions remain separate from verification verdicts: `allow`, `block`, `escalate`, or `require_review` are not collapsed into `MATCH`, `DRIFT`, or `UNVERIFIABLE`.
- External side effects, including repo writes, benchmark publication, model upload, worker scheduling, and paid compute, produce action receipts that survive trace retention.
- Fault tolerance emits typed failure codes instead of prose-only failures: `binding_failed`, `unjoinable_action`, `verification_unverifiable`, `stale_criterion`, `authority_gap`, `evidence_gap`, `duplicate_idempotency_key`, and `external_request_id_missing`.
- Context packs and loop ledgers keep large-codebase work resumable without trusting inherited confidence from a previous model context.

## Near-Term Build Lanes

1. **Rollout receipt adapter:** Define a minimal post-training run packet with rollout id, policy/checkpoint ref, verifier ref, reward digest, sandbox receipt, and dataset mutation ref.
2. **Verifier/reward split:** Keep reward score, verifier verdict, admission policy, and promotion decision as separate records.
3. **Compute lease receipts:** Treat paid GPU jobs and cluster workers as external writes with idempotency keys, budget refs, queue ids, and terminal status.
4. **Failure corpus:** Build negative fixtures for changed rollout args, missing sandbox evidence, stale reward model, unjoinable checkpoint, duplicate dataset append, and unverifiable benchmark claim.
5. **Interop posture:** Make the spine host-neutral across CLI, MCP, Python SDKs, OpenAI/Anthropic tool hosts, Slime-like training frameworks, and custom labs.

## Why This Can Surpass Slime Shape-Wise

Slime's public center of gravity is high-performance post-training execution. Telos can compete around operational trust: receipts, replayability, model/workflow provenance, human review, cross-tool routing, and negative conformance tests. The bar is not "we trained a bigger model"; the bar is that an enterprise or lab can leave a long-running agentic RL/post-training workflow alone and later know exactly what was proposed, admitted, executed, verified, compensated, or left unverifiable.
