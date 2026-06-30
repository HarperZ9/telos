# Architecture

The mission is one line: give a stateless model durable, verified contact with state and range. This page is the deep version of how that gets built. The README has the pitch. Here are the parts and how they fit.

The short statement. A transformer is a stateless pure function over a token window. It has no symbol table for live bindings, no heap for actual values, no execution cursor for an ordered trace. So you do not fix the model. You build the missing organs around it and put a membrane between the two. You verify the membrane, because you cannot verify the model.

---

## The body and its organs

Four organs make up the body. Each one supplies something a stateless function structurally lacks.

```
                        the model (stateless prior)
                                  ▲   │
                  reads as fact   │   │  asks to act
                                  │   ▼
        ┌─────────────────────────────────────────────────┐
        │                  THE MEMBRANE                    │
        │     read-gate  ───────────────  write-gate       │
        └─────────────────────────────────────────────────┘
             ▲            ▲            ▲            ▲
             │            │            │            │
        ┌────┴───┐   ┌────┴────┐  ┌────┴─────┐  ┌───┴────┐
        │ PERSIS-│   │ PERCEP- │  │  GATED   │  │ CLOCK  │
        │ TENCE  │   │  TION   │  │ ACTUATION│  │        │
        │        │   │         │  │          │  │        │
        │ address│   │ ground  │  │ effects  │  │ as-of  │
        │ -able  │   │ truth → │  │ checked  │  │ stamp  │
        │ store  │   │ bytes   │  │ before   │  │ on     │
        │        │   │         │  │ they land│  │ every  │
        │        │   │         │  │          │  │ fact   │
        └────────┘   └─────────┘  └──────────┘  └────────┘
                                  │
                          ground truth (the world you can pause/replay)
```

**Persistence, an addressable store.** The model recalls, and recall drifts. The store does not. Instead of asking the model to hold a binding in its head across a long window, you give it an address and it reads the value back. The point is the swap: every "reason about it" becomes "read the artifact."

**Perception, faithful and provenance-pinned projections.** Ground truth is not text, so something has to turn it into bytes the model can read. That projection has to be faithful (it shows what is there) and pinned (you can say where it came from and when). A perception the model cannot trace is just another guess.

**Gated actuation, effects checked before they land.** Reading is half the loop. Doing is the other half. An intended effect is not applied directly. It is proposed, checked against invariants, and only then committed, in a way you can undo. Nothing leaves as an effect unless the invariants allow it.

**The clock, every fact stamped as-of-when.** State changes. A fact without a timestamp is a fact you cannot reconcile, because you do not know which version of the world it describes. So every fact carries an `asof`. This is what makes a snapshot meaningful and a replay possible.

---

## The membrane: two gates

The body is a membrane with a read side and a write side. The two gates enforce one rule each.

```
   READ GATE                                WRITE GATE
   ─────────                                ──────────
   nothing enters the model as fact         nothing leaves as an effect
   unless the store witnessed it            unless the invariants allow it

   guess  ──►  [ was this witnessed? ]      intent ──►  [ check invariants ]
                    │      │                              │        │
                  yes      no                           pass      fail
                    │      │                              │        │
                  admit   refuse                        commit    abort
                          as fact                      (reversible)
```

The read gate is the honest part of perception. A claim only enters as *fact* if the store can witness it. Everything else is still just a guess, and is labeled as one.

The write gate is the honest part of action. An effect only lands if it trips no named invariant, and it lands reversibly.

**A real limit, stated plainly.** The membrane controls what the model *sees*, not what it *believes*. Pretraining priors are a second read path you cannot gate. The model can "know" something the store never told it, and act on it. That second path is sealed only at the write gate. So the read gate makes perception honest, and the write gate is where belief is actually contained.

---

## The reconcile and its Certificate

The membrane's core operation is the *reconcile*. It is small and re-runnable on purpose.

```
   perceive an artifact
        │
        ▼
   recover its invariant            (the property that must hold)
        │
        ▼
   check against an external          (a criterion the model did NOT author)
   criterion
        │
        ▼
   emit a Certificate:   MATCH  ·  DRIFT  ·  UNVERIFIABLE
                                              ▲
                                              └─ never "trusted"
```

Three outcomes, and the third is the one that matters.

- **MATCH.** The recovered invariant agrees with the external criterion.
- **DRIFT.** It disagrees. You caught a problem.
- **UNVERIFIABLE.** You could not check it. Maybe the artifact was blank, maybe a perception failed, maybe no criterion applies. This is **fail-closed**: when the loop cannot verify, it says so, instead of returning a guess dressed as a pass.

There is no "trusted" outcome by design. The Certificate carries its own evidence and re-checks from it. You trust it by re-deriving it: **trust by re-derivability, not authority**. If someone hands you a Certificate, you do not take their word. You run the check again.

**A second real limit.** A MATCH means "tripped no *named* failure," not "correct." The loop is only as sound as its declared invariants. Coverage grows the honest way. When a bug escapes, you promote it to a new named check, and the next reconcile catches its kind. Convergence here is asymptotic. Confidently-wrong is reduced, not eliminated.

