# Project Telos Connection Map

Generated: 2026-06-29

This document is the canonical connection map for the five Project Telos
flagships. It turns the current research packets and live tool dogfood into a
single operating map: Gather senses, Index remembers, Forum routes, Crucible
verifies, and Telos binds the loop into durable work.

## Input Receipts

Local research packets digested with Gather MCP:

| Packet | Method | SHA256 | Digest seal |
| --- | --- | --- | --- |
| `C:\Users\Zain\.codex\attachments\96becef4-d943-468f-a079-ea06ea4ab6a0\pasted-text.txt` | `file-read` | `dc6780ba0e52f00a3e734d15082a539bb2c340a26b9c7048e967ca00c945fdc1` | `43aa038825eea817a3eb362cb8b54056a8a04ac13d00c91746e6749440ab7edd` |
| `C:\Users\Zain\.codex\attachments\773e5613-c40e-44b7-b041-3ee739b0c53c\pasted-text.txt` | `file-read` | `4aa65ce9bdafb9a8a5f3632b13d5085f4d5d56374398200d0c75033901192990` | `dc240ab440dd74e53f121945b52638a1630717f0570cbec38afb9a3b00600414` |

Live dogfood snapshot from the installed MCP surfaces:

| Tool | Version | Status | Role |
| --- | --- | --- | --- |
| Gather | `1.5.0` | `MATCH` | perception and source intake |
| Index | `2.8.0` | `MATCH` | workspace structure and context |
| Forum | `1.12.0` | `MATCH` | orchestration and routing |
| Crucible | `1.1.0` | `MATCH` | verification pressure |
| Telos | source demo | `MATCH` catalog and server manifest | shared room, engine, and contracts |

Dogfood note: the loaded Index MCP status returned the shorter
`2.8.0 workspace atlas, certificates, freshness, benchmarking, and MCP parity`
string while the source checkout already includes
`selection-aware context envelopes`. This is not a product claim failure; it is
the exact host-loaded-server drift the Telos MCP freshness contract is meant to
detect before a host trusts a stale server.

## Constellation

Project Telos is the membrane and growth layer. The sibling tools are not side
projects; they are organs with independent CLI/MCP value and a shared object
spine.

| Project | Role | Sends to Telos | Receives from Telos |
| --- | --- | --- | --- |
| Gather | Sensory intake and provenance. | Source receipts, method, references, content hashes, corpus digests, availability states. | Scope targets, research recipes, source correction trails, freshness demands. |
| Index | Workspace atlas and substrate memory. | Workspace graphs, context envelopes, evidence edges, freshness roots, architecture certificates. | Receipts to store, changed-claim pulses, missing-link signals, expansion handles. |
| Forum | Routing tissue and operator language. | Route decisions, task DAGs, ledgers, budgets, prose-humanization results, replay state. | Context envelopes, action policies, verifier feedback, route decay and reinforcement signals. |
| Crucible | Measurement and verdict gate. | `MATCH`, `DRIFT`, `UNVERIFIABLE`, measurement packets, negative fixtures, cleanroom review bundles. | Claims, theses, evidence packets, replay descriptors, criteria. |
| Telos | Shared room, action membrane, creative engine, model-foundry surface. | Action receipts, loop ledgers, model-foundry packets, creative packets, MCP manifests, promotion records. | Evidence, context, routes, measurements, verdicts, failure codes, promotion decisions. |

The compact positioning is:

```text
Gather senses.
Index remembers.
Forum routes.
Crucible verifies.
Telos turns the loop into durable, replayable, creative, self-improving work.
```

## Shared Object Spine

All five tools should interoperate through a small set of durable objects rather
than bespoke handoffs.

