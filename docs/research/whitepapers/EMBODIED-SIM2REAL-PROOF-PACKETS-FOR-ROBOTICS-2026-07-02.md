# Embodied Sim-to-Real Proof Packets for Robotics

Author: Zain Dana Harper
Date: 2026-07-02
Status: working paper, not archive-submitted

## Abstract

Embodied AI and robotics research now spans foundation models, VLA policies,
physical simulators, world models, safety surveys, surgical assistance, soft
robotics, and manufacturing control. The common weakness is not lack of
algorithms; it is claim promotion without portable proof packets that bind
source provenance, robot units, commands, environment state, sensor traces,
tolerances, safety envelopes, and negative controls. This working paper proposes
Project Telos embodied sim-to-real proof packets. The current contribution is a
small deterministic differential-drive fixture that emits
`EMBODIED_SIM2REAL_FIXTURE_MATCH` when the nominal predicted and observed traces
match within tolerance, safety and latency bounds hold, and five negative
controls are rejected. The fixture is not a real robot result, a surgical
result, a foundation-model benchmark, or a BuildLang/buildc-native result. It is
a preflight contract for what stronger embodied robotics claims must contain
before public promotion.

## Problem

Robotics collapses many hard fields into one system: perception, language,
control, causal state, materials, energy, actuation, human safety, clinical
boundaries, manufacturing tolerances, and real-world deployment. A model can
sound fluent about a robot task while silently losing unit contracts, sensor
state, action budgets, obstacle clearance, latency, or the difference between
simulation and deployment.

The Project Telos goal is not another isolated robotics library. The product
shape is proof-carrying robotics research:

- source intake and benchmark cards,
- typed robot and environment state,
- model/tool action records,
- trace comparison,
- safety envelopes,
- negative controls,
- verifier verdicts,
- learning objects, and
- publishable non-claim boundaries.

## Source Intake Boundary

The source ledger for this pass is
`demo/research/embodied-sim2real-source-receipts.json`. It contains arXiv
metadata rows and Gather digest seals from searches over embodied foundation
models, vision-language-action robotics, world models, surgical robotics, and
soft robotics.

The ledger is not a full-paper corpus. It stores source leads and requirements
pressure. It does not promote paper claims, reproduce external experiments, or
quote full text. The rows shape requirements:

- Embodied foundation-model and VLA work pressures benchmark cards, action
  budgets, and contamination checks.
- Simulator and world-model work pressures trace, environment, and sim-to-real
  gap metadata.
- Safety surveys pressure risk, attack, defense, and envelope fields.
- Surgical robotics work pressures clinical non-claim language and domain review
  receipts.
- Soft-robotics work pressures material parameters, deformation traces, and
  environment coupling.

## Fixture

The local fixture is implemented in `demo/embodied-sim2real-proof-packet.mjs`.
It defines a planar differential-drive robot, command sequence, workspace,
obstacle, predicted trace, observed trace, tolerances, and negative controls.

The nominal packet verifies:

- units are declared for time, wheel speed, distance, heading, latency, and
  clearance,
- commands stay within wheel-speed and angular-speed bounds,
- predicted and observed traces stay within mean, max, terminal-position, and
  terminal-heading tolerances,
- workspace and obstacle-clearance checks hold,
- observed latency is within limit, and
- negative controls fail.

The expected result is:

```json
{
  "result": "EMBODIED_SIM2REAL_FIXTURE_MATCH",
  "claim_card": {
    "verdict": "MATCH"
  }
}
```

## Negative Controls

The preflight rejects:

- wrong wheel base,
- swapped wheels,
- centimeters treated as meters,
- unsafe clearance, and
- latency over limit.

These controls matter because robotics claim packets must fail visibly. A trace
that accepts swapped wheels, unit mistakes, or unsafe clearance should not be
allowed to support any public embodied claim.

## Product Shape

The embodied sim-to-real workbench should be a megatool formed by existing
Telos flagships:

