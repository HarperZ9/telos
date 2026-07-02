# Causal Research Workbench for Proof-Carrying Claims

Author: Zain Dana Harper
Date: 2026-07-02
Status: working paper, not archive-submitted

## Abstract

AI-assisted research needs a stronger boundary between a plausible causal story
and a promoted causal claim. This working paper proposes a Project Telos causal
research workbench where every causal claim carries graph assumptions, source
receipts, adjustment-set logic, negative controls, replayable checks, and
explicit non-claims. The current contribution is intentionally small: a
deterministic toy DAG fixture that emits `CAUSAL_DAG_FIXTURE_MATCH` when the
minimal adjustment set is exactly `age + baseline_health` and several invalid
adjustments are rejected. The result is not a causal-discovery result, a
biomedical result, an LLM benchmark result, or a BuildLang/buildc-native result.
It is a preflight contract for what stronger causal research packets must
contain before they are allowed into public claims.

## Problem

The operator goal is broader than one tool: source intake, model reasoning,
workspace context, verification, education, and runtime receipts should combine
into megatools that can advance real research. Causality is a useful pressure
test because it punishes vague automation. A causal claim cannot be verified by
confidence, summary fluency, or source volume alone. It needs a declared
treatment, outcome, population, graph or identification strategy, assumptions,
adjustment rationale, negative controls, uncertainty, and a replay path.

The current market and research landscape contains strong fragments:

- benchmark papers that test whether LLMs reason causally,
- causal-discovery algorithms and time-series variants,
- biomedical ML reporting standards,
- privacy-preserving healthcare ML requirements,
- workflow tools that can run data pipelines, and
- agent tools that can trace model actions.

The gap hypothesis is that these fragments rarely bind source provenance,
workspace state, graph assumptions, model/tool action receipts, verification
verdicts, and educational replay into one proof-carrying packet.

## Source Intake Boundary

The source ledger for this pass is
`demo/research/causal-workbench-source-receipts.json`. It contains arXiv
metadata rows and Gather digest seals from causal inference, causal discovery,
LLM causal reasoning, biology ML validation, and healthcare ML privacy searches.

The ledger is not a full-paper corpus. It stores source leads and requirements
pressure. It does not promote paper claims, reproduce external experiments, or
quote full text. The papers shape requirements:

- LLM causal-reasoning work pressures the benchmark-card and hidden-test
  hygiene requirements.
- Causal-discovery work pressures the learned-graph versus assumed-graph
  separation.
- Time-series causal-discovery work pressures lag, latent-confounder, and
  stability metadata.
- Biology and healthcare ML reporting work pressures domain validation, privacy
  boundaries, and downstream clinical non-claim language.

## Fixture

The local fixture is implemented in `demo/causal-workbench-proof-packet.mjs`.
It defines a toy DAG:

- `age -> exercise`
- `age -> health_outcome`
- `baseline_health -> exercise`
- `baseline_health -> health_outcome`
- `encouragement -> exercise`
- `exercise -> health_outcome`
- `exercise -> biomarker`
- `health_outcome -> biomarker`

The treatment is `exercise`; the outcome is `health_outcome`; observed variables
are `age`, `baseline_health`, `biomarker`, and `encouragement`.

The fixture verifies:

- the graph is acyclic,
- treatment descendants are detected,
- backdoor paths are enumerated,
- adjustment candidates do not include treatment descendants,
- active backdoor paths are blocked, and
- minimal valid adjustment sets are derived by enumeration.

The expected result is:

```json
{
  "result": "CAUSAL_DAG_FIXTURE_MATCH",
  "minimal_adjustment_sets": [["age", "baseline_health"]]
}
```

## Negative Controls

The preflight rejects these adjustment choices:

- `[]`: both confounding paths stay active.
- `["age"]`: the baseline-health backdoor remains active.
- `["baseline_health"]`: the age backdoor remains active.
- `["encouragement"]`: the confounding paths remain active.
- `["biomarker"]`: the variable is a treatment descendant in the fixture.

These controls matter because a causal workbench should fail visibly. A demo
that only shows a passing path can become a claim-promotion machine. The
negative controls force the packet to demonstrate what it will not accept.

## Product Shape

