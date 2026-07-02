# Proof Lanes Progress Ledger

This is a factual progress ledger for the operator master-plan proof-lane
roadmap. The roadmap lists six delivery-order demos. This document records, for
each one, where it is shipped, the CLI command where applicable, the packet
schema id, the proof-surface export contract, and the honesty guarantee the lane
enforces.

A proof lane is not a trace. A trace explains what a run did. A proof lane
produces a receipt that justifies a claim: it recomputes every load-bearing
value from the packet's own embedded materials, derives the verdict from the
recomputed checks rather than trusting an asserted one, and floors an empty
check set to `UNVERIFIABLE` instead of a silent `MATCH`. A canned `MATCH` is
structurally impossible in every shipped lane.

## Status vocabulary

- `shipped-in-telos-proof`: the lane assembles, verifies, and exports from
  `demo/proof.mjs` in this repository, with its own contract, verifier, tests in
  CI, and a read-only MCP tool.
- `shipped-elsewhere`: the lane ships in a sibling flagship repository.
- `embedded`: the capability is present as a stage inside the telos lanes rather
  than as a standalone lane.

## Delivery-order ledger

| Order | Demo | Status | Telos CLI | Schema id | proof-surface export |
| --- | --- | --- | --- | --- | --- |
| 1 | agent-action | shipped-in-telos-proof | `node demo/proof.mjs agent-action --demo` | `project-telos.proof-packet/v1` | `agent-action-proof-packet/v0` |
| 2 | research | shipped-in-telos-proof | `node demo/proof.mjs research --demo` | `project-telos.research-proof-packet/v1` | `research-claim-proof-packet/v0` |
| 3 | buildlang-runtime | shipped-in-telos-proof | `node demo/proof.mjs build --demo` | `project-telos.build-proof-packet/v1` | `conservation-proof-packet/v0` |
| 4 | learn-lesson | shipped-elsewhere | not applicable | consumes any proof packet version | not applicable |
| 5 | emet-witness | embedded | not applicable | not applicable | `proof-surface-bundle/v0` (emet adapter) |
| 6 | visual-truth | shipped-in-telos-proof | `node demo/proof.mjs visual --demo` | `project-telos.visual-proof-packet/v1` | `visual-measurement-proof-packet/v0` |

The telos lanes share one CLI. `node demo/proof.mjs verify <packet.json|->` and
`node demo/proof.mjs export <packet.json|->` dispatch by the packet's own schema
id, so each lane is re-checked and exported by its own verifier and exporter and
an unknown schema is an error rather than a silent pass.

## Lane detail

### 1. Agent-action (shipped-in-telos-proof)

- MCP tool: `telos.proof`.
- Contract: `demo/integrations/proof-packet-conventions.json`.
- Module: `demo/proof.mjs` with `demo/proof-core.mjs`, `demo/proof-witness.mjs`,
  and `demo/proof-export.mjs`.
- The packet joins source refs, context refs, route, admission, side effects,
  and output digests by reference, composing the existing action-receipt,
  context-envelope, and loop-ledger contracts rather than copying their payloads.
- Honesty guarantee: the verifier derives `MATCH`, `DRIFT`, or `UNVERIFIABLE`
  from named checks (required fields, state-model legality, packet-hash and
  artifact-digest recomputation, admission-before-execution ordering, and
  compensation presence for external writes). An optional Emet coherence witness
  stage records `unavailable` honestly when no implementation is reachable and
  never fabricates a verdict. A canned verdict cannot win.

### 2. Research-claim (shipped-in-telos-proof)

- MCP tool: `telos.proof.research`.
- Contract: `demo/integrations/research-proof-packet-conventions.json`.
- Module: `demo/proof-research.mjs`.
- Honesty guarantee: the verifier recomputes each source and negative-fixture
  digest from the embedded body, requires a negative control that the claim
  survived, and refuses to assert a reproduction-gated promotion rung
  (`PROMOTED_DISCOVERY`, `LAW_CANDIDATE`) inside a single packet. An empty check
  set floors to `UNVERIFIABLE`.