| Layer | Responsibility |
| --- | --- |
| Gather | Capture robotics papers, model cards, benchmark cards, protocol docs, datasets, videos, and safety reports as receipts. |
| Index | Package robot morphology, command logs, sensor traces, environment geometry, source refs, and local code into context envelopes. |
| Forum | Route claims through robotics, safety, domain, verification, and publication lanes. |
| Crucible | Turn falsifiable robotics claims plus measurements into `MATCH`, `DRIFT`, or `UNVERIFIABLE`. |
| Learn | Convert packets and failures into exercises about units, kinematics, trace comparison, clearance, latency, and overclaim boundaries. |
| BuildLang/buildc | Provide typed units, kinematics/dynamics kernels, trace schemas, safety envelope checks, and report-runtime receipts. |
| Telos | Bind source, state, model action, environment, verdict, and learning receipts into one packet. |

This should become a family of products:

- Embodied Claim Preflight for robotics papers and internal research notes.
- VLA Benchmark Card Auditor for model and task claims.
- Unit-Safe Robot Runtime for BuildLang/buildc.
- Sim-to-Real Gap Ledger for predicted/observed trace deltas.
- Surgical Robotics Non-Claim Gate for clinical-adjacent language.
- Soft Robotics Deformation Workbench for materials and actuation traces.

## What Already Exists

The current pass adds:

- metadata-only source receipts,
- a replayable differential-drive fixture,
- a local test,
- an emitted proof packet,
- public official/working/outreach copy,
- Crucible thesis and measurement receipts, and
- a Learn prooflesson target.

The broader Telos substrate already includes Gather, Index, Forum, Crucible,
Telos, Learn, browser evidence, model foundry, loop ledger, action receipts,
BuildLang/buildc, causal workbench, hyphal context benchmark, biology/network
intelligence packet, formal replay preflight, color/calibration lanes, and
creative measurement layers.

## What Still Needs Work

The missing work is substantial:

- BuildLang/buildc-native typed-unit execution.
- Higher-fidelity dynamics and contact modeling.
- Manipulation fixtures with object pose, grasp state, and contact events.
- Real dataset adapters with raw-data privacy and licensing boundaries.
- VLA benchmark-card parser and contamination checks.
- Human-in-the-loop safety and escalation receipts.
- Surgical/medical claim gate with primary evidence and domain review.
- Soft-robot material and deformation trace schemas.
- Browser/visual evidence for trajectories and environment state.
- Crucible gates that recompute trajectories from raw commands and sensor logs.

## Public Demo Recommendation

The top public demo should be:

1. A BuildLang/buildc typed differential-drive replay.
2. A command log with units and hashes.
3. A generated predicted trace.
4. A recorded or synthetic observed trace.
5. A safety envelope with workspace and obstacle clearance.
6. A set of negative controls for units, morphology, latency, and safety.
7. A Crucible verdict.
8. A Learn lesson that explains why each negative control fails.

This demo makes the wedge clearer than a prose robotics roadmap: it shows that
the system refuses embodied claims when units, morphology, trace evidence, or
safety boundaries are wrong.

## Claim Boundary

This paper claims:

- Project Telos has a replayable embodied sim-to-real preflight fixture.
- The preflight can carry units, commands, traces, tolerances, safety envelopes,
  negative controls, and non-claims.
- The workbench architecture is a plausible next product shape for
  proof-carrying embodied robotics research.

This paper does not claim:

- real robot safety,
- surgical or medical validity,
- foundation-model robotic-control validation,
- solved sim-to-real transfer,
- full paper digestion,
- BuildLang/buildc-native robotics runtime,
- new robotics theory, or
- deployment readiness.

## Thirty-Day Push

The primary 30-day market and research push should be an Embodied Claim
Preflight pilot for robotics and embodied AI teams:

- Week 1: BuildLang/buildc typed-unit schema for differential-drive commands,
  traces, and tolerances.
- Week 2: manipulation fixture with object pose, contact flags, action budget,
  and negative controls.
- Week 3: VLA benchmark-card parser and safety/non-claim gate.
- Week 4: public demo page, Crucible receipts, Learn lesson, and outreach to
  robotics, embodied AI, medical robotics, manufacturing robotics, and
  simulation-tool builders.

The wedge is not "another robot simulator." The wedge is claim accountability:
source to units to commands to traces to safety envelope to verdict to lesson,
with no promotion path for embodied claims that cannot be replayed.
