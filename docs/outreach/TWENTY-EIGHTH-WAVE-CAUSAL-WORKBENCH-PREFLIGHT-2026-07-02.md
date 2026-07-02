# Twenty-Eighth Wave: Causal Workbench Preflight

Date: 2026-07-02
Verdict: `CAUSAL_DAG_FIXTURE_MATCH`

## What Changed

This pass promotes the causal-inference lane from source-intake hypothesis into
a small replayable preflight. It does not claim causal discovery, biomedical
validity, or LLM causal-reasoning capability. It proves only that Project Telos
can carry a causal claim with graph assumptions, adjustment-set logic, negative
controls, source receipts, and bounded non-claims in one packet.

The concrete artifact is a deterministic toy DAG about `exercise` and
`health_outcome`. The fixture checks acyclicity, treatment descendants,
backdoor paths, minimal adjustment sets, and invalid adjustment controls. The
expected minimal adjustment set is exactly `age + baseline_health`; no smaller
or descendant-contaminated set is accepted.

## Captured Source Leads

The source ledger stays metadata-only:

- `2407.08029v1`: critical review of LLM causal-reasoning benchmarks.
- `2309.13103v1`: automated causal-inference opportunity finding.
- `2202.02891v1`: tractable-circuit causal inference.
- `2001.04197v4`: LiNGAM causal discovery with latent confounders.
- `2209.03427v1`: time-series causal discovery with latent confounders.
- `2306.08946v2`: bootstrap aggregation and confidence measures for time-series
  causal discovery.
- `2410.19412v3`: robust time-series causal discovery for agent-based model
  validation.
- `1911.07420v1`: graph autoencoder approach to causal structure learning.
- `2006.16189v4`: DOME validation recommendations for biology ML.
- `2303.15563v1`: privacy-preserving healthcare ML challenges.

These rows are source leads and requirements pressure, not proof that the
fixture solves the papers' problems.

## Receipts

- Source ledger:
  `demo/research/causal-workbench-source-receipts.json`
- Fixture CLI:
  `demo/causal-workbench-proof-packet.mjs`
- Fixture test:
  `demo/causal-workbench-proof-packet.test.mjs`
- Fixture output:
  `docs/outreach/receipts/twenty-eighth-wave/causal-workbench-proof-packet-2026-07-02.json`
- Crucible thesis:
  `docs/outreach/receipts/twenty-eighth-wave-causal-workbench-thesis-2026-07-02.json`
- Crucible measurements:
  `docs/outreach/receipts/twenty-eighth-wave-causal-workbench-measurements-2026-07-02.json`
- Crucible run:
  `docs/outreach/receipts/twenty-eighth-wave-causal-workbench-run-2026-07-02.json`
- Crucible report:
  `docs/outreach/receipts/twenty-eighth-wave-causal-workbench-report-2026-07-02.md`
- Learn packet:
  `docs/outreach/receipts/twenty-eighth-wave/causal-workbench.learn-packet.json`
- Learn prooflesson:
  `docs/outreach/receipts/twenty-eighth-wave/learn-causal-workbench/tutor/twenty-eighth-wave-causal-workbench.prooflesson.json`
- Learn reverify witness SHA-256:
  `6e358d9ea652f8e5efee0882ca7046705dc1f1c23421763d9607dd3274b6ad35`

## Claim Boundary

Allowed:

- "The toy DAG fixture emits `CAUSAL_DAG_FIXTURE_MATCH`."
- "The fixture's minimal adjustment set is exactly `age + baseline_health`."
- "The source ledger records arXiv metadata rows and digest seals as source
  leads."
- "The publication copy blocks causal-discovery, LLM causal-reasoning,
  biomedical, and BuildLang/buildc-native claims for this pass."

Blocked:

- "Project Telos solved causal discovery."
- "Project Telos validated LLM causal reasoning."
- "The fixture is a medical or public-health recommendation."
- "The fixture is already BuildLang/buildc-native."
- "The arXiv rows are full-paper proofs inside the repo."

## Megatool Integration

The preflight establishes the product shape for a future causal research
workbench:

1. Gather captures papers, lecture videos, benchmark cards, datasets, and
   metadata as source receipts.
2. Index packages the local graph, variables, code, docs, and source refs into
   a context envelope.
3. Forum routes the claim through statistics, domain, and verification lanes.
4. Crucible rejects claims without graph assumptions, adjustment rationale,
   negative controls, and a replayable check.
5. Learn turns the fixture into exercises about confounding, colliders,
   descendants, and overclaim boundaries.
6. BuildLang/buildc becomes the typed graph and adjustment-check runtime after
   the JavaScript fixture has stabilized.
7. Telos binds the whole run into a proof-carrying research packet.

## Next Tooling Target

The next iteration should promote one of these fixtures:

- A synthetic SCM with a known treatment effect, confounders, collider, and
  randomized encouragement variable.
- A time-series causal fixture with known lagged edges and latent-confounder
  warning labels.
- A benchmark-card parser that refuses LLM causal-reasoning claims unless task
  data, hidden-test hygiene, graph assumptions, and verifier outputs are
  present.

The strongest public demo is the synthetic SCM because it can produce a known
ground truth, falsifiable estimates, and a clear `MATCH` / `DRIFT` boundary.

## Tool Results

Crucible returned `MATCH 3 / DRIFT 0 / UNVERIFIABLE 0` for the bounded causal
preflight claims. Learn generated and reverified the prooflesson as `VERIFIED`,
with witnessed SHA-256
`6e358d9ea652f8e5efee0882ca7046705dc1f1c23421763d9607dd3274b6ad35`.
