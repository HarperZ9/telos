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
node demo/flagship-workflow.mjs
```

`room.mjs` is the quickest operator view: it summarizes readiness across
Gather, Crucible, Index, Forum, and Telos, and `node demo/room.mjs --json`
emits the same Project Telos action envelope for hosts and plugins.

`catalog.mjs --summary` prints the same provider-neutral tool catalog as a short
operator map, while plain `catalog.mjs` keeps the full JSON contract for hosts.

`flagship-workflow.mjs` dogfoods the five-tool chain by mapping Telos with
Index, gathering the operator-spine spec with Gather, routing the work through
Forum, checking smoke claims with Crucible, and reconciling the result through
the Telos certificate loop.

`showcase.mjs` starts the OSS Proof Showcase lane. It can rank a fixture-backed
candidate offline and, when the GitHub CLI is available, scout live public
issues without making public changes.
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