**And the one that reframes the whole thing.** An *unverified* membrane is worse than no membrane. It takes a falsehood and stamps it with ground-truth authority. It launders the guess. The value is entirely in the *verified*. The instruction is always "add a *verified* membrane," never just "add a membrane."

---

## The adapter contract: the verbs

The architecture above is domain-agnostic. To attach it to a specific world, a renderer, a filesystem, a simulation, a database, you implement a small set of verbs. This is the contract. A world that supplies these can be given a body. A world that cannot is not ready yet. It needs to be pausable and replayable first.

```
fault(ref)                       a reference is touched / demanded; bring it into play

project(cell)                    read a cell as a faithful, pinned projection
   → { value, hash, asof, derivation }
        value       the bytes/observation itself
        hash        content identity, what it is
        asof        the clock stamp, when it was true
        derivation  how it was produced, the trace back to ground truth

stage(slice, salience)           bring a slice of the world into view, ranked by salience

pin(set)                         hold a set fixed so a reconcile sees a stable world

snapshot(asof) → cut             take a coherent cut of state as-of a moment

invalidate(cell)                 mark a cell stale; its old projection no longer witnessed

propose(intent)                  the write-gate sequence:
   → check(invariants)               run the named checks against the intent
   → commit(reversible) | abort      land it reversibly, or refuse, never halfway
```

How the verbs map back to the organs.

| Verb | Organ | What it guarantees |
|---|---|---|
| `project` | perception + clock | a read is faithful, identified (`hash`), stamped (`asof`), and traceable (`derivation`) |
| `fault`, `stage`, `pin` | perception | the right part of the world is in view and held still while you check it |
| `snapshot` | persistence + clock | a coherent as-of cut you can reconcile or replay against |
| `invalidate` | persistence + clock | staleness is explicit, so you never reconcile against a fact the clock has moved past |
| `propose → check → commit\|abort` | gated actuation | effects are checked before they land, and land reversibly or not at all |

`project` returning all four of `{value, hash, asof, derivation}` is what makes the read gate real. A projection without a `hash` cannot be reconciled, because there is no identity to check. Without an `asof` it cannot be reconciled *coherently*, because you do not know which world it describes. Without a `derivation` you cannot re-derive it, and re-derivability is the whole basis of trust here.

---

## The bricks the body is built from

Telos is one body, but the organs are built and proven as separate, real tools. Each face of the loop has a brick that implements it. The flagship is the mission. These are the components it is assembled from, and each one stands on its own.

```
            perceive ──────────► verify ──────────► generate
               │                    │                   │
          THE STUDIO           the reconcile       studio-engine
           surface          (viable-viz / the      (generation
        (perception)         reconcile loop          engine)
                              → Certificate)
               │                    │                   │
               └────────────── built on tools ──────────┘
                                    │
                   render-nd  ·  sense-core  ·  render-sound
                   (project a       (perceive,      (project sound
                    structure        recover the      faithfully)
                    into bytes)      invariant)
```

- **Perception, the Studio surface.** Where ground truth becomes a faithful, pinned projection. This is `project` and `stage` made concrete.
- **Verification, viable-viz and the reconcile.** The live reconcile loop that recovers an invariant, checks it against the external criterion, and emits the Certificate. This is the mechanism above, running. *The demo ships from here.*
- **Generation, studio-engine.** A generation engine exposed over a local REST API. It proposes, and the reconcile checks. Generation without a verifier just agrees with itself, so generation is always paired with the reconcile.

### Studio specimens, overlays, and model visibility

The Studio uses fractals, flow fields, OBJ imports, sound, and geometry as practical subject matter. They are not magic AI interfaces. They are controllable specimens: visual or simulated worlds a person and model can inspect together while Telos records measurements, constants, projections, and verifier outcomes.

The target surface is half editor/renderer and half measurement overlay. A regular local or hosted LLM can attach through the same protocol seams, but the truthful data it receives are the projections and measurements, not hidden access to its private state.

For model-state questions, Telos should expose observable proxies instead of overclaiming: prompt and context spans, retrieved cells, token and tool timelines, verifier verdicts, salience maps over the projected scene, changed constants, budget pressure, and bias or drift probes. Closed models do not reveal their internal activation zones. Open-weight or instrumented models may provide deeper traces, but those traces are evidence fields with provenance and uncertainty, not a claim that the system can see a static mind state.

The shared tools underneath.

- **render-nd** projects a structure (for example an n-dimensional polytope) into bytes you can perceive.
- **sense-core** perceives a projection and recovers the invariant to be checked.
- **render-sound** projects sound faithfully, the same contract in a different modality.

The split is deliberate. Because the organs are independent tools, you can verify each one on its own, and you can compose them into the body without trusting any single black box. That is the same reason the demo vendors the minimal organs directly. The loop should be re-runnable end to end without taking anything on faith.

---

## Where this sits

This is an early, honest instance. The author says as much in public ("still trying to finish the third model and demo"). The architecture is real and the organs are open and tested. The body is not finished. Treat the limits in this document as part of the design, not as caveats bolted on after. The honest floor, UNVERIFIABLE instead of a confident guess, is the feature, not the gap.

See also: [How it works](HOW-IT-WORKS.md) for the reconcile loop step by step, and [Who uses it](WHO-USES-IT.md) for concrete use.