### 3. Build scientific-runtime (buildlang-runtime, shipped-in-telos-proof)

- MCP tool: `telos.proof.build`.
- Contract: `demo/integrations/build-proof-packet-conventions.json`.
- Module: `demo/proof-build.mjs`.
- This realizes the BuildLang scientific-runtime demo without requiring the
  buildlang toolchain: the buildc receipt is carried as a fixture with the source
  program text and its SHA-256 digest, an effect and policy summary, and an
  honest backend label.
- Honesty guarantee: the verifier recomputes a conserved-quantity invariant
  (mean total energy) and a conservation drift (maximum relative energy drift)
  from the run's own embedded samples with stdlib math, and checks the claimed
  values within tolerances bounded to a small fraction of each metric's physical
  range so an oversized author-declared tolerance is itself `DRIFT`. A required
  negative fixture must break the invariant; a control that does not break it has
  no discriminating power and is `DRIFT`. An empty run recomputes nothing and is
  `UNVERIFIABLE`, never a silent `MATCH`.

### 4. Learn-lesson (shipped-elsewhere)

- Home: the `learn` repository, `src/tutor/prooflesson.mjs` and
  `src/tutor/prooflessonverify.mjs`.
- The lesson lane is a teaching layer over proof packets, not a new packet
  contract. It reads a proof packet (of any version), generates a
  predict-then-check lesson keyed to the packet's claim, sources, and verdict,
  and binds the lesson to the packet in an append-only ledger. It defines no
  telos CLI command and no telos schema id; it consumes the same receipts the
  telos lanes produce.

### 5. Emet-witness (embedded)

- Emet is the coherence witness. In telos it is embedded as the optional witness
  stage of the agent-action lane: over a clean packet the stage witnesses the
  packet's own canonical bytes against their re-derived form and records
  `COHERENT`, and when no Emet implementation is reachable it records
  `unavailable` rather than a fabricated verdict.
- Emet also ships a standalone proof-surface bundle witness in its own
  repository: `emet/adapters/proof_surface_receipt.py` re-derives each file in a
  `proof-surface-bundle/v0` manifest to witness the bundle, rather than trusting
  a recorded digest. That adapter is the emet-witness demo; the telos lanes reuse
  the same coherence discipline as an embedded stage.

### 6. Visual-truth (shipped-in-telos-proof)

- MCP tool: `telos.proof.visual`.
- Contract: `demo/integrations/visual-proof-packet-conventions.json`.
- Module: `demo/proof-visual.mjs`.
- Honesty guarantee: the verifier recomputes every relative-luminance and CIE76
  delta-E measurement from the artifact's own embedded sRGB samples with stdlib
  color math, rejects a non-read-only packet, rejects a physical-calibration
  claim over a read-only surface, and bounds each measurement tolerance to a
  per-method ceiling so an oversized tolerance cannot launder a false value into
  `MATCH`. An empty measurement set floors to `UNVERIFIABLE`.

## Shared invariants across the telos lanes

- Every load-bearing claim (a source digest, an invariant value, a measurement)
  is recomputed from the packet's embedded materials. A claim with no
  recomputable basis is an `UNVERIFIABLE` gap named by its JSON path, never a
  silent pass.
- The verdict is folded from the checks alone. An embedded verdict that
  disagrees with the derived one is itself a failure at the derived severity, so
  an embedded `MATCH` over tampered materials stays `DRIFT` and an embedded
  `MATCH` over an incomplete packet stays `UNVERIFIABLE`.
- The canonical hash scope excludes wall-clock time, so the same fixture yields a
  byte-identical canonical packet and the same SHA-256 across runs.
- The proof-surface export derives its `decision_summary` from the overall
  verdict: `MATCH` approves, `DRIFT` blocks, `UNVERIFIABLE` escalates. The
  exporter never imports proof-surface at runtime; each lane freezes the
  proof-surface field list as a telos test fixture instead.
