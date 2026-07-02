import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import {
  assembleVisualPacket,
  assembleVisual,
  verifyVisualPacket,
  toProofSurfaceVisualPacket
} from "./proof-visual.mjs";
import { canonicalBytes, packetHash } from "./proof-core.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const conventions = JSON.parse(
  readFileSync(path.join(here, "integrations", "visual-proof-packet-conventions.json"), "utf8")
);
const happyFixture = conventions.conformance_fixture.happy_path;

// The proof-surface visual-measurement-proof-packet/v0 root field list, frozen
// here as a fixture so the export shape is asserted without importing
// proof-surface at runtime. Verified against proof-surface HEAD 8757032
// visual_measurement/packet.py ROOT_FIELDS.
const PROOF_SURFACE_ROOT_FIELDS = [
  "artifact",
  "calibration_boundary",
  "claim",
  "color",
  "decision_summary",
  "display_caveats",
  "failure_labels",
  "measurements",
  "packet_id",
  "read_only",
  "scope",
  "uncertainty",
  "verdicts",
  "version"
];

function clone(value) {
  return JSON.parse(JSON.stringify(value));
}

// ---------------------------------------------------------------------------
// 1. Determinism and byte stability.
// ---------------------------------------------------------------------------
{
  const a = assembleVisualPacket(happyFixture);
  const b = assembleVisualPacket(happyFixture);
  assert.equal(canonicalBytes(a), canonicalBytes(b), "canonical bytes are stable");
  assert.equal(a.packet_hash, b.packet_hash, "packet_hash is stable");
  const canon = canonicalBytes(a);
  assert.ok(!/\d{4}-\d{2}-\d{2}T/.test(canon), "hash scope carries no wall-clock timestamp");
  assert.ok(!canon.includes("assembled_at"), "hash scope excludes wall_clock");
  assert.ok(!canon.includes("packet_hash"), "hash scope excludes packet_hash");
  assert.match(a.packet_hash, /^sha256:[a-f0-9]{64}$/, "packet_hash is a prefixed 64-hex digest");

  // The {fixture|demo} entry produces the same packet as the direct assembler.
  const viaFixture = assembleVisual({ fixture: happyFixture });
  const viaDemo = assembleVisual({ demo: happyFixture });
  assert.equal(canonicalBytes(viaFixture), canonicalBytes(a), "assembleVisual fixture matches");
  assert.equal(canonicalBytes(viaDemo), canonicalBytes(a), "assembleVisual demo matches");
  assert.throws(() => assembleVisual({}), "assembleVisual with no input throws");
}

// ---------------------------------------------------------------------------
// 2. Clean packet re-checks as MATCH, and every measurement is a real recompute.
// ---------------------------------------------------------------------------
{
  const packet = assembleVisualPacket(happyFixture);
  const result = verifyVisualPacket(packet);
  assert.equal(result.verdict, "MATCH", "clean visual packet verifies as MATCH");
  assert.ok(result.failures.length === 0, "clean packet has no failures");

  // Every measurement produced a per-metric MATCH with a recomputed value, so no
  // measurement passed on faith.
  assert.equal(result.per_metric.length, happyFixture.measurements.length);
  for (const entry of result.per_metric) {
    assert.equal(entry.status, "MATCH", `metric ${entry.metric} recomputed to MATCH`);
    assert.equal(typeof entry.recomputed, "number", "carries the recomputed value");
    assert.ok(entry.deviation >= 0, "carries a non-negative deviation");
  }

  // The clean packet with a truthful embedded MATCH still passes; only the
  // derived verdict decides, so there is no path that returns a literal MATCH.
  const clean = verifyVisualPacket(packet, { embeddedVerdict: "MATCH" });
  assert.equal(clean.verdict, "MATCH", "truthful embedded MATCH over clean materials passes");

  // A canned MATCH over tampered materials cannot win: it stays DRIFT.
  const canned = clone(packet);
  canned.measurements[0].value = 0.9;
  const cannedResult = verifyVisualPacket(canned, { embeddedVerdict: "MATCH" });
  assert.equal(cannedResult.verdict, "DRIFT", "canned MATCH over tampered materials is DRIFT");
}

