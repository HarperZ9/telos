# Introduction to Telos

Telos is a zero-dependency local workbench for creating, simulating, and replaying AI work. It runs on Node 20 or newer, installs nothing, and gives you three things in one repo:

1. **A five-server MCP surface.** One manifest launches gather, index, forum, crucible, and telos as stdio MCP servers, 69 tools total plus 29 declared auxiliary compatibility tools, with ready-to-paste host config for Codex, Claude, and OpenAI Agents. Every MCP tool has a CLI fallback under `demo/`, so nothing depends on a host being present.
2. **A doctor and proof toolkit.** Nine offline doctors audit CI state, README parity, static accessibility, byte budgets, protocol coverage, and operator discoverability. Four proof lanes (agent-action, research-claim, visual-truth, build) assemble packets whose verifiers recompute every load-bearing claim from embedded materials and can genuinely fail.
3. **A creative and research engine.** Deterministic kernels, ten measurement meters, a renderer selection contract from WebGPU down to static artifacts, and deterministic research preflights for causal inference, embodied sim-to-real, and quantum error correction.

## Why it exists

A model's confidence does not fall when its accuracy does, so a confident mistake reads exactly like a confident truth. Telos exists to put the record outside the model: every command writes a receipt, every check ends in MATCH, DRIFT, or UNVERIFIABLE, and an honest UNVERIFIABLE always beats a polished guess. You do not have to care about that framing to use the tools; it is simply why they are shaped the way they are.

## Core concepts

- **Flagship action envelope.** Every CLI command returns a `project-telos.flagship-action/v1` JSON envelope: tool, version, command, status, inputs, outputs, receipts. Uniform shape means uniform automation.
- **The three verdicts.** MATCH (the claim re-derives from the evidence), DRIFT (it no longer does), UNVERIFIABLE (there is not enough evidence to say). There is deliberately no TRUSTED.
- **Receipts.** A receipt pins what happened: source refs, digests, timestamps, decisions. Receipts are the replay handles that let a reviewer re-check work tomorrow.
- **Proof packets.** A proof packet embeds its own verification materials. `node demo/proof.mjs verify <packet.json>` recomputes the claims from the packet body alone and dispatches to the right lane by schema id. Editing a load-bearing field flips the verdict.
- **Doctors.** A doctor is a read-only auditor that scans local state (workflow files, READMEs, HTML, manifests) and emits a verdict plus routed next actions, without raw payloads or writes.
- **The five flagships.** Gather (source intake), Index (workspace maps and context), Forum (agent routing with a causal ledger), Crucible (claim verification), and Telos (this workbench, which launches and reconciles the other four). They are peers; each stands alone.

## Your first ten minutes

Clone and run the certificate demo:

```bash
git clone https://github.com/HarperZ9/telos.git
cd telos
node demo/run.mjs
```

You will see a 4-D cube rendered, perceived through independent channels, and certified against a criterion the loop did not author (16 vertices, 32 edges). Then the same loop receives an unreadably small render and returns UNVERIFIABLE instead of a pass. That failure is the point: a verifier that cannot fail is not a verifier.

Get oriented:

```bash
node demo/catalog.mjs --summary          # every tool across the five flagships
node demo/server-manifest.mjs --summary  # the 5-server MCP launch map
node demo/status.mjs --summary           # current state envelope
node demo/doctor.mjs --summary           # self-check
```

Run a doctor against this repo:

```bash
node demo/operator-doctor.mjs --summary
```

It checks README quick start, status surface, catalog and MCP parity, CI coverage, and next-action guidance, and returns a verdict.

Build and replay a proof packet:

```bash
node demo/proof.mjs agent-action --demo --json > packet.json
node demo/proof.mjs verify packet.json
```

Expected: `verdict MATCH`, `witness witnessed / MATCH`. Open `packet.json` and change any digest, then verify again to watch it fail honestly.

Finally, open the visual surface at `demo/index.html` in a browser, or start the MCP server for a host with `npm start` and wire it in using the config printed by `node demo/server-manifest.mjs`.

## Where to go next

- [HOW-IT-WORKS.md](HOW-IT-WORKS.md): the verifier loop step by step, including where it stops and why AlphaZero is the right comparison.
- [ARCHITECTURE.md](ARCHITECTURE.md) and [PROJECT-CONNECTION-MAP.md](PROJECT-CONNECTION-MAP.md): system shape and flagship connections.
- [PROOF-LANES.md](PROOF-LANES.md): the four proof-lane contracts and delivery ledger.
- [CURRENT-STATE.md](CURRENT-STATE.md): the live evidence-first state packet.
- [WHO-USES-IT.md](WHO-USES-IT.md): workflows where the record matters.
- [../USAGE.md](../USAGE.md): the compact install, run, MCP, and verify reference.

Telos is at 0.2.0. Interfaces may move between minor versions, npm publishing is operator-gated, and the tests and receipts in the repo are the evidence to trust over any prose summary, including this one.