| Object | Primary owner | Consumers | Purpose |
| --- | --- | --- | --- |
| `provenance_receipt` | Gather | Index, Crucible, Telos | Records source, method, reference, timestamp, hash, and derivation. |
| `gather_digest` | Gather | Index, Crucible, Telos | Seals an intake run. |
| `workspace_atlas` | Index | Forum, Telos, site | Maps repos, docs, dependencies, and evidence. |
| `context_envelope` | Index | Forum, Telos, model foundry | Carries low-token context with source-ref expansion handles. |
| `route_ledger` | Forum | Telos, Crucible, Index | Records routing decisions, tasks, results, budgets, and replay state. |
| `action_intent_id` | Telos | All projects | Joins proposed action, admission, execution, evidence, review, and compensation. |
| `action_receipt` | Telos | Forum, Crucible, Index, external systems | Durable operational claim for tool calls, writes, deployments, compute jobs, PRs, and external effects. |
| `measurement_packet` | Crucible, Telos | Crucible, Forum, Telos | Minimal measurable artifact without raw private payloads. |
| `verdict_certificate` | Crucible | All projects | Recheckable `MATCH`, `DRIFT`, or `UNVERIFIABLE` result. |
| `failure_code` | Telos, Crucible, Forum | All projects | Machine-readable negative signal such as `evidence_gap`, `stale_criterion`, `unjoinable_action`, or `duplicate_idempotency_key`. |
| `loop_ledger` | Telos, Forum | Index, Crucible, model foundry | Durable state for long-running research, agent loops, and scheduled bounded runs. |
| `promotion_record` | Telos, Crucible | Model foundry, creative engine, revived tools | Records what moved up, why, against which evidence, and what remains unverifiable. |

## Operating Flows

### Research Intake

```text
Gather source run
  -> provenance receipts
  -> gathered corpus digest
  -> Index map and context handles
  -> Forum route
  -> Crucible claim check
  -> Telos action/verdict receipt
```

This is the default evidence loop. Gather says how the source arrived. Index says
where it fits. Forum says what should happen next. Crucible says what survived
measurement. Telos records what was proposed, admitted, executed, verified, and
remembered.

### Agent Execution

```text
operator intent
  -> Telos action_intent_id
  -> Forum route, budget, and task DAG
  -> Index context envelope
  -> model/tool execution
  -> Telos action receipt
  -> Crucible verdict
  -> Forum ledger and Index memory update
```

The route is part of the artifact, not an invisible planner trace. This is what
lets a fresh-context run resume one bounded action instead of inheriting
unearned confidence.

### Claim Verification

```text
claim or thesis
  -> Gather evidence packet
  -> Index evidence location and freshness roots
  -> Crucible measurement gate
  -> MATCH, DRIFT, or UNVERIFIABLE
  -> Telos durable verdict and next action
```

There is no `TRUSTED` verdict. `UNVERIFIABLE` is an explicit result, not a
polite pass.

### Model Foundry and RL Scaling

```text
rollout or post-training action
  -> rollout receipt
  -> verifier result
  -> reward digest
  -> sandbox receipt
  -> dataset mutation reference
  -> checkpoint or promotion decision
  -> compute lease receipt
  -> Crucible eval gate
```

Telos should wrap Slime-class and custom post-training systems with receipts,
not pretend this repo alone is a frontier-scale training cluster. The
differentiator is durable operational trust: rollout, reward, verifier, compute,
checkpoint, dataset, benchmark, and promotion evidence all join by receipt.

### Creative Engine

```text
scene or media intent
  -> source and asset refs
  -> transform graph
  -> renderer or kernel choice
  -> measurement packet
  -> artifact receipt
  -> Crucible gate
  -> promotion or branch record
```

Creative work is a first-class Telos lane. It includes generative art, retro CGI,
glitch, dithering, pixel sorting, plotter paths, typography, sound, image/video
timelines, shader graphs, mathematical demos, and measurement overlays.

## Distribution Wedges

Do not send the same pitch everywhere. Send the organ that matches the pain.

| Audience | Lead project | Message |
| --- | --- | --- |
| Research intake, newsroom, due diligence, clinical-adjacent review | Gather | "Trust what went in." |
| Coding agents, multi-repo teams, enterprise developer experience | Index | "Map the workspace from evidence, not memory." |
| Agent orchestration, workflow engines, long-running loops | Forum | "Make the route replayable." |
| Standards, observability, security-minded agent tooling | Crucible and Telos | "Telemetry is not a receipt; join spans to durable accountability." |
| Post-training and RL infrastructure | Telos model foundry | "Wrap rollouts, rewards, verifiers, compute, checkpoints, and promotions with receipts." |
| Creative coding, media, film, design systems | Telos creative engine | "Give AI measurable creative tools for the domains where raw text is weakest." |
| Regulated or enterprise external writes | Telos action receipts and Forum | "Record intent, authority, execution, evidence, review, idempotency, and compensation." |

