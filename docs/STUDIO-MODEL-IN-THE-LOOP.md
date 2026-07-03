# Studio Model-in-the-Loop

Date: 2026-07-02
Status: slice shipped, live wiring specified
Follows: `docs/PROJECT-TELOS-FEATURE-LEADERSHIP-2026-07-02.md` (standout feature 1)
Code: `demo/model-adapter.js`, `demo/model-adapter-cli.mjs`, `demo/model-adapter.test.mjs`
Rides on: `demo/effects-protocol.js` (`project-telos.scene-spec/v1`, `project-telos.scene-receipt/v1`)

## What this is

Model-in-the-loop live generation for the Telos Studio showcase surface. A
person (or an upstream agent) types a natural-language intent, a model edits the
scene parameters, an Arena-style two-proposal pick renders both side by side, and
the WITNESS step certifies the kept proposal into the existing scene receipt.

Accountability is the floor. This feature rides on the scene-spec and
scene-receipt substrate that already exists in `effects-protocol.js`. It does not
replace receipts. Every kept proposal joins a real `MATCH` / `DRIFT` /
`UNVERIFIABLE` receipt, with the intent and the parameter edit recorded as an
auditable, hashed trail.

## What is shipped in this slice

All four pieces below are shipped, headless, and tested in
`demo/model-adapter.test.mjs`. None of them require a network or a live model.

1. **A model-adapter contract** (`ADAPTER_CONTRACT`,
   `project-telos.model-adapter/v1`). One seam: `propose(intent, baseScene, variant)
   -> proposal`. Any backend that satisfies the contract can drive the Studio. The
   contract declares the strand parameter surface, the required proposal fields, and
   that live-model wiring is specified but not shipped.

2. **A deterministic offline model stub** (`createOfflineAdapter`). A rule-based
   reader that turns an intent string into a parameter edit. It is honestly a stub,
   not a language model. The same intent against the same base always produces the
   same edit, which is what makes the surface re-derivable and testable. Recognized
   intents today: symmetry fold ("5-fold", "seven-fold", "tile at 3"), palette warmth
   (warmer / cooler), loop speed (slower / faster), contrast, density, and intensity.
   An unrecognized intent is a no-op edit, not a crash or a guess.

3. **The Arena** (`runArena`). One intent produces two proposals, variant `a` and
   variant `b`, from distinct scene specs. Variant `b` explores an adjacent point in
   the parameter space via a deterministic seed nudge and a second, lighter reading,
   so the two proposals genuinely differ while both honestly answer the same intent.
   The Arena is itself deterministic: the same intent and base yield the same
   `arena_id`.

4. **The witness** (`witnessPick`). The user picks a variant; the kept proposal is
   certified into a `project-telos.scene-receipt/v1` receipt under the criterion
   `project-telos.model-adapter/v1#bounded-model-edit`. The criterion is one the
   model did not author: the kept strand must be within its declared bounds and the
   `spec_hash` must recompute over the edited spec. If either fails, the verdict is
   `DRIFT` and the decision is `hold`, not `allow`. A strand-less proposal is
   `UNVERIFIABLE`. The witness is not a rubber stamp; the test suite proves it can
   fail on tampered input. The model-in-the-loop provenance (adapter, intent,
   intent hash, kept and rejected variants, matched rules, edit delta, strand) is
   joined to the receipt and covered by `receipt_hash`.

### Strand parameter surface

The scene-spec already carries `seed`, `layers`, `intensity`, `density`, and
`frame`. Intents like "tile at 5-fold", "warmer palette", and "slower loop" need a
richer, named, bounded block, so the adapter folds a `strand` block into the spec
and re-hashes so `spec_hash` covers the edit:

| key             | label          | min | max | notes            |
| --------------- | -------------- | --- | --- | ---------------- |
| `symmetry`      | Symmetry fold  | 1   | 12  | integer          |
| `palette_warmth`| Palette warmth | -1  | 1   | negative = cooler |
| `loop_speed`    | Loop speed     | 0.1 | 4   | 1.0 = base       |
| `contrast`      | Contrast       | 0   | 1   |                  |

Every edit is clamped to these bounds, so a proposal can never leave the
declared surface. That clamp is exactly what the witness re-checks.

## How to run

```
node demo/model-adapter-cli.mjs
node demo/model-adapter-cli.mjs "warmer palette, 7-fold, slower loop"
node demo/model-adapter-cli.mjs --json "faster, cooler"
node demo/model-adapter.test.mjs
```

## What is specified, not shipped

The following are deliberately out of this slice. They are the browser wiring and
the live-model path. The shippable slice is the adapter contract plus the offline
stub; these ride on it without changing it.

### Live-model adapter

Replace the offline stub with a live model behind the same
`propose(intent, baseScene, variant)` seam. The live adapter sends the intent, the
base scene, and the strand parameter surface (with bounds) to a model, and the
model returns a strand edit. The returned edit passes through the same
`normalizeStrand` clamp and the same witness, so a live model cannot escape the
declared bounds or skip the receipt. Determinism is not required of the live path;
re-derivability is provided by the receipt, which records the exact edit the model
produced, not the model call. The contract already marks the live model as
"specified, not shipped" so no caller mistakes the stub for a language model.

Open questions for the live path: prompt shape for reliable strand-JSON output,
how to surface a low-confidence or refused edit as `UNVERIFIABLE` rather than a
silent no-op, and per-variant model or temperature choice for the Arena.

### Browser Arena UI

The `demo/index.html` Studio surface would gain an intent input, a two-pane
side-by-side render of variant `a` and variant `b` (each a live canvas driven by
the folded strand), a pick control, and a receipt panel that shows the witnessed
verdict for the kept variant. `effects-engine.js` already renders scenes from a
scene-spec; the wiring is to have it read the `strand` block (symmetry fold,
palette warmth, loop speed, contrast) and to call `runArena` / `witnessPick` from
the page. This is a rendering and event-wiring task on top of the shipped
substrate, not a change to the substrate.

### Later

Cross-examine as a forkable timeline of steers (each intent a branchable step),
and a share-link that reopens the exact kept World from its receipt. Both are
listed as "later" in the feature-leadership addendum and both build on this slice
plus the existing scene-spec encode/decode.

## Honest limitations

- The offline stub is a rule-based reader, not a language model. It recognizes a
  fixed vocabulary and does nothing on intents outside it. That is by design for
  the deterministic, testable slice, and it is labelled as a stub everywhere.
- The `strand` block is consumed by the browser renderer only once the browser
  Arena UI is wired (specified above). In this slice the strand is a bounded,
  hashed, witnessed parameter edit; it is not yet drawn on a live canvas in the
  shipped code.
- Variant `b`'s exploration heuristic (seed nudge plus a lighter second reading)
  is a simple, deterministic way to make the two proposals differ. A live model
  would explore the space more richly; the Arena seam does not change.
