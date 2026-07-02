# Demo: the reconcile -> Certificate loop

For the polished visual walkthrough, open [`index.html`](index.html). The command-line
proof remains [`run.mjs`](run.mjs), and the visual page is a static companion for the
same certificate loop.

Project Telos exists to give a stateless model durable, verified contact with state and range. This folder is the smallest runnable piece of that: a system that **perceives something, checks what it perceived against a truth it did not make up, and reports MATCH, DRIFT, or "I cannot verify this," never just "trusted."**

It is the core mechanism behind the larger project, isolated down to one concrete example you can run in a few seconds.

## What it shows

The subject is a **4-dimensional cube** (a tesseract). Its true structure is known in advance: **16 vertices, 32 edges**. That known truth is the **criterion**. It comes from the geometry, not from the loop, and the perception step is never allowed to read it.

The loop does three things.

1. **Perceive.** It renders the cube and reads it back two independent ways: a geometric reader (counts distinct projected vertices) and a pixel reader (finds bright blobs in the rasterized image). Each produces its own estimate of (vertices, edges). Neither looks at the criterion.

2. **Check against the criterion.** A regulator compares both estimates to the known truth. It only reports **CERTIFIED** when *every* channel both agrees and matches (unanimity, fail-closed). If a view is degenerate, the loop **amplifies**: it nudges the rotation, adds another viewing angle, fuses in a sound channel, cheapest fix first, and checks again.

3. **Emit a Certificate that carries its own evidence.** The Certificate can `recheck()` itself. It re-derives the verdict from the stored criterion and the stored recovered values, with no access to the live run. You trust the re-derivation, not the loop's word.

The three possible outcomes.

- **MATCH (CERTIFIED).** Perception agreed with the criterion across every channel.
- **DRIFT.** Perception and criterion disagree in a measured way.
- **UNVERIFIABLE.** The system could not establish a match it can stand behind, so it says so instead of guessing.

## How to run

```
node demo/run.mjs
```

Operator-spine scripts emit the same JSON action envelope used by the other
flagships:

```
node demo/status.mjs
node demo/doctor.mjs
node demo/room.mjs
node demo/catalog.mjs --summary
node demo/server-manifest.mjs --summary
node demo/admission-telemetry.mjs
node demo/context-envelope.mjs
node demo/action-receipt.mjs
node demo/loop-ledger.mjs
node demo/flagship-workflow.mjs
```

`room.mjs` is the quickest operator view: it summarizes readiness across
Gather, Crucible, Index, Forum, and Telos, and `node demo/room.mjs --json`
emits the same Project Telos action envelope for hosts and plugins.

`catalog.mjs --summary` prints the same provider-neutral tool catalog as a short
operator map, while plain `catalog.mjs` keeps the full JSON contract for hosts.

`server-manifest.mjs --summary` prints the five-server MCP launch map. Plain
`server-manifest.mjs` returns the full manifest; `--codex` emits TOML and
`--claude-json` emits a JSON block for stdio MCP hosts.

`admission-telemetry.mjs` returns the admission decision and verification
verdict convention: `allow/block/escalate/require_review` stays separate from
`match/drift/unverifiable`, and evidence is represented by hashes or redacted
references instead of raw prompts or tool arguments.

`context-envelope.mjs`, `action-receipt.mjs`, and `loop-ledger.mjs` are the
Analytical Engine layer for agent work: pack large workspaces into readable
source references, record action receipts, and persist loop state so a fresh
context can pick one next action with evidence instead of inheriting confidence.

`browser-evidence.mjs --summary` returns the browser evidence kernel contract:
automated browsing and work-actuation page state is reduced to redacted refs,
digests, side-effect classes, and `MATCH` / `DRIFT` / `UNVERIFIABLE` verdicts
so Index and Forum can feed council/review paths without raw browser payloads.

`flagship-workflow.mjs` dogfoods the five-tool chain by mapping Telos with
Index, gathering the operator-spine spec with Gather, routing the work through
Forum, checking smoke claims with Crucible, and reconciling the result through
the Telos certificate loop.

`showcase.mjs` starts the OSS Proof Showcase lane. It can rank a fixture-backed
candidate offline and, when the GitHub CLI is available, scout live public
issues without making public changes.

