import assert from "node:assert/strict";

// The scene substrate is a classic browser script that attaches a global; the
// adapter reads that global. Import both as side effects, mirroring how
// effects-protocol.test.mjs loads effects-protocol.js.
await import("./effects-protocol.js");
await import("./model-adapter.js");

const adapterApi = globalThis.TelosModelAdapter;
const protocol = globalThis.TelosEffectsProtocol;

const {
  ADAPTER_CONTRACT,
  STRAND_PARAMS,
  createOfflineAdapter,
  normalizeStrand,
  clampStrandValue,
  readIntent,
  runArena,
  witnessPick,
  evaluateProposal
} = adapterApi;

// ---- Contract shape ------------------------------------------------------

assert.equal(ADAPTER_CONTRACT.protocol, "project-telos.model-adapter/v1");
assert.ok(
  ADAPTER_CONTRACT.required_proposal_fields.includes("scene_spec"),
  "the contract must require a scene_spec on every proposal"
);
assert.ok(
  ADAPTER_CONTRACT.live_model.includes("not shipped"),
  "the contract must label the live model as specified, not shipped"
);
assert.deepEqual(
  STRAND_PARAMS.map((param) => param.key),
  ["symmetry", "palette_warmth", "loop_speed", "contrast"]
);

// ---- Strand bounds -------------------------------------------------------

assert.equal(clampStrandValue("symmetry", 99), 12, "symmetry clamps to its max");
assert.equal(clampStrandValue("symmetry", 0), 1, "symmetry clamps to its min");
assert.equal(clampStrandValue("symmetry", 5.4), 5, "symmetry is an integer");
assert.equal(clampStrandValue("palette_warmth", 2), 1, "warmth clamps to +1");
assert.equal(clampStrandValue("palette_warmth", -2), -1, "warmth clamps to -1");
assert.equal(clampStrandValue("loop_speed", 100), 4, "loop speed clamps to its max");
assert.equal(clampStrandValue("loop_speed", 0), 0.1, "loop speed clamps to its min");

const defaults = normalizeStrand({});
assert.deepEqual(defaults, { symmetry: 1, palette_warmth: 0, loop_speed: 1, contrast: 0.5 });

// ---- Intent -> parameter edit is DETERMINISTIC ---------------------------
// The core headless claim: the same intent against the same base always yields
// the same edit. Run the read twice and require byte-identical results.

const base = { mode: "all", seed: 5505, intensity: 0.82, density: 0.64, frame: 0 };
const intent = "make the field tile at 5-fold, warmer palette, slower loop";

const editOnce = readIntent(intent, base);
const editTwice = readIntent(intent, base);
assert.deepEqual(editOnce, editTwice, "intent parsing must be deterministic");

// The named intent must produce the specific parameter edits the directive
// calls out: 5-fold symmetry, a warmer palette, a slower loop.
assert.equal(editOnce.strand.symmetry, 5, "5-fold intent sets symmetry to 5");
assert.ok(editOnce.strand.palette_warmth > 0, "warmer intent raises palette_warmth");
assert.ok(editOnce.strand.loop_speed < 1, "slower intent lowers loop_speed");
assert.deepEqual(editOnce.matched_rules, ["symmetry.fold", "palette.warmer", "loop.slower"]);

// Word-number and other phrasings resolve too.
assert.equal(readIntent("seven-fold tiling", base).strand.symmetry, 7, "seven-fold word form");
assert.equal(readIntent("tile it at 3", base).strand.symmetry, 3, "tile at N form");
assert.ok(readIntent("cooler, icy palette", base).strand.palette_warmth < 0, "cooler lowers warmth");
assert.ok(readIntent("much faster loop", base).strand.loop_speed > 1, "faster raises loop_speed");

// An intent the stub does not understand is a no-op edit, not a crash.
const noop = readIntent("please make it nicer somehow", base);
assert.deepEqual(noop.matched_rules, [], "unrecognized intent matches no rules");
assert.deepEqual(noop.strand, normalizeStrand(base.strand), "unrecognized intent leaves strand at base");

// ---- Two Arena proposals genuinely DIFFER --------------------------------

const adapter = createOfflineAdapter();
const arena = runArena(adapter, intent, base);

assert.equal(arena.protocol, "project-telos.model-arena/v1");
assert.equal(arena.proposals.length, 2, "the Arena produces exactly two proposals");
assert.equal(arena.proposals[0].variant, "a");
assert.equal(arena.proposals[1].variant, "b");
assert.equal(arena.differ, true, "the two proposals must differ");
assert.notEqual(
  arena.proposals[0].scene_spec.spec_hash,
  arena.proposals[1].scene_spec.spec_hash,
  "the two proposals must have distinct spec hashes"
);
// Both proposals honestly answer the same intent (both are 5-fold here).
assert.equal(arena.proposals[0].scene_spec.strand.symmetry, 5);
assert.equal(arena.proposals[1].scene_spec.strand.symmetry, 5);

