# Who uses it

The mission is to give a stateless model durable, verified contact with state and range. This page is about who that mission helps, in concrete terms. Each case is a short before and after: what handing work to a model looks like today, and what it looks like with the reconcile loop in place. No aspirational sweep. Just the situations where an external, re-runnable check actually changes the outcome.

The common thread. A stateless model is a strong guesser that sounds equally sure when right and when wrong. These are the moments where that costs you, and where a Certificate gives you a check to re-run.

---

## 1. Engineers handing real work to an AI agent, who want receipts

You let an agent make a change across a codebase or a dataset. The work is plausible. The question is whether to trust it.

**Before.** The agent reports: "Done. Refactored the module, updated the call sites, tests should pass." You either re-do the audit yourself (so what did the agent save you?) or you take the summary on faith. The summary is the agent's own account of its own work. The model is grading itself. If it is confidently wrong, the report reads exactly like a correct one.

**After.** The agent hands back a Certificate alongside the diff. The reconcile perceived the actual before and after state, recovered the invariants that had to hold (the call sites still resolve, the count of references matches, the named checks stay clear), and checked them against a criterion from outside the agent. You get **MATCH**, **DRIFT**, or **UNVERIFIABLE**, and the evidence to re-derive any of them. You re-run the agent's *check* in place of reading its *prose*.

> What changes: you trust what you re-derived. "It says it is fine" becomes "I re-ran the check, and here is the result and where it points."

---

## 2. ML practitioners building agent loops, who want a grounded verifier step

You are building a loop where a model proposes, critiques, and revises, and the critique step is helping less than you hoped.

**Before.** The loop is generate, then self-critique, then revise. The critic is the same model judging its own output, so it drifts toward "looks good to me." The loop can iterate for a long time and stay confidently wrong, because every judgment comes from inside the model.

**After.** You replace ungrounded self-critique with a **reconcile** as the verifier step: prior, then external check. The proposal is checked against a criterion from outside the model: recomputed values, the rules of the world, a second independent measurement, a spec. The loop advances on a MATCH it can re-derive. A DRIFT sends it back with a concrete discrepancy, and an UNVERIFIABLE holds it in place until the missing input arrives.

> What changes: the verifier step stops being a mirror. Generation paired with an external, re-runnable check is the AlphaZero shape, where the network guesses and the search verifies, instead of a model nodding at itself.

---

## 3. Anyone who needs an honest "I cannot verify this"

You ask a model something where being wrong is expensive, and the honest answer might be "unknown."

**Before.** The model answers confidently either way. There is no signal that separates "I checked this and it holds" from "I produced a fluent guess." A fabrication and a fact arrive in the same tone. You find out which it was later, usually at the worst time.

**After.** The loop is fail-closed. When a check cannot run (the artifact was blank, a perception failed, no criterion applied) it returns **UNVERIFIABLE** with the reason. That tells you which input is missing, so you can go get it.

> What changes: "I am sure" splits into "verified," "drifted," and "this check is missing an input." The third answer is the one this loop adds.

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

The first path shows the loop certifying real work with evidence you can re-derive. The second path shows it returning UNVERIFIABLE on an 8 by 8 pixel render. Run `node demo/run.mjs` and the summary prints both:

```
  RUN A (honest render)  : CERTIFIED      recheck=true
  RUN B (broken render)  : UNVERIFIABLE   recheck=true
```

---

## Where it fits

It fits when:

- the work produces an **artifact you can perceive**: a render, a file, a diff, a frame, a value, a sound;
- there is an **external criterion** available: rules, a spec, a recomputed value, an independent measurement;
- the world can be **paused or replayed**, so the reconcile sees a stable state to check.

It needs an outside criterion and a system you can step or record. Wire the check to a real criterion such as a spec, a recomputed value or a second measurement; a criterion the model wrote turns the check back into self-grading.

This is an early, working instance. The cases above are where it helps: each verdict can be checked, and a blocked check names the input it needs.

See also: [How it works](HOW-IT-WORKS.md) for the loop, and [Architecture](ARCHITECTURE.md) for the organs and the adapter verbs.