`proof.mjs` is the agent-action proof lane. `node demo/proof.mjs agent-action
--demo [--out <dir>] [--json]` assembles the fixture proof packet, runs the
verifier, and attempts the optional Emet witness stage. `node demo/proof.mjs
verify <packet.json|-> [--json]` replays required-field validation, state-model
legality, packet-hash and artifact-digest recomputation, admission ordering,
compensation presence, and the witness stage, then prints `MATCH`, `DRIFT`, or
`UNVERIFIABLE`. It exits `0` on `MATCH`, `1` on `DRIFT`, and `2` on
`UNVERIFIABLE`, mirroring the Emet exit codes. A tampered packet drifts with the
actual deltas, a packet missing evidence is unverifiable with the missing item
named, and a canned `MATCH` embedded in a packet can never win because the
verdict is always derived from the checks. `node demo/proof.mjs export
<packet.json|->` prints the proof-surface `agent-action-proof-packet/v0` shaped
object for cross-tool interchange.

`proof.mjs` also carries three sibling lanes. `node demo/proof.mjs research --demo
[--out <dir>] [--json]` assembles the research-claim proof packet, whose verifier
recomputes each source and negative-fixture digest from the embedded body,
requires a negative control that the claim survived, and refuses to assert a
reproduction-gated promotion rung inside one packet. `node demo/proof.mjs visual
--demo [--out <dir>] [--json]` assembles the visual-truth proof packet, whose
verifier recomputes each relative-luminance and CIE76 delta-E measurement from
the artifact's own embedded sRGB samples, rejects a non-read-only packet, and
rejects a physical-calibration overclaim. `node demo/proof.mjs build --demo
[--out <dir>] [--json]` assembles the build scientific-runtime proof packet, whose
verifier recomputes a conserved-quantity invariant (mean total energy) and a
conservation drift (maximum relative energy drift) from the run's own embedded
samples with stdlib math, bounds each tolerance to a small fraction of the
metric's physical range so an oversized author-declared tolerance is itself
`DRIFT`, and requires a negative fixture that must break the invariant.
`node demo/proof.mjs verify <packet.json|->` and `node demo/proof.mjs export
<packet.json|->` dispatch by the packet's schema id, so each lane is re-checked
and exported by its own verifier and exporter. The research lane exports to
`research-claim-proof-packet/v0`, the visual lane to
`visual-measurement-proof-packet/v0`, and the build lane to
`conservation-proof-packet/v0`. As with the agent-action lane, a tampered packet
drifts with the actual deltas, a missing recomputable basis is unverifiable with
the item named, and a canned `MATCH` can never win.

`research/youtube-learning-forge-receipts.json` records the current Learning
Forge seed intake: eight video metadata/transcript receipts and two channel-list
receipts captured through Gather and yt-dlp. It intentionally stores hashes,
counts, titles, and refs only; raw transcripts stay in the local `.telos/`
corpus and are ignored by git.
- **Node >= 18.** (Tested on Node 25.)
- **Zero external dependencies.** No `npm install`. The organs the loop needs (`render-nd`, `render-sound`, `sense-core`, `viable-viz`) are vendored into this folder as plain ESM `.mjs` files. Nothing is fetched, nothing is built.

The script runs two cases and exits `0` only if both come out as expected.

## What to look for

The demo runs the **same true cube twice**.

**Run A, an honest render.** The pixel channel has enough resolution. You will watch the loop fail to certify on the first few checks, amplify (GENERIC -> VIEW2 -> VIEW3 -> SOUND), and then reach **CERTIFIED** once the channels agree. `recheck()` is `true`.

**Run B, a deliberately broken render (8x8 pixels).** Eight pixels across is far too coarse to resolve 16 vertices. The geometric channel still reads the scene correctly, but the pixel channel cannot. It over-counts noise (you will see it report dozens of "vertices"). The two channels disagree, so unanimity never holds. After exhausting every amplification, the loop returns **UNVERIFIABLE**.

**That UNVERIFIABLE is the point.** The geometric channel was right the whole time. A system optimized to look successful would have leaned on it and reported a pass. This one does not. When it cannot verify a result across its checks, it reports that it cannot, rather than handing back a confident answer it cannot support. The honest floor, "I cannot verify this," is a feature, not a failure.

## Files

- `run.mjs`, the entry point. Both runs, with comments explaining each step.
- `viable-viz/`, the reconcile loop, the regulator, the subject, and the Certificate.
- `render-nd/`, `render-sound/`, `sense-core/`, the render-and-perceive organs the loop depends on. Vendored unchanged so this folder runs on its own.

## Honest limits

- "CERTIFIED" means **"tripped no named failure check,"** not "correct in every possible sense." The guarantee is only as wide as the checks. Every escaped error should become a new check.
- The criterion here is a known combinatorial fact about a polytope. The mechanism generalizes to any subject where you can state a criterion the perceiver did not author and re-derive the verdict from evidence.
- This is one small, honest instance of the idea, not a finished system.