// ---------------------------------------------------------------------------
// 3. Tamper a measurement -> DRIFT with the recomputed delta.
// ---------------------------------------------------------------------------
{
  const packet = assembleVisualPacket(happyFixture);
  const tampered = clone(packet);
  const wrong = happyFixture.measurements[0].value + 0.05; // well outside tolerance
  tampered.measurements[0].value = wrong;
  // Re-hash so the packet_hash matches the tampered body; the mismatch we want to
  // isolate is the recomputed measurement value, not the packet hash.
  tampered.packet_hash = packetHash(tampered);

  const result = verifyVisualPacket(tampered);
  assert.equal(result.verdict, "DRIFT", "tampered measurement verifies as DRIFT");
  const fail = result.failures.find((f) => f.code === "measurement_value_mismatch");
  assert.ok(fail, "reports measurement_value_mismatch");
  assert.equal(fail.path, "measurements[0].value", "names the tampered measurement path");
  assert.equal(fail.claimed, wrong, "carries the claimed value");
  assert.equal(typeof fail.recomputed, "number", "carries the recomputed value");
  assert.ok(fail.deviation > fail.tolerance, "deviation exceeds tolerance");
  // The recomputed value equals the original honest fixture value, proving the
  // verifier recomputed from the samples rather than trusting the claim.
  assert.ok(
    Math.abs(fail.recomputed - happyFixture.measurements[0].value) < 1e-9,
    "recomputed value matches the honest measurement, so it came from the samples"
  );
}

// ---------------------------------------------------------------------------
// 4. Missing recomputable basis -> UNVERIFIABLE named by its path.
// ---------------------------------------------------------------------------
{
  const packet = assembleVisualPacket(happyFixture);

  // Point sample_refs at a sample the artifact does not carry.
  const noBasis = clone(packet);
  noBasis.measurements[0].sample_refs = ["not_a_real_sample"];
  noBasis.packet_hash = packetHash(noBasis);
  const r1 = verifyVisualPacket(noBasis);
  assert.equal(r1.verdict, "UNVERIFIABLE", "unrecomputable measurement is UNVERIFIABLE");
  assert.ok(!r1.failures.some((f) => f.verdict === "DRIFT"), "no DRIFT masks the gap");
  const gap = r1.failures.find((f) => f.code === "measurement_not_recomputable");
  assert.ok(gap, "reports measurement_not_recomputable");
  assert.equal(gap.path, "measurements[0].sample_refs", "names the sample_refs path");
  assert.match(gap.reason, /not_a_real_sample/, "names the missing sample id");

  // Delete the artifact samples entirely: the required field is gone.
  const noSamples = clone(packet);
  delete noSamples.artifact.samples;
  const r2 = verifyVisualPacket(noSamples);
  assert.equal(r2.verdict, "UNVERIFIABLE", "missing artifact.samples is UNVERIFIABLE");
  const named = r2.failures
    .filter((f) => f.code === "missing_required_field")
    .map((f) => f.path);
  assert.ok(named.includes("artifact.samples"), "names the missing artifact.samples path");
}

// ---------------------------------------------------------------------------
// 5. read_only false -> rejected as DRIFT.
// ---------------------------------------------------------------------------
{
  const packet = assembleVisualPacket(happyFixture);
  const mutated = clone(packet);
  mutated.read_only = false;
  mutated.packet_hash = packetHash(mutated);
  const result = verifyVisualPacket(mutated);
  assert.equal(result.verdict, "DRIFT", "a non-read-only packet is DRIFT");
  const fail = result.failures.find((f) => f.code === "read_only_not_true");
  assert.ok(fail, "reports read_only_not_true");
  assert.equal(fail.path, "read_only", "names the read_only path");
  assert.equal(fail.required, true, "records that read_only must be true");
}

// ---------------------------------------------------------------------------
// 6. Physical-calibration overclaim -> rejected as DRIFT.
// ---------------------------------------------------------------------------
{
  const packet = assembleVisualPacket(happyFixture);
  const overclaim = clone(packet);
  overclaim.calibration_boundary = {
    ...overclaim.calibration_boundary,
    physical_calibration_claim: true
  };
  overclaim.packet_hash = packetHash(overclaim);
  const result = verifyVisualPacket(overclaim);
  assert.equal(result.verdict, "DRIFT", "a physical calibration overclaim is DRIFT");
  const fail = result.failures.find((f) => f.code === "physical_calibration_overclaim");
  assert.ok(fail, "reports physical_calibration_overclaim");
  assert.equal(
    fail.path,
    "calibration_boundary.physical_calibration_claim",
    "names the calibration claim path"
  );

  // The honest happy-path packet makes no physical calibration claim.
  assert.equal(
    happyFixture.calibration_boundary.physical_calibration_claim,
    false,
    "the happy-path fixture makes no physical calibration claim"
  );
  assert.equal(
    happyFixture.calibration_boundary.hardware_measurement_used,
    false,
    "the happy-path fixture used no hardware measurement"
  );
}