The causal workbench should be a megatool formed by existing Telos flagships:

| Layer | Responsibility |
| --- | --- |
| Gather | Capture paper, video, benchmark, data, and protocol receipts without raw-payload overreach. |
| Index | Package graph files, code, local docs, source refs, and run state into context envelopes. |
| Forum | Route claims through statistics, domain, verification, and publication lanes. |
| Crucible | Turn falsifiable causal claims and measurements into `MATCH`, `DRIFT`, or `UNVERIFIABLE`. |
| Learn | Convert proofs and failures into exercises, labs, and domain learning packets. |
| BuildLang/buildc | Provide the typed DAG, SCM, tensor, numerical, and report-runtime layer after the fixture stabilizes. |
| Telos | Bind the source, graph, action, verdict, and learning receipts into one packet. |

This should not become a monolithic app. It should be a family of products:

- Causal Claim Preflight for papers and internal research memos.
- Benchmark Card Auditor for LLM causal-reasoning claims.
- Synthetic SCM Lab for known-ground-truth causal estimation.
- Biomedical Non-Claim Gate for clinical-adjacent research.
- Time-Series Causal Lab for robotics, medicine, economics, climate, and
  infrastructure systems.
- BuildLang Causal Runtime for typed graph and estimator receipts.

## What Already Exists

The current pass adds:

- metadata-only source receipts,
- a replayable causal DAG fixture,
- a local test,
- an emitted proof packet,
- public official/working/outreach copy,
- Crucible thesis and measurement receipts, and
- a Learn prooflesson target.

The broader Telos substrate already includes Gather, Index, Forum, Crucible,
Telos, Learn, browser evidence, model foundry, loop ledger, action receipts,
display/color lanes, creative measurement layers, and BuildLang/buildc as a
strategic language/runtime pillar.

## What Still Needs Work

The missing work is substantial:

- BuildLang/buildc-native typed DAG execution.
- Synthetic SCM data generation with known average treatment effect.
- Estimator receipts for adjustment, weighting, matching, and front-door tests.
- Countergraph comparison and sensitivity analysis.
- Benchmark-card parser for LLM causal-reasoning tasks.
- Dataset cards and privacy gates for biomedical use.
- Domain-specific causal interfaces for biology, robotics, medicine, finance,
  security, climate, and infrastructure.
- Visual graph editor with source-linked assumptions.
- Crucible gates that recompute estimates, not just fixture structure.
- Learn labs that teach why each negative control fails.

## Public Demo Recommendation

The top public demo should be:

1. A synthetic SCM with known ground truth.
2. A DAG receipt with treatment, outcome, variables, and assumptions.
3. A generated dataset and checksum.
4. A set of candidate adjustment strategies.
5. A verifier that accepts only strategies that recover the known effect within
   tolerance.
6. A negative-control strategy that fails.
7. A Learn lesson that explains the failure.
8. A BuildLang/buildc target plan for the same graph.

This demo would make the wedge clearer than the current toy DAG: not only
"identify adjustment sets," but "recover a causal quantity under declared
assumptions and reject overclaims."

## Claim Boundary

This paper claims:

- Project Telos has a replayable toy causal-claim preflight.
- The preflight can carry explicit assumptions, checks, negative controls, and
  non-claims.
- The workbench architecture is a plausible next product shape for
  proof-carrying causal research.

This paper does not claim:

- causal discovery,
- medical recommendation,
- LLM causal-reasoning validation,
- solved benchmark results,
- full paper digestion,
- BuildLang/buildc-native causal runtime,
- new causal theory, or
- real-world causal effect estimation.

## Thirty-Day Push

The primary 30-day market and research push should be a Causal Claim Preflight
pilot for AI-assisted research teams:

- Week 1: synthetic SCM fixture and BuildLang/buildc DAG schema draft.
- Week 2: benchmark-card parser for LLM causal-reasoning claims.
- Week 3: biology or healthcare reporting card with privacy and non-claim
  gates.
- Week 4: public demo page, Crucible receipts, Learn lesson, and outreach to
  causal ML, AI4Science, and research-tool builders.

The wedge is not "another causal library." The wedge is claim accountability:
source to graph to code to verdict to lesson, with no promotion path for claims
that cannot be replayed.
