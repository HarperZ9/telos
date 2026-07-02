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

From the projection, recover the property that has to hold. This is the part you can actually check. A depth that must stay in `[0,1]`. A count that cannot go negative. A vertex and edge relationship a polytope must satisfy. A buffer that did not overflow. The invariant is a concrete, checkable claim about the artifact, not a feeling about whether it "looks right."

Recovering the invariant independently matters. If you can perceive the artifact two different ways and recover the same invariant from each, a single broken perception cannot quietly pass.

### 3. Check against an external criterion

Now compare the recovered invariant to a criterion, and the criterion has to come from somewhere other than the model. This is the load-bearing rule of the whole system.

> **The criterion is external. The model did not author it.**

If the model both produces the answer and supplies the standard it is graded against, you have built a loop that agrees with itself. Ungrounded self-critique converges to "looks fine to me." The criterion is the rules of the world, a spec, a recomputed value, a second independent measurement. Something that exists whether or not the model likes the answer.

### 4. Emit a Certificate

The check produces one of three results, and never a fourth.

```
   MATCH         invariant agrees with the external criterion
   DRIFT         invariant disagrees, a real problem, caught
   UNVERIFIABLE  the check could not be made
```

- **MATCH** is the good case, with the honest caveat below.
- **DRIFT** is the loop doing its job. It found a discrepancy you would otherwise have shipped.
- **UNVERIFIABLE** is the one that makes the rest trustworthy.

There is deliberately no `TRUSTED`. The Certificate is not an authority telling you it is fine. It is a bundle of evidence you can re-run.

---

## Fail-closed

When the loop cannot verify something, it returns **UNVERIFIABLE**, not a guess.

```
   blank render            ──►  UNVERIFIABLE   (not a fake "looks empty, pass")
   wrong/garbled artifact  ──►  DRIFT or UNVERIFIABLE
   no applicable criterion ──►  UNVERIFIABLE   (not "probably fine")
   perception failed       ──►  UNVERIFIABLE
```

This is the opposite of how a stateless model behaves on its own. The expensive failure of a bare model is that its confidence does not drop when its accuracy does. Confidently wrong reads exactly like confidently right. Fail-closed inverts that. The absence of a check produces an explicit "I cannot verify this," which is a useful, actionable output. An honest UNVERIFIABLE tells you exactly where to look. A confident fabrication tells you nothing and costs you later.

The demo makes this concrete on purpose. It runs the loop on a good artifact and prints a CERTIFIED result that re-checks. Then it feeds a blank or wrong render and shows the loop returning UNVERIFIABLE instead of a fake pass. That second half is the point of the demo, not an afterthought.

---

## Trust by re-derivability, not authority

A Certificate is only worth something if you do not have to trust it.

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

The same verification ethos shows up in **D-Wave's "Quantum Computing for Computational Advantage."** There, a claimed quantum advantage is treated as credible only when an **adversarial classical baseline** certifies it. You do not get to claim the win until a strong, skeptical, independent method has tried and failed to match you, under explicit anti-overclaiming rules. That is the same instinct as the external criterion. The standard has to be one you did not author and that is actively trying to catch you.

---

## What this loop is and is not

It **is** a small, re-runnable verifier that turns "trust me" into "re-derive it," and turns "I am sure" into an honest MATCH, DRIFT, or UNVERIFIABLE.

It **is not** a correctness oracle. A MATCH means "tripped no *named* failure," not "correct." It needs a world you can pause and replay, not real-time control. And it is only as honest as its criteria are external. Point it at a criterion the model authored and you have rebuilt the self-agreeing loop it was meant to replace.

Used as intended, with an external criterion, fail-closed, and re-derivable, it gives a stateless guesser something it has never had on its own: a way to check itself against the world, and to admit when it cannot.

See also: [Architecture](ARCHITECTURE.md) for the organs and verbs, and [Who uses it](WHO-USES-IT.md) for concrete cases.