## Adapter Priorities

The next adapter work should make the spine visible inside existing surfaces:

- MCP host profiles for Codex, Claude, OpenAI Agents, OpenAI Apps, IDEs, CLIs,
  TUIs, and application workbenches.
- OpenTelemetry GenAI joins where spans carry timing and telemetry while Telos
  receipts carry durable operational claims.
- Haystack and Mastra style workflow bridges for component/pipeline step
  receipts.
- SmallHarness style session and approval exporters for append-only local
  agent logs.
- Slime-class rollout adapters for post-training receipts around verifier,
  reward, sandbox, dataset, checkpoint, and compute events.
- GitHub PR/write receipts for good-faith open-source patch demonstrations.

The standards position is intentionally narrow:

```text
MCP gives the port.
OpenTelemetry gives the spans.
Telos gives the durable receipt.
Crucible decides what can be verified.
```

## Hyphal Context Protocol

The biology and mycology research lane should become an engineering protocol,
not a scientific overclaim.

| Biological inspiration | Engineering primitive | Primary tools |
| --- | --- | --- |
| Growth toward gradients | Route expansion toward high-value evidence, tasks, and tools | Forum, Index |
| Reinforced useful paths | Route reinforcement, decay, and damage rerouting | Forum |
| Sparse electrical or chemical signals | Low-token pulses that trigger retrieval | Gather, Index |
| Soil or wood as substrate | Durable receipts, graph state, and context envelopes | Index, Telos |
| Injury or pathogen response | Quarantine, negative telemetry, and typed failure codes | Crucible, Telos |
| Symbiosis without central command | Multi-agent local contracts and verifiable exchange | Forum, Telos |

The benchmark should compare a full-context route against a hyphal route:

```text
full-context route:
  send every candidate context item into the model

hyphal route:
  send gradient pulse plus receipt ids
  retrieve evidence only on demand
  verify claims through Crucible
```

Measure tokens spent, relevant evidence recovered, false claims emitted,
`MATCH` / `DRIFT` / `UNVERIFIABLE` rates, resume quality after context loss, and
whether every later claim joins to evidence.

## Promotion Rules

Older tools should move toward flagship status by contract, not nostalgia.

1. Gather the source and README into digests.
2. Index the code, dependencies, and likely host boundary.
3. Forum routes the tool into a flagship lane.
4. Crucible defines the first measurable claim or safety boundary.
5. Telos records a promotion candidate with privacy, I/O, MCP, CLI, test, and
   documentation next actions.

Dormant tools should not become runtime dependencies until they have a source
receipt, a lane, a risk boundary, tests, and a host contract.

## Claim Boundaries

- External ecosystem facts in the attached research packets are source leads
  unless refreshed from primary sources before public claims.
- Shadow-library or inaccessible full text is not accepted as public provenance;
  it can only be recorded as a non-evidentiary lead for lawful cross-reference.
- A trace span can observe an action, but it is not the durable receipt.
- A policy denial is not the same as an unverifiable action binding.
- `UNVERIFIABLE` must stay explicit across docs, ledgers, receipts, and demos.

## Highest-Leverage Next Commits

1. Keep this map linked from the README and current-state docs.
2. Add versioned docs for `action_receipt`, `context_envelope`, and
   `verdict_certificate`.
3. Make `demo/flagship-workflow.mjs` emit one joined artifact across all five
   projects.
4. Add fixtures for MCP failed tool calls, OpenTelemetry joins, GitHub write
   receipts, and external-write compensation.
5. Add a hyphal-context benchmark directory with full-context vs gradient-envelope
   comparison data.
6. Build first adapter demos for GitHub PR receipts and Slime-class rollout
   receipts.
7. Keep the website and five README pages synchronized around the same product
   presentation.