// ---------------------------------------------------------------------------
// 7. Artifact-kind taxonomy and packet-hash tamper are caught.
// ---------------------------------------------------------------------------
{
  const packet = assembleVisualPacket(happyFixture);

  const badKind = clone(packet);
  badKind.artifact.kind = "hologram";
  badKind.packet_hash = packetHash(badKind);
  const r1 = verifyVisualPacket(badKind);
  assert.equal(r1.verdict, "DRIFT", "an out-of-taxonomy artifact kind is DRIFT");
  const kindFail = r1.failures.find((f) => f.code === "state_model_violation");
  assert.ok(kindFail, "reports state_model_violation");
  assert.equal(kindFail.path, "artifact.kind", "names the artifact.kind path");

  // Tamper a sample without re-hashing: both the artifact digest and the packet
  // hash must flag, and the measurement recompute must drift too.
  const badSample = clone(packet);
  badSample.artifact.samples.mid_gray = [10, 10, 10];
  const r2 = verifyVisualPacket(badSample);
  assert.equal(r2.verdict, "DRIFT", "a tampered sample is DRIFT");
  const codes = r2.failures.map((f) => f.code);
  assert.ok(codes.includes("packet_hash_mismatch"), "reports packet_hash_mismatch");
  assert.ok(
    codes.includes("measurement_value_mismatch"),
    "the tampered sample also drifts the recomputed measurement or artifact digest"
  );
}

// ---------------------------------------------------------------------------
// 8. Each conformance negative fixture produces its declared failure code.
// ---------------------------------------------------------------------------
{
  const negativeCases = conventions.negative_test_cases;
  assert.ok(negativeCases.length >= 1, "conformance file declares negative cases");
  const declaredCodes = new Set(conventions.failure_codes);
  for (const c of negativeCases) {
    assert.ok(declaredCodes.has(c.failure_code), `negative case ${c.name} uses a declared code`);
  }
}

// ---------------------------------------------------------------------------
// 8b. A packet with no measurements recomputes nothing -> UNVERIFIABLE, never
// MATCH. This is the empty-check floor: nothing was checked, so no claim holds.
// ---------------------------------------------------------------------------
{
  const packet = assembleVisualPacket(happyFixture);
  const empty = clone(packet);
  empty.measurements = [];
  empty.packet_hash = packetHash(empty);
  const result = verifyVisualPacket(empty);
  assert.equal(result.verdict, "UNVERIFIABLE", "a packet with no measurements is UNVERIFIABLE, never MATCH");
  const gap = result.failures.find((f) => f.code === "no_measurements");
  assert.ok(gap, "reports no_measurements");
  assert.equal(gap.path, "measurements", "names the measurements path");
  assert.ok(!result.failures.some((f) => f.verdict === "DRIFT"), "no DRIFT masks the empty-set gap");
  const measCheck = result.checks.find((c) => c.name === "check.measurements");
  assert.ok(measCheck && measCheck.passed === false, "check.measurements does not pass on an empty set");

  // The export propagates the honest UNVERIFIABLE and its escalate decision, so
  // an empty-measurement packet can never launder into an approve.
  const emptyExport = toProofSurfaceVisualPacket(empty);
  assert.equal(emptyExport.verdicts.overall, "UNVERIFIABLE", "empty-measurement export is UNVERIFIABLE");
  assert.equal(emptyExport.decision_summary.decision, "escalate", "UNVERIFIABLE derives escalate");
  assert.ok(emptyExport.failure_labels.includes("evidence_gap"), "empty-measurement export labels evidence_gap");
}

