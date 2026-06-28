import assert from "node:assert/strict";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const protocol = require("./effects-protocol.js");

const {
  EFFECT_LAYERS,
  EFFECT_PRESETS,
  createReceiptChain,
  createSceneReceipt,
  createSceneSpec,
  decodeSceneSpec,
  encodeSceneSpec,
  normalizeLayerList
} = protocol;

assert.ok(EFFECT_LAYERS.length >= 19, "the protocol should expose the full visual layer bank");
assert.deepEqual(
  EFFECT_PRESETS.map((preset) => preset.id),
  ["all", "scientific", "poster", "flagship", "terminal", "radiance", "diagnostic"]
);

const scientificSpec = createSceneSpec({
  density: 0.63,
  frame: 3,
  host: "node-test",
  intensity: 0.75,
  layers: ["contour", "vector", "clustered", "contour", "unknown"],
  mode: "scientific",
  seed: 42,
  source: "effects-protocol.test.mjs"
});

assert.equal(scientificSpec.protocol, "project-telos.scene-spec/v1");
assert.equal(scientificSpec.mode, "scientific");
assert.deepEqual(scientificSpec.layers, ["contour", "vector", "clustered"]);
assert.equal(scientificSpec.io.protocol_agnostic, true);
assert.equal(scientificSpec.privacy.raw_payload_exported, false);
assert.match(scientificSpec.action_intent_id, /^telos-action-/);
assert.match(scientificSpec.args_hash, /^fnv1a:/);
assert.match(scientificSpec.spec_hash, /^fnv1a:/);

const roundTrip = decodeSceneSpec(encodeSceneSpec(scientificSpec));
assert.deepEqual(roundTrip, scientificSpec);

const firstReceipt = createSceneReceipt(scientificSpec, {
  frame: 3,
  reduced_motion: false,
  render_ms: 14,
  result_ref: "canvas://effect-canvas"
});

assert.equal(firstReceipt.protocol, "project-telos.scene-receipt/v1");
assert.equal(firstReceipt.action_intent_id, scientificSpec.action_intent_id);
assert.equal(firstReceipt.args_hash, scientificSpec.args_hash);
assert.equal(firstReceipt.decision_outcome, "allow");
assert.equal(firstReceipt.verification_verdict, "MATCH");
assert.equal(firstReceipt.verdict, "MATCH");
assert.equal(firstReceipt.raw_payload_exported, false);
assert.match(firstReceipt.evidence_ref, /^receipt:\/\/scene\//);
assert.match(firstReceipt.receipt_hash, /^fnv1a:/);

const secondReceipt = createReceiptChain(scientificSpec, firstReceipt, { frame: 4, render_ms: 9 });
assert.equal(secondReceipt.previous_receipt_hash, firstReceipt.receipt_hash);
assert.notEqual(secondReceipt.receipt_hash, firstReceipt.receipt_hash);

assert.deepEqual(normalizeLayerList(["bogus", "glitch", "retro", "glitch"]), ["glitch", "retro"]);
assert.ok(EFFECT_LAYERS.some((layer) => layer.id === "halftone"));
assert.ok(EFFECT_LAYERS.some((layer) => layer.id === "layout"));