// The Arena itself is deterministic: same intent + base -> same arena id.
const arenaAgain = runArena(adapter, intent, base);
assert.equal(arenaAgain.arena_id, arena.arena_id, "the Arena is deterministic");
assert.equal(
  arenaAgain.proposals[0].scene_spec.spec_hash,
  arena.proposals[0].scene_spec.spec_hash
);

// ---- The kept proposal is WITNESSED into a receipt -----------------------

const receipt = witnessPick(arena, "a", { render_ms: 12, reduced_motion: false });

// It rides on the existing scene-receipt substrate, not a parallel one.
assert.equal(receipt.protocol, "project-telos.scene-receipt/v1");
assert.equal(receipt.verdict, "MATCH", "a bounded edit witnesses MATCH");
assert.equal(receipt.verification_verdict, "MATCH");
assert.equal(receipt.criterion_ref, "project-telos.model-adapter/v1#bounded-model-edit");
assert.match(receipt.receipt_hash, /^fnv1a:/);

// The model-in-the-loop provenance is joined to the receipt as an audit trail.
assert.ok(receipt.model_loop, "the receipt carries model-loop provenance");
assert.equal(receipt.model_loop.kept_variant, "a");
assert.equal(receipt.model_loop.rejected_variant, "b");
assert.equal(receipt.model_loop.intent, intent);
assert.equal(receipt.model_loop.arena_id, arena.arena_id);
assert.deepEqual(receipt.model_loop.matched_rules, ["symmetry.fold", "palette.warmer", "loop.slower"]);
assert.equal(receipt.model_loop.strand.symmetry, 5);

// The receipt hash must actually cover the model_loop block: recomputing over
// the receipt (minus its own hash) must reproduce receipt_hash.
const recomputed = protocol.hashStable({ ...receipt, receipt_hash: undefined });
assert.equal(recomputed, receipt.receipt_hash, "receipt_hash covers the model-loop edit");

// Witnessing is deterministic too.
const receiptAgain = witnessPick(arena, "a", { render_ms: 12, reduced_motion: false });
assert.equal(receiptAgain.receipt_hash, receipt.receipt_hash, "witness is deterministic");

// Picking the other variant yields a different, still-valid receipt.
const receiptB = witnessPick(arena, "b", { render_ms: 12 });
assert.equal(receiptB.verdict, "MATCH");
assert.notEqual(receiptB.receipt_hash, receipt.receipt_hash, "a different pick yields a different receipt");
assert.equal(receiptB.model_loop.kept_variant, "b");
assert.equal(receiptB.model_loop.rejected_variant, "a");

// ---- The criterion can FAIL (DRIFT), it is not theatrical ----------------
// A hand-built proposal whose strand is out of bounds must NOT witness MATCH.
// This proves the witness is a real check, not a rubber stamp.

const tamperedOutOfBounds = {
  scene_spec: {
    ...arena.proposals[0].scene_spec,
    strand: { symmetry: 99, palette_warmth: 5, loop_speed: 0, contrast: 0.5 }
  }
};
assert.equal(
  evaluateProposal(tamperedOutOfBounds),
  "DRIFT",
  "an out-of-bounds strand must be DRIFT, not MATCH"
);

// A proposal whose spec_hash no longer matches its content is DRIFT.
const tamperedHash = {
  scene_spec: {
    ...arena.proposals[0].scene_spec,
    strand: { symmetry: 6, palette_warmth: 0.35, loop_speed: 0.7, contrast: 0.5 }
    // spec_hash left stale on purpose (still the 5-fold hash)
  }
};
assert.equal(
  evaluateProposal(tamperedHash),
  "DRIFT",
  "a stale spec_hash must be DRIFT"
);

// A proposal with no strand at all is UNVERIFIABLE, not silently MATCH.
assert.equal(
  evaluateProposal({ scene_spec: { spec_hash: "fnv1a:00000000" } }),
  "UNVERIFIABLE",
  "a strand-less proposal is UNVERIFIABLE"
);

// A DRIFT verdict is honestly carried into the receipt (decision held, not allowed).
const driftArena = {
  arena_id: "telos-arena-test",
  proposals: [
    { variant: "a", adapter: "test", intent: "x", intent_hash: "fnv1a:0", matched_rules: [], edit_delta: {}, ...tamperedOutOfBounds }
  ]
};
const driftReceipt = witnessPick(driftArena, "a");
assert.equal(driftReceipt.verdict, "DRIFT", "an out-of-bounds pick witnesses DRIFT");
assert.equal(driftReceipt.decision_outcome, "hold", "a DRIFT verdict holds, it does not allow");

// ---- Edit delta is honest ------------------------------------------------
// The reported delta must equal the actual difference from the base strand.

const proposalA = arena.proposals[0];
assert.equal(proposalA.edit_delta.strand.symmetry, 4, "5-fold from a 1-fold base is a +4 delta");
assert.ok(proposalA.edit_delta.strand.loop_speed < 0, "a slower loop is a negative delta");
assert.ok(proposalA.edit_delta.strand.palette_warmth > 0, "a warmer palette is a positive delta");

process.stdout.write("model-adapter.test.mjs: all assertions passed\n");
