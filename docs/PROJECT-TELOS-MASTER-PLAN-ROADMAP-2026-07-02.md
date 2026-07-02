# Project Telos Master Plan Roadmap Appendix

Date: 2026-07-02

Parent plan: `docs/PROJECT-TELOS-MASTER-PLAN-2026-07-02.md`

## Product Surfaces

### 1. Frontier Proof OS

User-visible promise: turn serious AI work into a packet that can be inspected tomorrow.

First command:

```bash
telos proof research --source <url-or-store> --context <path> --lane <lane>
```

Outputs:

- Gather source receipts.
- Index context envelope.
- Forum route.
- Telos action receipt.
- Crucible verifier result.
- Emet witness when public consistency matters.
- Packet summary and promotion status.

### 2. Research Foundry

User-visible promise: turn papers, preprints, college databases, datasets, repositories, and claims into proof-packet queues.

First lanes:

- Formal theorem packet.
- AI4Science claim-to-experiment packet.
- Mixed-source protein packet.
- Robotics benchmark packet.
- Climate uncertainty packet.
- Materials property packet.
- Institution claim graph.

### 3. Agent Action Proof

User-visible promise: audit-grade receipts for agent work, not just traces.

Minimum fields:

- Objective.
- Source refs.
- Context refs.
- Route.
- Authority/admission.
- Tool call.
- Side-effect class.
- Output digest.
- Verifier.
- Compensation path.
- Final status.

### 4. Build Scientific Runtime

User-visible promise: scientific programs that are born with receipts.

First demos:

- Constraint encoding proof packet.
- Hamiltonian runtime branch receipt.
- Reaction invariant checker.
- Display/color measurement packet.
- BuildLang `check --receipt` bridge into Telos.

### 5. Learning Forge

User-visible promise: study and model improvement loops that prove what was learned honestly.

First demos:

- Proof-packet-to-lesson generator.
- Misconception extraction from failed proof attempts.
- Model explanation faithfulness lab.
- Research operator mastery dashboard.

### 6. Emet Witness

User-visible promise: independent source/view consistency across generated artifacts and code.

First demos:

- Packet schema conformance across Python, Node, and Rust.
- README-to-demo consistency witness.
- Generated plan-to-implementation consistency witness.

## 30-Day Plan

1. Freeze research expansion except for selected demo evidence.
2. Ship `telos proof` as a local CLI over one lane.
3. Choose the first lane: agent action proof packet or research proof packet.
4. Build a proof-packet schema package shared by Telos, Crucible, Learn, BuildLang/buildc, and Emet.
5. Convert pass 0149-0151 source federation into an executable adapter registry.
6. Add Emet witness output to one generated packet.
7. Add Learn lesson generation from one proof packet.
8. Add BuildLang/buildc receipt ingestion into one Telos packet.
9. Publish one polished public demo page and one technical whitepaper.

## 60-Day Plan

1. Build three proof lanes: agent action, research source, scientific runtime.
2. Store packet data in a local SQLite or DuckDB graph.
3. Add packet search and lineage views.
4. Add negative-fixture regression tests per lane.
5. Add model-foundry post-training data export from verified packets.
6. Run a small local model experiment on packet classification, route selection, or claim demotion.
7. Publish buyer briefs for research labs, AI infra teams, and scientific compute teams.

## 90-Day Plan

1. Demonstrate a closed loop: source intake -> model plan -> admitted action -> verifier -> learning update -> Emet witness.
2. Produce the first model eval suite where success requires proof-packet correctness, not only answer accuracy.
3. Add BuildLang/buildc scientific kernels for one numerical or optimization domain.
4. Add a public research foundry demo using arXiv/bioRxiv/PubMed/college repositories.
5. Package Telos as a local-first developer product with hosted optional extensions.

## 180-Day Plan

1. Train or fine-tune specialist proof-native models on verified packet data.
2. Add domain foundries for formal math, biology, robotics/control, climate, materials, and economics.
3. Build hosted collaboration around packet review, verifier runs, and learning labs.
4. Turn BuildLang/buildc into the default receipt-bearing runtime for selected kernels.
5. Position Emet as the public consistency witness for published claims.

## Public Demos To Ship

### Agent Action Proof Packet

Flow: source -> context -> route -> admitted action -> verifier -> Emet witness.

Why it matters: this is the clearest market wedge against agent observability tools. The demo should show that traces are not enough; action proof needs source refs, workspace state, authority, side-effect classification, and verifier status.

### Research Proof Packet

Flow: archive/preprint/college source -> claim extraction -> negative fixture -> Crucible verdict.

Why it matters: this turns the source federation into a concrete research lab product. The demo should use a bounded claim, not a grand theorem or clinical result.

### BuildLang Scientific Runtime Packet

Flow: source code -> buildc receipt -> numerical run -> measurement -> verifier.

Why it matters: this makes BuildLang/buildc a strategic pillar without claiming it is already a finished Julia replacement. The pitch is accountable scientific compute.

### Learn Proof Lesson

Flow: proof packet -> lesson path -> retrieval practice -> mastery receipt.

Why it matters: this turns research into learning and model-improvement data. It also differentiates Learn from answer-giving AI tutors.

### Visual Truth Packet

Flow: color/display/rendering result -> measurement layer -> proof packet.

Why it matters: visual truth is tangible, demonstrable, and underrepresented in AI proof tooling.

### Emet Source/View Witness

Flow: generated artifact -> source view -> Python/Node/Rust conformance -> MATCH/DRIFT/UNVERIFIABLE.

Why it matters: public trust improves when the consistency witness is external to the generator.

## Operating Rules

- No source count becomes coverage.
- No metadata hit becomes truth.
- No preprint becomes peer review.
- No benchmark result becomes product capability without environment and metric receipts.
- No BuildLang backend is promoted beyond verified maturity.
- No model answer is promoted without source and verifier status.
- No `UNVERIFIABLE` result is rewritten as a failure.
- No public claim ships without Emet or equivalent witness where source/view consistency matters.

## Success Metrics

Technical:

- Packet creation latency.
- Source replay success rate.
- Context freshness pass rate.
- Forum route confidence and escalation quality.
- Crucible MATCH/DRIFT/UNVERIFIABLE distribution.
- Negative-fixture catch rate.
- Emet consistency pass rate.
- BuildLang receipt ingestion pass rate.

Model:

- Claim demotion accuracy.
- Tool-use admission accuracy.
- Citation/source grounding accuracy.
- Verifier-aware planning accuracy.
- Failed-proof recovery quality.
- Learning receipt fidelity.

Product:

- Public demo completion rate.
- Buyer packet inspection feedback.
- Proof packet reuse across lanes.
- Adapter contribution count.
- Time from source to verified packet.
- Number of high-quality training examples generated from verified work.

## Delivery Order

1. Agent Action Proof Packet.
2. Research Proof Packet.
3. BuildLang Scientific Runtime Packet.
4. Learn Proof Lesson.
5. Emet Source/View Witness.
6. Visual Truth Packet.

This order keeps the first release close to Telos' strongest local evidence while moving directly toward the proof-native model-building stack.
