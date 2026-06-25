# Who uses it

The mission is to give a stateless model durable, verified contact with state and range. This page is about who that mission helps, in concrete terms. Each case is a short before and after: what handing work to a model looks like today, and what it looks like with the reconcile loop in place. No aspirational sweep. Just the situations where an external, re-runnable check actually changes the outcome.

The common thread. A stateless model is a strong guesser with no way to check itself, and its confidence does not fall when its accuracy does. These are the moments where that gap costs you, and where a Certificate closes it.

---

## 1. Engineers handing real work to an AI agent, who want receipts

You let an agent make a change across a codebase or a dataset. The work is plausible. The question is whether to trust it.

**Before.** The agent reports: "Done. Refactored the module, updated the call sites, tests should pass." You either re-do the audit yourself (so what did the agent save you?) or you take the summary on faith. The summary is the agent's own account of its own work. The model is grading itself. If it is confidently wrong, the report reads exactly like a correct one.

**After.** The agent hands back a Certificate alongside the diff. The reconcile perceived the actual before and after state, recovered the invariants that had to hold (the call sites still resolve, the count of references matches, the named checks did not trip), and checked them against a criterion the agent did not author. You get **MATCH**, **DRIFT**, or **UNVERIFIABLE**, and the evidence to re-derive any of them. You are no longer auditing the agent's *prose*. You are re-running its *check*.

> What changes: trust by reputation becomes trust by re-derivation. "It says it is fine" becomes "I re-ran the check and it is fine, or it is not, and here is exactly where."

---

## 2. ML practitioners building agent loops, who want a grounded verifier step

You are building a loop where a model proposes, critiques, and revises. You have noticed the critique step does not help as much as it should.

**Before.** The loop is generate, then self-critique, then revise. With no external criterion, the critic is the same model judging its own output, so it drifts toward "looks good to me." Self-agreement is dressed up as verification. The loop can iterate forever and still be confidently wrong, because nothing outside the model ever pushes back.

**After.** You replace ungrounded self-critique with a **reconcile** as the verifier step: prior, then external check. The proposal is checked against a criterion the model did not author: recomputed values, the rules of the world, a second independent measurement, a spec. The loop only advances on a MATCH it can re-derive. A DRIFT sends it back with a concrete discrepancy, and an UNVERIFIABLE stops it from advancing on something it could not actually check.

> What changes: the verifier step stops being a mirror. Generation paired with an external, re-runnable check is the AlphaZero shape, where the network guesses and the search verifies, instead of a model nodding at itself.

---

## 3. Anyone who needs an honest "I cannot verify this"

You ask a model something where being wrong is expensive, and the honest answer might be "unknown."

**Before.** The model answers confidently either way. There is no signal that separates "I checked this and it holds" from "I produced a fluent guess." A fabrication and a fact arrive in the same tone. You find out which it was later, usually at the worst time.

**After.** The loop is fail-closed. When it cannot verify (the artifact was blank, a perception failed, no criterion applied) it returns **UNVERIFIABLE** instead of a guess wearing the costume of an answer. That is a *useful* output. It tells you exactly where the ground is missing, so you can go get it. An UNVERIFIABLE you can act on beats a confident fabrication you cannot.

> What changes: "I am sure" splits into "verified," "drifted," and "I genuinely cannot check this." The third one is the one bare models never give you.

---

## A worked example: the polytope demo

The runnable demo is the smallest honest version of all three cases at once.

It renders a structure, an n-dimensional polytope, perceives it two independent ways, recovers the invariant, checks it against the criterion, and emits a Certificate.

```
   good render   ──► perceive ×2 ──► recover invariant ──► check ──► CERTIFIED
                                                                     (re-checks)

   blank/wrong   ──► perceive ×2 ──► recover invariant ──► check ──► UNVERIFIABLE
   render                                                            (NOT a fake pass)
```

The first path shows the loop certifying real work with evidence you can re-derive. The second path, the blank or wrong render returning UNVERIFIABLE instead of a false CERTIFIED, is the part that proves the loop is honest. A system that only ever says "looks good" has not demonstrated anything. One that refuses to certify what it cannot check has.

---

## Where it fits, and where it does not

It fits when:

- the work produces an **artifact you can perceive** (a render, a file, a diff, a frame, a value, a sound), not just a claim;
- there is an **external criterion** available: rules, a spec, a recomputed value, an independent measurement;
- the world can be **paused or replayed**, so the reconcile sees a stable state to check.

It does not fit when there is nothing external to check against (then you have only got the model grading itself again), or when the system is real-time and cannot be stepped or recorded. And one warning that belongs in front of every use case: an **unverified** membrane is worse than none. It stamps a guess with ground-truth authority. The value is entirely in the *verified*. Wire the check to a real, external criterion, or do not wire it at all.

This is an early, working instance, used honestly. The cases above are where it earns its place: not by being more confident than a bare model, but by being checkable, and by admitting, out loud, when it cannot be.

See also: [How it works](HOW-IT-WORKS.md) for the loop, and [Architecture](ARCHITECTURE.md) for the organs and the adapter verbs.
