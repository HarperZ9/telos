# How it works

Project Telos has one mission: give a stateless model durable, verified contact with state and range. The verifier loop is the part you can run, and the part the trust rests on. This page walks that loop one step at a time, says plainly where it stops, and explains why AlphaZero is the right comparison rather than a slogan.

The README states the loop in four lines. Here is what each line actually does.

---

## The loop, step by step

```
   ┌─────────────────────────────────────────────────────────────┐
   │                                                             │
   │   1. perceive an artifact                                   │
   │           │                                                 │
   │           ▼                                                 │
   │   2. recover its invariant                                  │
   │           │                                                 │
   │           ▼                                                 │
   │   3. check against an external criterion                    │
   │      (one the model did NOT author)                         │
   │           │                                                 │
   │           ▼                                                 │
   │   4. emit a Certificate:  MATCH · DRIFT · UNVERIFIABLE       │
   │                                                             │
   └─────────────────────────────────────────────────────────────┘
```

### 1. Perceive an artifact

Start from a real thing, not a description of a thing. A render, a file, a frame of a simulation, a stretch of sound. Project it into bytes you can read, and pin where those bytes came from. The output of this step is a projection that carries its own provenance: a content identity (`hash`), an as-of timestamp (`asof`), and a `derivation` back to ground truth.

Why it comes first: if you skip perception and reason about the artifact from memory, you have already lost. The whole method is replacing "reason about it" with "read it."

### 2. Recover its invariant

From the projection, recover the property that has to hold. This is the part you can check. A depth that must stay in `[0,1]`. A count that stays at zero or above. The vertex and edge counts a polytope must have. A buffer that stayed inside its bounds. The invariant is a concrete claim about the artifact that a program can test.

Recover the invariant through more than one channel. When two different perceptions of the artifact recover the same invariant, a single broken perception shows up as disagreement.

### 3. Check against an external criterion

Now compare the recovered invariant to a criterion, and the criterion has to come from somewhere other than the model. This is the load-bearing rule of the whole system.

> **The criterion comes from outside the model.**

If the model both produces the answer and supplies the standard it is graded against, you have built a loop that agrees with itself. Ungrounded self-critique converges to "looks fine to me." The criterion is the rules of the world, a spec, a recomputed value, a second independent measurement. Something that exists whether or not the model likes the answer.

### 4. Emit a Certificate

The check produces one of three results.

```
   MATCH         invariant agrees with the external criterion
   DRIFT         invariant disagrees, a real problem, caught
   UNVERIFIABLE  the check could not be made
```

- **MATCH** is the good case. The section at the end says what a MATCH covers.
- **DRIFT** is the loop doing its job. It found a discrepancy you would otherwise have shipped.
- **UNVERIFIABLE** is the one that makes the rest trustworthy.

The Certificate is a bundle of evidence you can re-run, and the verdict set stops at these three.

---

## Fail-closed

When a check is missing an input, the loop returns **UNVERIFIABLE** and names the missing input.

```
   blank render            ──►  UNVERIFIABLE   (not a fake "looks empty, pass")
   wrong/garbled artifact  ──►  DRIFT or UNVERIFIABLE
   no applicable criterion ──►  UNVERIFIABLE   (not "probably fine")
   perception failed       ──►  UNVERIFIABLE
```

A model on its own sounds equally sure when it is right and when it is wrong. Fail-closed gives you a separate answer for a check that could not run. UNVERIFIABLE comes with its reason, so you know which input to go and get.

The demo makes this concrete on purpose. It runs the loop on a good artifact and prints a CERTIFIED result that re-checks. Then it feeds a blank or wrong render and shows the loop returning UNVERIFIABLE instead of a fake pass. That second half is the point of the demo, not an afterthought.

---

## Trust by re-derivability, not authority

A Certificate carries the evidence to re-run its own check.

```
   ┌──────────────────────────────┐
   │ Certificate                  │
   │   verdict:  MATCH            │
   │   evidence: { the artifact,  │        re-run the check
   │               the invariant, │  ───────────────────────►   same verdict?
   │               the criterion, │                                  │
   │               asof, hash }   │                          yes ◄───┴───► no
   │                              │                           │           │
   └──────────────────────────────┘                        holds       it drifted
                                                                       (you just
                                                                        caught it)
```

The Certificate carries the evidence it was derived from. So you verify it the only honest way: you re-derive it. Re-run the check against the same evidence and see if you get the same verdict. Trust is not granted because something said "trust me." It is earned each time by re-derivation. This is why `project` returns a `derivation` and a `hash`. Without a trace and a content identity, there is nothing to re-derive against.

This also means a Certificate ages honestly. If the world moved (`asof` is in the past) and you re-derive against the current state, you may now get DRIFT. That is correct behavior. It is the clock doing its job, not a flaw.

---

## Why AlphaZero is the right comparison

The shape here is not new. It is exactly what made AlphaZero superhuman, and it is worth being precise about, because the precision is the argument.

AlphaZero is a single neural network, a **stateless prior**: a policy head (a guess at good moves) and a value head (a guess at who is winning). On its own, that network plays well but not superhumanly. It becomes superhuman only when you bolt on **MCTS**, Monte Carlo Tree Search, an external and re-runnable search that reconciles the network's cheap guess against the actual rules of the game before committing to a move.

Line the pieces up against the reconcile.

```
   AlphaZero                          Project Telos
   ─────────                          ─────────────
   value head (compressed state)  ≈   persistence (durable state)
   policy head (the guess)        ≈   the model's cheap guess (the prior)
   MCTS search (re-runnable)      ≈   the reconcile (re-runnable verifier)
   the rules of the game          ≈   the external criterion (not self-authored)
   risk ∝ verified evidence       ≈   trust ∝ what re-derives
```

The correspondences that matter.

- The **value head is durable, compressed state.** That is the same role persistence plays here.
- The **search is the verifier.** It is external to the bare network's forward pass and it can be re-run. So can the reconcile.
- AlphaZero takes **risk in proportion to verified evidence.** It commits to lines the search has actually explored. The reconcile extends trust in proportion to what re-derives.

The grounding for this framing is **Prof. Mihai Nica's *AlphaZero Explained* series** on the 3cycle channel. In that walkthrough, the rollouts are presented as an inspectable "thinking budget." You can look inside the tree and watch the search actually reasoning, rather than taking the network's word for a move. And David Silver, quoted in the series, reduces the whole method to "three steps and literally nothing else." That plainness is the appeal. It is a small, legible loop, not a mystery.

The same verification ethos shows up in **D-Wave's "Quantum Computing for Computational Advantage."** There, a claimed quantum advantage counts once an **adversarial classical baseline** has tried to match it and fallen short, under written rules for what may be claimed. That is the same instinct as the external criterion: the standard comes from someone else, and it is built to catch you.

---

## What a MATCH covers

It is a small, re-runnable verifier that turns "trust me" into "re-derive it," and turns "I am sure" into an honest MATCH, DRIFT, or UNVERIFIABLE.

A MATCH means the artifact passed every *named* check. The loop needs a world you can pause and replay. Its strength comes from the criterion: give it one from outside the model, such as a spec, a recomputed value or a second measurement.

With an outside criterion, a fail-closed check and a re-derivable Certificate, a stateless model gets a way to check its work against the world and to report UNVERIFIABLE when an input is missing. `node demo/run.mjs` shows both outcomes on one cube.

See also: [Architecture](ARCHITECTURE.md) for the organs and verbs, and [Who uses it](WHO-USES-IT.md) for concrete cases.
