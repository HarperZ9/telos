import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import {
  assembleBuildPacket,
  assembleBuild,
  verifyBuildPacket,
  toProofSurfaceBuildPacket
} from "./proof-build.mjs";
import { canonicalBytes, packetHash, digestBytes } from "./proof-core.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const conventions = JSON.parse(
  readFileSync(path.join(here, "integrations", "build-proof-packet-conventions.json"), "utf8")
);
const happyFixture = conventions.conformance_fixture.happy_path;

// The proof-surface conservation-proof-packet/v0 root field list, frozen here as
// a fixture so the export shape is asserted without importing proof-surface at
// runtime. Verified against proof-surface HEAD 8757032
// conservation/packet.py ROOT_FIELDS.
const PROOF_SURFACE_ROOT_FIELDS = [
  "boundary_fixture",
  "claim",
  "decision_summary",
  "failure_labels",
  "invariant",
  "negative_fixture",
  "packet_id",
  "scope",
  "sources",
  "transformation",
  "uncertainty",
  "verdicts",
  "version",
  "witnesses"
];

const PROOF_SURFACE_OVERALL_VERDICTS = new Set(["MATCH", "DRIFT", "UNVERIFIABLE"]);
const PROOF_SURFACE_WITNESS_KINDS = new Set(["algebraic", "numeric", "symbolic"]);
const PROOF_SURFACE_FAILURE_CODES = new Set([
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

function clone(value) {
  return JSON.parse(JSON.stringify(value));
}

// The proof-surface boundary-fixture and negative-fixture gate rules, frozen here
// so a MATCH export is asserted to satisfy them in-suite without importing or
// spawning proof-surface. Verified verbatim against proof-surface HEAD 8757032
// conservation/_gates.py validate_negative_fixture and validate_boundary_fixture.
// The negative fixture must break the invariant (breaks_invariant true AND drift >
// tolerance); the optional boundary fixture must show the goal HOLDING
// (goal_holds true) and the claimed condition FAILING (condition_holds false).
// Returns a list of proof-surface-shaped gate issues; an empty list means valid.
function proofSurfaceGateIssues(exported) {
  const issues = [];
  const neg = exported.negative_fixture;
  if (!neg || typeof neg !== "object") {
    issues.push("$.negative_fixture: expected object");
  } else {
    if (neg.breaks_invariant !== true) {
      issues.push("$.negative_fixture.breaks_invariant: expected true");
    } else if (
      typeof neg.drift === "number" &&
      typeof neg.tolerance === "number" &&
      neg.drift <= neg.tolerance
    ) {
      issues.push("$.negative_fixture: breaks_invariant is true but drift is within tolerance");
    }
  }
  const bnd = exported.boundary_fixture;
  if (bnd !== null && bnd !== undefined) {
    if (typeof bnd !== "object") {
      issues.push("$.boundary_fixture: expected object");
    } else {
      if (bnd.goal_holds !== true) {
        issues.push("$.boundary_fixture.goal_holds: a boundary fixture must show the goal HOLDING");
      }
      if (bnd.condition_holds !== false) {
        issues.push("$.boundary_fixture.condition_holds: a boundary fixture must show the claimed condition FAILING");
      }
    }
  }
  return issues;
}

// ---------------------------------------------------------------------------
// 1. Determinism and byte stability.
// ---------------------------------------------------------------------------
{
  const a = assembleBuildPacket(happyFixture);
  const b = assembleBuildPacket(happyFixture);
  assert.equal(canonicalBytes(a), canonicalBytes(b), "canonical bytes are stable");
  assert.equal(a.packet_hash, b.packet_hash, "packet_hash is stable");
  const canon = canonicalBytes(a);
  assert.ok(!/\d{4}-\d{2}-\d{2}T/.test(canon), "hash scope carries no wall-clock timestamp");
  assert.ok(!canon.includes("assembled_at"), "hash scope excludes wall_clock");
  assert.ok(!canon.includes("packet_hash"), "hash scope excludes packet_hash");
  assert.match(a.packet_hash, /^sha256:[a-f0-9]{64}$/, "packet_hash is a prefixed 64-hex digest");

  // The assembler resolved the "recompute" source-digest placeholder into a real
  // digest over the embedded source program.
  assert.match(a.receipt.source_digest, /^sha256:[a-f0-9]{64}$/, "source_digest is a real digest");
  assert.equal(
    a.receipt.source_digest,
    digestBytes(a.receipt.source_program),
    "source_digest recomputes from the embedded source program"
  );

  // The {fixture|demo} entry produces the same packet as the direct assembler.
  const viaFixture = assembleBuild({ fixture: happyFixture });
  const viaDemo = assembleBuild({ demo: happyFixture });
  assert.equal(canonicalBytes(viaFixture), canonicalBytes(a), "assembleBuild fixture matches");
  assert.equal(canonicalBytes(viaDemo), canonicalBytes(a), "assembleBuild demo matches");
  assert.throws(() => assembleBuild({}), "assembleBuild with no input throws");
}

// ---------------------------------------------------------------------------
// 2. Clean packet re-checks as MATCH, and every invariant is a real recompute.
// ---------------------------------------------------------------------------
{
  const packet = assembleBuildPacket(happyFixture);
  const result = verifyBuildPacket(packet);
  assert.equal(result.verdict, "MATCH", "clean build packet verifies as MATCH");
  assert.equal(result.failures.length, 0, "clean packet has no failures");

  // The invariant produced a per-invariant MATCH with a recomputed value, so it
  // did not pass on faith.
  assert.equal(result.per_invariant.status, "MATCH", "invariant recomputed to MATCH");
  assert.equal(typeof result.per_invariant.recomputed, "number", "carries the recomputed value");
  assert.ok(result.per_invariant.deviation >= 0, "carries a non-negative deviation");
  // The recomputed mean equals the honest claimed value.
  assert.ok(
    Math.abs(result.per_invariant.recomputed - happyFixture.invariant.value) < 1e-9,
    "recomputed invariant equals the claimed value, so it came from the samples"
  );

  // Every named check ran and passed or was skipped.
  for (const check of result.checks) {
    assert.ok(check.passed || check.skipped, `${check.name} passed or was skipped`);
  }

  // A truthful embedded MATCH still passes; only the derived verdict decides, so
  // there is no path that returns a literal MATCH.
  const clean = verifyBuildPacket(packet, { embeddedVerdict: "MATCH" });
  assert.equal(clean.verdict, "MATCH", "truthful embedded MATCH over clean materials passes");
}

// ---------------------------------------------------------------------------
// 3. Tamper the source program -> DRIFT with the expected-vs-recomputed digest.
// ---------------------------------------------------------------------------
{
  const packet = assembleBuildPacket(happyFixture);
  const tampered = clone(packet);
  tampered.receipt.source_program = tampered.receipt.source_program + " // tampered";
  const result = verifyBuildPacket(tampered);
  assert.equal(result.verdict, "DRIFT", "tampered source program verifies as DRIFT");
  const codes = result.failures.map((f) => f.code);
  assert.ok(codes.includes("source_digest_mismatch"), "reports source_digest_mismatch");
  assert.ok(codes.includes("packet_hash_mismatch"), "tamper also breaks the packet hash");
  const fail = result.failures.find((f) => f.code === "source_digest_mismatch");
  assert.equal(fail.path, "receipt.source_digest", "names the source digest path");
  assert.equal(fail.expected, packet.receipt.source_digest, "carries the claimed digest");
  assert.equal(
    fail.recomputed,
    digestBytes(tampered.receipt.source_program),
    "carries the recomputed digest over the tampered program"
  );
  assert.notEqual(fail.expected, fail.recomputed, "the delta is a real mismatch");
}

// ---------------------------------------------------------------------------
// 4. Tamper the invariant value -> DRIFT carrying the recomputed delta.
// ---------------------------------------------------------------------------
{
  const packet = assembleBuildPacket(happyFixture);
  const tampered = clone(packet);
  const wrong = happyFixture.invariant.value + 0.5; // well outside tolerance
  tampered.invariant.value = wrong;
  // Re-hash so the packet_hash matches the tampered body; the mismatch we isolate
  // is the recomputed invariant value, not the packet hash.
  tampered.packet_hash = packetHash(tampered);
  const result = verifyBuildPacket(tampered);
  assert.equal(result.verdict, "DRIFT", "tampered invariant value verifies as DRIFT");
  const fail = result.failures.find((f) => f.code === "invariant_value_mismatch" && f.path === "invariant.value");
  assert.ok(fail, "reports invariant_value_mismatch on the invariant value");
  assert.equal(fail.claimed, wrong, "carries the claimed value");
  assert.equal(typeof fail.recomputed, "number", "carries the recomputed value");
  assert.ok(fail.deviation > fail.tolerance, "deviation exceeds tolerance");
  // The recomputed value equals the honest fixture value, proving the verifier
  // recomputed from the samples rather than trusting the claim.
  assert.ok(
    Math.abs(fail.recomputed - happyFixture.invariant.value) < 1e-9,
    "recomputed invariant equals the honest value, so it came from the samples"
  );
}

// ---------------------------------------------------------------------------
// 4b. Tamper the drift value -> DRIFT naming the drift path.
// ---------------------------------------------------------------------------
{
  const packet = assembleBuildPacket(happyFixture);
  const tampered = clone(packet);
  tampered.drift.value = happyFixture.drift.value + 0.05; // outside the drift tolerance
  tampered.packet_hash = packetHash(tampered);
  const result = verifyBuildPacket(tampered);
  assert.equal(result.verdict, "DRIFT", "a tampered drift value is DRIFT");
  const fail = result.failures.find((f) => f.code === "invariant_value_mismatch" && f.path === "drift.value");
  assert.ok(fail, "reports invariant_value_mismatch on the drift value");
  assert.ok(
    Math.abs(fail.recomputed - happyFixture.drift.value) < 1e-9,
    "recomputed drift equals the honest value, so it came from the samples"
  );
}

// ---------------------------------------------------------------------------
// 5. Missing negative fixture -> UNVERIFIABLE, naming the missing item.
// ---------------------------------------------------------------------------
{
  const packet = assembleBuildPacket(happyFixture);
  const noNeg = clone(packet);
  delete noNeg.negative_fixture;
  const result = verifyBuildPacket(noNeg);
  assert.equal(result.verdict, "UNVERIFIABLE", "missing negative fixture is UNVERIFIABLE");
  assert.ok(!result.failures.some((f) => f.verdict === "DRIFT"), "no DRIFT masks the missing fixture");
  const named = result.failures.filter((f) => f.code === "missing_required_field").map((f) => f.path);
  assert.ok(named.includes("negative_fixture.id"), "names negative_fixture.id");
  assert.ok(named.includes("negative_fixture.samples"), "names negative_fixture.samples");
  assert.ok(named.includes("negative_fixture.conservation_tolerance"), "names the conservation tolerance");
}

// ---------------------------------------------------------------------------
// 5b. A negative control that does not break the invariant -> DRIFT.
// The control run is replaced with conserved samples, so its recomputed drift no
// longer exceeds the conservation tolerance: the check does not discriminate.
// ---------------------------------------------------------------------------
{
  const packet = assembleBuildPacket(happyFixture);
  const conserved = clone(packet);
  conserved.negative_fixture.samples = clone(happyFixture.run.samples);
  conserved.packet_hash = packetHash(conserved);
  const result = verifyBuildPacket(conserved);
  assert.equal(result.verdict, "DRIFT", "a non-breaking negative control is DRIFT");
  const fail = result.failures.find((f) => f.code === "negative_control_conserved");
  assert.ok(fail, "reports negative_control_conserved");
  assert.equal(fail.path, "negative_fixture.samples", "names the control samples path");
  assert.ok(
    fail.recomputed_drift <= fail.conservation_tolerance,
    "the control's recomputed drift is within tolerance, so it does not break the invariant"
  );
}

// ---------------------------------------------------------------------------
// 5c. The boundary run must show the goal HOLDING while the claimed condition
// FAILS. A boundary run whose recomputed mean lands on the claimed value makes
// condition_holds true, which proof-surface's boundary-fixture gate rejects; the
// verifier must catch it first as DRIFT so no MATCH ever pairs with a
// proof-surface-invalid export. This is the guard that closes the laundered-MATCH
// hole where a hash-consistent boundary equal to the happy run verified clean.
// ---------------------------------------------------------------------------
{
  const packet = assembleBuildPacket(happyFixture);

  // Boundary run equal to the happy run: its mean lands on the claimed value, so
  // the claimed condition holds. That must be DRIFT, not MATCH.
  const conditionHolds = clone(packet);
  conditionHolds.boundary_run.samples = clone(happyFixture.run.samples);
  conditionHolds.packet_hash = packetHash(conditionHolds);
  const cResult = verifyBuildPacket(conditionHolds);
  assert.equal(cResult.verdict, "DRIFT", "a boundary run on which the claimed condition holds is DRIFT, not MATCH");
  const cFail = cResult.failures.find((f) => f.code === "boundary_condition_holds");
  assert.ok(cFail, "reports boundary_condition_holds");
  assert.equal(cFail.path, "boundary_run.samples", "names the boundary samples path");
  assert.ok(cFail.delta <= cFail.invariant_tolerance, "the boundary mean is within the invariant tolerance of the claimed value");
  // The export of this DRIFT packet blocks, never approves.
  const cExport = toProofSurfaceBuildPacket(conditionHolds);
  assert.equal(cExport.verdicts.overall, "DRIFT", "the condition-holds boundary export is DRIFT");
  assert.equal(cExport.decision_summary.decision, "block", "DRIFT derives block, not approve");
  assert.equal(cExport.boundary_fixture.condition_holds, true, "the export honestly records condition_holds true");

  // Boundary run that is not conserved (the damped control): the goal does not
  // hold, so it is a mislabeled negative case, not a sufficiency boundary. DRIFT.
  const goalBroken = clone(packet);
  goalBroken.boundary_run.samples = clone(happyFixture.negative_fixture.samples);
  goalBroken.packet_hash = packetHash(goalBroken);
  const gResult = verifyBuildPacket(goalBroken);
  assert.equal(gResult.verdict, "DRIFT", "a boundary run whose energy is not conserved is DRIFT");
  const gFail = gResult.failures.find((f) => f.code === "boundary_goal_broken");
  assert.ok(gFail, "reports boundary_goal_broken");
  assert.ok(gFail.recomputed_drift > gFail.goal_tolerance, "the boundary drift exceeds the conservation tolerance");

  // A boundary run whose samples cannot be recomputed is an UNVERIFIABLE gap.
  const unrecomputable = clone(packet);
  unrecomputable.boundary_run.samples = [[0, "x", 1]];
  unrecomputable.packet_hash = packetHash(unrecomputable);
  const uResult = verifyBuildPacket(unrecomputable);
  assert.equal(uResult.verdict, "UNVERIFIABLE", "a boundary run that cannot be recomputed is UNVERIFIABLE");
  assert.ok(
    uResult.failures.some((f) => f.code === "invariant_not_recomputable" && f.path === "boundary_run.samples"),
    "names the boundary samples path as the unrecomputable basis"
  );
  assert.ok(!uResult.failures.some((f) => f.verdict === "DRIFT"), "no DRIFT masks the boundary evidence gap");

  // The honest happy-path boundary keeps the goal holding and the condition
  // failing, so it stays MATCH.
  const clean = verifyBuildPacket(packet);
  assert.equal(clean.verdict, "MATCH", "the honest happy-path boundary stays MATCH");
  const boundaryCheck = clean.checks.find((c) => c.name === "check.boundary_run");
  assert.ok(boundaryCheck && boundaryCheck.passed, "check.boundary_run passes on the honest boundary");
}

// ---------------------------------------------------------------------------
// 6. Nothing checked: an empty run sample series -> UNVERIFIABLE, never MATCH.
// This is the empty-check floor: nothing was recomputed, so no claim holds.
// ---------------------------------------------------------------------------
{
  const packet = assembleBuildPacket(happyFixture);
  const empty = clone(packet);
  empty.run.samples = [];
  empty.packet_hash = packetHash(empty);
  const result = verifyBuildPacket(empty);
  assert.equal(result.verdict, "UNVERIFIABLE", "a run with no samples is UNVERIFIABLE, never MATCH");
  const gap = result.failures.find((f) => f.code === "no_run_samples");
  assert.ok(gap, "reports no_run_samples");
  assert.equal(gap.path, "run.samples", "names the run samples path");
  assert.ok(!result.failures.some((f) => f.verdict === "DRIFT"), "no DRIFT masks the empty-set gap");
  const runCheck = result.checks.find((c) => c.name === "check.run_samples");
  assert.ok(runCheck && runCheck.passed === false, "check.run_samples does not pass on an empty set");

  // The export propagates the honest UNVERIFIABLE and its escalate decision.
  const emptyExport = toProofSurfaceBuildPacket(empty);
  assert.equal(emptyExport.verdicts.overall, "UNVERIFIABLE", "empty-run export is UNVERIFIABLE");
  assert.equal(emptyExport.decision_summary.decision, "escalate", "UNVERIFIABLE derives escalate");
  assert.ok(emptyExport.failure_labels.includes("evidence_gap"), "empty-run export labels evidence_gap");
}

// ---------------------------------------------------------------------------
// 7. Tolerance is bounded to the metric's physical range. A whole-range
// tolerance cannot launder a false value into MATCH: an oversized tolerance is
// itself DRIFT, so the recompute's discriminating power can never be nullified.
// ---------------------------------------------------------------------------
{
  const packet = assembleBuildPacket(happyFixture);

  // An honest value with a whole-range invariant tolerance is still DRIFT: the
  // tolerance exceeds the metric's bounded range (mean energy / 100).
  const oversized = clone(packet);
  oversized.invariant.tolerance = happyFixture.invariant.value; // == the whole mean; ceiling is mean/100
  oversized.packet_hash = packetHash(oversized);
  const result = verifyBuildPacket(oversized);
  assert.equal(result.verdict, "DRIFT", "an invariant tolerance above its ceiling is DRIFT even with an honest value");
  const fail = result.failures.find((f) => f.code === "tolerance_exceeds_bound" && f.path === "invariant.tolerance");
  assert.ok(fail, "reports tolerance_exceeds_bound on the invariant tolerance");
  assert.equal(fail.method, "mean_total_energy", "names the method");
  assert.ok(fail.observed > fail.ceiling, "records the oversized tolerance");

  // The concrete laundering attempt: a false invariant value hidden behind a
  // whole-range tolerance no longer reaches MATCH; it is DRIFT on the bound.
  const launder = clone(packet);
  launder.invariant.value = happyFixture.invariant.value + 100;
  launder.invariant.tolerance = 1000;
  launder.packet_hash = packetHash(launder);
  const laundered = verifyBuildPacket(launder);
  assert.equal(laundered.verdict, "DRIFT", "a false value behind a whole-range tolerance is DRIFT, not MATCH");

  // A whole-range drift tolerance is likewise rejected.
  const oversizedDrift = clone(packet);
  oversizedDrift.drift.tolerance = 0.5; // ceiling is 0.1
  oversizedDrift.packet_hash = packetHash(oversizedDrift);
  const driftResult = verifyBuildPacket(oversizedDrift);
  assert.equal(driftResult.verdict, "DRIFT", "a drift tolerance above its ceiling is DRIFT");
  const driftFail = driftResult.failures.find((f) => f.code === "tolerance_exceeds_bound" && f.path === "drift.tolerance");
  assert.ok(driftFail, "reports tolerance_exceeds_bound on the drift tolerance");
  assert.equal(driftFail.ceiling, 0.1, "carries the drift ceiling");

  // The honest happy-path tolerances are within their ceilings.
  const clean = verifyBuildPacket(packet);
  assert.equal(clean.verdict, "MATCH", "the honest happy-path packet stays MATCH under the tolerance bound");
  assert.ok(
    !clean.failures.some((f) => f.code === "tolerance_exceeds_bound"),
    "no honest tolerance trips the bound"
  );
}

// ---------------------------------------------------------------------------
// 7b. A run whose energy drifts beyond tolerance -> DRIFT (drift_exceeds_tolerance).
// The run samples are replaced with the damped control, which is lossy, while the
// claimed drift value is set honestly to the recomputed damped drift; the run is
// still DRIFT because the recomputed drift exceeds the conservation tolerance.
// ---------------------------------------------------------------------------
{
  const packet = assembleBuildPacket(happyFixture);
  const lossy = clone(packet);
  lossy.run.samples = clone(happyFixture.negative_fixture.samples); // the damped, lossy run
  // Recompute the honest mean and drift for the lossy run so only the conservation
  // failure remains, not a value mismatch.
  const mass = lossy.run.constants.mass;
  const stiffness = lossy.run.constants.stiffness;
  const energy = ([, x, v]) => 0.5 * mass * v * v + 0.5 * stiffness * x * x;
  const Es = lossy.run.samples.map(energy);
  const mean = Es.reduce((a, b) => a + b, 0) / Es.length;
  const maxRelDrift = Math.max(...Es.map((e) => Math.abs(e - mean) / mean));
  lossy.invariant.value = mean;
  lossy.drift.value = maxRelDrift;
  lossy.packet_hash = packetHash(lossy);
  const result = verifyBuildPacket(lossy);
  assert.equal(result.verdict, "DRIFT", "a lossy run whose energy drifts beyond tolerance is DRIFT");
  const fail = result.failures.find((f) => f.code === "drift_exceeds_tolerance");
  assert.ok(fail, "reports drift_exceeds_tolerance");
  assert.ok(fail.recomputed > fail.tolerance, "the recomputed drift exceeds the conservation tolerance");
}

// ---------------------------------------------------------------------------
// 8. Backend maturity outside the taxonomy -> DRIFT.
// ---------------------------------------------------------------------------
{
  const packet = assembleBuildPacket(happyFixture);
  const bad = clone(packet);
  bad.receipt.backend_maturity = "production_grade";
  bad.packet_hash = packetHash(bad);
  const result = verifyBuildPacket(bad);
  assert.equal(result.verdict, "DRIFT", "a backend maturity outside the taxonomy is DRIFT");
  const fail = result.failures.find(
    (f) => f.code === "state_model_violation" && f.path === "receipt.backend_maturity"
  );
  assert.ok(fail, "reports state_model_violation on backend_maturity");
  assert.equal(fail.observed, "production_grade", "names the offending value");
  assert.ok(Array.isArray(fail.allowed), "carries the allowed set");
}

// ---------------------------------------------------------------------------
// 9. Canned-verdict impossibility.
// ---------------------------------------------------------------------------
{
  const packet = assembleBuildPacket(happyFixture);
  const tampered = clone(packet);
  tampered.receipt.source_program = tampered.receipt.source_program + " // silently tampered";
  const result = verifyBuildPacket(tampered, { embeddedVerdict: "MATCH" });
  assert.equal(result.verdict, "DRIFT", "canned MATCH over tampered materials is DRIFT");
  const derivationFail = result.failures.find((f) => f.code === "embedded_verdict_not_derived");
  assert.ok(derivationFail, "reports embedded_verdict_not_derived");
  assert.equal(derivationFail.embedded, "MATCH", "records the dishonest embedded verdict");
  assert.equal(derivationFail.derived, "DRIFT", "records the derived verdict");

  // There is no code path that returns a literal MATCH: the verdict is folded
  // from the checks alone.
  const clean = verifyBuildPacket(packet, { embeddedVerdict: "MATCH" });
  assert.equal(clean.verdict, "MATCH", "truthful embedded MATCH over clean materials passes");
}

// ---------------------------------------------------------------------------
// 10. Every declared conformance negative case produces its declared code.
// ---------------------------------------------------------------------------
{
  const negativeCases = conventions.negative_test_cases;
  assert.ok(negativeCases.length >= 1, "conformance file declares negative cases");
  const declaredCodes = new Set(conventions.failure_codes);
  for (const c of negativeCases) {
    assert.ok(declaredCodes.has(c.failure_code), `negative case ${c.name} uses a declared code`);
  }

  // Drive each conformance-fixture mutation and assert its declared verdict/code.
  const cases = {
    tampered_source_program: (p) => {
      p.receipt.source_program = p.receipt.source_program + " // conformance tamper";
      return { rehash: false };
    },
    tampered_invariant_value: (p) => {
      p.invariant.value = p.invariant.value + 0.5;
      return { rehash: true };
    },
    missing_negative_fixture: (p) => {
      delete p.negative_fixture;
      return { rehash: true };
    },
    no_run_samples: (p) => {
      p.run.samples = [];
      return { rehash: true };
    },
    negative_control_conserved: (p) => {
      p.negative_fixture.samples = clone(happyFixture.run.samples);
      return { rehash: true };
    },
    boundary_condition_holds: (p) => {
      p.boundary_run.samples = clone(happyFixture.run.samples);
      return { rehash: true };
    },
    boundary_goal_broken: (p) => {
      p.boundary_run.samples = clone(happyFixture.negative_fixture.samples);
      return { rehash: true };
    },
    tolerance_exceeds_bound: (p) => {
      p.invariant.tolerance = p.invariant.value; // above the mean/100 ceiling
      return { rehash: true };
    },
    backend_maturity_outside_taxonomy: (p) => {
      p.receipt.backend_maturity = "not_a_real_maturity";
      return { rehash: true };
    }
  };
  for (const [name, mutate] of Object.entries(cases)) {
    const spec = conventions.conformance_fixture[name];
    assert.ok(spec, `conformance fixture declares ${name}`);
    // Assemble from a per-iteration deep clone so one case's mutation can never
    // leak into the shared happy fixture and corrupt a later case.
    const packet = assembleBuildPacket(clone(happyFixture));
    const { rehash } = mutate(packet);
    if (rehash) {
      packet.packet_hash = packetHash(packet);
    }
    const result = verifyBuildPacket(packet);
    assert.equal(result.verdict, spec.expected_verdict, `${name} verdict is ${spec.expected_verdict}`);
    const codes = result.failures.map((f) => f.code);
    assert.ok(
      codes.includes(spec.expected_failure_code),
      `${name} reports ${spec.expected_failure_code}; got ${JSON.stringify(codes)}`
    );
  }

  // The embedded-canned-match conformance case: a tampered program with an
  // embedded MATCH stays DRIFT.
  const cannedSpec = conventions.conformance_fixture.embedded_canned_match;
  const cannedPacket = assembleBuildPacket(happyFixture);
  cannedPacket.receipt.source_program = cannedPacket.receipt.source_program + " // canned";
  const cannedResult = verifyBuildPacket(cannedPacket, { embeddedVerdict: "MATCH" });
  assert.equal(cannedResult.verdict, cannedSpec.expected_verdict, "embedded_canned_match is DRIFT");
  assert.ok(
    cannedResult.failures.some((f) => f.code === cannedSpec.expected_failure_code),
    "embedded_canned_match reports embedded_verdict_not_derived"
  );
}

// ---------------------------------------------------------------------------
// 11. Packet-hash tamper is caught.
// ---------------------------------------------------------------------------
{
  const packet = assembleBuildPacket(happyFixture);
  const tampered = clone(packet);
  tampered.claim = "a silently swapped claim";
  // Do not re-hash: the recorded packet_hash no longer matches the materials.
  const result = verifyBuildPacket(tampered);
  assert.equal(result.verdict, "DRIFT", "a materials/hash mismatch is DRIFT");
  const fail = result.failures.find((f) => f.code === "packet_hash_mismatch");
  assert.ok(fail, "reports packet_hash_mismatch");
  assert.equal(fail.observed, packet.packet_hash, "carries the recorded hash");
  assert.notEqual(fail.expected, fail.observed, "the recomputed hash differs");
}

// ---------------------------------------------------------------------------
// 12. proof-surface conservation shape conformance (frozen field list).
// ---------------------------------------------------------------------------
{
  const packet = assembleBuildPacket(happyFixture);
  packet.verifier = verifyBuildPacket(packet);
  const exported = toProofSurfaceBuildPacket(packet);

  assert.deepEqual(
    Object.keys(exported).sort(),
    [...PROOF_SURFACE_ROOT_FIELDS].sort(),
    "export keys equal the frozen proof-surface root field list"
  );
  assert.equal(exported.version, "conservation-proof-packet/v0");
  assert.equal(exported.verdicts.overall, "MATCH");
  assert.ok(PROOF_SURFACE_OVERALL_VERDICTS.has(exported.verdicts.overall), "overall is a known verdict");

  // sources: bare 64-hex sha256.
  assert.ok(Array.isArray(exported.sources) && exported.sources.length >= 1, "at least one source");
  for (const source of exported.sources) {
    assert.match(source.sha256, /^[0-9a-f]{64}$/, "source sha256 is bare 64-hex");
    assert.ok(typeof source.ref === "string" && source.ref.length > 0, "source carries a ref");
    assert.deepEqual(Object.keys(source).sort(), ["ref", "sha256"], "source carries only ref and sha256");
  }

  // transformation: description and domain only.
  assert.deepEqual(
    Object.keys(exported.transformation).sort(),
    ["description", "domain"],
    "transformation carries only description and domain"
  );
  assert.equal(exported.transformation.domain, "scientific-compute", "domain is scientific-compute");
  // The backend label is honest: no maturity overclaim in the description.
  assert.ok(
    exported.transformation.description.includes("C verified backend"),
    "transformation labels the backend honestly"
  );

  // invariant: name and declared only.
  assert.deepEqual(
    Object.keys(exported.invariant).sort(),
    ["declared", "name"],
    "invariant carries only name and declared"
  );
  assert.equal(exported.invariant.name, happyFixture.invariant.name, "invariant name carries through");

  // witnesses: at least one, each with a valid kind, a non-negative drift, and a
  // positive tolerance, all re-derived from the samples.
  assert.ok(Array.isArray(exported.witnesses) && exported.witnesses.length >= 1, "at least one witness");
  for (const w of exported.witnesses) {
    assert.ok(PROOF_SURFACE_WITNESS_KINDS.has(w.kind), `witness kind ${w.kind} is valid`);
    assert.ok(typeof w.drift === "number" && w.drift >= 0, "witness drift is non-negative");
    assert.ok(typeof w.tolerance === "number" && w.tolerance > 0, "witness tolerance is positive");
    assert.ok(typeof w.method === "string" && w.method.length > 0, "witness names a method");
    assert.deepEqual(
      Object.keys(w).sort(),
      ["drift", "kind", "method", "tolerance"],
      "witness carries only the proof-surface witness fields"
    );
  }
  // The conservation witness drift equals the recomputed run drift.
  const conservationWitness = exported.witnesses.find((w) => /relative energy drift/.test(w.method));
  assert.ok(conservationWitness, "the export carries a conservation witness");
  assert.ok(
    Math.abs(conservationWitness.drift - happyFixture.drift.value) < 1e-9,
    "the conservation witness drift equals the recomputed run drift"
  );

  // negative_fixture: breaks the invariant, drift exceeds tolerance.
  assert.equal(exported.negative_fixture.breaks_invariant, true, "the negative fixture breaks the invariant");
  assert.ok(
    exported.negative_fixture.drift > exported.negative_fixture.tolerance,
    "the negative fixture drift exceeds its tolerance"
  );
  assert.deepEqual(
    Object.keys(exported.negative_fixture).sort(),
    ["breaks_invariant", "description", "drift", "tolerance"],
    "negative fixture carries only the proof-surface gate fields"
  );

  // boundary_fixture: the goal holds while the claimed condition fails.
  assert.ok(exported.boundary_fixture, "a boundary fixture is exported");
  assert.equal(exported.boundary_fixture.goal_holds, true, "the boundary fixture goal holds");
  assert.equal(exported.boundary_fixture.condition_holds, false, "the boundary fixture condition fails");
  assert.deepEqual(
    Object.keys(exported.boundary_fixture).sort(),
    ["condition_holds", "description", "goal_holds"],
    "boundary fixture carries only the proof-surface gate fields"
  );

  // verdicts: overall only.
  assert.deepEqual(Object.keys(exported.verdicts), ["overall"], "verdicts carries only overall");

  // decision_summary derives from the overall verdict.
  assert.equal(exported.decision_summary.decision, "approve", "MATCH derives approve");
  assert.equal(exported.decision_summary.confidence, "high", "MATCH derives high confidence");
  assert.ok(Array.isArray(exported.decision_summary.missing_evidence), "missing_evidence is an array");

  // failure_labels is a (possibly empty) list of proof-surface codes.
  assert.ok(Array.isArray(exported.failure_labels), "failure_labels is an array");
  for (const label of exported.failure_labels) {
    assert.ok(PROOF_SURFACE_FAILURE_CODES.has(label), `failure label ${label} is a proof-surface code`);
  }

  // uncertainty discloses at least the finite-run and fixture-receipt basis.
  assert.ok(Array.isArray(exported.uncertainty) && exported.uncertainty.length >= 1);

  // A DRIFT export derives a block decision and a binding_failed label.
  const drifted = clone(packet);
  drifted.invariant.value = happyFixture.invariant.value + 0.5;
  drifted.verifier = verifyBuildPacket(drifted, { embeddedVerdict: "MATCH" });
  const driftExport = toProofSurfaceBuildPacket(drifted);
  assert.equal(driftExport.verdicts.overall, "DRIFT", "tampered export is DRIFT");
  assert.equal(driftExport.decision_summary.decision, "block", "DRIFT derives block");
  assert.ok(driftExport.failure_labels.includes("binding_failed"), "DRIFT export labels binding_failed");
}

// ---------------------------------------------------------------------------
// 12b. A MATCH export satisfies the proof-surface negative-fixture and
// boundary-fixture gates, and the boundary-condition-holds and conserved-negative
// DRIFT exports are correctly flagged by those same gates. This asserts the core
// contract that closed the review holes: no MATCH is ever paired with an export
// that proof-surface would reject, because the verifier catches both the
// condition-holds boundary and the conserved negative control as DRIFT first.
// ---------------------------------------------------------------------------
{
  // The honest MATCH export passes both gates.
  const packet = assembleBuildPacket(happyFixture);
  const matchResult = verifyBuildPacket(packet);
  assert.equal(matchResult.verdict, "MATCH", "the happy-path packet verifies as MATCH");
  const matchExport = toProofSurfaceBuildPacket(packet);
  assert.deepEqual(
    proofSurfaceGateIssues(matchExport),
    [],
    "the MATCH export satisfies the proof-surface negative and boundary gates"
  );

  // The condition-holds boundary is DRIFT, so it is never exported as a MATCH; the
  // export it does produce (block) is the honestly-labeled DRIFT document, and the
  // gate flags the condition_holds:true it records.
  const conditionHolds = clone(packet);
  conditionHolds.boundary_run.samples = clone(happyFixture.run.samples);
  conditionHolds.packet_hash = packetHash(conditionHolds);
  const chResult = verifyBuildPacket(conditionHolds);
  assert.notEqual(chResult.verdict, "MATCH", "a condition-holds boundary never reaches MATCH");
  const chExport = toProofSurfaceBuildPacket(conditionHolds);
  assert.ok(
    proofSurfaceGateIssues(chExport).some((i) => i.includes("condition_holds")),
    "the condition-holds boundary export is flagged by the boundary gate, and it is a DRIFT/block document"
  );

  // A conserved negative control is DRIFT, so it is never a MATCH; the gate flags
  // the breaks_invariant:false it records, and the export is a block document.
  const conservedNeg = clone(packet);
  conservedNeg.negative_fixture.samples = clone(happyFixture.run.samples);
  conservedNeg.packet_hash = packetHash(conservedNeg);
  const cnResult = verifyBuildPacket(conservedNeg);
  assert.notEqual(cnResult.verdict, "MATCH", "a conserved negative control never reaches MATCH");
  const cnExport = toProofSurfaceBuildPacket(conservedNeg);
  assert.equal(cnExport.decision_summary.decision, "block", "the conserved-control export blocks, never approves");
  assert.ok(
    proofSurfaceGateIssues(cnExport).some((i) => i.includes("breaks_invariant")),
    "the conserved-control export is flagged by the negative gate, and it is a DRIFT/block document"
  );
}

// ---------------------------------------------------------------------------
// 12c. The assembler does not alias the fixture: mutating a nested field of an
// assembled packet can never corrupt the shared fixture for a later assembly.
// This is the robustness guard behind the deep clone in assembleBuildPacket.
// ---------------------------------------------------------------------------
{
  const shared = clone(happyFixture);
  const first = assembleBuildPacket(shared);
  // The assembled packet must not share references with the fixture.
  assert.notEqual(first.run, shared.run, "assembled run does not alias the fixture run");
  assert.notEqual(first.run.samples, shared.run.samples, "assembled samples do not alias the fixture samples");
  assert.notEqual(first.invariant, shared.invariant, "assembled invariant does not alias the fixture");
  assert.notEqual(first.negative_fixture, shared.negative_fixture, "assembled negative fixture does not alias the fixture");
  assert.notEqual(first.boundary_run, shared.boundary_run, "assembled boundary run does not alias the fixture");

  // Mutate the first packet in place, then assemble again from the same fixture.
  const originalLength = shared.run.samples.length;
  first.run.samples.length = 0;
  first.invariant.value = -12345;
  const second = assembleBuildPacket(shared);
  assert.equal(second.run.samples.length, originalLength, "a later assembly is unaffected by an earlier mutation");
  assert.notEqual(second.invariant.value, -12345, "the fixture invariant value was not corrupted");
  const secondResult = verifyBuildPacket(second);
  assert.equal(secondResult.verdict, "MATCH", "the later assembly still verifies as MATCH");
}

// ---------------------------------------------------------------------------
// 13. No secrets, no raw external payloads.
// ---------------------------------------------------------------------------
{
  const packet = assembleBuildPacket(happyFixture);
  const text = JSON.stringify(packet);
  assert.ok(
    !/[A-Za-z0-9_-]*(?:SECRET|PASSWORD|APIKEY|TOKEN)[A-Za-z0-9_-]*=/.test(text),
    "no secret assignments"
  );
  assert.ok(!/-----BEGIN [A-Z ]+PRIVATE KEY-----/.test(text), "no private key blocks");
  assert.ok(!/\bsk-[A-Za-z0-9]{20,}\b/.test(text), "no api-key-shaped tokens");
  assert.match(packet.receipt.source_digest, /^sha256:[a-f0-9]{64}$/, "receipt carries a source digest");
}

// ---------------------------------------------------------------------------
// 14. Em-dash and en-dash scan over the lane's new files.
// ---------------------------------------------------------------------------
{
  const emDash = String.fromCharCode(0x2014);
  const enDash = String.fromCharCode(0x2013);
  const laneFiles = [
    path.join(here, "proof-build.mjs"),
    path.join(here, "proof-build.test.mjs"),
    path.join(here, "integrations", "build-proof-packet-conventions.json")
  ];
  for (const file of laneFiles) {
    const bytes = readFileSync(file, "utf8");
    assert.ok(!bytes.includes(emDash), `${path.basename(file)} contains no em-dash`);
    assert.ok(!bytes.includes(enDash), `${path.basename(file)} contains no en-dash`);
  }
}

process.stdout.write("proof-build.test.mjs: all assertions passed\n");