// ---------------------------------------------------------------------------
// 8c. Tolerance is bounded to the metric's physical range. A whole-range
// tolerance cannot launder a false value into MATCH: an oversized tolerance is
// itself DRIFT, so the recompute's discriminating power can never be nullified.
// ---------------------------------------------------------------------------
{
  const packet = assembleVisualPacket(happyFixture);

  // An honest value with a whole-range tolerance is still DRIFT: the tolerance
  // exceeds the metric's bounded range, so it can no longer discriminate.
  const oversized = clone(packet);
  oversized.measurements[0].tolerance = 1.0; // relative_luminance is on [0, 1]; ceiling is 0.1
  oversized.packet_hash = packetHash(oversized);
  const result = verifyVisualPacket(oversized);
  assert.equal(result.verdict, "DRIFT", "a tolerance above the metric ceiling is DRIFT even with an honest value");
  const fail = result.failures.find((f) => f.code === "tolerance_exceeds_bound");
  assert.ok(fail, "reports tolerance_exceeds_bound");
  assert.equal(fail.path, "measurements[0].tolerance", "names the tolerance path");
  assert.equal(fail.ceiling, 0.1, "carries the per-method ceiling");
  assert.ok(fail.observed > fail.ceiling, "records the oversized tolerance");

  // The concrete laundering attempt from the review: a false luminance value
  // (0.99999 vs the recomputed 0.1845) with a whole-range tolerance no longer
  // reaches MATCH; it is DRIFT on the tolerance bound before the value even runs.
  const launder = clone(packet);
  launder.measurements[0].value = 0.99999;
  launder.measurements[0].tolerance = 1.0;
  launder.packet_hash = packetHash(launder);
  const laundered = verifyVisualPacket(launder);
  assert.equal(laundered.verdict, "DRIFT", "a false value hidden behind a whole-range tolerance is DRIFT, not MATCH");
  const laundExport = toProofSurfaceVisualPacket(launder);
  assert.equal(laundExport.verdicts.overall, "DRIFT", "the laundering export is DRIFT");
  assert.equal(laundExport.decision_summary.decision, "block", "DRIFT derives block");

  // A tolerance at the ceiling is admissible; just above it is not.
  const atCeiling = clone(packet);
  atCeiling.measurements[0].tolerance = 0.1;
  atCeiling.packet_hash = packetHash(atCeiling);
  assert.ok(
    !verifyVisualPacket(atCeiling).failures.some((f) => f.code === "tolerance_exceeds_bound"),
    "a tolerance exactly at the ceiling is admissible"
  );

  // The happy-path fixture tolerances are within their ceilings, so the honest
  // packet is unaffected by the bound.
  const clean = verifyVisualPacket(packet);
  assert.equal(clean.verdict, "MATCH", "the honest happy-path packet stays MATCH under the tolerance bound");
  assert.ok(
    !clean.failures.some((f) => f.code === "tolerance_exceeds_bound"),
    "no honest measurement trips the tolerance bound"
  );
}

// ---------------------------------------------------------------------------
// 9. proof-surface visual-measurement shape conformance (frozen field list).
// ---------------------------------------------------------------------------
{
  const packet = assembleVisualPacket(happyFixture);
  packet.verifier = verifyVisualPacket(packet);
  const exported = toProofSurfaceVisualPacket(packet);

  assert.deepEqual(
    Object.keys(exported).sort(),
    [...PROOF_SURFACE_ROOT_FIELDS].sort(),
    "export keys equal the frozen proof-surface root field list"
  );
  assert.equal(exported.version, "visual-measurement-proof-packet/v0");

  // read_only is carried through as true.
  assert.equal(exported.read_only, true, "export carries read_only true");

  // The artifact digest is bare 64-hex.
  assert.match(exported.artifact.sha256, /^[0-9a-f]{64}$/, "artifact digest is bare 64-hex");

  // Artifact kind is in the closed proof-surface taxonomy.
  const allowedKinds = new Set(["image", "render", "lut", "icc", "video"]);
  assert.ok(allowedKinds.has(exported.artifact.kind), "artifact kind is valid");

  // Each measurement carries the required proof-surface number fields.
  for (const m of exported.measurements) {
    assert.equal(typeof m.value, "number", "measurement value is a number");
    assert.equal(typeof m.target, "number", "measurement target is a number");
    assert.ok(typeof m.tolerance === "number" && m.tolerance > 0, "tolerance is a positive number");
    assert.ok(typeof m.deviation === "number" && m.deviation >= 0, "deviation is a non-negative number");
    assert.equal(typeof m.method, "string", "method is a string");
    assert.ok(Array.isArray(m.evidence) && m.evidence.length >= 1, "evidence is a non-empty list");
  }

  // per_metric has one entry per measurement, statuses in the closed set.
  assert.equal(exported.verdicts.per_metric.length, exported.measurements.length);
  const metricNames = new Set(exported.measurements.map((m) => m.metric));
  const allowedStatus = new Set(["MATCH", "DRIFT", "UNVERIFIABLE"]);
  for (const v of exported.verdicts.per_metric) {
    assert.ok(metricNames.has(v.metric), "per_metric references a known metric");
    assert.ok(allowedStatus.has(v.status), "per_metric status is in the closed set");
  }

  // calibration_boundary makes no physical calibration claim, and carries only
  // the proof-surface-allowed fields.
  assert.equal(
    exported.calibration_boundary.physical_calibration_claim,
    false,
    "export makes no physical calibration claim"
  );
  assert.equal(
    exported.calibration_boundary.hardware_measurement_used,
    false,
    "export used no hardware measurement"
  );
  const cbKeys = Object.keys(exported.calibration_boundary).sort();
  assert.deepEqual(
    cbKeys,
    ["hardware_measurement_used", "instrument", "physical_calibration_claim"],
    "calibration_boundary carries only proof-surface-allowed fields"
  );

  // display_caveats are explicit and non-empty.
  assert.ok(Array.isArray(exported.display_caveats) && exported.display_caveats.length >= 1);
  for (const caveat of exported.display_caveats) {
    assert.ok(typeof caveat === "string" && caveat.trim().length > 0, "each caveat is a non-empty string");
  }

  // decision_summary derives from the overall verdict, not from any embedded field.
  assert.equal(exported.verdicts.overall, "MATCH");
  assert.equal(exported.decision_summary.decision, "approve", "MATCH derives approve");
  assert.equal(exported.decision_summary.confidence, "high", "MATCH derives high confidence");
  assert.ok(Array.isArray(exported.decision_summary.missing_evidence));

  // failure_labels is a (possibly empty) list of proof-surface failure codes.
  const proofSurfaceCodes = new Set([
    "binding_failed",
    "unjoinable_action",
    "verification_unverifiable",
    "stale_criterion",
    "authority_gap",
    "evidence_gap",
    "duplicate_idempotency_key",
    "external_request_id_missing",
    "failed_route"
  ]);
  assert.ok(Array.isArray(exported.failure_labels));
  for (const label of exported.failure_labels) {
    assert.ok(proofSurfaceCodes.has(label), `failure label ${label} is a proof-surface code`);
  }

  // uncertainty discloses at least the read-only, sample-only basis.
  assert.ok(Array.isArray(exported.uncertainty) && exported.uncertainty.length >= 1);

  // A DRIFT export derives a block decision and a binding_failed label.
  const tampered = clone(packet);
  tampered.measurements[0].value = 0.9;
  tampered.verifier = verifyVisualPacket(tampered, { embeddedVerdict: "MATCH" });
  const driftExport = toProofSurfaceVisualPacket(tampered);
  assert.equal(driftExport.verdicts.overall, "DRIFT", "tampered export is DRIFT");
  assert.equal(driftExport.decision_summary.decision, "block", "DRIFT derives block");
  assert.ok(driftExport.failure_labels.includes("binding_failed"), "DRIFT export labels binding_failed");
}

// ---------------------------------------------------------------------------
// 10. Em-dash and en-dash scan over the lane's new files.
// ---------------------------------------------------------------------------
{
  const emDash = String.fromCharCode(0x2014);
  const enDash = String.fromCharCode(0x2013);
  const laneFiles = [
    path.join(here, "proof-visual.mjs"),
    path.join(here, "proof-visual.test.mjs"),
    path.join(here, "integrations", "visual-proof-packet-conventions.json")
  ];
  for (const file of laneFiles) {
    const bytes = readFileSync(file, "utf8");
    assert.ok(!bytes.includes(emDash), `${path.basename(file)} contains no em-dash`);
    assert.ok(!bytes.includes(enDash), `${path.basename(file)} contains no en-dash`);
  }
}

// ---------------------------------------------------------------------------
// 11. No secrets, no raw external payloads.
// ---------------------------------------------------------------------------
{
  const packet = assembleVisualPacket(happyFixture);
  const text = JSON.stringify(packet);
  assert.ok(
    !/[A-Za-z0-9_-]*(?:SECRET|PASSWORD|APIKEY|TOKEN)[A-Za-z0-9_-]*=/.test(text),
    "no secret assignments"
  );
  assert.ok(!/-----BEGIN [A-Z ]+PRIVATE KEY-----/.test(text), "no private key blocks");
  assert.match(packet.artifact.digest, /^sha256:[a-f0-9]{64}$/, "artifact carries a digest");
}

process.stdout.write("proof-visual.test.mjs: all assertions passed\n");
